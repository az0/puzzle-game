# Andrew Ziem, July 2018

game <- read.csv('game.csv')

# Summarize the distribution of solutions per board
summary(game$solution_count)

# Visualize the distribution of solutions per board
require(ggplot2)
png('analyze.png', width=600, height=600)
qplot(game$solution_count, geom="histogram")
dev.off()
