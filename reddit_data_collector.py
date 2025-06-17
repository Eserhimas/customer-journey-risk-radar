import praw  
import csv  
import json  
import os
import datetime  
from typing import List, Dict, Any  
import time 
from dotenv import load_dotenv

load_dotenv()

class RedditDataCollector:  
    def __init__(self, client_id: str, client_secret: str, user_agent: str):  
        """Reddit API connection."""  
        self.reddit = praw.Reddit(  
            client_id=client_id,  
            client_secret=client_secret,  
            user_agent=user_agent  
        )  
      
    def search_subreddits(self,   
                         subreddits: List[str],   
                         keywords: List[str],  
                         limit: int = 100,  
                         time_filter: str = "week") -> List[Dict[str, Any]]:  
        """  
        Search multiple subreddits for posts containing keywords.  
          
        Args:  
            subreddits: List of subreddits  
            keywords: List of keywords  
            limit: Maximum posts per keyword & per subreddit  
            time_filter: Period ("all", "day", "week", "month", "year")  
          
        Returns:  
            list of dictionaries containing posts  
        """  
        collected_data = []  
          
        for subreddit_name in subreddits:  
            print(f"Searching r/{subreddit_name}...")  
            subreddit = self.reddit.subreddit(subreddit_name)  
              
            for keyword in keywords:  
                print(f"  Searching for: '{keyword}'")  
                try:  
                    for submission in subreddit.search(  
                        query=keyword,  
                        sort="relevance",  
                        time_filter=time_filter,  
                        limit=limit  
                    ):  
                        post_data = self._extract_submission_data(submission, keyword)  
                        collected_data.append(post_data)  
                          
                    # Reddit's API limiting the rate
                    time.sleep(1)  
                      
                except Exception as e:  
                    print(f"Error searching r/{subreddit_name} for '{keyword}': {e}")  
                    continue  
          
        return collected_data  
      
    def _extract_submission_data(self, submission, search_keyword: str) -> Dict[str, Any]:  
        """extracting the relevant data"""  
        return {  
            'id': submission.id,  
            'title': submission.title,  
            'selftext': submission.selftext,  # Post body text  
            'author': str(submission.author) if submission.author else '[deleted]',  
            'subreddit': str(submission.subreddit),  
            'score': submission.score,  
            'upvote_ratio': submission.upvote_ratio,  
            'num_comments': submission.num_comments,  
            'created_utc': submission.created_utc,  
            'created_datetime': datetime.datetime.fromtimestamp(submission.created_utc).isoformat(),  
            'url': submission.url,  
            'permalink': f"https://reddit.com{submission.permalink}",  
            'is_self': submission.is_self,  
            'over_18': submission.over_18,  
            'search_keyword': search_keyword,  
            'collected_at': datetime.datetime.now().isoformat()  
        }  
      
    def save_to_json(self, data: List[Dict[str, Any]], filename: str):  
        """saving the data as JSON"""  
        with open(filename, 'w', encoding='utf-8') as f:  
            json.dump(data, f, indent=2, ensure_ascii=False)  
        print(f"Data saved to {filename}")  
      
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str):  
        """saving the data as CSV."""  
        if not data:  
            print("No data to save")  
            return  
              
        fieldnames = data[0].keys()  
        with open(filename, 'w', newline='', encoding='utf-8') as f:  
            writer = csv.DictWriter(f, fieldnames=fieldnames)  
            writer.writeheader()  
            writer.writerows(data)  
        print(f"Data saved to {filename}")  
        
def main():  
    # Reddit configs  
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
     
    USER_AGENT = "RedditDataCollector/1.0 by YourUsername"  
      
    # subreddits and keywords  
    target_subreddits = [  
        "netflix",  
        "cordcutters",   
        "netflixbestof"
    ]  
      
    search_keywords = [  
        "ads", "trending", "heard", "trailer",
        "signup", "sign up", "create account", "email issue",
        "onboarding", "welcome screen", "device setup",
        "recommendation", "search", "can't find", "suggestions",
        "buffering", "lag", "audio out of sync", "playback", "4K issue",
        "charged", "billing", "payment failed", "credit card",
        "cancel", "unsubscribe", "switching", "quitting"  
    ]  
      
    # init collector  
    collector = RedditDataCollector(CLIENT_ID, CLIENT_SECRET, USER_AGENT)  
      
    # data collecting
    print("Starting data collection...")  
    collected_posts = collector.search_subreddits(  
        subreddits=target_subreddits,  
        keywords=search_keywords,  
        limit=50,  # Posts per keyword per subreddit  
        time_filter="week"  
    )  
      
    print(f"Collected {len(collected_posts)} posts")  
      
    # results  
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  
    collector.save_to_json(collected_posts, f"reddit_data_{timestamp}.json")  
    collector.save_to_csv(collected_posts, f"reddit_data_{timestamp}.csv")  
  
if __name__ == "__main__":  
    main()