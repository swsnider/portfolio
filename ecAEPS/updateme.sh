#!/bin/bash
kill $1
cd ecaeps
svn up -r$2
cd ..
python start-ecaeps.py &
