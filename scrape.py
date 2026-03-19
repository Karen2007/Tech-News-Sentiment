import pandas as pd
import requests
from bs4 import BeautifulSoup
from handle_data import save_to_csv
from datetime import datetime


urls = {
    'Hacker News' : 'https://brutalist.report/source/hn?hours=1', # Hacker News
    'The Verge' : 'https://brutalist.report/source/verge?hours=1', # The Verge
    'Engadget' : 'https://brutalist.report/source/engadget?hours=1', # Engadget
    'TechCrunch' : 'https://brutalist.report/source/techcrunch?hours=1', # TechCrunch
    'TechRadar' : 'https://brutalist.report/source/techradar?hours=1' # TechRadar
}

def fetch_headlines():
    """
    Fetch headlines from different sources on brutalist.report
    """

    columns = ['headline', 'source', 'link', 'datetime']

    headlines = pd.DataFrame(columns=columns)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'}

    for name, url in urls.items():
        try:
            page = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(page.text, 'html.parser') # Scrape the html contents from the site

            li_tags = soup.find_all('li') # Find all <li>-s in the html

            for tag in li_tags:
                try:
                    a_tag = tag.find('a') # Find the <a>-s in the <li>-s

                    # Add the new entry to the data frame
                    entry = [
                        a_tag.get_text(strip=True), # Headline
                        name, # Source
                        a_tag['href'], # Link to the article
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Date added
                    ]
                    headlines.loc[len(headlines)] = entry

                except AttributeError as e:
                    pass
        except Exception as e:
            print(f"Error {e} while fetching the headlines")

    return headlines


if __name__ == "__main__":
    data = fetch_headlines()
    save_to_csv(data)
    print(f"Saved {len(data)} headlines.")