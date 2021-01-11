import time
import argparse

import requests

import config as cfg


heroids = [i for i in range(1, 115)]
heroids = heroids.extend([119, 120, 121, 123, 126, 128, 129])
laneids = [1, 2, 3]
parser = argparse.ArgumentParser(description="Query OPENDOTA (https://www.opendota.com) for Hero Matchups")
parser.add_argument("hero1", type=int, choices=heroids, help="ID of the first hero")
parser.add_argument("hero2", type=int, choices=heroids, help="ID of the second hero")
parser.add_argument("lane1", type=int, choices=laneids,
                    help="ID of the lane where hero 1 was played. 1 = Safe, 2 = Mid, 3 = Off", metavar="lane1")
parser.add_argument("lane2", type=int, choices=laneids,
                    help="ID of the lane where hero 2 was played. 1 = Safe, 2 = Mid, 3 = Off", metavar="lane2")

SQL = """SELECT m.match_id,
p1.personaname AS p1_name,
p2.personaname AS p2_name,
pm1.lane AS pm1_lane,
pm2.lane AS pm2_lane,
m.start_time
FROM matches m
INNER JOIN player_matches pm1 ON (m.match_id = pm1.match_id)
INNER JOIN player_matches pm2 ON (m.match_id = pm2.match_id)
INNER JOIN players p1 ON (pm1.account_id = p1.account_id)
INNER JOIN players p2 ON (pm2.account_id = p2.account_id)
WHERE p1.account_id != p2.account_id
AND (pm1.player_slot < 5 AND pm2.player_slot > 127)
AND (pm1.hero_id = {0} AND pm2.hero_id = {1} OR pm1.hero_id = {1} AND pm2.hero_id = {0})
AND (pm1.lane_role = {2} AND pm2.lane_role = {3} OR pm1.lane_role = {3} AND pm2.lane_role = {2})
ORDER BY m.start_time DESC"""


def send_request(query):
    payload = {"sql": query}
    r = requests.get(cfg.HOST + cfg.EXPLORER_ENDPOINT, params=payload)
    if r.status_code != 200:
        print("OPENDOTA responded with error code: {0}".format(r.status_code))
        return []
    else:
        return parse_response(r.json())

def parse_response(response):
    if response["rowCount"] > 0:
        rows = response["rows"]
        return [row for row in rows]
    else:
        return []

def main():
    args = parser.parse_args()
    
    rows = send_request(SQL.format(args.hero1, args.hero2, args.lane1, args.lane2))
    if len(rows) > 0:
        print("{0:<12} {1:<30} {2:<32} {3:<32}".format("MATCH ID",
                                                       "DATE",
                                                       "PLAYER 1 (LANE)",
                                                       "PLAYER 2 (LANE)"))
        for row in rows:
            print("{0:<12} {1:<30} {2:<32} {3:<32}".format(row["match_id"],
                                                           time.ctime(row["start_time"]),
                                                           row["p1_name"] + " (" + str(row["pm1_lane"]) + ")",
                                                           row["p2_name"] + " (" + str(row["pm2_lane"]) + ")"))

    else:
        print("No results")


if __name__ == "__main__":
    main()
