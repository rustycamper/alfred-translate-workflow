#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from workflow import Workflow, ICON_WARNING
import argparse
from collections import OrderedDict

from base_translate import GOOGL_API, MSFT_API
from google_translate import PROPS as GOOGLE_PROPS, GoogleTranslate
from msft_translate import PROPS as MSFT_PROPS, MicrosoftTranslate

ICON_PATH = 'icons'


class BaseLanguage(object):
    def __init__(self, wf):
        self._wf = wf
        self._languages = None
        self._target_lang_code = None
        self._prop_target_lang = None
        self._default_icon = None

    @property
    def languages(self):
        return OrderedDict(sorted(self._languages.items(), key=lambda t: t[1]))

    @property
    def prop_target_lang(self):
        return self._prop_target_lang

    @property
    def target_lang_code(self):
        return self._wf.settings.get(self.prop_target_lang, None)

    @target_lang_code.setter
    def target_lang_code(self, value):
        self._wf.settings[self.prop_target_lang] = value

    @property
    def target_lang_name(self):
        """Get full target language name.

            Returns:
                Language name.
        """
        return self._languages[self.target_lang_code]

    def get_icon(self, lang_code):
        raise NotImplemented


class GoogleLanguage(BaseLanguage):
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

    def __init__(self, wf):
        super(GoogleLanguage, self).__init__(wf)
        self._prop_target_lang = GOOGLE_PROPS['TARGET_LANG']
        self._languages = self.languages

    def get_icon(self, lang_code):
        return GoogleTranslate.get_icon(lang_code)


class MicrosoftLanguage(BaseLanguage):
    languages = {
        'af': 'Afrikaans',
        'ar': 'Arabic',
        'bs-Latn': 'Bosnian (Latin)',
        'bg': 'Bulgarian',
        'ca': 'Catalan',
        'zh-CHS': 'Chinese Simplified',
        'zh-CHT': 'Chinese Traditional',
        'hr': 'Croatian',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'en': 'English',
        'et': 'Estonian',
        'fi': 'Finnish',
        'fr': 'French',
        'de': 'German',
        'el': 'Greek',
        'ht': 'Haitian Creole',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'mww': 'Hmong Daw',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'sw': 'Kiswahili',
        'tlh': 'Klingon',
        # 'tlh-Qaak': 'Klingon (pIqaD)', # encoding not supported by Alfred
        'ko': 'Korean',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'ms': 'Malay',
        'mt': 'Maltese',
        'no': 'Norwegian',
        'fa': 'Persian',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'otq': 'Queretaro Otomi',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sr-Cyrl': 'Serbian (Cyrillic)',
        'sr-Latn': 'Serbian (Latin)',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'es': 'Spanish',
        'sv': 'Swedish',
        'th': 'Thai',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese',
        'cy': 'Welsh',
        'yua': 'Yucatec Maya',
    }

    def __init__(self, wf):
        super(MicrosoftLanguage, self).__init__(wf)
        self._prop_target_lang = MSFT_PROPS['TARGET_LANG']
        self._languages = self.languages

    def get_icon(self, lang_code):
        return MicrosoftTranslate.get_icon(lang_code)


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    # Target language
    parser.add_argument('--setlang', dest='target_lang', nargs='?',
                        default=None)
    args = parser.parse_args(wf.args)

    api_provider = wf.settings.get('api', None)
    # Make sure user has selected a translation service.
    if not api_provider:
        wf.add_item('No translation service set.',
                    'Type tr-setapi to set a translation service.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    if api_provider == GOOGL_API:
        api = GoogleLanguage(wf)
    elif api_provider == MSFT_API:
        api = MicrosoftLanguage(wf)
    else:
        raise RuntimeError('Unsupported API')

    if args.target_lang:
        api.target_lang_code = args.target_lang
        return 0

    lang = args.query
    hit = False
    pattern = re.compile('^' + lang, re.IGNORECASE)
    for (code, name) in api.languages.items():
        if pattern.match(name):
            wf.add_item(name, code, arg=code, valid=True,
                        icon=api.get_icon(code))
            hit = True
    if not hit:
        wf.add_item(lang, "No matching language found.",
                    icon=ICON_WARNING, valid=False)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
