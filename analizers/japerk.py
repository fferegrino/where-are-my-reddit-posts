import requests # http://docs.python-requests.org/en/master/user/quickstart/#make-a-request

mashape_key = ""

def japerk_sentiment(text):
    # http://text-processing.com/docs/sentiment.html
    url = 'https://japerk-text-processing.p.mashape.com/sentiment/'
    headers = {
        "X-Mashape-Key": mashape_key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    payload = {
        "language": "english",
        "text": text
    }
    request = requests.post(url, headers=headers, data=payload)
    return request.json()
