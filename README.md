# Tech News Sentiment Analysis

![Daily Pulse Automation](https://github.com/Karen2007/Tech-News-Sentiment/actions/workflows/daily_pulse.yaml/badge.svg)

Welcome to my project designed to monitor the "market mood" of the tech world. 
This project automates the collection of headlines and reports their sentiment score using 
tools to perform natural language processing.

---

## Project Overview
The system fetches real-time headlines from various news sources in the tech industry and calculates a sentiment index score 
by processing headlines through a multi-stage automated pipeline.

* **Data Sourcing**: Scrapes the latest headlines from [The Brutalist Report](https://brutalist.report).
* **Sentiment Engine**: Utilizes **FinBERT** (`ProsusAI/finbert`), a BERT model specifically pre-trained for high-accuracy sentiment classification 
* (positive/negative/neutral news).
* **Automation**: Runs every 3 hours via **GitHub Actions** to ensure the dataset remains 'relevant'.

## Technical Architecture
The project is split into three distinct phases:

1.  **Extraction (`scrape.py`)**: Fetches raw headline data and timestamps from 5 different sources on 
[The Brutalist Report](https://brutalist.report).
2.  **Data Handling (`handle_data.py`)**: Handles the fetched data, and transforms it into a CSV file, for the next step in the pipeline.
3. **Analysis (`analysis.py`)**: Processes text through the with the help of the `transformers` library to generate sentiment scores (Positive, Negative, Neutral).
After performing the analysis, uploads the newly obtained data into another CSV file called [`sentiment_index_history.csv`]
4. **Automation**: Repeats the process indefinitely and commits updated datasets to the repository:
    * `tech_sentiment_data.csv`: Latest raw sentiment results.
    * `sentiment_index_history.csv`: Historical aggregate data for trend analysis.

## Setup and Installation
To run this project locally, ensure you have Python 3.10+ installed:

```bash
# Clone the repository
git clone [https://github.com/Karen2007/Tech-News-Sentiment.git](https://github.com/Karen2007/Tech-News-Sentiment.git)

# Install dependencies (CPU-optimized for efficiency)
pip install -r requirements.txt

# Run the pipeline manually
python scrape.py && python analysis.py