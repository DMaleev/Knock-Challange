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
      <v-btn
        style="width:100%; margin-top: 10px;"
        :loading="loading"
        :disabled="loading"
        color="green"
        :dark="true"
        @click="addUser"
      >
        Add user
      </v-btn>
      <v-btn
        style="width:100%; margin-top: 10px;"
        :loading="loading"
        :disabled="loading"
        color="primary"
        :dark="true"
        @click="createThread"
      >
        Create thread
      </v-btn>
    </v-form>
    <div class="text-center">
      <v-chip
        v-for="user in users"
        :key="user"
        class="ma-2"
        close
        @click:close="removeUser(user)"
      >
        {{ user }}
      </v-chip>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "ThreadCreate",
  data() {
    return {
      username: "",
      valid: true,
      users: [],

      usernameRules: [
        (value) => !!value || "Required",
        (value) => (value && value.length <= 15) || "Max 15 characters",
      ],

      loading: false,
    };
  },
  methods: {
    createThread() {
      this.loading = true;
      if (this.users.length >= 2) {
        this.axios
          .post(`http://127.0.0.1:8000/thread/`, {
            users: this.users,
          })
          .then((response) => {
            this.$router.push({
              name: "Thread",
              params: { thread_id: response.data.thread_id },
            });
          })
          .catch(function(error) {
            console.log(error);
          });
      }

      this.loading = false;
    },
    addUser() {
      if (this.users.includes(this.username)) {
        this.username = "";
      } else {
        this.users.push(this.username);
      }

      this.username = "";
    },
    removeUser(user) {
      console.log(user);
      this.users = this.users.filter((e) => e !== user);
    },
    isNormalInteger(str) {
      return /^[1-9][0-9]*$/.test(str);
    },
  },
};
</script>
