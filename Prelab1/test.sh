#!/bin/bash
# Problem 10 Script

 counter=0

 for file in *; do
  while read line
   do
   evenNO=$(($counter%2))
if ([ $evenNO -ne 0 ] && [ "$file" != "test.sh" ]) then
     echo "$file: $line"
fi
      ((counter ++))
   done < "$file"
   counter=0
 done
