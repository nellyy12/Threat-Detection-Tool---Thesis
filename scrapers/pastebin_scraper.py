import requests
from bs4 import BeautifulSoup

def scrape_pastebin(domain):
    results = []
    query = f"site:pastebin.com {domain}"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')
        if link and 'pastebin.com' in link['href']:
            paste_url = link['href']
            paste_content = fetch_pastebin_content(paste_url)
            results.append({
                'url': paste_url,
                'content': paste_content
            })
    return results

def fetch_pastebin_content(url):
    try:
        # Convert to raw URL if possible
        if '/raw/' not in url:
            if url.endswith('/'):
                url = url[:-1]
            url = url.replace('pastebin.com/', 'pastebin.com/raw/')
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text[:2000]  # Limit to first 2000 chars for safety
        else:
            return f"Failed to fetch content: HTTP {resp.status_code}"
    except Exception as e:
        return f"Error fetching content: {e}"

def scrape_pastebin_psbdmp(term, search_type='general'):
    """
    Search Pastebin dumps using the psbdmp.ws API.
    search_type: 'general', 'email', or 'domain'
    """
    if search_type == 'general':
        url = f'https://psbdmp.ws/api/search/{term}'
    elif search_type == 'email':
        url = f'https://psbdmp.ws/api/search/email/{term}'
    elif search_type == 'domain':
        url = f'https://psbdmp.ws/api/search/domain/{term}'
    else:
        return {'error': 'Invalid search_type'}

    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        return {'error': f'HTTP {resp.status_code}', 'url': url}
    data = resp.json()
    results = []
    # Robustly handle different response types
    if isinstance(data, dict) and 'data' in data:
        entries = data['data']
    elif isinstance(data, list):
        entries = data
    else:
        entries = []
    for entry in entries:
        paste_id = entry.get('id') if isinstance(entry, dict) else None
        if paste_id:
            results.append(f'https://psbdmp.ws/{paste_id}')
    return {
        'search_type': search_type,
        'term': term,
        'count': len(results),
        'urls': results
    } 