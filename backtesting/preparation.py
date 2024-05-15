import yfinance as yf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year


def fetch_monthly_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")

    monthly_data = (
        hist.resample("ME")
        .agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }
        )
        .dropna()
    )

    return monthly_data


def save_to_csv(data, filename):
    data.to_csv(filename, index=True)


def load_and_prepare_data(spark: SparkSession, file_path: str) -> None:
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df = df.withColumn("date", to_date(col("Date"), "yyyy-MM-dd"))
    df = df.withColumn("year", year("date"))
    df.createOrReplaceTempView("stock_base")
