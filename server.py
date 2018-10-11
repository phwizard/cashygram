from flask import Flask, Response, request, redirect
from twilio.jwt.client import ClientCapabilityToken
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/token', methods=['GET'])
def get_capability_token():
    """Respond to incoming requests."""

    # Find these values at twilio.com/console
    account_sid = '<Twilio sid>'
    auth_token = '<Twilio auth token>'

    capability = ClientCapabilityToken(account_sid, auth_token)

    # Twilio Application Sid
    application_sid = '<TwilioML app sid>'
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming('joey')
    token = capability.generate()

    return Response(token, mimetype='application/jwt')


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message

    if "Respond with the following code to confirm your transaction: " in body:
      body_split = body.split("Respond with the following code to confirm your transaction: ")
      # print body_split[1]
      resp.message(body_split[1])
    #elif resp.message("")

    #if body == 'hello':
    #    resp.message("Hi!")
    #elif body == 'bye':
    #    resp.message("Goodbye")

    if str(resp):
     return str(resp)
    else:
     return ""

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host = '188.166.146.169',port=5005)