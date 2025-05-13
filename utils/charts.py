import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_cumulative_returns(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative_Strategy'],
                             mode='lines', name='Strategy', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative_Market'],
                             mode='lines', name='Market', line=dict(color='gray')))
    fig.update_layout(title='Cumulative Returns', xaxis_title='Date', yaxis_title='Return',
                      hovermode='x unified')
    return fig

def plot_strategy_dashboard(df, strategy_name):
    if strategy_name == "MACD":
        return plot_price_macd(df)
    elif strategy_name == "RSI":
        return plot_price_rsi(df)
    else:
        return plot_signals(df)
    
def plot_signals(df, show_signals=True, show_indicators=True):
    fig = go.Figure()

    # Close price
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'],
        mode='lines', name='Close Price',
        line=dict(color='blue')
    ))

    # Buy/Sell signals
    if show_signals:
        fig.add_trace(go.Scatter(
            x=df[df['Signal'] == 1]['Date'], y=df[df['Signal'] == 1]['Close'],
            mode='markers', name='Buy',
            marker=dict(symbol='triangle-up', color='green', size=15)
        ))
        fig.add_trace(go.Scatter(
            x=df[df['Signal'] == -1]['Date'], y=df[df['Signal'] == -1]['Close'],
            mode='markers', name='Sell',
            marker=dict(symbol='triangle-down', color='red', size=15)
        ))

    # Technical indicators
    if show_indicators:
        if 'SMA_Short' in df.columns and 'SMA_Long' in df.columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_Short'], name='SMA Short', line=dict(color='cyan', dash='dot')))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_Long'], name='SMA Long', line=dict(color='orange', dash='dash')))
        elif 'EWMA_Short' in df.columns and 'EWMA_Long' in df.columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['EWMA_Short'], name='EWMA Short', line=dict(color='cyan', dash='dot')))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['EWMA_Long'], name='EWMA Long', line=dict(color='orange', dash='dash')))
        elif 'Upper_Breakout' in df.columns and 'Lower_Breakout' in df.columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Upper_Breakout'], name='Upper Breakout', line=dict(color='green', dash='dot')))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Lower_Breakout'], name='Lower Breakout', line=dict(color='red', dash='dot')))

    fig.update_layout(
        title="Price with Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode='x unified'
    )

    return fig

def plot_price_macd(df, show_signals=True):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
        subplot_titles=("Price with Buy/Sell Signals", "MACD")
    )

    # Price
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Close"], name="Close Price", line=dict(color="blue")
    ), row=1, col=1)

    if show_signals:
        fig.add_trace(go.Scatter(
            x=df[df["Signal"] == 1]["Date"], y=df[df["Signal"] == 1]["Close"],
            mode="markers", name="Buy", marker=dict(symbol="triangle-up", color="green", size=15)
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df[df["Signal"] == -1]["Date"], y=df[df["Signal"] == -1]["Close"],
            mode="markers", name="Sell", marker=dict(symbol="triangle-down", color="red", size=15)
        ), row=1, col=1)

    # MACD panel
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["MACD"], name="MACD", line=dict(color="purple")
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Signal_Line"], name="Signal Line", line=dict(color="gray", dash="dot")
    ), row=2, col=1)

    fig.update_layout(
        title="MACD Strategy Dashboard",
        height=700,
        hovermode="x unified"
    )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)

    return fig

def plot_price_rsi(df, show_signals=True):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
        subplot_titles=("Price with Buy/Sell Signals", "RSI")
    )

    # Price
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Close"], name="Close Price", line=dict(color="blue")
    ), row=1, col=1)

    if show_signals:
        fig.add_trace(go.Scatter(
            x=df[df["Signal"] == 1]["Date"], y=df[df["Signal"] == 1]["Close"],
            mode="markers", name="Buy", marker=dict(symbol="triangle-up", color="green", size=15)
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df[df["Signal"] == -1]["Date"], y=df[df["Signal"] == -1]["Close"],
            mode="markers", name="Sell", marker=dict(symbol="triangle-down", color="red", size=15)
        ), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["RSI"], name="RSI", line=dict(color="orange")
    ), row=2, col=1)

    # Thresholds
    fig.add_hline(y=70, line=dict(dash="dash", color="red"), row=2, col=1)
    fig.add_hline(y=30, line=dict(dash="dash", color="green"), row=2, col=1)

    fig.update_layout(
        title="RSI Strategy Dashboard",
        height=700,
        hovermode="x unified"
    )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="RSI (0-100)", row=2, col=1)

    return fig

def plot_drawdown(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Drawdown'], mode='lines',
                             name='Drawdown', line=dict(color='orange')))
    fig.update_layout(title='Drawdown Over Time', xaxis_title='Date', yaxis_title='Drawdown',
                      hovermode='x unified')
    return fig

def plot_return_histogram(df):
    fig = px.histogram(df, x='Strategy_Returns', nbins=50,
                       title='Histogram of Strategy Daily Returns',
                       labels={'Strategy_Returns': 'Daily Return',
                               'count': 'Frequency'},
                       color_discrete_sequence=['purple'])
    return fig
