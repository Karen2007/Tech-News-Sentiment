from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd

model_name = 'ProsusAI/finbert'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name) # Load the tokenizer and model


nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer) # Create the pipeline

data = pd.read_csv('tech_sentiment_data.csv')
sentences = list(data['headline'])

results = nlp(sentences)

sentiment_score = 0

for sentence, result in zip(sentences, results):
    print(f'Sentence: {sentence}')
    print(f'Sentiment: {result["label"]}, Score: {round(result["score"], 4)}\n')
    if result['label'] == 'negative':
        sentiment_score -= round(result['score'], 4)
    elif result['label'] == 'positive':
        sentiment_score += round(result['score'], 4)


total_headlines = len(results)
if total_headlines > 0:
    average_sentiment = sentiment_score / total_headlines
    print(f"Total Headlines: {total_headlines}")
    print(f"Global Sentiment Index: {round(average_sentiment, 4)}")