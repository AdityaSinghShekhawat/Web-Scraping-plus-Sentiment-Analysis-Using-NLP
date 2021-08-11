# Importing libraries.
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st
import requests  # To fetch the source code of a website.
from bs4 import BeautifulSoup  # To scrap the data.
import pandas as pd
import numpy as np
import nltk
import emoji
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()


# Webpage title.
def webpage():
    st.set_page_config(page_title="Amazon product scrap")
    st.title("Amazon Product Reviews Web Scrapping")


# Contains video.
def video_section():
    st.header("Working")
    video_file = open('Process.mkv', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)


# Return URL.
def url_section():
    st.header("Enter Amazon Product URL")
    url = st.text_input("")
    if ('/gp/' in url):
        url = url.replace("/gp/", "/product-review/", 1)
        url = url + "&pageNumber="
    elif ('/dp/' in url):
        url = url.replace("/dp/", "/product-review/", 1)
        url = url + "&pageNumber="
    return url


# Scrap URL.
def scrapping(url):
    cust_name = []
    review_dates = []
    ratings = []
    review_title = []
    cust_reviews = []
    error = []
    count = 1
    with st.spinner('Fetching data...'):
        my_bar = st.progress(0)
        for i in range(1, 101):
            my_bar.progress(i/100)
            new_url = url + str(i)
            try:
                page = requests.get(new_url)
                if str(page) == "<Response [200]>":
                    soup = BeautifulSoup(page.content, 'html.parser')
                    names = soup.select('span.a-profile-name')
                    dates = soup.select('span.review-date')
                    stars = soup.select("a.a-link-normal i span.a-icon-alt")
                    titles = soup.select("a.review-title-content span")
                    reviews = soup.select('span.review-text-content span')
                    if (len(names) != len(stars)):
                        names = names[2:]
                        dates = dates[2:]
                    while (len(names) != len(reviews)):
                        if(len(names) > len(reviews)):
                            reviews.append("None")
                        else:
                            reviews.pop()
                    for j in range(len(names)):
                        cust_name.append(names[j].get_text())
                        review_dates.append(dates[j].get_text().replace(
                            "Reviewed in India on ", ""))
                        ratings.append(stars[j].get_text().replace(
                            " out of 5 stars", "/5"))
                        review_title.append(titles[j].get_text())
                        if (isinstance(reviews[j], str)):
                            cust_reviews.append(reviews[j])
                        else:
                            cust_reviews.append(
                                reviews[j].get_text().strip("\n  "))
                    if names != []:
                        count += 1
                    else:
                        count += 1
                        my_bar.progress(1.0)
                        my_bar.empty()
                        break
                else:
                    st.error(
                        "Page either not compatible or does not exist. Please watch above video.")
                    my_bar.progress(1.0)
                    my_bar.empty()
                    error.append(i)
                    break
            except:
                st.error("Invalid URL. Please watch above video.")
                my_bar.progress(1.0)
                my_bar.empty()
                break
    placeholder = st.empty()
    placeholder.success('Done!')
    time.sleep(0.5)
    placeholder.empty()
    return cust_name, review_dates, ratings, review_title, cust_reviews, error


# Adding scrapped data in dataframe.
def dataframe(cust_name, review_dates, ratings, review_title, cust_reviews, error):
    df = pd.DataFrame()
    df['Customer Name'] = cust_name
    df['Date'] = review_dates
    df['Ratings'] = ratings
    df['Title'] = review_title
    df['Reviews'] = cust_reviews
    return df


# Adding 'sentiment_score' column according to 'Reviews' column.
def addSentiment(df):
    compound = list()
    sentiment = list()
    total_rows = df['Customer Name'].count()
    for i in range(total_rows):
        review = df.iloc[i]['Reviews']
        score = sia.polarity_scores(review)
        compound.append(score['compound'])

        if ((score['compound'] >= -1) and (score['compound'] < -0.6)):
            sentiment.append(str(
                round((compound[i]+1)*2+1, 2))+"/5 "+emoji.emojize(":angry:", use_aliases=True))
        elif ((score['compound'] >= -0.6) and (score['compound'] < -0.2)):
            sentiment.append(
                str(round((compound[i]+1)*2+1, 2))+"/5 "+emoji.emojize(":worried:", use_aliases=True))
        elif ((score['compound'] >= -0.2) and (score['compound'] < 0.2)):
            sentiment.append(
                str(round((compound[i]+1)*2+1, 2))+"/5 "+emoji.emojize(":neutral_face:", use_aliases=True))
        elif ((score['compound'] >= 0.2) and (score['compound'] < 0.6)):
            sentiment.append(str(
                round((compound[i]+1)*2+1, 2))+"/5 "+emoji.emojize(":blush:", use_aliases=True))
        elif ((score['compound'] >= 0.6) and (score['compound'] <= 1)):
            sentiment.append(str(
                round((compound[i]+1)*2+1, 2))+"/5 "+emoji.emojize(":smile:", use_aliases=True))
    df['Score'] = compound
    df['Sentiment'] = sentiment
    return df


# Evaluating overall sentiment.
def meanSentiment(score_df):
    score_mean = score_df['Score'].mean()
    if ((score_mean >= -1) and (score_mean < -0.6)):
        st.write("Overall Sentiment: " +
                 str(round((score_mean+1)*2+1, 2))+"/5 :angry:.")
    elif ((score_mean >= -0.6) and (score_mean < -0.2)):
        st.write("Overall Sentiment: " +
                 str(round((score_mean+1)*2+1, 2))+"/5 :worried:.")
    elif ((score_mean >= -0.2) and (score_mean < 0.2)):
        st.write("Overall Sentiment: " +
                 str(round((score_mean+1)*2+1, 2))+"/5 :neutral_face:.")
    elif ((score_mean >= 0.2) and (score_mean < 0.6)):
        st.write("Overall Sentiment: " +
                 str(round((score_mean+1)*2+1, 2))+"/5 :blush:.")
    elif ((score_mean >= 0.6) and (score_mean <= 1)):
        st.write("Overall Sentiment: " +
                 str(round((score_mean+1)*2+1, 2))+"/5 :smile:.")


if __name__ == "__main__":
    webpage()
    video_section()
    url = url_section()
    if url:
        cust_name, review_dates, ratings, review_title, cust_reviews, error = scrapping(
            url)
        df = dataframe(cust_name, review_dates, ratings,
                       review_title, cust_reviews, error)
        if df.empty:
            st.markdown(
                "Sorry no reviews present for this product. Try for different product.:expressionless:")
        else:
            score_df = addSentiment(df)
            score_df.index = np.arange(1, len(score_df)+1)
            st.dataframe(score_df[['Customer Name', 'Date',
                                   'Ratings', 'Title', 'Reviews', 'Sentiment']], 1400, 400)
            meanSentiment(score_df)
