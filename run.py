from pprint import pprint

import eliza
from utils import kill_container, recognize_emotion, start_docker_container

eliza = eliza.Eliza()
eliza.load("doctor.txt")
container_erc = start_docker_container("tae898/emoberta-large", 10006)

print("type bye to exit.\n")
dialog = []

bot_utterance = eliza.initial()
bot_emotion = recognize_emotion(bot_utterance)
bot_utterance = f"Bot: ({bot_emotion}) {bot_utterance}"
dialog.append(bot_utterance)

print(bot_utterance)

while True:
    my_utterance = input("> ")
    bot_utterance = eliza.respond(my_utterance)

    my_emotion = recognize_emotion(my_utterance)
    my_utterance = f"You: ({my_emotion}) {my_utterance}"
    dialog.append(my_utterance)

    print(my_utterance)
    if bot_utterance is None:
        break

    bot_emotion = recognize_emotion(bot_utterance)
    bot_utterance = f"Bot: ({bot_emotion}) {bot_utterance}"
    dialog.append(bot_utterance)
    print(bot_utterance)

bot_utterance = eliza.final()
bot_emotion = recognize_emotion(bot_utterance)
bot_utterance = f"Bot: ({bot_emotion}) {bot_utterance}"
dialog.append(bot_utterance)
print(bot_utterance)

pprint(dialog)
with open("dialog.txt", "w") as stream:
    for utterance in dialog:
        stream.write(utterance + "\n")

kill_container(container_erc)
