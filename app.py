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
count = 0
url = st.text_input("")
url = url.replace("dp", "product-review", 1)
cust_name = []
ratings = []
cust_reviews = []
error = []
if url:
    url = url + "&pageNumber="
    my_bar = st.progress(0)
    with st.spinner('Fetching data...'):
        for i in range(1, 201):
            my_bar.progress(i/200)
            new_url = url + str(i)
            page = requests.get(new_url)
            if str(page) == "<Response [200]>":
                soup = BeautifulSoup(page.content, 'html.parser')
                names = soup.select('span.a-profile-name')[2:]
                stars = soup.select("a.a-link-normal i span.a-icon-alt")
                reviews = soup.select('span.review-text-content span')
                for j in range(len(names)):
                    if (len(names) == len(stars)) and (len(stars) == len(reviews)):
                        cust_name.append(names[j].get_text())
                        ratings.append(stars[j].get_text())
                        cust_reviews.append(
                            reviews[j].get_text().strip("\n  "))
                if names != []:
                    count += 1
                else:
                    count += 1
                    my_bar.progress(1.0)
                    break
            else:
                error.append(i)
    st.success('Done!')
    df = pd.DataFrame()
    df['Customer Name'] = cust_name
    df['Ratings'] = ratings
    df['Reviews'] = cust_reviews
    df.index = np.arange(1, len(df)+1)
    st.write(df)
