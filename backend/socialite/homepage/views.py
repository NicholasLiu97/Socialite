import tweepy
import requests
from django import forms
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.


class NewPostForm(forms.Form):
    img = forms.ImageField()
    # task = forms.IntegerField(min_value=0, max_value=10)
    content = forms.CharField(label="content")


def handle_uploaded_file(f, fname):
    with open(str(settings.BASE_DIR) + '/' + fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data["content"]
            img = form.cleaned_data["img"]

            # upload files to storage
            handle_uploaded_file(request.FILES['img'], str(img))
        else:
            return render(request, "homepage/index.html", context={
                "form": form
            })
        if content:
            print('Content: ', content)
            print(f"img: {img}")

            tw_response = publish_to_tw(content)
            fb_response = publish_to_fb(content)

            print(f"tw_post_response: {tw_response}")
            print(f"fb_post_response: {fb_response}")

            return redirect('index')

    return render(request, 'homepage/index.html', context={
        "form": NewPostForm()
    })
