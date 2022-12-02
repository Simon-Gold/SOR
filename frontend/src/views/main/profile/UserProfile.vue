<template>
  <div class="container">
    <div class="card text-left">
      <div class="card-body">
        <h4 class="card-title text-primary">User Profile</h4>
        <hr class="mb-5" />
        <label class="text-secondary">First Name</label>
        <h5 class="text-primary mb-1">
          {{ userProfile && userProfile.first_name ? userProfile.first_name : "------" }}
        </h5>
        <label class="text-secondary">Last Name</label>
        <h5 class="text-primary mb-1">
          {{ userProfile && userProfile.last_name ? userProfile.last_name : "------" }}
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
