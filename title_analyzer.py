import spacy
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
import transformers
import re

# This file should determine whether an article title contains any words relevant to stocks
# The stock code, its price, the date of the article, and the prediction is recorded.

# load large pretrained English language model
nlp = spacy.load('en_core_web_lg')

# use finbert for identifying stock-related topics/words
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

finance_keywords = ["acquisition", "analysis", "dividends", 
                    "earnings", "economy", "forecast", 
                    "growth", "hedge", "invest", "IPO", 
                    "market", "price", "revenue", "stock", 
                    "trading", "valuation"]

def relevant(some_title):
    doc = nlp(some_title.lower().strip())
    org_entities = any(ent.label_ == 'ORG' for ent in doc.ents)
    has_finance_words = any(word in some_title for word in finance_keywords)

    return (org_entities and has_finance_words)

print(relevant('Meta stocks increase'))