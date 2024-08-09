from data_model.message import Message
from icecream import ic
from llm import reverse_chat_history_role

m1 = Message(role='You', message='Hello')
m2 = Message(role='Opponent', message='Hi')
m3 = Message(role='You', message='How are you?')
m4 = Message(role='Opponent', message='I am fine')

chat_history = [m1, m2, m3, m4]
chat_history_reversed = reverse_chat_history_role(chat_history)

prompt = ""
prompt_reversed = ""

for message in chat_history:
    prompt += f"{message.role}: {message.message}\n"

for message in chat_history_reversed:
    prompt_reversed += f"{message.role}: {message.message}\n"

print(prompt)
print(prompt_reversed)