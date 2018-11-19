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
