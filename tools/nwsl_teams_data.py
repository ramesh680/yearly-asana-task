"""NWSL teams, with city and stadium. Source: nwslsoccer.com / Wikipedia."""
NWSL_EDITION = "Clubs (2025 season)"
NWSL_SOURCE_URL = "https://www.nwslsoccer.com/"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
NWSL_TEAMS=[
 _t(1,"Angel City FC","Los Angeles, CA","BMO Stadium","Angel_City_FC"),
 _t(2,"Bay FC","San Jose, CA","PayPal Park","Bay_FC"),
 _t(3,"Chicago Stars FC","Bridgeview, IL","SeatGeek Stadium","Chicago_Stars_FC"),
 _t(4,"Houston Dash","Houston, TX","Shell Energy Stadium","Houston_Dash"),
 _t(5,"Kansas City Current","Kansas City, MO","CPKC Stadium","Kansas_City_Current"),
 _t(6,"NJ/NY Gotham FC","Harrison, NJ","Sports Illustrated Stadium","NJ/NY_Gotham_FC"),
 _t(7,"North Carolina Courage","Cary, NC","WakeMed Soccer Park","North_Carolina_Courage"),
 _t(8,"Orlando Pride","Orlando, FL","Inter&Co Stadium","Orlando_Pride"),
 _t(9,"Portland Thorns FC","Portland, OR","Providence Park","Portland_Thorns_FC"),
 _t(10,"Racing Louisville FC","Louisville, KY","Lynn Family Stadium","Racing_Louisville_FC"),
 _t(11,"San Diego Wave FC","San Diego, CA","Snapdragon Stadium","San_Diego_Wave_FC"),
 _t(12,"Seattle Reign FC","Seattle, WA","Lumen Field","Seattle_Reign_FC"),
 _t(13,"Utah Royals FC","Sandy, UT","America First Field","Utah_Royals_FC"),
 _t(14,"Washington Spirit","Washington, D.C.","Audi Field","Washington_Spirit"),
]
