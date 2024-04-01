import streamlit as st
import openai
import os
# from chat_internal import get_challenge_tags
import sqlite3
from datetime import datetime
from random import randint
# from sidebar import sidebar
from dotenv import load_dotenv
import json

# conn = sqlite3.connect('chat_data.db')
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS chat_history (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         session_id INTEGER,
#         user_msg TEXT,
#         assistant_msg TEXT,
#         master_schema NVARCHAR,
#         incremental_update NVARCHAR,
#         changelog NVARCHAR,
#         timestamp TEXT,
#         FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
#     )
               
# ''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
#     user_id INTEGER PRIMARY KEY,
#     aggregated_tags TEXT,
#     summary TEXT,
#     engagement_metrics TEXT,
#     last_interaction TIMESTAMP,
#     total_interactions INTEGER
# );
# ''')

def create_tables():
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    
    # create chat_history 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id INTEGER,
        user_msg TEXT,
        assistant_msg TEXT,
        master_schema NVARCHAR,
        incremental_update NVARCHAR,
        changelog NVARCHAR,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
    )
               
''')
    # create user_profiles
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        aggregated_tags TEXT,
        summary TEXT,
        engagement_metrics TEXT,
        last_interaction TIMESTAMP,
        total_interactions INTEGER
    );
    ''')
    
    # #Submit changes and close database connection
    # conn.commit()
    # conn.close()
    
#Calling functions to create tables
create_tables()
    


load_dotenv()

# sidebar()

# openai_api_key = st.session_state.get("OPENAI_API_KEY")
openai_api_key = st.secrets["OPENAI_API_KEY"]

# if not openai_api_key:
#     st.warning(
#         "Enter your OpenAI API key in the sidebar. You can get a key at"
#         " https://platform.openai.com/account/api-keys."
#     )



master_schema = {
  "initial_source": {
    "online_forums": {"present": None, "indicative_text": ""},
    "medical_professionals": {"present": None, "indicative_text": ""},
    "family_friends": {"present": None, "indicative_text": ""},
    "social_media": {"present": None, "indicative_text": ""},
    "news_articles": {"present": None, "indicative_text": ""},
    "tv_movies": {"present": None, "indicative_text": ""}
  },
  "initial_knowledge": {
    "beginner": {"present": None, "indicative_text": ""},
    "intermediate": {"present": None, "indicative_text": ""},
    "advanced": {"present": None, "indicative_text": ""},
    "expert": {"present": None, "indicative_text": ""}
  },
  "relationship": {
    "parent": {"present": None, "indicative_text": ""},
    "sibling": {"present": None, "indicative_text": ""},
    "grandparent": {"present": None, "indicative_text": ""},
    "child": {"present": None, "indicative_text": ""},
    "friend": {"present": None, "indicative_text": ""},
    "coworker": {"present": None, "indicative_text": ""},
    "acquaintance": {"present": None, "indicative_text": ""},
    "stranger": {"present": None, "indicative_text": ""},
    "non_directed": {"present": None, "indicative_text": ""},
    "long_term": {"present": None, "indicative_text": ""},
    "short_term": {"present": None, "indicative_text": ""},
    "very_close": {"present": None, "indicative_text": ""},
    "moderately_close": {"present": None, "indicative_text": ""},
    "not_close": {"present": None, "indicative_text": ""},
    "strained": {"present": None, "indicative_text": ""},
    "estranged": {"present": None, "indicative_text": ""}
  },
  "reaction_and_motivation": {
    "altruism": {"present": None, "indicative_text": ""},
    "personal_fulfillment": {"present": None, "indicative_text": ""},
    "health_concerns": {"present": None, "indicative_text": ""},
    "family_pressure": {"present": None, "indicative_text": ""},
    "positive": {"present": None, "indicative_text": ""},
    "negative": {"present": None, "indicative_text": ""},
    "uncertain": {"present": None, "indicative_text": ""}
  },
  "emotions_and_support": {
    "supported": {"present": None, "indicative_text": ""},
    "unsupported": {"present": None, "indicative_text": ""},
    "neutral": {"present": None, "indicative_text": ""},
    "anxiety": {"present": None, "indicative_text": ""},
    "hopeful": {"present": None, "indicative_text": ""},
    "fearful": {"present": None, "indicative_text": ""},
    "relief": {"present": None, "indicative_text": ""},
    "gratitude": {"present": None, "indicative_text": ""},
    "isolation": {"present": None, "indicative_text": ""},
    "professional_support": {"present": None, "indicative_text": ""},
    "family_support": {"present": None, "indicative_text": ""},
    "friend_support": {"present": None, "indicative_text": ""},
    "online_community_support": {"present": None, "indicative_text": ""}
  },
  "information_seeking_behavior": {
    "active_searcher": {"present": None, "indicative_text": ""},
    "passive_interest": {"present": None, "indicative_text": ""},
    "specific_questions": {"present": None, "indicative_text": ""},
    "general_information": {"present": None, "indicative_text": ""},
    "medical_procedures": {"present": None, "indicative_text": ""},
    "donor_rights": {"present": None, "indicative_text": ""},
    "health_outcomes": {"present": None, "indicative_text": ""},
    "psychological_impact": {"present": None, "indicative_text": ""},
    "insurance_costs": {"present": None, "indicative_text": ""}
  },
  "concerns_and_health": {
    "recovery_time": {"present": None, "indicative_text": ""},
    "health_risks": {"present": None, "indicative_text": ""},
    "lifestyle_impact": {"present": None, "indicative_text": ""},
    "long_term_health": {"present": None, "indicative_text": ""},
    "surgery_fears": {"present": None, "indicative_text": ""},
    "underlying_conditions": {"present": None, "indicative_text": ""},
    "immediate_health_concerns": {"present": None, "indicative_text": ""},
    "eligibility_worries": {"present": None, "indicative_text": ""}
  },
  "lifestyle_changes": {
    "diet_changes": {"present": None, "indicative_text": ""},
    "exercise_limitations": {"present": None, "indicative_text": ""},
    "activity_restrictions": {"present": None, "indicative_text": ""},
    "long_term_lifestyle": {"present": None, "indicative_text": ""},
    "short_term_adjustments": {"present": None, "indicative_text": ""},
    "work_life_balance": {"present": None, "indicative_text": ""},
    "daily_routines": {"present": None, "indicative_text": ""}
  },
  "ethical_and_social_perceptions": {
    "ethical_dilemmas": {"present": None, "indicative_text": ""},
    "moral_responsibility": {"present": None, "indicative_text": ""},
    "social_judgment": {"present": None, "indicative_text": ""},
    "societal_pressure": {"present": None, "indicative_text": ""},
    "cultural_beliefs": {"present": None, "indicative_text": ""},
    "family_expectations": {"present": None, "indicative_text": ""},
    "donor_anonymity": {"present": None, "indicative_text": ""},
    "recipient_compatibility": {"present": None, "indicative_text": ""}
  },
  "decision_stage": {
    "considering": {"present": None, "indicative_text": ""},
    "researching": {"present": None, "indicative_text": ""},
    "deciding": {"present": None, "indicative_text": ""},
    "preparing": {"present": None, "indicative_text": ""},
    "awaiting_surgery": {"present": None, "indicative_text": ""},
    "post_decision_reflections": {"present": None, "indicative_text": ""}
  },
  "readiness_and_impact": {
    "emotionally_ready": {"present": None, "indicative_text": ""},
    "not_ready": {"present": None, "indicative_text": ""},
    "financially_prepared": {"present": None, "indicative_text": ""},
    "financial_concerns": {"present": None, "indicative_text": ""},
    "family_impact": {"present": None, "indicative_text": ""},
    "career_impact": {"present": None, "indicative_text": ""},
    "emotional_impact": {"present": None, "indicative_text": ""},
    "physical_preparedness": {"present": None, "indicative_text": ""},
    "health_assessment_actions": {"present": None, "indicative_text": ""}
  },
  "long_term_implications": {
    "health_monitoring": {"present": None, "indicative_text": ""},
    "lifestyle_adjustments": {"present": None, "indicative_text": ""},
    "medical_follow_up": {"present": None, "indicative_text": ""},
    "insurance_implications": {"present": None, "indicative_text": ""},
    "future_health_concerns": {"present": None, "indicative_text": ""},
    "dietary_considerations": {"present": None, "indicative_text": ""},
    "activity_level_adjustments": {"present": None, "indicative_text": ""}
  },
  "recipient_influence": {
    "urgent_need": {"present": None, "indicative_text": ""},
    "stable_condition": {"present": None, "indicative_text": ""},
    "declining_health": {"present": None, "indicative_text": ""},
    "medical_advisability": {"present": None, "indicative_text": ""},
    "compatibility_concerns": {"present": None, "indicative_text": ""},
    "success_likelihood": {"present": None, "indicative_text": ""}
  },
  "relationship_dynamics": {
    "emotional_bond": {"present": None, "indicative_text": ""},
    "expectations_post_donation": {"present": None, "indicative_text": ""},
    "relationship_concerns": {"present": None, "indicative_text": ""},
    "positive_dynamics": {"present": None, "indicative_text": ""},
    "negative_dynamics": {"present": None, "indicative_text": ""},
    "family_dynamics": {"present": None, "indicative_text": ""},
    "social_dynamics": {"present": None, "indicative_text": ""}
  },
  "additional_information_needs": {
    "medical_procedures": {"present": None, "indicative_text": ""},
    "donor_rights": {"present": None, "indicative_text": ""},
    "experiences_of_other_donors": {"present": None, "indicative_text": ""},
    "long_term_outcomes": {"present": None, "indicative_text": ""},
    "psychological_support": {"present": None, "indicative_text": ""},
    "financial_assistance": {"present": None, "indicative_text": ""},
    "legal_aspects": {"present": None, "indicative_text": ""},
    "recipient_recovery": {"present": None, "indicative_text": ""}
  },
  "social_influence_and_perception": {
    "media_influence": {"present": None, "indicative_text": ""},
    "social_network_opinions": {"present": None, "indicative_text": ""},
    "public_perception": {"present": None, "indicative_text": ""},
    "stigma": {"present": None, "indicative_text": ""},
    "celebrity_endorsements": {"present": None, "indicative_text": ""},
    "community_support": {"present": None, "indicative_text": ""},
    "misinformation": {"present": None, "indicative_text": ""}
  },
  "personal_values_and_growth": {
    "sense_of_purpose": {"present": None, "indicative_text": ""},
    "moral_alignment": {"present": None, "indicative_text": ""},
    "helping_others": {"present": None, "indicative_text": ""},
    "self_improvement": {"present": None, "indicative_text": ""},
    "personal_fears": {"present": None, "indicative_text": ""},
    "societal_benefit": {"present": None, "indicative_text": ""},
    "legacy": {"present": None, "indicative_text": ""},
    "altruistic_identity": {"present": None, "indicative_text": ""}
  },
  "additional_thoughts": {
    "unresolved_questions": {"present": None, "indicative_text": ""},
    "personal_anecdotes": {"present": None, "indicative_text": ""},
    "seeking_reassurance": {"present": None, "indicative_text": ""},
    "looking_for_connections": {"present": None, "indicative_text": ""},
    "expressing_gratitude": {"present": None, "indicative_text": ""},
    "sharing_concerns": {"present": None, "indicative_text": ""},
    "request_for_resources": {"present": None, "indicative_text": ""},
    "desire_for_discussion": {"present": None, "indicative_text": ""}
  }
}

Template = f'''
Category descriptions are given first, followed by the JSON schema to fill in with each iteration.
1. initial_source: The initial source where the user learned about living kidney donation.
2. initial_knowledge: How knowledgeable the user feels they are at the beginning of the conversation.
3. relationship: The relationship the user has with the person who needs a kidney, length of relationship, etc.
4. reaction_and_motivation: The initial reaction the user had when they learned about the person who needs the kidney, and what motivated the user to learn more about living donation.
5. emotions_and_support: The emotions frequently experienced by the user when thinking about kidney donation and the type of support they have or seek. 
6. information_seeking_behavior: Whether the user actively seeks out information about kidney donation and the kind of questions they have. 
7. concerns_and_health: The user's concerns about living kidney donation and their health-related worries. 
8. lifestyle_changes: How the user considers the potential lifestyle changes resulting from kidney donation. 
9. ethical_and_social_perceptions: The user's ethical or moral considerations and social concerns about kidney donation. 
10. decision_stage: The current stage of the user's decision-making process about whether to donate a kidney. 
11. readiness_and_impact: The user's feelings of readiness for kidney donation and the anticipated or experienced impact on their life. 
12. long_term_implications: The user's considerations regarding the long-term implications of living with one kidney.
13. recipient_influence: How the recipient's current health status and prognosis influence the user's decision. 
14. relationship_dynamics: The complexity of the user's relationship with the recipient and its effect on the decision process.
15. additional_information_needs: Areas where the user feels they need more information to make an informed decision. 
16. social_influence_and_perception: The influence of social perception and external opinions on the user's decision-making process. 
17. personal_values_and_growth: How the decision to donate aligns with the user's personal values and the potential for personal growth. 
18. additional_thoughts: Any additional thoughts or questions the user has about living kidney donation. 

The following JSON schema shows how you should report your analysis of the conversation. Replace 'None' with True if the factor is described by the user. 
    For each True entry, please also provide the text from the user that indicates why the tag is present for the user. You only need to report the tags which are present. 
    Here is the master schema:{master_schema}\
Remember, you don't need to update the entire master schema in your response. Only return the JSON portion of the new tags you've discovered, delimited by special markers
'<<<' and '>>>', and we will update the master schema separately. '''


system_instructions = f"""
You are KidnAI. Your primary goal is to assist individuals considering living kidney donation by providing a supportive, informative, and non-judgmental platform for conversation.
You will guide users through a detailed exploration of their thoughts, feelings, and concerns regarding kidney donation, gathering essential information for a\
comprehensive profile that will help us provide tailored and personalized support to the user. \n \n The schema which needs to be explored is:  + "\n" + {Template} + "\n \n"

Note that the user's feelings may change over the course of the conversation.
User Engagement:
Greet users warmly and introduce your purpose.
Ask open-ended questions to encourage detailed responses.
Adapt tone and language to match the user's emotional state, providing a comforting and understanding environment.
Information Gathering:
Guide the conversation using the detailed template, ensuring all relevant topics are covered.
Ask follow-up questions based on the user's responses to gather more specific information.
Clarify and summarize the user's input when necessary to confirm understanding and accuracy.
Encourage reflection on factors influencing the decision, including health, ethical, moral, social, and psychological aspects.
Providing Information:
Share relevant information about living kidney donation as prompted by the user’s questions or concerns. 
Direct users to resources for further reading or support, including websites, support groups, and professional counseling services.
When asking questions, ask only one at a time. Also note that the schema is only for you, not the user."""

st.title("KidnAI")



# def update_master_schema_and_create_change_log(master_schema, incremental_updates, timestep):
#     change_log_entry = {"timestep": timestep, "changes": []}
    
#     for category, updates in incremental_updates.items():
#         for tag, details in updates.items():
#             present = details.get("present")
#             indicative_text = details.get("indicative_text")
#             if category in master_schema and tag in master_schema[category]:
#                 master_schema[category][tag]["present"] = present
#                 master_schema[category][tag]["indicative_text"] = indicative_text
#                 change_log_entry["changes"].append({
#                     "category": category,
#                     "tag": tag,
#                     "present": present,
#                     "indicative_text": indicative_text
#                 })
#             else:
#                 # Optionally handle new tags/categories if applicable
#                 pass
                
#     return master_schema, change_log_entry

def update_master_schema_and_create_change_log(master_schema, incremental_updates, timestep):
    change_log_entry = {"timestep": timestep, "changes": []}
    
    for category, updates in incremental_updates.items():
        for tag, details in updates.items():
            present = details.get("present")
            indicative_text = details.get("indicative_text")
            if category in master_schema:
                if tag in master_schema[category]:
                    # Update existing tag
                    master_schema[category][tag]["present"] = present
                    master_schema[category][tag]["indicative_text"] = indicative_text
                else:
                    # Add new tag to existing category
                    master_schema[category][tag] = {"present": present, "indicative_text": indicative_text}
            else:
                # Create new category and add new tag
                master_schema[category] = {tag: {"present": present, "indicative_text": indicative_text}}
            
            # Record the change log
            change_log_entry["changes"].append({
                "category": category,
                "tag": tag,
                "present": present,
                "indicative_text": indicative_text
            })
                
    return master_schema, change_log_entry


def analyze_and_fill_template(conversation_history, template):
    # Concatenate conversation history into a single string
    # OR do we take only the last step as input?
    conversation_text = " ".join([message["content"] for message in conversation_history if message["role"] in ["user", "assistant"]])

    # Here, you'd call your second LLM to analyze the conversation.
    # For demonstration, I'll call the same OpenAI API, but you'd replace this with your specific analysis call.
    analysis_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  
        response_format={"type":"json_object"},
        messages=[{"role": "system", "content": "Your task is to identify and return JSON tags based on relevant information. I will give you the user's written answers \
                            (extracted from a chatbot conversation) and based on the provided answers you must fill and return the tags that will be put into the new sample of our database\
                            As I will be progressively providing you the answers, you can also progressively fill information from the schema"},
        {"role": "user", "content": f"Analyze the conversation and extract living kidney donor profile tags in JSON format, with coarse and granular tags \
                                    as shown: \nConversation: {conversation_text}\n\nTemplate: {template}"}])
    
    filled_template = analysis_response.choices[0]["message"]["content"]
    return filled_template

def extract_json_from_response(response):
    start_marker = "<<<"
    end_marker = ">>>"
    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index)
    if start_index != -1 and end_index != -1:
        json_str = response[start_index + len(start_marker):end_index].strip()
        try:
          return json.loads(json_str)
        except json.JSONDecodeError:
          print("Error decoding JSON")  
          return None


def insert_into_chat_history(user_id, session_id, user_msg, assistant_msg, master_schema, incremental_update, changelog):
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    
  
    master_schema_json = json.dumps(master_schema)
    incremental_update_json = json.dumps(incremental_update)
    changelog_json = json.dumps(changelog)
    
    cursor.execute('''
        INSERT INTO chat_history (user_id, session_id, user_msg, assistant_msg, master_schema, incremental_update, changelog)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, session_id, user_msg, assistant_msg, master_schema_json, incremental_update_json, changelog_json))

    # conn.commit()
    # conn.close()

def insert_into_user_profiles(user_id, aggregated_tags, summary, engagement_metrics, last_interaction, total_interactions):
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_profiles (user_id, aggregated_tags, summary, engagement_metrics, last_interaction, total_interactions)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, aggregated_tags, summary, engagement_metrics, last_interaction, total_interactions))

    # conn.commit()
    # conn.close()



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_instructions})
    response_initial = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
    #response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": "give me a brief introduction and engage me into a interactive conversation by asking me questions to fill in the usecase template !"}
    ]
    )
    print(response_initial.choices[0])
    st.session_state.messages.append({"role": "assistant", "content": response_initial.choices[0]["message"]["content"]})

# initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-4-1106-preview"
if 'disabled' not in st.session_state:
    st.session_state.disabled = False
if 'return_filled_template' not in st.session_state:
    st.session_state.return_filled_template = f"Filled Template: \n {Template}"
if 'master_schema' not in st.session_state:
    st.session_state.master_schema = master_schema

# Setting system message

for message in st.session_state["messages"]:
    if (message["role"] == "user") or (message["role"] == "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 1000px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
    
# input from user
user_input = st.chat_input("Your prompt",disabled=st.session_state.disabled)
# st.sidebar.markdown(st.session_state.return_filled_template)
if user_input:
    st.session_state.disabled = True
    st.chat_input("The answer is being generated, please wait...", disabled=st.session_state.disabled)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        #st.chat_input("Your prompt",disabled=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})



    chat_history = {}
    chat_length = 0
    print(len(st.session_state["messages"]))
    for message in st.session_state["messages"]:
        if (message["role"] == "user") or (message["role"] == "assistant"):
            chat_length= chat_length+1
            chat_history[chat_length] = {message["role"]: message["content"]}
    #print(chat_history)
    # temp_items = get_challenge_tags(str(chat_history))
    filled_template = analyze_and_fill_template(st.session_state.messages, Template)
    incremental_update = extract_json_from_response(filled_template)
    if incremental_update:
        master_schema, change_log_entry = update_master_schema_and_create_change_log(master_schema, incremental_update, chat_length)
    # After calling `analyze_and_fill_template`
    st.markdown(f"#### Updated Master Schema:")
    st.write(master_schema)

    # Sort the list based on the numeric values in descending order
    #print(items_temp)
    # st.session_state.return_filled_template = "Filled Template: \n" + temp_items

    st.session_state.disabled = False
    st.rerun()
