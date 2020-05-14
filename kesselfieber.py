#!/usr/bin/env python3

# In segments.json data is stored with segment as key.
# We only need data for some athlets but all of it, change the index key

import copy
import json

segments = json.load(open("test/segments.json", "r"))
athlete_results_total = {}

for gender in ["M", "F"]:
    athlete_results = {}
    leaderboard_total = {}

    for segment in segments:
        if 'leaderboard' not in segment:
            continue
        entries = segment['leaderboard'][gender]['entries']
        for entry in entries:
            name = entry['athlete_name']
            # Add segment result to user
            segment_result = {
                "id": segment["index"],
                "elapsed_time": entry["elapsed_time"],
                "rank_segment": entry["rank"]

            }
            if name not in athlete_results:
                segment_result_empty = [{"id": str(segment_id)}
                                        for segment_id in range(1, int(segment["index"]))]
                athlete_results[name] = {
                    "athlete_name": name,
                    "segments": [*segment_result_empty, segment_result]
                }
            else:
                athlete_results[name]["segments"].append(segment_result)

            rank = entry['rank']
            points = len(entries) - entry['rank'] + 1
            # Track leaderboard to calculate rank afterwards
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
                "rank_total": rank,
                "points": value["points"],
            }
            last_segment = athlete_results[name]["segments"][-1]
            if "id" in last_segment and last_segment["id"] == segment["index"]:
                last_segment.update(segment_result)
            else:
                athlete_results[name]["segments"].append(segment_result)
    athlete_results_total[gender] = list(athlete_results.values())

json.dump(athlete_results_total, open("test/athlete_results.json", "w"))
