import tweepy

from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')

        if content:
            print('Content: ', content)

            # OAuth 2 Authentication
            client = tweepy.Client(consumer_key=settings.TW_API_KEY,
                                   consumer_secret=settings.TW_API_KEY_SECRET,
                                   access_token=settings.TW_ACCESS_TOKEN,
                                   access_token_secret=settings.TW_ACCESS_TOKEN_SECRET)

            response = client.create_tweet(text=content)
            print(response)

            return redirect('index')

    return render(request, 'homepage/index.html')
