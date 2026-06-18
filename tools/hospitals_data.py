"""
Baked-in "best hospital" reference data (United States).

This is the offline fallback used when the live sources can't be reached
(the ranking sites are heavily JS-rendered / protected, so a hosted scrape
will often fail). The data below is the latest published edition as of
build time and is clearly versioned so it can be refreshed each year.

Sources:
- U.S. News & World Report - Best Hospitals 2025-2026 Honor Roll (20 hospitals,
  non-ordinal / alphabetical by state).
  https://health.usnews.com/health-care/best-hospitals/articles/best-hospitals-honor-roll-and-overview
- Newsweek / Statista - World's Best Hospitals 2026, United States ranking.
  https://rankings.newsweek.com/worlds-best-hospitals-2026/united-states
"""

# ---------------------------------------------------------------------------
# U.S. News & World Report - 2025-2026 Best Hospitals Honor Roll
# The Honor Roll is non-ordinal (no 1..20 ranking); listed alphabetically
# by state, then hospital, matching how U.S. News publishes it.
# ---------------------------------------------------------------------------
US_NEWS_EDITION = "2025-2026"
US_NEWS_SOURCE_URL = (
    "https://health.usnews.com/health-care/best-hospitals/articles/"
    "best-hospitals-honor-roll-and-overview"
)

US_NEWS_HONOR_ROLL = [
    {"hospital": "Mayo Clinic-Arizona", "city": "Phoenix", "state": "Arizona"},
    {"hospital": "Cedars-Sinai Medical Center", "city": "Los Angeles", "state": "California"},
    {"hospital": "Stanford Health Care-Stanford Hospital", "city": "Palo Alto", "state": "California"},
    {"hospital": "UCLA Medical Center", "city": "Los Angeles", "state": "California"},
    {"hospital": "UCSF Health-UCSF Medical Center", "city": "San Francisco", "state": "California"},
    {"hospital": "AdventHealth Orlando", "city": "Orlando", "state": "Florida"},
    {"hospital": "Northwestern Medicine-Northwestern Memorial Hospital", "city": "Chicago", "state": "Illinois"},
    {"hospital": "Rush University Medical Center", "city": "Chicago", "state": "Illinois"},
    {"hospital": "Johns Hopkins Hospital", "city": "Baltimore", "state": "Maryland"},
    {"hospital": "Brigham and Women's Hospital", "city": "Boston", "state": "Massachusetts"},
    {"hospital": "Massachusetts General Hospital", "city": "Boston", "state": "Massachusetts"},
    {"hospital": "University of Michigan Health", "city": "Ann Arbor", "state": "Michigan"},
    {"hospital": "Mayo Clinic-Rochester", "city": "Rochester", "state": "Minnesota"},
    {"hospital": "Hackensack University Medical Center at Hackensack Meridian Health", "city": "Hackensack", "state": "New Jersey"},
    {"hospital": "Mount Sinai Hospital", "city": "New York City", "state": "New York"},
    {"hospital": "New York-Presbyterian Hospital-Columbia and Cornell", "city": "New York City", "state": "New York"},
    {"hospital": "NYU Langone Hospitals", "city": "New York City", "state": "New York"},
    {"hospital": "Cleveland Clinic", "city": "Cleveland", "state": "Ohio"},
    {"hospital": "Hospitals of the University of Pennsylvania-Penn Presbyterian", "city": "Philadelphia", "state": "Pennsylvania"},
    {"hospital": "Houston Methodist Hospital", "city": "Houston", "state": "Texas"},
]

# ---------------------------------------------------------------------------
# Newsweek / Statista - World's Best Hospitals 2026, United States (top 50)
# This list IS ordinal (rank + score).
# ---------------------------------------------------------------------------
NEWSWEEK_EDITION = "2026"
NEWSWEEK_SOURCE_URL = "https://rankings.newsweek.com/worlds-best-hospitals-2026/united-states"

NEWSWEEK_US = [
    {"rank": 1, "hospital": "Mayo Clinic - Rochester", "city": "Rochester", "state": "Minnesota", "score": "96.28%"},
    {"rank": 2, "hospital": "Cleveland Clinic", "city": "Cleveland", "state": "Ohio", "score": "92.13%"},
    {"rank": 3, "hospital": "Massachusetts General Hospital", "city": "Boston", "state": "Massachusetts", "score": "91.96%"},
    {"rank": 4, "hospital": "The Johns Hopkins Hospital", "city": "Baltimore", "state": "Maryland", "score": "89.77%"},
    {"rank": 5, "hospital": "Ronald Reagan UCLA Medical Center", "city": "Los Angeles", "state": "California", "score": "89.68%"},
    {"rank": 6, "hospital": "Brigham and Women's Hospital", "city": "Boston", "state": "Massachusetts", "score": "89.64%"},
    {"rank": 7, "hospital": "The Mount Sinai Hospital", "city": "New York City", "state": "New York", "score": "88.37%"},
    {"rank": 8, "hospital": "Stanford Health Care - Stanford Hospital", "city": "Stanford", "state": "California", "score": "88.19%"},
    {"rank": 9, "hospital": "UCSF Medical Center", "city": "San Francisco", "state": "California", "score": "86.77%"},
    {"rank": 10, "hospital": "Cedars-Sinai Medical Center", "city": "Los Angeles", "state": "California", "score": "86.73%"},
    {"rank": 11, "hospital": "Mayo Clinic - Jacksonville", "city": "Jacksonville", "state": "Florida", "score": "86.69%"},
    {"rank": 12, "hospital": "University of Michigan Health - Ann Arbor", "city": "Ann Arbor", "state": "Michigan", "score": "86.59%"},
    {"rank": 13, "hospital": "Northwestern Memorial Hospital", "city": "Chicago", "state": "Illinois", "score": "86.33%"},
    {"rank": 14, "hospital": "Duke University Hospital", "city": "Durham", "state": "North Carolina", "score": "86.13%"},
    {"rank": 15, "hospital": "Hospital of the University of Pennsylvania", "city": "Philadelphia", "state": "Pennsylvania", "score": "85.78%"},
    {"rank": 16, "hospital": "Mayo Clinic - Phoenix", "city": "Phoenix", "state": "Arizona", "score": "84.71%"},
    {"rank": 17, "hospital": "NewYork-Presbyterian Columbia University Irving Medical Center", "city": "New York City", "state": "New York", "score": "84.22%"},
    {"rank": 18, "hospital": "Houston Methodist Hospital", "city": "Houston", "state": "Texas", "score": "84.21%"},
    {"rank": 19, "hospital": "NYU Langone Hospitals - Tisch Hospital", "city": "New York City", "state": "New York", "score": "83.14%"},
    {"rank": 20, "hospital": "Beth Israel Deaconess Medical Center", "city": "Boston", "state": "Massachusetts", "score": "81.65%"},
    {"rank": 21, "hospital": "Vanderbilt University Medical Center", "city": "Nashville", "state": "Tennessee", "score": "81.19%"},
    {"rank": 22, "hospital": "Rush University Medical Center", "city": "Chicago", "state": "Illinois", "score": "80.73%"},
    {"rank": 23, "hospital": "University of Chicago Medical Center", "city": "Chicago", "state": "Illinois", "score": "80.23%"},
    {"rank": 24, "hospital": "UCLA Health - Santa Monica Medical Center", "city": "Santa Monica", "state": "California", "score": "79.69%"},
    {"rank": 25, "hospital": "Yale New Haven Hospital", "city": "New Haven", "state": "Connecticut", "score": "79.03%"},
    {"rank": 26, "hospital": "NewYork-Presbyterian Weill Cornell Medical Center", "city": "New York City", "state": "New York", "score": "78.55%"},
    {"rank": 27, "hospital": "Barnes-Jewish Hospital", "city": "St. Louis", "state": "Missouri", "score": "78.09%"},
    {"rank": 28, "hospital": "Johns Hopkins Bayview Medical Center", "city": "Baltimore", "state": "Maryland", "score": "76.83%"},
    {"rank": 29, "hospital": "Emory University Hospital", "city": "Atlanta", "state": "Georgia", "score": "76.64%"},
    {"rank": 30, "hospital": "Keck Hospital of USC", "city": "Los Angeles", "state": "California", "score": "76.53%"},
    {"rank": 31, "hospital": "UW Health - University Hospital", "city": "Madison", "state": "Wisconsin", "score": "74.90%"},
    {"rank": 32, "hospital": "University of Washington Medical Center", "city": "Seattle", "state": "Washington", "score": "73.46%"},
    {"rank": 33, "hospital": "Jacobs Medical Center at UC San Diego Health", "city": "San Diego", "state": "California", "score": "73.21%"},
    {"rank": 34, "hospital": "Virginia Mason Medical Center", "city": "Seattle", "state": "Washington", "score": "72.92%"},
    {"rank": 35, "hospital": "University of California Davis Medical Center", "city": "Sacramento", "state": "California", "score": "72.72%"},
    {"rank": 36, "hospital": "Cleveland Clinic - Fairview Hospital", "city": "Cleveland", "state": "Ohio", "score": "72.30%"},
    {"rank": 37, "hospital": "Ohio State University - Wexner Medical Center", "city": "Columbus", "state": "Ohio", "score": "72.18%"},
    {"rank": 38, "hospital": "UT Southwestern Medical Center", "city": "Dallas", "state": "Texas", "score": "72.17%"},
    {"rank": 39, "hospital": "Thomas Jefferson University Hospital", "city": "Philadelphia", "state": "Pennsylvania", "score": "72.16%"},
    {"rank": 40, "hospital": "Cleveland Clinic Weston Hospital", "city": "Weston", "state": "Florida", "score": "72.13%"},
    {"rank": 41, "hospital": "Brigham and Women's Faulkner Hospital", "city": "Boston", "state": "Massachusetts", "score": "71.94%"},
    {"rank": 42, "hospital": "University of Kansas Hospital", "city": "Kansas City", "state": "Kansas", "score": "71.77%"},
    {"rank": 43, "hospital": "UCHealth University of Colorado Hospital", "city": "Aurora", "state": "Colorado", "score": "71.71%"},
    {"rank": 44, "hospital": "University Hospitals Cleveland Medical Center", "city": "Cleveland", "state": "Ohio", "score": "71.65%"},
    {"rank": 45, "hospital": "Scripps Memorial Hospital La Jolla", "city": "La Jolla", "state": "California", "score": "71.63%"},
    {"rank": 46, "hospital": "Baylor St. Luke's Medical Center", "city": "Houston", "state": "Texas", "score": "71.33%"},
    {"rank": 47, "hospital": "University of Utah Hospital", "city": "Salt Lake City", "state": "Utah", "score": "71.23%"},
    {"rank": 48, "hospital": "Penn State Health - Milton S. Hershey Medical Center", "city": "Hershey", "state": "Pennsylvania", "score": "71.14%"},
    {"rank": 49, "hospital": "Tufts Medical Center", "city": "Boston", "state": "Massachusetts", "score": "71.07%"},
    {"rank": 50, "hospital": "Torrance Memorial Medical Center", "city": "Torrance", "state": "California", "score": "71.04%"},
]
