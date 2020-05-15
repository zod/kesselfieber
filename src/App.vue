<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Kesselfieber</a>
      <ul class="navbar-nav mr-auto">
        <!--
        <li class="nav-item">
          <a class="nav-link" href="#">Ergebnisse</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Segmentfieber</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Gesamtfieber</a>
        </li>
        -->
      </ul>
      <AthleteSearch :athletes="athletes" @add="addAthlete" />
    </nav>
    <table class="table">
      <tr>
        <td>Name</td>
        <td
          v-for="segment in segments"
          :key="segment.index"
        >{{ segment.name }} ({{segment.entry_count}})</td>
      </tr>
      <tr v-for="athlete_result in athlete_results" :key="athlete_result.athlete_name">
        <td>{{ athlete_result.athlete_name }}</td>
        <td v-for="segment in athlete_result.segments">{{ segment.rank_segment }}</td>
      </tr>
    </table>
    <LeaderboardList />
  </div>
</template>

<script>
import AthleteSearch from "./AthleteSearch.vue";
import LeaderboardList from "./LeaderboardList.vue";
import segments_raw from "../test/segments.json";

export default {
  components: { AthleteSearch, LeaderboardList },
  data: function() {
    return {
      athlete_gender: "M"
    };
  },
  computed: {
    athletes: function() {
      var athletes = new Set();
      segments_raw.forEach(segment => {
        if (segment.visible && segment.leaderboard) {
          segment.leaderboard[this.athlete_gender].entries.forEach(entry => {
            athletes.add(entry.athlete_name);
          });
        }
      });
      return Array.from(athletes.values()).sort();
    },
    athlete_results: function() {
      var athlete_results = new Map();
      var leaderboard_total = new Map();
      segments_raw.forEach(segment => {
        if (segment.visible && segment.leaderboard) {
          segment.leaderboard[this.athlete_gender].entries.forEach(entry => {
            /* Assign efforts to each athlete */
            var athlete_name = entry.athlete_name;
            var segment_result = {
              index: segment.index,
              elapsed_time: entry.elapsed_time,
              rank_segment: entry.rank
            };
            if (!athlete_results.has(athlete_name)) {
              var segment_results_empty = [];
              for (var i = 1; i < segment.index; i++) {
                segment_results_empty.push({ index: i });
              }
              athlete_results.set(athlete_name, {
                athlete_name: athlete_name,
                segments: [...segment_results_empty, segment_result]
              });
            } else {
              athlete_results.get(athlete_name).segments.push(segment_result);
            }

            /* Assign points into global leaderboard */
            var points =
              segment.leaderboard[this.athlete_gender].entry_count -
              entry.rank +
              1;
            if (!leaderboard_total.has(athlete_name)) {
              leaderboard_total.set(athlete_name, points);
            } else {
              leaderboard_total.set(
                athlete_name,
                points + leaderboard_total.get(athlete_name)
              );
            }
          });
          /* Assign rank for every segment */
          var leaderboard_sorted = Array.from(leaderboard_total.entries()).sort(
            (a, b) => a[1] < b[1]
          );
          for (
            var i = 0, rank = 0, rank_same = 0;
            i < leaderboard_sorted.length;
            i++
          ) {
            var [athlete_name, points] = leaderboard_sorted[i];
            if (i > 0 && points == leaderboard_sorted[i - 1].points) {
              rank_same += 1;
            } else {
              rank += 1 + rank_same;
              rank_same = 0;
            }
            var segment_result = {
              index: segment.index,
              rank_total: rank,
              points: points
            };
            var athlete_segments = athlete_results.get(athlete_name).segments;
            var last_segment = athlete_segments[athlete_segments.length - 1];
            if (last_segment.index == segment.index) {
              Object.assign(last_segment, segment_result);
            } else {
              athlete_results.get(athlete_name).segments.push(segment_result);
            }
          }
        }
      });
      return Array.from(athlete_results.values());
    },
    segments: function() {
      var segments = [];
      segments_raw.forEach(segment => {
        if (segment.visible && segment.leaderboard) {
          var entry_kom = segment.leaderboard[this.athlete_gender].entries[0];
          segments.push({
            index: segment.index,
            name: segment.name,
            entry_count: segment.leaderboard[this.athlete_gender].entry_count,
            kom: {
              elapsed_time: entry_kom.elapsed_time
            }
          });
        }
      });
      return segments;
    }
  },
  methods: {
    addAthlete: function(athlete_name) {
      console.log(this.athlete_results);
      console.log("test", athlete_name);
    }
  }
};
</script>