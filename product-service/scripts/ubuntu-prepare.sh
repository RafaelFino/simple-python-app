!#/bin/bash
# Update system
apt update -y && apt install python3 python3-pip git -y && apt upgrade python3 python3-pip -y

# Change Work dir
cd ~

# Get repo
git clone https://github.com/RafaelFino/simple-python-app.git

# Change work dir
cd simple-python-app/currency-service

# Install app python dependencies
pip3 install -r requirements.txt

# Start application
uvicorn app.main:app --reload --log-level trace --port 8082 --host 0.0.0.0 --log-config etc/log-config.yml
