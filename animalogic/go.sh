echo Running Python program to generate random boards and solve them.
echo Please be patient. This may take a few minutes.
time python3 animalogic.py > game.csv

echo
echo Running R for analysis.
R CMD BATCH analyze.R
