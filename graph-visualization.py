import nltk
from nltk.corpus import wordnet as wn
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import networkx as nx
import matplotlib.pyplot as plt
import re

# MANUAL TOKENIZER
def simple_tokenize(text):
    # Use regex to capture words and ignore punctuation
    return re.findall(r'\b\w+\b', text.lower())

# GET SYN ANTONYMS AND COLLOCATIONS
def get_synonyms(word):
    syns = set()
    for syn in wn.synsets(word):
        for lem in syn.lemmas():
            if lem.name().lower() != word.lower():
                syns.add(lem.name().replace('_',' '))
    return list(syns)

def get_antonyms(word):
    ants = set()
    for syn in wn.synsets(word):
        for lem in syn.lemmas():
            for ant in lem.antonyms():
                ants.add(ant.name().replace('_',' '))
    return list(ants)

def get_collocations(word, text, max_collocations=10):
    tokens = simple_tokenize(text)  # Using the manual tokenizer
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_ngram_filter(lambda w1, w2: word not in (w1, w2))
    scored = finder.score_ngrams(BigramAssocMeasures.likelihood_ratio)
    collocs = [" ".join(bigram) for bigram, score in scored]
    return collocs[:max_collocations]

# EX CORPUS // JAMES JOYCE FINNEGANS WAKE
corpus = """
A lone a last a loved a long the riverrun,
past Eve and Adam’s, from swerve of shore to bend of bay,
brings us by a commodius vicus of recirculation back to Howth Castle and Environs.
"""

# ASK USER FOR A WORD
word = input("Enter a word: ").strip().lower()

# BUILD GRAPH
G = nx.Graph()

# MAIN WORD NODE
G.add_node(word, type="main")
for syn in get_synonyms(word):
    G.add_node(syn, type="synonym")
    G.add_edge(word, syn)
for ant in get_antonyms(word):
    G.add_node(ant, type="antonym")
    G.add_edge(word, ant)
for col in get_collocations(word, corpus):
    G.add_node(col, type="collocation")
    G.add_edge(word, col)

# COLOR
def get_color(t):
    return {"main":"black","synonym":"green","antonym":"red","collocation":"blue"}.get(t,"gray")

pos    = nx.spring_layout(G, seed=42)
colors = [get_color(G.nodes[n]["type"]) for n in G.nodes()]
sizes  = [1200 if G.nodes[n]["type"]=="main" else 800 for n in G.nodes()]

# DRAW
plt.figure(figsize=(8,6))
nx.draw(
  G, pos,
  with_labels=True,
  node_color=colors,
  node_size=sizes,
  font_color='black',
  font_weight='bold',
  edge_color='gray',
  width=1.5
)
plt.title(f"Word Graph for '{word}' (offline, NLTK)")
plt.axis('off')
plt.show()
