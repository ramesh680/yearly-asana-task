"""LaLiga clubs (2025-26 season, 20). Source: laliga.com / Wikipedia."""
LALIGA_EDITION = "2025-26 season (20 clubs)"
LALIGA_SOURCE_URL = "https://en.wikipedia.org/wiki/2025%E2%80%9326_La_Liga"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
LALIGA_CLUBS=[
 _t(1,"Real Madrid","Madrid","Santiago Bernabéu","Real_Madrid_CF"),
 _t(2,"Barcelona","Barcelona","Spotify Camp Nou","FC_Barcelona"),
 _t(3,"Atlético Madrid","Madrid","Riyadh Air Metropolitano","Atlético_Madrid"),
 _t(4,"Athletic Bilbao","Bilbao","San Mamés","Athletic_Bilbao"),
 _t(5,"Villarreal","Villarreal","Estadio de la Cerámica","Villarreal_CF"),
 _t(6,"Real Betis","Seville","Benito Villamarín","Real_Betis"),
 _t(7,"Celta Vigo","Vigo","Balaídos","RC_Celta_de_Vigo"),
 _t(8,"Rayo Vallecano","Madrid","Estadio de Vallecas","Rayo_Vallecano"),
 _t(9,"Osasuna","Pamplona","El Sadar","CA_Osasuna"),
 _t(10,"Mallorca","Palma","Mallorca Son Moix","RCD_Mallorca"),
 _t(11,"Real Sociedad","San Sebastián","Reale Arena","Real_Sociedad"),
 _t(12,"Valencia","Valencia","Mestalla","Valencia_CF"),
 _t(13,"Getafe","Getafe","Coliseum","Getafe_CF"),
 _t(14,"Espanyol","Cornellà de Llobregat","RCDE Stadium","RCD_Espanyol"),
 _t(15,"Alavés","Vitoria-Gasteiz","Mendizorroza","Deportivo_Alavés"),
 _t(16,"Sevilla","Seville","Ramón Sánchez-Pizjuán","Sevilla_FC"),
 _t(17,"Girona","Girona","Montilivi","Girona_FC"),
 _t(18,"Levante","Valencia","Ciutat de València","Levante_UD"),
 _t(19,"Elche","Elche","Martínez Valero","Elche_CF"),
 _t(20,"Real Oviedo","Oviedo","Carlos Tartiere","Real_Oviedo"),
]
