#!/usr/bin/env python3

import copy
import json
athlete_results = {}
leaderboard_total = {}

segments = json.load(open("test/segments.json", "r"))
for segment in segments:
    if 'leaderboard' not in segment:
        continue
    entries = segment['leaderboard']['M']['entries']
    for entry in entries:
        name = entry['athlete_name']
        rank = entry['rank']
        points = len(entries) - entry['rank'] + 1
        if name not in leaderboard_total:
            leaderboard_total[name] = {
                'points': points,
            }
        else:
            leaderboard_total[name]['points'] += points

    # Now rank them, if they have the same score, they should get the same rank
    leaderboard_sorted = sorted(
        leaderboard_total.items(), key=lambda x: x[1]['points'], reverse=True)
    rank_same = 0
    rank = 0
    for index, entry in enumerate(leaderboard_sorted):
        name = entry[0]
        value = entry[1]
        if index > 0 and value['points'] == leaderboard_sorted[index - 1][1]['points']:
            rank_same += 1
        else:
            rank += 1 + rank_same
            rank_same = 0
        segment_result = {
            "id": segment["index"],
            "rank": rank,
            "points": value["points"],
        }
        if name in athlete_results:
            athlete_results[name]["segments"].append(segment_result)
        else:
            segment_results_empty = [{
                "id": str(segment_id),
                "rank": -1,
                "points": -1
            } for segment_id in range(1, int(segment["index"]))]
            athlete_results[name] = {
                "athlete_name": name,
                "segments": [*segment_results_empty, segment_result]
            }

json.dump(list(athlete_results.values()),
          open("test/athlete_results.json", "w"))
