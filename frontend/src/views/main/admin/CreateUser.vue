<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <form>
          <div class="card">
            <div class="card-body">
              <h4 class="card-title text-primary">Create User</h4>
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
                        required
                      />
                    </div>
                    <p class="help is-danger" v-if="showFNError">Please enter first name</p>
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
                        required
                      />
                    </div>
                    <p class="help is-danger" v-if="showLNError">Please enter last name</p>
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
                        required
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
                  <div class="field">
                    <label class="label">Username</label>
                    <div class="control">
                      <input
                        class="input"
                        :class="{ 'is-danger': showUNError }"
                        type="text"
                        v-model="username"
                        @input="checkUN"
                        placeholder="Enter username"
                        required
                      />
                    </div>
                    <p class="help is-danger" v-if="showUNError">Please enter username</p>
                  </div>
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="isSuperuser" />
                        User is superuser ({{ isSuperuser ? "currently is a superuser" : "currently is not a superuser" }})
                      </label>
                    </div>
                  </div>
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="isActive" />
                        User is active ({{ isActive ? "currently active" : "currently not active" }})
                      </label>
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
                        placeholder="Enter password"
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
                    <button type="button" class="button is-dark" @click="cancel">Cancel</button>
                    <button type="button" class="button is-warning" @click="reset">Reset</button>
                    <button
                      type="submit"
                      class="button is-success"
                      @click="submit"
                      :disabled="showEmailError || showFNError || showLNError || showP1Error || showP2Error || showUNError"
                    >
                      Save
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from "@/interfaces";
import { dispatchGetUsers, dispatchCreateUser } from "@/store/admin/actions";

@Component
export default class CreateUser extends Vue {
  public valid = false;
  public fullName: string = "";
  public firstName: string = "";
  public lastName: string = "";
  public username: string = "";
  public email: string = "";
  public isActive: boolean = true;
  public isSuperuser: boolean = false;
  public setPassword = false;
  public password1: string = "";
  public password2: string = "";

  public showFNError: boolean = false;
  public showLNError: boolean = false;
  public showUNError: boolean = false;
  public showEmailError: boolean = false;
  public emailErrorMessage: string = "";
  public regex = /^\S+@\S+\.\S+$/gi;

  public showP1Error: boolean = false;
  public showP2Error: boolean = false;
  public passErrorMessage: string = "";

  checkFN() {
    this.showFNError = this.firstName.length > 0 ? false : true;
  }

  checkLN() {
    this.showLNError = this.lastName.length > 0 ? false : true;
  }

  checkUN() {
    this.showUNError = this.username.length > 0 ? false : true;
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

  public async mounted() {
    // await dispatchGetUsers(this.$store);
    this.reset();
  }

  public reset() {
    this.password1 = "";
    this.password2 = "";
    this.fullName = "";
    this.firstName = "";
    this.lastName = "";
    this.username = "";
    this.email = "";
    this.isActive = true;
    this.isSuperuser = false;
    this.showEmailError = false;
    this.showFNError = false;
    this.showLNError = false;
    this.showP1Error = false;
    this.showP2Error = false;
    this.showUNError = false;
    this.$validator.reset();
  }

  public cancel() {
    // this.$router.back();
    this.$router.push("/main/admin/users/all");
  }

  public async submit() {
    const updatedProfile: IUserProfileCreate = {
      email: this.email,
      first_name: this.firstName,
      last_name: this.lastName,
      username: this.username,
    };
    if (this.fullName) {
      updatedProfile.full_name = this.fullName;
    }
    if (this.firstName) {
      updatedProfile.first_name = this.firstName;
    }
    if (this.lastName) {
      updatedProfile.last_name = this.lastName;
    }
    if (this.username) {
      updatedProfile.username = this.username;
    }
    if (this.email) {
      updatedProfile.email = this.email;
    }
    updatedProfile.is_active = this.isActive;
    updatedProfile.is_superuser = this.isSuperuser;
    updatedProfile.password = this.password1;
    await dispatchCreateUser(this.$store, updatedProfile);
    this.$router.push("/main/admin/users/all");
  }
}
</script>
