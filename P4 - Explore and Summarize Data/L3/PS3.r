library(ggplot2)
data(diamonds)
summary(diamonds)
?diamonds

names(diamonds)

qplot(x = price, data = diamonds)

sum(diamonds$price < 500)
sum(diamonds$price < 250)
sum(diamonds$price >= 15000)

qplot(x = price, data = diamonds, binwidth = 100, xlim = c(0,2000))

qplot(x = price, data = diamonds) +
  facet_wrap(~cut)

by(diamonds$price, diamonds$cut, max)
by(diamonds$price, diamonds$cut, min)
by(diamonds$price, diamonds$cut, summary)

qplot(x = price, data = diamonds) +
  facet_wrap(~cut, scales="free_y")

qplot(x = price/carat, data = diamonds, binwidth = .02) +
  scale_x_log10() +
  facet_wrap(~cut, scales="free_y")

qplot(x = color, y = price, data = diamonds, geom = 'boxplot')

by(diamonds$price, diamonds$color, summary)
by(diamonds$price, diamonds$color, IQR)

IQR(subset(diamonds, price <1000)$price)

qplot(x = color, y = price/carat, data = diamonds, geom = 'boxplot')

qplot(x = friend_count, y = ..count../sum(..count..), 
      data = subset(pf, !is.na(gender)), 
      xlab = 'Friend Count',
      ylab = 'Proportion of Users with that friend count',
      binwidth = 10, geom = "freqpoly", color = gender) +
  scale_x_continuous(limits = c(0, 1000),
                     breaks = seq(0, 1000, 50))

qplot(x = carat, data = diamonds, binwidth = .01, geom = "freqpoly")
table(diamonds$carat)

install.packages(tidyr)
library(tidyr)
