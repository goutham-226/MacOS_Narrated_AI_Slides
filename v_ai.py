from macos_speech import Synthesizer
import time
import replicate

from term_image.image import from_file 

import requests
import os

import cv2
import base64
from PIL import Image
from io import BytesIO
import sys

import threading

from dotenv import load_dotenv

# Load secrets from a local .env file (never commit it)
load_dotenv()
api_tkn = os.getenv("REPLICATE_API_TOKEN")
if not api_tkn:
    sys.exit("REPLICATE_API_TOKEN is not set. Copy .env.example to .env and add your token.")

speaker = Synthesizer()

speaker.text = "Hi I'm Lisa"
speaker.voice = "Alex"
speaker.talk()
speaker.text = "An AI Assistant"
speaker.talk()
speaker.text = "Trained on all of the internet"
time.sleep(1)
speaker.text = "please start searching"
speaker.talk()
print("Type:")
prompt_1 = "-write a narrator only script for 250 seconds that explains the topic"
prompt = input()
prompt = prompt + prompt_1
abt_weather = False
#remove trailing and leading spaces in prompt
test_str = ""
x = 0
while prompt[x] == ' ':
    x+=1
y = len(prompt) - 1
while prompt[y]==' ':
    y-=1
for i in range(x,y+1):
    test_str = test_str + prompt[i]
new_prompt = test_str
print(test_str)

LLM = replicate.Client(api_token=api_tkn)
frst_output=LLM.run("qwen/qwen3-235b-a22b-instruct-2507",
    input={
        "top_p": 1,
        "prompt":test_str,
        "max_tokens": 1024,
        "temperature": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    },
)

script_to_talk = ""
for char in frst_output:
    script_to_talk = script_to_talk + char

spl_inst = " Using the information in the script create 25 prompts to make images place prompts in tags represented by <prmpt></prmpt> for each prompt" 

new_prompt = script_to_talk + spl_inst
output = LLM.run(
    "qwen/qwen3-235b-a22b-instruct-2507",
    input={
        "top_p": 1,
        "prompt": new_prompt,
        "max_tokens": 1024,
        "temperature": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    },
)
llm_output  = ""
for s in output:
    llm_output = llm_output + s
#print(llm_output)

S = llm_output
array_prmpts = []
indx = 0
str_tmp = ''
ln = len(S)
for i in range(0,ln):
    if S[i] == '>':
        str_tmp = ''
    elif S[i] == '<' and S[i+1] == '/':
        array_prmpts.append(str_tmp)
    else:
        str_tmp += S[i]

print()

#for arr in array_prmpts:
    #print(arr)

fl_indx_1_0 = 0
file_names_array = []
for prmpt in array_prmpts:
    temp_str = "output_img"
    temp_str = temp_str+str(fl_indx_1_0)
    temp_str = temp_str+".png"
    file_names_array.append(temp_str)
    fl_indx_1_0 = fl_indx_1_0 + 1
    
fl_index_1_2 = 0
for prmpt in array_prmpts: 
    img_output_server_call = LLM.run(
    "black-forest-labs/flux-2-pro",
    input={
        "prompt": prmpt,
        "resolution": "1 MP",
        "aspect_ratio": "1:1",
        "input_images": [],
        "output_format": "webp",
        "output_quality": 80,
        "safety_tolerance": 2
    })
    #print(img_output_server_call.url)
    response = requests.get(img_output_server_call.url)
    with open(file_names_array[fl_index_1_2],'wb') as file:
         file.write(img_output_server_call.read())
    fl_index_1_2 = fl_index_1_2 + 1

         

     
def talk(str_to_talk):
    speaker.text = str_to_talk
    speaker.talk()
    os.system('clear')

def display_images(file_n):
    for file_1 in file_n:
        image = from_file(file_1)
        image.draw()
        time.sleep(10) 
        os.system('clear')
    

threading.Thread(target=talk, args=(script_to_talk,)).start()
threading.Thread(target=display_images, args=(file_names_array,)).start()


"""
#developer note

#tokenise tags and create a string array
#loop through send each string through a function 
#that creates a string containing prompts
#for each prompt create 10 output files
#in each of those store generated images
#create an async function to generate speech
#create an async function to draw the slide show

# create a function to tokenise each prompt
# take in the string array
# new_final_result = '<prmpt>the prompt</prompt>'
# loop every character
# add to a temp string 
# if temp string if charcter == '>' set temp string to ""
# then add all characters to a temp string
# return temp string

#end of note

"""




#img_model_output = LLM.run('google/imagen-3',input=img_model_input)


#file_name='out.jpg'
#response = requests.get(img_model_output)
#with open(file_name,'wb') as f:
    #f.write(response.content)

#img_Ai = from_file('out.jpg')
#img_Ai.draw()

#speaker.text = llm_output
#speaker.talk()





























