from django.shortcuts import render
import openai
import os
from storyapp.models import GeneratedStory
from .models import Lists
import time
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {api_key}"}


def images_generator(pro):
    url = "https://api.openai.com/v1/images/generations"

    payload = {"model": "dall-e-2", "prompt": pro,
               "n": 1, "size": "1024x1024"}
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()

    url = response['data'][0]['url']
    print(url)
    return url


# check if last character is a full stop
def jay_s(story_list):
    generated_urls = []
    im = 0
    for pro in story_list:
        im += 1
        print(im)
        if im == 6 or im == 11 or im == 16 or im == 21:
            print("Rate limit exceeded. Waiting for 30 seconds...")
            time.sleep(50)
        url = images_generator(pro)
        generated_urls.append(url)
        # generated_url = Images(image_link=url)
        # generated_url.save()
    return generated_urls


def homie(request):
    if request.method == "POST":
        last_story = GeneratedStory.objects.latest('created_at')
        latest_story = last_story.generated_text
        story = str(latest_story)

        story_list = [sentence.strip() for sentence in story.split(".") if sentence.strip()]
        print(story_list)
        print("Length of story_list is: ", len(story_list))

        url_list = jay_s(story_list)
        zipped_list = list(zip(story_list, url_list))

        # Convert the lists to strings with each element separated by a newline character
        url_list_str = '\n'.join(url_list)
        story_list_str = '\n'.join(story_list)

        # Create a new Story object and save it to the database
        new_story = Lists.objects.create(url_list=url_list_str, story_list=story_list_str)

        return render(request, "imagesapp/images.html", {'zipped_list': zipped_list})
    return render(request, "imagesapp/images.html")
