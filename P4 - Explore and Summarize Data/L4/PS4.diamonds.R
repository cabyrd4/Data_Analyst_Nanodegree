library(ggplot2)
library(dplyr)
library(gridExtra)
data("diamonds")

head(diamonds)

ggplot(aes(x = x, y = price), data = diamonds) + 
  geom_point()

cor.test(diamonds$price, diamonds$x, method = 'pearson')
cor.test(diamonds$price, diamonds$y, method = 'pearson')
cor.test(diamonds$price, diamonds$z, method = 'pearson')

ggplot(aes(x = depth, y = price), data = diamonds) + 
  geom_point()

ggplot(aes(x = depth, y = price), data = diamonds) + 
  geom_point(alpha = 1/100) +
  scale_x_continuous(breaks = seq(0,80,2))

summary(diamonds$depth)

cor.test(diamonds$price, diamonds$depth, method = 'pearson')

ggplot(data = diamonds,aes(x = carat, y = price)) + 
  xlim(0,quantile(diamonds$carat,0.99)) +
  ylim(0,quantile(diamonds$price,0.99)) +
  geom_point()

diamonds$volume = diamonds$x * diamonds$y * diamonds$z

ggplot(data = diamonds,aes(x = volume, y = price)) + 
  geom_point()

diamonds_filtered = filter(diamonds, volume != 0 & volume < 800)

cor.test(diamonds_filtered$price, diamonds_filtered$volume, method = 'pearson')

ggplot(aes(x = volume, y = price), data = diamonds_filtered) + 
  geom_point(alpha = 1/100) +
  stat_smooth(method = "lm", formula = y ~ x, size = 1)

clarity_groups = group_by(diamonds, clarity)
diamondsByClarity = summarise(clarity_groups,
                                 price_mean = mean(price),
                                 price_median = median(price),
                                 price_min = min(price),
                                 price_max = max(price),
                                 n = n())
diamondsByClarity = arrange(diamondsByClarity, clarity)

head(diamondsByClarity)

diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

p1  <- ggplot(diamonds_mp_by_clarity, aes(x = clarity, y = mean_price, fill= clarity)) +
  geom_bar(stat = "identity")

p2 <- ggplot(diamonds_mp_by_color, aes(x = color, y = mean_price, fill= color)) +
  geom_bar(stat = "identity")

grid.arrange(p1,p2, ncol =2)

