import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, time

# === Strategy Functions ===
from strategies.sma_crossover_strategy import generate_signals as sma_signals
from strategies.rsi_bollinger_strategy import generate_signals as rsi_signals
from strategies.macd_strategy import generate_signals as macd_signals
from strategies.ewma_crossover_strategy import generate_signals as ewma_signals
from strategies.atr_breakout_strategy import generate_signals as atr_signals
from utils.metrics import calculate_metrics
from utils.data import load_price_data
from utils.charts import *

# === Page Setup ===
st.set_page_config(page_title='Strategy Backtester', layout='wide')
st.title('Interactive Strategy Backtester')

# === User Inputs ===
col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input('Enter Ticker Symbol', value='AAPL')
    strategy = st.selectbox('Choose a Strategy',
                             ['SMA', 'EWMA', 'MACD', 'RSI', 'ATR'],
                             help='Select a trading strategy to backtest and visualize.')

    strategy_descriptions = {
    'SMA': 'Simple Moving Average crossover: Buy when short SMA crosses above long SMA; sell when it crosses below.',
    'EWMA': 'Exponentially Weighted MA crossover: Like SMA, but with more recent prices weighted heavier.',
    'MACD': 'Moving Average Convergence Divergence: Momentum strategy using EWMA crossovers and a signal line.',
    'RSI': 'Relative Strength Index: Measures overbought/oversold conditions. Buy when RSI < 30 & price hits lower band.',
    'ATR': 'Average True Range breakout: Volatility-based breakout strategy using ATR and 20-day highs/lows.'
    }
    st.markdown(f'**Strategy Summary:** {strategy_descriptions[strategy]}')


with col2:
    start_date = st.date_input('Start Date', value=datetime(2021, 1, 1))
    end_date = st.date_input('End Date', value=datetime(2023, 1, 1))

# Convert to datetime
start_date = datetime.combine(start_date, time.min)
end_date = datetime.combine(end_date, time.min)

# === Strategy-Specific Inputs ===
if strategy == 'SMA':
    st.subheader('SMA Parameters')
    short_window = st.slider('Short Window', min_value=5, max_value=50, value=20,
                             help='The period for the short-term moving average. Used to generate entry/exit signals.')
    long_window = st.slider('Long Window', min_value=10, max_value=200, value=50,
                            help='The period for the long-term moving average. Signals are generated when the short MA crosses this.')
elif strategy == 'EWMA':
    st.subheader('EWMA Parameters')
    short_window = st.slider('Short Window', min_value=5, max_value=50, value=20,
                             help='The short EWMA emphasizes recent prices more heavily for responsiveness.')
    long_window = st.slider('Long Window', min_value=10, max_value=200, value=50,
                            help='The long EWMA provides smoother signals and serves as the baseline trend.')
elif strategy == 'MACD':
    st.subheader('MACD Parameters')
    short_window = st.slider('Short EMA Window', 5, 20, 12,
                             help='Fast EWMA used in MACD calculation (default 12).')
    long_window = st.slider('Long EMA Window', 10, 50, 26,
                            help='Slow EWMA used in MACD calculation (default 26).')
    signal_window = st.slider('Signal Line Window', 5, 20, 9,
                              help='EWMA of the MACD line, used to generate buy/sell signals.')
elif strategy == 'RSI':
    st.subheader('RSI Parameters')
    rsi_period = st.slider('RSI Period', min_value=5, max_value=30, value=14,
                           help='The lookback period for RSI. Common default is 14 days.')
elif strategy == 'ATR':
    st.subheader('ATR Breakout Parameters')
    atr_window = st.slider('ATR Window', 5, 50, 14,
                           help='ATR period defines the volatility baseline. Higher values = smoother breakout levels.')
    breakout_window = st.slider('Breakout Window', 10, 50, 20,
                                help='Period over which recent highs/lows are tracked for breakout logic.')
    scale_factor = st.slider('Scale Factor', 0.1, 3.0, 0.5, step=0.1,
                             help='Multiplier applied to ATR for adjusting breakout thresholds.')

# === Wrapper Helper ===
def trim_warmup(df, warmup_window, start_date):
    # Find the first row after warmup_window periods from the start of the DataFrame
    warmup_idx = df.index[df['Date'] >= start_date][0]
    return df.loc[warmup_idx:].copy()

# === Strategy Wrappers ===
def run_sma_backtest(ticker, start, end, short_w, long_w):
    warmup_window = max(short_w, long_w)
    start_extended = start - timedelta(days=warmup_window * 2)
    df = load_price_data(ticker, start_extended, end)
    df, warmup = sma_signals(df, short_w, long_w)
    df = trim_warmup(df, warmup_window, start)
    df, metrics_df = calculate_metrics(df)
    return df, metrics_df

def run_ewma_backtest(ticker, start, end, short_w, long_w):
    warmup_window = max(short_w, long_w)
    start_extended = start - timedelta(days=warmup_window * 2)
    df = load_price_data(ticker, start_extended, end)
    df, warmup = ewma_signals(df, short_w, long_w)
    df = trim_warmup(df, warmup_window, start)
    df, metrics_df = calculate_metrics(df)
    return df, metrics_df

def run_macd_backtest(ticker, start, end, short_w, long_w, signal_w):
    warmup_window = max(short_w, long_w, signal_w)
    start_extended = start - timedelta(days=warmup_window * 2)
    df = load_price_data(ticker, start_extended, end)
    df, warmup = macd_signals(df, short_w, long_w, signal_w)
    df = trim_warmup(df, warmup_window, start)
    df, metrics_df = calculate_metrics(df)
    return df, metrics_df

def run_rsi_backtest(ticker, start, end, rsi_period):
    bollinger_window = 20
    warmup_window = max(rsi_period, bollinger_window)
    start_extended = start - timedelta(days=warmup_window * 2)
    df = load_price_data(ticker, start_extended, end)
    df, warmup = rsi_signals(df, rsi_period)
    df = trim_warmup(df, warmup_window, start)
    df, metrics_df = calculate_metrics(df)
    return df, metrics_df

def run_atr_backtest(ticker, start, end, atr_w, breakout_w, scale):
    warmup_window = max(atr_w, breakout_w)
    start_extended = start - timedelta(days=warmup_window * 2)
    df = load_price_data(ticker, start_extended, end)
    df, warmup = atr_signals(df, scale, atr_w, breakout_w)
    df = trim_warmup(df, warmup_window, start)
    df, metrics_df = calculate_metrics(df)
    return df, metrics_df

# === Toggle Buttons ===
st.markdown("### Display Options")

show_signals = st.checkbox(
    "Show Buy/Sell Markers", value=True,
    help="Toggles entry and exit signal markers on the price chart.")

show_indicators = st.checkbox(
    "Show Indicator Overlays", value=True,
    help="Overlay technical indicators like SMAs, EWMAs, or breakout bands.")

show_subplots = st.checkbox(
    "Show Subplots (MACD/RSI Panels)", value=True,
    help="Adds separate MACD or RSI subpanels below the price chart if relevant.")

# === Run Backtest ===
if st.button('Run Backtest'):
    if strategy == 'SMA':
        df, metrics = run_sma_backtest(ticker, start_date, end_date, short_window, long_window)
    elif strategy == 'EWMA':
        df, metrics = run_ewma_backtest(ticker, start_date, end_date, short_window, long_window)
    elif strategy == 'MACD':
        df, metrics = run_macd_backtest(ticker, start_date, end_date, short_window, long_window, signal_window)
    elif strategy == 'RSI':
        df, metrics = run_rsi_backtest(ticker, start_date, end_date, rsi_period)
    elif strategy == 'ATR':
        df, metrics = run_atr_backtest(ticker, start_date, end_date, atr_window, breakout_window, scale_factor)

    # === Plot Results ===
    st.subheader('Cumulative Returns')
    st.markdown('**Compare the cumulative performance of the strategy vs. the overall market.**')
    st.plotly_chart(plot_cumulative_returns(df), use_container_width=True)

    st.subheader('Strategy Visualization')
    st.markdown('**Visualize buy/sell signals and technical indicators specific to the selected strategy.**')
    st.plotly_chart(plot_strategy_dashboard(df, strategy, show_signals, show_indicators, show_subplots),
    use_container_width=True)

    st.subheader('Drawdown Over Time')
    st.markdown('**Track the peak-to-trough declines in strategy value over time.**')
    st.plotly_chart(plot_drawdown(df), use_container_width=True)

    st.subheader('Daily Return Distribution')
    st.markdown('**Examine the distribution of daily strategy returns to assess volatility and skew.**')
    st.plotly_chart(plot_return_histogram(df), use_container_width=True)

    st.subheader('Performance Metrics')
    st.markdown('**Key statistics summarizing return, risk, and efficiency of the selected strategy.**')
    st.dataframe(metrics.style.format({'Value': '{:.3f}'}))