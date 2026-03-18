# Test Unitari per scanner.py

Questo documento descrive la suite di test unitari creata per verificare il funzionamento corretto dello scanner ETF.

## Struttura dei Test

### File Principali
- `test_scanner.py` - Suite completa di test unitari
- `requirements-test.txt` - Dipendenze per i test

### Classi di Test

#### `TestETFScanner`
Test delle funzioni principali di scanning e analisi:

1. **`test_is_etf_duplicato`** - Verifica il rilevamento di ETF duplicati
2. **`test_get_etf_fallback`** - Test della lista fallback di ETF
3. **`test_ticker_to_yahoo_ticker_*`** - Test conversione ticker Yahoo Finance
4. **`test_calcola_yield_reale`** - Test calcolo yield da dividendi reali
5. **`test_get_portfolio_returns`** - Test caricamento rendimenti portafoglio
6. **`test_calculate_max_correlation`** - Test calcolo correlazione massima
7. **`test_analizza_etf_*`** - Test analisi completa ETF (successi, fallimenti, filtri)
8. **`test_main_workflow`** - Test del workflow principale

#### `TestConfigConstants`
Test delle costanti di configurazione:

1. **`test_filter_constants`** - Verifica valori dei filtri
2. **`test_portfolio_constants`** - Verifica configurazione portafoglio

## Esecuzione dei Test

### Installazione Dipendenze
```bash
python -m pip install -r requirements-test.txt
```

### Esecuzione Completa
```bash
python -m pytest test_scanner.py -v
```

### Esecuzione Singolo Test
```bash
python -m pytest test_scanner.py::TestETFScanner::test_analizza_etf_success -v
```

### Coverage Report
```bash
python -m pytest test_scanner.py --cov=scanner --cov-report=html
```

## Casi di Test Coperti

### ✅ Funzionalità Testate
- Rilevamento duplicati ETF
- Conversione ticker Yahoo Finance (.MI, base, fallback)
- Calcolo yield reali da dividendi storici
- Caricamento dati portafoglio esistente
- Calcolo correlazioni con portafoglio
- Analisi completa ETF con filtri hard discard
- Workflow end-to-end
- Costanti di configurazione

### 🧪 Mock Utilizzati
- `yf.Ticker` per dati Yahoo Finance
- `justetf_scraping` per dati justETF
- Dati storici pandas con indici temporali realistici
- Portfolio returns con >= 30 giorni di dati

### 📊 Filtri Verificati
- Net Yield ≥ 1.0%
- Total Return 1y ≥ -5.0%
- Max Drawdown ≥ -25.0%
- Max Correlation ≤ 0.90
- Consistency ≥ 0.5
- AUM minimo
- Esclusione duplicati

## Risultati Attesi

 Tutti i 15 test dovrebbero passare con successo:
```
============================= test session starts ==============================
collected 15 items

test_scanner.py::TestETFScanner::test_is_etf_duplicato PASSED
test_scanner.py::TestETFScanner::test_get_etf_fallback PASSED
...
============================= 15 passed in X.XXs ===============================
```

## Troubleshooting

### Errori Comuni
1. **ImportError** - Installare le dipendenze con `pip install -r requirements-test.txt`
2. **DateError** - Verificare compatibilità pandas (usare 'ME' invece di 'M')
3. **MockError** - Assicurarsi che i mock abbiano dati sufficienti (≥ 30 giorni per correlazione, ≥ 50 giorni per analisi ETF)

### Debug
Per debug dettagliato, eseguire con:
```bash
python -m pytest test_scanner.py -v -s --tb=long
```

## Manutenzione

### Aggiungere Nuovi Test
1. Creare metodo `test_*` nella classe appropriata
2. Usare mock per dipendenze esterne
3. Verificare casi limite e edge cases
4. Aggiornare questo README

### Aggiornare Test Esistenti
Quando si modifica `scanner.py`:
1. Eseguire tutti i test
2. Aggiornare i mock se necessario
3. Verificare coverage delle nuove funzionalità
4. Documentare nuovi casi di test

## Best Practices

- ✅ Usare mock per tutte le dipendenze esterne (API, database)
- ✅ Testare sia casi positivi che negativi
- ✅ Verificare filtri e condizioni di errore
- ✅ Usare dati realistici con indici temporali corretti
- ✅ Mantenere i test indipendenti l'uno dall'altro
- ✅ Documentare casi di test non ovvi
