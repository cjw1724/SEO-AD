import feedparser

url = "https://trends.google.com/trending/rss?geo=KR"
feed = feedparser.parse(url)

if feed.entries:
    entry = feed.entries[0]
    print(entry.keys())
    for k, v in entry.items():
        if 'traffic' in k:
            print(k, v)
