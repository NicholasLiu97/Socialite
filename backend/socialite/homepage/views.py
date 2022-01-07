import tweepy
import requests
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.

def publish_to_tw(content):
    # OAuth 2 Authentication
    tw_client = tweepy.Client(consumer_key=settings.TW_API_KEY,
                            consumer_secret=settings.TW_API_KEY_SECRET,
                            access_token=settings.TW_ACCESS_TOKEN,
                            access_token_secret=settings.TW_ACCESS_TOKEN_SECRET)
    
    return tw_client.create_tweet(text=content)

def publish_to_fb(content):
    post_url = f"https://graph.facebook.com/{settings.FB_PAGE_ID}/feed"
    payload = {
        "message": content,
        "access_token": settings.FB_ACCESS_TOKEN
    }

    r = requests.post(post_url, data=payload)
    return r.text
    
def index(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')

        if content:
            print('Content: ', content)

            tw_response = publish_to_tw(content)
            fb_response = publish_to_fb(content)
            print(f"tw_post_response: {tw_response}")
            print(f"fb_post_response: {fb_response}")
            return redirect('index')

    return render(request, 'homepage/index.html')
