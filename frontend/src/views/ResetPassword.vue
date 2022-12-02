<template>
  <div class="container d-flex justify-content-center align-items-center" style="height: 99vh">
    <div class="card" style="max-width: 500px !important">
      <header class="card-header" style="background-color: #00d1b2">
        <h4 class="card-header-title m-0" style="color: white">{{ appName }} - eset Password</h4>
      </header>
      <div class="card-content">
        <div class="content">
          <p>Enter your new password below</p>
          <div class="row">
            <div class="col-12">
              <form @keyup.enter="submit">
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
              </form>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-12">
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserProfileUpdate } from "@/interfaces";
import { appName } from "@/env";
import { commitAddNotification } from "@/store/main/mutations";
import { dispatchResetPassword } from "@/store/main/actions";

@Component
export default class UserProfileEdit extends Vue {
  public appName = appName;
  public valid = true;
  public password1 = "";
  public password2 = "";

  public showP1Error: boolean = false;
  public showP2Error: boolean = false;
  public passErrorMessage: string = "";

  public mounted() {
    this.checkToken();
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
    this.$router.push("/");
  }

  public checkToken() {
    const token = this.$router.currentRoute.query.token as string;
    if (!token) {
      commitAddNotification(this.$store, {
        content: "No token provided in the URL, start a new password recovery",
        color: "error",
      });
      this.$router.push("/recover-password");
    } else {
      return token;
    }
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const token = this.checkToken();
      if (token) {
        await dispatchResetPassword(this.$store, { token, password: this.password1 });
        this.$router.push("/");
      }
    }
  }
}
</script>
