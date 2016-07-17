library(ggplot2)
library(ggthemes)
theme_set(theme_wsj())
data(diamonds)

head(diamonds)

ggplot(aes(x = price, fill = cut), data = diamonds) +
  geom_histogram(binwidth = 1000) +
  facet_wrap(~color)

ggplot(aes(x = table, y = price), data = diamonds) +
  geom_point(alpha = 1/10,aes(color = cut))

summary(diamonds[diamonds$cut == 'Ideal',]$table)
summary(diamonds[diamonds$cut == 'Premium',]$table)

diamonds <- transform(diamonds, volume = x * y * z)
ggplot(aes(x = volume, y = price), data = diamonds) + 
  geom_point(aes(color = clarity), alpha = 1/20) +
  scale_y_log10()+
  xlim(0, quantile(diamonds$volume, 0.99))

pf <- read.csv('pseudo_facebook.tsv', sep = '\t')
names(pf)
pf <- transform(pf, prop_initiated  = friendships_initiated/friend_count)

pf$year_joined = floor(2014 - (pf$tenure / 365))
pf$year_joined.bucket = cut(pf$year_joined, c(2004,2009,2011,2012,2014))
table(pf$year_joined.bucket)

ggplot(aes(x = tenure, y = prop_initiated),
       data = subset(pf, !is.na(year_joined.bucket))) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median)

ggplot(aes(x = tenure, y = prop_initiated), data = pf) +
  geom_smooth(aes(color = year_joined.bucket))

summary(pf[pf$year_joined.bucket == '(2012,2014]',]$prop_initiated)

ggplot(aes(x = cut, y = price/carat), data = diamonds) +
  geom_jitter(aes(color = color)) +
  facet_wrap(~ clarity)
