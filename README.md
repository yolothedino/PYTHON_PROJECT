# PYTHON_PROJECT
P5 G26 (deadline 23 oct)

**OBJECTIVE**
Implement a chatbot in C that converses in console

## Progression

(according to hints from the proj writeup)

* Make sure you understand the skeleton code
* Implement smalltalk functions - chatbot_is_smalltalk() and chatbot_do_smalltalk()
* Implement hardcoded QnA to test ability to understand and answer questions
* Implement ability to 'insert' knowledge into the database directly, and have the bot adapt
* Upgrade the bot to ask for answers if it don't understand question and then use the answer later
* Add function for bot to reset itself
* Implement loading function, test if bot can properly understand questions/answers from the loaded files
* Implement saving function and test if it saves properly and works with loading

## Chatbox should:

1. Recognize stock (standard) words and phrases, giving pre-defined replies accordingly. For example, saying "hi" to the bot should get the bot to say "hi" back. **At least 5 items of small talk needed**
2. Understand extremely simple English sentences that consists only of 'intent' and 'entity' portions (and in that order). E.g "do joke
3. Be able to 'learn'. When the chatbot is does not know the answer to a user's question, the user may give the bot the answer. The bot will then save this answer and use it as an answer to the same question next time.

Instructions that the chatbot **MUST** be able to understand

* RESET - Erases all of the chatbox knowledge, leaving only the hardcoded smalltalk. Only erases locally within the program, does not actually deletes files
* LOAD <filename> - Loads entities and responses from a filename 
* SAVE <filename> - Save current known entities and responses to a filename. This includes the 'learned' answers from Point 3 of above.
* EXIT - exits

*Instructions that we may ALSO implement*

* JOKE (tells a joke from a list of jokes)
* LAUGH (says hahaha)

Questions and entities that the chatbot MUST be able to understand

* WHERE <noun>
* WHAT <noun>
* WHO <name>

## Chatbot DO NOT HAVE TO

* take in entities/responses that are longer than MAX_ENTITY/MAX_RESPONSE amount of characters
* Account for every single 'where/what/who'. If there is a "Who is Bob" it's not a must for there to be a "What is Bob" and "Where is Bob".
* check for acronyms, sophisticated matching, case-sensitivity, etc. Case insensitive is fine.

## Other important Things

Chatbot's 'knowledge file' to be stored in .ini format or other similar file formats. There's already an initialized INI file inside the repo for your reference
