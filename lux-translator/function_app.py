import azure.functions as func
import logging
import json
import base64
from lux_translator import lux_to_morse, morse_to_text

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="")
def ica_lux_translator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Decode the base64-encoded request body
        encoded_body = req.get_body()  # Get raw request body as bytes
        decoded_body = base64.b64decode(encoded_body).decode('utf-8')  # Decode from base64
        logging.info(f"Decoded body: {decoded_body}")

        # Parse the decoded body as JSON
        request_json = json.loads(decoded_body)
        logging.info(f"Parsed JSON: {request_json}")

        lux_values = request_json.get('data', {}).get('body', {}).get('lux_values')
        if not lux_values:
            raise ValueError("No lux_values provided.")

        msg_origin = request_json.get('data', {}).get('body', {}).get('from')

        # Convert lux values to Morse code
        morse_code = lux_to_morse(lux_values)
        logging.info(f"Morse Code: {morse_code}")

        # Translate Morse code to English text
        english_text = morse_to_text(morse_code)
        logging.info(f"Translated Text: {english_text}")

        return func.HttpResponse(f"Message received: {english_text} <br> From: {msg_origin} <br> Morse code: {morse_code}")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=400)