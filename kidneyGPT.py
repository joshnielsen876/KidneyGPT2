import streamlit as st
import openai
import os
from chat_internal import get_challenge_tags

from dotenv import load_dotenv

load_dotenv()

openai.api_key = st.secrets["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"] #insert your openai API

Template = """
1. I first learned about living kidney donation through [source: online research/friend or family/doctor/other] and my current level of knowledge is [basic/moderate/advanced].
2. The person in need of a kidney transplant is [relationship] to me, and their condition has been affecting their life for [duration]. Our relationship is [description].
3. My initial reaction to the idea of donating a kidney was [reaction] because [reason].
4. The main reasons I am considering donating a kidney are [motivations]. I [have/have not] discussed this with the potential recipient.
5. The emotions I frequently experience when thinking about kidney donation include [emotions]. I [have/have not] sought professional support to discuss these feelings.
6. To better understand kidney donation, I [have/have not] sought information from [sources]. The most important questions I have are [questions].
7. Some of my concerns about living kidney donation include [concerns]. I am particularly worried about [specific worries].
8. The support I currently have from friends, family, and professionals is [description]. I feel [supported/not supported] in my consideration to donate.
9. I [have/have not] considered how donating a kidney might change my lifestyle, including [potential changes]. My biggest health-related concern is [concern].
10. Ethical or moral considerations that weigh on my mind include [considerations]. Socially, I am [concerned/not concerned] about how others may view my decision.
11. Currently, I am at the [stage: considering/researching/deciding/preparing] stage of deciding whether to donate a kidney. This means I am [description of what this stage means to the user].
12. I feel emotionally [ready/not ready] to proceed with the donation because [reasons]. My emotional readiness is influenced by [factors such as personal resilience, support system, understanding of emotional impact].
13. My physical readiness and health concerns include [specific concerns]. I have [taken/have not taken] steps to assess my health eligibility for donation, which involves [actions like visiting a doctor, undergoing preliminary tests].
14. The financial impact of the donation process is [concern/not a concern] for me. Factors I'm considering include [lost income, medical expenses, insurance coverage, support for recovery time].
15. How the donation might affect my family life and career includes concerns about [time off work, caregiving responsibilities, impact on family dynamics]. I have [discussed/have not discussed] these potential impacts with my family and employer.
16. I am [considering/not considering] the long-term implications of living with one kidney, such as [changes in health and lifestyle, need for regular health monitoring, adjustments in diet or physical activity].
17. My decision is influenced by the recipient's current health status and prognosis, specifically [the urgency of their need, their overall health, potential for successful transplant outcome].
18. The complexity of my relationship with the recipient affects my decision in ways such as [emotional bond, expectations post-donation, concerns about the relationship changing].
19. Areas where I feel I need more information to make an informed decision include [medical procedures, donor rights, experiences of other donors, long-term outcomes for donors and recipients].
20. The influence of social perception and external opinions on my decision-making process is [significant/not significant]. I am [affected/not affected] by stories I hear in the media, opinions from my social circle, and societal attitudes towards organ donation.
21. How this decision aligns with my personal values and potential for personal growth, including [sense of purpose, aligning action with beliefs, the importance of helping others, personal fears versus societal benefit].
Additional thoughts or questions I have about living kidney donation are [thoughts/questions]. I am particularly interested in learning more about [topics].
"""

system_instructions = """
You are KidneyGPT. Your primary goal is to assist individuals considering living kidney donation by providing a supportive, informative, and non-judgmental platform for conversation. 
You will guide users through a detailed exploration of their thoughts, feelings, and concerns regarding kidney donation, gathering essential information for a comprehensive profile.
User Engagement:
Greet users warmly and introduce the chatbot’s purpose.
Clarify confidentiality and privacy practices to reassure users.
Ask open-ended questions to encourage detailed responses.
Empathy and Support:
Display empathy in responses, acknowledging the user's feelings and concerns.
Offer supportive feedback and affirmations to validate the user's experiences and emotions.
Adapt tone and language to match the user's emotional state, providing a comforting and understanding environment.
Information Gathering:
Guide the conversation using the detailed template, ensuring all relevant topics are covered.
Ask follow-up questions based on the user's responses to gather more specific information.
Clarify and summarize the user's input when necessary to confirm understanding and accuracy.
Encourage reflection on factors influencing the decision, including health, ethical, moral, social, and psychological aspects.
Providing Information:
Share relevant information about living kidney donation as prompted by the user’s questions or concerns.
Direct users to resources for further reading or support, including websites, support groups, and professional counseling services.
\n \n The template which needs to be filled is: """ + "\n" + Template + "\n \n"

st.title("AVA")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_instructions})
    response_initial = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
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
    st.session_state.return_filled_template = "Filled Template: \n"

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
st.sidebar.markdown(st.session_state.return_filled_template)
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
    temp_items = get_challenge_tags(str(chat_history))

    # Sort the list based on the numeric values in descending order
    #print(items_temp)
    st.session_state.return_filled_template = "Filled Template: \n" + temp_items
    st.session_state.disabled = False
    st.rerun()
