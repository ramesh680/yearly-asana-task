"""Ligue 1 clubs (2025-26 season, 18). Source: ligue1.com / Wikipedia."""
LIGUE1_EDITION = "2025-26 season (18 clubs)"
LIGUE1_SOURCE_URL = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Ligue_1"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
LIGUE1_CLUBS=[
 _t(1,"Paris Saint-Germain","Paris","Parc des Princes","Paris_Saint-Germain_F.C."),
 _t(2,"Olympique de Marseille","Marseille","Stade Vélodrome","Olympique_de_Marseille"),
 _t(3,"AS Monaco","Monaco","Stade Louis II","AS_Monaco_FC"),
 _t(4,"OGC Nice","Nice","Allianz Riviera","OGC_Nice"),
 _t(5,"Lille OSC","Lille","Stade Pierre-Mauroy","Lille_OSC"),
 _t(6,"Olympique Lyonnais","Lyon","Groupama Stadium","Olympique_Lyonnais"),
 _t(7,"RC Lens","Lens","Stade Bollaert-Delelis","RC_Lens"),
 _t(8,"Stade Brestois 29","Brest","Stade Francis-Le Blé","Stade_Brestois_29"),
 _t(9,"RC Strasbourg Alsace","Strasbourg","Stade de la Meinau","RC_Strasbourg_Alsace"),
 _t(10,"Toulouse FC","Toulouse","Stadium de Toulouse","Toulouse_FC"),
 _t(11,"AJ Auxerre","Auxerre","Stade de l'Abbé-Deschamps","AJ_Auxerre"),
 _t(12,"Stade Rennais FC","Rennes","Roazhon Park","Stade_Rennais_F.C."),
 _t(13,"FC Nantes","Nantes","Stade de la Beaujoire","FC_Nantes"),
 _t(14,"Angers SCO","Angers","Stade Raymond Kopa","Angers_SCO"),
 _t(15,"Le Havre AC","Le Havre","Stade Océane","Le_Havre_AC"),
 _t(16,"FC Lorient","Lorient","Stade du Moustoir","FC_Lorient"),
 _t(17,"Paris FC","Paris","Stade Jean-Bouin","Paris_FC"),
 _t(18,"FC Metz","Metz","Stade Saint-Symphorien","FC_Metz"),
]
