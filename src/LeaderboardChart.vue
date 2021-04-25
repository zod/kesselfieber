<template>
  <div class="container-xl">
    <line-chart :chart-data="chartdata" :options="chartoptions"></line-chart>
  </div>
</template>

<script>
import "chartjs-plugin-colorschemes";
import LineChart from "./LineChart.js";

export default {
  components: { LineChart },
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
        datasets: this.athlete_results.map(athlete_result => {
          return {
            lineTension: 0,
            label: athlete_result.athlete.fullname,
            fill: false,
            data: athlete_result.segments.map(segment => {
              return segment.rank_total;
            })
          };
        })
      };
    },
    chartoptions: function() {
      return {
        plugins: {
          colorschemes: {
            scheme: "brewer.Paired12"
          }
        },
        tooltips: {
          mode: "index",
          intersect: false
        },
        scales: {
          xAxes: [
            {
              position: "top"
            }
          ],
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
    }
  }
};
</script>