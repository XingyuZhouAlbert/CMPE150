#!/bin/bash
# only prints the even numbered lines of each file in the current directory. 
# The output should be filename: line for each even numbered line.

# Declare Varialbes
file=$0
counter=0

for file in *; do
while read line
do
evenNo=$(($counter%2))
if [ $evenNo -ne 0 ]
then
echo "$file: $line"
fi
((counter ++))
done < "$file"
done