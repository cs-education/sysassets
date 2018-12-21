#!/bin/bash
curl -s "https://cs-education.github.io/sysassets/chapters/chapter01/play-3-2-test.c" | gcc -xc - -o test
if [ $? != 0 ]
then
    echo compilation failed
else
    ./test ./program
fi