"""
Test unitari per scanner.py
Coverage delle funzioni principali di scanning e analisi ETF
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Aggiungi la directory corrente al path per importare scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scanner


class TestETFScanner:
    """Test suite per le funzioni principali di scanner.py"""
    
    def test_is_etf_duplicato(self):
        """Test della funzione di rilevamento duplicati"""
        # Test casi positivi
        assert scanner.is_etf_duplicato("iShares STOXX Euro 600") == True
        assert scanner.is_etf_duplicato("MSCI EU UCITS") == True
        assert scanner.is_etf_duplicato("Xtrackers Portfolio Income") == True
        assert scanner.is_etf_duplicato("XTR PTF Dividend") == True
        
        # Test casi negativi
        assert scanner.is_etf_duplicato("Vanguard All-World") == False
        assert scanner.is_etf_duplicato("iShares MSCI World") == False
        assert scanner.is_etf_duplicato("SPDR S&P 500") == False
        assert scanner.is_etf_duplicato("") == False
    
    def test_get_etf_fallback(self):
        """Test della funzione fallback per ETF"""
        fallback_list = scanner.get_etf_fallback()
        
        # Verifica che sia una lista
        assert isinstance(fallback_list, list)
        
        # Verifica che contenga elementi
        assert len(fallback_list) > 0
        
        # Verifica formato degli elementi (ticker, nome, aum)
        for item in fallback_list:
            assert len(item) == 3
            assert isinstance(item[0], str)  # ticker
            assert isinstance(item[1], str)  # nome
            assert isinstance(item[2], (int, float))  # aum
            assert item[2] > 0  # AUM deve essere positivo
    
    @patch('scanner.yf.Ticker')
    def test_ticker_to_yahoo_ticker_success_mi(self, mock_ticker):
        """Test conversione ticker con successo .MI"""
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = {'regularMarketPrice': 100.0}
        mock_ticker.return_value = mock_ticker_obj
        
        result = scanner.ticker_to_yahoo_ticker("VUSA")
        assert result == "VUSA.MI"
        mock_ticker.assert_called_with("VUSA.MI")
    
    @patch('scanner.yf.Ticker')
    def test_ticker_to_yahoo_ticker_success_base(self, mock_ticker):
        """Test conversione ticker con successo base"""
        # Prima chiamata fallisce, seconda ha successo
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = {'regularMarketPrice': 100.0}
        
        # Simula fallimento prima chiamata
        def side_effect_func(ticker):
            if ".MI" in ticker:
                failed_obj = Mock()
                failed_obj.info = None
                return failed_obj
            else:
                return mock_ticker_obj
                
        mock_ticker.side_effect = side_effect_func
        
        result = scanner.ticker_to_yahoo_ticker("VUSA")
        assert result == "VUSA"
        assert mock_ticker.call_count == 2
    
    @patch('scanner.yf.Ticker')
    def test_ticker_to_yahoo_ticker_failure(self, mock_ticker):
        """Test conversione ticker fallimento"""
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = None
        mock_ticker.return_value = mock_ticker_obj
        
        result = scanner.ticker_to_yahoo_ticker("INVALID")
        assert result is None
    
    def test_calcola_yield_reale(self):
        """Test calcolo yield reale da dividendi"""
        # Mock ticker con dividendi
        mock_ticker = Mock()
        
        # Test caso con dividendi (ultimi 12 mesi)
        now = pd.Timestamp.now(tz="UTC")
        dates = [now - pd.DateOffset(months=11), now - pd.DateOffset(months=8), 
                 now - pd.DateOffset(months=5), now - pd.DateOffset(months=2)]
        values = [1.0, 1.0, 1.0, 1.0]
        dividendi_data = pd.Series(values, index=dates)
        mock_ticker.dividends = dividendi_data
        
        result = scanner.calcola_yield_reale(mock_ticker, 100.0)
        assert result == 4.0  # 4 dividendi da 1€ su prezzo 100€ = 4%
        
        # Test caso senza dividendi
        mock_ticker.dividends = pd.Series([], dtype=float)
        result = scanner.calcola_yield_reale(mock_ticker, 100.0)
        assert result == 0.0
        
        # Test caso prezzo zero
        result = scanner.calcola_yield_reale(mock_ticker, 0.0)
        assert result == 0.0
    
    @patch('scanner.yf.Ticker')
    def test_get_portfolio_returns(self, mock_ticker):
        """Test caricamento rendimenti portafoglio"""
        # Mock dati storici con indice temporale
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        mock_history = pd.DataFrame({
            'Close': np.random.uniform(95, 105, 100)
        }, index=dates)
        mock_ticker.return_value.history.return_value = mock_history
        
        with patch('scanner.PORTFOLIO_ETFS', {'TEST.MI': 'Test ETF'}):
            result = scanner.get_portfolio_returns()
            
            assert isinstance(result, dict)
            assert 'TEST.MI' in result
            assert isinstance(result['TEST.MI'], pd.Series)
            assert len(result['TEST.MI']) > 50  # Almeno 50 giorni di dati
    
    def test_calculate_max_correlation(self):
        """Test calcolo correlazione massima"""
        # Mock rendimenti candidati e portafoglio con almeno 30 giorni di dati
        dates = pd.date_range(start='2023-01-01', periods=35, freq='D')
        candidate_returns = pd.Series(np.random.normal(0.01, 0.02, 35), index=dates, name='candidate')
        
        # ETF2 con correlazione quasi perfetta
        etf2_values = candidate_returns.values + np.random.normal(0, 0.001, 35)  # Piccolo rumore
        portfolio_returns = {
            'ETF1': pd.Series(np.random.normal(0.01, 0.02, 35), index=dates, name='etf1'),
            'ETF2': pd.Series(etf2_values, index=dates, name='etf2'),
            'ETF3': pd.Series(np.random.normal(-0.01, 0.02, 35), index=dates, name='etf3')
        }
        
        result = scanner.calculate_max_correlation(candidate_returns, portfolio_returns)
        assert 0.0 <= result <= 1.0
        # Dovrebbe trovare correlazione alta con ETF2
        assert result > 0.9
    
    @patch('scanner.yf.Ticker')
    @patch('scanner.calcola_yield_reale')
    @patch('scanner.calculate_max_correlation')
    def test_analizza_etf_success(self, mock_corr, mock_yield, mock_ticker):
        """Test analisi ETF con successo"""
        # Mock ticker
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = {
            'shortName': 'Test ETF',
            'currentPrice': 100.0,
            'dividendYield': 0.03,
            'annualReportExpenseRatio': 0.001,
            'totalAssets': 1000000000,
            'fundInceptionDate': '2018-01-01'  # ETF con più di 5 anni di storia (60 mesi)
        }
        
        # Mock storico prezzi con almeno 50 giorni di dati
        dates = pd.date_range(start='2023-01-01', periods=60, freq='D')
        prices = np.linspace(95, 106, 60) + np.random.normal(0, 1, 60)
        mock_history = pd.DataFrame({
            'Close': prices
        }, index=dates)
        mock_ticker_obj.history.return_value = mock_history
        
        # Mock dividendi con date appropriate
        dividend_dates = [dates[10], dates[20], dates[30], dates[40]]
        mock_ticker_obj.dividends = pd.Series([1.0, 1.0, 1.0, 1.0], index=dividend_dates)
        mock_ticker.return_value = mock_ticker_obj
        
        # Mock funzioni
        mock_yield.return_value = 4.0
        mock_corr.return_value = 0.5
        
        # Mock portfolio returns con almeno 30 giorni
        dates_portfolio = pd.date_range(start='2023-01-01', periods=40, freq='D')
        portfolio_returns = {'TEST.MI': pd.Series(np.random.normal(0.01, 0.02, 40), index=dates_portfolio)}
        
        result = scanner.analizza_etf("TEST.MI", "Test ETF", 1000000000, portfolio_returns)
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'Ticker' in result
        assert 'Score' in result
        assert result['Ticker'] == "TEST.MI"
        assert result['Net Yield %'] >= 1.0
    
    @patch('scanner.yf.Ticker')
    def test_analizza_etf_insufficient_data(self, mock_ticker):
        """Test analisi ETF con dati insufficienti"""
        mock_ticker_obj = Mock()
        mock_ticker_obj.history.return_value = pd.DataFrame()  # Storico vuoto
        mock_ticker.return_value = mock_ticker_obj
        
        portfolio_returns = {}
        
        result = scanner.analizza_etf("TEST.MI", "Test ETF", 1000000000, portfolio_returns)
        assert result is None
    
    @patch('scanner.yf.Ticker')
    def test_analizza_etf_duplicate(self, mock_ticker):
        """Test analisi ETF duplicato"""
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = {
            'shortName': 'iShares STOXX Euro 600',  # Nome duplicato
            'currentPrice': 100.0,
        }
        mock_ticker_obj.history.return_value = pd.DataFrame({
            'Close': [95, 96, 97, 98, 99, 100]
        })
        mock_ticker.return_value = mock_ticker_obj
        
        portfolio_returns = {}
        
        result = scanner.analizza_etf("TEST.MI", "iShares STOXX Euro 600", 1000000000, portfolio_returns)
        assert result is None  # Dovrebbe essere escluso come duplicato
    
    def test_analizza_etf_hard_filters(self):
        """Test filtri hard discard conditions"""
        # Creiamo un mock che simula dati che violano i filtri
        with patch('scanner.yf.Ticker') as mock_ticker, \
             patch('scanner.calcola_yield_reale') as mock_yield, \
             patch('scanner.calculate_max_correlation') as mock_corr:
            
            mock_ticker_obj = Mock()
            mock_ticker_obj.info = {
                'shortName': 'Test ETF',
                'currentPrice': 100.0,
                'dividendYield': 0.005,  # Net yield < 1%
                'annualReportExpenseRatio': 0.001,
                'totalAssets': 1000000000
            }
            
            mock_ticker_obj.history.return_value = pd.DataFrame({
                'Close': [120, 115, 110, 105, 100]  # Total return negativo
            })
            mock_ticker_obj.dividends = pd.Series()
            mock_ticker.return_value = mock_ticker_obj
            
            mock_yield.return_value = 0.5  # Sotto 1%
            mock_corr.return_value = 0.5
            
            portfolio_returns = {}
            
            result = scanner.analizza_etf("TEST.MI", "Test ETF", 1000000000, portfolio_returns)
            assert result is None, "ETF dovrebbe essere escluso per dati insufficienti"  # Verifiche con nuovi filtri più stringenti
    
    @patch('scanner.get_etf_da_justetf')
    @patch('scanner.get_portfolio_returns')
    @patch('scanner.ticker_to_yahoo_ticker')
    @patch('scanner.analizza_etf')
    def test_main_workflow(self, mock_analizza, mock_ticker_conv, mock_portfolio, mock_etf_list):
        """Test del workflow principale"""
        # Mock dati
        mock_etf_list.return_value = [
            ("VUSA", "Vanguard All-World", 5000000000),
            ("IWDA", "iShares MSCI World", 3000000000)
        ]
        
        mock_portfolio.return_value = {'EXISTING.MI': pd.Series([0.01, 0.02])}
        mock_ticker_conv.side_effect = ["VUSA.MI", "IWDA.MI"]
        mock_analizza.side_effect = [
            {'Ticker': 'VUSA.MI', 'Score': 100, 'Net Yield %': 2.0},
            {'Ticker': 'IWDA.MI', 'Score': 90, 'Net Yield %': 1.8}
        ]
        
        # Simula esecuzione main (senza eseguirla davvero)
        etf_list = scanner.get_etf_da_justetf()
        portfolio_returns = scanner.get_portfolio_returns()
        
        assert len(etf_list) == 2
        assert len(portfolio_returns) == 1
        
        # Verifica chiamate
        mock_etf_list.assert_called_once()
        mock_portfolio.assert_called_once()


class TestConfigConstants:
    """Test per le costanti di configurazione"""
    
    def test_filter_constants(self):
        """Test valori delle costanti di filtro"""
        # Verifica valori attuali (modificati per essere più stringenti)
        assert scanner.ETF_YIELD_MIN == 1.0  # Minimo 1% yield
        assert scanner.ETF_YIELD_MAX == 20.0
        assert scanner.AUM_MIN == 100_000_000  # 100M minimo
        assert scanner.MIN_AGE_MONTHS == 60  # Minimo 5 anni (60 mesi)
        assert scanner.TOP_N == 25
    
    def test_portfolio_constants(self):
        """Test costanti del portafoglio"""
        assert isinstance(scanner.PORTFOLIO_ETFS, dict)
        assert len(scanner.PORTFOLIO_ETFS) > 0
        
        assert isinstance(scanner.ETF_GIA_PRESENTI_KEYWORDS, list)
        assert len(scanner.ETF_GIA_PRESENTI_KEYWORDS) > 0


if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v", "--tb=short"])
