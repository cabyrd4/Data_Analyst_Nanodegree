#Make Effective Data Visualization

By Carvus Byrd

##Summary

These data visualization illustrate changes over a four year stretch of how much NBA teams can change with only the addition (or subtraction) of one or two key players.  The slope graph below display changes in Winning Percentage (W.L.%) when comparing between the two regular seasons in 2013 and 2014 vs. the two regular seasons in 2015 and 2016.

##Design

###Exploratory Data Analysis

I decided to use the same dataset that I created for a previous (P4) Udacity Nanodegree project.  This dataset includes NBA regular season team level statistics from 1981 to 2016.  The dataset was compiled by using R to scrape the information from HTML tables on Basketball Reference  I’ve included a small snippet to help explain:

*I have recently been reading "Mathletics" by Wayne Winston (http://waynewinston.com). It's a neat book where this sport enthusiast and math professor walks the reader through how to calculate most any statistic for baseball, basketball, and football. I found his chapters on basketball and the NBA very fun to read. I also wanted to test his thoughts on how to predict wins for NBA teams using only information from the box score. He issues the assertion that you can create a wins model by looking at about 8 different variables regarding everything from effectiveness in the team's shooting to the other team's effectiveness in getting to the free throw line.*

*To create the model, Winston compares a team's abilities against their opponents (i.e. The team's EFG% vs the opponent's EFG%). This is done with EFG, TTP, RebRate, and FTR by just take the differences between the team's statistics and their opponents.*

Throughout the project, I examined several scatterplots and boxplots that were rich in information from the early 80’s to the most recent 2016 season.  However, when going back to the project, none of these graphs gave me any ideas for a truly explanatory visualization.  It wasn’t until this last week, as I was watching NBA teams chase free agent players and make trades, that I realized there may be a visualization to show why teams covet these select few players.  A basketball team only has 10 to 15 players on a roster and only 5 can play at one time.  Adding one (or two) significant player can completely change a team.  I wanted to show the impact a small number of players and their movement among teams can make on a team’s winning percentage.

While looking through potential visualizations to show the impact of player movement and team performance year to year, I quickly realized that 30 line “line graph” over a 35 year time frame would look messy and wouldn’t really tell a story.  The more I closed the gap on the time range, the more my graph looked like a slopegraph.  I quickly realized this would be the best way to show recent changes.

I reshaped my data to combine the 2013 and 2014 seasons vs the 2015 and 2016 seasons.  I picked this trench between the 4 seasons because this was a huge free agent class (http://www.sbnation.com/nba/2014/6/19/5815124/nba-free-agents-2014-rankings), both in size and quality of players.  My initial Excel “sketch” visualization is below:

##Data Visualization (D3)

##Initial Design

My initial sketch is helpful, but I immediately realize there are things I will need to correct when using D3.js.
 - Label the lines in a way that isn’t cluttered.  A legend might not be very helpful as there are 30 teams but adding small labels beside each line might work.
 - I will need to stretch out visualization vertically to order to better show impact and difference between good and bad teams.
 - Will I need axis lines?  I can either have a vertical axis or add value labels to slope lines.
 - I will not need gridlines if everything is labeled correctly.
 - Enable slope lines to be singled out by hovering over them.

I found a great slopegraph example (http://bl.ocks.org/zbjornson/2573074) to build upon for my own data.  For a baseline, I used the vanilla package plus the basic requirements mentioned.  The initial design visualization can be found in “index0.html”.

My initial impression is that the graph does show drastic changes for some teams and small changes for others.  One would be able to craft a lot of different stories from the visualization but I think there is one story that stands out more than others.  Lebron James: He left the Miami Heat and joined the Cleveland Cavaliers.  The changes that occurred for both teams shows his total impact.

###“After Collecting Feedback” Design

I’ve summarized helpful feedback (actual feedback is further down) points here:
 - Fix overlapping labels and stretch out visualization to show top to bottom differences
 - Add summary information about graph and things to look for in visualization
 - Improve color scheme

I was able to tweak the spacing and stretched the design to improve visibility and differentiation of good and bad teams.  To better help the reader (and non-basketball fans), I added a summary of the visualization and helpful tips on things to look for in the graph.  To improve the color scheme, I choose a “Facebook” blue color scheme from “ColourLovers” (http://www.colourlovers.com/palette/59867/Blown_Entrepreneur) but went with a red color for the hover interaction to help it stand out.

The “After Collecting Feedback” design visualization can be found in “index1.html” or “index.html”.

##Feedback

###Feedback #1 Kate Byrd

**What do you notice in the visualization?**

I notice the labels and values are overlapping when the values are close together.  This makes it confusing and difficult to read 

**What questions do you have about the data?**

How is the labels ordered? What am I looking at? Why did you choose a slopegraph?

**What relationships do you notice?**



**What do you think is the main takeaway from this visualization?**

I’m not sure this slopegraph best illustrates the relationships since the lines go so many directions.

**Is there something you don’t understand in the graphic?**

Not much of a sports fan so it doesn’t make as much sense to me.

###Feedback #2 Helyn Byrd

**What do you notice in the visualization?**

Cleveland improves significantly.  Golden State Warriors go from an “okay” team to the best team in the league.

**What questions do you have about the data?**

Are there deeper stories of why certain teams changed so significantly?

**What relationships do you notice?**



**What do you think is the main takeaway from this visualization?**

It’s a zero sum game/business.  When one team wins, another loses.  The graph shows that as teams get better, others get worse.

**Is there something you don’t understand in the graphic?**

I think it needs more color to help differentiate labels and lines

###Feedback #3 Caroline Byrd

**What do you notice in the visualization?**

I like the interactive lines/labels.  I like being able to pick out certain teams to isolate and compare with others.

**What questions do you have about the data?**

I’m not sure this visualization is understandable on first glance.  It needs some summary information. 

**What relationships do you notice?**

Miami Heat fell dramatically.  The impact of Lebron James leaving was big.

**What do you think is the main takeaway from this visualization?**

The NBA teams can go from bad to good and good to bad very quickly.

**Is there something you don’t understand in the graphic?**

##Resources

D3.js
https://d3js.org/

D3 Slopegraph 2
http://bl.ocks.org/zbjornson/2573074

Colour Lovers
http://www.colourlovers.com/palette/59867/Blown_Entrepreneur

NBA 2014 Free Agent Class
http://www.sbnation.com/nba/2014/6/19/5815124/nba-free-agents-2014-rankings
