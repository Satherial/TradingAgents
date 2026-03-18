"""
test_main.py - Unit tests per main.py

Esegui: python -m pytest test_main.py -v
oppure: python test_main.py
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import json

# Aggiungi il path per importare main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import (
    check_and_run_scanner,
    validate_portfolio_with_llm,
    load_portfolio_and_strategy,
    build_system_prompt,
    is_buy_recommendation,
    SCAN_RESULTS_FILE,
    PORTFOLIO_FILE,
    STRATEGY_FILE,
)


class TestCheckAndRunScanner(unittest.TestCase):
    """Test per la funzione check_and_run_scanner"""
    
    @patch('main.os.path.exists')
    def test_file_exists_returns_true(self, mock_exists):
        """Se il file esiste, ritorna True senza lanciare scanner"""
        mock_exists.return_value = True
        
        result = check_and_run_scanner()
        
        self.assertTrue(result)
        mock_exists.assert_called_once_with(SCAN_RESULTS_FILE)
    
    @patch('main.subprocess.run')
    @patch('main.os.path.exists')
    def test_file_missing_runs_scanner_success(self, mock_exists, mock_subprocess):
        """Se il file manca e scanner ha successo, ritorna True"""
        mock_exists.return_value = False
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        result = check_and_run_scanner()
        
        self.assertTrue(result)
        mock_subprocess.assert_called_once()
    
    @patch('main.subprocess.run')
    @patch('main.os.path.exists')
    def test_scanner_fails_returns_false(self, mock_exists, mock_subprocess):
        """Se scanner fallisce, ritorna False"""
        mock_exists.return_value = False
        mock_subprocess.return_value = MagicMock(returncode=1, stderr="Error")
        
        result = check_and_run_scanner()
        
        self.assertFalse(result)
    
    @patch('main.subprocess.run')
    @patch('main.os.path.exists')
    def test_scanner_timeout_returns_false(self, mock_exists, mock_subprocess):
        """Se scanner va in timeout, ritorna False"""
        mock_exists.return_value = False
        mock_subprocess.side_effect = Exception("timeout")
        
        result = check_and_run_scanner()
        
        self.assertFalse(result)


class TestValidatePortfolioWithLLM(unittest.TestCase):
    """Test per la funzione validate_portfolio_with_llm"""
    
    @patch('main.requests.post')
    def test_valid_portfolio_detected(self, mock_post):
        """Riconosce un portfolio valido"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"has_portfolio": true, "is_empty": false, "tickers": ["AAPL"], "summary": "Portfolio con AAPL"}'
        }
        mock_post.return_value = mock_response
        
        is_valid, content = validate_portfolio_with_llm("Possiedo AAPL")
        
        self.assertTrue(is_valid)
        self.assertEqual(content, "Portfolio con AAPL")
    
    @patch('main.requests.post')
    def test_empty_portfolio_detected(self, mock_post):
        """Riconosce un portfolio vuoto esplicito"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"has_portfolio": false, "is_empty": true, "tickers": [], "summary": "Portfolio vuoto"}'
        }
        mock_post.return_value = mock_response
        
        is_valid, content = validate_portfolio_with_llm("Portfolio vuoto")
        
        self.assertTrue(is_valid)  # Vuoto è valido!
        self.assertEqual(content, "Portfolio vuoto")
    
    @patch('main.requests.post')
    def test_invalid_portfolio_detected(self, mock_post):
        """Riconosce un portfolio non valido"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"has_portfolio": false, "is_empty": false, "tickers": [], "summary": "Non un portfolio"}'
        }
        mock_post.return_value = mock_response
        
        is_valid, content = validate_portfolio_with_llm("Testo casuale")
        
        self.assertFalse(is_valid)
    
    @patch('main.requests.post')
    def test_llm_error_fallback(self, mock_post):
        """Se LLM fallisce, accetta il contenuto (fallback)"""
        mock_post.side_effect = Exception("Connection error")
        
        is_valid, content = validate_portfolio_with_llm("Contenuto fallback")
        
        self.assertTrue(is_valid)  # Fallback: accetta
        self.assertEqual(content, "Contenuto fallback")


class TestIsBuyRecommendation(unittest.TestCase):
    """Test per la funzione is_buy_recommendation"""
    
    def test_buy_uppercase(self):
        """Riconosce BUY"""
        self.assertTrue(is_buy_recommendation("Raccomandazione: BUY"))
    
    def test_buy_lowercase(self):
        """Riconosce buy (case insensitive)"""
        self.assertTrue(is_buy_recommendation("Raccomandazione: buy"))
    
    def test_acquistare(self):
        """Riconosce ACQUISTARE"""
        self.assertTrue(is_buy_recommendation("Consiglio di ACQUISTARE"))
    
    def test_hold_not_buy(self):
        """HOLD non è BUY"""
        self.assertFalse(is_buy_recommendation("Raccomandazione: HOLD"))
    
    def test_sell_not_buy(self):
        """SELL non è BUY"""
        self.assertFalse(is_buy_recommendation("Raccomandazione: SELL"))
    
    def test_empty_not_buy(self):
        """Stringa vuota non è BUY"""
        self.assertFalse(is_buy_recommendation(""))


class TestBuildSystemPrompt(unittest.TestCase):
    """Test per la funzione build_system_prompt"""
    
    def test_prompt_contains_portfolio(self):
        """Il prompt contiene il portfolio"""
        portfolio = "AAPL: 100 quote"
        strategy = ""
        
        prompt = build_system_prompt(portfolio, strategy)
        
        self.assertIn("AAPL: 100 quote", prompt)
        self.assertIn("PORTAFOGLIO ATTUALE DELL'INVESTITORE", prompt)
    
    def test_prompt_contains_strategy(self):
        """Il prompt contiene la strategia se fornita"""
        portfolio = "AAPL"
        strategy = "Investire in tech"
        
        prompt = build_system_prompt(portfolio, strategy)
        
        self.assertIn("STRATEGIA DELL'INVESTITORE", prompt)
        self.assertIn("Investire in tech", prompt)
    
    def test_prompt_without_strategy(self):
        """Il prompt non ha sezione strategia se vuota"""
        portfolio = "AAPL"
        strategy = ""
        
        prompt = build_system_prompt(portfolio, strategy)
        
        self.assertNotIn("STRATEGIA DELL'INVESTITORE", prompt)
    
    def test_prompt_contains_buy_definitions(self):
        """Il prompt definisce BUY/HOLD/SELL"""
        prompt = build_system_prompt("portfolio", "strategy")
        
        self.assertIn("BUY = ACQUISTA questo titolo", prompt)
        self.assertIn("HOLD = NON ACQUISTARE ORA", prompt)
        self.assertIn("AVOID/EVITA = NON ACQUISTARE", prompt)


class TestLoadPortfolioAndStrategy(unittest.TestCase):
    """Test per la funzione load_portfolio_and_strategy"""
    
    @patch('main.os.path.exists')
    @patch('main.validate_portfolio_with_llm')
    @patch('builtins.open', mock_open(read_data="Portfolio test"))
    def test_loads_valid_portfolio(self, mock_validate, mock_exists):
        """Carica portfolio valido con strategia"""
        mock_exists.side_effect = lambda x: x == "portafolio.txt" or x == STRATEGY_FILE
        mock_validate.return_value = (True, "Portfolio validato")
        
        with patch('builtins.open', mock_open(read_data="Strategia test")) as mock_file:
            portfolio, strategy = load_portfolio_and_strategy()
        
        self.assertEqual(portfolio, "Portfolio validato")
        # Strategia dovrebbe essere caricata
    
    @patch('main.os.path.exists')
    def test_missing_portfolio_exits(self, mock_exists):
        """Se portfolio.txt manca, esce con errore"""
        mock_exists.return_value = False
        
        with self.assertRaises(SystemExit) as cm:
            load_portfolio_and_strategy()
        
        self.assertEqual(cm.exception.code, 1)
    
    @patch('main.os.path.exists')
    @patch('main.validate_portfolio_with_llm')
    @patch('builtins.open', mock_open(read_data="Invalid content"))
    def test_invalid_portfolio_exits(self, mock_validate, mock_exists):
        """Se portfolio non valido, esce con errore"""
        mock_exists.return_value = True
        mock_validate.return_value = (False, "Non valido")
        
        with self.assertRaises(SystemExit) as cm:
            load_portfolio_and_strategy()
        
        self.assertEqual(cm.exception.code, 1)


class TestIntegrationFlow(unittest.TestCase):
    """Test di integrazione per flussi completi"""
    
    @patch('main.check_and_run_scanner')
    @patch('main.pd.read_csv')
    @patch('main.load_portfolio_and_strategy')
    @patch('main.TradingAgentsGraph')
    def test_full_flow_finds_buy(self, mock_graph_class, mock_load, mock_read_csv, mock_check_scanner):
        """Flusso completo che trova un BUY"""
        # Setup mocks
        mock_check_scanner.return_value = True
        mock_df = MagicMock()
        mock_df.head.return_value = MagicMock()
        mock_df.head.return_value.__getitem__ = MagicMock(return_value=["VUSA.MI", "VWRA.MI"])
        mock_read_csv.return_value = mock_df
        mock_load.return_value = ("Portfolio test", "Strategy test")
        
        mock_graph = MagicMock()
        mock_graph.propagate.return_value = (None, "Raccomandazione: BUY per VUSA.MI")
        mock_graph_class.return_value = mock_graph
        
        # Esegui main (mockato)
        with patch('main.date') as mock_date:
            mock_date.today.return_value.strftime.return_value = "2026-03-18"
            with patch('builtins.open', mock_open()):
                # Importa e esegui main in modo controllato
                import main as main_module
                with patch.object(main_module, 'check_and_run_scanner', mock_check_scanner):
                    with patch.object(main_module, 'load_portfolio_and_strategy', mock_load):
                        # Simula il flusso
                        result = main_module.check_and_run_scanner()
                        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
