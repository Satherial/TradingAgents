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
  <!-- Keep these links. Translations will automatically update with the README. -->
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

# TradingAgents: Multi-Agents LLM Financial Trading Framework

## News
- [2026-03] **TradingAgents v0.2.1** released with GPT-5.4, Gemini 3.1, Claude 4.6 model coverage and improved system stability.
- [2026-02] **TradingAgents v0.2.0** released with multi-provider LLM support (GPT-5.x, Gemini 3.x, Claude 4.x, Grok 4.x) and improved system architecture.
- [2026-01] **Trading-R1** [Technical Report](https://arxiv.org/abs/2509.11420) released, with [Terminal](https://github.com/TauricResearch/Trading-R1) expected to land soon.

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

> 🎉 **TradingAgents** officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

<div align="center">

🚀 [TradingAgents](#tradingagents-framework) | ⚡ [Installation & CLI](#installation-and-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Package Usage](#tradingagents-package) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## TradingAgents Framework

TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. By deploying specialized LLM-powered agents: from fundamental analysts, sentiment experts, and technical analysts, to trader, risk management team, the platform collaboratively evaluates market conditions and informs trading decisions. Moreover, these agents engage in dynamic discussions to pinpoint the optimal strategy.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

Our framework decomposes complex trading tasks into specialized roles. This ensures the system achieves a robust, scalable approach to market analysis and decision-making.

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installation and CLI

### Installation

Clone TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Create a virtual environment in any of your favorite environment managers:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Required APIs

TradingAgents supports multiple LLM providers. Set the API key for your chosen provider:

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage (optional)
export FINNHUB_API_KEY=...         # Finnhub (optional)
```

**For local models**, configure Ollama with environment variables:
```bash
export LLM_PROVIDER=ollama
export LLM_QUICK=llama3.1:8b
export LLM_DEEP=qwen3:14b
export OLLAMA_HOST=http://localhost:11434
```

**Data Sources:**
- **Default:** yfinance (free, no API key required)
- **Optional:** Alpha Vantage or Finnhub for enhanced data

Alternatively, copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

### CLI Usage

You can also try out the CLI directly by running:
```bash
python -m cli.main
```
You will see a screen where you can select your desired tickers, date, LLMs, research depth, etc.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents Package

### Implementation Details

We built TradingAgents with LangGraph to ensure flexibility and modularity. The framework supports multiple LLM providers: OpenAI, Google, Anthropic, xAI, OpenRouter, and Ollama.

### Python Usage

To use TradingAgents inside your code, you can import the `tradingagents` module and initialize a `TradingAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
config["deep_think_llm"] = "gpt-5.2"     # Model for complex reasoning
config["quick_think_llm"] = "gpt-5-mini" # Model for quick tasks
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

See `tradingagents/default_config.py` for all configuration options.

## Automated Trading Flow

The `main.py` script provides a complete automated trading workflow that combines ETF discovery with portfolio-aware analysis to find optimal investment opportunities.

### Features

**Smart Workflow Automation:**
- Automatically runs `scanner.py` if results file is missing
- Sequential analysis of top ETF candidates until first BUY recommendation
- Portfolio-aware analysis using your existing holdings and investment strategy
- Stops at first BUY to save time and computational resources

**Portfolio Integration:**
- `portafolio.txt` - List your current holdings and sector exposure
- `strategia.txt` - Define your investment rules, risk profile, and objectives
- LLM-powered portfolio validation ensures consistency
- Avoids duplicate sector exposure and aligns with your strategy

**Intelligent Analysis:**
- Uses TradingAgents multi-agent system for each candidate
- Bull/Bear debate rounds for balanced decision making
- Context-aware recommendations (BUY/HOLD/AVOID)
- Results saved to `decisione_finale.txt`

### Quick Start

1. **Configure your portfolio:**
```bash
# Copy and edit templates
cp portfolio_example.txt portafolio.txt
cp strategia_example.txt strategia.txt

# Edit with your actual holdings and strategy
```

2. **Set up LLM configuration (.env):**
```bash
# For local models
LLM_PROVIDER=ollama
LLM_QUICK=llama3.1:8b
LLM_DEEP=qwen3:14b
OLLAMA_HOST=http://localhost:11434
```

3. **Run automated analysis:**
```bash
python main.py
```

### File Structure

```
├── main.py                    # Automated trading workflow
├── scanner.py                 # ETF discovery and analysis
├── portafolio.txt             # Your current holdings (create from template)
├── strategia.txt              # Your investment strategy (create from template)
├── portfolio_example.txt      # Portfolio template with examples
├── strategia_example.txt      # Strategy template with examples
├── scan_etf_risultati.csv     # Scanner output (auto-generated)
└── decisione_finale.txt       # Final BUY recommendation (auto-generated)
```

### Workflow Process

1. **Discovery:** Runs scanner to find dividend ETF candidates
2. **Validation:** Checks portfolio.txt and strategia.txt with LLM validation
3. **Analysis:** Tests each ETF with full TradingAgents system
4. **Selection:** Stops at first BUY recommendation
5. **Output:** Saves detailed analysis and recommendation

### Customization

- **Risk Profile:** Modify `strategia.txt` for conservative/aggressive approach
- **Sector Preferences:** Define target sectors in portfolio analysis
- **Investment Amount:** Change liquidità in strategia.txt
- **LLM Models:** Configure quick/deep models in .env

## ETF Scanner

The `scanner.py` module provides a comprehensive ETF discovery and analysis tool specifically designed for income-focused dividend ETFs. This scanner exclusively targets the best dividend-paying ETFs while systematically ignoring all other investment vehicles.

### Key Features

**Dividend-Focused Discovery:**
- Downloads complete ETF listings from justETF database
- Filters exclusively for "Distributing" ETFs (dividend-paying)
- Lists only ETFs quoted on Borsa Italiana with AUM ≥100M€
- Excludes non-dividending ETFs, growth ETFs, and accumulation funds

**Comprehensive Analysis Pipeline:**
For each dividend ETF candidate, the system calculates:

**Dividend Metrics:**
- Real yield based on actual 12-month distributions
- Net yield (yield minus TER costs)
- Consistency score (payment reliability)
- Dividend growth trend (growing vs shrinking distributions)

**Financial Performance Metrics:**
- Total Return 1 year (price + dividends)
- Sharpe ratio (return per unit of risk)
- Maximum drawdown (worst temporary loss)
- 3-month momentum

**Risk Management:**
- Portfolio correlation analysis to avoid overlap
- Hard exclusion filters for underperforming assets
- AUM stability assessment

**Selection Criteria:**
ETFs are automatically excluded if they fail any of these conditions:
- Total return < -5% (negative performance)
- Maximum drawdown < -25% (excessive risk)
- Correlation > 90% with existing portfolio
- Consistency score < 50% (unreliable payments)
- Net yield < 1% (insufficient dividends)

**Composite Scoring System:**
Only ETFs passing all filters receive a composite score weighted towards:
- **Net Yield** (weight 2.5) - highest priority
- **Total Return** (weight 1.5)
- **Sharpe Ratio** (weight 2.0)
- **Payment Consistency** (weight 1.0)
- **Dividend Growth** (weight 1.0)
- **Correlation Penalty** (weight 3.0) - avoids portfolio overlap

### Usage

```bash
python scanner.py
```

The scanner outputs the top 15 dividend ETFs ranked by composite score, providing:
- Ticker and name
- Current price and yield metrics
- Risk indicators (Sharpe, drawdown, correlation)
- Performance data (total return, momentum)
- Composite score for ranking

Results are saved to `scan_etf_risultati.csv` and a watchlist is generated for integration with TradingAgents.

### Dependencies

```bash
pip install justetf-scraping yfinance pandas numpy
```

## Testing

The project includes comprehensive unit tests for core functionality:

```bash
# Run all tests
python -m pytest -v

# Run specific test files
python test_main.py          # Test automated workflow (22 tests)
python test_scanner.py       # Test ETF scanner (15 tests)
```

**Test Coverage:**
- **main.py:** Scanner integration, portfolio validation, LLM communication
- **scanner.py:** ETF discovery, ticker conversion, correlation analysis
- **Mock-based:** Tests use mocks for external APIs and LLM calls

Tests ensure reliability of the automated workflow and scanner components.

## Contributing

We welcome contributions from the community! Whether it's fixing a bug, improving documentation, or suggesting a new feature, your input helps make this project better. If you are interested in this line of research, please consider joining our open-source financial AI research community [Tauric Research](https://tauric.ai/).

## Citation

Please reference our work if you find *TradingAgents* provides you with some help :)

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
