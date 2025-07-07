import shutil
import os
import csv
from project import (
    loading_existing_titles,
    loading_exisiting_sentiment_titles,
    write_csv,
    write_data,
    Sentiment_analysis,
    graph,
    web_scrape,
)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Override folderPath to use test folder
import project
project.folderPath = "C:/Users/Khuba/project/News-Sentiment-Analysis/test_data/"
folderPath = project.folderPath

os.makedirs(folderPath, exist_ok=True)

# Clean up previous test files
for file in ["test_articles.csv", "test_Sentiment_Data.csv"]:
    path = os.path.join(folderPath, file)
    if os.path.exists(path):
        os.remove(path)

# --- Test 1: write_csv and loading_existing_titles 
def test_write_csv_and_loading_existing_titles():
    write_csv("Test Article", "http://example.com", "2025-06-24", "This is content")
    titles = loading_existing_titles()
    assert "Test Article" in titles
    print("Test 1 passed: write_csv + loading_existing_titles")


# --- Test 2: write_data and loading_exisiting_sentiment_titles
def test_write_data_and_loading_exisiting_sentiment_titles():
    write_data("Sentiment Title", "2025-06-24", 0.1, 0.7, 0.2, 0.4)
    titles = loading_exisiting_sentiment_titles()
    assert "Sentiment Title" in titles
    print("Test 2 passed: write_data + loading_exisiting_sentiment_titles")


# --- Test 3: Sentiment_analysis (depends on articles.csv)
def test_sentiment_analysis():
    write_csv("Analyze Me", "http://test.com", "2025-06-24", "Amazing product. Loved it.")
    Sentiment_analysis()
    titles = loading_exisiting_sentiment_titles()
    assert "Analyze Me" in titles
    print("Test 3 passed: Sentiment_analysis writes new data")


# --- Test 4: graph() (runs without crash)
def test_graph_runs():
    try:
        graph()
        print("Test 4 passed: graph runs without error")
    except Exception as e:
        assert False, f"Graph raised error: {e}"


# --- Test 5: web_scrape() (basic check that it runs)
def test_web_scrape_runs():
    try:
        web_scrape()
        print("Test 5 passed: web_scrape runs without crashing")
    except Exception as e:
        assert False, f"web_scrape raised error: {e}"


# --- Run all tests 
if __name__ == "__main__":
    test_write_csv_and_loading_existing_titles()
    test_write_data_and_loading_exisiting_sentiment_titles()
    test_sentiment_analysis()
    test_graph_runs()
    test_web_scrape_runs()

    for filename in os.listdir(folderPath):
        file_path = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    print("Cleanup complete: all test files deleted.")   