<template>
  <v-container style="background-color:#C5C6C7; min-height:100%; padding: 0;">
    <v-container fluid style="padding: 0;">
      <v-row no-gutters>
        <v-col sm="2">
          <v-card elevation="2" class="ma-2 pa-2 text-center">
            <template v-if="username"
              ><p>You are logged in as {{ username }}</p>
              <v-btn block plain @click="logOut">
                Log Out
              </v-btn></template
            >
            <template v-else>
              <v-text-field
                v-model="usernametmp"
                label="Username"
                :counter="15"
                :dark="false"
                :rules="usernameRules"
              ></v-text-field>
              <v-btn block plain @click="login">
                Login
              </v-btn>
            </template>
          </v-card>
        </v-col>
        <v-col sm="10" style="position: relative; max-height: 100vh;">
          <div id="chat-container">
            <div
              id="chat"
              style="overflow-y: scroll; height:90vh; padding:20px;"
            >
              <v-row
                no-gutters
                v-for="(message, idx) in messages"
                :key="idx"
                style="margin-top:10px;"
              >
                <v-col cols="1">
                  <div sm="pr-1" outlined style="text-align: right;">
                    <strong>{{ message.username }}</strong
                    >:
                  </div>
                </v-col>
                <v-col cols="5">
                  <v-card
                    class="pa-2 ml-2"
                    outlined
                    style="display: inline-block;"
                  >
                    {{ message.message }}
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </div>

          <div class="typer">
            <v-divider></v-divider>
            <v-container class="align-center" style="max-width:80%;">
              <v-row no-gutters>
                <v-col>
                  <div class="d-flex flex-row align-center">
                    <v-text-field
                      v-model="msg"
                      placeholder="Type Something"
                      @keypress.enter="sendMessage"
                      :counter="200"
                      :rules="messageRules"
                    ></v-text-field>
                    <v-btn
                      icon
                      class="ml-4"
                      :disabled="!isLoggedIn"
                      @click="sendMessage"
                      ><v-icon>mdi-send</v-icon></v-btn
                    >
                  </div>
                </v-col>
              </v-row>
            </v-container>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar
      :timeout="2000"
      :value="showAlert"
      color="blue-grey"
      absolute
      right
      rounded="pill"
      elevation="5"
      top
    >
      {{ errorMsg }}
    </v-snackbar>
  </v-container>
</template>

<script>
//import Thread from "@/components/Thread.vue";

export default {
  name: "ThreadView",
  components: {
    // Thread,
  },
  data() {
    return {
      messages: [],
      username: window.localStorage.getItem("username") || "",
      isLoggedIn: !this.username,
      usernametmp: "",
      msg: "",
      snackbar: !!window.localStorage.getItem("username"),
      errorMsg: "",
      showAlert: false,

      usernameRules: [
        (value) => !!value || "Required",
        (value) => (value && value.length <= 15) || "Max 15 characters",
      ],
      messageRules: [
        (value) => !!value || "Required",
        (value) => (value && value.length <= 200) || "Max 200 characters",
      ],
    };
  },
  methods: {
    getMessages() {
      this.axios
        .get("http://127.0.0.1:8000/thread/" + this.$route.params.thread_id)
        .then((response) => {
          this.messages = response.data.messages;
          this.$nextTick(() => {
            const objDiv = window.document.getElementById("chat");
            objDiv.scrollTop = objDiv.scrollHeight;
          });
        });
    },
    sendMessage() {
      this.axios
        .post(
          `http://127.0.0.1:8000/thread/${this.$route.params.thread_id}/${this.username}`,
          {
            message: this.msg,
          },
        )
        .then(() => {
          this.getMessages();
          this.msg = "";
        })
        .catch((error) => {
          if (error.response.status === 403) {
            this.errorMsg = `${this.username} doesnt have a permission to write in this thread`;
            this.showAlert = true;
          }
        });
    },
    logOut() {
      window.localStorage.clear();
      this.username = "";
      this.isLoggedIn = false;
    },
    login() {
      window.localStorage.setItem("username", this.usernametmp);
      this.username = this.usernametmp;
      this.usernametmp = "";
      this.isLoggedIn = true;
    },
  },
  created() {
    this.getMessages();
  },
};
</script>

<style scoped>
.scrollable {
  overflow-y: auto;
  height: 90vh;
}
.typer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 10vh;

  z-index: 999;
  background-color: #f2f2f2;
}
#chat-container {
  max-height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f2f2f2;
  min-height: 100vh;
}
</style>
