"""Combat sports with international governing body. Source: Wikipedia (Combat sport)."""
COMBAT_EDITION = "Major combat sports & disciplines"
COMBAT_SOURCE_URL = "https://en.wikipedia.org/wiki/Combat_sport"
W="https://en.wikipedia.org/wiki/"
def _t(rank,sport,body,website,wiki):
    return {"rank":rank,"sport":sport,"governing_body":body,"website":website,"wikipedia":W+wiki}
COMBAT_SPORTS=[
 _t(1,"Boxing","World Boxing / WBA, WBC, IBF, WBO","","Boxing"),
 _t(2,"Mixed martial arts (MMA)","IMMAF / UFC (promotion)","https://www.immaf.org/","Mixed_martial_arts"),
 _t(3,"Wrestling","United World Wrestling (UWW)","https://uww.org/","Wrestling"),
 _t(4,"Judo","International Judo Federation (IJF)","https://www.ijf.org/","Judo"),
 _t(5,"Karate","World Karate Federation (WKF)","https://www.wkf.net/","Karate"),
 _t(6,"Taekwondo","World Taekwondo (WT)","https://www.worldtaekwondo.org/","Taekwondo"),
 _t(7,"Brazilian jiu-jitsu","IBJJF","https://ibjjf.com/","Brazilian_jiu-jitsu"),
 _t(8,"Muay Thai","IFMA","https://muaythai.sport/","Muay_Thai"),
 _t(9,"Kickboxing","WAKO","https://wako.sport/","Kickboxing"),
 _t(10,"Fencing","International Fencing Federation (FIE)","https://fie.org/","Fencing"),
 _t(11,"Sumo","International Sumo Federation (IFS)","","Sumo"),
 _t(12,"Wushu (sanda)","International Wushu Federation (IWUF)","https://www.iwuf.org/","Wushu_(sport)"),
 _t(13,"Sambo","International Sambo Federation (FIAS)","https://sambo.sport/","Sambo_(martial_art)"),
 _t(14,"Kendo","International Kendo Federation (FIK)","","Kendo"),
 _t(15,"Savate","International Savate Federation (FISav)","","Savate"),
 _t(16,"Jujutsu","Ju-Jitsu International Federation (JJIF)","https://jjif.org/","Jujutsu"),
 _t(17,"Aikido","Aikikai Foundation","","Aikido"),
 _t(18,"Capoeira","","","Capoeira"),
 _t(19,"Krav Maga","","","Krav_Maga"),
 _t(20,"Lethwei","","","Lethwei"),
 _t(21,"Pankration","","","Pankration"),
 _t(22,"Catch wrestling","","","Catch_wrestling"),
]
