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
        <li class="nav-item nav-link disabled" v-if="!segments_raw.length">
          Lade Leistungen...
        </li>
      </ul>
      <AthleteSearch
        :athletes="athletes"
        :athlete_gender_initial="athlete_gender"
        @add="addAthlete"
        @changeGender="changeGender"
      />
    </nav>
    <LeaderboardList
      :athlete_results="athlete_results_visible"
      :segments="segments"
      @remove="removeAthlete"
    />
    <LeaderboardChart
      :athlete_results="athlete_results_visible"
      :segments="segments"
    />
  </div>
</template>

<script>
import AthleteSearch from "./AthleteSearch.vue";
import LeaderboardChart from "./LeaderboardChart.vue";
import LeaderboardList from "./LeaderboardList.vue";
import Vue from 'vue'

export default {
  components: { AthleteSearch, LeaderboardChart, LeaderboardList },
  created() {
    if (localStorage.getItem("athlete_gender")) {
      this.athlete_gender = localStorage.getItem("athlete_gender");
    }
    if (localStorage.getItem("athlete_filter")) {
      try {
        this.athlete_filter = JSON.parse(
          localStorage.getItem("athlete_filter")
        );
      } catch (e) {
        localStorage.removeItem("athlete_filter");
      }
    }
  },
  mounted() {
    fetch("https://smb21.kesseln.cc/api/segments")
      .then((response) => response.json())
      .then((segments) => {
        this.segments_raw = segments;
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  },
  data() {
    return {
      segments_raw: [],
      athlete_gender: "M",
      athlete_filter: [],
    };
  },
  computed: {
    athletes() {
      return this.athlete_results
        .map((athlete_result) => athlete_result.athlete)
        .sort((a, b) => a.fullname.localeCompare(b.fullname));
    },
    athlete_results() {
      var athlete_results = new Map();
      var leaderboard_total = new Map();
      this.segments_raw.forEach((segment) => {
        if (segment.display && segment.efforts) {
          segment.efforts.forEach((entry) => {
            /* Assign efforts to each athlete */
            var athlete_id = entry.athlete.id;
            var segment_result = {
              order: segment.order,
              elapsed_time: entry.elapsed_time,
              rank_segment: entry.rank,
            };
            if (!athlete_results.has(athlete_id)) {
              var segment_results_empty = [];
              for (var i = 1; i < segment.order; i++) {
                segment_results_empty.push({ order: i });
              }
              athlete_results.set(athlete_id, {
                athlete: entry.athlete,
                segments: [...segment_results_empty, segment_result],
              });
            } else {
              athlete_results.get(athlete_id).segments.push(segment_result);
            }

            /* Assign points into global leaderboard */
            var points = entry.points;
            if (!leaderboard_total.has(athlete_id)) {
              leaderboard_total.set(athlete_id, points);
            } else {
              leaderboard_total.set(
                athlete_id,
                points + leaderboard_total.get(athlete_id)
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
            var [athlete_id, points] = leaderboard_sorted[i];
            if (i > 0 && points == leaderboard_sorted[i - 1].points) {
              rank_same += 1;
            } else {
              rank += 1 + rank_same;
              rank_same = 0;
            }
            var segment_result = {
              order: segment.order,
              rank_total: rank,
              points: points,
            };
            var athlete_segments = athlete_results.get(athlete_id).segments;
            var last_segment = athlete_segments[athlete_segments.length - 1];
            if (last_segment.order == segment.order) {
              Object.assign(last_segment, segment_result);
            } else {
              athlete_results.get(athlete_id).segments.push(segment_result);
            }
          }
        }
      });
      return Array.from(athlete_results.values());
    },
    athlete_results_visible() {
      return this.athlete_results
        .filter((athlete_result) =>
          this.athlete_filter.includes(athlete_result.athlete.id)
        )
        .sort((a, b) => a.athlete.fullname.localeCompare(b.athlete.fullname));
    },
    segments() {
      var segments = [];
      this.segments_raw.forEach((segment) => {
        if (
          segment.display &&
          segment.efforts &&
          segment.efforts.length > 0
        ) {
          var entry_kom = segment.efforts[0];
          segments.push({
            order: segment.order,
            id: segment.id,
            name: segment.name,
            entry_count: segment.efforts.length,
            kom: {
              elapsed_time: entry_kom.elapsed_time,
            },
          });
        }
      });
      return segments;
    },
  },
  methods: {
    addAthlete(athlete_id) {
      this.athlete_filter.push(athlete_id);
      this.saveAthletes();
    },
    removeAthlete(athlete_id_remove) {
      this.athlete_filter = this.athlete_filter.filter(
        (athlete_id) => athlete_id !== athlete_id_remove
      );
      this.saveAthletes();
    },
    saveAthletes() {
      localStorage.setItem(
        "athlete_filter",
        JSON.stringify(this.athlete_filter)
      );
    },
    changeGender(gender) {
      this.athlete_gender = gender;
      this.athlete_filter = [];
      localStorage.setItem("athlete_gender", gender);
      this.saveAthletes();
      this.segments_raw.forEach((segment) => {
        if (segment.display) {
          fetch(
            `https://smb21.kesseln.cc/api/segments/${segment.id}/efforts?gender=${this.athlete_gender}`
          )
            .then((response) => response.json())
            .then((efforts) => {
              var idx = this.segments_raw.findIndex(
                (segment_raw) => segment_raw.id == segment.id
              );
              Vue.set(this.segments_raw[idx], 'efforts', efforts);
            });
        }
      });
    },
  },
};
</script>