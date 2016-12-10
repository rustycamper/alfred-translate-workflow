#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from urllib2 import quote, HTTPError
from hashlib import sha224

from workflow import web, PasswordNotFound, KeychainError

MAX_AGE_CACHE = 60*60*24  # in sec.
API_URL = 'https://translation.googleapis.com/language/translate/v2'
QUICK_LOOK_URL = 'https://translate.google.com/'
ICON_PATH = 'icons'
PROPS = {
    'API_KEY': 'google_translate_api_key',
    'TARGET_LANG': 'google_target_lang',
}
DEFAULT_ICON = 'google-tr-icon.png'


class GoogleTranslate(object):
    def __init__(self, wf, query=None, source_lang='#auto'):
        self.wf = wf
        self._query = query
        self._source_lang = source_lang

    def __get_translations(self):
        """ Get translation from Google Translate API.

        Returns:
             A list of translation dictionaries.

        Google Translate URL and arguments:
            https://translation.googleapis.com/language/translate/v2?
                key=API_KEY (required)
                &source=<SOURCE_LANG> (optional)
                &target=<TARGET_LANG> (required)
                &q=<QUERY> (required)
        """

        params = dict(key=self.api_key, target=self.target_lang, q=self.query)
        r = web.get(API_URL, params)
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.code == 400:
                raise RuntimeError('Please make sure that your Google '
                                   'API key is correct  /code 400: invalid request/.')
            else:
                raise e

        # Parse the JSON returned and extract the translations.
        result = r.json()
        translations = result['data']['translations']
        return translations

    @property
    def api_key(self):
        try:
            __api_key = self.wf.get_password(PROPS['API_KEY'])
            return __api_key
        except PasswordNotFound as e:
            raise e

    @api_key.setter
    def api_key(self, value):
        try:
            self.wf.save_password(PROPS['API_KEY'], value)
        except KeychainError as e:
            raise e

    @property
    def target_lang(self):
        return self.wf.settings.get(PROPS['TARGET_LANG'], None)

    @target_lang.setter
    def target_lang(self, value):
        self.wf.settings[PROPS['TARGET_LANG']] = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value

    @property
    def source_lang(self):
        return self._source_lang

    @source_lang.setter
    def source_lang(self, value):
        self._source_lang = value

    def get_translations(self):
        cache_key = sha224((self.target_lang + self.query)
                           .encode('utf-8')).hexdigest()
        # Get from cache translations newer than MAX_AGE_CACHE
        translations = self.wf.cached_data(cache_key,
                                           self.__get_translations,
                                           max_age=MAX_AGE_CACHE)

        trans = []
        for tr in translations:
            trans.append({
                'title': tr['translatedText'],
                'subtitle': self.query + ' [google]',
                'valid': True,
                'arg': tr['translatedText'],
                'copytext': tr['translatedText'],
                'largetext': tr['translatedText'],
                'quicklookurl': QUICK_LOOK_URL + self.source_lang
                                + '/' + self.target_lang + '/'
                                + quote(self.query.encode('utf-8')),
                'icon': GoogleTranslate.get_icon(self.target_lang)})
        return trans

    @staticmethod
    def get_icon(lang_code=None):
        """Get language icon.

            Arguments:
                lang_code: language code

            Returns:
                Language icon if it exists, else default icon.
        """
        default_icon = os.path.join(ICON_PATH, DEFAULT_ICON)
        if not lang_code:
            return default_icon

        icon_file = os.path.join(ICON_PATH, lang_code + '.png')
        if os.path.exists(icon_file):
            return icon_file
        else:
            return default_icon
