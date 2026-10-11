import logging
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 30


def _post(payload):
    try:
        response = requests.post(settings.SIGNUP_EMAIL_WEBHOOK_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        if response.json().get('ok') is not True:
            logger.error('Signup email webhook rejected the list: %s', response.text[:200])
    except (requests.RequestException, ValueError):
        logger.exception('Signup email webhook failed (%s signups)', len(payload['signups']))


def send_signup_list(signups):
    """Email the names and emails on the signup sheet via the Google Apps Script web app.

    Takes the signups before they're deleted, sends in a background thread so clearing
    the sheet isn't delayed, and never raises. Does nothing when there are no signups
    or SIGNUP_EMAIL_WEBHOOK_URL is unset.
    """
    if not (settings.SIGNUP_EMAIL_WEBHOOK_URL and signups):
        return
    payload = {
        'secret': settings.SIGNUP_EMAIL_WEBHOOK_SECRET,
        'signups': [
            {
                'first_name': signup.user.first_name,
                'last_name': signup.user.last_name,
                'email': signup.user.email,
                'marketing_opt_in': signup.user.user_utilities.marketing_opt_in,
            }
            for signup in signups
        ],
    }
    threading.Thread(target=_post, args=(payload,), daemon=True).start()
