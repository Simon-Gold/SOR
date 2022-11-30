<template>
  <div class="container">
    <div class="card text-left">
      <div class="card-body">
        <h4 class="card-title text-primary">User Profile</h4>
        <hr class="mb-5" />
        <label class="text-secondary">First Name</label>
        <h5 class="text-primary mb-1">
          {{
            userProfile && userProfile.first_name
              ? userProfile.first_name
              : "------"
          }}
        </h5>
        <label class="text-secondary">Last Name</label>
        <h5 class="text-primary mb-1">
          {{
            userProfile && userProfile.last_name
              ? userProfile.last_name
              : "------"
          }}
        </h5>
        <label class="text-secondary">Email</label>
        <h5 class="text-primary mb-2">
          {{ userProfile && userProfile.email ? userProfile.email : "------" }}
        </h5>
        <hr />
        <div class="buttons">
          <router-link to="/main/profile/edit" tag="button">
            <button class="button is-primary mr-1">Edit</button>
          </router-link>
          <router-link to="/main/profile/edit" tag="button">
            <button class="button is-link">Change Password</button>
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <!-- <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">User Profile</div>
      </v-card-title>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">First Name</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.first_name">{{userProfile.first_name}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Last Name</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.last_name">{{userProfile.last_name}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
        <div class="my-3">
          <div class="subheading secondary--text text--lighten-3">Email</div>
          <div class="title primary--text text--darken-2" v-if="userProfile && userProfile.email">{{userProfile.email}}</div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/edit">Edit</v-btn>
        <v-btn to="/main/profile/password">Change password</v-btn>
      </v-card-actions>
    </v-card>
  </v-container> -->
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { readUserProfile } from "@/store/main/getters";

@Component
export default class UserProfile extends Vue {
  get userProfile() {
    return readUserProfile(this.$store);
  }

  public goToEdit() {
    this.$router.push("/main/profile/edit");
  }

  public goToPassword() {
    this.$router.push("/main/profile/password");
  }
}
</script>
