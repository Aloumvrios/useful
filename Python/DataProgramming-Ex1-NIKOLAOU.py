#!/usr/bin/env python

#########################################################################
# Data Proramming - MSc in Data Science 2018 - Assignment 1/2
# Author: ENTER YOUR NAME HERE
#########################################################################

import sys
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re

CRAN_COLL = './cran.all.1400'
INDEX_FILE = 'cran.ind'

SYMBOLS = '!@#$%^&*()[]{};\':",.<>/?`~-_=+'


def parse_documents(cran_file=CRAN_COLL):
    """Parse the document body and title fields of the Cranfield collection.
    Arguments:
        cran_file: (str) the path to the Cranfield collection file
    Return:
        (body_kwds, title_kwds): where body_kwds and title_kwds are
        dictionaries of the form {docId: [words]}.
    """
    body_kwds = {}
    title_kwds = {}
    cran_file = open(CRAN_COLL)
    for line in cran_file:
        if line.startswith('.I '):
            section = "I"
            docId = line.split()[-1]
            # print("found index!")
        elif line.startswith(".T"):
            words = []
            section = "T"
        elif line.startswith(".A"):
            words = []
            section = "A"
        elif line.startswith(".B"):
            words = []
            section = "B"
        elif line.startswith(".W"):
            words = []
            section = "W"
        elif section == "T":
            words = [word for word in line.split()]
            title_kwds[docId] = words
            # print(title_kwds)
            # if docId =="1":
            #     print(title_kwds)
        elif section == "W":
            words = [word for word in line.split()]
            body_kwds[docId] = words

    # x=title_kwds['1']
    # print(title_kwds)
    print(body_kwds["1"])
    return body_kwds, title_kwds


def pre_process(words):
    """Preprocess the list of words provided.
    Arguments:
        words: (list of str) A list of words or terms
    Return:
        a shorter list of pre-processed words
    """
    # Get list of stop-words and instantiate a stemmer:
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    # Make all lower-case:
    low_words = [word.lower() for word in words]

    # Remove symbols:
    no_symbols = [re.sub(r'[^\w]', ' ', word) for word in low_words]

    # Remove words <= 3 characters:
    more_than_three = [re.sub(r'\b[a-z]{1,3}\b', '', word) for word in no_symbols]

    # Remove space
    no_space = [word.replace(" ", "") for word in more_than_three]

    # Remove stopwords:
    no_stopwords = [word for word in no_space if word not in stopwords.words('english')]

    # Stem terms:
    stemmed = [stemmer.stem(word) for word in no_stopwords]

    # remove empty entries
    final = list(filter(None, stemmed))

    return final


def create_inv_index(bodies, titles):
    """Create a single inverted index for the dictionaries provided. Treat
    all keywords as if they come from the same field. In the inverted index
    retail document and term frequencies per the form below.
    Arguments:
        bodies: A dictionary of the form {doc_id: [terms]} for the terms found
        in the body (.W) of a document
        titles: A dictionary of the form {doc_id: [terms]} for the terms found
        in the title (.T) of a document
    Return:
        index: a dictionary {docId: [df, postings]}, where postings is a
        dictionary {docId: tf}.
        E.g. {'word': [3, {4: 2, 7: 1, 9: 3}]}
               ^       ^   ^        ^
               term    df  docid    tf
    """
    # Create a joint dictionary with pre-processed terms


def load_inv_index(filename=INDEX_FILE):
    """Load an inverted index from the disk. The index is assumed to be stored
    in a text file with one line per keyword. Each line is expected to be
    `eval`ed into a dictionary of the form created by create_inv_index().

    Arguments:
        filename: the path of the inverted index file
    Return:
        a dictionary containing all keywords and their posting dictionaries
    """


def write_inv_index(inv_index, outfile=INDEX_FILE):
    """Write the given inverted index in a file.
    Arguments:
        inv_index: an inverted index of the form {'term': [df, {doc_id: tf}]}
        outfile: (str) the path to the file to be created
    """


def eval_conj(inv_index, terms):
    """Evaluate the conjunction given in list of terms. In other words, the
    list of terms represent the query `term1 AND term2 AND ...`
    The documents satisfying this query will have to contain ALL terms.
    Arguments:
        inv_index: an inverted index
        terms: a list of terms of the form [str]
    Return:
        a set of (docId, score) tuples -- You can ignore `score` by
        substituting it with None
    """
    # Get the posting "lists" for each of the ANDed terms:

    # Basic AND - find the documents all terms appear in, setting scores to
    # None (set scores to tf.idf for ranked retrieval):


def eval_disj(conj_results):
    """Evaluate the conjunction results provided, essentially ORing the
    document IDs they contain. In other words the resulting list will have to
    contain all unique document IDs found in the partial result lists.
    Arguments:
        conj_results: results as they return from `eval_conj()`, i.e. of the
        form {(doc_id, score)}, where score can be None for non-ranked
        retrieval. 
    Return:
        a set of (docId, score) tuples - You can ignore `score` by substituting
        it with None
    """
    # Basic boolean - no scores, max(tf.idf) for ranked retrieval:


def main():
    """Load or create an inverted index. Parse user queries from stdin
    where words on each line are ANDed, while whole lines between them are
    ORed. Match the user query to the Cranfield collection and output matching
    documents as "ID: title", each on its own line, on stdout.
    """

    # If an index file exists load it; otherwise create a new inverted index
    # and write it into a file (you can use the variable INDEX_FILE):

    try:
        inv_index = load_inv_index(INDEX_FILE)
    except:
        sys.stderr.write("File does not exist. Let's create it!")

        # (body_kwds, title_kwds): where body_kwds and title_kwds are
        #     dictionaries of the form {docId: [words]}.
        body_kwds, title_kwds = parse_documents()

        # new dictionaries with pre processed words!
        bodies, titles = {}

        for key, words in body_kwds:
            bodies[key] = pre_process(words)

        for key, words in title_kwds:
            titles[key] = pre_process(words)

        create_inv_index(bodies, titles)
        write_inv_index()

    # Get and evaluate user queries from stdin. Terms on each line should be
    # ANDed, while results between lines should be ORed.
    # The output should be a space-separated list of document IDs. In the case
    # of unranked boolean retrieval they should be sorted by document ID, in
    # the case of ranked solutions they should be reverse-sorted by score
    # (documents with higher scores should appear before documents with lower
    # scores):


if __name__ == '__main__':
    main()
