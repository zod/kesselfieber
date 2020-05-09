<template>
  <div id="app">
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Segment 1 Zeit</th>
          <th>Segment 1 Platz</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>KOM</th>
          <td>3:57</td>
          <td>Simon B.</td>
        </tr>
        <tr>
          <th>Manuel F.</th>
          <td v-for="item in leaderboards">{{ item }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import leaderboards from "../test/leaderboards.json";

console.log(leaderboards);

export default {
  name: "app",
  data() {
    return {
      leaderboards: leaderboards
    };
  }
};
</script>