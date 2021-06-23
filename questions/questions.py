from typing import no_type_check_decorator
import nltk
import sys
import string
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = {}
    
    for filename in os.listdir(directory):
        file = open(os.path.join(directory, filename))
        contents[filename] = file.read()
            
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document.lower())
    words_to_remove = []

    for word in tokens:
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            words_to_remove.append(word)

    for word in words_to_remove:
        tokens.remove(word)

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfvals = {}
    for document in documents:
        words_done = []
        for word in documents[document]:
            if word not in words_done:
                if word not in idfvals:
                    idfvals[word] = 1
                else:
                    idfvals[word] += 1
                words_done.append(word)

    for word in idfvals:
        idfvals[word] = math.log(len(documents)/idfvals[word])
        
    return idfvals

    


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = {}
    for file in files:
        tfidfs[file] = 0

    for file in files:
        for word in query:
            if word in files[file]:
                for term in files[file]:
                    if word == term:
                        tfidfs[file] += idfs[word]

    tfidfs_sorted = {k: v for k, v in sorted(tfidfs.items(), key=lambda x:x[1], reverse=True)}
    
    filenames = list(tfidfs_sorted.keys())[0:n]

    return filenames



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idfsr = {}
    for sentence in sentences:
        idfsr[sentence] = (0, 0)

    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                new1 = idfsr[sentence][0] + idfs[word]
                new2 = idfsr[sentence][1] + sentences[sentence].count(word)
                idfsr[sentence] = (new1, new2)

    for sentence in sentences:
        idfsr[sentence] = (idfsr[sentence][0], idfsr[sentence][1] / len(sentences[sentence]))

    # order sentences
    sorted_by_first = dict(sorted(idfsr.items(),key=lambda k: k[1][0], reverse=True))
    sorted_by_first_1 = {}
    for sentence in sorted_by_first:
        sorted_by_first_1[sentence] = sorted_by_first[sentence][0]
    
    largest = max(sorted_by_first_1.values())
    filenames = []

    while True:
        for sentence in sorted_by_first_1:
            if sorted_by_first_1[sentence] == largest:
                filenames.append(sentence)
                sorted_by_first_1[sentence] = 0
                if len(filenames) >= n:
                    temp_largest = largest


        if len(filenames) >= n:
            break
        else:
            largest = max(sorted_by_first_1.values())

    on_the_bubble = []
    for sentence in sorted_by_first_1:
        if sorted_by_first[sentence][0] == temp_largest:
            on_the_bubble.append(sentence)
    
    sorted_by_second = dict(sorted(idfsr.items(),key=lambda k: k[1][1]))
    diff = len(filenames) - n

    count = 0
    for sentence in sorted_by_second:
        if sentence in on_the_bubble:
            count += 1
            if count > diff:
                on_the_bubble.remove(sentence)

    for sentence in on_the_bubble:
        filenames.remove(sentence)

    return filenames


if __name__ == "__main__":
    main()
