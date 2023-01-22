#!/usr/bin/env python
# encoding: utf-8

# A quickly bodged-together Python script that will use Todoist's "quick add"
# API method to add a new task (optionally to a specific project.)
#
# Works on macOS Sierra without any additional stuff installed, using
# the default Python 2.7 installation. This makes it easy to install and
# use with an Alfred app workflow.
#
# All criticism welcome, but please bear in mind that this is my first Python
# script :D

import httplib, urllib, sys, argparse, json, uuid, json

parser = argparse.ArgumentParser(usage = "todoistquickadd [-t token] [-p project] task")
parser.add_argument("-t", "--token", required = True)
parser.add_argument("-p", "--projectid", required = True, help = "Target project ID (you can find this in the URL of the project page.)")
parser.add_argument("task")
args = parser.parse_args()

token = args.token
projectid = args.projectid
task = args.task

params = json.dumps({"content": task, "project_id": projectid })

headers = {
    "Content-type": "application/json",
    "X-Request-Id": str(uuid.uuid4()),
    "Authorization": "Bearer " + token
}

try:
    conn = httplib.HTTPSConnection("api.todoist.com")
    try:
        conn.request("POST", "/rest/v2/tasks", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("Got non-successful response code from Todoist: " + str(response.status))
        result = json.load(response)
        print 'Successfully added item ' + result['content'] + ((" to project ID " + projectid) if projectid else "")

    finally:
        conn.close()

except Exception as e:
    print("Something terrible happened: " + str(e))
    sys.exit("Unable to add task: " + str(e))
