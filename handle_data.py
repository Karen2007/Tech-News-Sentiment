import pandas as pd
from datetime import datetime
import os


def save_to_csv(data_list):
    """
    Takes a list of dictionaries and saves it to a CSV.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for unit in data_list:
        raw_headline = unit.get('headline', '')
        unit['headline'] = raw_headline.replace('\xa0', ' ').replace('&nbsp;', ' ') # Replace weird &nbsp; characters
        unit['datetime'] = now # Add a datetime column to the data frame

    df = pd.DataFrame(data_list)
    file_path = 'tech_sentiment_data.csv'
    file_exists = os.path.isfile(file_path)
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)

    return df