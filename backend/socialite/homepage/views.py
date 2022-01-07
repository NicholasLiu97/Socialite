import os
import tweepy
import requests
from django import forms
from django.conf import settings
from django.shortcuts import render, redirect
import facebook as fb

# Create your views here.


class NewPostForm(forms.Form):
    img = forms.ImageField()
    # task = forms.IntegerField(min_value=0, max_value=10)
    content = forms.CharField(label="content")


def handle_uploaded_file(f, fname):
    try:
        os.mkdir(str(settings.MEDIA_DIR))
    except:
        pass

    # with open(str(settings.BASE_DIR) + '/' + fname, 'wb+') as destination:
    
    with open(str(settings.MEDIA_DIR) + '/' + fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def publish_to_tw(content):
    # OAuth 2 Authentication
    tw_client = tweepy.Client(consumer_key=settings.TW_API_KEY,
                              consumer_secret=settings.TW_API_KEY_SECRET,
                              access_token=settings.TW_ACCESS_TOKEN,
                              access_token_secret=settings.TW_ACCESS_TOKEN_SECRET)

    return tw_client.create_tweet(text=content)

def publish_to_fb(img, content):
    access_token = settings.FB_ACCESS_TOKEN
    graph_api = fb.GraphAPI(access_token=access_token)
    if img and content:
        r = graph_api.put_photo(open(str(settings.MEDIA_DIR) + '/' + img, "rb"), message=content)

    elif img:
        r = graph_api.put_photo(open(str(settings.MEDIA_DIR) + '/' + img, "rb"))
    else:
        r = graph_api.put_object("me", "feed", message=content)
        
    return r



def index(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data["content"]
            img = str(form.cleaned_data["img"])

            # upload files to storage
            handle_uploaded_file(request.FILES['img'], img)
        else:
            return render(request, "homepage/index.html", context={
                "form": form
            })
        if content:
            print('Content: ', content)
            print(f"img: {img}")

            tw_response = publish_to_tw(content)
            fb_response = publish_to_fb(img, content)

            # print(f"tw_post_response: {tw_response}")
            # print(f"fb_post_response: {fb_response}")

            return redirect('index')

    return render(request, 'homepage/index.html', context={
        "form": NewPostForm()
    })
