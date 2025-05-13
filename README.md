
# Quant Backtester

An interactive Streamlit-based dashboard for visualizing and backtesting popular trading strategies on historical market data. Built for clarity, extensibility, and real-world relevance.

[Live App on Streamlit](https://quantbacktester.streamlit.app/)

---

## Features

- Backtest across five strategies:
  - SMA Crossover
  - EWMA Crossover
  - MACD
  - RSI + Bollinger Band
  - ATR Breakout
- Real-time performance metrics:
  - Sharpe ratio, Sortino, Max drawdown, CAGR, Profit factor
- Interactive strategy overlays:
  - Buy/sell signal markers
  - Technical indicators
  - Subpanels for RSI/MACD
- Drawdown analysis and return histograms
- Exportable trade log
- Custom date ranges, parameter tuning via UI

---

## Why I Built This

This project began as a personal exploration of algorithmic trading, backtesting methodologies, and data visualization. I wanted a tool that would be flexible, explainable, and visually clean enough to serve both as a learning platform and as a demonstration of my capabilities in Python, financial modeling, and UI design. It evolved into a full-featured backtesting dashboard that I now use to prototype ideas and showcase strategy logic clearly.

---

## How to Run

1. Clone the repo
```bash
git clone https://github.com/yourusername/quant-backtester.git
cd quant-backtester
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Launch the app
```bash
streamlit run app.py
```

---

## Project Structure
```
quant-backtester/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── strategies/             # All strategy logic modules
├── utils/
│   ├── metrics.py          # Performance calculation
│   └── charts.py           # Plotly visualizations
```

---

## Strategy Notes

Each strategy is fully documented with signal logic and parameter controls inside the app.

| Strategy | Logic |
|----------|--------|
| SMA      | Crosses of two simple moving averages |
| EWMA     | Exponential moving average crossover |
| MACD     | Fast/slow EWMA divergence with signal line confirmation |
| RSI      | Reversion strategy with Bollinger filter |
| ATR      | Volatility breakout using ATR and 20-day high/low |

---

## TODO / Next Steps

- Add position sizing models (fixed % / vol-adjusted)
- Simulate slippage / transaction cost scenarios
- Add rolling Sharpe ratio and drawdown charts
- Allow multi-strategy portfolio simulation

---

## Contact
Built by Tobias Safie. Reach out via [LinkedIn](https://linkedin.com/in/tsafie) or open an issue!
