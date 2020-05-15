<template>
  <div id="app">
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
      <AthleteSearch :athletes="athletes" @add="addAthlete" />
    </nav>
    <LeaderboardList />
  </div>
</template>

<script>
import AthleteSearch from "./AthleteSearch.vue";
import LeaderboardList from "./LeaderboardList.vue";
export default {
  components: { AthleteSearch, LeaderboardList },
  data: function() {
    return {
      athletes: ["Manuel F.", "Urs R."]
    };
  },
  methods: {
    addAthlete: function(athlete_name) {
      console.log("test", athlete_name);
    }
  }
};
</script>