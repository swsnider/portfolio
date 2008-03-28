#!/bin/bash
cd $1  #Go into the directory of swfs

for i in *.swf
do
swfdump -t $i > $i.txt
done
