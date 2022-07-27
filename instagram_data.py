from dotenv import load_dotenv
import os
from instagrapi import Client

load_dotenv()

cl = Client()
cl.login(os.getenv('username'), os.getenv('password'))

hashtag = cl.hashtag_info('tourism')
print(hashtag.dict())
