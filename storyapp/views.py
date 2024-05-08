from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from .models import GeneratedStory
import openai
# path = './saved_models/Story_generation_text'
#
# tokenizer = AutoTokenizer.from_pretrained(path)
# model = AutoModelForCausalLM.from_pretrained(path)
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv

load_dotenv()


def chain_setup():
    template = """Generate a short fictional story in 5-6 sentences on the given topic.
                                    ```{text}``` 
                  The story should have a clear beginning, middle, and end 
                  with a logical narrative flow. Develop the characters and 
                  setting with descriptive details to engage the reader. 
                  Incorporate elements of the specified genre such as mystery, romance, or 
                  science fiction. The story should be family-friendly and short in length.
                  
                  STORY:
               """

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
                         model_kwargs={"temperature": 1, "max_new_tokens": 250})

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    return llm_chain


def generate_response(question, llm_chain):
    response = llm_chain.run(question)
    return response


def split_string_at_story(text):
    text = text.split("STORY:", 1)[-1].strip()
    text_string = text[:(text.rfind('.')) + 1]
    return text_string


llm_chain = chain_setup()


# Create your views here.
def home(request):
    return render(request, "storyapp/home.html")


def story_predictor(request):
    if request.method == "POST":
        prompt = request.POST['prompt']

        response = generate_response(prompt, llm_chain)
        generated_text = split_string_at_story(response)

        generated_story = GeneratedStory(generated_text=generated_text)
        generated_story.save()

        return render(request, "storyapp/page.html", {'reslut': str(generated_text)})
    return render(request, "storyapp/page.html")
