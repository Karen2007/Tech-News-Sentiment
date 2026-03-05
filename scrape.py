import requests
from bs4 import BeautifulSoup
from handle_data import save_to_csv

urls = {
    'Hacker News' : 'https://brutalist.report/source/hn?hours=3', # Hacker News
    'The Verge' : 'https://brutalist.report/source/verge?hours=3', # The Verge
    'Engadget' : 'https://brutalist.report/source/engadget?hours=3', # Engadget
    'TechCrunch' : 'https://brutalist.report/source/techcrunch?hours=3', # TechCrunch
    'TechRadar' : 'https://brutalist.report/source/techradar?hours=3' # TechRadar
}

def fetch_headlines():
    """
    Fetches headlines from different sources on brutalist.report
    """
    headlines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'}

    for name, url in urls.items():
        try:
            page = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(page.text, 'html.parser')

            li_tags = soup.find_all('li')

            for tag in li_tags:
                try:
                    a_tag = tag.find('a')
                    entry = {
                        'headline': a_tag.get_text(strip=True),
                        'source': name,
                        'link': a_tag['href']
                    }
                    headlines.append(entry)
                except AttributeError as e:
                    pass
        except Exception as e:
            print(f"Error {e} while fetching the headlines")

    return headlines

if __name__ == "__main__":
    data = fetch_headlines()
    if data:
        save_to_csv(data)
        print(f"Saved {len(data)} headlines.")