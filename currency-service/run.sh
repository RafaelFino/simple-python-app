#!/bin/bash

uvicorn app.main:app --reload --log-level trace --port 8081 --host 0.0.0.0 --log-config etc/log-config.yml