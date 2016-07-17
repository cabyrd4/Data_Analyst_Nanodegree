install.packages("rvest")
install.packages("dplyr")
install.packages("pipeR")
install.packages("stringr")
install.packages("ggplot2")

library(rvest)
library(dplyr)
library(pipeR)
library(stringr)
library(ggplot2)
library(reshape2)

# Western Conference Records Table
base = 'http://www.basketball-reference.com/leagues/NBA_'
year = 2013
all_seasons_west_records = {}

while(year < 2017) {
  url = paste0(base, toString(year), '.html')
  team_table = '//*[@id="W_standings"]'
  
  nba = url %>%
    html() %>%
    html_nodes(xpath=team_table) %>%
    html_table()
  nba = nba[[1]]
  
  nba$year = year
  
  all_seasons_west_records = bind_rows(nba,all_seasons_west_records)
  year = year + 1 }

# Eastern Conference Records Table
base = 'http://www.basketball-reference.com/leagues/NBA_'
year = 2013
all_seasons_east_records = {}

while(year < 2017) {
  url = paste0(base, toString(year), '.html')
  team_table = '//*[@id="E_standings"]'
  
  nba = url %>%
    html() %>%
    html_nodes(xpath=team_table) %>%
    html_table()
  nba = nba[[1]]
  
  nba$year = year
  
  all_seasons_east_records = bind_rows(nba,all_seasons_east_records)
  year = year + 1 }

# Records Audit & Clean Up
# Western Conference
all_seasons_west_records$`Western Conference` = 
  str_replace_all(all_seasons_west_records$`Western Conference`, 
    "[(,),1,2,3,4,5,6,7,8,9,0,?]", "")

all_seasons_west_records$`Western Conference` =
  str_trim(all_seasons_west_records$`Western Conference`, 
    side = c("both", "left", "right"))

all_seasons_west_records = filter(all_seasons_west_records, 
  `Western Conference` != "Midwest Division",
  `Western Conference` != "Northwest Division",
  `Western Conference` != "Pacific Division",
  `Western Conference` != "Southwest Division")

all_seasons_west_records$Conference = "West"
all_seasons_west_records = rename(all_seasons_west_records, Team = `Western Conference`)

# Eastern Conference
all_seasons_east_records$`Eastern Conference` = 
  str_replace_all(all_seasons_east_records$`Eastern Conference`, 
                  "[(,),1,2,3,4,5,6,7,8,9,0,?]", "")

all_seasons_east_records$`Eastern Conference` = 
  str_replace_all(all_seasons_east_records$`Eastern Conference`, 
                  "Philadelphia ers", "Philadelphia 76ers")

all_seasons_east_records$`Eastern Conference` =
  str_trim(all_seasons_east_records$`Eastern Conference`, 
           side = c("both", "left", "right"))

all_seasons_east_records = filter(all_seasons_east_records, 
                                  `Eastern Conference` != "Central Division",
                                  `Eastern Conference` != "Atlantic Division",
                                  `Eastern Conference` != "Southeast Division")

all_seasons_east_records$Conference = "East"
all_seasons_east_records = rename(all_seasons_east_records, Team = `Eastern Conference`)

# Team Table
base = 'http://www.basketball-reference.com/leagues/NBA_'
year = 2013
all_seasons_team = {}

while(year < 2017) {
url = paste0(base, toString(year), '.html')
team_table = '//*[@id="team"]'

nba = url %>%
  html() %>%
  html_nodes(xpath=team_table) %>%
  html_table()
nba = nba[[1]]

nba$year = year
names(nba)[10] = "3P%"
names(nba)[13] = "2P%"

all_seasons_team = bind_rows(nba,all_seasons_team)
year = year + 1 }

# Opp Table
base = 'http://www.basketball-reference.com/leagues/NBA_'
year = 2013
all_seasons_opp = {}

while(year < 2017) {
url = paste0(base, toString(year), '.html')
opp_table = '//*[@id="opponent"]'
  
nba = url %>%
  html() %>%
  html_nodes(xpath=opp_table) %>%
  html_table()
nba = nba[[1]]
  
nba$year = year
names(nba)[10] = "3P%"
names(nba)[13] = "2P%"
  
all_seasons_opp = bind_rows(nba,all_seasons_opp)
year = year + 1 }

# Team & Opp Audit & Clean Up
# Team
all_seasons_team = filter(all_seasons_team, 
                                  Team != "League Average")

# Opp
all_seasons_opp = filter(all_seasons_opp, 
                          Team != "League Average")

all_seasons_opp = rename(all_seasons_opp, Opp_FG = FG, Opp_FGA = FGA, `Opp_FGA%` = `FG%`, `Opp_3P` = `3P`,
       `Opp_3PA` = `3PA`, `Opp_3P%` = `3P%`, Opp_2P = `2P`, Opp_2PA = `2PA`, `Opp_2P%` = `2P%`,
       Opp_FT = FT, Opp_FTA = FTA, `Opp_FT%` = `FT%`, Opp_ORB = ORB, Opp_DRB = DRB, 
       Opp_TRB = TRB, Opp_AST = AST, Opp_STL = STL, Opp_BLK = BLK, Opp_TOV = TOV, 
       Opp_PF = PF, Opp_PTS = PTS, `Opp_PTS/G` = `PTS/G`)

# Combining Tables
all_seasons_combined_records = bind_rows(all_seasons_east_records,all_seasons_west_records)

all_seasons_team_and_opp = merge(all_seasons_team, all_seasons_opp, by = c("Team", "year", "G", "MP"))

nba_data = merge(all_seasons_combined_records, all_seasons_team_and_opp, by = c("Team", "year"))

# Making Relevant Variables

# Fix Small Issues
nba_data$Team = ifelse(str_detect(nba_data$Team, "[*]") == TRUE, substr(nba_data$Team,1,nchar(nba_data$Team)-1), nba_data$Team)
nba_data$Team = ifelse(str_detect(nba_data$Team, "Charlotte Bobcats") == TRUE, "Charlotte Hornets", nba_data$Team)
nba_data$Team = ifelse(str_detect(nba_data$Team, "New Orleans Hornets") == TRUE, "New Orleans Pelicans", nba_data$Team)
nba_data$W = as.numeric(nba_data$W)
nba_data$L = as.numeric(nba_data$L)

# Year Grouping
nba_data$year_group = "2013-2014"
nba_data$year_group[nba_data$year > 2014] = "2015-2016"

summary(nba_data)

# Grouping Data
nba_data_by_year_group_team = nba_data %>%
  group_by(year_group, Team) %>%
  summarise(
    W = sum(W),
    L = sum(L),
    FG = sum(FG),
    `3P` = sum(`3P`),
    FGA = sum(FGA),
    Opp_FG = sum(Opp_FG),
    Opp_3P = sum(Opp_3P),
    Opp_FGA = sum(Opp_FGA),
    TOV = sum(TOV),
    Opp_TOV = sum(Opp_TOV),
    ORB = sum(ORB),
    DRB = sum(DRB),
    FT = sum(FT),
    FTA = sum(FTA),
    Opp_FT = sum(Opp_FT),
    Opp_FTA = sum(Opp_FTA)
    )

# WL%
nba_data_by_year_group_team$`W/L%` = nba_data_by_year_group_team$W /
  (nba_data_by_year_group_team$W + nba_data_by_year_group_team$L)

# Effective FG%
nba_data_by_year_group_team$EFG = (nba_data_by_year_group_team$FG + (0.5 * nba_data_by_year_group_team$`3P`)) / nba_data_by_year_group_team$FGA

# Opponents Eff FG%
nba_data_by_year_group_team$Opp_EFG = (nba_data_by_year_group_team$Opp_FG + (0.5 * nba_data_by_year_group_team$Opp_3P )) / nba_data_by_year_group_team$Opp_FGA

# Turnovers Committed / Possession
nba_data_by_year_group_team$TTP = nba_data_by_year_group_team$TOV / (nba_data_by_year_group_team$FG + nba_data_by_year_group_team$TOV + 
                      (nba_data_by_year_group_team$FTA * .44))

# Turnovers Caused / Possession
nba_data_by_year_group_team$DTTP = nba_data_by_year_group_team$Opp_TOV / (nba_data_by_year_group_team$Opp_FG + nba_data_by_year_group_team$Opp_TOV + 
                      (nba_data_by_year_group_team$Opp_FTA * .44))

# Offensive Rebound Rate
nba_data_by_year_group_team$ORebRate = nba_data_by_year_group_team$ORB / (nba_data_by_year_group_team$FGA - nba_data_by_year_group_team$FG)

# Defensive Rebound Rate
nba_data_by_year_group_team$DRebRate = nba_data_by_year_group_team$DRB / (nba_data_by_year_group_team$Opp_FGA - nba_data_by_year_group_team$Opp_FG)

# Free Throw Rate
nba_data_by_year_group_team$FTR = nba_data_by_year_group_team$FT / nba_data_by_year_group_team$FGA

# Opp Free Throw Rate
nba_data_by_year_group_team$OFTR = nba_data_by_year_group_team$Opp_FT / nba_data_by_year_group_team$Opp_FGA

# Diff Variables
nba_data_by_year_group_team$EFG_diff = nba_data_by_year_group_team$EFG - nba_data_by_year_group_team$Opp_EFG
nba_data_by_year_group_team$TTP_diff = nba_data_by_year_group_team$TTP - nba_data_by_year_group_team$DTTP
nba_data_by_year_group_team$RebRate_diff = nba_data_by_year_group_team$ORebRate - nba_data_by_year_group_team$DRebRate
nba_data_by_year_group_team$FTR_diff = nba_data_by_year_group_team$FTR - nba_data_by_year_group_team$OFTR

# Consolidating NBA Data Table
nba_data_by_year_group_team = select(nba_data_by_year_group_team, Team, year_group, `W/L%`, EFG, Opp_EFG, TTP, 
                 DTTP, ORebRate, DRebRate, FTR, OFTR, EFG_diff, TTP_diff, RebRate_diff, FTR_diff)

# Reshaping Tables
nba_data_win_percent = select(nba_data_by_year_group_team, Team, year_group, `W/L%`)
nba_data_win_percent = dcast(nba_data_win_percent, Team ~ year_group)

nba_data_efg_diff = select(nba_data_by_year_group_team, Team, year_group, EFG_diff)
nba_data_efg_diff = dcast(nba_data_efg_diff, Team ~ year_group)

nba_data_ttp_diff = select(nba_data_by_year_group_team, Team, year_group, TTP_diff)
nba_data_ttp_diff = dcast(nba_data_ttp_diff, Team ~ year_group)

nba_data_rebrate_diff = select(nba_data_by_year_group_team, Team, year_group, RebRate_diff)
nba_data_rebrate_diff = dcast(nba_data_rebrate_diff, Team ~ year_group)

nba_data_ftr_diff = select(nba_data_by_year_group_team, Team, year_group, FTR_diff)
nba_data_ftr_diff = dcast(nba_data_ftr_diff, Team ~ year_group)

#Export Data to CSV
write.csv(nba_data_win_percent, file = "nba_data_win_percent.csv")
write.csv(nba_data_efg_diff, file = "nba_data_efg_diff.csv")
write.csv(nba_data_ttp_diff, file = "nba_data_ttp_diff.csv")
write.csv(nba_data_rebrate_diff, file = "nba_data_rebrate_diff.csv")
write.csv(nba_data_ftr_diff, file = "nba_data_ftr_diff.csv")

