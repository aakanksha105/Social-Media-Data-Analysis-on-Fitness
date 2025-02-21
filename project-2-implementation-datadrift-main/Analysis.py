import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

def fetch_data(query):
    """Fetch data from PostgreSQL using SQLAlchemy."""
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

def preprocess_4chan_dates(data, date_column):
    """Preprocess 4chan created_at dates to a standard format."""
    try:
        # Extract date and time portion, ignoring unnecessary text like (Tue)
        data[date_column] = data[date_column].str.extract(r'(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2})')[0]
        data[date_column] = pd.to_datetime(data[date_column], format='%m/%d/%Y %H:%M:%S', errors='coerce')
        return data
    except Exception as e:
        print(f"Error preprocessing 4chan dates: {e}")
        return data

def plot_histogram(data, column, title, xlabel, ylabel, filename):
    """Plot histogram of a given column."""
    plt.hist(data[column].dropna(), bins=20, alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plot_scatter(data, x_column, y_column, title, xlabel, ylabel, filename):
    """Plot scatter plot of given columns."""
    plt.scatter(data[x_column], data[y_column], alpha=0.6)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plot_line_graph(data, date_column, value_column, title, xlabel, ylabel, filename, binning='D'):
    """Plot line graph showing trends over time."""
    if data.empty:
        print(f"Data for {title} is empty. Skipping plot generation.")
        return

    if date_column not in data or (value_column and value_column not in data):
        print(f"Missing columns in data for {title}. Skipping plot generation.")
        return

    try:
        data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        data = data.dropna(subset=[date_column])

        if data.empty:
            print(f"No valid data for {title} after cleaning. Skipping plot generation.")
            return

        if value_column:
            time_series = data.set_index(date_column).resample(binning)[value_column].mean()
        else:
            time_series = data.set_index(date_column).resample(binning).size()

        time_series.plot()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
        print(f"Plot saved as {filename}")
    except Exception as e:
        print(f"Error generating plot for {title}: {e}")

def plot_combined_datasets(data_4chan, data_reddit, data_reddit_politics_posts, data_reddit_politics_comments):
    """
    Plot all datasets on the same axes to compare toxicity scores across datasets.
    """
    # Add a source label to each dataset
    data_4chan['source'] = '4chan'
    data_reddit['source'] = 'Reddit'
    data_reddit_politics_posts['source'] = 'Reddit Politics Posts'
    data_reddit_politics_comments['source'] = 'Reddit Politics Comments'

    # Combine all datasets
    combined_data = pd.concat(
        [data_4chan, data_reddit, data_reddit_politics_posts, data_reddit_politics_comments],
        ignore_index=True
    )

    # Remove rows with missing toxicity scores
    combined_data = combined_data.dropna(subset=['toxicity'])

    # Plot the combined data
    plt.figure(figsize=(18, 10))  # Increase figure size for better visualization
    bins = 50  # Increase the number of bins for a detailed histogram
    range_values = (0, 20)  # Extend the x-axis range for a wider display

    for source, group in combined_data.groupby('source'):
        plt.hist(
            group['toxicity'],
            bins=bins,
            range=range_values,  # Control the x-axis range
            alpha=0.6,
            label=source,
            density=True  # Normalize histogram
        )

    # Add labels, legend, and grid
    plt.title('Toxicity Score Distribution Across All Datasets', fontsize=16)
    plt.xlabel('Toxicity Score', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc='upper right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the figure
    filename = 'combined_toxicity_comparison.png'
    plt.savefig(filename)
    plt.close()
    print(f"Combined toxicity comparison plot saved as {filename}")

def plot_politics_submissions_daily(data, date_column, filename):
    """Plot daily submissions in r/politics."""
    try:
        data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        data = data.dropna(subset=[date_column])
        daily_counts = data.set_index(date_column).resample('D').size()

        daily_counts.plot(kind='bar', figsize=(14, 7), color='skyblue')
        plt.title('Daily Submissions in r/politics (Nov 1, 2024 - Nov 14, 2024)', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Number of Submissions', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(filename)
        plt.close()
        print(f"Daily submissions plot saved as {filename}")
    except Exception as e:
        print(f"Error generating daily submissions plot: {e}")

def plot_politics_comments_hourly(data, date_column, filename):
    """Plot hourly comments in r/politics."""
    try:
        data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        data = data.dropna(subset=[date_column])
        hourly_counts = data.set_index(date_column).resample('H').size()

        hourly_counts.plot(kind='line', figsize=(14, 7), color='green')
        plt.title('Hourly Comments in r/politics (Nov 1, 2024 - Nov 14, 2024)', fontsize=16)
        plt.xlabel('Hour', fontsize=14)
        plt.ylabel('Number of Comments', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(filename)
        plt.close()
        print(f"Hourly comments plot saved as {filename}")
    except Exception as e:
        print(f"Error generating hourly comments plot: {e}")

def plot_4chan_comments_hourly(data, date_column, filename):
    """Plot hourly comments in 4chan’s /pol/."""
    try:
        data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
        data = data.dropna(subset=[date_column])
        hourly_counts = data.set_index(date_column).resample('H').size()

        hourly_counts.plot(kind='line', figsize=(14, 7), color='red')
        plt.title('Hourly Comments in 4chan’s /pol/ (Nov 1, 2024 - Nov 14, 2024)', fontsize=16)
        plt.xlabel('Hour', fontsize=14)
        plt.ylabel('Number of Comments', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(filename)
        plt.close()
        print(f"Hourly comments plot saved as {filename}")
    except Exception as e:
        print(f"Error generating hourly comments plot: {e}")


def analyze_and_visualize():
    """Perform all required analyses and generate figures."""
    # Fetch data from database
    query_reddit = """
        SELECT id, title AS content, created_utc, num_comments
        FROM reddit_posts
        WHERE created_utc BETWEEN '2024-11-01' AND '2024-11-14';
    """
    query_reddit_politics_posts = """
        SELECT post_id, title AS content, created_utc
        FROM reddit_politics_posts
        WHERE created_utc BETWEEN '2024-11-01' AND '2024-11-14';
    """
    query_reddit_politics_comments = """
        SELECT post_id, content AS content, created_utc
        FROM reddit_politics_comments
        WHERE created_utc BETWEEN '2024-11-01' AND '2024-11-14';
    """
    query_4chan = """
        SELECT id, data->>'com' AS content, "data"->>'now' AS created_at
        FROM posts
        WHERE "data"->>'now' BETWEEN '11/01/2024' AND '11/14/2024'
        AND board = 'fit';
    """
    
    reddit_data = fetch_data(query_reddit)
    reddit_politics_posts = fetch_data(query_reddit_politics_posts)
    reddit_politics_comments = fetch_data(query_reddit_politics_comments)
    fourchan_data = fetch_data(query_4chan)
    # fourchan_data_pol = fetch_data(query_4chan_pol)

    # Preprocess 4chan dates
    fourchan_data = preprocess_4chan_dates(fourchan_data, 'created_at')

    # Add mock toxicity data for demonstration
    reddit_data['toxicity'] = reddit_data['content'].str.len() / 100
    reddit_politics_posts['toxicity'] = reddit_politics_posts['content'].str.len() / 100
    reddit_politics_comments['toxicity'] = reddit_politics_comments['content'].str.len() / 100
    fourchan_data['toxicity'] = fourchan_data['content'].str.len() / 100

    # Plot Histogram of Toxicity
    plot_histogram(reddit_data, 'toxicity', 'Reddit Toxicity Distribution', 'Toxicity Score', 'Count', 'reddit_toxicity_histogram.png')
    plot_histogram(fourchan_data, 'toxicity', '4chan Toxicity Distribution', 'Toxicity Score', 'Count', '4chan_toxicity_histogram.png')

    # Plot Scatter Plot of Sentiment vs Engagement
    plot_scatter(reddit_data, 'toxicity', 'num_comments', 'Sentiment vs Engagement (Reddit)', 'Toxicity Score', 'Number of Comments', 'sentiment_engagement_scatter.png')

    # Plot Line Graph of Toxicity Over Time
    plot_line_graph(reddit_data, 'created_utc', 'toxicity', 'Reddit Toxicity Over Time', 'Date', 'Average Toxicity', 'reddit_toxicity_over_time.png')
    plot_line_graph(fourchan_data, 'created_at', 'toxicity', '4chan Toxicity Over Time', 'Date', 'Average Toxicity', '4chan_toxicity_over_time.png')

    # Plot Combined Toxicity Comparison
    plot_combined_datasets(fourchan_data, reddit_data, reddit_politics_posts, reddit_politics_comments)

    # Additional Required Plots
    plot_politics_submissions_daily(reddit_politics_posts, 'created_utc', 'daily_submissions_politics.png')
    plot_politics_comments_hourly(reddit_politics_comments, 'created_utc', 'hourly_comments_politics.png')
    #plot_4chan_comments_hourly(fourchan_data_pol, 'created_at', 'hourly_comments_pol.png')

    print("Figures generated successfully!")

if __name__ == "__main__":
    analyze_and_visualize()
