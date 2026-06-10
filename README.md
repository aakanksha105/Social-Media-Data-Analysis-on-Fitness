# Social Media Data Analysis on Fitness

An end-to-end social media analytics project focused on collecting, processing, analyzing, and visualizing fitness-related discussions from Reddit and 4chan data. The project combines Python-based data ingestion, PostgreSQL/TimescaleDB storage, Docker-based setup, toxicity and sentiment analysis, exploratory data analysis, and a Flask dashboard to identify engagement patterns, toxicity trends, and topic-level insights from unstructured social media text.

## Key Highlights

- Collected Reddit and 4chan data using Python-based crawlers.
- Stored and managed social media data using PostgreSQL/TimescaleDB.
- Used Docker for database setup and project environment support.
- Added database migration support for structured data management.
- Processed unstructured text data for toxicity, sentiment, and engagement analysis.
- Performed exploratory, statistical, and time-series analysis.
- Built a Flask dashboard for interactive analysis views and visualization outputs.
- Organized the project across multiple phases with proposal, implementation, and report documentation.

## Tech Stack

- **Languages:** Python, HTML, CSS
- **Backend / Dashboard:** Flask
- **Database:** PostgreSQL, TimescaleDB
- **Data Processing:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Text Analysis:** NLP preprocessing, toxicity analysis, sentiment analysis
- **Infrastructure:** Docker, Faktory, Linux VM
- **Other:** SQL migrations, virtual environments, environment variables

## Project Structure

```text
Social-Media-Data-Analysis-on-Fitness/
│
├── project-1-implementation-datadrift-main-2/
│   └── Data collection, Reddit/4chan crawlers, PostgreSQL/TimescaleDB setup, Docker, migrations
│
├── project-2-implementation-datadrift-main/
│   └── Toxicity analysis, sentiment analysis, exploratory analysis, and visualization scripts
│
├── project-3-implementation-datadrift-main/
│   └── Flask dashboard, background processing, templates, static files, and analysis views
│
├── project-1-report-datadrift-main/
├── project-2-report-datadrift-main/
├── project-3-report-datadrift-main/
│   └── Project reports, analysis results, and findings
│
├── project-1-proposal-datadrift-main/
├── project-2-proposal-datadrift-main/
├── project-3-proposal-datadrift-main/
│   └── Project proposals and planning documentation
│
└── README.md
```

## Project Phases

### Phase 1: Data Collection and Storage

The first phase focuses on collecting social media data and setting up the backend storage environment.

Key components:

- Reddit client and crawler
- 4chan client and crawler
- PostgreSQL/TimescaleDB database setup
- Docker-based database environment
- SQL migration support
- Faktory-based background processing setup

### Phase 2: Toxicity, Sentiment, and Trend Analysis

The second phase focuses on analyzing collected social media text data and generating insights.

Analysis includes:

- Toxicity distribution across Reddit and 4chan posts
- Sentiment vs. engagement analysis
- Toxicity trends over time
- Daily submission trends
- Hourly comment activity analysis
- Combined toxicity comparison across datasets

### Phase 3: Flask Dashboard

The third phase adds an interactive Flask dashboard to make the analysis easier to explore.

Dashboard views include:

- Toxicity vs. engagement
- Sentiment over time
- Toxicity distribution
- Reddit toxicity over time

The dashboard allows users to select an analysis type, provide input parameters such as date ranges or comment ranges, and view the generated analysis output.

## Analysis Performed

- Cleaned and processed unstructured social media text data.
- Analyzed toxicity patterns across Reddit and 4chan discussions.
- Studied the relationship between toxicity and user engagement.
- Compared sentiment changes over time.
- Identified time-based posting and commenting behavior.
- Created visualizations to support trend analysis and reporting.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/aakanksha105/Social-Media-Data-Analysis-on-Fitness.git
cd Social-Media-Data-Analysis-on-Fitness
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env/dev
source env/dev/bin/activate
```

### 3. Install Dependencies

Navigate to the relevant implementation folder and install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL/TimescaleDB with Docker

```bash
docker pull timescale/timescaledb-ha:pg16
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=testpassword timescale/timescaledb-ha:pg16
```

### 5. Run Analysis Scripts

For toxicity and sentiment analysis:

```bash
python3 Analysis.py
```

### 6. Run the Flask Dashboard

Navigate to the Project 3 implementation folder and run:

```bash
python3 background.py
python3 app.py
```

Then open the local Flask URL shown in the terminal:

```text
http://127.0.0.1:5000/
```

## Results and Insights

This project helps identify:

- Toxicity patterns in Reddit and 4chan fitness discussions
- Relationship between toxicity and engagement
- Sentiment changes over time
- Time-based posting and commenting trends
- Differences in discussion behavior across social media platforms
- Topic-level insights from fitness-related online conversations

## Learning Outcomes

Through this project, I gained hands-on experience in:

- Building end-to-end data analytics workflows
- Working with social media data from multiple sources
- Managing PostgreSQL/TimescaleDB environments with Docker
- Processing unstructured text data using Python
- Performing toxicity, sentiment, and engagement analysis
- Creating exploratory and time-series visualizations
- Building a Flask dashboard for interactive data exploration

## Future Improvements

- Add dashboard screenshots and sample visualizations.
- Add sample or mock data for easier local testing.
- Improve setup instructions for environment variables.
- Add automated tests for analysis and dashboard components.
- Improve error handling in data ingestion workflows.
- Deploy the Flask dashboard to a public hosting platform.

## Author

Aakanksha Bhondve
