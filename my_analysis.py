# my_analysis.py
# Lancia: python my_analysis.py

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from datetime import date
import requests
import json

# -------------------------------------------------------
# WATCHLIST — incolla qui l'output di scanner.py
# (oppure mettila a mano se vuoi testare titoli specifici)
# -------------------------------------------------------
WATCHLIST = []  # ← verrà popolata automaticamente da scan_risultati.csv

# Se scan_etf_risultati.csv esiste, carica la watchlist da lì
import os, pandas as pd
if os.path.exists("scan_etf_risultati.csv"):
    df_scan = pd.read_csv("scan_etf_risultati.csv", encoding="utf-8-sig", index_col=0)
    # Escludi quelli con settore già saturo
    # df_scan = df_scan[~df_scan["Settore"].str.startswith("⚠️", na=False)]
    WATCHLIST = df_scan.head(10)["Ticker"].tolist()
    print(f"📂 Watchlist caricata da scan_etf_risultati.csv: {WATCHLIST}\n")
else:
    # Fallback manuale se lo scanner non è stato ancora eseguito
    WATCHLIST = ['BPSO.MI', 'IG.MI', 'VAPX.MI', 'SPM.MI', 'AZM.MI', 'BAMI.MI', 'BMED.MI', 'ISP.MI', 'UCG.MI', 'UNI.MI', 'TDIV.MI', 'SRG.MI', 'TEN.MI', 'VHYL.MI', 'IDVY.MI']
    print(f"📋 Watchlist manuale: {WATCHLIST}\n")

# -------------------------------------------------------
# PORTAFOGLIO
# -------------------------------------------------------
with open("portafolio.txt", "r", encoding="utf-8") as f:
    portfolio_context = f.read()

portfolio_prompt = f"""
Sei un consulente finanziario esperto che deve raccomandare UN SOLO investimento
da 5.000€ per un investitore italiano con profilo di rischio MODERATO.

Stai aiutando un investitore italiano a decidere SE ACQUISTARE questo titolo.
L'investitore NON possiede ancora questo titolo e ha 5.000€ da investire.

La raccomandazione deve essere interpretata come:
- BUY = buon momento per acquistare adesso
- HOLD = aspetta un momento migliore per acquistare  
- SELL = non acquistare, condizioni sfavorevoli

Analizza il titolo considerando SEMPRE il portafoglio attuale dell'investitore:

{portfolio_context}

Per il titolo che stai analizzando, rispondi a:
1. È coerente con il portafoglio (non duplica settori già saturi)?
2. Aggiunge diversificazione reale?
3. Il dividendo è sostenibile (payout ragionevole, storia stabile)?
4. Il trend è davvero positivo o è rumore di breve periodo?
5. Quante unità si possono comprare con 5.000€?
6. BUY / HOLD / SELL — con motivazione chiara in italiano.
"""

# -------------------------------------------------------
# CONFIGURAZIONE TRADINGAGENTS
# -------------------------------------------------------
config = DEFAULT_CONFIG.copy()
config["llm_provider"]         = "ollama"
config["deep_think_llm"]       = "qwen3:14b"
config["quick_think_llm"]      = "llama3.1:8b"
config["max_debate_rounds"]    = 1      # 1 = veloce, 2 = più accurato
config["online_tools"]         = True
config["system_prompt_prefix"] = portfolio_prompt

ta   = TradingAgentsGraph(debug=False, config=config)
oggi = date.today().strftime("%Y-%m-%d")

# -------------------------------------------------------
# ANALISI SEQUENZIALE + COMPARATORE FINALE
# -------------------------------------------------------
risultati = {}

print("=" * 60)
print(f"📊 ANALISI MULTI-TITOLO — {oggi}")
print(f"   Modello: qwen3:14b (deep) + llama3.1:8b (quick)")
print("=" * 60 + "\n")

for i, ticker in enumerate(WATCHLIST, 1):
    print(f"[{i}/{len(WATCHLIST)}] 🔍 Analisi {ticker}...")
    try:
        _, decision = ta.propagate(ticker, oggi)
        risultati[ticker] = decision
        print(f"   ✅ {ticker}: {str(decision)[:80]}...\n")
    except Exception as e:
        print(f"   ❌ {ticker}: errore — {e}\n")
        risultati[ticker] = f"ERRORE: {e}"

# -------------------------------------------------------
# AGENTE COMPARATORE FINALE
# -------------------------------------------------------
print("\n" + "=" * 60)
print("🤖 COMPARATORE FINALE — scelgo il miglior investimento...")
print("=" * 60 + "\n")

confronto_prompt = f"""
Sei un consulente finanziario esperto. Hai analizzato i seguenti titoli
per un investitore italiano con 5.000€ da investire.

PORTAFOGLIO ATTUALE:
{portfolio_context}

RISULTATI DELLE ANALISI:
{json.dumps(risultati, ensure_ascii=False, indent=2)}

In base a tutto questo, fornisci in italiano:

## 🏆 RACCOMANDAZIONE FINALE

**Titolo consigliato:** [nome e ticker]
**Motivazione:** [perché è il migliore rispetto agli altri]
**Coerenza col portafoglio:** [come si integra con le posizioni esistenti]
**Quante unità comprare con 5.000€:** [calcolo]
**Rischi principali:** [cosa tenere d'occhio]

## 📊 RANKING COMPLETO
[classifica tutti i titoli analizzati dal migliore al peggiore con una riga di commento]

Sii diretto e pratico. Evita disclaimer generici.
"""

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:14b",
            "prompt": confronto_prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        },
        timeout=300
    )
    sintesi = response.json()["response"]
except Exception as e:
    sintesi = f"Errore nel comparatore: {e}"

print(sintesi)

# Salva il report completo
with open("report_investimento.txt", "w", encoding="utf-8") as f:
    f.write(f"REPORT INVESTIMENTO — {oggi}\n")
    f.write("=" * 60 + "\n\n")
    f.write("ANALISI SINGOLI TITOLI:\n")
    for ticker, dec in risultati.items():
        f.write(f"\n{ticker}:\n{dec}\n")
    f.write("\n" + "=" * 60 + "\n")
    f.write("RACCOMANDAZIONE FINALE:\n\n")
    f.write(sintesi)

print(f"\n💾 Report completo salvato in: report_investimento.txt")