import streamlit as st
import requests  # To fetch the source code of a website.
from bs4 import BeautifulSoup  # To scrap the data.
import pandas as pd
import numpy as np

string = "Web Scrapping"
st.set_page_config(page_title=string)
st.title("Amazon Product Reviews Web Scrapping")
st.header("Working")
video_file = open('Process.mkv', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.header("Enter Amazon Product URL")
count = 1
url = st.text_input("")
url = url.replace("dp", "product-review", 1)
cust_name = []
review_dates = []
ratings = []
review_title = []
cust_reviews = []
error = []
if url:
    url = url + "&pageNumber="
    with st.spinner('Fetching data...'):
        my_bar = st.progress(0)
        for i in range(1, 201):
            my_bar.progress(i/200)
            new_url = url + str(i)
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
                    ratings.append(stars[j].get_text())
                    review_title.append(titles[j].get_text())
                    stringcheck = 'Hello Stack!'
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
                error.append(i)
    st.success('Done!')
    df = pd.DataFrame()
    df['Customer Name'] = cust_name
    df['Date'] = review_dates
    df['Ratings'] = ratings
    df['Title'] = review_title
    df['Reviews'] = cust_reviews
    df.index = np.arange(1, len(df)+1)
    st.write(df)
