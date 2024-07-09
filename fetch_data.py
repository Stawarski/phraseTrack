import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

def fetch_page(url):
    """
    Fetches and returns the HTML content of a web page.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_urls(html, base_url):
    """
    Extracts URLs of episodes from the provided HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []

    links = soup.find_all('a', class_='category-page__member-link')
    for link in links:
        href = link.get('href')
        if href and href.startswith('/wiki/'):
            episode_url = f"{base_url}{href.split('/wiki/')[1]}"
            urls.append(episode_url)

    return urls

def extract_dialogue_data(html, episode_url):
    """
    Extracts dialogue data from the provided HTML content for a specific episode.
    Returns a list of strings where each string contains the episode name, character, and dialogue line.
    """
    episode_name_encoded = urlparse(episode_url).path.split('/')[-2]  # Extract episode name from URL path
    episode_name = unquote(episode_name_encoded.replace('_', ' '))  # Decode and replace underscores with spaces
    soup = BeautifulSoup(html, 'html.parser')
    dialogue_list = []

    rows = soup.find_all('tr')
    for row in rows:
        th = row.find('th')
        td = row.find('td')
        if th and td:
            th_text = th.get_text(strip=True)
            if 'Season' in th_text:
                break  # Stop processing if "Season" is found in <th>
            character = th_text
            dialogue_line = td.text.strip()
            dialogue_list.append(f"{episode_name}:{character}:{dialogue_line}")

    return dialogue_list