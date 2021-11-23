#!/bin/bash

for i in {100..2000..100}
do
	python3 average.py $i
done
gnuplot memory.p

