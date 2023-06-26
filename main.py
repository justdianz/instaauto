import instagrapi
import os.path as path
import logging
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(filename='logs/app.log', format='%(asctime)s: %(levelname)s: %(message)s',level=logging.INFO)

ig = instagrapi.Client(delay_range=[1,3])


try:
    if path.exists('./session.json'):
        ig.load_settings('./session.json')
    else:
        ig.login(os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'))
        ig.dump_settings('./session.json')
    logging.info('Success login')
except instagrapi.exceptions.LoginRequired as e:
    logging.error(e)
except Exception as e:
    logging.error(e)
    exit(1)

'''
Cek permintaan foollback lewat DM
'''
def dm_requests_follback():
    global ig
    threads = ig.direct_threads()

'''
Kasih like ke setiap feed post di beranda
'''
def give_like_feeds():
    global ig
    try:
        feeds = ig.get_timeline_feed()
        # filter hanya yang difollow untuk di like
         # feeds = list(filter(lambda feed: feed['media_or_ad']['user']['friendship_status']['following'] == True, feeds['feed_items']))
        for feed in feeds['feed_items']:
            if feed.get('media_or_ad') and feed['media_or_ad']['user']['friendship_status']['following'] == True and not feed['media_or_ad']['has_liked']:
                feedId = feed['media_or_ad']['id']
                ig.media_like(feedId)
                logging.info(f'liked post id: {feedId}')
    except Exception as e:
        logging.error(e)            

if __name__ == '__main__':    
    # run scheduler
    schedule.every(30).seconds.do(give_like_feeds)
    while True:
        schedule.run_pending()
        time.sleep(10)