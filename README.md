# Facebook-Bot
A bot for Facebook messenger built from the tutorial at: https://www.datacamp.com/community/tutorials/facebook-chatbot-python-deploy

## Technology Used
* Flask
* Gunicorn
* Python Requests library
* ngrok (soon to be replaced with AWS)
* Docker Containers
* NLTP
* SQLalchemy


## Current Thoughts
I like that the random prompts from literature kind of move the conversation along away from the whole "hi", "hi", "hello" cycle that keeps happening on the other method.

There are too many things in the database though (as much as I hate to waste all those hours it took to load it). I think I need a "teacher" mode where I can manually identify intents, correct typos, and ect.

I also think it can be combined with natural (modern) human responses by recording what people type in, but it would need to have some kind of intent or context as well as the responses to try to make it more of a conversation - to keep it on topic as the conversation goes along.

## Future Improvements
Within this database I should have tables for:
- contexts
- intents
- responses
- words/tokens
as well as tables that join these things in many-to-many relationships

I want to be able to analyze a response and put it into the appropriate place(s) in the database whenever anyone interacts with my bot. I should be able to start from one response (a smiley face, or the word 'hi') and then build out a fully conversational model for my bot based on the interactions it has with the outside world.

For "morals" I want to assign a vector to each response (or token? or intent?) as to how "acceptable" it is in a given context...positive or negative... and so from -5 thru 0 thru +5 and then give each interaction a weight that will nudge the scale.

As humans we have weights like "god", "parents", "teachers", "friends", and "enemies" that may get positive or negative nudges for various topics. I want to emulate that system somehow. I want people to have to earn trust in order to influence my bot. Everyone will not be treated equally (well, perhaps at first...)


Sentence builder (probably another module, but this is just some late night notes here, so more structure in the morning, right?)

I want to be able to read and write sentences with some intention or understanding... ie subject verb predicate... to identify who did what to whom and respond correctly in many forms of the sentence.

I want to correctly identify adjectives/adverbs and if they are positive or negative, when they are opposite in meaning (quick/slow, big/small), so there should be some kind of "picker" functions for each part of speech. Initially the sentences may be nonsense, but they shoudl be real sentences (and this also applies to my typing website - which has some primitive forms of it and could benefit from more advanced forms.)

I could totally add chatbots to my websites for Aspiring Writers (a "muse bot", and a good idea for an app as well. Tell it about your story and when you get stuck it will offer suggestions for the next plot twist) and for World Langauge Library as the language pages could benefit from a very controlled bot that can converse with you in the target language to practice your current lessons/progress through the languages. Again, a good place for an app as well as on the web-pages.

And finally, while thinking about my website empire... there are so many topics I could explore as blog posts/pages on my machine learning website. All the notes from the ML conference, and my notebooks from DataCamp and the books I'm reading. Every chapter is worth at least one blog post once it's broken down and reworded.  And if I take the time to get creative on my angle it may even be somehting really compelling in terms of the space online.

I think I need to focus more on this than on the job search for the time being. I do not think my current job hunt is going all that well, lots of bites, but lots of fish I don't want to take home and fry up for dinner if that makes sense.
