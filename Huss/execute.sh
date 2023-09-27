#! /bin/bash
#Hussein
read -p "How many times do you want to execute the attack: " iteration
read -p "Enter message to send (enter 'exit' to quit): " message1
i=$iteration
export message=$message1
while [ $i -gt 0 ];do
    sudo python attackFromKali.py
    ((i=i-1))
done
echo "---------------------------------------------------------------------------------"
echo "Attack has been successfuly executed $iteration time(s)"
