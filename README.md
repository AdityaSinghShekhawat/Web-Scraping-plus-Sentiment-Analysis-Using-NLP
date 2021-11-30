# Motivation:-
As customers, we need to rely largely on product reviews to make up our minds for better purchasing decisions. However, ratings on products are not standardized. That is, they do not take the emotion of customers into account. Hence there can be a huge difference between what the customer wrote and its rating of the product.

So, I have made a website which scrape reviews of products from Amazon and run sentiment analysis on them, thus ranking them based on customer happiness and comparing against the actual ratings.

# Technologies:-
## 1) Web Hosting:-
* Heroku

	[Main website](https://amazonproductreviewanalysis.herokuapp.com/) 

* Streamlit Share

	[Backup website](https://share.streamlit.io/adityasinghshekhawat/web-scraping-plus-sentiment-analysis-using-nlp/app.py)

## 2) Language:-
* Python == 3.9.6

## 3) Libraries:-
* requests == 2.26.0
* pandas == 1.3.1
* numpy == 1.21.1
* nltk == 3.6.2
* streamlit == 0.86.0

# Working:-
1. Take whole HTML page with the help of "request" library.
2. Take necessary data from URL like Customer name, Date, Ratings, Title, Reviews.
3. Evaluate sentiment of each review using "vader_lexicon" present in "nltk" library.
4. Take the mean of all sentiments and evaluate "Overall Sentiment" of the product.

# Limitations:-
1. It only selects maximum of first 1000 reviews as increasing number of reviews also increases computation time.
2. Some types of Amazon URL are not supported.
3. Sentiment recognition is done using Vader lexicon, which has accuracy 82.8%.

# Future Work:-
1. Add support to all type of Amazon URL.
2. Give a print option so that user can print whole data frame.
3. Add spam report.
