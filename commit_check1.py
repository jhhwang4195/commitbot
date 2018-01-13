# -*- coding: utf-8 -*-
#!/usr/bin/python
from slacker import Slacker
from datetime import datetime
import github3
import pytz
import os

local_tz = pytz.timezone('Asia/Seoul')

token = ""
try:
    token = os.environ['SLACK_BOT_TOKEN']
except Exception as err:
    print ("[Error] %s" % (str(err)))

slack = Slacker(token)
channels = ['#dailycommit']


def post_to_channel(message):
    slack.chat.post_message(channels[0], message)


def get_repo_last_commit_delta_time(owner, repo):
    repo = github3.repository(owner, repo)
    return repo.pushed_at.astimezone(local_tz)


def get_delta_time(last_commit):
    now = datetime.now(local_tz)
    last_push_date = datetime(last_commit.year, last_commit.month, last_commit.day)
    cur_date = datetime(now.year, now.month, now.day)
    delta = cur_date - last_push_date
    return delta.days


def main():
    members = (
        ('jhhwang4195', 'TIL', 'jhhwang'),
        ('hwauni', 'MachineLearning', 'sylee'),
    )
    reports = []

    for owner, repo, name in members:
        last_commit = get_repo_last_commit_delta_time(owner, repo)
        delta_time = get_delta_time(last_commit)

        if(delta_time == 0):
            reports.append('*%s* commited today.' % (name))
        else:
            reports.append('*%s* has not committed for *%s* days.' % (name, delta_time))

    print('\n A bot that checks daily commits.\n' + '\n'.join(reports))
    post_to_channel('\n A bot that checks daily commits.\n' + '\n'.join(reports))


if __name__ == '__main__':
    main()
