<template>
  <div>
    <table class="table table-hover">
      <thead class="thead-light">
        <tr>
          <th>Name</th>
          <th v-for="segment in segments" :key="segment.index">
            <a :href="segment.id | strava_segment_url">{{ segment.name }}</a>
            ({{ segment.entry_count }})
          </th>
        </tr>
      </thead>
      <tbody>
        <LeaderboardListItem
          v-for="athlete_result in athlete_results"
          :key="athlete_result.athlete_name"
          :athlete_result="athlete_result"
          v-on="$listeners"
        />
      </tbody>
    </table>
  </div>
</template>

<script>
import LeaderboardListItem from "./LeaderboardListItem.vue";

export default {
  components: { LeaderboardListItem },

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
  filters: {
    strava_segment_url: function(id) {
      return "https://strava.com/segments/" + id;
    }
  }
};
</script>
