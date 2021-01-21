import tweepy, csv
import json
import csv
import argparse

##Twitter API
CONSUMER_KEY ='P6F9glaUd7uB3kj5ElRWRXIDm'
CONSUMER_SECRET ='lasmKKLlE0WzOXTe61u1s1PERsuKludoUIkY9W2XWkHf6xxbsW'
auth=tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def run(args):
    filename = args.filename
    json_data=json.load(open(filename,'r'))
    emotion_minimum_words=0
    csv_filename = filename.split('.')[0] + '.csv'
    ids = []
    tags = []
    for item in json_data:
        ids.append(item['tweet_id'])
        tags.append(item['stance'])

    csvfile=open(csv_filename, 'w') 
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow([ 'Tweet ID', 'User', 'Body', 'Created At', 'Retweet Count', 'Favorite Count', 'Tag'])

    for i in range(len(ids)):
        try:
            tid = ids[i]
            tag = tags[i]
            tweet=api.get_status(tid)
            tweet=tweet._json
            user=tweet['user']['screen_name']
            time=tweet['created_at']
            body = tweet['text']
            retweets = tweet['retweet_count']
            favorites = tweet['favorite_count']
            csvwriter.writerow([tid, user, body, time, retweets, favorites, tag])
        except:
            continue
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Getting tweets by id')
    parser.add_argument('--filename', type=str, default='wtwt_ids.json')

    args = parser.parse_args()
    run(args)