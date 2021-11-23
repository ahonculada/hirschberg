set terminal size 500,500
set output 'results_time.png'
set title 'Time in Seconds'
plot 'results.txt' using 1:3
