import random
import json
import urllib.request
import re
from bs4 import BeautifulSoup
import requests

def fetch_from_random_word_generator_dot_com():
    """Extracts a random word from randomwordgenerator.com's data source."""
    url = "https://randomwordgenerator.com/json/words_ws.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            word_list = data.get("data", [])
            if word_list:
                return random.choice(word_list)["word"]["value"]
            return None
    except Exception:
        return None

def fetch_merriam_webster_data(word):
    """Scrapes definition, synonyms, examples, phrases, and audio from Merriam-Webster."""
    if not word: return None
    
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
            
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'word': word}
        
        # 1. Definitions (Top 3)
        def_elements = soup.select('.vg .dtText')
        definitions = []
        for el in def_elements[:3]:
            text = el.get_text().strip()
            if text.startswith(':'):
                text = text[1:].strip()
            definitions.append(text)
        
        data['definitions'] = definitions if definitions else ["Definition not found."]

        # 2. Synonyms (Top 5)
        syn_elements = soup.select('#synonyms .mw-grid-table-list li a')[:5]
        data['synonyms'] = [syn.get_text().strip() for syn in syn_elements]

        # 3. Examples (Top 3)
        ex_elements = soup.select('#examples .ex-sent')[:3]
        data['examples'] = [ex.get_text().strip() for ex in ex_elements]

        # 4. Phrases Containing (Top 5)
        phrase_links = soup.select('#related-phrases .related-phrases-list-item a')[:5]
        data['phrases'] = [phrase.get_text().strip() for phrase in phrase_links]

        # 5. Audio Pronunciation
        audio_btn = soup.select_one('.play-pron-v2')
        if audio_btn:
            data_file = audio_btn.get('data-file')
            if data_file:
                subdir = data_file[0]
                if data_file.startswith('bix'): subdir = 'bix'
                elif data_file.startswith('gg'): subdir = 'gg'
                elif re.match(r'^\d', data_file) or data_file.startswith('_'): subdir = 'number'
                
                audio_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{data_file}.mp3"
                data['audio_url'] = audio_url
            else:
                data['audio_url'] = None
        else:
            data['audio_url'] = None

        return data

    except Exception as e:
        return {"error": str(e)}

def fetch_related_images(word):
    """Scrapes top 3 related images from Yahoo Images."""
    if not word: return None
    
    url = f"https://images.search.yahoo.com/search/images?p={word}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return ["Error fetching images."]
            
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.select('.rs-img-cntr img')
        
        image_urls = []
        for img in images[:3]:
            src = img.get('src')
            if not src:
                src = img.get('data-src') 
            if src:
                image_urls.append(src)
                
        return image_urls if image_urls else []

    except Exception as e:
        return []

def fetch_youglish_data(word):
    """Scrapes 'Nearby words' and returns the YouGlish URL for pronunciation practice."""
    if not word: return None
    
    url = f"https://youglish.com/pronounce/{word}/english"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    data = {
        'url': url,
        'nearby_words': []
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            nearby_panel = soup.select_one('#nearByPanel')
            if nearby_panel:
                links = nearby_panel.select('ul.list-inline li a')
                words = [link.get_text().strip() for link in links if link.get_text().strip()]
                data['nearby_words'] = words[:15]
    except Exception:
        pass 
        
    return data

def get_full_word_data():
    """Aggregates all data for a random word."""
    word = fetch_from_random_word_generator_dot_com()
    if not word:
        return {"error": "Failed to generate word"}
    
    mw_data = fetch_merriam_webster_data(word)
    images = fetch_related_images(word)
    youglish = fetch_youglish_data(word)
    
    return {
        "word": word,
        "definitions": mw_data.get('definitions', []),
        "synonyms": mw_data.get('synonyms', []),
        "examples": mw_data.get('examples', []),
        "phrases": mw_data.get('phrases', []),
        "audio_url": mw_data.get('audio_url'),
        "images": images,
        "youglish": youglish
    }
