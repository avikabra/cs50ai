# Traffic
This project calls for the creation of a neural network AI that can identify different type of traffic signs. Signs in the database were from the German Traffic Sign Recognition Benchmark, which contains 43 different classes of signs split into 39000+ training images and 12000+ test images. </br>
The code itself resides entirely in the `traffic.py` file. In it, the load_data() and get_model() functions were implemented by me. The network structure that I chose had a convolutional layer of 512 filters (3x3 kernel), a max-pooling layer (4x4), and 3 hidden layers, each with 512 nodes and a dropout probability of 0.5. </br>
The bulk of the code for this project was taken from the CS50 Intro to AI course provided by HarvardX. This is an implementation of Project 5 - traffic. </br>
Link: https://cs50.harvard.edu/ai/2020/projects/5/traffic/
