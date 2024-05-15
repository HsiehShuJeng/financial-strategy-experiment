import matplotlib.pyplot as plt
import pandas as pd
import utilities as ut
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, to_date, year
import preparation
import transformation
import visualization


def main():
    ticker = "00631L.TW"
    file_path = "00631L_monthly_data.csv"

    ut.search_ticker(ticker)

    monthly_data = preparation.fetch_monthly_data(ticker)
    preparation.save_to_csv(monthly_data, file_path)

    spark = SparkSession.builder.appName("Backtesting 00631L Strategy").getOrCreate()

    preparation.load_and_prepare_data(spark, file_path)
    transformation_dir = "transformation"
    ut.check_dir(transformation_dir)
    stock_with_moving_avg = transformation.calculate_moving_average(spark)
    stock_with_moving_avg.show(truncate=1000)
    # partition = 1
    stock_with_moving_avg.repartition(1).write.csv(
        f"{transformation_dir}/stock_with_moving_avg", mode="overwrite"
    )

    result_with_actions = transformation.add_actions(spark)
    result_with_actions.repartition(1).write.csv(
        f"{transformation_dir}/result_with_actions", mode="overwrite"
    )
    result_with_strategy = transformation.update_holdings(spark)
    result_with_strategy.repartition(1).write.csv(
        f"{transformation_dir}/result_with_strategy", mode="overwrite"
    )
    result_with_cumulative_returns = transformation.calculate_returns(spark)
    result_with_cumulative_returns.repartition(1).write.csv(
        f"{transformation_dir}/result_with_cumulative_returns", mode="overwrite"
    )
    pandas_df = result_with_cumulative_returns.toPandas()
    print(pandas_df.head(10))
    visualization.plot_results(pandas_df)


if __name__ == "__main__":
    main()
