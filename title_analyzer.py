import spacy
from transformers import pipeline
import re

# This file should determine whether an article title contains any words relevant to stocks
# The stock code, its price, the date of the article, and the prediction is recorded.
# check if any 

#
nlp = spacy.load('en_core_web_sm')