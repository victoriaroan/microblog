import json
import requests

from flask import current_app
from flask_babel import _


def translate(text, src_lang, dest_lang):
    if not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    auth = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    resp = requests.get(
        f'https://api.microsofttranslator.com/v2/Ajax.svc/Translate?text={text}&from={src_lang}&to={dest_lang}',
        headers=auth
    )

    if resp.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(resp.content.decode('utf-8-sig'))
