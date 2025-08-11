import requests
import os
import json

def hackedlist(domain):
    url = "https://hackedlist.io/api/domain"
    params = {"domain": f"{domain}"}
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.8",
        "priority": "u=1, i",
        "referer": "https://hackedlist.io/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)
    data = None
    if response.status_code == 200:
        data = response.json()
    else:
        return {"error": f"Error: {response.status_code}, {response.text}"}

    # Save to output directory
    safe_domain = domain.replace('.', '_')
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{safe_domain}_hackedlist.json")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data 