from github import Github

def scrape_github(domain):
    # You must fill in your own token here
    g = Github("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")
    results = []
    query = f'"{domain}" in:readme in:description in:file'
    for repo in g.search_repositories(query=query)[:100]:
        results.append({
            "name": repo.full_name,
            "url": repo.html_url,
            "description": repo.description
        })
    return results 