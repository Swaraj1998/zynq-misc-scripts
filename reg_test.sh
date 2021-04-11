#!/bin/bash

for x in {0..63}
do
printf "For input 0x%02x :\n" $x
printf -v hexval "%x" "$x"
sudo python zynq_ftm.py p2f0 $hexval
sudo python zynq_ftm.py p2f3 0x40
sudo python zynq_ftm.py p2f3 0xc0
sudo python zynq_ftm.py f2p
done
