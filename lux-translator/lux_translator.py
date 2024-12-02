
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
        elif lux > 10:
            morse_code += "-"
        else:
            morse_code += " "
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
                l2r_trim = left_to_right_trimming(word)
                if l2r_trim:
                    decoded_message += l2r_trim
                else:
                    r2l_trim = right_to_left_trimming(word)
                    if r2l_trim:
                        decoded_message += r2l_trim
                    else:
                        trimmed_spaces = trim_spaces(word)
                        if trimmed_spaces:
                            decoded_message += trimmed_spaces
                        else:
                            # The last resort, interpreting character by character, which is not intuitive
                            decoded_message += character_mapping(word)

        decoded_message += " "  # Add space between words

    return decoded_message.strip()

def left_to_right_trimming(word) -> str:
    i = 0
    while i < len(word):
      # print('l2r: ', word[i:])
      common_word =  MORSE_CODE_COMMON_WORDS_DICT.get(word[i:])
      if common_word:
          return common_word
      else:
          morse_abbr = MORSE_CODE_ABBREVIATION_DICT.get(word[i:])
          if morse_abbr:
              return morse_abbr
      i+= 1
    return ''

def right_to_left_trimming(word) -> str:
    i = len(word)
    while i > 0:
      # print('r2l: ', word[:i])
      common_word =  MORSE_CODE_COMMON_WORDS_DICT.get(word[:i])
      if common_word:
          return common_word
      else:
          morse_abbr = MORSE_CODE_ABBREVIATION_DICT.get(word[:i])
          if morse_abbr:
              return morse_abbr
      i-= 1
    return ''

def trim_spaces(word) -> str:
    decoded_message = ''
    letters = word.split()  # Split letters by spaces
    for letter in letters:
        decoded_message += MORSE_CODE_DICT.get(letter, '')
    return decoded_message

def character_mapping(word) -> str:
    decoded_message = ''
    characters = list(word)
    buffer = []
    for character in characters:
        if buffer:
            letter = MORSE_CODE_DICT.get(''.join(buffer), '')        
        else:     
            letter = MORSE_CODE_DICT.get(character, '')
        if not letter:
            buffer.append(character)
        else:
            decoded_message += letter
            buffer.clear()
    return decoded_message

