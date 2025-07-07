# News Sentiment Analysis

#### Video Demo: https://youtu.be/wKdwOxGlV1g

## Description

This project is a fully automated News Sentiment Analysis pipeline that collects daily news headlines and articles from ABC News (Australia) headpage, performs sentiment analysis on the content using the VADER sentiment analysis model, and visualizes the sentiment scores over time. The goal of this project is to provide an evolving view of how news sentiment changes on a daily basis, and how that sentiment may reflect or influence public discourse.

This project is intended to be run daily, collecting the latest articles, scoring them for sentiment, and updating the visual history of sentiment in news content. It is designed to avoid duplicating work and hopefully builds a persistent historical dataset of sentiment trends.

---

## How It Works

The entire pipeline is coordinated through the `main()` function in `project.py`, which executes three core tasks in order: scraping, analyzing, and visualizing.

### 1. `web_scrape()`
This function scrapes news articles from the ABC News website. It identifies article links, extracts titles, publication dates, and full text content. It avoids duplicate entries by checking against an existing `articles.csv` file before writing new articles.

### 2. `Sentiment_analysis()`
After scraping, this function reads all unprocessed articles from `articles.csv` and uses VADER to generate sentiment scores (`neg`, `neu`, `pos`, `compound`). It saves these scores to a `Sentiment_Data.csv` file. Articles are skipped if they’ve already been analyzed, which is determined by title matching against the existing sentiment dataset.

### 3. `graph()`
This visualization function reads `Sentiment_Data.csv`, groups sentiment scores by day, and plots the average compound sentiment score for each date. The x-axis of the graph shows only dates for which articles exist, and the y-axis shows the average sentiment score for those articles. The result is a clear and meaningful trendline showing sentiment over time.

---

## Project Files

- **`project.py`**: The main Python script. Contains all logic for scraping, analyzing, and visualizing.
- **`test_project.py`**: Contains all tests for scraping, analyzing, and visualizing.
- **`Data`**: Folder containing data 
    - **`articles.csv`**: Stores scraped article titles, URLs, dates, and content.
    - **`Sentiment_Data.csv`**: Stores sentiment analysis results for each article (one row per article).
- **`README.md`**: This documentation file.
- **`requirements.txt`**: Any pip-installable libraries that your project requires listed here

---

## Design Decisions

Several design decisions were made with automation, scalability, and simplicity in mind:

- **File-based persistence**: Using CSV files allows the program to persist across runs without requiring a database. It makes debugging easier and keeps the project lightweight.
- **Title-based duplication check**: Each article’s title is assumed to be unique. This is used to prevent re-scraping and re-processing the same article.
- **Compound sentiment score only**: While VADER provides multiple scores, the compound score is used for plotting because it offers a single, comprehensive metric of sentiment.
- **Daily scheduling support**: The script can be run once per day (via a scheduler like Task Scheduler), and it will automatically add only new articles and plot updated 
results.

---

## Future Improvements

- Add support for multiple news sources.
- Store data in a database for more robust querying.
- Enable sentiment filtering or keyword-based analysis (e.g., per topic or per entity).
- Export visualizations as image files for reporting or sharing.

---

This project showcases the power of automation and natural language processing in understanding media trends over time. It's a practical demonstration of combining web scraping, sentiment analysis, and data visualization into a meaningful daily routine.
