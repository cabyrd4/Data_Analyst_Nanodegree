install.packages("rvest")
install.packages("dplyr")
install.packages("pipeR")
install.packages("stringr")

library(rvest)
library(dplyr)
library(pipeR)
library(stringr)

# Western Conference Records Table
base = 'http://www.basketball-reference.com/leagues/NBA_'
year = 1980
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
year = 1980
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
    "[(,),1,2,3,4,5,6,7,8,9,0,Â]", "")

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
                  "[(,),1,2,3,4,5,6,7,8,9,0,Â]", "")

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
year = 1980
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
year = 1980
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

# Made Playoffs
nba_data$MadePlayoffs = ifelse(str_detect(nba_data$Team, "[*]") == TRUE, "Yes", "No")
nba_data$Team = ifelse(str_detect(nba_data$Team, "[*]") == TRUE, substr(nba_data$Team,1,nchar(nba_data$Team)-1), nba_data$Team)


# Effective FG%
nba_data$EFG = (nba_data$FG + (0.5 * nba_data$`3P`)) / nba_data$FGA

# Opponents Eff FG%
nba_data$Opp_EFG = (nba_data$Opp_FG + (0.5 * nba_data$Opp_3P )) / nba_data$Opp_FGA

# Turnovers Committed / Possession
nba_data$TTP = nba_data$TOV / (nba_data$FG + nba_data$TOV + 
                      (nba_data$FTA * .44))

# Turnovers Caused / Possession
nba_data$DTTP = nba_data$Opp_TOV / (nba_data$Opp_FG + nba_data$Opp_TOV + 
                      (nba_data$Opp_FTA * .44))

# Offensive Rebound Rate
nba_data$ORebRate = nba_data$ORB / (nba_data$FGA - nba_data$FG)

# Defensive Rebound Rate
nba_data$DRebRate = nba_data$DRB / (nba_data$Opp_FGA - nba_data$Opp_FG)

# Free Throw Rate
nba_data$FTR = nba_data$FT / nba_data$FGA

# Opp Free Throw Rate
nba_data$OFTR = nba_data$Opp_FT / nba_data$Opp_FGA

# Consolidating NBA Data Table
nba_data = select(nba_data, Team, year, `W/L%`, Conference, MadePlayoffs, EFG, Opp_EFG, TTP, 
                  DTTP, ORebRate, DRebRate, FTR, OFTR)

#Export Data to CSV
write.csv(nba_data, file = "nba_data.csv")


