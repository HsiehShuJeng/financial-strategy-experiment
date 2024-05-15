import matplotlib.pyplot as plt
import os
import utilities as ut


def plot_results(pandas_df):
    output_dir = "output/visualization"
    ut.check_dir(output_dir)
    # Plot the closing price and moving average
    plt.figure(figsize=(14, 7))
    plt.plot(pandas_df["date"], pandas_df["Close"], label="Closing Price")
    plt.plot(
        pandas_df["date"],
        pandas_df["moving_avg"],
        label="12-Month Moving Average",
        linestyle="--",
    )
    plt.xlabel("date")
    plt.ylabel("Price")
    plt.title("Closing Price and Moving Average")
    plt.legend()
    plt.savefig(
        os.path.join(os.getcwd(), f"{output_dir}/closing_price_and_moving_avg.png")
    )

    # Plot the cumulative returns
    plt.figure(figsize=(14, 7))
    plt.plot(
        pandas_df["date"],
        pandas_df["cumulative_return"],
        label="Cumulative Return",
        color="green",
    )
    plt.xlabel("date")
    plt.ylabel("Cumulative Return")
    plt.title("Cumulative Return of the Strategy")
    plt.legend()
    plt.savefig(os.path.join(os.getcwd(), f"{output_dir}/cumulative_return.png"))
