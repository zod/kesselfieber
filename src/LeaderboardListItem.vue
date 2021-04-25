<template>
  <tr>
    <td>
      {{ athlete_result.athlete.fullname }}
      <button
        class="btn btn-outline-danger btn-sm"
        @click="$emit('remove', athlete_result.athlete.id)"
      >X</button>
    </td>
    <td v-for="segment in athlete_result.segments" :key="segment.id">{{ segment.rank_segment }}</td>
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