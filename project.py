from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import csv
import re
import os
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

folderPath = "C:/Users/Khuba/project/News-Sentiment-Analysis/data/"

def main():
    web_scrape()
    Sentiment_analysis()
    time.sleep(1)
    graph()


def graph(filepath=None):
    if filepath is None:
        filepath = os.path.join(folderPath, "Sentiment_Data.csv")
    
    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    
    


   
    daily_sentiment = df.groupby(df['Date'].dt.date)['compound'].mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(daily_sentiment.index, daily_sentiment.values, marker='o')

    # Format x-axis to show only YYYY-MM-DD
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate()  # auto-rotate for better readability

    plt.title("Average Daily News Sentiment (Compound Score) Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Compound Score")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def loading_exisiting_sentiment_titles(filename="Sentiment_Data.csv"):
    existing_data = set()
    filepath = os.path.join(folderPath, filename)
    if os.path.isfile(filepath):
       with open(filepath, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_data.add(row["Title"])
    
    return existing_data

def loading_existing_titles(filename="articles.csv"):
    existing_titles = set()
    filepath = os.path.join(folderPath, filename)
    if os.path.isfile(filepath):
       with open(filepath, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_titles.add(row["Title"])
    
    return existing_titles
    

def write_csv(title, url, date, content):
 

 file_exists = os.path.isfile(folderPath + "articles.csv")
 
 with open(folderPath + "articles.csv", "a", encoding="utf-8", newline="") as csvfile:
    fieldnames =["Title", "URL", "Date", "Content"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    

    if not file_exists:
        writer.writeheader()

    writer.writerow({
        "Title": title,
        "URL": url,
        "Date": date,
        "Content": content
    })

   

def web_scrape():
    base_url = "https://www.abc.net.au/"
    existing_titles = loading_existing_titles()
    request = requests.get("https://www.abc.net.au/news")
    soup = BeautifulSoup(request.text, "html.parser")
    target_class = "Link_link__kR0xA TopStoriesCard_link__D0AfC Link_link__5eL5m ScreenReaderOnly_srLinkHint__OysWz Link_showVisited__C1Fea Link_showFocus__ALyv2 Link_underlineNone__To6aJ"

    articles = soup.find_all("a", class_=target_class)

    for article in articles:
        title   = article.get_text(strip=True)
        href    = article.get("href")
        match   = re.search(r"\d{4}\-\d{2}\-\d{2}", href)
        
        if match:
            date = match.group()
        
            if href and date and title not in existing_titles:
                content_url = base_url + href
                request_new = requests.get(content_url)
                soup_new = BeautifulSoup(request_new.text, "html.parser")
                target_class_new = "paragraph_paragraph__iYReA"
                content = soup_new.find_all("p", class_=target_class_new)
                content_paragraphs = [a.get_text(strip=True) for a in content]
                full_content = " ".join(content_paragraphs)
                write_csv(title, content_url, date, full_content)
                print(f"Added article: {title}")

        

    
def Sentiment_analysis():
    existing_sentiment_titles = loading_exisiting_sentiment_titles()
    analyser = SentimentIntensityAnalyzer()
    with open(folderPath + "articles.csv", "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = row["Content"]
            title = row["Title"]
            date = row["Date"]
            
            if title in existing_sentiment_titles:
                continue

            vs = analyser.polarity_scores(content)
            neg = vs["neg"]
            neu = vs["neu"]
            pos = vs["pos"]
            compound = vs["compound"]
            write_data(title, date, neg, neu, pos, compound)
        print("✅ Sentiment data written.")


        
def write_data(title ,date, neg, neu, pos, compound):
    
    file_exists = os.path.isfile(folderPath + "Sentiment_Data.csv")
    with open(folderPath + "Sentiment_Data.csv", "a", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["Title", "Date", "neg", "neu", "pos", "compound"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Title": title,
            "Date": date,
            "neg": neg,
            "neu": neu,
            "pos": pos,
            "compound": compound
            })
                
  

if __name__ == "__main__":
    main()