import json
import re
from shlex import join
import requests
import unicodedata
from bs4 import BeautifulSoup as bs
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect
from deep_translator import GoogleTranslator

f = open('fonts.json')
data_fonts = json.load(f)

async def get_summarization(summarization):
    formatted_text = summarization.text if summarization.url is None else scraping_text(summarization.url)
    formatted_text = translate(formatted_text)
    stop_words = set(stopwords.words(str(summarization.language)))
    frequences_word = handle_frequence_word(stop_words, formatted_text)
    sentences = sent_tokenize(formatted_text)
    frequences_sentence = handle_sentences(frequences_word, sentences)
    return get_resume(frequences_sentence)
    
def scraping_text(url):
    response = requests.get(url)
    for data in data_fonts:
        if data in url:
           find, attrs, limit, children, attrs_children, limit_children = find_fields(data) 
    joined_text = handle_scraping(response, find, attrs, limit, children, attrs_children, limit_children) 
    return joined_text

def find_fields(field):
    find=data_fonts[field]['find_all']
    attrs=data_fonts[field]['attrs']
    limit=data_fonts[field]['limit']
    children=None
    attrs_children={}
    limit_children=10

    if data_fonts[field].get('children'):
        children = data_fonts[field]['children']['find_all']
        attrs_children = data_fonts[field]['children']['attrs']
        limit_children = data_fonts[field]['children']['limit']
    
    return find, attrs, limit, children, attrs_children, limit_children
    
def handle_scraping(response, find, attrs={}, limit=40, children=None, attrs_children={}, limit_children=10):
    soup = bs(response.content, 'lxml')
    result = soup.find_all(name=find, attrs= attrs, limit=limit)
    
    if children is not None:
        for r in result:
            child = r.find_all(name=children, attrs= attrs_children, limit=limit_children)
            joined_text = ''.join([p.text.strip().lower() for p in child])
    else:
        joined_text = ''.join([p.text.strip().lower() for p in result])
        
    joined_text = format_text(joined_text)
    return joined_text

def translate(text):
    lang_detect = detect(text.split('.')[0])
    
    if lang_detect == 'pt':
        return text
    
    text = GoogleTranslator(source=lang_detect, target='pt').translate(text)
    return text
    
def format_text(text):
    formatted_text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    formatted_text = re.sub(r'\[[0-9]*\]', ' ', formatted_text)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    return formatted_text

def handle_frequence_word(stop_words, text):
    words = word_tokenize(text)
    frequences_word = dict()
    for word in words:
        if word in stop_words:
            continue
        if word in frequences_word:
            frequences_word[word] += 1
        else:
            frequences_word[word] = 1
            
    return frequences_word

def handle_sentences(frequences_word, sentences):
    frequences_sentence = dict()
    for sentence in sentences:
        for word, freq in frequences_word.items():
            if word in sentence:
                if sentence in frequences_sentence:
                    frequences_sentence[sentence] += freq
                else:
                    frequences_sentence[sentence] = freq
    
    return frequences_sentence

def get_resume(frequences_sentence):
    select_lenght = int(len(frequences_sentence) * 0.3) # peso 30%
    summary = nlargest(select_lenght, frequences_sentence, key=frequences_sentence.get)
    final = [word for word in summary]
    summary = ''.join(final)
    return summary
    