<template>
  <div>
    <table class="table table-hover">
      <thead class="thead-light">
        <tr>
          <th>Name</th>
          <th
            v-for="segment in segments"
            :key="segment.index"
          >{{ segment.name }} ({{ segment.entry_count }})</th>
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
    <div class="container-xl">
      <LeaderboardChart :chart-data="chartdata" :options="chartoptions" />
    </div>
  </div>
</template>

<script>
import "chartjs-plugin-colorschemes";
import LeaderboardListItem from "./LeaderboardListItem.vue";
import LeaderboardChart from "./LeaderboardChart.vue";

export default {
  components: { LeaderboardListItem, LeaderboardChart },

  props: {
    athlete_results: {
      type: Array,
      required: true
    },
    segments: {
      type: Array,
      required: true
    }
  },
  computed: {
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
              scaleLabel: {
                display: true,
                labelString: "Rang in Gesamtwertung"
              },
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
  }
};
</script>
