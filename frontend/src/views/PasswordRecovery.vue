<template>
  <div class="container d-flex justify-content-center align-items-center" style="height: 99vh">
    <div class="card" style="max-width: 500px !important">
      <header class="card-header" style="background-color: #00d1b2">
        <h4 class="card-header-title m-0" style="color: white">{{ appName }} - Password Recovery</h4>
      </header>
      <div class="card-content">
        <div class="content">
          <p>A password recovery email will be sent to the registered account</p>
          <div class="row">
            <div class="col-12">
              <form @keyup.enter="submit">
                <div class="field">
                  <label class="label">Username</label>
                  <div class="control has-icons-left">
                    <input type="text" class="input" v-model="username" @keyup.enter="submit" @input="checkUN" required />
                    <span class="icon is-small is-left">
                      <i class="material-icons">person</i>
                    </span>
                  </div>
                  <p class="help is-danger" v-if="showError">This username field is required</p>
                </div>
              </form>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-12">
              <div class="buttons" style="float: right">
                <button type="button" class="button is-dark" @click="cancel">Login</button>
                <button type="submit" class="button is-link" @click.prevent="submit" :disabled="!username">Recover Password</button>
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
import { appName } from "@/env";
import { dispatchPasswordRecovery } from "@/store/main/actions";

@Component
export default class Login extends Vue {
  public valid = true;
  public username: string = "";
  public appName = appName;

  public showError = false;

  public checkUN() {
    this.showError = this.username.length > 0 ? false : true;
  }

  public cancel() {
    this.$router.back();
  }

  public submit() {
    dispatchPasswordRecovery(this.$store, { username: this.username });
  }
}
</script>

<style></style>
