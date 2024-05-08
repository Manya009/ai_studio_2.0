from django.shortcuts import render
import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv('OPENAI_API_KEY')
headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {api_key}"}


def image_generator(request):
    url = "https://api.openai.com/v1/images/generations"
    if request.method == "POST":
        pro = request.POST['prompt']

        payload = {"model": "dall-e-2", "prompt": pro,
                   "n": 1, "size": "512x512"}
        response = requests.post(url, json=payload, headers=headers)
        response = response.json()
        url = response['data'][0]['url']

        return render(request, "imageapp/image.html", {'reslut': str(url)})
    return render(request, "imageapp/image.html")
