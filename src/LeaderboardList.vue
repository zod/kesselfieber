<template>
  <div>
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
          @remove="removeAthlete"
        />
      </tbody>
    </table>
    <div class="container-xl">
      <LeaderboardChart :chart-data="chartdata" :options="chartoptions" />
    </div>
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
    },
    removeAthlete(nameToRemove) {
      this.athlete_filter = this.athlete_filter.filter(
        athlete_name => athlete_name !== nameToRemove
      );
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
