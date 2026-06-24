"""NBA teams (30), by conference and division. Source: nba.com / Wikipedia."""
NBA_EDITION = "30 teams (by conference & division)"
NBA_SOURCE_URL = "https://www.nba.com/teams"
W = "https://en.wikipedia.org/wiki/"
def _t(rank,team,conf,div,city,arena,slug,wiki):
    return {"rank":rank,"team":team,"conference":conf,"division":div,"city":city,"arena":arena,
            "website":"https://www.nba.com/%s"%slug,"wikipedia":W+wiki}
NBA_TEAMS=[
 _t(1,"Boston Celtics","Eastern","Atlantic","Boston, MA","TD Garden","celtics","Boston_Celtics"),
 _t(2,"Brooklyn Nets","Eastern","Atlantic","Brooklyn, NY","Barclays Center","nets","Brooklyn_Nets"),
 _t(3,"New York Knicks","Eastern","Atlantic","New York, NY","Madison Square Garden","knicks","New_York_Knicks"),
 _t(4,"Philadelphia 76ers","Eastern","Atlantic","Philadelphia, PA","Wells Fargo Center","sixers","Philadelphia_76ers"),
 _t(5,"Toronto Raptors","Eastern","Atlantic","Toronto, ON","Scotiabank Arena","raptors","Toronto_Raptors"),
 _t(6,"Chicago Bulls","Eastern","Central","Chicago, IL","United Center","bulls","Chicago_Bulls"),
 _t(7,"Cleveland Cavaliers","Eastern","Central","Cleveland, OH","Rocket Arena","cavaliers","Cleveland_Cavaliers"),
 _t(8,"Detroit Pistons","Eastern","Central","Detroit, MI","Little Caesars Arena","pistons","Detroit_Pistons"),
 _t(9,"Indiana Pacers","Eastern","Central","Indianapolis, IN","Gainbridge Fieldhouse","pacers","Indiana_Pacers"),
 _t(10,"Milwaukee Bucks","Eastern","Central","Milwaukee, WI","Fiserv Forum","bucks","Milwaukee_Bucks"),
 _t(11,"Atlanta Hawks","Eastern","Southeast","Atlanta, GA","State Farm Arena","hawks","Atlanta_Hawks"),
 _t(12,"Charlotte Hornets","Eastern","Southeast","Charlotte, NC","Spectrum Center","hornets","Charlotte_Hornets"),
 _t(13,"Miami Heat","Eastern","Southeast","Miami, FL","Kaseya Center","heat","Miami_Heat"),
 _t(14,"Orlando Magic","Eastern","Southeast","Orlando, FL","Kia Center","magic","Orlando_Magic"),
 _t(15,"Washington Wizards","Eastern","Southeast","Washington, D.C.","Capital One Arena","wizards","Washington_Wizards"),
 _t(16,"Denver Nuggets","Western","Northwest","Denver, CO","Ball Arena","nuggets","Denver_Nuggets"),
 _t(17,"Minnesota Timberwolves","Western","Northwest","Minneapolis, MN","Target Center","timberwolves","Minnesota_Timberwolves"),
 _t(18,"Oklahoma City Thunder","Western","Northwest","Oklahoma City, OK","Paycom Center","thunder","Oklahoma_City_Thunder"),
 _t(19,"Portland Trail Blazers","Western","Northwest","Portland, OR","Moda Center","blazers","Portland_Trail_Blazers"),
 _t(20,"Utah Jazz","Western","Northwest","Salt Lake City, UT","Delta Center","jazz","Utah_Jazz"),
 _t(21,"Golden State Warriors","Western","Pacific","San Francisco, CA","Chase Center","warriors","Golden_State_Warriors"),
 _t(22,"LA Clippers","Western","Pacific","Inglewood, CA","Intuit Dome","clippers","Los_Angeles_Clippers"),
 _t(23,"Los Angeles Lakers","Western","Pacific","Los Angeles, CA","Crypto.com Arena","lakers","Los_Angeles_Lakers"),
 _t(24,"Phoenix Suns","Western","Pacific","Phoenix, AZ","PHX Arena","suns","Phoenix_Suns"),
 _t(25,"Sacramento Kings","Western","Pacific","Sacramento, CA","Golden 1 Center","kings","Sacramento_Kings"),
 _t(26,"Dallas Mavericks","Western","Southwest","Dallas, TX","American Airlines Center","mavericks","Dallas_Mavericks"),
 _t(27,"Houston Rockets","Western","Southwest","Houston, TX","Toyota Center","rockets","Houston_Rockets"),
 _t(28,"Memphis Grizzlies","Western","Southwest","Memphis, TN","FedExForum","grizzlies","Memphis_Grizzlies"),
 _t(29,"New Orleans Pelicans","Western","Southwest","New Orleans, LA","Smoothie King Center","pelicans","New_Orleans_Pelicans"),
 _t(30,"San Antonio Spurs","Western","Southwest","San Antonio, TX","Frost Bank Center","spurs","San_Antonio_Spurs"),
]
