<template>
  <div class="form-inline my-2 my-lg-0">
    <label class="sr-only" for="selectGender">Geschlecht</label>
    <select
      class="custom-select"
      id="selectGender"
      v-model="athlete_gender"
      @change="$emit('changeGender', athlete_gender)"
    >
      <option selected>Geschlecht</option>
      <option value="M">Buaba</option>
      <option value="F">Mädla</option>
    </select>
    <label class="sr-only" for="selectAthlete">Name</label>
    <select class="custom-select" name="athlete" id="selectAthlete" v-model="athlete_name">
      <option v-for="athlete in athletes" :key="athlete" :value="athlete">{{ athlete }}</option>
    </select>

    <button
      class="btn btn-outline-primary my-2 my-sm-0"
      type="submit"
      @click="$emit('add', athlete_name)"
    >hinzufügen</button>
  </div>
</template>
<script>
export default {
  data() {
    return {
      athlete_name: "",
      athlete_gender: "M"
    };
  },
  props: {
    athletes: {
      type: Array,
      required: true
    }
  }
};
</script>