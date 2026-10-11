import html
import logging
import re
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 15


def _script_error(page):
    """Pull the readable message out of an Apps Script HTML error page."""
    page = re.sub(r'<(script|style).*?</\1>', ' ', page, flags=re.S)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', page)).split())[:300]


def _post(payload):
    who = payload.get('email') or payload.get('first_name')
    try:
        response = requests.post(settings.GOOGLE_SHEETS_WEBHOOK_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception('Google Sheets webhook failed for %s', who)
        return
    try:
        result = response.json()
    except ValueError:
        # Apps Script answers with an HTML page when the script itself crashes
        logger.error('Google Sheets script error for %s: %s', who, _script_error(response.text))
        return
    if result.get('ok') is not True:
        logger.error('Google Sheets webhook rejected signup for %s: %s', who, result)


def append_signup(user):
    """Add a row for this signup to the Google Sheet.

    Runs in a background thread so a slow Google response never delays the signup,
    and never raises. Does nothing when GOOGLE_SHEETS_WEBHOOK_URL is unset.
    """
    if not settings.GOOGLE_SHEETS_WEBHOOK_URL:
        return
    payload = {
        'secret': settings.GOOGLE_SHEETS_WEBHOOK_SECRET,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'marketing_opt_in': user.user_utilities.marketing_opt_in,
    }
    threading.Thread(target=_post, args=(payload,), daemon=True).start()
