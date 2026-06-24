"""MLS teams (30), by conference. Source: mlssoccer.com / Wikipedia."""
MLS_EDITION = "30 clubs (by conference)"
MLS_SOURCE_URL = "https://www.mlssoccer.com/"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,conf,city,stadium,wiki):
    return {"rank":rank,"team":team,"conference":conf,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
MLS_TEAMS=[
 _t(1,"Atlanta United FC","Eastern","Atlanta, GA","Mercedes-Benz Stadium","Atlanta_United_FC"),
 _t(2,"CF Montréal","Eastern","Montreal, QC","Saputo Stadium","CF_Montréal"),
 _t(3,"Charlotte FC","Eastern","Charlotte, NC","Bank of America Stadium","Charlotte_FC"),
 _t(4,"Chicago Fire FC","Eastern","Chicago, IL","Soldier Field","Chicago_Fire_FC"),
 _t(5,"FC Cincinnati","Eastern","Cincinnati, OH","TQL Stadium","FC_Cincinnati"),
 _t(6,"Columbus Crew","Eastern","Columbus, OH","Lower.com Field","Columbus_Crew"),
 _t(7,"D.C. United","Eastern","Washington, D.C.","Audi Field","D.C._United"),
 _t(8,"Inter Miami CF","Eastern","Fort Lauderdale, FL","Chase Stadium","Inter_Miami_CF"),
 _t(9,"Nashville SC","Eastern","Nashville, TN","Geodis Park","Nashville_SC"),
 _t(10,"New England Revolution","Eastern","Foxborough, MA","Gillette Stadium","New_England_Revolution"),
 _t(11,"New York City FC","Eastern","New York, NY","Yankee Stadium","New_York_City_FC"),
 _t(12,"New York Red Bulls","Eastern","Harrison, NJ","Sports Illustrated Stadium","New_York_Red_Bulls"),
 _t(13,"Orlando City SC","Eastern","Orlando, FL","Inter&Co Stadium","Orlando_City_SC"),
 _t(14,"Philadelphia Union","Eastern","Chester, PA","Subaru Park","Philadelphia_Union"),
 _t(15,"Toronto FC","Eastern","Toronto, ON","BMO Field","Toronto_FC"),
 _t(16,"Austin FC","Western","Austin, TX","Q2 Stadium","Austin_FC"),
 _t(17,"Colorado Rapids","Western","Commerce City, CO","Dick's Sporting Goods Park","Colorado_Rapids"),
 _t(18,"FC Dallas","Western","Frisco, TX","Toyota Stadium","FC_Dallas"),
 _t(19,"Houston Dynamo FC","Western","Houston, TX","Shell Energy Stadium","Houston_Dynamo_FC"),
 _t(20,"LA Galaxy","Western","Carson, CA","Dignity Health Sports Park","LA_Galaxy"),
 _t(21,"Los Angeles FC","Western","Los Angeles, CA","BMO Stadium","Los_Angeles_FC"),
 _t(22,"Minnesota United FC","Western","Saint Paul, MN","Allianz Field","Minnesota_United_FC"),
 _t(23,"Portland Timbers","Western","Portland, OR","Providence Park","Portland_Timbers"),
 _t(24,"Real Salt Lake","Western","Sandy, UT","America First Field","Real_Salt_Lake"),
 _t(25,"San Diego FC","Western","San Diego, CA","Snapdragon Stadium","San_Diego_FC"),
 _t(26,"San Jose Earthquakes","Western","San Jose, CA","PayPal Park","San_Jose_Earthquakes"),
 _t(27,"Seattle Sounders FC","Western","Seattle, WA","Lumen Field","Seattle_Sounders_FC"),
 _t(28,"Sporting Kansas City","Western","Kansas City, KS","Children's Mercy Park","Sporting_Kansas_City"),
 _t(29,"St. Louis City SC","Western","St. Louis, MO","Energizer Park","St._Louis_City_SC"),
 _t(30,"Vancouver Whitecaps FC","Western","Vancouver, BC","BC Place","Vancouver_Whitecaps_FC"),
]
