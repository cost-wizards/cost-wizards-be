#!/bin/bash

envault list -e prod > .env;
uvicorn cost_wiz.main:app --host 0.0.0.0 --reload