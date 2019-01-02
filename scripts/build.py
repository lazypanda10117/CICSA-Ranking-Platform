import os

if os.environ.get('BUILD_TYPE') in ["Init", "Update", "Run"]:
    print(os.environ.get('BUILD_TYPE'))
else:
    print("Run")
