#!/usr/bin/env python
# encoding: utf-8
import os
from urllib2 import quote, HTTPError
from hashlib import sha224
from xml.etree import ElementTree

from workflow import web, PasswordNotFound

MAX_AGE_CACHE = 60*60*24  # in sec.
API_URL = 'https://api.microsofttranslator.com/v2/http.svc/Translate'
QUICK_LOOK_URL = 'https://www.bing.com/translator/'
ICON_PATH = 'icons'
TOKEN_URL = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
PROPS = {
    'API_KEY': 'msft_translate_api_key',
    'TOKEN': 'msft_translate_token',
    'TARGET_LANG': 'msft_target_lang',
}
DEFAULT_ICON = 'msft-icon.png'


class MicrosoftTranslate(object):
    def __init__(self, wf, query=None, source_lang=None):
        self.wf = wf
        self._query = query
        self._source_lang = source_lang

    def __get_token(self):
        params = {'Subscription-Key': self.api_key}
        r = web.post(TOKEN_URL, params)
        r.raise_for_status()
        return 'Bearer' + ' ' + r.content

    @property
    def token(self):
        return self.wf.cached_data(PROPS['TOKEN'], self.__get_token,
                                   max_age=60*9)  # token expires in 10 min

    @token.setter
    def token(self, value):
        self.wf.settings[PROPS['TOKEN']] = value

    def __get_translations(self):
        """ Get translation from Microsoft Cognitive Services API.

        Returns:
             A list of translation dictionaries.

        MSFT Translate URL and arguments:
            https://api.microsofttranslator.com/v2/http.svc/Translate?
                appid=Bearer + ' ' + <TOKEN>(required)
                &from=<SOURCE_LANG> (optional)
                &to=<TARGET_LANG> (required)
                &text=<QUERY> (required)
        """

        params = dict(appid=self.token, to=self.target_lang, text=self.query)
        r = web.get(API_URL, params)
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.code == 400:
                raise RuntimeError('Please make sure that your MSFT API'
                                   ' key is correct  /code 400: invalid request/.')
            else:
                raise e

        # Parse the XML and extract the translation.
        result = ElementTree.fromstring(r.text.encode('utf-8'))
        return result.text

    @property
    def api_key(self):
        try:
            api_key = self.wf.get_password(PROPS['API_KEY'])
        except PasswordNotFound as e:
            raise e
        else:
            return api_key

    @api_key.setter
    def api_key(self, value):
        self.wf.save_password(PROPS['API_KEY'], value)

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
        translation = self.wf.cached_data(cache_key, self.__get_translations,
                                          max_age=MAX_AGE_CACHE)

        return [{
            'title': translation,
            'subtitle': self.query + ' [msft]',
            'valid': True,
            'arg': translation,
            'copytext': translation,
            'largetext': translation,
            'quicklookurl': QUICK_LOOK_URL + '?'
                            + 'to=' + self.target_lang
                            + '&text=' + quote(self.query.encode('utf-8')),
            'icon': MicrosoftTranslate.get_icon(self.target_lang)}]

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
