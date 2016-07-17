statesinfo = read.csv('stateData.csv')

stateSubset = subset(statesinfo, state.region == 1)
head(stateSubset, 2)
dim(stateSubset)

stateSubsetBracket = statesinfo[statesinfo$state.region == 1, ]
head(stateSubsetBracket, 2)
dim(stateSubsetBracket)

*********
  
reddit = read.csv('reddit.csv')
str(reddit)

table(reddit$employment.status)
summary(reddit)

levels(reddit$age.range)

library(ggplot2)
qplot(data = reddit, x = age.range)

is.factor(reddit$age.range)
age.range.o = ordered(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"))
qplot(data = reddit, x = age.range.o)
