import pandas as pd
import requests

NHL_BASE_URL = "http://statsapi.web.nhl.com"


"""
PLAY-OFF GAMES CODES
==============================================================================
2015 | 03 | 04 | 12 
2015 = season code, first year of the season (e.g., 2015 is for the 2015-16 seasons)
03   = game type code; 1 = preseason, 2 = regular season; 3 = playoffs
04   = playoff only: round number (1st round = 1, 2nd round = 2, ECF/WCF = 3, SCF = 4)
1    = series number: 1-8 in round 1, 1-4 in round 2, 1-2 in round 3,1 in round 4
2    = game number: 1-7 for any given series
==============================================================================

REGULAR SEASON / PRE SEASON GAMES CODES
==============================================================================
2015 | 03 | 0411
2015 = season code, first year of the season (e.g., 2015 is for the 2015-16 seasons)
02   = game type code; 1 = preseason, 2 = regular season; 3 = playoffs
0807 = game ID; generally 1-1230 in a normal regular season, but sometimes games will be missing 
       (e.g., games cancelled due to weather) and sometimes games will be added on the end, starting
        with 1231 (e.g., make-up games for weather-cancelled games). Numbers are usually approx. 
        1-130ish in the pre-season, but it can be arbitrary.
==============================================================================
"""
years = range(2016, 2017)
game_types = [3]
game_id_preseason = range(1, 140)
game_id_season = range(1, 1250)

games_code_list = []
for year in years:
    for game_type in game_types:
        if game_type == 1:
            for game_id in game_id_preseason:
                games_code_list.append("{0}{1:02d}{2:04d}".format(year, game_type, game_id))
        elif game_type == 2:
            for game_id in game_id_season:
                games_code_list.append("{0}{1:02d}{2:04d}".format(year, game_type, game_id))
        elif game_type == 3:
            # 2015 | 03 | 04 | 12
            for playoff in range(1, 5):
                for series in range(1, 9):
                    for game in range(1, 8):
                        games_code_list.append("{0}{1:02d}{2:02d}{3}{4}".format(year, game_type, playoff, series, game))
print(games_code_list)

game_list = []

for idx, game_code in enumerate(games_code_list):
    nhl_game_url = "{0}/api/v1/game/{1}/feed/live".format(NHL_BASE_URL, game_code)
    r = requests.get(nhl_game_url)

    print("index: {0}/{1}".format(idx, len(games_code_list)))

    if idx > 5:
        break

    if r.status_code == 200:    # valid request
        print("Request {0} Successful".format(nhl_game_url))
        r_json = r.json()

        game = r_json['gameData']
        start_time = game['datetime']['dateTime']
        end_time = game['datetime']['endDateTime']

        away_team = game['teams']['away']
        home_team = game['teams']['home']
        away_team_name = away_team['name']
        home_team_name = home_team['name']

        boxscore = r_json['liveData']['boxscore']
        offical_id = boxscore['officials'][0]['official']['id']
        offical_name = boxscore['officials'][0]['official']['fullName']

        row_dict = {"code": game_code,
                    'away_team': away_team_name,
                    'home_team': home_team_name,
                    'offical_1': offical_name}
        game_list.append(row_dict)
        print('something')
    else:
        print("No Response")

game_df = pd.DataFrame(game_list)
print(game_df)
