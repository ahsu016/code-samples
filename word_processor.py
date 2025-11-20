import json
import sys
import nltk
import random
from dotenv import load_dotenv
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

load_dotenv()

# NLTK DOWNLOADS, MODULE LEVEL BECAUSE THIS THING HATES ME
try:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('brown', quiet=True)
except Exception as e:
    print(f"Failed to download NLTK data: {str(e)}")

def is_valid_word(word):
    return bool(wn.synsets(word))

def get_synonyms(word, max_count=5):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.add(lemma.name().replace('_', ' '))
                if len(synonyms) >= max_count * 2:  # GET MORE
                    break
    
    # RETURN IF NOT ENOUGH
    synonyms_list = list(synonyms)
    random.shuffle(synonyms_list)  # RAND
    return synonyms_list[:max_count]

def get_antonyms(word, max_count=5):
    antonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            for ant in lemma.antonyms():
                antonyms.add(ant.name().replace('_', ' '))
                if len(antonyms) >= max_count * 2:  # GET MORE
                    break
    
    # RETURN IF::NOT ENOUGH
    antonyms_list = list(antonyms)
    random.shuffle(antonyms_list)  # RAND
    return antonyms_list[:max_count]

def get_collocations(word, corpus_text=None, max_count=5):
    try:
        if corpus_text is None:
            # BIG CORPUS
            tokens = list(brown.words())[:1000000]
        else:
            tokens = nltk.word_tokenize(corpus_text.lower())
        
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(tokens)
        
        # FREQ FILTER
        finder.apply_freq_filter(2)
        
        word_filter = lambda w1, w2: word.lower() in (w1.lower(), w2.lower())
        finder.apply_ngram_filter(word_filter)
        
        scored = finder.score_ngrams(bigram_measures.likelihood_ratio)
        
        # EXTRACT
        collocations = []
        for (pair, score) in scored:
            if len(collocations) >= max_count:
                break
                
            collocation = " ".join(pair)
            if word.lower() in collocation.lower() and not (pair[0].lower() == word.lower() and pair[1].lower() == word.lower()):
                collocations.append(collocation)
        
        if len(collocations) < max_count:
            word_stem = word.lower()
            if word_stem.endswith('s'):
                word_stem = word_stem[:-1]
            elif word_stem.endswith('ed'):
                word_stem = word_stem[:-2]
            elif word_stem.endswith('ing'):
                word_stem = word_stem[:-3]
                
            for (pair, score) in scored:
                if len(collocations) >= max_count:
                    break
                    
                collocation = " ".join(pair)

                if word_stem in pair[0].lower() or word_stem in pair[1].lower():
                    if collocation not in collocations:
                        collocations.append(collocation)
        
        return collocations[:max_count]
    except Exception as e:
        print(f"Error in get_collocations: {str(e)}")
        return []

def suggest_spelling(word):
    try:
        # SAMPLE SMALL FOR SPEED
        sample_synsets = list(wn.all_synsets())[:1000]
        word_list = list({w for syn in sample_synsets for w in syn.lemma_names()})
        matches = get_close_matches(word, word_list, n=1, cutoff=0.8)
        return matches[0] if matches else None
    except Exception as e:
        print(f"Error in suggest_spelling: {str(e)}")
        return None

def get_word_data(word, corpus_text=None):
    data = {
        "word": word,
        "valid": False,
        "synonyms": [],
        "antonyms": [],
        "collocations": [],
        "suggestion": None,
        "definition": None
    }

    try:
        if is_valid_word(word):
            synsets = wn.synsets(word)
            definition = synsets[0].definition() if synsets else "No definition found."

            synonyms = get_synonyms(word, max_count=5)
            antonyms = get_antonyms(word, max_count=5)
            collocations = get_collocations(word, corpus_text, max_count=5)
            
            if len(collocations) < 2 and len(synonyms) > 5:
                collocations.extend([f"{word} {s}" for s in synonyms[5:10] if len(collocations) < 5])
            
            data.update({
                "valid": True,
                "synonyms": synonyms[:5],
                "antonyms": antonyms[:5],
                "collocations": collocations[:5],
                "definition": definition 
            })
        else:
            data["suggestion"] = suggest_spelling(word)
            data["definition"] = "Word not found in WordNet."
    except Exception as e:
        print(f"Error in get_word_data: {str(e)}")
        data["error"] = str(e)
        data["definition"] = "An error occurred while fetching the definition."

    return data


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"valid": False, "error": "No word provided"}))
        sys.exit(1)

    word = sys.argv[1]
    word_data = get_word_data(word)
    print(json.dumps(word_data))