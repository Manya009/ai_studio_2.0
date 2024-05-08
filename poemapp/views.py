from django.shortcuts import render
from django.shortcuts import render
import re
import openai
import numpy as np
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv

load_dotenv()


def chain_setup():
    template = """Generate a lighthearted poem of 6-8 lines on the given topic.
                                    ```{text}``` 
                  The poem should follow an A-B-C-B rhyme scheme and use creative
                  wordplay or puns to add humor. Incorporate imaginative metaphors and 
                  vivid sensory details to bring the poem to life. The tone should be 
                  playful and whimsical.

                  POEM:
               """

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1",
                         model_kwargs={"max_new_tokens": 250})

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    return llm_chain


def generate_response(question, llm_chain):
    response = llm_chain.run(question)
    return response


def split_string_at_poem(text):
    return text.split("POEM:", 1)[-1].strip()


llm_chain = chain_setup()


def poem_predictor(request):
    if request.method == "POST":
        poem_prompt = request.POST['poem_prompt']

        response = generate_response(poem_prompt, llm_chain)
        generated_lyrics = split_string_at_poem(response)

        return render(request, "poemapp/page01.html", {'reslut': str(generated_lyrics)})
    return render(request, "poemapp/page01.html")
