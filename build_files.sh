#!/bin/bash

# Install Python 3.9 if not already installed
if ! command -v python3.9 &> /dev/null
then
    echo "Python 3.9 not found, installing..."
    # Adjust the installation command according to your OS
    sudo apt-get update
    sudo apt-get install python3.9
fi

# Install pip if not already installed
if ! command -v pip3.9 &> /dev/null
then
    echo "pip for Python 3.9 not found, installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.9 get-pip.py
fi

# Install requirements
pip3.9 install -r requirements.txt

# Run collectstatic
python3.9 manage.py collectstatic --noinput

echo "Build completed successfully."
