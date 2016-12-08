# alfred-workflow-google-translate

Translate from/to your favourite language using Google Translate.

To set up, you will need your own Google API key. Go here for instructions: https://cloud.google.com/translate/docs/getting-started#set_up_your_project

The workflow will prompt you the first you run it to enter your API key. Should you need to re-enter it, run "tr-setkey".

To set a target language (one you will translate to), run "tr-setlang". You won't need to set a source (from) language, as Google is pretty good at guessing.

* Simple - setup once and just use it.
* Secure - keys are stored in Mac's native Keychain tool.
* Fast - all queries are cached for speed.
