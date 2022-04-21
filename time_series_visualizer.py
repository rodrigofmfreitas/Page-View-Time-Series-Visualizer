import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(r"D:\digof\Documents\git\learning-python\boilerplate-page-view-time-series-visualizer-1\fcc-forum-pageviews.csv", parse_dates = ["date"], index_col = "date")
#df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates = ["date"], index_col = "date")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    fig, axes = plt.subplots(figsize = (30, 10))

    axes.plot(df.index, df["value"], "r")
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    axes.set_xlabel("Date")
    axes.set_ylabel("Page Views")




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.rename(columns = {"value": "Average Page Views"})
    df_bar["Years"] = df_bar.index.year
    df_bar["Months"] = df_bar.index.month_name()
    df_bar = df_bar.groupby(["Years", "Months"], sort = False)["Average Page Views"].mean()
    df_bar = df_bar.reset_index()

    # Need to fix the start of the first year, otherwise the label order gets messed up.
    fixing_month_problem = {"Years": [2016, 2016, 2016, 2016], "Months": ['January', 'February', 'March', 'April'], "Average Page Views": [0, 0, 0, 0]}
    df_fix = pd.DataFrame(fixing_month_problem)
    df_bar = pd.concat([df_fix, df_bar])

    # Draw bar plot
    fig, axes = plt.subplots(figsize = (10, 10))
    sns.barplot(x = "Years", y = "Average Page Views", hue = "Months", data = df_bar, palette = sns.color_palette())

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    box_plot = plt.subplots(nrows = 1, ncols = 2, figsize = (20, 10))
    fig, (ax1, ax2) = box_plot

    # Left boxplot
    sns.boxplot(x = "year", y = "value", ax = ax1, data = df_box)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Right boxplot
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(x = "month", y = "value", ax = ax2, order = months, data = df_box)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
