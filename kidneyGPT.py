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
import uuid
import re
from datetime import datetime
import pandas as pd

DATABASE_PATH = 'chat_data.db'
# print(f"Using database at: {os.path.abspath(DATABASE_PATH)}")

def query_database():
    try:
        # 连接数据库
        conn = sqlite3.connect(DATABASE_PATH)
        # print(f"Database Path: {DATABASE_PATH}")

        cursor = conn.cursor()

        # 执行查询操作
        cursor.execute("SELECT * FROM chat_history")

        # 检索所有结果
        rows = cursor.fetchall()

        # # 打印结果
        # if not rows:
        #     print("No data found in the table.")
        # else:
        #     print("Data retrieved successfully:")
        #     for row in rows:
        #         print(row)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # 关闭数据库连接
        conn.close()
        


def create_tables():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")  # 启用外键支持
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            user_msg TEXT,
            assistant_msg TEXT,
            master_schema NVARCHAR,
            incremental_update NVARCHAR,
            changelog NVARCHAR,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            time TEXT PRIMARY KEY,
            user_id TEXT,
            aggregated_tags TEXT,
            summary TEXT,
            engagement_metrics TEXT,
            last_interaction TEXT,
            total_interactions INTEGER
            
        )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


        
#Calling functions to create tables
create_tables()
    


load_dotenv()



# openai_api_key = st.session_state.get("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
Remember, you don't need to update the entire master schema in your response. Only return the JSON portion of the new tags you've discovered, enclosed within special markers using ```json and ```; we will update the master schema separately.
'''


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
When asking questions, ask ONLY ONE at a time."""

st.title("KidnAI")

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())
user_id = st.session_state['user_id']



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



def master_schema_to_dataframe(master_schema):
    data = []
    for category, tags in master_schema.items():
        for tag, details in tags.items():
            present = details.get('present')
            indicative_text = details.get('indicative_text')
            data.append({
                'Category': category,
                'Tag': tag,
                'Present': present,
                'Indicative Text': indicative_text
            })
    df = pd.DataFrame(data)
    return df

def display_master_schema_in_sidebar(master_schema):
    # Convert master schema to dataframe
    df = master_schema_to_dataframe(master_schema)
    
    # Hide the 'Category' column by only selecting the other columns
    df_display = df.drop(columns=['Category'])

    # Ensure session state for expander toggle exists
    if "show_schema" not in st.session_state:
        st.session_state["show_schema"] = True  # Set to True to display the expander initially

    # st.sidebar.title("Master Schema Overview")

    # Add a checkbox to control visibility
    st.session_state["show_schema"] = st.sidebar.checkbox("Show Master Schema", value=st.session_state["show_schema"])

    # Display the expander only if the checkbox is checked
    if st.session_state["show_schema"]:
        with st.sidebar.expander("Show Master Schema", expanded=True):
            st.table(df_display)




def analyze_and_fill_template(conversation_history, template):
    # Concatenate conversation history into a single string
    conversation_text = " ".join([
        message["content"] for message in conversation_history
        if message["role"] in ["user", "assistant"]
    ])

    # Call OpenAI API to analyze the conversation
    analysis_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": (
                    "Your task is to analyze the conversation and extract relevant tags "
                    "in JSON format. Ensure that all property names and string values use double quotes, "
                    "and that the JSON is properly formatted and escaped. "
                    "Please output only the JSON data, enclosed within "
                    "```json\n...\n```."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Please analyze the following conversation and extract tags based on the template:\n\n"
                    f"Conversation: {conversation_text}\n\n"
                    f"Template: {template}"
                )
            }
        ]
    )

    # Retrieve the response
    filled_template = analysis_response.choices[0]["message"]["content"]

    print(f"Filled Template with markers: {filled_template}")

    return filled_template






def extract_json_from_response(response):
    try:
        # print(f"Response content before JSON parsing: {response}")
        
        # Use regular expression to extract content between ```json and ```
        json_match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', response)
        if json_match:
            json_str = json_match.group(1).strip()
            # print(f"Extracted JSON string: {json_str}")
            
            # Clean up the JSON string to ensure it's valid
            json_str = json_str.replace('\\', '\\\\')  # Escape backslashes
            json_str = json_str.replace('\\"', '\\\\"')  # Escape existing escaped quotes
            # Do not replace single quotes
            json_str = json_str.replace("None", "null")
            json_str = json_str.replace("False", "false")
            json_str = json_str.replace("True", "true")
            
            # Parse the JSON string
            parsed_json = json.loads(json_str)
            # print(f"Parsed JSON: {parsed_json}")
            return parsed_json
        else:
            print("No JSON content found between markers.")
            return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None





def insert_into_chat_history(user_id, session_id, user_msg, assistant_msg, master_schema, incremental_update, changelog):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")  
        cursor = conn.cursor()
        

        master_schema_json = json.dumps(master_schema)
        incremental_update_json = json.dumps(incremental_update)
        changelog_json = json.dumps(changelog)

        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (user_id, session_id, user_msg, assistant_msg, master_schema, incremental_update, changelog)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, session_id, user_msg, assistant_msg, master_schema_json, incremental_update_json, changelog_json))

        conn.commit()
       

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()


    

def insert_into_user_profiles(time, user_id, aggregated_tags, summary, engagement_metrics, last_interaction, total_interactions):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
       
        aggregated_tags_json = json.dumps(aggregated_tags) if isinstance(aggregated_tags, (list, dict)) else str(aggregated_tags)
        summary_json = json.dumps(summary) if isinstance(summary, (list, dict)) else str(summary)
        engagement_metrics_json = json.dumps(engagement_metrics) if isinstance(engagement_metrics, (list, dict)) else str(engagement_metrics)

        # 确保时间戳为字符串
        if isinstance(last_interaction, datetime):
            last_interaction_str = last_interaction.isoformat()
        else:
            last_interaction_str = str(last_interaction)

        
        total_interactions_int = int(total_interactions) if total_interactions is not None else 0

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()


        cursor.execute('''
            INSERT INTO user_profiles (time, user_id, aggregated_tags, summary, engagement_metrics, last_interaction, total_interactions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (time, user_id, aggregated_tags_json, summary_json, engagement_metrics_json, last_interaction_str, total_interactions_int))

        conn.commit()
        # print(f"Data inserted successfully for user_id: {user_id}")

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        if conn:
            conn.close()



# print('Initializing messages in session state:', 'messages' in st.session_state)
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    st.session_state.messages.append({"role": "system", "content": system_instructions})
    response_initial = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
    #response_format={ "type": "json_object" },
    #add temperature setting for consistency
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": "give me a brief introduction and engage me into a interactive conversation by asking me questions to fill in the usecase template !"}
    ],
    temperature = 0
    )
    # print(response_initial.choices[0])
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
# Ensure session state for expander toggle exists
if "expander_open" not in st.session_state:
    st.session_state.expander_open = True  # Set initial state

# Call display function as early as possible
display_master_schema_in_sidebar(st.session_state.master_schema)

# Your other logic for processing the chat and user input below

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
    

def save_user_state():
    now = datetime.now() 
    time = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    user_id = st.session_state['user_id']
    aggregated_tags = st.session_state.master_schema
    summary = "Summary of user interaction"
    engagement_metrics = "User engagement data"
    last_interaction = datetime.now()
    total_interactions = len(st.session_state.messages)

   
    insert_into_user_profiles(
        time,
        user_id,
        aggregated_tags,
        summary,
        engagement_metrics,
        last_interaction,
        total_interactions
    )


# input from user
user_input = st.chat_input("Your prompt", disabled=st.session_state.disabled)

if user_input:
    st.session_state.disabled = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate assistant's reply
    full_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
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
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Analyze and fill template
    filled_template = analyze_and_fill_template(st.session_state.messages, Template)

    # Extract and update JSON data
    incremental_update = extract_json_from_response(filled_template)
    if incremental_update:
        st.session_state.master_schema, change_log_entry = update_master_schema_and_create_change_log(
            st.session_state.master_schema, incremental_update, len(st.session_state.messages)
        )
       
        #

        # Calculate interaction count
        chat_length = len([msg for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]])
        
        # Insert data into chat_history
        temp_user_id = st.session_state.get('user_id', str(uuid.uuid4()))
        temp_session_id = st.session_state.get('session_id', str(uuid.uuid4()))
        
       
        save_user_state()

        
        insert_into_chat_history(
            user_id, temp_session_id, user_input, full_response,
            st.session_state.master_schema, incremental_update, change_log_entry
        )

        
        # Save user state to user_profiles
        save_user_state()
    else:
        print("No incremental update available.")
    
    #Display the pretty version of the schema in the sidebar
    display_master_schema_in_sidebar(master_schema)
    # Re-enable input after response
    st.session_state.disabled = False

    # Optionally display updated master schema
    # st.markdown(f"#### Updated Master Schema:")
    # st.write(st.session_state.master_schema)

    chat_history = {}
    chat_length = 0
    # print(len(st.session_state["messages"]))
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


    st.session_state.disabled = False
    st.rerun()
