#!/usr/bin/env python
# coding: utf-8

# # Assignment 1: Text Preprocessing
# 
# Nikolaou Nikolaos - DSC18014

# # Question A

# In[19]:


import nltk
import string
import requests
from readability.readability import Document
from bs4 import BeautifulSoup
import codecs
import os
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')
import nltk.data
# nltk.data.path.append("/mnt/c/users/nick/Google Drive/Study/DataScience/2. NLP/Assignments/Exercise 1/.nltk_data/")
# nltk.data.path.append("C:/Users/nnikolao/PycharmProjects/.nltk_data/")


# What is the word count and vocabulary of this Web page?

# In[5]:


url = 'https://en.wikipedia.org/wiki/Artificial_neural_network'


# In[6]:


r = requests.get(url)
html = r.text


# In[7]:


TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']


# In[47]:


def preprocess(f):
    paper = Document(f)
    soup = BeautifulSoup(paper.summary())
    # kill all script and style elements
    for script in soup(["script", "style","math"]):
        script.decompose()    # rip it out
    output = [paper.title()]
    for tag in soup.find_all(TAGS):
        # Get the HTML node text
        paragraph = tag.get_text()

        # Sentence Tokenize
        sentences = nltk.sent_tokenize(paragraph)
        for idx, sentence in enumerate(sentences):
            # Word Tokenize and Part of Speech Tagging
            sentences[idx] = nltk.pos_tag(nltk.word_tokenize(sentence))

        # Yield a list of sentences (the paragraph); each sentence of
        # which is a list of tuples in the form (token, tag).
        yield sentences


# In[48]:


try:
    os.mkdir("./nlp_data")
except OSError:  
    print ("Directory already exists")
outpath = os.path.join("./nlp_data/", "outfile" + ".txt")
with codecs.open(outpath, 'w+', encoding='utf-8') as f:
    # Write paragraphs double newline separated and sentences
    # separated by a single newline. Also write token/tag pairs.
    for paragraph in preprocess(html):
        for sentence in paragraph:
            f.write(" ".join("%s/%s" % (word, tag) for word, tag in sentence))
            f.write("\n")
            f.write("\n")


# Now in the Outfile, we have the preprocessed document

# In[49]:


# Construct stopwords
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(list(string.punctuation))          # Remove punctuation
stopwords.extend(["''", '``', "'s", "n't", "'ll"])  # Custom stopwords


# In[50]:


# Construct the corpus
corpus = nltk.corpus.TaggedCorpusReader("./nlp_data",r'.*txt')


# In[51]:


# Get the interesting words from corpus
words = [word.lower() for word in corpus.words() if word not in stopwords]


# In[52]:


# Count the words,sentences and tags
tokens    = nltk.FreqDist(corpus.words())
unigrams  = nltk.FreqDist(words)
bigrams   = nltk.FreqDist(nltk.bigrams(words))
tags      = nltk.FreqDist(tag for word, tag in corpus.tagged_words())


# In[53]:


# Eliminate stopwords
for word in stopwords:
    unigrams.pop(word, None)
    bigrams.pop(word, None)


# In[54]:


# Enumerate the vocabulary and word count
vocab     = len(tokens)            # The number of unique tokens
sents     = len(corpus.sents())
count     = sum(tokens.values())   # The word count for the entire corpus


# Answering the questions:

# In[55]:


print("1. What is the word count and vocabulary of this Web page?")
print (" This corpus contains %i words with a vocabulary of %i tokens."  % (count, vocab))

print("\n2. How many sentences are contained in the page?")
print (" This corpus contains %i sentences."  % (sents))

print("\n3. What is the lexical diversity of the page?")
print (" The lexical diversity is %0.3f" % (float(count) / float(vocab)))


# In[56]:


print("4. What are the 5 most common lexical categories (parts of speech)?")
print (" The 5 most common tags are:")
for idx, tag in enumerate(tags.most_common(5)):
    print ("    %i. %s (%i samples)" % ((idx+1,) + tag))


# In[57]:


print("5. What are the 10 most common unigrams, the 10 most common bigrams?")
print (" The 10 most common unigrams are:")
for idx, tag in enumerate(unigrams.most_common(10)):
    print ("    %i. %s (%i samples)" % ((idx+1,) + tag))
print ("\n The 10 most common bigrams are:")
for idx, tag in enumerate(bigrams.most_common(10)):
    print ("    %i. %s (%i samples)" % ((idx+1,) + tag))


# In[58]:


print("6. How many nouns are in the page?")
print (" There are %i nouns in the corpus" % sum(val for key,val in tags.items() if key.startswith('N')))


# # Question B

# In[32]:


import csv


# In[33]:


csv_outpath = os.path.join("./nlp_data/", "csv_outfile" + ".csv")
with codecs.open(csv_outpath, 'w', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')
    csv_writer.writerow(['Νικόλαος', 'Νικολάου','“Μεταπτυχιακό στην Επιστήμη Δεδομένων”'])

