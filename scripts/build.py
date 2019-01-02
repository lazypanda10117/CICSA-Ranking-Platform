import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "rtype",
    help="Return Type (1: Build Type, 2: Build Location)",
    type=int
)
args = parser.parse_args()

if args.rtype == 1:
    if os.environ.get('BUILD_TYPE') in ["DEV", "PROD"]:
        print(os.environ.get('BUILD_TYPE'))
    else:
        print("PROD")
elif args.rtype == 2:
    if os.environ.get('BUILD_LOC') in ["LOCAL", "SERVER"]:
        print(os.environ.get('BUILD_LOC'))
    else:
        print("LOCAL")
else:
    raise SystemError('Not a Valid Return Type')
