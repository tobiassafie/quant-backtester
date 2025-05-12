import numpy as np
import pandas as pd

def calculate_metrics(df):
    # --- Basic Return Calculations ---
    df['Market_Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Market_Returns'] * df['Position'].shift(1)

    df['Cumulative_Market'] = (1 + df['Market_Returns']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()

    df['Cumulative_Market_Percent'] = (df['Cumulative_Market'] - 1.0) * 100
    df['Cumulative_Strategy_Percent'] = (df['Cumulative_Strategy'] - 1.0) * 100

    df['Outperformance'] = df['Cumulative_Strategy'] - df['Cumulative_Market']
    df['Daily_Outperformance'] = df['Strategy_Returns'] - df['Market_Returns']

    df = df.dropna()

    # --- Final Metrics ---
    final_strategy_return = (df['Cumulative_Strategy'].iloc[-1] - 1) * 100
    final_market_return = (df['Cumulative_Market'].iloc[-1] - 1) * 100

    strategy_volatility = np.std(df['Strategy_Returns']) * np.sqrt(252) * 100
    market_volatility = np.std(df['Market_Returns']) * np.sqrt(252) * 100

    strategy_sharpe = (np.mean(df['Strategy_Returns']) / np.std(df['Strategy_Returns'])) * np.sqrt(252)
    market_sharpe = (np.mean(df['Market_Returns']) / np.std(df['Market_Returns'])) * np.sqrt(252)

    df['Cumulative_Strategy_Rolling_Max'] = df['Cumulative_Strategy'].cummax()
    df['Drawdown'] = df['Cumulative_Strategy'] / df['Cumulative_Strategy_Rolling_Max'] - 1
    max_drawdown = abs(df['Drawdown'].min() * 100)

    downside_returns = df[df['Strategy_Returns'] < 0]['Strategy_Returns']
    sortino_ratio = (np.mean(df['Strategy_Returns']) / np.std(downside_returns)) * np.sqrt(252)

    gains = df[df['Strategy_Returns'] > 0]['Strategy_Returns'].sum()
    losses = df[df['Strategy_Returns'] < 0]['Strategy_Returns'].sum()
    profit_factor = gains / abs(losses) if losses != 0 else np.inf

    metrics = {
        'Metric': [
            'Final Strategy Return (%)',
            'Final Market Return (%)',
            'Strategy Volatility (%)',
            'Market Volatility (%)',
            'Max Drawdown (%)',
            'Strategy Sharpe Ratio',
            'Market Sharpe Ratio',
            'Sortino Ratio',
            'Profit Factor'
        ],
        'Value': [
            round(final_strategy_return, 2),
            round(final_market_return, 2),
            round(strategy_volatility, 2),
            round(market_volatility, 2),
            round(max_drawdown, 2),
            round(strategy_sharpe, 2),
            round(market_sharpe, 2),
            round(sortino_ratio, 2),
            round(profit_factor, 2)
        ]
    }

    metrics_df = pd.DataFrame(metrics)
    return df, metrics_df