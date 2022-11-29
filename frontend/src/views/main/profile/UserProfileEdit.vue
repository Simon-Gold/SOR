<template>
  <div class="container">
    <div class="card text-left">
      <div class="card-body">
        <h4 class="card-title text-primary">Edit User Profile</h4>
        <hr />
        <div class="row">
          <div class="col-12">
            <div class="field">
              <label class="label">First Name</label>
              <div class="control">
                <input
                  class="input"
                  :class="{ 'is-danger': showFNError }"
                  type="text"
                  v-model="firstName"
                  @input="checkFN"
                  placeholder="Enter First Name"
                />
              </div>
              <p class="help is-danger" v-if="showFNError">
                Please enter first name
              </p>
            </div>
            <div class="field">
              <label class="label">Last Name</label>
              <div class="control">
                <input
                  class="input"
                  :class="{ 'is-danger': showLNError }"
                  type="text"
                  v-model="lastName"
                  @input="checkLN"
                  placeholder="Enter last name"
                />
              </div>
              <p class="help is-danger" v-if="showLNError">
                Please enter last name
              </p>
            </div>
            <div class="field">
              <label class="label">Email</label>
              <div class="control has-icons-left has-icons-right">
                <input
                  class="input"
                  :class="{ 'is-danger': showEmailError }"
                  type="email"
                  v-model="email"
                  @input="checkEmail"
                  placeholder="Enter email address"
                />
                <span class="icon is-small is-left">
                  <i class="material-icons">mail</i>
                </span>
                <span class="icon is-small is-right" v-if="showEmailError">
                  <i class="material-icons">warning</i>
                </span>
              </div>
              <p class="help is-danger" v-if="showEmailError">
                {{ emailErrorMessage }}
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
              <button
                class="button is-success"
                @click="submit"
                :disabled="showEmailError || showFNError || showLNError"
              >
                Save
              </button>
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
  public firstName: string = "";
  public lastName: string = "";
  public email: string = "";

  public showFNError: boolean = false;
  public showLNError: boolean = false;
  public showEmailError: boolean = false;
  public emailErrorMessage: string = "";
  public regex = /^\S+@\S+\.\S+$/gi;

  $refs!: {
    form: HTMLFormElement;
  };

  public created() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      this.firstName = userProfile.first_name;
      this.lastName = userProfile.last_name;
      this.email = userProfile.email;
    }
  }

  checkFN() {
    this.showFNError = this.firstName.length > 0 ? false : true;
  }

  checkLN() {
    this.showLNError = this.lastName.length > 0 ? false : true;
  }

  checkEmail() {
    if (this.email.length > 0) {
      if (!this.email.match(this.regex)) {
        this.showEmailError = true;
        this.emailErrorMessage = "This email address invalid";
      } else {
        this.showEmailError = false;
      }
    } else {
      this.showEmailError = true;
      this.emailErrorMessage = "Please enter email address";
    }
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }

  public reset() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      this.firstName = userProfile.first_name;
      this.lastName = userProfile.last_name;
      this.email = userProfile.email;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    const updatedProfile: IUserProfileUpdate = {};
    if (this.firstName) {
      updatedProfile.first_name = this.firstName;
    }
    if (this.lastName) {
      updatedProfile.last_name = this.lastName;
    }
    if (this.email) {
      updatedProfile.email = this.email;
    }
    await dispatchUpdateUserProfile(this.$store, updatedProfile);
    this.$router.push("/main/profile");
  }
}
</script>
