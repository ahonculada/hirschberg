#!/bin/bash

for i in {100..6000..500}
do
	python3 average.py $i
done
gnuplot time.p
gnuplot memory.p

