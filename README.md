# financial-strategy-experiment


## Development
```bash
python -m venv .venv
source .venv/bin/activate

jupyter lab
jupyter lab build
```

## Local installation
1. install 
    ```bash
    curl -O https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
    tar -xzf spark-3.5.1-bin-hadoop3.tgz
    if [ ! -d "/opt/spark" ]; then
        sudo mkdir -p /opt/spark
    fi
    sudo mv spark-3.5.1-bin-hadoop3 /opt/spark
    sudo mv /opt/spark/spark-3.5.1-bin-hadoop3/* /opt/spark/
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.13/3.5.1/spark-hadoop-cloud_2.13-3.5.1.jar && sudo mv spark-hadoop-cloud_2.13-3.5.1.jar /opt/spark/jars
    ```
2. set up envs in `~/.bash_profile` or similar file.
    edit
    ```text
    # set up envs
    export SPARK_HOME=/opt/spark
    export PATH=$SPARK_HOME/bin:$PATH
    ```
    source
    ```bash
    source ~/.bash_profile
    ```

## Execution
```python
cd backtesting
pyhon backtesting.py
```
After executing, its generated output will be similar as the following under the directory of `backtesting`:
```bash
.
├── 00631L_monthly_data.csv
├── __pycache__
│   ├── preparation.cpython-312.pyc
│   ├── transformation.cpython-312.pyc
│   ├── utilities.cpython-312.pyc
│   └── visualization.cpython-312.pyc
├── output
│   ├── transformation
│   │   ├── _SUCCESS
│   │   └── part-00000-cce2f9b7-4d06-478c-8bae-8a2d3215fcaf-c000.csv
│   └── visualization
│       ├── closing_price_and_moving_avg.png
│       └── cumulative_return.png
├── transformation
│   ├── result_with_actions
│   │   ├── _SUCCESS
│   │   └── part-00000-6b68ae81-1c0b-487a-baf4-066ca560f642-c000.csv
│   ├── result_with_cumulative_returns
│   │   ├── _SUCCESS
│   │   └── part-00000-e63504c6-099c-4b18-b39b-4523ad1bc21e-c000.csv
│   ├── result_with_strategy
│   │   ├── _SUCCESS
│   │   └── part-00000-c6447829-0e24-4fa2-9d0f-a53227ea2390-c000.csv
│   └── stock_with_moving_avg
│       ├── _SUCCESS
│       └── part-00000-04076d84-18a8-4894-8e99-43eedeebb1ad-c000.csv
```

## Thoughts
1. **Calculating Moving Average**
    * Defined a SQL query to calculate the 12-month moving average of the closing prices.
    * Created a temporary view for the data with the calculated moving average.
2. **Defining Actions**
    * Added a column to define actions (buy, sell, or hold) based on the comparison between the closing price and the moving average.
3. **Updating Holdings**
    * Calculated the cumulative holdings based on the buy/sell actions.
    * Defined a window function to sum the holdings over time.
4. **Calculating Returns**
    * Calculated returns based on the difference between current and previous closing prices when a sell action is performed.
    * Computed cumulative returns to assess the overall performance of the strategy.

## Steps to Improve and Validate the Strategy
1. **Experiment with Parameters**  
    Try different lengths for the moving average and see how they impact performance.
2. **Include Transaction Costs**  
    Incorporate realistic transaction costs into your backtesting to get a more accurate picture of potential returns.
3. **Test on Different Timeframes**
    Backtest the strategy on different historical periods to see if the results are consistent.
4. **Analyze Drawdowns**
    Look at the drawdowns (peak-to-trough declines) to understand the risk profile of the strategy.
5. **Compare with Benchmarks**  
    Compare the strategy’s performance with a relevant benchmark, like a buy-and-hold strategy, to evaluate its relative performance.
6. **Robustness Testing** 
    Use techniques like walk-forward optimization and Monte Carlo simulation to test the robustness of the strategy.