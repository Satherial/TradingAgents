"""
main.py - Flusso automatizzato di trading

1. Verifica/Crea scan_etf_risultati.csv via scanner.py
2. Analizza titoli uno per uno fino al primo BUY
3. Usa portfolio.txt e strategia.txt per contesto

Configurazione LLM via .env:
- LLM_PROVIDER=ollama
- LLM_QUICK=llama3.1:8b
- LLM_DEEP=qwen3:14b
- OLLAMA_HOST=http://localhost:11434
"""

import os
import sys
import subprocess
import pandas as pd
import requests
import json
from datetime import date
from dotenv import load_dotenv

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables
load_dotenv()

# Configurazione LLM da .env
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_QUICK = os.getenv("LLM_QUICK", "llama3.1:8b")
LLM_DEEP = os.getenv("LLM_DEEP", "qwen3:14b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

SCAN_RESULTS_FILE = "scan_etf_risultati.csv"
PORTFOLIO_FILE = "portafolio.txt"
STRATEGY_FILE = "strategia.txt"


def check_and_run_scanner():
    """Verifica se esiste il file scan, altrimenti lancia scanner.py"""
    if os.path.exists(SCAN_RESULTS_FILE):
        print(f"✅ Trovato {SCAN_RESULTS_FILE}")
        return True
    
    print(f"⚠️  {SCAN_RESULTS_FILE} non trovato. Avvio scanner.py...")
    print("   (questo potrebbe richiedere diversi minuti)")
    
    try:
        result = subprocess.run(
            [sys.executable, "scanner.py"],
            capture_output=True,
            text=True,
            timeout=600  # 10 minuti max
        )
        
        if result.returncode == 0:
            print(f"✅ Scanner completato con successo")
            return True
        else:
            print(f"❌ Scanner fallito:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Scanner timeout (10 minuti)")
        return False
    except Exception as e:
        print(f"❌ Errore avviando scanner: {e}")
        return False


def validate_portfolio_with_llm(content: str) -> tuple[bool, str]:
    """
    Usa il modello quick per validare se il file contiene un portfolio valido
    o se indica esplicitamente che il portfolio è vuoto.
    
    Returns: (is_valid, parsed_content)
    """
    prompt = f"""Analizza il seguente contenuto del file portfolio.

CONTENUTO:
{content}

Rispondi in italiano:
1. Questo file contiene un elenco di titoli posseduti? (si/no)
2. Oppure indica esplicitamente che il portfolio è vuoto? (si/no)
3. Estrai l'elenco dei titoli posseduti (se presente)

Rispondi SOLO in formato JSON:
{{
  "has_portfolio": true/false,
  "is_empty": true/false,
  "tickers": ["TICKER1", "TICKER2"] o [],
  "summary": "descrizione breve del contenuto"
}}"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": LLM_QUICK,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=30
        )
        
        result = response.json()["response"]
        # Estrai JSON dalla risposta
        json_start = result.find("{")
        json_end = result.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            parsed = json.loads(result[json_start:json_end])
            is_valid = parsed.get("has_portfolio", False) or parsed.get("is_empty", False)
            return is_valid, parsed.get("summary", content)
        
        return True, content  # Fallback: accetta il contenuto così com'è
        
    except Exception as e:
        print(f"⚠️  Errore validazione LLM: {e}")
        return True, content  # Fallback: accetta il contenuto


def load_portfolio_and_strategy() -> tuple[str, str]:
    """Carica portfolio e strategia dai file, con validazione"""
    
    # Check portfolio
    if not os.path.exists(PORTFOLIO_FILE):
        print(f"❌ File {PORTFOLIO_FILE} non trovato!")
        print(f"   Crea il file basandoti su portfolio_example.txt")
        sys.exit(1)
    
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        portfolio_raw = f.read()
    
    print("🔍 Validazione portfolio con LLM...")
    is_valid, portfolio_content = validate_portfolio_with_llm(portfolio_raw)
    
    if not is_valid:
        print(f"❌ Il file {PORTFOLIO_FILE} non contiene un portfolio valido!")
        print(f"   Deve contenere l'elenco dei titoli posseduti o indicare 'portfolio vuoto'")
        sys.exit(1)
    
    print("✅ Portfolio validato")
    
    # Load strategy (optional)
    strategy_content = ""
    if os.path.exists(STRATEGY_FILE):
        with open(STRATEGY_FILE, "r", encoding="utf-8") as f:
            strategy_content = f.read()
        print("✅ Strategia caricata")
    else:
        print(f"⚠️  {STRATEGY_FILE} non trovato, uso strategia di default")
    
    return portfolio_content, strategy_content


def build_system_prompt(portfolio: str, strategy: str) -> str:
    """Costruisce il system prompt per l'analisi"""
    
    base_prompt = f"""Sei un consulente finanziario esperto che deve raccomandare UN SOLO investimento da 5.000€ per un investitore italiano con profilo di rischio MODERATO.

Stai aiutando un investitore italiano a decidere SE ACQUISTARE questo titolo.
L'investitore NON possiede ancora questo titolo e ha 5.000€ da investire.

La raccomandazione finale deve essere UNA di queste tre:
- BUY = ACQUISTA questo titolo (buon momento per nuovo investimento)
- HOLD = NON ACQUISTARE ORA (aspetta momento migliore, titolo interessante ma non ora)
- AVOID/EVITA = NON ACQUISTARE (condizioni sfavorevoli, evitare questo titolo)

IMPORTANTE: Questo titolo NON è ancora nel portafoglio. Stai consigliando SE aggiungerlo.

PORTFOLIO ATTUALE DELL'INVESTITORE:
{portfolio}
"""
    
    if strategy.strip():
        base_prompt += f"""
STRATEGIA DELL'INVESTITORE:
{strategy}
"""
    
    base_prompt += """
Per il titolo che stai analizzando, rispondi a:
1. È coerente con il portafoglio (non duplica settori già saturi)?
2. Aggiunge diversificazione reale?
3. Il dividendo è sostenibile (payout ragionevole, storia stabile)?
4. Il trend è davvero positivo o è rumore di breve periodo?
5. Quante unità si possono comprare con 5.000€?
6. Raccomandazione finale: BUY / HOLD / AVOID — con motivazione chiara in italiano.

Usa AVOID (o EVITA) quando il titolo NON va acquistato.
"""
    
    return base_prompt


def is_buy_recommendation(decision: str) -> bool:
    """Verifica se la decisione contiene una raccomandazione BUY"""
    decision_upper = decision.upper()
    return "BUY" in decision_upper or "ACQUISTARE" in decision_upper


def main():
    print("=" * 60)
    print("🤖 TRADINGAGENTS - Flusso Automatizzato")
    print("=" * 60)
    
    # Step 1: Verifica/Crea scan results
    if not check_and_run_scanner():
        print("❌ Impossibile ottenere i risultati dello scanner")
        sys.exit(1)
    
    # Step 2: Carica watchlist
    try:
        df_scan = pd.read_csv(SCAN_RESULTS_FILE, encoding="utf-8-sig", index_col=0)
        watchlist = df_scan.head(10)["Ticker"].tolist()
        etf_names = df_scan.head(10).set_index("Ticker")["Nome"].to_dict()
        print(f"📊 Watchlist caricata: {len(watchlist)} titoli")
        print(f"   Primi 5: {watchlist[:5]}")
    except Exception as e:
        print(f"❌ Errore caricando watchlist: {e}")
        sys.exit(1)
    
    # Step 3: Carica portfolio e strategia
    portfolio, strategy = load_portfolio_and_strategy()
    
    # Step 4: Configura TradingAgents
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = LLM_PROVIDER
    config["deep_think_llm"] = LLM_DEEP
    config["quick_think_llm"] = LLM_QUICK
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    config["system_prompt_prefix"] = build_system_prompt(portfolio, strategy)
    
    # Configura data vendors
    config["data_vendors"] = {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    }
    
    print(f"\n⚙️  Configurazione LLM:")
    print(f"   Provider: {LLM_PROVIDER}")
    print(f"   Quick: {LLM_QUICK}")
    print(f"   Deep: {LLM_DEEP}")
    
    # Step 5: Analisi sequenziale
    ta = TradingAgentsGraph(debug=True, config=config)
    oggi = date.today().strftime("%Y-%m-%d")
    
    print(f"\n🚀 Inizio analisi sequenziale ({oggi})...")
    print("=" * 60)
    
    for i, ticker in enumerate(watchlist, 1):
        etf_name = etf_names.get(ticker, ticker)
        print(f"\n[{i}/{len(watchlist)}] 🔍 Analisi {ticker} - {etf_name}...")
        print("-" * 40)
        
        try:
            _, decision = ta.propagate(ticker, oggi)
            print(f"\n📊 RISULTATO per {ticker}:")
            print(decision)
            
            # Verifica se è un BUY
            if is_buy_recommendation(decision):
                print("\n" + "=" * 60)
                print(f"🎯 TROVATO BUY: {ticker}")
                print("=" * 60)
                print(f"\n✅ Raccomandazione finale: ACQUISTA {ticker}")
                
                # Salva risultato completo
                with open("decisione_finale.txt", "w", encoding="utf-8") as f:
                    f.write(f"DECISIONE FINALE - {oggi}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"🎯 TITOLARE SELEZIONATO: {ticker} - {etf_name}\n")
                    f.write(f"📊 RACCOMANDAZIONE: BUY (ACQUISTA)\n\n")
                    f.write("=" * 60 + "\n")
                    f.write("📋 RIEPILOGO DECISIONE\n")
                    f.write("=" * 60 + "\n\n")
                    f.write("✅ Motivazione principale: Buon momento per acquistare\n")
                    f.write("✅ Analisi completa del TradingAgents multi-agent system\n")
                    f.write("✅ Valutazione basata su portafoglio e strategia personalizzati\n\n")
                    f.write("=" * 60 + "\n")
                    f.write("🔍 ANALISI DETTAGLIATA\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(decision)
                    f.write(f"\n\n" + "=" * 60 + "\n")
                    f.write("📊 INFORMAZIONI AGGIUNTIVE\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Data analisi: {oggi}\n")
                    f.write(f"Ticker: {ticker}\n")
                    f.write(f"Nome ETF: {etf_name}\n")
                    f.write(f"Raccomandazione: BUY (ACQUISTA ORA)\n")
                    f.write(f"Profilo rischio: MODERATO\n")
                    f.write(f"Importo suggerito: 5.000€\n")
                    f.write(f"Fonte dati: yfinance + TradingAgents analysis\n\n")
                    f.write("⚠️  NOTA: Questa è una raccomandazione generata da AI.\n")
                    f.write("      Fai sempre le tue verifiche prima di investire.\n")
                
                print(f"\n💾 Decisione salvata in: decisione_finale.txt")
                return  # Termina al primo BUY
            
            print(f"\n⏭️  {ticker}: non è un BUY, passo al prossimo...")
            
        except Exception as e:
            print(f"❌ Errore analizzando {ticker}: {e}")
            continue
    
    # Se arriviamo qui, nessun BUY trovato
    print("\n" + "=" * 60)
    print("⚠️  NESSUN BUY TROVATO")
    print("=" * 60)
    print("Analizzati tutti i titoli della watchlist, nessuno ha")
    print("generato una raccomandazione BUY.")


if __name__ == "__main__":
    main()
