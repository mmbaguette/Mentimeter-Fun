import requests as rq
import os
import threading
from menti import *

menti_ID = input("Please enter your menti presentation ID: ")

post_word_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " 
    + "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
post_word_data = {
    "question_type": "wordcloud"
}

class UnauthorizedError(Exception):
    pass

def divide_chunks(l, n):
    for i in range(0, len(l), n):
	    yield l[i:i + n]

def send_word_cloud(word_list: list, identifier: str, public_key: str):    
    if word_list == "":
        print("Your word list is empty!")
        return
    post_word_headers["x-identifier"] = identifier
    vote_str = " ".join([word.replace(" ","_") for word in word_list])
    post_word_data["vote"] = vote_str
    post_word_URL = f"https://www.menti.com/core/votes/{public_key}"
    post_word_request = rq.post(post_word_URL, headers=post_word_headers, data=post_word_data)
    
    if post_word_request.status_code == 200:
        return #  Success!
    elif post_word_request.status_code == 401:
        print("\nRequest URL:", post_word_URL)
        print("Status code:", post_word_request.status_code)
        print("Response body:", post_word_request.text)
        raise(UnauthorizedError("Invalid identifier header!"))
    elif post_word_request.status_code != 400: # 400 duplicate identifer header
        print("\nRequest URL:", post_word_URL)
        print("Status code:", post_word_request.status_code)
        print("Response body:", post_word_request.text)
        raise(Exception("We couldn't post these words to this menti!"))

def spam_word_cloud(word_list: list, public_key: str, max_words: int = 3):
    while True:
        for word_list in divide_chunks(word_list, max_words):
            identifier = get_identifier()
            send_word_cloud(word_list, identifier, public_key)

def main():
    menti_info = get_menti_info(menti_ID) # We only need to get it once
    menti_questions = menti_info["questions"]
    public_key = menti_info["pace"]["active"] # Every question has a unique key. this one is the active question's key.
    max_words = int(find_question(menti_questions, public_key)["max_nb_words"]) 
    my_word_list = ["hi", "hello"] # List of words to post in menti (will cut to max number of words)
    spamming = True

    if spamming:
        for _ in range(os.cpu_count()):
            thread = threading.Thread(target=spam_word_cloud,args=(my_word_list, public_key, max_words,))
            thread.start()
    else:
        identifier = get_identifier()
        send_word_cloud(my_word_list, identifier, public_key)

if __name__=='__main__':
    main()
