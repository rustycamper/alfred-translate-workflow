#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import argparse
import urllib2

from workflow import Workflow, web, ICON_WARNING, PasswordNotFound


def get_translations(api_key, target_lang, query):
    """ Get translation from Google Translate API.

    Args:
        api_key: Google Translate personal API key.
        target_lang: Target language - the language we translate to.
        query: The text we are translating.

    Returns:
         A list of translation dictionaries.

    """
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = dict(key=api_key, target=target_lang, q=query)
    r = web.get(url, params)

    # Throw an error if request failed.
    # Workflow will catch this and show it to the user.
    try:
        r.raise_for_status()
    except urllib2.HTTPError as e:
        if e.code == 400:
            raise RuntimeError('Please make sure that your Google '
                               'API key is correct - invalid request.')
        else:
            raise e

    # Parse the JSON returned and extract the translations.
    result = r.json()
    translations = result['data']['translations']
    return translations


def main(wf):
    import hashlib

    if wf.update_available:
        # Download new version and tell Alfred to install it
        wf.start_update()

    parser = argparse.ArgumentParser()
    # Add an optional (nargs='?') --setkey argument and save its
    # value to 'api_key' (dest). This will be called from a separate "Run Script"
    # Alfred action with the API key.
    parser.add_argument('--setkey', dest='api_key', nargs='?', default=None)

    # Add a query to be translated.
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    """Save the API key, if such."""
    if args.api_key:
        wf.save_password('google_translate_api_key', args.api_key)
        return 0

    """Ensure we have the API key saved to Keychain."""
    try:
        api_key = wf.get_password('google_translate_api_key')
    except PasswordNotFound:
        wf.add_item('No API key set.',
                    'Type "tr-setkey" to set your Google API key.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    """Ensure we have a target language set."""
    target_lang = wf.settings.get('target_lang', None)
    if not target_lang:
        wf.add_item('No target language set.',
                    'Type tr-setlang to set a language to translate to.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # Get query from Alfred
    if not args.query:
        raise RuntimeError("Expecting argument!")
    # Get args from Workflow as normalized Unicode
    query = args.query

    """Google Translate URL and arguments.

    https://translation.googleapis.com/language/translate/v2?key=API_KEY
    &source=<SOURCE_LANG>
    &target=<TARGET_LANG>
    &q=<QUERY>
    """

    def wrapper():
        """`cached_data` can only take a bare callable (no args),
        so we need to wrap callables needing arguments in a function
        that needs none.
        """
        return get_translations(api_key, target_lang, query)

    def get_icon():
        """Get icon for language."""
        return os.path.join('icons', target_lang + '.png')

    cache_key = hashlib.sha224(target_lang+query).hexdigest()
    # Retrieve from cache translations newer than 600 sec, if any.
    translations = wf.cached_data(cache_key, wrapper, max_age=600)

    for tr in translations:
        wf.add_item(title=tr['translatedText'],
                    subtitle=query,
                    valid=True,
                    arg=tr['translatedText'],
                    copytext=tr['translatedText'],
                    largetext=tr['translatedText'],
                    quicklookurl='https://translate.google.com/#auto/'
                                 + target_lang + '/'
                                 + urllib2.quote(query),
                    icon=get_icon())

    # Send output to Alfred as XML.
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'pbojkov/alfred-workflow-google-translate',
        'frequency': 3
    })
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
