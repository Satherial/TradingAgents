<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Mantieni questi link. Le traduzioni si aggiorneranno automaticamente con il README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=en">English</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: Framework di Trading Finanziario Multi-Agent LLM

## Novità
- [2026-03] **TradingAgents v0.2.1** rilasciata con supporto per modelli GPT-5.4, Gemini 3.1, Claude 4.6 e stabilità del sistema migliorata.
- [2026-02] **TradingAgents v0.2.0** rilasciata con supporto multi-provider LLM (GPT-5.x, Gemini 3.x, Claude 4.x, Grok 4.x) e architettura di sistema migliorata.
- [2026-01] **Trading-R1** [Report Tecnico](https://arxiv.org/abs/2509.11420) rilasciato, con [Terminale](https://github.com/TauricResearch/Trading-R1) in arrivo presto.

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

> 🎉 **TradingAgents** ufficialmente rilasciato! Abbiamo ricevuto numerose richieste sul nostro lavoro e vorremmo esprimere il nostro ringraziamento per l'entusiasmo della nostra community.
>
> Così abbiamo deciso di rilasciare completamente il framework open-source. Non vediamo l'ora di costruire progetti impattanti con voi!

<div align="center">

🚀 [TradingAgents](#tradingagents-framework) | ⚡ [Installazione & CLI](#installazione-e-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Utilizzo Pacchetto](#utilizzo-del-pacchetto-tradingagents) | 🤝 [Contributi](#contributi) | 📄 [Citazione](#citazione)

</div>

## Framework TradingAgents

TradingAgents è un framework di trading multi-agent che replica le dinamiche delle società di trading reali. Impiegando agenti specializzati basati su LLM: da analisti fondamentali, esperti di sentiment e analisti tecnici, a trader e team di gestione del rischio, la piattaforma valuta collaborativamente le condizioni di mercato e informa le decisioni di trading. Inoltre, questi agenti si impegnano in discussioni dinamiche per individuare la strategia ottimale.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> Il framework TradingAgents è progettato per scopi di ricerca. Le performance di trading possono variare basandosi su molti fattori, inclusi i modelli linguistici scelti, la temperatura del modello, i periodi di trading, la qualità dei dati e altri fattori non deterministici. [Non è inteso come consiglio finanziario, di investimento o di trading.](https://tauric.ai/disclaimer/)

Il nostro framework decomprime compiti di trading complessi in ruoli specializzati. Questo assicura che il sistema raggiunga un approccio robusto e scalabile all'analisi di mercato e al processo decisionale.

### Team di Analisti
- **Analista Fondamentale**: Valuta i dati finanziari aziendali e le metriche di performance, identificando valori intrinseci e potenziali segnali di allarme.
- **Analista di Sentiment**: Analizza i social media e il sentimento pubblico utilizzando algoritmi di scoring del sentiment per valutare l'umore di mercato a breve termine.
- **Analista di News**: Monitora le notizie globali e gli indicatori macroeconomici, interpretando l'impatto degli eventi sulle condizioni di mercato.
- **Analista Tecnico**: Utilizza indicatori tecnici (come MACD e RSI) per rilevare pattern di trading e prevedere movimenti di prezzo.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Team di Ricercatori
- Comprende ricercatori sia rialzisti che ribassisti che valutano criticamente le intuizioni fornite dal Team di Analisti. Attraverso dibattiti strutturati, bilanciano potenziali guadagni contro rischi intrinseci.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Agente Trader
- Compone report da analisti e ricercatori per prendere decisioni di trading informate. Determina il tempismo e la magnitudine delle operazioni basandosi su intuizioni di mercato complete.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Gestione del Rischio e Portfolio Manager
- Valuta continuamente il rischio del portafoglio analizzando la volatilità di mercato, la liquidità e altri fattori di rischio. Il team di gestione del rischio valuta e aggiusta le strategie di trading, fornendo report di valutazione al Portfolio Manager per la decisione finale.
- Il Portfolio Manager approva/rifiuta la proposta di transazione. Se approvata, l'ordine verrà inviato all'exchange simulato ed eseguito.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installazione e CLI

### Installazione

Clona TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Crea un ambiente virtuale con qualsiasi dei tuoi gestori di ambiente preferiti:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Installa le dipendenze:
```bash
pip install -r requirements.txt
```

### API Richieste

TradingAgents supporta molteplici provider LLM. Imposta la chiave API per il tuo provider scelto:

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage (opzionale)
export FINNHUB_API_KEY=...         # Finnhub (opzionale)
```

**Per modelli locali**, configura Ollama con variabili d'ambiente:
```bash
export LLM_PROVIDER=ollama
export LLM_QUICK=llama3.1:8b
export LLM_DEEP=qwen3:14b
export OLLAMA_HOST=http://localhost:11434
```

**Fonti Dati:**
- **Default:** yfinance (gratuito, nessuna chiave API richiesta)
- **Opzionale:** Alpha Vantage o Finnhub per dati migliorati

In alternativa, copia `.env.example` in `.env` e inserisci le tue chiavi:
```bash
cp .env.example .env
```

### Utilizzo CLI

Puoi anche provare direttamente la CLI eseguendo:
```bash
python -m cli.main
```
Vedrai una schermata dove puoi selezionare i tuoi ticker desiderati, data, LLM, profondità di ricerca, ecc.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

Apparirà un'interfaccia che mostra i risultati mentre caricano, permettendoti di tracciare il progresso dell'agente mentre viene eseguito.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## Pacchetto TradingAgents

### Dettagli Implementazione

Abbiamo costruito TradingAgents con LangGraph per garantire flessibilità e modularità. Il framework supporta molteplici provider LLM: OpenAI, Google, Anthropic, xAI, OpenRouter e Ollama.

### Utilizzo Python

Per utilizzare TradingAgents nel tuo codice, puoi importare il modulo `tradingagents` e inizializzare un oggetto `TradingAgentsGraph()`. La funzione `.propagate()` restituirà una decisione. Puoi eseguire `main.py`, ecco anche un esempio rapido:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# propagazione in avanti
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

Puoi anche regolare la configurazione di default per impostare la tua scelta di LLM, round di dibattito, ecc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
config["deep_think_llm"] = "gpt-5.2"     # Modello per ragionamento complesso
config["quick_think_llm"] = "gpt-5-mini" # Modello per compiti rapidi
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

Vedi `tradingagents/default_config.py` per tutte le opzioni di configurazione.

## Flusso di Trading Automatizzato

Lo script `main.py` fornisce un flusso di lavoro di trading completamente automatizzato che combina la scoperta di ETF con analisi consapevole del portafoglio per trovare opportunità di investimento ottimali.

### Funzionalità

**Automazione Intelligente del Workflow:**
- Esegue automaticamente `scanner.py` se il file dei risultati è mancante
- Analisi sequenziale dei migliori candidati ETF fino alla prima raccomandazione BUY
- Analisi consapevole del portafoglio utilizzando le tue partecipazioni esistenti e strategia di investimento
- Si ferma al primo BUY per risparmiare tempo e risorse computazionali

**Integrazione Portfolio:**
- `portafolio.txt` - Elenca le tue partecipazioni attuali e l'esposizione settoriale
- `strategia.txt` - Definisci le tue regole di investimento, profilo di rischio e obiettivi
- Validazione del portfolio basata su LLM assicura coerenza
- Evita esposizione settoriale duplicata e si allinea con la tua strategia

**Analisi Intelligente:**
- Utilizza il sistema multi-agent TradingAgents per ogni candidato
- Round di dibattito Bull/Bear per decisione bilanciata
- Raccomandazioni consapevoli del contesto (BUY/HOLD/AVOID)
- Risultati salvati in `decisione_finale.txt`

### Framework Economico e Logica Decisionale

**Parametri di Investimento:**
- **Importo Flessibile**: Importo di investimento specificato in `strategia.txt` (es., €5.000)
- **Profilo di Rischio**: MODERATO default (approccio bilanciato crescita/rendimento)
- **Tipi di Decisione**: BUY / HOLD / AVOID con chiara ratio economica

**Principi Economici Fondamentali:**

**1. Teoria di Ottimizzazione del Portfolio**
- **Diversificazione**: Evita sovrapposizione settoriale (massimo 30% di esposizione per settore)
- **Analisi di Correlazione**: Penalizza ETF con >90% di correlazione con partecipazioni esistenti
- **Rendimenti Rettificati per il Rischio**: Utilizza il ratio di Sharpe per valutazione del rendimento per unità di rischio

**2. Framework di Sostenibilità dei Dividendi**
- **Analisi del Rendimento**: Rendimento da dividendo reale a 12 mesi vs. rendimento pubblicizzato
- **Scoring di Coerenza**: Affidabilità dei pagamenti (coerenza minima del 50% richiesta)
- **Ragionevolezza del Payout**: Valuta se le distribuzioni dei dividendi sono sostenibili
- **Trend di Crescita**: Analizza la crescita dei dividendi vs. pattern di riduzione

**3. Analisi di Trend e Timing di Mercato**
- **Valutazione del Momentum**: Momentum a 3 mesi per identificare trend attuali
- **Protezione dal Drawdown**: Soglia massima di drawdown del -25% per controllo del rischio
- **Filtro Performance**: Requisito minimo di rendimento totale del -5%

**4. Economia Computazionale**
- **Strategia First-BUY**: Si ferma alla prima raccomandazione BUY per ottimizzare i costi LLM
- **Analisi Sequenziale**: Processa i candidati per ranking del punteggio composito
- **Efficienza delle Risorse**: Bilancia profondità di analisi vs. spesa computazionale

**Matrice di Logica Decisionale:**
```
BUY = ✅ Coerenza portfolio + ✅ Dividendo sostenibile + ✅ Trend positivo + ✅ Rischio accettabile
HOLD = ⚠️ Fondamentali buoni ma ⚠️ Timing/punto di ingresso subottimale
AVOID = ❌ Fondamentali scarsi OPPURE ❌ Rischio eccessivo OPPURE ❌ Sovrapposizione portfolio
```

**Criteri di Validazione Investimento:**
1. **Coerenza Portfolio**: Nessuna duplicazione settoriale con partecipazioni esistenti
2. **Valore di Diversificazione**: Aggiunge esposizione geografica/settoriale nuova
3. **Sostenibilità dei Dividendi**: Ratio di payout ragionevole con storia stabile
4. **Qualità del Trend**: Trend rialzista genuino vs. rumore a breve termine
5. **Economia delle Unità**: Unità massime acquistabili basate sull'importo specificato dalla strategia

### Avvio Rapido

1. **Configura il tuo portfolio:**
```bash
# Copia e modifica i template
cp portfolio_example.txt portafolio.txt
cp strategia_example.txt strategia.txt

# Modifica con le tue partecipazioni e strategia effettive
```

2. **Imposta la configurazione LLM (.env):**
```bash
# Per modelli locali
LLM_PROVIDER=ollama
LLM_QUICK=llama3.1:8b
LLM_DEEP=qwen3:14b
OLLAMA_HOST=http://localhost:11434
```

3. **Esegui l'analisi automatizzata:**
```bash
python main.py
```

### Struttura File

```
├── main.py                    # Workflow di trading automatizzato
├── scanner.py                 # Scoperta e analisi ETF
├── portafolio.txt             # Le tue partecipazioni attuali (crea dal template)
├── strategia.txt              # La tua strategia di investimento (crea dal template)
├── portfolio_example.txt      # Template portfolio con esempi
├── strategia_example.txt      # Template strategia con esempi
├── scan_etf_risultati.csv     # Output scanner (auto-generato)
└── decisione_finale.txt       # Raccomandazione BUY finale (auto-generata)
```

### Processo Workflow

1. **Scoperta:** Esegue lo scanner per trovare candidati ETF a dividendo
2. **Validazione:** Controlla portafoglio.txt e strategia.txt con validazione LLM
3. **Analisi:** Testa ogni ETF con il sistema completo TradingAgents
4. **Selezione:** Si ferma alla prima raccomandazione BUY
5. **Output:** Salva analisi dettagliata e raccomandazione

### Flusso Implementazione Tecnica

**Esecuzione Passo-Passo:**

**Fase 1: Integrazione Scanner**
```python
# main.py controlla automaticamente scan_etf_risultati.csv
if not exists:
    subprocess.run(["python", "scanner.py"], timeout=600)  # 10 minuti max
```

**Fase 2: Validazione Portfolio**
```python
# Validazione basata su LLM utilizzando il modello quick
portfolio_content = validate_portfolio_with_llm(portfolio_raw)
# Assicura che il file contenga partecipazioni valide o "portfolio vuoto" esplicito
```

**Fase 3: Configurazione TradingAgents**
```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = LLM_PROVIDER  # ollama/openai/anthropic
config["deep_think_llm"] = LLM_DEEP      # qwen3:14b/gpt-5.2
config["quick_think_llm"] = LLM_QUICK    # llama3.1:8b/gpt-5-mini
config["max_debate_rounds"] = 2
config["system_prompt_prefix"] = build_system_prompt(portfolio, strategy)
```

**Fase 4: Loop Analisi Sequenziale**
```python
for ticker in watchlist:  # Top 10 ETF dallo scanner
    _, decision = ta.propagate(ticker, date)
    
    if is_buy_recommendation(decision):
        # Estrai motivazione e salva report completo
        etf_details = get_etf_details(ticker, name)
        save_decision_file(ticker, decision, etf_details)
        break  # Ottimizzazione First-BUY
```

**Fase 5: Generazione Output Decisionale**
- Estrae la motivazione chiave dalla risposta LLM
- Recupera dati completi ETF da yfinance
- Calcola le unità acquistabili con l'importo specificato dalla strategia
- Genera report strutturato in `decisione_finale.txt`

**Funzionalità Tecniche Chiave:**
- **Gestione Errori**: Continua al candidato successivo se l'analisi fallisce
- **Protezione Timeout**: Limite di 10 minuti per l'esecuzione dello scanner
- **Tracciamento Progresso**: Output in tempo reale del progresso dell'analisi
- **Validazione Dati**: Verifica la disponibilità dei dati ETF prima dell'analisi
- **Meccanismi Fallback**: Tentativi multipli di formato ticker (.MI, base)

**Pattern Integrazione LLM:**
```python
# Costruzione del system prompt
prompt = f"""Sei un consulente finanziario esperto che deve raccomandare 
UN SOLO investimento per un investitore italiano con profilo di rischio MODERATO.

Portfolio attuale: {portfolio}
Strategia: {strategy}
Domande da valutare: [diversification, sustainability, trend, units based on strategy amount, recommendation]
"""
```

### Personalizzazione

- **Profilo di Rischio:** Modifica `strategia.txt` per approccio conservativo/aggressivo
- **Preferenze Settoriali:** Definisci settori target nell'analisi del portfolio
- **Importo Investimento:** Modifica liquidità in strategia.txt
- **Modelli LLM:** Configura modelli quick/deep in .env

## Scanner ETF

Il modulo `scanner.py` fornisce uno strumento completo di scoperta e analisi ETF specificamente progettato per ETF a dividendo focalizzati sul reddito. Questo scanner prende di mira esclusivamente i migliori ETF che pagano dividendi ignorando sistematicamente tutti gli altri veicoli di investimento.

### Funzionalità Chiave

**Scoperta Focalizzata sui Dividendi:**
- Scarica elenchi completi ETF dal database justETF
- Filtra esclusivamente per ETF "Distributing" (che pagano dividendi)
- Elenca solo ETF quotati su Borsa Italiana con AUM ≥100M€
- Esclude ETF non distribuenti, ETF di crescita e fondi di accumulazione

**Pipeline di Analisi Completa:**
Per ogni candidato ETF a dividendo, il sistema calcola:

**Metriche dei Dividendi:**
- Rendimento reale basato su distribuzioni reali a 12 mesi
- Rendimento netto (rendimento meno costi TER)
- Punteggio di coerenza (affidabilità dei pagamenti)
- Trend di crescita dei dividendi (crescente vs. decrescente)

**Metriche Performance Finanziaria:**
- Rendimento Totale 1 anno (prezzo + dividendi)
- Ratio di Sharpe (rendimento per unità di rischio)
- Drawdown massimo (perdita temporanea peggiore)
- Momentum a 3 mesi

**Gestione del Rischio:**
- Analisi di correlazione del portfolio per evitare sovrapposizioni
- Filtri di esclusione rigidi per asset sottoperformanti
- Valutazione stabilità AUM

**Criteri di Selezione:**
Gli ETF vengono automaticamente esclusi se falliscono una qualsiasi di queste condizioni:
- Rendimento totale < -5% (performance negativa)
- Drawdown massimo < -25% (rischio eccessivo)
- Correlazione > 90% con portfolio esistente
- Punteggio di coerenza < 50% (pagamenti inaffidabili)
- Rendimento netto < 1% (dividendi insufficienti)

**Sistema di Punteggio Composito:**
Solo gli ETF che superano tutti i filtri ricevono un punteggio composito ponderato verso:
- **Rendimento Netto** (peso 2.5) - priorità massima
- **Rendimento Totale** (peso 1.5)
- **Ratio di Sharpe** (peso 2.0)
- **Coerenza Pagamenti** (peso 1.0)
- **Crescita Dividendi** (peso 1.0)
- **Penalità Correlazione** (peso 3.0) - evita sovrapposizione portfolio

### Utilizzo

```bash
python scanner.py
```

Lo scanner outputta i primi 15 ETF a dividendo classificati per punteggio composito, fornendo:
- Ticker e nome
- Prezzo attuale e metriche di rendimento
- Indicatori di rischio (Sharpe, drawdown, correlazione)
- Dati performance (rendimento totale, momentum)
- Punteggio composito per classificazione

I risultati vengono salvati in `scan_etf_risultati.csv` e una watchlist viene generata per l'integrazione con TradingAgents.

### Dipendenze

```bash
pip install justetf-scraping yfinance pandas numpy
```

## Testing

Il progetto include test unitari completi per funzionalità core:

```bash
# Esegui tutti i test
python -m pytest -v

# Esegui file di test specifici
python test_main.py          # Test workflow automatizzato (22 test)
python test_scanner.py       # Test scanner ETF (15 test)
```

**Copertura Test:**
- **main.py:** Integrazione scanner, validazione portfolio, comunicazione LLM
- **scanner.py:** Scoperta ETF, conversione ticker, analisi correlazione
- **Basati su Mock:** I test usano mock per API esterne e chiamate LLM

I test assicurano l'affidabilità del workflow automatizzato e dei componenti dello scanner.

## Contributi

Accogliamo contributi dalla community! Che si tratti di correggere un bug, migliorare la documentazione o suggerire una nuova funzionalità, il tuo input aiuta a rendere questo progetto migliore. Se sei interessato a questa linea di ricerca, considera di unirti alla nostra community di ricerca finanziaria AI open-source [Tauric Research](https://tauric.ai/).

## Citazione

Per favore, cita il nostro lavoro se trovi che *TradingAgents* ti fornisce qualche aiuto :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
