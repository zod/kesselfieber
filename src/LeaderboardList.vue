<template>
  <table class="table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Segment 1 Zeit</th>
        <th>Segment 1 Platz</th>
      </tr>
    </thead>
    <tbody>
      <LeaderboardListItem v-for="athlete in athletes" :athlete="athlete" />
    </tbody>
  </table>
</template>

<script>
import LeaderboardListItem from "./LeaderboardListItem.vue";
export default {
  components: { LeaderboardListItem },
  data() {
    return {
      athletes: [
        { name: "Manuel F.", segments: [{ rank: 1 }, { rank: 2 }] },
        { name: "Urs R." }
      ]
    };
  }
};
</script>