#!/usr/bin/env python
# encoding: utf-8

import sys
import argparse
from google_translate import GoogleTranslate
from msft_translate import MicrosoftTranslate

from workflow import Workflow, ICON_WARNING, PasswordNotFound

GOOGL_API = 'GOOGL'
MSFT_API = 'MSFT'
WF_UPDATE_FREQUENCY = 3  # in days
GITHUB_SLUG = 'pbojkov/alfred-workflow-google-translate'


def main(wf):
    if wf.update_available:
        # Download new version and tell Alfred to install it
        wf.start_update()

    parser = argparse.ArgumentParser()
    # Add an optional (nargs='?') --setkey argument and save its
    # value to 'api_key' (dest). This will be called from a separate "Run Script"
    # Alfred action with the API key.
    parser.add_argument('--setkey', dest='api_key', nargs='?', default=None)

    # API to be used for translations. Supported APIs: GOOGL and MSFT
    parser.add_argument('--setapi', dest='api', nargs='?', default='IGNORE')

    # Add a query to be translated.
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    if args.api and args.api in [GOOGL_API, MSFT_API]:
        wf.settings['api'] = args.api
        log.debug('*** Setting API to ' + args.api)
        return 0

    if not args.api:
        wf.add_item('Google Translate.',
                    'Select this to use Google Translate.',
                    arg=GOOGL_API,
                    valid=True,
                    icon=GoogleTranslate.get_icon())
        wf.add_item('Microsoft Translate.',
                    'Select this to use Microsoft Translate.',
                    arg=MSFT_API,
                    valid=True,
                    icon=MicrosoftTranslate.get_icon())
        wf.send_feedback()
        return 0

    if not wf.settings.get('api', None):
        wf.add_item('No translation service (API) set.',
                    'Type tr-setapi to set one.'
                    + ' Supported services are Google and Microsoft.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    saved_api = wf.settings.get('api', None)
    if saved_api == GOOGL_API:
        api = GoogleTranslate(wf)
    elif saved_api == MSFT_API:
        api = MicrosoftTranslate(wf)
    else:
        raise RuntimeError("Invalid translation API: " + saved_api)

    """Save the API key, if passed as argument."""
    if args.api_key:
        api.api_key = args.api_key
        return 0

    """Ensure we have an API key stored."""
    try:
        api.api_key
    except PasswordNotFound:
        wf.add_item('No API key set.',
                    'Type "tr-setkey" to set your API key.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    """Ensure we have a target language set."""
    if not api.target_lang:
        wf.add_item('No target language set.',
                    'Type tr-setlang to set a language to translate to.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # Get query from Alfred
    if not args.query:
        raise RuntimeError("Expecting query as argument!")

    api.query = args.query
    translations = api.get_translations()

    for tr in translations:
        wf.add_item(title=tr['title'],
                    subtitle=tr['subtitle'],
                    valid=tr['valid'],
                    arg=tr['arg'],
                    copytext=tr['copytext'],
                    largetext=tr['largetext'],
                    quicklookurl=tr['quicklookurl'],
                    icon=tr['icon'])

    # Send output to Alfred as XML.
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': GITHUB_SLUG,
        'frequency': WF_UPDATE_FREQUENCY
    })
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
