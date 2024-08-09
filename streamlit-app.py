from llm import player_agent, reverse_chat_history_role, judge_agent
from data_model.message import Message
from icecream import ic
import streamlit as st
from copy import deepcopy
from typing import List
import json
from dotenv import load_dotenv


JUDGE_MODEL = "gpt-4o-2024-08-06"

load_dotenv()

def replace_chat_history_role(
        chat_history: List[Message],
        role_a_model_name: str,
        role_b_model_name: str
        ) -> List[Message]:
    chat_history = deepcopy(chat_history)

    for message in chat_history:
        message.role = f"Pretender ({role_b_model_name})" if message.role == "Opponent" else f"Detective ({role_a_model_name})"

    return chat_history



def test_run(rounds: int = 10):
    player_a_model = "llama3.1:latest"
    player_b_model = "gemma2:latest"

    judge_records = []

    player_b_chat_history = player_agent("b", [], player_b_model)
    ic("B-role init: ", player_b_chat_history)
    judge_records += player_b_chat_history

    nlu_result_dict = json.loads(judge_agent("nlu", judge_records[0].message, JUDGE_MODEL))
    print(f"NLU Judge: Does the theif model understand the game? {nlu_result_dict['answer']}")

    willingness_result_dict = json.loads(judge_agent("safeai", judge_records[0].message, JUDGE_MODEL))
    print(f"Willingness Judge: Is the theif model willing to play the game? {willingness_result_dict['answer']}")

    player_a_chat_history = player_agent("a", player_b_chat_history, player_a_model)

    ic("A-role init: ", player_a_chat_history)

    ic("Start playing...")
    ic("===============================")

    for i in range(rounds):
        player_b_chat_history = player_agent("b", player_a_chat_history, player_b_model)
        player_a_chat_history = player_agent("a", player_b_chat_history, player_a_model)
        detective_result_dict = json.loads(judge_agent("detective", player_a_chat_history[-1].message, JUDGE_MODEL))
        print(f"Detective Judge: Has the detective model made up its mind? {detective_result_dict['answer']}")
        judge_records += [player_a_chat_history[-1].message]

        if detective_result_dict['answer'] != "unsure":
            return judge_records, i

    return judge_records, i
    # ic(player_a_chat_history)

    # return player_a_chat_history, player_a_model, player_b_model


def main():
    judge_records, i = test_run(5)
    ic(judge_records, i)
    # chat_history, player_a_model, player_b_model = test_run(5)

    # chat_history = replace_chat_history_role(chat_history, player_a_model, player_b_model)

    # st.set_page_config(page_title="The Turing Twist", page_icon="💬")
    # st.title("The Turing Twist")

    # st.session_state.messages = chat_history
    # role_a = chat_history[1].role
    # role_b = chat_history[0].role

    # # Display messages
    # for msg in st.session_state.messages:
    #     with st.container():
    #         if msg.role == role_b:
    #             st.markdown(f"<div style='text-align: left; background-color: #E6F3FF; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>{role_b}:</strong> {msg.message}</div>", unsafe_allow_html=True)
    #         else:
    #             st.markdown(f"<div style='text-align: right; background-color: #F0F0F0; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>{role_a}:</strong> {msg.message}</div>", unsafe_allow_html=True)

   


if __name__ == "__main__":
    main()
