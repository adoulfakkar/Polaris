#!/usr/bin/python

"""
 This code sample demonstrates an implementation of the Lex Code Hook Interface
 in order to serve a bot which manages dentist appointments.
 Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
 as part of the 'MakeAppointment' template.

 For instructions on how to set up and test this bot, as well as additional samples,
 visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""

import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'ElicitSlot',
			'intentName': intent_name,
			'slots': slots,
			'slotToElicit': slot_to_elicit,
			'message': message,
			'responseCard': response_card
		}
	}


def confirm_intent(session_attributes, intent_name, slots, message, response_card):
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'ConfirmIntent',
			'intentName': intent_name,
			'slots': slots,
			'message': message,
			'responseCard': response_card
		}
	}


def close(session_attributes, fulfillment_state, message):
	response = {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'Close',
			'fulfillmentState': fulfillment_state,
			'message': message
		}
	}

	return response


def delegate(session_attributes, slots):
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'Delegate',
			'slots': slots
		}
	}





""" --- Functions that control the bot's behavior --- """


def get_information(intent_request):
	"""
	Performs dialog management and fulfillment for booking a dentists appointment.

	Beyond fulfillment, the implementation for this intent demonstrates the following:
	1) Use of elicitSlot in slot validation and re-prompting
	2) Use of confirmIntent to support the confirmation of inferred slot values, when confirmation is required
	on the bot model and the inferred slot values fully specify the intent.
	"""
	city = intent_request['currentIntent']['slots']['city']
	phone_number = intent_request['currentIntent']['slots']['PhoneNumber']
	address = intent_request['currentIntent']['slots']['Address']
	email = intent_request['currentIntent']['slots']['Address']
	#email = intent_request['invocationSource']
	output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
	booking_map = json.loads(try_ex(lambda: output_session_attributes['bookingMap']) or '{}')
	data = {}
	data['phone_number'] = phone_number
	data['city'] = city
	data['phone_number'] = phone_number
	data['email'] = email
	json_data = json.dumps(data)

	s3 = boto3.resource('s3')
	s3.Object('Polaris2018', json_data).put(Body=open(json_data, 'rb'))



""" --- Intents --- """


def dispatch(intent_request):
	"""
	Called when the user specifies an intent for this bot.
	"""

	logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

	intent_name = intent_request['currentIntent']['name']

	# Dispatch to your bot's intent handlers
	if intent_name == 'nonProfitPolaris':
		return get_information(intent_request)
	raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
	"""
	Route the incoming request based on intent.
	The JSON body of the request is provided in the event slot.
	"""
	# By default, treat the user request as coming from the America/New_York time zone.
	print(event)
	os.environ['TZ'] = 'America/New_York'
	time.tzset()
	logger.debug('event.bot.name={}'.format(event['bot']['name']))

	return dispatch(event)

