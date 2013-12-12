#!/bin/bash
find . -iname '*.pyc' -exec sudo rm {} \;
echo "removed .pyc files"
touch core/wsgi.py
echo "touched my wsgi"
