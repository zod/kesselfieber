<template>
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
</template>

<script>
import LeaderboardListItem from "./LeaderboardListItem.vue";
import athlete_results from "../test/athlete_results.json";
import segments from "../test/segments.json";

export default {
  components: { LeaderboardListItem },
  data() {
    return {
      segments: segments,
      athlete_results: athlete_results
    };
  }
};
</script>