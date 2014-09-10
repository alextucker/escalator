Escalator
=========

Escalator is a system for quickly starting conference calls. It was built with the
intention of being used as an incident reponse tool, but could be used for
any scenario where you need to start a conference call quickly.

Before you start
----------------

## Twilio

You will need a Twilio account with some credit in it. Please be aware that every minute of every user connected to a confernce will be billed to your Twilio account.

## Google oAuth 2.0

Today the only login mechanism into Escalator is Google.

## Email Backend

Escalator sends invite emails using Django `send_mail`. Make sure to configure an email backend.

Required Environment Variables
------------------------------

`ESCALATOR_BASE_URL` - The base URL of your Escalator instance. This is required for letting
Twilio know what routes to hit.

`ESCALATOR_TWILIO_SID` - A Twilio SID

`ESCALATOR_TWILIO_TOKEN` - A Twilio Secret

`ESCALATOR_TWILIO_OUTGOING` - A Twilio Provisioned Phone Number or Verified 
Outgoing Number

`ESCALATOR_GOOGLE_OAUTH2_KEY` - Google API ClientID

`ESCALATOR_GOOGLE_OAUTH2_SECRET` - Google API Secret


Local Development
-----------------

Since Escalator uses Twilio, your local development machine will need to be uniquely reachable on the internet. The best way to do this is via Ngrok.


Deploying with Heroku
---------------------

Coming soon


TODO
----

1. Add more login options and make logins configurable.
2. Improve Django tests
3. Add JS tests
