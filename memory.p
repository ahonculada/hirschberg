set terminal png size 500,500
set output 'results.png'
set title 'Memory Usage'
plot 'results.txt' using 1:2