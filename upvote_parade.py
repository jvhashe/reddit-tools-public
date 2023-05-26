import getpass
import praw
import random
import sys
import time

from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment

_DEFAULT_SUB_FILE = './submissions.txt'

_possible_comments = ['Upvoted', 'Upvoted!', 'updooted', 'got you', 'have an upvote', 'take some karma']

_submissions_seen = set()


def write_submission_file(file_name: str):
    with open(file_name, 'w') as file:
        for sub_id in _submissions_seen:
            file.write(sub_id)
            file.write('\n')


def read_submission_file(file_name: str):
    with open(file_name, 'r') as file:
        for line in file:
            _submissions_seen.add(line.strip())


if __name__ == '__main__':
    passw = getpass.getpass()

    reddit = praw.Reddit(client_id='CLIENT_ID_HERE',
                         client_secret='CLIENT_SECRET_HERE',
                         password=passw,
                         user_agent='PUT_WHATEVER_YOU_WANT',
                         username='USER_NAME_HERE')

    read_submission_file(_DEFAULT_SUB_FILE)

    submission: Submission
    for submission in reddit.subreddit('FreeKarma4U').hot(limit=20):
        print('Title: ', submission.title, 'Sub ID: ', submission.id)
        if submission.stickied:
            print('Submission is stickied, skipping...\n')
            continue
        if submission.id in _submissions_seen:
            print('Submission already seen, skipping...\n')
            continue
        _submissions_seen.add(submission.id)
        write_submission_file(_DEFAULT_SUB_FILE)
        submission.upvote()

        comment: Comment
        for comment in submission.comments:
            if comment.author != reddit.user:
                try:
                    comment.upvote()
                    comment.reply(random.choice(_possible_comments))
                except:
                    print('Error upvoting comment.', file=sys.stderr)
            time.sleep(random.randint(15, 30))

