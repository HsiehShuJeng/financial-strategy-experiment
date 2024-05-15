from pyspark.sql import SparkSession


def calculate_moving_average(spark: SparkSession):
    query = """
        SELECT *,
               AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS moving_avg
        FROM stock_base
        ORDER BY `year` DESC, Date DESC
    """
    stock_with_moving_avg = spark.sql(query)
    stock_with_moving_avg.createOrReplaceTempView("stock_with_moving_avg")
    return stock_with_moving_avg


def add_actions(spark: SparkSession):
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
    returns_query = """
        SELECT *,
               CASE
                   WHEN action = 'sell' THEN (Close - LAG(Close, 1) OVER (PARTITION BY year ORDER BY Date)) * holdings
                   ELSE 0
               END AS daily_return
        FROM stock_with_strategy
        ORDER BY Date
    """
    result_with_returns = spark.sql(returns_query)
    result_with_returns.createOrReplaceTempView("stock_with_returns")

    cumulative_returns_query = """
        SELECT *,
               SUM(daily_return) OVER (ORDER BY Date) AS cumulative_return
        FROM stock_with_returns
        ORDER BY `year` DESC, Date DESC
    """
    result_with_cumulative_returns = spark.sql(cumulative_returns_query)
    return result_with_cumulative_returns
