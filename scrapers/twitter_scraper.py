import tweepy

def scrape_twitter(domain):
    # You must fill in your own credentials here
    client = tweepy.Client(bearer_token="4af875071b17cc9d92c5d8ae193e4a59f4c86e23")
    results = []
    query = f'"{domain}" -is:retweet'
    tweets = client.search_recent_tweets(query=query, max_results=100)
    for tweet in tweets.data or []:
        results.append({
            "id": tweet.id,
            "text": tweet.text
        })
    return results 