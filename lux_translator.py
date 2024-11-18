import logging
import azure.functions as func

# Morse Code Dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9', '..--..': '?',
    '-.-.--': '!', '.-.-.-': '.', '--..--': ','
}

MORSE_CODE_ABBREVIATION_DICT = {
    "...---...": "SOS",
    "-.-. --.-": "CQ",
    "-.. .": "DE",
    "--... ...--": "73",
    "---.. ---..": "88",
    ".- .-.": "AR",
    "...-.-": "SK",
    "-... -.-": "BK",
    ".-.": "R",
    "-.--.-": "K",  # Also used for KN
    "- ..-": "TU",
    "--.- - ....": "QTH",
    "--.- .-. --": "QRM",
    "--.- .-. -.": "QRN",
    "--.- .-. ...": "QRS",
    "--.- .-. --.-": "QRQ",
    "--.- ... .-..": "QSL",
    "--.- ... -...": "QSB"
}

MORSE_CODE_COMMON_WORDS_DICT = {
    "......-...--.": "HELP",
    "..-....-..": "FIRE",
    "...----.--.": "STOP",
    "----.-": "OKAY"
}


def lux_to_morse(lux_values):
    """
    Converts a sequence of lux values to Morse code.
    Assume:
    - Short pulse (dot) for lux values > 100
    - Long pulse (dash) for lux values <= 100
    """
    morse_code = ""
    for lux in lux_values:
        if lux > 100:
            morse_code += "."
        else:
            morse_code += "-"
    return morse_code

def morse_to_text(morse_sequence):
    """
    Converts Morse code sequence into English text.
    """
    words = morse_sequence.split(" / ")  # Split words by slash
    decoded_message = ""

    for word in words:
        common_word = MORSE_CODE_COMMON_WORDS_DICT.get(word)
        if common_word:
            decoded_message += common_word
        else:
            morse_abbr = MORSE_CODE_ABBREVIATION_DICT.get(word)
            if morse_abbr:
                decoded_message += morse_abbr
            else:    
                letters = word.split()  # Split letters by spaces
                for letter in letters:
                    decoded_message += MORSE_CODE_DICT.get(letter, '')
        decoded_message += " "  # Add space between words
    return decoded_message.strip()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        lux_values = req.get_json().get('lux_values')
        if not lux_values:
            raise ValueError("No lux_values provided.")

        # Convert lux values to Morse code
        morse_code = lux_to_morse(lux_values)
        logging.info(f"Morse Code: {morse_code}")

        # Translate Morse code to English text
        english_text = morse_to_text(morse_code)
        logging.info(f"Translated Text: {english_text}")

        return func.HttpResponse(f"The translated text is: {english_text}")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=400)