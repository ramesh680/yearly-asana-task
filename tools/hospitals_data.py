"""
Baked-in best-hospital reference data (United States), with official websites.

Versioned yearly snapshot served by the app (the ranking sites are JS-rendered,
so a hosted scrape is unreliable). Refresh by editing this file each year.

Sources:
- U.S. News & World Report - Best Hospitals 2025-2026 Honor Roll (non-ordinal).
  https://health.usnews.com/health-care/best-hospitals/articles/best-hospitals-honor-roll-and-overview
- Newsweek / Statista - World's Best Hospitals 2026, United States.
  https://rankings.newsweek.com/worlds-best-hospitals-2026/united-states
"""

US_NEWS_EDITION = "2025-2026"
US_NEWS_SOURCE_URL = (
    "https://health.usnews.com/health-care/best-hospitals/articles/"
    "best-hospitals-honor-roll-and-overview"
)

US_NEWS_HONOR_ROLL = [
    {"hospital": "Mayo Clinic-Arizona", "city": "Phoenix", "state": "Arizona", "website": "https://www.mayoclinic.org/"},
    {"hospital": "Cedars-Sinai Medical Center", "city": "Los Angeles", "state": "California", "website": "https://www.cedars-sinai.org/"},
    {"hospital": "Stanford Health Care-Stanford Hospital", "city": "Palo Alto", "state": "California", "website": "https://www.stanfordhealthcare.org/"},
    {"hospital": "UCLA Medical Center", "city": "Los Angeles", "state": "California", "website": "https://www.uclahealth.org/"},
    {"hospital": "UCSF Health-UCSF Medical Center", "city": "San Francisco", "state": "California", "website": "https://www.ucsfhealth.org/"},
    {"hospital": "AdventHealth Orlando", "city": "Orlando", "state": "Florida", "website": "https://www.adventhealth.com/"},
    {"hospital": "Northwestern Medicine-Northwestern Memorial Hospital", "city": "Chicago", "state": "Illinois", "website": "https://www.nm.org/"},
    {"hospital": "Rush University Medical Center", "city": "Chicago", "state": "Illinois", "website": "https://www.rush.edu/"},
    {"hospital": "Johns Hopkins Hospital", "city": "Baltimore", "state": "Maryland", "website": "https://www.hopkinsmedicine.org/"},
    {"hospital": "Brigham and Women's Hospital", "city": "Boston", "state": "Massachusetts", "website": "https://www.brighamandwomens.org/"},
    {"hospital": "Massachusetts General Hospital", "city": "Boston", "state": "Massachusetts", "website": "https://www.massgeneral.org/"},
    {"hospital": "University of Michigan Health", "city": "Ann Arbor", "state": "Michigan", "website": "https://www.uofmhealth.org/"},
    {"hospital": "Mayo Clinic-Rochester", "city": "Rochester", "state": "Minnesota", "website": "https://www.mayoclinic.org/"},
    {"hospital": "Hackensack University Medical Center at Hackensack Meridian Health", "city": "Hackensack", "state": "New Jersey", "website": "https://www.hackensackmeridianhealth.org/"},
    {"hospital": "Mount Sinai Hospital", "city": "New York City", "state": "New York", "website": "https://www.mountsinai.org/"},
    {"hospital": "New York-Presbyterian Hospital-Columbia and Cornell", "city": "New York City", "state": "New York", "website": "https://www.nyp.org/"},
    {"hospital": "NYU Langone Hospitals", "city": "New York City", "state": "New York", "website": "https://www.nyulangone.org/"},
    {"hospital": "Cleveland Clinic", "city": "Cleveland", "state": "Ohio", "website": "https://my.clevelandclinic.org/"},
    {"hospital": "Hospitals of the University of Pennsylvania-Penn Presbyterian", "city": "Philadelphia", "state": "Pennsylvania", "website": "https://www.pennmedicine.org/"},
    {"hospital": "Houston Methodist Hospital", "city": "Houston", "state": "Texas", "website": "https://www.houstonmethodist.org/"},
]

NEWSWEEK_EDITION = "2026"
NEWSWEEK_SOURCE_URL = "https://rankings.newsweek.com/worlds-best-hospitals-2026/united-states"

NEWSWEEK_US = [
    {"rank": 1, "hospital": "Mayo Clinic - Rochester", "city": "Rochester", "state": "Minnesota", "score": "96.28%", "website": "https://www.mayoclinic.org/"},
    {"rank": 2, "hospital": "Cleveland Clinic", "city": "Cleveland", "state": "Ohio", "score": "92.13%", "website": "https://my.clevelandclinic.org/"},
    {"rank": 3, "hospital": "Massachusetts General Hospital", "city": "Boston", "state": "Massachusetts", "score": "91.96%", "website": "https://www.massgeneral.org/"},
    {"rank": 4, "hospital": "The Johns Hopkins Hospital", "city": "Baltimore", "state": "Maryland", "score": "89.77%", "website": "https://www.hopkinsmedicine.org/"},
    {"rank": 5, "hospital": "Ronald Reagan UCLA Medical Center", "city": "Los Angeles", "state": "California", "score": "89.68%", "website": "https://www.uclahealth.org/"},
    {"rank": 6, "hospital": "Brigham and Women's Hospital", "city": "Boston", "state": "Massachusetts", "score": "89.64%", "website": "https://www.brighamandwomens.org/"},
    {"rank": 7, "hospital": "The Mount Sinai Hospital", "city": "New York City", "state": "New York", "score": "88.37%", "website": "https://www.mountsinai.org/"},
    {"rank": 8, "hospital": "Stanford Health Care - Stanford Hospital", "city": "Stanford", "state": "California", "score": "88.19%", "website": "https://www.stanfordhealthcare.org/"},
    {"rank": 9, "hospital": "UCSF Medical Center", "city": "San Francisco", "state": "California", "score": "86.77%", "website": "https://www.ucsfhealth.org/"},
    {"rank": 10, "hospital": "Cedars-Sinai Medical Center", "city": "Los Angeles", "state": "California", "score": "86.73%", "website": "https://www.cedars-sinai.org/"},
    {"rank": 11, "hospital": "Mayo Clinic - Jacksonville", "city": "Jacksonville", "state": "Florida", "score": "86.69%", "website": "https://www.mayoclinic.org/"},
    {"rank": 12, "hospital": "University of Michigan Health - Ann Arbor", "city": "Ann Arbor", "state": "Michigan", "score": "86.59%", "website": "https://www.uofmhealth.org/"},
    {"rank": 13, "hospital": "Northwestern Memorial Hospital", "city": "Chicago", "state": "Illinois", "score": "86.33%", "website": "https://www.nm.org/"},
    {"rank": 14, "hospital": "Duke University Hospital", "city": "Durham", "state": "North Carolina", "score": "86.13%", "website": "https://www.dukehealth.org/"},
    {"rank": 15, "hospital": "Hospital of the University of Pennsylvania", "city": "Philadelphia", "state": "Pennsylvania", "score": "85.78%", "website": "https://www.pennmedicine.org/"},
    {"rank": 16, "hospital": "Mayo Clinic - Phoenix", "city": "Phoenix", "state": "Arizona", "score": "84.71%", "website": "https://www.mayoclinic.org/"},
    {"rank": 17, "hospital": "NewYork-Presbyterian Columbia University Irving Medical Center", "city": "New York City", "state": "New York", "score": "84.22%", "website": "https://www.nyp.org/"},
    {"rank": 18, "hospital": "Houston Methodist Hospital", "city": "Houston", "state": "Texas", "score": "84.21%", "website": "https://www.houstonmethodist.org/"},
    {"rank": 19, "hospital": "NYU Langone Hospitals - Tisch Hospital", "city": "New York City", "state": "New York", "score": "83.14%", "website": "https://www.nyulangone.org/"},
    {"rank": 20, "hospital": "Beth Israel Deaconess Medical Center", "city": "Boston", "state": "Massachusetts", "score": "81.65%", "website": "https://www.bidmc.org/"},
    {"rank": 21, "hospital": "Vanderbilt University Medical Center", "city": "Nashville", "state": "Tennessee", "score": "81.19%", "website": "https://www.vanderbilthealth.com/"},
    {"rank": 22, "hospital": "Rush University Medical Center", "city": "Chicago", "state": "Illinois", "score": "80.73%", "website": "https://www.rush.edu/"},
    {"rank": 23, "hospital": "University of Chicago Medical Center", "city": "Chicago", "state": "Illinois", "score": "80.23%", "website": "https://www.uchicagomedicine.org/"},
    {"rank": 24, "hospital": "UCLA Health - Santa Monica Medical Center", "city": "Santa Monica", "state": "California", "score": "79.69%", "website": "https://www.uclahealth.org/"},
    {"rank": 25, "hospital": "Yale New Haven Hospital", "city": "New Haven", "state": "Connecticut", "score": "79.03%", "website": "https://www.ynhh.org/"},
    {"rank": 26, "hospital": "NewYork-Presbyterian Weill Cornell Medical Center", "city": "New York City", "state": "New York", "score": "78.55%", "website": "https://www.nyp.org/"},
    {"rank": 27, "hospital": "Barnes-Jewish Hospital", "city": "St. Louis", "state": "Missouri", "score": "78.09%", "website": "https://www.barnesjewish.org/"},
    {"rank": 28, "hospital": "Johns Hopkins Bayview Medical Center", "city": "Baltimore", "state": "Maryland", "score": "76.83%", "website": "https://www.hopkinsmedicine.org/"},
    {"rank": 29, "hospital": "Emory University Hospital", "city": "Atlanta", "state": "Georgia", "score": "76.64%", "website": "https://www.emoryhealthcare.org/"},
    {"rank": 30, "hospital": "Keck Hospital of USC", "city": "Los Angeles", "state": "California", "score": "76.53%", "website": "https://www.keckmedicine.org/"},
    {"rank": 31, "hospital": "UW Health - University Hospital", "city": "Madison", "state": "Wisconsin", "score": "74.90%", "website": "https://www.uwhealth.org/"},
    {"rank": 32, "hospital": "University of Washington Medical Center", "city": "Seattle", "state": "Washington", "score": "73.46%", "website": "https://www.uwmedicine.org/"},
    {"rank": 33, "hospital": "Jacobs Medical Center at UC San Diego Health", "city": "San Diego", "state": "California", "score": "73.21%", "website": "https://health.ucsd.edu/"},
    {"rank": 34, "hospital": "Virginia Mason Medical Center", "city": "Seattle", "state": "Washington", "score": "72.92%", "website": "https://www.vmfh.org/"},
    {"rank": 35, "hospital": "University of California Davis Medical Center", "city": "Sacramento", "state": "California", "score": "72.72%", "website": "https://www.health.ucdavis.edu/"},
    {"rank": 36, "hospital": "Cleveland Clinic - Fairview Hospital", "city": "Cleveland", "state": "Ohio", "score": "72.30%", "website": "https://my.clevelandclinic.org/"},
    {"rank": 37, "hospital": "Ohio State University - Wexner Medical Center", "city": "Columbus", "state": "Ohio", "score": "72.18%", "website": "https://www.wexnermedical.osu.edu/"},
    {"rank": 38, "hospital": "UT Southwestern Medical Center", "city": "Dallas", "state": "Texas", "score": "72.17%", "website": "https://www.utsouthwestern.edu/"},
    {"rank": 39, "hospital": "Thomas Jefferson University Hospital", "city": "Philadelphia", "state": "Pennsylvania", "score": "72.16%", "website": "https://www.jeffersonhealth.org/"},
    {"rank": 40, "hospital": "Cleveland Clinic Weston Hospital", "city": "Weston", "state": "Florida", "score": "72.13%", "website": "https://my.clevelandclinic.org/"},
    {"rank": 41, "hospital": "Brigham and Women's Faulkner Hospital", "city": "Boston", "state": "Massachusetts", "score": "71.94%", "website": "https://www.brighamandwomensfaulkner.org/"},
    {"rank": 42, "hospital": "University of Kansas Hospital", "city": "Kansas City", "state": "Kansas", "score": "71.77%", "website": "https://www.kansashealthsystem.com/"},
    {"rank": 43, "hospital": "UCHealth University of Colorado Hospital", "city": "Aurora", "state": "Colorado", "score": "71.71%", "website": "https://www.uchealth.org/"},
    {"rank": 44, "hospital": "University Hospitals Cleveland Medical Center", "city": "Cleveland", "state": "Ohio", "score": "71.65%", "website": "https://www.uhhospitals.org/"},
    {"rank": 45, "hospital": "Scripps Memorial Hospital La Jolla", "city": "La Jolla", "state": "California", "score": "71.63%", "website": "https://www.scripps.org/"},
    {"rank": 46, "hospital": "Baylor St. Luke's Medical Center", "city": "Houston", "state": "Texas", "score": "71.33%", "website": "https://www.stlukeshealth.org/"},
    {"rank": 47, "hospital": "University of Utah Hospital", "city": "Salt Lake City", "state": "Utah", "score": "71.23%", "website": "https://www.healthcare.utah.edu/"},
    {"rank": 48, "hospital": "Penn State Health - Milton S. Hershey Medical Center", "city": "Hershey", "state": "Pennsylvania", "score": "71.14%", "website": "https://www.pennstatehealth.org/"},
    {"rank": 49, "hospital": "Tufts Medical Center", "city": "Boston", "state": "Massachusetts", "score": "71.07%", "website": "https://www.tuftsmedicine.org/"},
    {"rank": 50, "hospital": "Torrance Memorial Medical Center", "city": "Torrance", "state": "California", "score": "71.04%", "website": "https://www.torrancememorial.org/"},
]
