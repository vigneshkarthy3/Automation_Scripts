#If you found module not found error, do the below
#Please install slackclient-1.3.2 by "pip install slackclient==1.3.2"
import os
import time
import re
import sys
import subprocess
from slackclient import SlackClient
# instantiate Slack client

slack_token = ""
sc = SlackClient(slack_token)
#global e='error'
# Color Templates
GENERAL = '#428bca'         # Blue
SUCCESS = '#5cb85c'         # Green
INFO    = '#5bc0de'         # Light blue
WARNING = '#f0ad4e'         # Orange
ERROR   = '#d9534f'         # Red

# user_id constants
bot_id = ""
bot_name = "<@" + bot_id + ">"
message = None
help_message = """
Hey how are you this is a slack bot talking to you!
    """
def post_message(text_msg):
    sc.api_call(
            'chat.postMessage',
            channel=channel,
            text=text_msg,
            as_user='true:'
            )
def post_attachments(text):
    sc.api_call(
            'chat.postMessage',
            channel=channel,
            attachments=text,
            as_user='true:'
            )
def format_text_color(txt_msg,col):
    print(txt_msg)
    attachments_json = [
{
    "color": col,
    "attachment_type": "default",
    "text": txt_msg
}
]
    return attachments_json

def display_msg():
    value = """
    Anything to showcase when you call your bot
    """
    text="{}".format(value)
    post_message(text)
    return value

def error1_handle():
    error_message = format_text_color("Hey! you got some error", ERROR)
    post_attachments(error_message)

def handle_script(text):
    try:
        message = "Processing the request .... Please wait"
        wait_message = format_text_color(message, SUCCESS)
        post_attachments(wait_message)
        parse_output=text.split()
        args=['/bin/sh','run_some_script.sh'] ## You can run a script to process based on the request
        total=len(parse_output)
        for line in parse_output[2:]:
            args.append(line)
        if total <= 3:
             parse_output=help_message
             msg="You missed something"
             text=format_text_color(msg, ERROR)
             post_attachments(text)
        else:
            parse_output=text.split()
            if total > 3 and len(parse_output[2]) < 10:
                output = subprocess.check_output(args, cwd='/home/directory') 
                output1 = output.decode('utf-8')
                final_message = format_text_color(output1, SUCCESS)
                post_attachments(final_message)
            else:
                msg="You missed something"
                text=format_text_color(msg, ERROR)
                post_attachments(text)
    except subprocess.CalledProcessError as e:
        error_message = format_text_color("Seems there's some issue with config, update your config", ERROR)
        post_attachments(error_message)

def main_command_handle(channel, username, text):
    if 'help' == text.lower():
        text="Hey! this is your help message, how can i help you? ".format(username)
        post_message(text)
        display_msg()
    elif ';' or ',' in text.lower():
        error1_handle()
    elif 'do this' in text.lower():
        handle_script(text)
    else:
        text="provide your github repo readme to help users provide proper data"
        post_message(text)

def parse_output(output_lists):
    if output_lists and len(output_lists) > 0:
        for output in output_lists:
            if output and 'text' in output and bot_name in output['text']:
                print("outputresult",output)
                channel = output['channel']
                text = output['text'].split(bot_name)[1].strip().lower()
                user = output['user']
                if ('subtitle' in output and output.get('type') == 'desktop_notification' ):
                    subtitle = output['subtitle']
                return output.get('channel'),output.get('user'),output.get('text').split(bot_name)[1].strip()
    return None, None, None

if __name__ == "__main__":
    if sc.rtm_connect(with_team_state=False):
        print("Bot is connected and running!")
        while True:
            try:
              events = sc.rtm_read()
              #print("events",events) You will get all the events recorded, you can check this out in a Database
              channel, user, text = parse_output(events)
              #print(channel, user, text)
              #print(user, channel)
              if text and channel and user != "userid":
               userinfo = sc.api_call("users.info", user=user)
               username = userinfo['user']['profile']['real_name_normalized']
               email_id = userinfo['user']['profile']['email']
               main_command_handle(channel,username,text)
               time.sleep(.5)
            except:
              sc.api_call("chat.postMessage", channel=channel,text="Sorry, we encountered some error", as_user=True)
              time.sleep(30)
              sc.rtm_connect()
    else:
        print("Connection failed. Invalid Slack token or Bot ID?")
        sys.exit(255)