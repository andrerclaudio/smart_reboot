#!/usr/bin/env python3
import logging
import json
import sys
import os


# Print in software terminal
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(process)d | %(levelname)s:  %(message)s',
                    datefmt='%d/%b/%Y - %H:%M:%S')

logger = logging.getLogger(__name__)
# Disable logs by default
logger.propagate = False

HOSTNAME = "google.com"
THRESHOLD_TO_REBOOT = 3


def main(argv):
    """
    argv: The value "on" will be parsed in order to enable the terminal logs.
    """

    if 'on' in argv:
        # If "on" was passed, enable logs.
        logger.propagate = True

    try:
        # Ping
        response = os.system("ping -c 1 " + HOSTNAME)

        #and then check the response...
        if response == 0:
            logger.info('Connection is up! Reseting the counter.')
            counter = {"counter": 0}
            with open("status.json", "w", encoding='utf-8') as file:
                json.dump(counter, file)

        else:
            # Add 1 to the counter
            with open("status.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                val = data["counter"] + 1
                counter = {"counter": val}

                logger.info(f'Counter[{THRESHOLD_TO_REBOOT} to reboot]: {val}')

            if val >= THRESHOLD_TO_REBOOT:
                # Cleaning the variable
                counter = {"counter": 0}
                with open("status.json", "w", encoding='utf-8') as file:
                    json.dump(counter, file)

                logger.info("Sending reboot command!")
                os.system('systemctl reboot -i')

            else:
                with open("status.json", "w", encoding='utf-8') as file:
                    json.dump(counter, file)
    
    except Exception as exc:
        logger.exception(exc, exc_info=False)


if __name__ == "__main__":
    # Run the main function sharing any passed arguments.
    main(sys.argv[1:])
