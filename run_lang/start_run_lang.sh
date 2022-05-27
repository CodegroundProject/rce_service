#!/bin/bash

waitress-serve --port=6004 --call 'run_lang:create_app'
