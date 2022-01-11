#!/bin/bash

# /etc/systemd/system/vinbot.service

cd /home/smriti/vinay/te_bot
source bot/bin/activate
python3 vinvns_bot.py >> ./logs/myapp.log 2>&1
