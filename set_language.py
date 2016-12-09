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
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'co': 'Corsican',
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
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
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
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
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
            Path to language flag (icon) if it exists.
            If not, Google Translate icon.
    """
    icon_file = os.path.join('icons', lang_code + '.png')
    if not os.path.exists(icon_file):
        icon_file = os.path.join('icons', 'google-tr-icon.png')
    return icon_file


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    # add a target language
    parser.add_argument('--setlang', dest='target_lang', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    if args.target_lang:
        log.debug("+++++++ Setting target_lang to: " + args.target_lang)
        wf.settings['googl_target_lang'] = args.target_lang
        return 0

    lang = args.query
    hit = False
    pattern = re.compile('^' + lang, re.IGNORECASE)
    for (code, name) in sorted_languages.items():
        if pattern.match(name):
            wf.add_item(name, code, arg=code, valid=True, icon=get_icon(code))
            hit = True
    if not hit:
        wf.add_item(lang, "No matching language found.", icon=ICON_WARNING, valid=False)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
