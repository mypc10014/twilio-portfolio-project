# main.py
# Author: [Your Name]
# Personal portfolio project - Twilio API + Flask

import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

app = Flask(__name__)

# Config
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

# Init client
if not ACCOUNT_SID or not AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
    print("WARNING: Twilio env vars not set. SMS will fail.")
    client = None
else:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)


@app.route('/')
def index():
    """Server status check."""
    return jsonify({"status": "running"})

@app.route('/test-sms', methods=['POST'])
def send_test_sms():
    """Endpoint for dev testing."""
    
    if not client:
        return jsonify({"error": "Twilio client not initialized"}), 500

    # Test with my own number from env vars
    MY_TEST_NUMBER = os.environ.get('MY_PERSONAL_PHONE_NUMBER') 

    if not MY_TEST_NUMBER:
        return jsonify({"error": "MY_PERSONAL_PHONE_NUMBER not set"}), 500

    message_body = "Flask test message."

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=MY_TEST_NUMBER
        )
        
        print(f"Message sent: {message.sid}")
        return jsonify({"success": True, "sid": message.sid})

    except TwilioRestException as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Unexpected server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
