<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th v-for="segment in segments" :key="segment.id">{{ segment.name }}</th>
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
    <LeaderboardChart :chartdata="chartdata" :options="chartoptions" />
  </div>
</template>

<script>
import LeaderboardListItem from "./LeaderboardListItem.vue";
import LeaderboardChart from "./LeaderboardChart.vue";
import athlete_results from "../test/athlete_results.json";
import segments from "../test/segments.json";

export default {
  components: { LeaderboardListItem, LeaderboardChart },
  data() {
    return {};
  },
  computed: {
    athlete_results: function() {
      return athlete_results.filter(
        athlete_result =>
          athlete_result.athlete_name == "Manuel F." ||
          athlete_result.athlete_name == "Urs R."
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
        scales: { yAxes: [{ ticks: { reverse: true } }] }
      };
    },
    datasets: function() {
      return this.athlete_results.map(athlete_result => {
        return {
          label: athlete_result.athlete_name,
          fill: false,
          data: athlete_result.segments.map(segment => {
            return segment.rank;
          })
        };
      });
    }
  }
};
</script>