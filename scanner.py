# scanner.py
# pip install justetf-scraping yfinance pandas numpy

import yfinance as yf
import pandas as pd
import numpy as np
import justetf_scraping
import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------
# PARAMETRI FILTRO
# -------------------------------------------------------
ETF_YIELD_MIN       = 1.5    # % minimo yield (da distribuzioni reali)
ETF_YIELD_MAX       = 15.0   # % massimo (sopra = dato anomalo)
AUM_MIN             = 100_000_000   # 100M€ AUM minimo (stabilità)
TOP_N               = 15

# -------------------------------------------------------
# PORTAFOGLIO ESISTENTE - per calcolo correlazione
# -------------------------------------------------------
PORTFOLIO_ETFS = {
    "EXSA.MI": "iShares STOXX Euro 600",
    "IMEU.MI": "iShares Core MSCI EU", 
    "XDWD.MI": "Xtrackers Portfolio Income",
    "XDEB.MI": "Xtrackers Portfolio"
}

# -------------------------------------------------------
# PORTAFOGLIO — ETF già presenti (escludi duplicati)
# -------------------------------------------------------
ETF_GIA_PRESENTI_KEYWORDS = [
    "stoxx euro 600", "msci eu", "xtrackers portfolio income",
    "xtrackers portfolio", "xtr ptf"
]

def is_etf_duplicato(nome: str) -> bool:
    nome_lower = nome.lower()
    return any(k in nome_lower for k in ETF_GIA_PRESENTI_KEYWORDS)


# -------------------------------------------------------
# STEP 1 — Discovery completa da justETF
# Scarica TUTTI gli ETF distributing quotati su Borsa Italiana
# -------------------------------------------------------
def get_etf_da_justetf() -> list[tuple[str, str, float]]:
    """
    Restituisce lista di (isin, nome, aum) per ETF distributing
    quotati su Borsa Italiana con AUM sufficiente.
    """
    print("Scarico lista completa ETF da justETF...")
    print("   (solo distributing, quotati a Milano — può richiedere 30-60s)\n")

    try:
        # Carica overview di tutti gli ETF long-only con enrich per ISIN e exchange
        df = justetf_scraping.load_overview(strategy="epg-longOnly", enrich=True)

        print(f"   Totale ETF trovati da justETF: {len(df)}")

        # Filtro 1: solo distributing
        if "dividends" in df.columns:
            df = df[df["dividends"] == "Distributing"]
        print(f"   Dopo filtro distributing: {len(df)}")

        # Filtro 2: solo quotati su Borsa Italiana
        if "exchange" in df.columns:
            df = df[df["exchange"].astype(str).str.contains("Borsa Italiana", case=False, na=False)]
        print(f"   Dopo filtro Borsa Italiana: {len(df)}")

        # Filtro 3: AUM minimo
        aum_col = "size" if "size" in df.columns else None

        if aum_col:
            df[aum_col] = pd.to_numeric(df[aum_col], errors="coerce").fillna(0)
            # justETF a volte usa milioni come unità
            if df[aum_col].median() < 10000:
                # valori in milioni → converti in unità
                df = df[df[aum_col] >= AUM_MIN / 1_000_000]
            else:
                df = df[df[aum_col] >= AUM_MIN]
            print(f"   Dopo filtro AUM ≥{AUM_MIN//1e6:.0f}M€: {len(df)}")

        # Estrai colonne utili
        ticker_col = "ticker" if "ticker" in df.columns else df.columns[1]  # ticker è seconda colonna
        nome_col = "name" if "name" in df.columns else "shortName"
        aum_val  = df[aum_col] if aum_col else pd.Series([0]*len(df))

        risultato = []
        for _, row in df.iterrows():
            ticker = str(row.get(ticker_col, "")).strip()
            nome = str(row.get(nome_col, ticker)).strip()
            aum  = float(row.get(aum_col, 0)) if aum_col else 0
            if ticker:  # Usa ticker invece di ISIN
                risultato.append((ticker, nome, aum))

        print(f"\n   {len(risultato)} ETF candidati trovati\n")
        return risultato

    except Exception as e:
        print(f"   Errore justETF: {e}")
        print("   Uso lista fallback...\n")
        return get_etf_fallback()


def get_etf_fallback() -> list[tuple[str, str, float]]:
    """Lista minima di fallback con ticker verificati se justETF non risponde."""
    return [
        ("VUSA", "Vanguard All-World High Div",      11_000_000_000),
        ("VWRA", "Vanguard All-World Dist",           5_000_000_000),
        ("IWDA", "iShares MSCI World Dist",           3_000_000_000),
        ("SX5E", "iShares Euro Stoxx 50",             5_000_000_000),
        ("DLVP", "VanEck Dividend Leaders",           2_000_000_000),
        ("CS51", "iShares Core Euro Stoxx 50",        8_000_000_000),
        ("IWDA", "iShares Core MSCI World",          30_000_000_000),
        ("VWRA", "Vanguard Dev Europe Dist",          3_000_000_000),
        ("SX5E", "iShares Euro Dividend",             1_000_000_000),
        ("IDVY", "iShares STOXX Global Select Div",  2_000_000_000),
    ]


# -------------------------------------------------------
# STEP 2 — Converti ticker justETF in ticker Yahoo Finance .MI
# -------------------------------------------------------
def ticker_to_yahoo_ticker(ticker: str) -> str | None:
    """
    Converte il ticker justETF in ticker Yahoo Finance.
    Usa ricerca più robusta con fallback multipli.
    """
    try:
        # 1. Prova prima con suffisso .MI per Borsa Italiana
        ticker_mi = f"{ticker}.MI"
        test = yf.Ticker(ticker_mi)
        if test.info and test.info.get('regularMarketPrice'):
            return ticker_mi
        
        # 2. Prova il ticker base
        test_base = yf.Ticker(ticker)
        if test_base.info and test_base.info.get('regularMarketPrice'):
            return ticker
            
        # 3. Ricerca avanzata per nome simile
        try:
            risultati = yf.Search(ticker, max_results=10).quotes
            for r in risultati:
                symbol = r.get("symbol", "")
                shortname = r.get("shortname", "").lower()
                
                # Priorità alta per .MI
                if symbol.endswith(".MI"):
                    return symbol
                
                # Priorità media per ticker simili
                if ticker.lower() in symbol.lower():
                    return symbol
                    
                # Priorità bassa per nomi simili (solo se contengono ETF/UCITS)
                if "etf" in shortname or "ucits" in shortname:
                    if symbol.endswith((".PA", ".DE", ".L", ".AS", ".SW")):
                        return symbol
        except:
            pass
            
        return None
    except Exception:
        return None


# -------------------------------------------------------
# STEP 3 — Analisi storico 12 mesi via yfinance
# -------------------------------------------------------
def calcola_yield_reale(ticker_obj, prezzo: float) -> float:
    try:
        dividendi = ticker_obj.dividends
        if dividendi.empty or prezzo == 0:
            return 0.0
        un_anno_fa = pd.Timestamp.now(tz="UTC") - pd.DateOffset(years=1)
        dist_annua = dividendi[dividendi.index >= un_anno_fa].sum()
        return round((dist_annua / prezzo) * 100, 2)
    except Exception:
        return 0.0


def get_portfolio_returns() -> dict[str, pd.Series]:
    """
    Scarica i rendimenti giornalieri degli ETF già in portafoglio
    per il calcolo della correlazione.
    """
    portfolio_returns = {}
    
    for ticker, name in PORTFOLIO_ETFS.items():
        try:
            t = yf.Ticker(ticker)
            storico = t.history(period="1y")
            if not storico.empty and len(storico) > 50:
                returns = storico["Close"].pct_change().dropna()
                portfolio_returns[ticker] = returns
                print(f"   Caricato {ticker} ({name}): {len(returns)} giorni")
            else:
                print(f"   Dati insufficienti per {ticker}")
        except Exception as e:
            print(f"   Errore caricando {ticker}: {e}")
    
    return portfolio_returns


def calculate_max_correlation(candidate_returns: pd.Series, portfolio_returns: dict[str, pd.Series]) -> float:
    """
    Calcola la correlazione massima con gli ETF del portafoglio.
    """
    max_corr = 0.0
    
    for port_ticker, port_returns in portfolio_returns.items():
        try:
            # Allinea le date e calcola correlazione
            common_dates = candidate_returns.index.intersection(port_returns.index)
            if len(common_dates) > 30:  # Minimo 30 giorni di dati sovrapposti
                cand_aligned = candidate_returns.loc[common_dates]
                port_aligned = port_returns.loc[common_dates]
                
                correlation = abs(cand_aligned.corr(port_aligned))
                max_corr = max(max_corr, correlation)
        except Exception:
            continue
    
    return max_corr


def analizza_etf(ticker: str, nome_noto: str, aum: float, portfolio_returns: dict[str, pd.Series]) -> dict | None:
    try:
        t    = yf.Ticker(ticker)
        info = t.info
        storico = t.history(period="1y")
        
        # Verifica dati minimi
        if storico.empty or len(storico) < 50:
            return None
            
        prezzi = storico["Close"]
        dividendi = t.dividends
        
        nome   = (info.get("shortName") or nome_noto or ticker)[:40]
        prezzo = (info.get("currentPrice") or
                  info.get("regularMarketPrice") or
                  info.get("navPrice") or prezzi.iloc[-1])

        if prezzo == 0:
            return None

        # -------------------------------------------------------
        # NUOVO: Validazione ISIN e Mercato
        # -------------------------------------------------------
        isin = info.get("isin", "")
        exchange = info.get("exchange", "")
        currency = info.get("currency", "USD")
        market = "EU" if exchange in ["Borsa Italiana", "XETRA", "Euronext"] else "USA"
        
        # Avvisa se ETF è molto recente
        inception_date = info.get("fundInceptionDate")
        if inception_date:
            try:
                inception = pd.to_datetime(inception_date)
                months_old = (pd.Timestamp.now(tz="UTC") - inception).days / 30
                if months_old < 12:  # Meno di 1 anno
                    print(f"   ETF molto recente ({months_old:.0f} mesi) - dati storici limitati")
            except:
                pass

        # Salta se troppo simile agli ETF già in portafoglio
        if is_etf_duplicato(nome):
            print(f"   {ticker} ({nome}) troppo simile al portafoglio")
            return None

        # -------------------------------------------------------
        # 1. Calcolo rendimenti giornalieri
        # -------------------------------------------------------
        daily_returns = prezzi.pct_change().dropna()
        mean_daily_return = daily_returns.mean()
        std_daily_return = daily_returns.std()
        
        # -------------------------------------------------------
        # 2. Sustainable yield e Total Return
        # -------------------------------------------------------
        yield_val = calcola_yield_reale(t, prezzo)
        
        # Fallback: usa campo info se distribuzioni non disponibili
        if yield_val == 0:
            raw = info.get("dividendYield") or 0
            yield_val = round(raw * 100 if raw < 1 else raw, 2)

        # Calcolo total return 1 anno
        un_anno_fa = prezzi.index[-1] - pd.DateOffset(years=1)
        prezzo_un_anno_fa = prezzi[prezzi.index >= un_anno_fa].iloc[0] if len(prezzi[prezzi.index >= un_anno_fa]) > 0 else prezzi.iloc[0]
        
        dividendi_1y = dividendi[dividendi.index >= un_anno_fa].sum() if not dividendi.empty else 0
        total_return_1y = ((prezzo - prezzo_un_anno_fa + dividendi_1y) / prezzo_un_anno_fa) * 100

        # -------------------------------------------------------
        # 3. Distribution consistency
        # -------------------------------------------------------
        dividendi_1y_dates = dividendi[dividendi.index >= un_anno_fa]
        actual_payments = len(dividendi_1y_dates)
        
        # Determina frequenza attesa
        if actual_payments > 8:
            expected_payments = 12  # Monthly
        elif 3 <= actual_payments <= 5:
            expected_payments = 4   # Quarterly
        elif 1 <= actual_payments <= 2:
            expected_payments = 2   # Semi-annual
        else:
            expected_payments = 4   # Default quarterly
            
        consistency_score = min(actual_payments / expected_payments, 1.0) if expected_payments > 0 else 0

        # -------------------------------------------------------
        # 4. Distribution trend
        # -------------------------------------------------------
        if len(dividendi_1y_dates) >= 2:
            first_div = dividendi_1y_dates.iloc[0]
            last_div = dividendi_1y_dates.iloc[-1]
            div_growth = ((last_div - first_div) / first_div * 100) if first_div > 0 else 0
        else:
            div_growth = 0

        # -------------------------------------------------------
        # 5. Sharpe ratio (simplified)
        # -------------------------------------------------------
        sharpe = (mean_daily_return / std_daily_return * np.sqrt(252)) if std_daily_return > 0 else 0

        # -------------------------------------------------------
        # 6. Maximum drawdown
        # -------------------------------------------------------
        rolling_max = prezzi.expanding().max()
        drawdown = ((prezzi - rolling_max) / rolling_max) * 100
        max_drawdown = drawdown.min()

        # -------------------------------------------------------
        # 7. Momentum 3 mesi
        # -------------------------------------------------------
        tre_mesi_fa = prezzi.index[-1] - pd.DateOffset(months=3)
        prezzi_3m = prezzi[prezzi.index >= tre_mesi_fa]
        if len(prezzi_3m) > 0:
            prezzo_3m_fa = prezzi_3m.iloc[0]
            momentum_3m = ((prezzo - prezzo_3m_fa) / prezzo_3m_fa) * 100
        else:
            momentum_3m = 0

        # -------------------------------------------------------
        # 8. Portfolio correlation
        # -------------------------------------------------------
        max_correlation = calculate_max_correlation(daily_returns, portfolio_returns)

        # -------------------------------------------------------
        # 9. TER e AUM
        # -------------------------------------------------------
        ter = info.get("annualReportExpenseRatio") or 0
        ter_pct = ter * 100
        net_yield = yield_val - ter_pct
        
        aum_yf = info.get("totalAssets") or 0
        aum_finale = aum_yf if aum_yf > 0 else aum
        
        # AUM penalty
        aum_penalty = 0
        if aum_finale < 50_000_000:
            aum_penalty = -5
        elif aum_finale < 100_000_000:
            aum_penalty = -2
        elif aum_finale > 500_000_000:
            aum_penalty = 0.5  # Small bonus for liquidity

        # -------------------------------------------------------
        # HARD DISCARD CONDITIONS
        # -------------------------------------------------------
        if total_return_1y < -5.0:
            return None
        if max_drawdown < -25.0:
            return None
        if max_correlation > 0.90:
            return None
        if consistency_score < 0.5:
            return None
        if net_yield < 1.0:
            return None

        # -------------------------------------------------------
        # COMPOSITE SCORE
        # -------------------------------------------------------
        score = (
            net_yield              * 2.5   # dividend after costs
            + total_return_1y        * 1.5   # real performance
            + sharpe                 * 2.0   # return per unit of risk
            + consistency_score      * 1.0   # reliability of payments
            + div_growth             * 1.0   # growing vs shrinking distributions
            + momentum_3m            * 0.5   # recent direction
            - abs(max_drawdown)      * 1.5   # worst temporary loss
            - max_correlation        * 3.0   # overlap with existing portfolio
            - (ter_pct * 2.0)                # annual cost drag
            + aum_penalty                   # AUM stability bonus/penalty
        )

        return {
            "Ticker":           ticker,
            "Nome":             nome,
            "ISIN":             isin,
            "Exchange":         exchange,
            "Currency":         currency,
            "Prezzo €":         round(prezzo, 2),
            "Yield %":          yield_val,
            "Net Yield %":      round(net_yield, 2),
            "Total Return 1y %": round(total_return_1y, 1),
            "Sharpe":          round(sharpe, 2),
            "Max Drawdown %":  round(max_drawdown, 1),
            "Momentum 3m %":   round(momentum_3m, 1),
            "Consistency":     round(consistency_score, 2),
            "Div Growth %":    round(div_growth, 1),
            "Max Correlation": round(max_correlation, 3),
            "AUM":              f"{aum_finale/1e9:.1f}B" if aum_finale > 0 else "N/D",
            "TER %":           round(ter_pct, 2) if ter_pct > 0 else "N/D",
            "Score":           round(score, 2),
        }

    except Exception as e:
        print(f"   ⚠️  {ticker}: {e}")
        return None


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print("SCANNER ETF — DISCOVERY COMPLETA DA JUSTETF")
    print(f"     Solo distributing | Borsa Italiana | AUM >= {AUM_MIN//1e6:.0f}M€")
    print(f"     Yield reale >= {ETF_YIELD_MIN}% | Trend annuale positivo")
    print("=" * 65 + "\n")

    # Step 1: discovery completa da justETF
    etf_list = get_etf_da_justetf()

    if not etf_list:
        print(" Nessun ETF trovato da justETF.")
        print(" Nessun ETF trovato da justETF.")
        exit()

    # Step 1.5: carica dati del portafoglio esistente per correlazione
    print(" Carico dati del portafoglio esistente...")
    portfolio_returns = get_portfolio_returns()
    print(f"   Caricati {len(portfolio_returns)} ETF del portafoglio\n")

    # Step 2: converti ticker justETF → ticker Yahoo e analizza
    print(f" Ricerco ticker Yahoo e analizzo {len(etf_list)} ETF...\n")
    risultati = []

    for i, (ticker, nome_noto, aum) in enumerate(etf_list, 1):
        print(f"[{i:03d}/{len(etf_list)}] {ticker}  {nome_noto[:35]:<35}", end=" ")

        yahoo_ticker = ticker_to_yahoo_ticker(ticker)
        if not yahoo_ticker:
            print("X  ticker Yahoo non trovato")
            continue

        r = analizza_etf(yahoo_ticker, nome_noto, aum, portfolio_returns)
        if r:
            risultati.append(r)
            print(f"OK  {ticker}  net_yield:{r['Net Yield %']}%  score:{r['Score']}")
        else:
            print(f"X  {ticker} escluso")

    if not risultati:
        print("\nNessun ETF ha superato i filtri.")
        exit()

    df = (pd.DataFrame(risultati)
            .sort_values("Score", ascending=False)
            .reset_index(drop=True))
    df.index += 1

    print("\n\n" + "=" * 65)
    print(f"TOP {TOP_N} ETF DISTRIBUTING — MIGLIORI PER IL TUO PORTAFOGLIO")
    print("=" * 65)
    cols = ["Ticker","Nome","ISIN","Exchange","Currency","Prezzo €","Yield %","Net Yield %","Total Return 1y %",
            "Sharpe","Max Drawdown %","Momentum 3m %","Consistency","Div Growth %",
            "Max Correlation","AUM","TER %","Score"]
    print(df.head(TOP_N)[cols].to_string())

    df.to_csv("scan_etf_risultati.csv", encoding="utf-8-sig", index=True)
    print(f"\nSalvato in: scan_etf_risultati.csv")
    watchlist = df.head(TOP_N)["Ticker"].tolist()
    print(f"\nWATCHLIST ETF PER TRADINGAGENTS:")
    print(f"WATCHLIST = {watchlist}")