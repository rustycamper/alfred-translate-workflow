#!/usr/bin/env python
# encoding: utf-8
import os
from urllib2 import quote, HTTPError
import hashlib

from workflow import web, PasswordNotFound

MAX_AGE_CACHE = 600  # in sec.
API_URL = 'https://translation.googleapis.com/language/translate/v2'
QUICK_LOOK_URL = 'https://translate.google.com/'
ICON_PATH = 'icons'
PROPS = {
    'API_KEY': 'google_translate_api_key',
    'TARGET_LANG': 'googl_target_lang',
}


class GoogleTranslate:
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

    def set_api_key(self, api_key):
        self.wf.save_password(PROPS['API_KEY'], api_key)

    @property
    def api_key(self):
        try:
            api_key = self.wf.get_password(PROPS['API_KEY'])
        except PasswordNotFound as e:
            raise e
        else:
            return api_key

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

    @property
    def icon(self):
        """Returns language icon."""
        return os.path.join(ICON_PATH, self.target_lang + '.png')

    def get_translations(self):
        cache_key = hashlib.sha224(self.target_lang + self.query).hexdigest()
        # Get from cache translations newer than MAX_AGE_CACHE
        translations = self.wf.cached_data(cache_key, self.__get_translations,
                                           max_age=MAX_AGE_CACHE)

        trans = []
        for tr in translations:
            trans.append({
                'title': tr['translatedText'],
                'subtitle': self.query,
                'valid': True,
                'arg': tr['translatedText'],
                'copytext': tr['translatedText'],
                'largetext': tr['translatedText'],
                'quicklookurl': QUICK_LOOK_URL + self.source_lang
                                + '/' + self.target_lang + '/'
                                + quote(self.query),
                'icon': self.icon})
        return trans
