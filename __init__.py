#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import re
import random
from collections import OrderedDict
import configobj
from datetime import datetime

from models import *

__plugin_name__ = "f12019"
__plugin_link__ = "https://www.f1calendar.com/#!/timezone/Australia-Sydney"
__plugin_color__ = "#33ccff"
__requires_slackbot_version__ = 161110

# a dictionary where the keys are the commands and values are explainations of the bot's responses
commands_info = OrderedDict()
commands_info["!next"] = "bot will reply with the next race"

admin_commands_info = OrderedDict()
admin_commands_info["!all"] = "display all the races in the database"

def command_next(user, chat_string, channel, teamid):
    # respond with a random item from our greeting messages from the database
    race = Season2019.select().where(Season2019.datetime >= datetime.date.today()).order_by(Season2019.datetime).limit(1).get()
    outputs.append([channel, "{}, {} - {}".format(race.name, race.city, race.datetime.strftime("%d %B, %H:%M"))])

def command_all(user, chat_string, channel, teamid):
    for race in Season2019.select():
        outputs.append([channel, "{}, {} - {}".format(race.name, race.city, race.datetime.strftime("%d %B, %H:%M"))])

"""
    EVERYTHING BELOW HERE IS BOILER PLATE PLUGIN CODE
"""

__plugin_version__ = 161110

crontable = []
outputs = []
attachments = []
typing_sleep = 0

directory = os.path.dirname(sys.argv[0])
if not directory.startswith('/'):
    directory = os.path.abspath("{}/{}".format(os.getcwd(), directory))

cfgfile = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "plugins", __plugin_name__, "config.ini")
if not os.path.isfile(cfgfile):
    config = configobj.ConfigObj()
    config.filename = cfgfile

    config['owner'] = ""
    config['admin_list'] = ""
    config.write()

def process_cmd(cmd, user, chat_string, channel, teamid):
    pattern_cmd = re.compile("^%s" % cmd)
    if pattern_cmd.match(chat_string.lower()):
        command = "command_%s" % cmd.replace('!', '').replace(' ', '_')
        #try:
        logging.info("Processing command: {}".format(command))
        chat_string = re.sub("^%s" % cmd, '', chat_string, flags=re.IGNORECASE)
        globals()[command](user, chat_string.lstrip(' '), channel, teamid)
        #except Exception as e:
        #    logging.error("Something failed when firing the command {}".format(command))
        #    logging.error(e)
        #    logging.debug(chat_string)

        return True
    else:
        return False

def prep_data(data):
    """ accepts in a slack data dictionary and grabs out the things we need
    """

    status = True
    try:
        config = configobj.ConfigObj(cfgfile)
    except (IOError, KeyError, AttributeError) as e:
        print("Failed to read config file.")
        status = False

    try:
        user = data['user']
    except:
        logging.error("Could not grab username")
        logging.debug(data)
        status = False

    try:
        if "subtype" in data:
            if data['subtype'] == "message_changed":
                chat_string = data['message']['text']
            else:
                chat_string = data['text']
        else:
            chat_string = data['text']

    except:
        logging.debug("Error: didn't find a usable line of chat in the data")
        logging.debug(data)
        status = False

    try:
        channel = data['channel']
    except:
        logging.error("Could not grab channel")
        logging.debug(data)
        status = False

    try:
        teamid = data['team']
    except:
        logging.error("Could not grab teamid")
        logging.debug(data)
        status = False

    if status:
        return config, user, chat_string, channel, teamid
    else:
        return False, False, False, False, False


def process_message(data):
    """ this function processes each line of chat seen by the bot
        if a chat line matches a command, the appropriate function is called
    """

    config, user, chat_string, channel, teamid = prep_data(data)

    if config:
        if user in config['admin_list'] or user in config['owner']:
            for cmd in admin_commands_info.keys():
                if process_cmd(cmd.replace("{} ".format(__plugin_name__), ''), user, chat_string, channel, teamid):
                    return True

        for cmd in commands_info.keys():
            if process_cmd(cmd, user, chat_string, channel, teamid):
                return True

        return False
    else:
        return False


def process_help(data):
    """ sends back an attachment which displays this plugins commands
        if the user is an admin, also includes admin commands
    """

    config, user, chat_string, channel, teamid = prep_data(data)

    print("{} wants help".format(user))

    help_attachments = []

    if config:

        if len(commands_info) > 0:
            commands_list = []
            responses_list = []
            fallback_list = ["{} Plugin Features:".format(__plugin_name__.capitalize())]

            if (sys.version_info > (3, 0)):
                for k, v in commands_info.items():
                    commands_list.append("`{}`".format(k))
                    responses_list.append(v)
                    fallback_list.append("`{}`: {}".format(k, v))
            else:
                for k, v in commands_info.iteritems():
                    commands_list.append("`{}`".format(k))
                    responses_list.append(v)
                    fallback_list.append("`{}`: {}".format(k, v))
            commands = "\n".join(commands_list)
            responses = "\n".join(responses_list)
            fallback = "\n".join(fallback_list)
            attachment = [{
                "title": "{} Plugin Features".format(__plugin_name__.capitalize()),
                "title_link": "{}".format(__plugin_link__),
                "color": __plugin_color__,
                "fallback": fallback,
                "fields": [
                    {"title": "Command", "value": commands, "short": True},
                    {"title": "Response", "value": responses, "short": True}
                ],
                "mrkdwn_in": ["fields"]
            }]

            help_attachments.append([data['channel'], "{} commands:".format(__plugin_name__), attachment])

        if (user in config['admin_list'] or user in config['owner']) and len(admin_commands_info) > 0:
            commands_list = []
            responses_list = []
            fallback_list = ["Admin Commands:"]

            if (sys.version_info > (3, 0)):
                for k, v in admin_commands_info.items():
                    commands_list.append("`{}`".format(k))
                    responses_list.append(v)
                    fallback_list.append("`{}`: {}".format(k, v))
            else:
                for k, v in admin_commands_info.iteritems():
                    commands_list.append("`{}`".format(k))
                    responses_list.append(v)
                    fallback_list.append("`{}`: {}".format(k, v))
            commands = "\n".join(commands_list)
            responses = "\n".join(responses_list)
            fallback = "\n".join(fallback_list)
            attachment = [{
                "color": __plugin_color__,
                "fallback": fallback,
                "fields": [
                    {"title": "Admin Command", "value": commands, "short": True},
                    {"title": "Response", "value": responses, "short": True}
                ],
                "mrkdwn_in": ["fields"]
            }]

            help_attachments.append([data['channel'], "{} admin commands:".format(__plugin_name__), attachment])

        attachments.extend(help_attachments)
