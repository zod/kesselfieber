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
  }
};
</script>
