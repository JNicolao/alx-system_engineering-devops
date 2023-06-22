#!/usr/bin/python3
""" This script contains function that queries the Reddit API,
    parses the title of all hot articles, and prints a sorted count
    of given keywords.

    Globals:
        @posts: the list of a hot posts from a given subreddit
        @after: the link that keeps track of a pagination
"""
from requests import get
from sys import argv

posts = []
after = None


def print_counts(posts, word_list):
    """ Prints a sorted count of given keywords (case-insensitive)

        Args:
            @posts: list of a hottest posts
            @word_list: a list of keywords to print

        Globals:
            @posts: the list of a hot posts from a given subreddit
            @after: the link that keeps track of a pagination
    """
    results = {}
    for word in word_list:
        results[word.lower()] = 0

    for title in posts:
        words = title.split(" ")
        for word in words:
            if results.get(word) is not None:
                results[word] += 1

    keywords = sorted(results, key=results.get, reverse=True)
    for kword in keywords:
        if results.get(kword):
            for word in word_list:
                if kword == word.lower():
                    print("{}: {}".format(word, results[kword]))


def count_words(subreddit, word_list):
    """ Queries the Reddit API, parses the title of all hot articles,
        prints a sorted count of given keywords (case-insensitive,
        delimited by spaces. E.g., JavaScript should count as javascript,
        but java should not).

        Args:
            @subreddit: a subreddit to retrieve
            @word_list: a list of keywords to search
    """
    global posts
    global after

    headers = {"User-Agent": "0x16. API advanced"}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    if after:
        url = url + "?after={}".format(after)

    count = get(url, headers=headers).json().get("data")

    for post in count.get("children"):
        posts.append(post.get("data").get("title").lower())

    after = count.get("after")
    if after is not None:
        return count_words(subreddit, word_list)

    return print_counts(posts, word_list)


if __name__ == "__main__":
    count_words(argv[1], argv[2].split(" "))