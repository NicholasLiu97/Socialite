import os
import tweepy
import requests
from django import forms
from django.conf import settings
from django.shortcuts import render, redirect
import facebook as fb
from django.contrib.auth.decorators import login_required

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

    with open(str(settings.MEDIA_DIR) + '/' + fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def publish_to_tw(img, content):
    # OAuth 1.0a
    auth = tweepy.OAuthHandler(settings.TW_API_KEY, settings.TW_API_KEY_SECRET)
    auth.set_access_token(settings.TW_ACCESS_TOKEN,
                          settings.TW_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    media = api.media_upload(str(settings.MEDIA_DIR) + '/' + img)

    print(media.media_id_string)

    return api.update_status(content, media_ids=[media.media_id_string])


def publish_to_fb(img, content):
    access_token = settings.FB_ACCESS_TOKEN
    graph_api = fb.GraphAPI(access_token=access_token)
    if img and content:
        r = graph_api.put_photo(
            open(str(settings.MEDIA_DIR) + '/' + img, "rb"), message=content)

    elif img:
        r = graph_api.put_photo(
            open(str(settings.MEDIA_DIR) + '/' + img, "rb"))
    else:
        r = graph_api.put_object("me", "feed", message=content)

    return r

@login_required
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

            tw_response = publish_to_tw(img, content)
            fb_response = publish_to_fb(img, content)

            # print(f"tw_post_response: {tw_response}")
            # print(f"fb_post_response: {fb_response}")

            return redirect('index')

    return render(request, 'homepage/index.html', context={
        "form": NewPostForm()
    })
