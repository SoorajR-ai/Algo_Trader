<!DOCTYPE html>
<html lang="en">
<body>
    <h1>Algo Trader Bot</h1>
    <p>This project implements an Exponential Moving Average (EMA) crossover trading strategy using Python. The bot fetches historical stock data, calculates EMA crossovers, and logs trades into an Excel file.</p>
    <h2>Features</h2>
    <ul>
        <li>Retrieves historical stock data using the Yahoo Finance API.</li>
        <li>Calculates short-term and long-term EMAs.</li>
        <li>Identifies EMA crossovers for trade signals.</li>
        <li>Logs trade details to an Excel file without overwriting previous data.</li>
    </ul>
    <h2>Prerequisites</h2>
    <ul>
        <li>Python 3.7 or higher</li>
        <li><code>yfinance</code> library</li>
        <li><code>pandas</code> library</li>
        <li><code>numpy</code> library</li>
    </ul>
    <h2>Installation</h2>
    <ol>
        <li>Clone the repository:
            <pre><code>git clone https://github.com/SoorajR-ai/Algo_Trader.git</code></pre>
        </li>
        <li>Install the required dependencies:
            <pre><code>pip install yfinance pandas numpy</code></pre>
        </li>
    </ol>
    <h2>Usage</h2>
    <p>Run the trading bot script:</p>
    <pre><code>python trading_bot.py</code></pre>
    <p>The bot will fetch stock data, calculate EMA crossovers, and log trades to <code>trading_log.xlsx</code>.</p>
    <h2>Code Overview</h2>
    <p>The main script, <code>trading_bot.py</code>, contains the following key functions:</p>
    <ul>
        <li><code>calculate_ema_angle(ema_series)</code>: Calculates the angle of an EMA line.</li>
        <li><code>main()</code>: Main loop for running the strategy.</li>
        <li><code>EMA_cross_scanner(stock, index)</code>: Scans for EMA crossovers and logs trades.</li>
        <li><code>write_to_excel()</code>: Writes the trade log to an Excel file.</li>
    </ul>
    <h2>Contributing</h2>
    <p>Contributions are welcome! Please fork the repository and submit a pull request.</p>
    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>
    <h2>Contact</h2>
    <p>For any questions or issues, please open an issue in the GitHub repository>your.email@example.com</a>.</p>
</body>
</html>
