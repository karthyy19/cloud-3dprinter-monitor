"""Cognito post-confirmation trigger: emails the admin a link to approve the new user."""
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse

import boto3
from botocore.config import Config

KEY = os.environ["APPROVAL_KEY"].encode()
APPROVE_URL = os.environ["APPROVE_URL"]
TOPIC_ARN = os.environ["TOPIC_ARN"]
LINK_SECONDS = 7 * 24 * 3600

# Cognito waits only 5 seconds for this trigger, so fail fast and let the except below return the event
sns = boto3.client("sns", config=Config(connect_timeout=1, read_timeout=2, retries={"max_attempts": 1}))


def make_token(pool_id, username, email):
    """base64(json).hmac - approve.py checks the signature and the expiry."""
    payload = base64.urlsafe_b64encode(json.dumps({
        "pool": pool_id, "user": username, "email": email, "exp": int(time.time()) + LINK_SECONDS,
    }).encode()).decode()
    return payload + "." + hmac.new(KEY, payload.encode(), hashlib.sha256).hexdigest()


def handler(event, context):
    # Cognito needs the event handed back, and a failed email must not break the user's sign-up
    try:
        if event.get("triggerSource") == "PostConfirmation_ConfirmSignUp":  # not password resets
            email = event["request"]["userAttributes"].get("email", "?")
            link = APPROVE_URL + "?" + urllib.parse.urlencode(
                {"t": make_token(event["userPoolId"], event["userName"], email)})
            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="Dashboard sign-up approval requested",
                Message="%s has registered for the printer dashboard.\n\nTo review and approve:\n%s\n\n"
                        "The link works for 7 days. Ignore this email to leave them without access."
                        % (email, link),
            )
    except Exception as exc:
        print("notify failed: %r" % exc, flush=True)
    return event
