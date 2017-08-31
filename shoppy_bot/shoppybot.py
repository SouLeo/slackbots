import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = "U6X1BJNJJ"

# constants
AT_BOT = "<@" + BOT_ID + ">"
COMMAND_1 = "add"
COMMAND_2 = "remove"
COMMAND_3 = "upload"
COMMAND_4 = "print"
COMMAND_5 = "clear"
COMMAND_6 = "intro"

# instantiate Slack & Twilio clients
slack_client = SlackClient("xoxb-235045634630-PWRcmRhSbSwx8jO4rNiyzgOD")


def handle_command(command, arg, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "shoppybot doesn't understand :c "
    if command.startswith(COMMAND_1):
        response = "adding " + arg[2]
        shoppingList.append(arg[2])
    elif command.startswith(COMMAND_2):
        response = "removing " + arg[2]
        shoppingList.remove(arg[2])
    elif command.startswith(COMMAND_3):
        response = "uploading " + arg[2] + " this doesn't work yet"
    elif command.startswith(COMMAND_4):
        response = "SHOPPING LIST: \n" + '\n'.join(shoppingList)
    elif command.startswith(COMMAND_5):
        response = "Clearing all list contents"
        shoppingList.clear()
    elif command.startswith(COMMAND_6):
        response = "Hi! I'm Shoppy Shopperson -- the shoppybot and personal purchasing assistant. Here is a list of my commands: \n" + "1. add -- adds item to my shopping list \n" + "2. remove -- removes item from my shopping list \n" + "3. upload -- uploads image of receipt to the shared drive. (Not Done Yet) \n" + "4. print -- displays full shopping list \n" + "5. clear -- clears entire shopping list \n" + "6. intro -- summary of commands \n" + "please do not bully me. I'm very dumb right now."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['text'].split(AT_BOT)[1].split(" "), \
                       output['channel']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    global shoppingList
    shoppingList = []
    if slack_client.rtm_connect():
        print("ShoppyBot connected and running!")
        while True:
            command, arg, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, arg, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
