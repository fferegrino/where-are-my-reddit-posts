# where are my reddit posts?  

This code was written for the Masters Develpment Project at the University Of Glasgow.

### Dependencies
The scripts developed have dependencies to:  

 - `argparse`
 - `nltk`
 - `praw`
 - `news-please`. 

## 1. Crawl Reddit

The first step was obtaining the links to each news article submission, focused on the information regarding the identifier of the submission within the Reddit system, the URL of the article submitted and how many downvotes, upvotes and the overall score of the submission. For this task, we used the Python Reddit API Wrapper (PRAW) in its 5.1.0 version. This library is available via the ‘Python Package Index’, the PRAW library is one of the most reliable API clients for the Reddit API, as it is configured to automatically respect the rules set by Reddit when consuming their services.  

```
usage: crawl.py [-h] [-o OUTPUT_FILE] subreddit from_date to_date keys_file

Crawl posts from a subreddit given a pair of dates

positional arguments:
  subreddit             the subreddit to crawl
  from_date             ending date (yyyy-MM-dd)
  to_date               starting date (yyyy-MM-dd)
  keys_file             route to the file containing the keys for reddit

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        the file where I should save the results
```

Example:  

```
python crawl.py glasgow 2017-01-01 2017-02-01 keys.txt -o data/glasgow-posts.csv
```

## 2. Crawl News sites
The second step was to retrieve the actual news article from the respective publisher’s website, as well as the comments made about the article on Reddit, but because of the time and resource limitations, from the average of 20 submissions per day we tried to download only 5 per day, but since some sites are hard to scrape, we end up with an average of 4.5 articles per day. For this task, we used two packages, one of them is again, PRAW. The library we were currently using for the first step. With PRAW we are collecting the *score* of each submission as well as the comments (each comment also has a score associated).  

As for the news scraping, we tried several packages before settling with `news-please`, which is a “news crawler that extracts structured information from almost any news website”. Given a specific news article's URL, as we are doing currently, *news-please* is able to extract the headline, lead paragraph, main content (textual), images, author's name, publication date and language.    

```
usage: process.py [-h] [-o OUTPUT_FOLDER] input_file keys_file

Get the news and the comments from a set of given reddit submissions

positional arguments:
  input_file            the file to process
  keys_file             route to the file containing the keys for reddit

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        the file where I should save the results
```

Example:  

```
python process.py data/glasgow-posts.csv -o data/crawled
```

## 3. Extract sentiments.   
VADER is used to derive a sentiment score from each news and user opinion on news. VADER provides a compound sentiment score between -1.0 and 1.0 for the text fed to it. Each text sentiment score is then compared to a (compound sentiment) threshold for classification as either positive or negative.   

```
usage: analize.py [-h] [-o OUTPUT_FILE] input_folder

Analyze the sentiments of a bunch of News and their Reddit coments

positional arguments:
  input_folder          the file folder with the .json files to process

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        the file where I should save the results
```

```
python analize.py data/crawled
```

