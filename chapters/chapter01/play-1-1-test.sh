#!/bin/bash
curl -s "localhost:8000/sysassets/chapters/chapter01/play-1-1-test.c" | gcc -xc - -o test
if [ $? != 0 ]
then
    echo compilation failed
else
    ./test ./program
fi