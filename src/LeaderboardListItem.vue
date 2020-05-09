<template>
  <tr>
    <th>{{ athlete.name }}</th>
    <td v-for="segment in athlete.segments">{{ segment.rank }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    athlete: {
      type: Object,
      required: true
    }
  }
};
</script>