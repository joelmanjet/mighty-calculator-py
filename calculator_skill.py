# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import calculator as calc

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
continue_msg = ". Do you want to calculate another equation?"


def extract_numbers(handler_input):
    first_number = ask_utils.get_slot_value(handler_input, "firstNumber")
    first_decimal = ask_utils.get_slot_value(handler_input, "firstDecimal")
    second_number = ask_utils.get_slot_value(handler_input, "secondNumber")
    second_decimal = ask_utils.get_slot_value(handler_input, "secondDecimal")

    a = f"{first_number}"
    b = f"{second_number}"

    if first_decimal != None:
        a = f"{first_number}.{first_decimal}"
    if second_decimal != None:
        b = f"{second_number}.{second_decimal}"

    number_dict = {
        "n1": a,
        "n2": b
    }

    return number_dict


def speakable(x):
    y = round(x, 1)
    z = int(y)
    if y == z:
        return z
    else:
        return y



class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sound_effect = '<audio src="soundbank://soundlibrary/musical/amzn_sfx_trumpet_bugle_03"/>'
        speak_output = f"{sound_effect} Welcome to the Mighty Calculator. You can say, add 2 and 4.7, or multiply 4 and 8, for a more information say help, to exit say stop."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .set_should_end_session(False)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can perform addition, subtraction, multiplication and division operations with this calculator. " \
                       " To add, just say add 2.2 and 5.1." \
                       " To subtract, just say subtract 5 minus 2." \
                       " To multiply, just say what is 2 times 4." \
                       " To divide, just say what is 6 by 2." \
                       " Anytime you want to stop just say stop."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input) or
                ask_utils.is_intent_name("NoIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sound_effect = '<audio src="soundbank://soundlibrary/musical/amzn_sfx_trumpet_bugle_04"/>'
        speak_output = f"{sound_effect} Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return (handler_input
                .response_builder
                .set_should_end_session(True)
                .response)


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "I do not understand what you asked, please try again. Say <b>Help</b> for to find the ways to ask equations."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                # .ask("Do you want to me to figure another equation for you?")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again later. Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                # .ask(speak_output)
                .response
        )


class AddIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AddIntent")(handler_input)

    def handle(self, handler_input):
        numbers = extract_numbers(handler_input)
        n1 = numbers["n1"]
        n2 = numbers["n2"]
        result = speakable(calc.addition(n1, n2))

        speak_output = f"The result of {n1} plus {n2} is {result} {continue_msg} "
        card = SimpleCard("My Calculator", str(result))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(card)
                .set_should_end_session(False)
                .response
        )


class YesIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("YesIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("in yes intent handler")

        speak_output = " You can now say your next equation. "

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                .set_should_end_session(False)
                .response
        )


class SubtractIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SubtractIntent")(handler_input)

    def handle(self, handler_input):
        numbers = extract_numbers(handler_input)
        n1 = numbers["n1"]
        n2 = numbers["n2"]
        result = speakable(calc.subtraction(n1, n2))

        speak_output = f"The result of {n1} minus {n2} is {result} {continue_msg} "
        card = SimpleCard("My Calculator", str(result))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(card)
                .set_should_end_session(False)
                .response
        )


class MultiplicationIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MultiplyIntent")(handler_input)

    def handle(self, handler_input):
        numbers = extract_numbers(handler_input)
        n1 = numbers["n1"]
        n2 = numbers["n2"]
        result = speakable(calc.multiplication(n1, n2))

        speak_output = f"The result of {n1} times {n2} is {result} {continue_msg} "
        card = SimpleCard("My Calculator", str(result))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(card)
                .set_should_end_session(False)
                .response
        )


class DivisionIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DivideIntent")(handler_input)

    def handle(self, handler_input):
        numbers = extract_numbers(handler_input)
        n1 = numbers["n1"]
        n2 = numbers["n2"]
        result = speakable(calc.division(n1, n2))

        speak_output = f"The result of {n1} by {n2} is {result} {continue_msg} "
        card = SimpleCard("My Calculator", str(result))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(card)
                .set_should_end_session(False)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AddIntentHandler())
sb.add_request_handler(SubtractIntentHandler())
sb.add_request_handler(MultiplicationIntentHandler())
sb.add_request_handler(DivisionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
