import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pd = {}
    n = len(corpus[page])
    for page_name in corpus.keys():
        if page_name in corpus[page]:
            pd[page_name] = damping_factor / n
        else:
            pd[page_name] = 0

    for page_name in corpus.keys():
        pd[page_name] += (1 - damping_factor) / len(corpus.keys())

    return pd

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    for key in corpus.keys():
        pr[key] = 0
    
    pageInd = random.randint(0, len(corpus)-1)
    page = random.choice(list(corpus.keys()))
    pr[page] = 1
    
    for i in range(n-1):
        pd = transition_model(corpus, page, damping_factor)

        #scales to bounds
        for j in range(1, len(pd.keys())):
            pd[list(pd.keys())[j]] += pd[list(pd.keys())[j-1]]

        #gen rand test
        test = random.random()

        for key in pd.keys():
            if pd[key] > test:
                pr[key] = pr[key] + 1
                page = key
                break

    for key in pr.keys():
        pr[key] /= n

    return pr

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    last_change = {}
    N = len(corpus)
    for key in corpus.keys():
        pr[key] = 1/N
        last_change[key] = 0.1

    changes_neg = False

    while (not changes_neg):
        for key in pr.keys():
            temp = (1-damping_factor)/N
            for page in corpus.keys():
                if key in corpus[page]:
                    temp += damping_factor * pr[page] / len(corpus[page])

                if len(corpus[page]) == 0:
                    temp += damping_factor * pr[page] / N

            last_change[key] = abs(temp - pr[key])
            pr[key] = temp

        changes_neg = True
        for key in last_change.keys():
            if last_change[key] > 0.001:
                changes_neg = False
                break

    return pr
    

if __name__ == "__main__":
    main()

