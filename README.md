# alfred-workflow-google-translate

**Translate from/to your favourite language using Google or Microsoft Translate.**

Usage:
---
* `tr` <query>: translate query.
* `tr-setkey` <API key>: set your API key.
* `tr-setlang` <language>: set target language (language to translate to).


*Note*: You won't need to set a source (from) language. Both Google and Microsoft are pretty good at guessing 
the origin language.

Features:
---
* Simple: setup once and just use it.
* Secure: keys are stored in Mac's native Keychain tool.
* Fast: repeat queries are cached for speed.

Keyboard Shortcuts:
---
* Enter: copy translation to clipboard.
* Command + C: copy translation to clipboard.
* Command + Y: show quick preview on the respective translation web site.
* Command + L: show translated text in large font.

Requirements:
---
The first time you run the workflow, it will prompt you to enter your API key for Google or Microsoft. 
* Instructions on how to get a Google API key: https://cloud.google.com/translate/docs/getting-started#set_up_your_project
* Instructions on how to get a Microsoft API key: https://www.microsoft.com/en-us/translator/getstarted.aspx
