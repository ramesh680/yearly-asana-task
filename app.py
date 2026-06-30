from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# TOOLS Dictionary with all categories
TOOLS = [
    # Healthcare
    {
        "title": "Best Hospitals (US)",
        "category": "Healthcare",
        "description": "Pulls the latest U.S. best-hospital lists from U.S. News & World Report and Newsweek/Statista, with each hospital's official website and social handles.",
        "endpoint": "best_hospitals",
        "available": True,
        "count": 5000
    },

    # Education
    {
        "title": "Best Colleges (US)",
        "category": "Education",
        "description": "U.S. News Best National Universities (Top 100, 2026), with each school's official website and social handles.",
        "endpoint": "best_colleges",
        "available": True,
        "count": 2500
    },

    # Finance
    {
        "title": "Russell 3000",
        "category": "Finance",
        "description": "All Russell 3000 constituents ranked by index weight with official data.",
        "endpoint": "russell_3000",
        "available": True,
        "count": 3000
    },
    {
        "title": "S&P 500",
        "category": "Finance",
        "description": "Standard & Poor's 500 index companies with detailed financial metrics and social handles.",
        "endpoint": "sp_500",
        "available": True,
        "count": 500
    },

    # Sports - Golf
    {
        "title": "Golf Brand Discovery",
        "category": "Sports",
        "description": "Golf tournaments, players, and brands with official data and social handles.",
        "endpoint": "golf_brand_discovery",
        "available": True,
        "count": 2000
    },

    # Sports - Basketball
    {
        "title": "National Basketball Association",
        "category": "Sports",
        "description": "NBA teams with rosters, statistics, and social handles.",
        "endpoint": "nba",
        "available": True,
        "count": 450
    },

    # Sports - Ice Hockey
    {
        "title": "National Hockey League",
        "category": "Sports",
        "description": "NHL teams, rosters, and statistics.",
        "endpoint": "nhl",
        "available": True,
        "count": 700
    },

    # Sports - Soccer (MLS)
    {
        "title": "Major League Soccer",
        "category": "Sports",
        "description": "MLS teams with rosters and statistics.",
        "endpoint": "mls",
        "available": True,
        "count": 360
    },

    # Sports - Soccer (NWSL)
    {
        "title": "National Women's Soccer League",
        "category": "Sports",
        "description": "NWSL teams and player data.",
        "endpoint": "nwsl",
        "available": True,
        "count": 240
    },

    # Sports - Baseball (MLB)
    {
        "title": "Major League Baseball",
        "category": "Sports",
        "description": "MLB teams, rosters, and statistics.",
        "endpoint": "mlb",
        "available": True,
        "count": 1200
    },

    # Sports - Baseball (Minor Leagues)
    {
        "title": "Minor League Baseball",
        "category": "Sports",
        "description": "Minor league teams and player data.",
        "endpoint": "minor_league_baseball",
        "available": True,
        "count": 2500
    },

    # Sports - Soccer (Brasileirão)
    {
        "title": "Brasileiro Serie A",
        "category": "Sports",
        "description": "Brazilian top division teams and data.",
        "endpoint": "brasileiro_serie_a",
        "available": True,
        "count": 480
    },

    # Sports - Soccer (Bundesliga)
    {
        "title": "Bundesliga",
        "category": "Sports",
        "description": "German Bundesliga teams and statistics.",
        "endpoint": "bundesliga",
        "available": True,
        "count": 550
    },

    # Sports - Soccer (LaLiga)
    {
        "title": "LaLiga",
        "category": "Sports",
        "description": "Spanish LaLiga teams and player data.",
        "endpoint": "laliga",
        "available": True,
        "count": 600
    },

    # Sports - Soccer (Ligue 1)
    {
        "title": "Ligue 1",
        "category": "Sports",
        "description": "French Ligue 1 teams and player data.",
        "endpoint": "ligue_1",
        "available": True,
        "count": 480
    },

    # Sports - Soccer (Serie A)
    {
        "title": "Serie A",
        "category": "Sports",
        "description": "Italian Serie A teams and statistics.",
        "endpoint": "serie_a",
        "available": True,
        "count": 500
    },

    # Sports - Combat Sports
    {
        "title": "Combat Sports",
        "category": "Sports",
        "description": "Boxing, MMA, and wrestling data.",
        "endpoint": "combat_sports",
        "available": True,
        "count": 3000
    },

    # Sports - Sporting Events Brand Discovery
    {
        "title": "Sporting Events Brand Discovery",
        "category": "Sports",
        "description": "Major sports events and tournaments worldwide with brand data.",
        "endpoint": "sporting_events_brand_discovery",
        "available": True,
        "count": 1500
    },

    # Sports - Sports Leagues by Revenue
    {
        "title": "Sports Leagues by Revenue",
        "category": "Sports",
        "description": "Global sports leagues ranked by revenue and market value.",
        "endpoint": "sports_leagues_revenue",
        "available": True,
        "count": 150
    },

    # Streaming
    {
        "title": "Streaming Services Brand Discovery",
        "category": "Streaming",
        "description": "Major streaming platforms with subscription data and content libraries.",
        "endpoint": "streaming_services_brand_discovery",
        "available": True,
        "count": 5000
    },
    {
        "title": "Top Twitch Streamers",
        "category": "Streaming",
        "description": "The top channels from TwitchTracker's rankings with viewership data.",
        "endpoint": "twitch_streamers",
        "available": True,
        "count": 10000
    },

    # Video Games
    {
        "title": "Video Game Franchises Brand Discovery",
        "category": "Streaming",
        "description": "Major video game franchises and their data.",
        "endpoint": "video_game_franchises_brand_discovery",
        "available": True,
        "count": 3500
    },
    {
        "title": "Video Game Platforms Brand Discovery",
        "category": "Streaming",
        "description": "Gaming platforms, consoles, and their specifications.",
        "endpoint": "video_game_platforms_brand_discovery",
        "available": True,
        "count": 150
    },
    {
        "title": "Video Game Publishers Brand Discovery",
        "category": "Streaming",
        "description": "Major video game publishers and studios worldwide.",
        "endpoint": "video_game_publishers_brand_discovery",
        "available": True,
        "count": 2000
    },

    # Consumer Packaged Goods
    {
        "title": "CPG Brand Search",
        "category": "Finance",
        "description": "Consumer packaged goods brands with market data and social handles.",
        "endpoint": "cpg_brand_search",
        "available": True,
        "count": 8000
    },
]

@app.route("/")
def index():
    """Home page displaying all tools"""
    app_name = "Yearly Asana task"
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("index.html", app_name=app_name, tools=TOOLS, today=today)

@app.route("/best_hospitals")
def best_hospitals():
    """Best Hospitals page"""
    return render_template("best_hospitals.html")

@app.route("/best_colleges")
def best_colleges():
    """Best Colleges page"""
    return render_template("best_colleges.html")

@app.route("/russell_3000")
def russell_3000():
    """Russell 3000 page"""
    return render_template("russell_3000.html")

@app.route("/sp_500")
def sp_500():
    """S&P 500 page"""
    return render_template("sp_500.html")

@app.route("/golf_brand_discovery")
def golf_brand_discovery():
    """Golf Brand Discovery page"""
    return render_template("golf_brand_discovery.html")

@app.route("/nba")
def nba():
    """NBA page"""
    return render_template("nba.html")

@app.route("/nhl")
def nhl():
    """NHL page"""
    return render_template("nhl.html")

@app.route("/mls")
def mls():
    """MLS page"""
    return render_template("mls.html")

@app.route("/nwsl")
def nwsl():
    """NWSL page"""
    return render_template("nwsl.html")

@app.route("/mlb")
def mlb():
    """MLB page"""
    return render_template("mlb.html")

@app.route("/minor_league_baseball")
def minor_league_baseball():
    """Minor League Baseball page"""
    return render_template("minor_league_baseball.html")

@app.route("/brasileiro_serie_a")
def brasileiro_serie_a():
    """Brasileirão Série A page"""
    return render_template("brasileiro_serie_a.html")

@app.route("/bundesliga")
def bundesliga():
    """Bundesliga page"""
    return render_template("bundesliga.html")

@app.route("/laliga")
def laliga():
    """LaLiga page"""
    return render_template("laliga.html")

@app.route("/ligue_1")
def ligue_1():
    """Ligue 1 page"""
    return render_template("ligue_1.html")

@app.route("/serie_a")
def serie_a():
    """Serie A page"""
    return render_template("serie_a.html")

@app.route("/combat_sports")
def combat_sports():
    """Combat Sports page"""
    return render_template("combat_sports.html")

@app.route("/sporting_events_brand_discovery")
def sporting_events_brand_discovery():
    """Sporting Events Brand Discovery page"""
    return render_template("sporting_events_brand_discovery.html")

@app.route("/sports_leagues_revenue")
def sports_leagues_revenue():
    """Sports Leagues by Revenue page"""
    return render_template("sports_leagues_revenue.html")

@app.route("/streaming_services_brand_discovery")
def streaming_services_brand_discovery():
    """Streaming Services Brand Discovery page"""
    return render_template("streaming_services_brand_discovery.html")

@app.route("/twitch_streamers")
def twitch_streamers():
    """Twitch Streamers page"""
    return render_template("twitch_streamers.html")

@app.route("/video_game_franchises_brand_discovery")
def video_game_franchises_brand_discovery():
    """Video Game Franchises Brand Discovery page"""
    return render_template("video_game_franchises_brand_discovery.html")

@app.route("/video_game_platforms_brand_discovery")
def video_game_platforms_brand_discovery():
    """Video Game Platforms Brand Discovery page"""
    return render_template("video_game_platforms_brand_discovery.html")

@app.route("/video_game_publishers_brand_discovery")
def video_game_publishers_brand_discovery():
    """Video Game Publishers Brand Discovery page"""
    return render_template("video_game_publishers_brand_discovery.html")

@app.route("/cpg_brand_search")
def cpg_brand_search():
    """CPG Brand Search page"""
    return render_template("cpg_brand_search.html")

if __name__ == "__main__":
    app.run(debug=True)
