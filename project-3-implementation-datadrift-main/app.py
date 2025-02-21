from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fetch data from the database
def fetch_data(query):
    """Fetch data from PostgreSQL using SQLAlchemy."""
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

# Generate data for Reddit Toxicity Over Time
def generate_reddit_toxicity_over_time(start_date, end_date, min_comments, max_comments):
    """Fetch and filter Reddit posts based on date range and comment count."""
    query = f"""
        SELECT post_id, title AS content, created_utc, num_comments
        FROM reddit_posts
        WHERE created_utc BETWEEN '{start_date}' AND '{end_date}'
          AND num_comments BETWEEN {min_comments} AND {max_comments}
    """
    data = fetch_data(query)
    data['created_utc'] = pd.to_datetime(data['created_utc'], errors='coerce')
    data['toxicity'] = data['content'].str.len() / 100  
    return data

# Function to plot Reddit Toxicity Over Time
def plot_reddit_toxicity_over_time(data):
    """Plot Reddit toxicity trends over time with proper date formatting."""
    if data.empty:
        return None  
    
    data.set_index('created_utc', inplace=True)
    time_series = data.resample('D')['toxicity'].mean()  
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_series.index, time_series.values, color='blue', marker='o')
    plt.title('Reddit Toxicity Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Toxicity')
    plt.grid(True)

    # Format the x-axis to show dates clearly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  
    plt.xticks(rotation=45)  

    # Adjust layout to prevent cutoff
    plt.tight_layout(pad=2.0)
    
    filename = 'reddit_toxicity_over_time.png'
    plt.savefig(f'static/{filename}')
    plt.close()
    return filename

# Function to generate analysis data
def generate_analysis(start_date, end_date):
    """Generate analysis with varying dates."""
    query = f"""
        SELECT post_id, title AS content, created_utc, num_comments
        FROM reddit_posts
        WHERE created_utc BETWEEN '{start_date}' AND '{end_date}'
    """
    data = fetch_data(query)
    data['toxicity'] = data['content'].str.len() / 100  
    data['engagement'] = data['num_comments']  
    return data

# Function to plot Toxicity vs Engagement
def plot_toxicity_vs_engagement(data):
    """Plot Toxicity vs Engagement."""
    plt.scatter(data['toxicity'], data['engagement'])
    plt.title('Toxicity vs Engagement')
    plt.xlabel('Toxicity')
    plt.ylabel('Engagement')
    plt.grid(True)
    filename = 'toxicity_vs_engagement.png'  
    plt.savefig(f'static/{filename}')        
    plt.close()
    return filename  

# Function to plot Sentiment Trends Over Time
def plot_sentiment_over_time(data, date_column='created_utc'):
    """Plot Sentiment Over Time."""
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    time_series = data.set_index(date_column).resample('D').size()
    time_series.plot(kind='line')
    plt.title('Sentiment Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.grid(True)
    filename = 'sentiment_over_time.png'  
    plt.savefig(f'static/{filename}')     
    plt.close()
    return filename  

# Function to plot Toxicity Distribution
def plot_toxicity_distribution(data):
    """Plot Toxicity Distribution."""
    plt.hist(data['toxicity'].dropna(), bins=20, alpha=0.7)
    plt.title('Toxicity Distribution')
    plt.xlabel('Toxicity')
    plt.ylabel('Count')
    plt.grid(True)
    filename = 'toxicity_distribution.png'  
    plt.savefig(f'static/{filename}')       
    plt.close()
    return filename  

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analysis
@app.route('/analysis/<analysis_type>', methods=['GET', 'POST'])
def analysis(analysis_type):
    if request.method == 'POST':
        
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        min_comments = int(request.form.get('min_comments', 0))
        max_comments = int(request.form.get('max_comments', 1000))

        # Generate data for the analysis
        if analysis_type == 'reddit_toxicity_over_time':
            data = generate_reddit_toxicity_over_time(start_date, end_date, min_comments, max_comments)
            plot_url = plot_reddit_toxicity_over_time(data)
        elif analysis_type == 'toxicity_vs_engagement':
            data = generate_analysis(start_date, end_date)
            plot_url = plot_toxicity_vs_engagement(data)
        elif analysis_type == 'sentiment_over_time':
            data = generate_analysis(start_date, end_date)
            plot_url = plot_sentiment_over_time(data)
        elif analysis_type == 'toxicity_distribution':
            data = generate_analysis(start_date, end_date)
            plot_url = plot_toxicity_distribution(data)
        else:
            return f"Analysis type '{analysis_type}' is not recognized.", 400

        # Pass the filename to the template
        return render_template(
            'analysis.html',
            analysis_type=analysis_type,
            plot_url=plot_url,
            start_date=start_date,
            end_date=end_date,
            min_comments=min_comments,
            max_comments=max_comments,
        )

    return render_template('analysis.html', analysis_type=analysis_type)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
