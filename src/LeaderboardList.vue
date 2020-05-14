<template>
  <div>
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
      <div class="form-inline my-2 my-lg-0">
        <label class="sr-only" for="selectGender">Geschlecht</label>
        <select class="custom-select" id="selectGender" v-model="athlete_gender">
          <option selected>Geschlecht</option>
          <option value="M">Buaba</option>
          <option value="F">Mädla</option>
        </select>
        <label class="sr-only" for="selectAthlete">Name</label>
        <select class="custom-select" name="athlete" id="selectAthlete" v-model="athlete_add">
          <option
            v-for="athlete in athletes"
            :key="athlete.athlete_name"
            :value="athlete.athlete_name"
          >{{ athlete.athlete_name }}</option>
        </select>
        <button
          type="submit"
          class="btn btn-outline-primary my-2 my-sm-0"
          v-on:click="addAthlete"
        >hinzufügen</button>
      </div>
    </nav>
    <table class="table table-hover">
      <thead class="thead-light">
        <tr>
          <th>Name</th>
          <th
            v-for="segment in segments"
            :key="segment.id"
          >{{ segment.name }} ({{ segment.leaderboard[athlete_gender].effort_count }})</th>
        </tr>
      </thead>
      <tbody>
        <LeaderboardListItem
          v-for="athlete_result in athlete_results"
          :key="athlete_result.athlete_name"
          :athlete_result="athlete_result"
        />
      </tbody>
    </table>
    <LeaderboardChart :chart-data="chartdata" :options="chartoptions" />
  </div>
</template>

<script>
import "chartjs-plugin-colorschemes";
import LeaderboardListItem from "./LeaderboardListItem.vue";
import LeaderboardChart from "./LeaderboardChart.vue";
import athlete_results from "../test/athlete_results.json";
import segments from "../test/segments.json";

export default {
  components: { LeaderboardListItem, LeaderboardChart },
  data() {
    return {
      athlete_add: "",
      athlete_filter: [],
      athlete_gender: "M"
    };
  },
  methods: {
    addAthlete() {
      this.athlete_filter.push(this.athlete_add);
    }
  },
  computed: {
    athletes: function() {
      return athlete_results[this.athlete_gender].sort((a, b) =>
        a.athlete_name.localeCompare(b.athlete_name)
      );
    },
    athlete_results: function() {
      return athlete_results[this.athlete_gender].filter(athlete_result =>
        this.athlete_filter.includes(athlete_result.athlete_name)
      );
    },
    segments: function() {
      return segments.filter(segment => segment.name);
    },
    chartdata: function() {
      return {
        labels: this.segments.map(segment => {
          return segment.name;
        }),
        datasets: this.datasets
      };
    },
    chartoptions: function() {
      return {
        plugins: {
          colorschemes: {
            scheme: "brewer.Paired12"
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                suggestedMin: 1,
                reverse: true
              }
            }
          ]
        }
      };
    },
    datasets: function() {
      return this.athlete_results.map(athlete_result => {
        return {
          lineTension: 0,
          label: athlete_result.athlete_name,
          fill: false,
          data: athlete_result.segments.map(segment => {
            return segment.rank_total;
          })
        };
      });
    }
  },
  watch: {
    athlete_gender: function() {
      this.athlete_filter = [];
    }
  }
};
</script>
