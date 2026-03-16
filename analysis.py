import pandas as pd
import os

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from datetime import datetime, UTC

model_name = 'ProsusAI/finbert'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name) # Load the tokenizer and model


nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer) # Create the pipeline

data = pd.read_csv('tech_sentiment_data.csv')
sentences = list(data['headline']) # Get all the headlines

results = nlp(sentences)

# Scores
sentiment_index_score = 0
negative_count = 0
positive_count = 0
neutral_count = 0

for sentence, result in zip(sentences, results):
    print(f'Sentence: {sentence}')
    print(f'Sentiment: {result["label"]}, Score: {round(result["score"], 4)}\n')
    if result['label'] == 'negative':
        sentiment_index_score -= round(result['score'], 4)
        negative_count += 1
    elif result['label'] == 'positive':
        sentiment_index_score += round(result['score'], 4)
        positive_count += 1
    else:
        neutral_count += 1


total_headlines = len(results)

if total_headlines > 0:
    average_sentiment_score = sentiment_index_score / total_headlines
    print(f"Total Headlines: {total_headlines}")
    print(f"Global Sentiment Index: {round(average_sentiment_score, 4)}")


def create_sentiment_report():

    current_hour = datetime.now(UTC).hour # Current universal time
    hour_start = current_hour - (current_hour % 3)
    hour_end = (hour_start + 3) % 24

    df = pd.DataFrame({
        'date' :                  [datetime.now().date()],
        'weekday' :               [datetime.now().strftime('%A')],
        'hour_start' :            [hour_start],
        'hour_end' :              [hour_end],
        'headline_count' :        [total_headlines],
        'positive_count' :        [positive_count],
        'negative_count' :        [negative_count],
        'neutral_count' :         [neutral_count],
        'sentiment_index_score' : [round(average_sentiment_score, 4)]
    })

    file_path = 'sentiment_index_history.csv'
    file_exists = os.path.isfile(file_path)
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)

    return None

if __name__ == '__main__':
    create_sentiment_report()