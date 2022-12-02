<template>
  <div class="container">
    <div class="card text-left">
      <div class="card-body">
        <h4 class="card-title text-primary">Set Password</h4>
        <hr />
        <div class="row">
          <div class="col-12">
            <div class="field">
              <label class="label text-primary">User</label>
              <div class="control has-icons-left">
                <input class="input" type="text" :value="fName" readonly />
                <span class="icon is-small is-left">
                  <i class="material-icons">person</i>
                </span>
              </div>
            </div>
            <div class="field">
              <label class="label">Password</label>
              <div class="control has-icons-right">
                <input
                  class="input"
                  :class="{ 'is-danger': showP1Error }"
                  type="password"
                  v-model="password1"
                  @input="checkPass1"
                  placeholder="Enter password"
                />
                <span class="icon is-small is-right" v-if="showP1Error">
                  <i class="material-icons">warning</i>
                </span>
              </div>
              <p class="help is-danger" v-if="showP1Error">The password field is required</p>
            </div>
            <div class="field">
              <label class="label">Confirm Password</label>
              <div class="control has-icons-right">
                <input
                  class="input"
                  :class="{ 'is-danger': showP2Error }"
                  type="password"
                  v-model="password2"
                  @input="checkPass2"
                  placeholder="Enter confirm password"
                />
                <span class="icon is-small is-right" v-if="showP2Error">
                  <i class="material-icons">warning</i>
                </span>
              </div>
              <p class="help is-danger" v-if="showP2Error">
                {{ passErrorMessage }}
              </p>
            </div>
          </div>
        </div>
        <hr />
        <div class="row">
          <div class="col-12 text-right">
            <div class="buttons" style="justify-content: flex-end">
              <button class="button is-dark" @click="cancel">Cancel</button>
              <button class="button is-warning" @click="reset">Reset</button>
              <button class="button is-success" @click="submit" :disabled="showP1Error || showP2Error">Save</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserProfileUpdate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchUpdateUserProfile } from "@/store/main/actions";

@Component
export default class UserProfileEdit extends Vue {
  public valid = true;
  public password1 = "";
  public password2 = "";

  public showP1Error: boolean = false;
  public showP2Error: boolean = false;
  public passErrorMessage: string = "";

  get userProfile() {
    return readUserProfile(this.$store);
  }

  get fName() {
    const user = readUserProfile(this.$store);
    if (user?.first_name || user?.last_name) {
      return user.first_name + " " + user.last_name;
    } else {
      return user?.email;
    }
  }

  public checkPass1() {
    this.showP1Error = this.password1.length > 0 ? false : true;
  }

  public checkPass2() {
    if (this.password2.length > 0) {
      if (this.password2 !== this.password1) {
        this.showP2Error = true;
        this.passErrorMessage = "The password confirmation does not match";
      } else {
        this.showP2Error = false;
      }
    } else {
      this.showP2Error = true;
      this.passErrorMessage = "The password field is required";
    }
  }

  public reset() {
    this.password1 = "";
    this.password2 = "";
    this.showP1Error = true;
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      updatedProfile.password = this.password1;
      await dispatchUpdateUserProfile(this.$store, updatedProfile);
      this.$router.push("/main/profile");
    }
  }
}
</script>
