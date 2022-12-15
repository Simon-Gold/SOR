<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <form>
          <div class="card">
            <div class="card-body">
              <h4 class="card-title text-primary">Edit User</h4>
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
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="setPassword" />
                        Set Password
                      </label>
                    </div>
                  </div>
                  <div class="field" v-show="setPassword">
                    <label class="label">Password</label>
                    <div class="control has-icons-right">
                      <input
                        class="input"
                        :class="{ 'is-danger': showP1Error }"
                        type="password"
                        v-model="password1"
                        @input="checkPass1"
                        placeholder="Set password"
                      />
                      <span class="icon is-small is-right" v-if="showP1Error">
                        <i class="material-icons">warning</i>
                      </span>
                    </div>
                    <p class="help is-danger" v-if="showP1Error">The password field is required</p>
                  </div>
                  <div class="field" v-show="setPassword">
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
import { IUserProfile, IUserProfileUpdate } from "@/interfaces";
import { dispatchGetUser, dispatchUpdateUser } from "@/store/admin/actions";
import { readAdminOneUser } from "@/store/admin/getters";

@Component
export default class EditUser extends Vue {
  public valid = true;
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

  user?: IUserProfile;

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

  public async created() {
    await dispatchGetUser(this.$store, { id: this.$router.currentRoute.params.id }).then((data) => {
      this.user = data;
    });
    this.reset();
  }

  public reset() {
    this.setPassword = false;
    this.password1 = "";
    this.password2 = "";
    this.showEmailError = false;
    this.showFNError = false;
    this.showLNError = false;
    this.showP1Error = false;
    this.showP2Error = false;
    this.showUNError = false;
    this.$validator.reset();
    if (this.user) {
      this.firstName = this.user.first_name;
      this.lastName = this.user.last_name;
      this.username = this.user.username;
      this.email = this.user.email;
      this.isActive = this.user.is_active;
      this.isSuperuser = this.user.is_superuser;
    }
  }

  public cancel() {
    this.$router.push({ name: "main-admin-users" });
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
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
      if (this.setPassword) {
        updatedProfile.password = this.password1;
      }
      await dispatchUpdateUser(this.$store, {
        id: this.user!.id,
        user: updatedProfile,
      });
      this.$router.push({ name: "main-admin-users" });
    }
  }
}
</script>
