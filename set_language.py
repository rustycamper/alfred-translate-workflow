#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import os
from workflow import Workflow, ICON_WARNING
import argparse
from collections import OrderedDict


# Google's supported language codes and their corresponding names
languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarussian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'pt-BZ': 'Brazilian Portuguese',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Hatian Creole',
    'ha': 'Hausa',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'km': 'Khmer',
    'ko': 'Korean',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mk': 'Macedonian',
    'ms': 'Malay',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mo': 'Moldavian',
    'mn': 'Mongolian',
    'sr-ME': 'Montenegrin',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'nn': 'Norwegian (Nynorsk)',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu',
}
# sort languages by value
sorted_languages = OrderedDict(sorted(languages.items(), key=lambda t: t[1]))


def get_language_name(lang_code):
    """Get full language name.

        Args:
            lang_code: language code

        Returns:
            Language name.
    """
    return languages[lang_code]


def get_icon(lang_code):
    """Get icon with language country flag.

        Args:
            lang_code: language code

        Returns:
            Path to language flag (icon).
    """
    return os.path.join('icons', lang_code + '.png')


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    # add a target language
    parser.add_argument('--setlang', dest='target_lang', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    if args.target_lang:
        log.debug("+++++++ Setting target_lang to: " + args.target_lang)
        wf.settings['target_lang'] = args.target_lang
        return 0

    lang = args.query
    hit = False
    pattern = re.compile('^' + lang, re.IGNORECASE)
    for (code, name) in sorted_languages.items():
        if pattern.match(name):
            wf.add_item(name, code, arg=code, valid=True, icon=get_icon(code))
            log.debug("+++++++ We got ourselves a hit: " + code)
            hit = True
    if not hit:
        wf.add_item(lang, "No matching language found.", icon=ICON_WARNING, valid=False)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
