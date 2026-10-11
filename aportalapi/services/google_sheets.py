import logging
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 15


def _post(payload):
    try:
        response = requests.post(settings.GOOGLE_SHEETS_WEBHOOK_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        if response.json().get('ok') is not True:
            logger.error('Google Sheets webhook rejected signup: %s', response.text[:200])
    except (requests.RequestException, ValueError):
        logger.exception('Google Sheets webhook failed for %s', payload.get('email') or payload.get('first_name'))


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
