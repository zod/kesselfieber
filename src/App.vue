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
        <li class="nav-item nav-link disabled" v-if="!segments_raw.length">Lade Leistungen...</li>
      </ul>
      <AthleteSearch :athletes="athletes" @add="addAthlete" @changeGender="changeGender" />
    </nav>
    <LeaderboardList
      :athlete_results="athlete_results_visible"
      :segments="segments"
      @remove="removeAthlete"
    />
    <LeaderboardChart :athlete_results="athlete_results_visible" :segments="segments" />
  </div>
</template>

<script>
import AthleteSearch from "./AthleteSearch.vue";
import LeaderboardChart from "./LeaderboardChart.vue";
import LeaderboardList from "./LeaderboardList.vue";

export default {
  components: { AthleteSearch, LeaderboardChart, LeaderboardList },
  mounted() {
    fetch("https://bergzeitfahren.kesseln.cc/api/segments")
      .then(response => response.json())
      .then(data => {
        this.segments_raw = data;
      })
      .catch(error => {
        console.log("Error:", error);
      });
  },
  data() {
    return {
      segments_raw: [],
      athlete_gender: "M",
      athlete_filter: []
    };
  },
  computed: {
    athletes() {
      return this.athlete_results
        .map(athlete_result => athlete_result.athlete_name)
        .sort();
    },
    athlete_results() {
      var athlete_results = new Map();
      var leaderboard_total = new Map();
      this.segments_raw.forEach(segment => {
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
            (a, b) => b[1] - a[1]
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
    athlete_results_visible() {
      return this.athlete_results
        .filter(athlete_result =>
          this.athlete_filter.includes(athlete_result.athlete_name)
        )
        .sort((a, b) => a.athlete_name.localeCompare(b.athlete_name));
    },
    segments() {
      var segments = [];
      this.segments_raw.forEach(segment => {
        if (
          segment.visible &&
          segment.leaderboard[this.athlete_gender].effort_count > 0
        ) {
          var entry_kom = segment.leaderboard[this.athlete_gender].entries[0];
          segments.push({
            index: segment.index,
            id: segment.id,
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
    addAthlete(athlete_name) {
      this.athlete_filter.push(athlete_name);
    },
    removeAthlete(athlete_name_remove) {
      this.athlete_filter = this.athlete_filter.filter(
        athlete_name => athlete_name !== athlete_name_remove
      );
    },
    changeGender(gender) {
      this.athlete_gender = gender;
      this.athlete_filter = [];
    }
  }
};
</script>