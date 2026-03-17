import pandas as pd
from datetime import datetime
import os


def save_to_csv(data_frame):
    """
    Takes a list of dictionaries and saves it to a CSV.
    """

    file_path = 'tech_sentiment_data.csv'

    with open(file=file_path, mode='w', encoding='utf-8') as f:
        f.truncate()
        f.write('headline,source,link,datetime')
        data_frame.to_csv(file_path, mode='a', index=False)

    return None