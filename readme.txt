08.01.2019

Second iteration of the bootstrap for one of our client.

First iteration is a uber simple push to talk todolist creator, on top of a regular talkie walkie like app. We also added another A to our name (don't ask. It sounds cooler.)

Kraaft use the following components :
1. Zello for the talkie walkie part
2. Homemade component to get all zello files in a neatly organized folder in .RAW
3. Google speech API to transform that to text
4. Simple decision-based tree to parse for keyword (if keyword then todo, else nope)
5. Wunderlist to recieve the filtered to do messages, and add the .MP3 of the todo to the card

Cheers !

-----------------------
19.11.2018

Very first bootstrap to test Kraft, our voice-enabled Slack for factories.

Kraft use the following components :
1. Zello (https://zello.com/) for voice, push-to-talk and user interface
2. Homemade component to get all zello files in a neatly organized folder
3. Google speech (https://cloud.google.com/speech-to-text/) API to transform that to text
4. Simple decision-based tree to choose what to do with the message
5. Custom code to push the result of that decision tree back to the user

Cheers !

Kraft team
