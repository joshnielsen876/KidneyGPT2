import openai
import os
import streamlit as st


openai.api_key = st.secrets["OPENAI_API_KEY"]


detected_text = """
You must classify each AgriFood use case into multiple one-word tags that will later be used 
to match the use case with a certain pre-existing template for defining the use case challenge in depth. 
Each use case may have more than one tag and may be matched with more than one template. 
Your job is to provide the tags, NOT to find the challenge template to match the use case with. 

The user input is a chat converation with an AI chatbot, so based on the chat conversation, please extract and understand the discussed usecase, and then classify this 
extracted usecase from the chat conversation into multiple one-words tags with the corresponding confidence/relevance factor (ranging from 0.0 to 1.0) next to it.
\n
Also, when classifying a usecase into multiple one-word tags please mention the confidence/relevance factor (ranging from 0 to 1) for with the given usecase is similar to each classified one-word tag.


"""

def read_list_from_file(file_path):
    with open(file_path, 'r') as file:
        # Reading the content of the file
        content = file.read()
        # Evaluating the content to convert it to a list
        list_from_file = eval(content)
    return list_from_file

tag_list = read_list_from_file("tags_AVA.txt")
tags_str = ", ".join(tag_list)

def get_challenge_tags(chat_convo):
    global tags_str
    global detected_text
    prompt = ""
    tag_cond = ""
    tag_cond = tag_cond + " Sometimes the input tags are redundant, i.e. multiple tags have similar meaning/use, I want you to condense/club these similar tags and then classify the user-input usecases into multiple one-word clubbed/condensed/clustered tags. \n"
    tag_cond = tag_cond + " Based on the provided one-word tags, you must classify each user-given/input usecase (the uscase must be analyzed and extracted from a chat conversation with an AI chatbot) into. each one-word tag is seperated by commas',' . Please refer to these one-word tags only, and classify the following user-input usecases (the uscase must be analyzed and extracted from a chat conversation with an AI chatbot) into these mentioned tags only. You must classify each user-input AgriFood use case into multiple one-word tags given here. \n The multiple one-word tags are: "
    tag_cond = tag_cond + tags_str
    prompt = tag_cond + detected_text

    response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "system", "content": prompt},
                            {"role": "user", "content": "Input USE Case Coveration (please analyze the user usecase from this conversation with an AI chatbot to generate relevant multiple one-word tags with corresponding relevance/confidence factor next to it), also only just give me the one-word tags, do not provide any justfications on why these tags are genrated, just only give me the one-word tags with corresponsing confidence/relevance scores (the oneword tags and the corresponding relevance score should be represented/seperated using ' - ', i.e. oneword_tag - relevance_score) for each usecase extraced from the input/given user conversation: \n \n " + chat_convo}
                ])
    return str(response["choices"][0]["message"]["content"])
    