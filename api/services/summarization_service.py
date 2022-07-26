import re
import requests
import unicodedata
from bs4 import BeautifulSoup as bs
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

async def get_summarization(summarization):
    formatted_text = summarization.text if summarization.url is None else scraping_text(summarization.url)
    stop_words = set(stopwords.words(str(summarization.language)))
    frequences_word = handle_frequence_word(stop_words, formatted_text)
    sentences = sent_tokenize(formatted_text)
    frequences_sentence = handle_sentences(frequences_word, sentences)
    return get_resume(frequences_sentence)
    
def scraping_text(url):
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    paragraph = soup.find_all(name='p', attrs= {"class": "pw-post-body-paragraph"}, limit=40)
    joined_text = ''.join([p.text.strip().lower() for p in paragraph])
    joined_text = format_text(joined_text)
    return joined_text

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
    