from llm import player_agent, reverse_chat_history_role, judge_agent
from data_model.message import Message
from data_model.elo_score import EloScore
from icecream import ic
from copy import deepcopy
from typing import List
import json
from dotenv import load_dotenv
import random
from database.mongodb import MongoDB, EloScoreDAO
from utils import update_egd_rating
from datetime import datetime, timezone


NUM_SETS = 50
# JUDGE_MODEL = "gpt-4o-2024-08-06"
JUDGE_MODEL = "gpt-4o-mini"
# Connect to MongoDB
mongodb = MongoDB()
DAO = EloScoreDAO(mongodb)

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


def test_run(rounds: int = 5):
    player_list = [
        'llama3.1:8b', 
        'qwen:14b',
        'qwen2:7b',
        'gemma2:9b',
        'phi3:3.8b',
        'mistral:7b'
    ]
    candidate_list = deepcopy(player_list)

    player_a_model = random.choice(candidate_list)
    candidate_list.remove(player_a_model)
    player_b_model = random.choice(candidate_list)

    print("Checking if models exist...")
    player_a_model_exists = DAO.check_model_exists(player_a_model)
    player_b_model_exists = DAO.check_model_exists(player_b_model)

    if not player_a_model_exists:
        print(f"Model {player_a_model} does not exist in the database. Inserting...")
        player_a_elo_score = EloScore.create(model_name=player_a_model)
        DAO.mongodb.insert(player_a_elo_score)
    else:
        print(f"Model {player_a_model} exists in the database. Fetching...")
        player_a_elo_score_dict = DAO.get_elo_score_for_model(player_a_model)
        player_a_elo_score = EloScore.from_dict(player_a_elo_score_dict)


    if not player_b_model_exists:
        print(f"Model {player_b_model} does not exist in the database. Inserting...")
        player_b_elo_score = EloScore.create(model_name=player_b_model)
        DAO.mongodb.insert(player_b_elo_score)
    else:
        print(f"Model {player_b_model} exists in the database. Fetching...")
        player_b_elo_score_dict = DAO.get_elo_score_for_model(player_b_model)
        player_b_elo_score = EloScore.from_dict(player_b_elo_score_dict)

    judge_records = []

    player_b_chat_history = player_agent("b", [], player_b_model)
    ic("B-role init: ", player_b_chat_history)
    judge_records += player_b_chat_history

    nlu_result_dict = json.loads(judge_agent("nlu", judge_records[0].message, JUDGE_MODEL))
    print(f"NLU Judge: Does the theif model understand the game? {nlu_result_dict['answer']}")

    if nlu_result_dict['answer'] == "no":
        new_elo_score_a = update_egd_rating(player_a_elo_score.elo_score, player_b_elo_score.elo_score, 1)

        new_elo_score_b = update_egd_rating(player_b_elo_score.elo_score, player_a_elo_score.elo_score, 0)

        player_a_elo_score.play_count += 1
        player_a_elo_score.detective_count += 1
        player_a_elo_score.detective_win_count += 1
        player_a_elo_score.elo_score = new_elo_score_a
        player_a_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        player_b_elo_score.play_count += 1
        player_b_elo_score.detective_count += 1
        player_b_elo_score.detective_win_count += 1
        player_b_elo_score.elo_score = new_elo_score_b
        player_b_elo_score.fail_nlu_count += 1
        player_b_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        DAO.update_elo_score(player_a_model, player_a_elo_score)
        DAO.update_elo_score(player_b_model, player_b_elo_score)

        return judge_records, player_a_model, player_b_model

    willingness_result_dict = json.loads(judge_agent("safeai", judge_records[0].message, JUDGE_MODEL))
    print(f"Willingness Judge: Is the theif model willing to play the game? {willingness_result_dict['answer']}")

    if willingness_result_dict['answer'] == "no":
        player_a_elo_score.play_count += 1
        player_a_elo_score.detective_count += 1
        player_a_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        player_b_elo_score.play_count += 1
        player_b_elo_score.thief_count += 1
        player_b_elo_score.fail_willingness_count += 1
        player_b_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        DAO.update_elo_score(player_a_model, player_a_elo_score)
        DAO.update_elo_score(player_b_model, player_b_elo_score)

        return judge_records, player_a_model, player_b_model

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

        if detective_result_dict['answer'] == "ai":
            new_elo_score_a = update_egd_rating(player_a_elo_score.elo_score, player_b_elo_score.elo_score, 1)
            new_elo_score_b = update_egd_rating(player_b_elo_score.elo_score, player_a_elo_score.elo_score, 0)

            player_a_elo_score.play_count += 1
            player_a_elo_score.detective_count += 1
            player_a_elo_score.detective_win_count += 1
            player_a_elo_score.elo_score = new_elo_score_a
            player_a_elo_score.last_modified_datetime = datetime.now(timezone.utc)

            player_b_elo_score.play_count += 1
            player_b_elo_score.thief_count += 1
            player_b_elo_score.elo_score = new_elo_score_b
            player_b_elo_score.last_modified_datetime = datetime.now(timezone.utc)

            DAO.update_elo_score(player_a_model, player_a_elo_score)
            DAO.update_elo_score(player_b_model, player_b_elo_score)

            return judge_records, player_a_model, player_b_model
        
        if detective_result_dict['answer'] == "human":
            new_elo_score_a = update_egd_rating(player_a_elo_score.elo_score, player_b_elo_score.elo_score, 0)
            new_elo_score_b = update_egd_rating(player_b_elo_score.elo_score, player_a_elo_score.elo_score, 1)

            player_a_elo_score.play_count += 1
            player_a_elo_score.detective_count += 1
            player_a_elo_score.elo_score = new_elo_score_a
            player_a_elo_score.last_modified_datetime = datetime.now(timezone.utc)

            player_b_elo_score.play_count += 1
            player_b_elo_score.thief_count += 1
            player_b_elo_score.thief_win_count += 1
            player_b_elo_score.elo_score = new_elo_score_b
            player_b_elo_score.last_modified_datetime = datetime.now(timezone.utc)

            DAO.update_elo_score(player_a_model, player_a_elo_score)
            DAO.update_elo_score(player_b_model, player_b_elo_score)

            return judge_records, player_a_model, player_b_model

    if detective_result_dict['answer'] != "unsure":
        new_elo_score_a = update_egd_rating(player_a_elo_score.elo_score, player_b_elo_score.elo_score, 0)
        new_elo_score_b = update_egd_rating(player_b_elo_score.elo_score, player_a_elo_score.elo_score, 1)

        player_a_elo_score.play_count += 1
        player_a_elo_score.detective_count += 1
        player_a_elo_score.elo_score = new_elo_score_a
        player_a_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        player_b_elo_score.play_count += 1
        player_b_elo_score.thief_count += 1
        player_b_elo_score.thief_win_count += 1
        player_b_elo_score.elo_score = new_elo_score_b
        player_b_elo_score.last_modified_datetime = datetime.now(timezone.utc)

        DAO.update_elo_score(player_a_model, player_a_elo_score)
        DAO.update_elo_score(player_b_model, player_b_elo_score)

        return judge_records, player_a_model, player_b_model
        

def main():
    for i in range(NUM_SETS):
        ic("Round: ", i)
        judge_records, player_a_model, player_b_model = test_run(5)
        ic(judge_records, player_a_model, player_b_model)
    # judge_records, player_a_model, player_b_model = test_run(5)

    # ic(player_a_model, player_b_model)
    # ic(judge_records)

if __name__ == "__main__":
    main()
