<template>
  <v-row
    justify="center"
    style="padding-top: 35vh;
"
  >
    <v-col>
      <v-main>
        <v-container style="max-width: 400px;">
          <v-tabs v-model="tab" background-color="transparent" dark fixed-tabs>
            <v-tab v-for="item in items" :key="item.tab">
              {{ item.tab }}
            </v-tab>
          </v-tabs>
          <template v-if="tab == 0"><Login /></template>
          <template v-else><ThreadCreate /></template>
        </v-container>
      </v-main>
    </v-col>
  </v-row>
</template>

<script>
import Login from "@/components/Login.vue";
import ThreadCreate from "@/components/ThreadCreate.vue";

export default {
  name: "Home",
  components: {
    Login,
    ThreadCreate,
  },
  data() {
    return {
      tab: 0,
      items: [{ tab: "Enter" }, { tab: "Create" }],
    };
  },
};
</script>
