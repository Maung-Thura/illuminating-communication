import unittest
from lux_translator import lux_to_morse, morse_to_text
import json

class TestLuxToText(unittest.TestCase):

    def test_sos(self):
        # Simulate lux values for S.O.S (Short - Short - Short / Long - Long - Long / Short - Short - Short)
        lux_values = [150, 150, 150, 50, 50, 50, 150, 150, 150]  # Morse equivalent: ... --- ...
        morse_code = lux_to_morse(lux_values)
        self.assertEqual(morse_code, "...---...")

        # Translate to English
        translated_text = morse_to_text(morse_code)
        self.assertEqual(translated_text, "SOS")

# ......-...--.
    def test_help(self):
        # Simulate lux values for HELP 
        lux_values = [150, 150, 150, 150, 150, 150, 50, 150, 150, 150, 50, 50, 150] 
        morse_code = lux_to_morse(lux_values)
        self.assertEqual(morse_code, "......-...--.")

        # Translate to English
        translated_text = morse_to_text(morse_code)
        self.assertEqual(translated_text, "HELP")

    def test_json_parser(self):
        # JSON string
        json_string = """{
        "id":"7c0ea26a-f89d-10a6-7b05-ae2bec8b3d45",
        "topic":"/SUBSCRIPTIONS/2C28E045-9EB5-4A42-BD37-68F67E30F959/RESOURCEGROUPS/MAUNG_THU_RA_RESOURCES/PROVIDERS/MICROSOFT.DEVICES/IOTHUBS/MAUNG-THU-RA-HUB",
        "subject":"devices/de10nano-mthura",
        "eventType":"Microsoft.Devices.DeviceTelemetry",
        "data":{
            "properties":{},
            "systemProperties":{
                "iothub-content-type":"application/JSON",
                "iothub-content-encoding":"UTF-8",
                "iothub-connection-device-id":"de10nano-mthura",
                "iothub-connection-auth-method":"{\\"scope\\":\\"device\\",\\"type\\":\\"sas\\",\\"issuer\\":\\"iothub\\"}",
                "iothub-connection-auth-generation-id":"638642053641823949",
                "iothub-enqueuedtime":"2024-11-17T22:40:06.7200000Z",
                "iothub-message-source":"Telemetry",
                "dt-dataschema":"dtmi:Terasic:FCC:DE10_Nano;1"
            },
            "body":{
                "lux":10.128000259399414,
                "from":"2145 Sheridan Rd 60208",
                "notify":true
            }
        },
        "dataVersion":"",
        "metadataVersion":"1",
        "eventTime":"2024-11-17T22:40:06.72Z"
        }"""

        # Parse the JSON string
        data = json.loads(json_string)

        # Extract the 'lux' value
        lux_value = data["data"]["body"]["lux"]

        # Assert the extracted value
        self.assertEqual(lux_value, 10.128000259399414)

    def test_random_morse_code(self):
        morse_sequence = "...----.-.---"
        translated_text = morse_to_text(morse_sequence)
        self.assertEqual(translated_text, 'EEETTTTETETTT')


if __name__ == '__main__':
    unittest.main()