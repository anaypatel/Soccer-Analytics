library(dplyr)
library(tidyverse)
library(ggplot2)
library(clue)
library(plyr)

source('createPitchETM.R')

setwd("~/Desktop/Soccer Analytics/R Programs")

#passes_2017 = read.csv('../Soccer Data/2017 Stats/raw passes.csv')
#passes_2018 = read.csv('../Soccer Data/2018 Stats/raw passes.csv')
#passes_2019 = read.csv('../Soccer Data/2019 Stats/raw passes.csv')

#passes = rbind(passes_2017, passes_2018, passes_2019)

pass_to_kp = read.csv('../Soccer Data/Other Stats/2017-2019 SJE pass to key passes.csv')
pass_to_kp = pass_to_kp[pass_to_kp$passToKeyPass == 1,]

passer = 'Andrew Tarbell'
recipient = 'Cristian Espinoza'
team = 'San Jose'

#passes = pass_to_kp[pass_to_kp$team == team,]

View(pass_to_kp %>% dplyr::filter(season == 2019) %>% dplyr::group_by(passer) %>% dplyr::summarise(p.t.kp = n()))

passes = pass_to_kp %>% dplyr::filter(recipient == 'Cristian Espinoza' | recipient == 'Shea Salinas')

passes$x = 1.15*passes$x
passes$endX = 1.15*passes$endX
passes$y = 0.8*passes$y
passes$endY = 0.8*passes$endY

passes$distance = sqrt((passes$x - passes$endX)^2 + (passes$y - passes$endY)^2)
passes$passHorizontal = passes$endY - passes$y
passes$passVertical = passes$endX - passes$x
passes$passAngle = atan(passes$passVertical/passes$passHorizontal)
passes$passGoalDistanceEnd = sqrt((passes$endX - 100)^2 + (passes$endY - 50)^2)

cluster_cols=c('x','y','endX', 'endY', 'longball', 'cross', 'headpass', 'throughball',
                    'keyPass', 'distance', 'passHorizontal', 'passVertical', 
                    'passAngle', 'passGoalDistanceEnd')

rownames(passes) <- 1:nrow(passes)


passes.clust=na.omit(sample_n(passes, 64))

kmeans=kmeans(passes.clust[,cluster_cols], center=12, iter.max=1000, algorithm="MacQueen")

passes$cluster=cl_predict(kmeans, newdata=passes[,cluster_cols])

cluster_ranks = as.data.frame(order(-table(passes$cluster)))
names(cluster_ranks) = c('rank')
cluster_ranks$index = seq.int(nrow(cluster_ranks))

passes$cluster_rank = mapvalues(passes$cluster, from=cluster_ranks$rank, to=cluster_ranks$index)

createPitch(data=sample_n(passes,64))+
  geom_segment(aes(x=x, y=y, xend=endX, yend=endY, color=as.character(cluster)), arrow=arrow(length=unit(4,"points")))+
  facet_wrap(~cluster_rank)+
  theme(legend.position = "none")+
  ggtitle('2019 SJ Earthquakes Pass To Key Pass K-Means Clustering', 'Data: @AnalysisEvolved, Insp: @tacticsplatform, @etmckinley')

#ggsave('../Visualizations/Jesse Meeting 2/2019 SJ Earthquakes Pass To Key Pass K-Means Clustering.png')

