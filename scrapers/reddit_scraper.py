import praw

def scrape_reddit(domain):
    # You must fill in your own credentials here
    reddit = praw.Reddit(
        client_id="zTi5erZpMr4OXKNq_HIskw",
        client_secret="knTk6JLAONFKHMmIuDMFo_M_D2AgVg",
        user_agent="scraper by tester"
    )
    results = []
    for submission in reddit.subreddit("all").search(domain, limit=100):
        results.append({
            "title": submission.title,
            "url": submission.url,
            "permalink": f"https://reddit.com{submission.permalink}"
        })
    return results 