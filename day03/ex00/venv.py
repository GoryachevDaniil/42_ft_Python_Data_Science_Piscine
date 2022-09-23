import os

# python3 -m venv mturquin
# source mturquin/bin/activate
# chmod +x file.py

if __name__ == '__main__':
    print(f"Your current virtual env is {os.environ['VIRTUAL_ENV']}")

# deactivate