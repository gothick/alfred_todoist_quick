#!/usr/bin/env python

# A quickly bodged-together Python script that will use Todoist's "quick add"
# API method to add a new task (optionally to a specific project.) 
#
# Works on macOS Sierra without any additional stuff installed, using 
# the default Python 2.7 installation. This makes it easy to install and
# use with an Alfred app workflow.
#
# All criticism welcome, but please bear in mind that this is my first Python
# script :D

import httplib, urllib, sys, argparse, json

parser = argparse.ArgumentParser(usage = "todoistquickadd [-t token] [-p project] task")
parser.add_argument("-t", "--token", required = True)
parser.add_argument("-p", "--project", help = "Target project")
parser.add_argument("task")
args = parser.parse_args()

token = args.token
project = args.project
task = args.task

# Todoist's "quick add" API uses the same syntax as Quick Add in the 
# apps/web version: 
# https://support.todoist.com/hc/en-us/articles/115001745265-Task-Quick-Add
# ...so we can just tag #ProjectName on to the task string to add it 
# to the "Project Name" project.
if project:
    task = task + " #" + project

params = urllib.urlencode({'text': task, 'token': token})
headers = {"Content-type": "application/x-www-form-urlencoded"}

try:
    conn = httplib.HTTPSConnection("todoist.com")
    try:
        conn.request("POST", "/API/v7/quick/add", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("Got non-successful response code from Todoist: " + str(response.status))
        result = json.load(response)
        print "Successfully added item " + result['content'] + ((" to " + project) if project else "")
        
    finally:
        conn.close()

except Exception as e:
    print("Something terrible happened: " + str(e))
    sys.exit("Unable to add task: " + str(e))
