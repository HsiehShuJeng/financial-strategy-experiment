from pyspark.sql import SparkSession


def calculate_moving_average(spark: SparkSession):
    """
    Calculate the 12-month moving average for the stock prices.

    Args:
        spark (SparkSession): The Spark session.

    Returns:
        DataFrame: A Spark DataFrame containing the stock data with the calculated moving average.
    """
    query = """
        SELECT *,
            AVG(close) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS moving_avg
        FROM stock_base
        ORDER BY `date` DESC
    """
    stock_with_moving_avg = spark.sql(query)
    stock_with_moving_avg.createOrReplaceTempView("stock_with_moving_avg")
    return stock_with_moving_avg


def add_actions(spark: SparkSession):
    """
    Add buy/sell actions based on the closing price and the moving average.

    Args:
        spark (SparkSession): The Spark session.

    Returns:
        DataFrame: A Spark DataFrame containing the stock data with added action column.
    """
    actions_query = """
        SELECT *,
               CASE
                   WHEN Close >= moving_avg THEN 'buy'
                   WHEN Close < moving_avg THEN 'sell'
                   ELSE ''
               END AS action,
               0 AS initial_holdings
        FROM stock_with_moving_avg
    """
    result_with_actions = spark.sql(actions_query)
    result_with_actions.createOrReplaceTempView("stock_with_actions")
    return result_with_actions


def update_holdings(spark: SparkSession):
    """
    Update holdings based on the buy/sell actions.

    Args:
        spark (SparkSession): The Spark session.

    Returns:
        DataFrame: A Spark DataFrame containing the stock data with updated holdings.
    """
    holdings_query = """
        SELECT *,
               SUM(CASE
                       WHEN action = 'buy' THEN 1
                       WHEN action = 'sell' THEN -1
                       ELSE 0
                   END) OVER (ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS holdings
        FROM stock_with_actions
        ORDER BY `year` DESC, Date DESC
    """
    result_with_strategy = spark.sql(holdings_query)
    result_with_strategy.createOrReplaceTempView("stock_with_strategy")
    return result_with_strategy


def calculate_returns(spark: SparkSession):
    """
    Calculate monthly and cumulative returns based on the buy/sell actions and holdings.

    Args:
        spark (SparkSession): The Spark session.

    Returns:
        DataFrame: A Spark DataFrame containing the stock data with calculated monthly and cumulative returns.
    """
    returns_query = """
        SELECT *,
               CASE
                   WHEN action = 'sell' THEN (close - LAG(close, 1) OVER (ORDER BY date)) * holdings
                   ELSE 0
               END AS monthly_return
        FROM stock_with_strategy
        ORDER BY date
    """
    result_with_returns = spark.sql(returns_query)
    result_with_returns.createOrReplaceTempView("stock_with_returns")

    cumulative_returns_query = """
        SELECT *,
               SUM(monthly_return) OVER (ORDER BY date) AS cumulative_return
        FROM stock_with_returns
        ORDER BY year DESC, date DESC
    """
    result_with_cumulative_returns = spark.sql(cumulative_returns_query)
    return result_with_cumulative_returns
