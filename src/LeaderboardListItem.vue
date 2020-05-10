<template>
  <tr>
    <td>{{ athlete_result.athlete_name }}</td>
    <td v-for="segment in athlete_result.segments">{{ segment.rank }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    athlete_result: {
      type: Object,
      required: true
    }
  }
};
</script>