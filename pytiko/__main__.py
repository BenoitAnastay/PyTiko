import argparse
import json
import sys
import logging


from pytiko.client import TikoClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=True, help="Email")
    parser.add_argument("-p", "--password", required=True, help="Password")
    parser.add_argument("--debug", action="store_true", help="Print debug messages to stderr")
    args = parser.parse_args()

    if args.debug:
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    client = TikoClient(args.email, args.password)
    client.login()

if __name__ == '__main__':
    main()