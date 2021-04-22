<template>
  <v-container fill-height>
    <v-form ref="form" v-model="valid" lazy-validation style="width:100%;">
      <v-text-field
        v-model="username"
        label="Username"
        :counter="15"
        :dark="true"
        :disabled="loading"
        :rules="usernameRules"
      ></v-text-field>
      <v-text-field
        v-model.number="thread_id"
        label="Thread id"
        :dark="true"
        :disabled="loading"
        :rules="thread_idRules"
      ></v-text-field>
      <v-btn
        style="width:100%; margin-top: 10px;"
        :loading="loading"
        :disabled="loading"
        color="primary"
        :dark="true"
        @click="enterThread"
      >
        Enter thread
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      thread_id: null,
      valid: true,

      usernameRules: [
        (value) => !!value || "Required",
        (value) => (value && value.length <= 15) || "Max 15 characters",
      ],

      thread_idRules: [
        (value) => !!value || "Required",
        (value) =>
          (value && this.isNormalInteger(value)) ||
          "Value should be valid integer",
      ],

      loading: false,
    };
  },
  methods: {
    enterThread() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        window.localStorage.setItem("username", this.username);
        this.$router.push({
          name: "Thread",
          params: { thread_id: this.thread_id },
        });
      }
      this.loading = false;
    },
    isNormalInteger(str) {
      return /^[1-9][0-9]*$/.test(str);
    },
  },
};
</script>
