import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

frontier = ["https://www.bbc.com/news"]
visited = {}


def parse_links(soup, base_url):
    links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(base_url, href)
        if full_url.startswith("http"):
            links.append(full_url)
    return links


while len(frontier) > 0:
    url_to_visit = frontier.pop()
    if url_to_visit in visited:
        continue

    try:
        response = requests.get(url_to_visit)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url_to_visit}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    candidate_links = parse_links(soup, url_to_visit)
    for current in candidate_links:
        if current not in visited:
            frontier.append(current)

    unix_ts = int(datetime.now().timestamp())
    file_to_save = f"bbc_{unix_ts}.html"
    with open(file_to_save, "w") as html_file:
        html_file.write(response.text)

    visited[url_to_visit] = datetime.now().isoformat()
