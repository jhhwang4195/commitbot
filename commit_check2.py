# -*- coding: utf-8 -*-
#!/usr/bin/python
from slacker import Slacker
from datetime import datetime
import github3
import pytz
import os
import threading
import time
import signal
import sys


def signal_handler(signal, frame):
    print("signal=%s, frame=%s" % (signal, frame))
    time.sleep(1)
    sys.exit(0)


class SlackPost(threading.Thread):
    def __init__(self, token=None, channels=None, repos=None, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)

        self.local_tz = pytz.timezone('Asia/Seoul')
        self.slack = Slacker(token)
        self.channels = channels
        self.repos = repos
        self.signal = True
        return

    def run(self):
        while self.signal:
            time.sleep(1)
            now = datetime.now()
            if now.minute == 0 and now.second == 0:
                self.send_slack_message(self.repos)

    def post_to_channel(self, message):
        self.slack.chat.post_message(self.channels[0], message)

    def get_repo_last_commit_delta_time(self, owner, repo):
        repo = github3.repository(owner, repo)
        return repo.pushed_at.astimezone(self.local_tz)

    def get_delta_time(self, last_commit):
        now = datetime.now(self.local_tz)
        last_push_date = datetime(last_commit.year, last_commit.month, last_commit.day)
        cur_date = datetime(now.year, now.month, now.day)
        delta = cur_date - last_push_date
        return delta.days

    def send_slack_message(self, repos):
        old_name = ""
        reports = []

        for owner, repo, name in repos:
            if old_name != "" and old_name != name:
                reports.append("```")

            if repo is "":
                reports.append("> *%s*" % owner)
                reports.append("```")
                old_name = name
                continue

            last_commit = self.get_repo_last_commit_delta_time(owner, repo)
            delta_time = self.get_delta_time(last_commit)

            if(delta_time == 0):
                reports.append("%s/%s commited today." % (owner, repo))
            else:
                reports.append("%s/%s has not committed for %s days." % (owner, repo, delta_time))

            old_name = name

        reports.append("```")

        title = "\n *A bot that checks daily commits. (%s) *\n" % datetime.now()
        print (title + "\n".join(reports))
        self.post_to_channel(title + "\n".join(reports))


if __name__ == '__main__':
    print("=========================================")
    print("> Type exit or quit to exit.")
    print("=========================================")

    # set signal
    signal.signal(signal.SIGINT, signal_handler)

    # set slack bot token
    token = ""
    try:
        token = os.environ['SLACK_BOT_TOKEN']
    except Exception as err:
        print ("[Error] %s" % (str(err)))

    # set repository
    repos = (
        ('jhhwang4195', '', ''),
        ('jhhwang4195', 'TIL', 'jhhwang'),
        ('jhhwang4195', 'my_source', 'jhhwang'),
        ('jhhwang4195', 'my_config', 'jhhwang'),
        ('jhhwang4195', 'slackbot', 'jhhwang'),
        ('jhhwang4195', 'commitbot', 'jhhwang'),
        ('hwauni', '', ''),
        ('hwauni', 'MachineLearning', 'sylee'),
    )

    # start thread
    t = SlackPost(name="slack_post", token=token, channels=['#dailycommit'], repos=repos)
    t.start()

    while True:
        time.sleep(1)
        in_data = raw_input()
        if in_data == "exit" or in_data == "quit":
            t.signal = False
            signal.alarm(1)
