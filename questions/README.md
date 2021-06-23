# Questions AI
An AI that answers questions by scanning .txt entries as its knowledge base and using query words to isolate the most relevant sentence in the most relevant file. </br>
One python file (`questions.py`) was used throughout this project. In the main function, files were loaded from the corpus into memory (load_data). They were then tokenized into a list of words, where each word had an inverse document frequency. The user query was matched first to the most relevant file and later to the most relevant sentence using tf-idf and outputed to the user. </br>
The bulk of the code for this project was taken from the CS50 Intro to AI course provided by HarvardX. This is an implementation of Project 6 - questions.
Link: https://cs50.harvard.edu/ai/2020/projects/6/questions/
