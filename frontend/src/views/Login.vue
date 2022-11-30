<template>
  <div class="container d-flex justify-content-center align-items-center">
    <div class="card" style="max-width: 400px !important">
      <header class="card-header" style="background-color: #00d1b2">
        <h4 class="card-header-title m-0" style="color: white">
          {{ appName }}
        </h4>
      </header>
      <div class="card-content">
        <div class="content">
          <div class="row">
            <div class="col-12">
              <form @keyup.enter="submit">
                <div class="field">
                  <label class="label">Login</label>
                  <div class="control has-icons-left">
                    <input type="text" class="input" v-model="email" />
                    <span class="icon is-small is-left">
                      <i class="material-icons">person</i>
                    </span>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Password</label>
                  <div class="control has-icons-left">
                    <input type="password" class="input" v-model="password" />
                    <span class="icon is-small is-left">
                      <i class="material-icons">lock</i>
                    </span>
                  </div>
                </div>
              </form>
            </div>
            <div class="col-12">
              <router-link to="/recover-password"
                >Forgot your password?</router-link
              >
            </div>
            <div class="col-12 mt-2" v-if="loginError">
              <div class="alert alert-danger" role="alert">
                <i
                  class="material-icons mr-2"
                  style="position: relative; top: 5px"
                  >warning</i
                >
                <span>Incorrect email or password</span>
              </div>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-12">
              <button
                style="float: right"
                type="submit"
                class="button is-link"
                @click.prevent="submit"
              >
                Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{ appName }}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field
                  @keyup.enter="submit"
                  v-model="email"
                  prepend-icon="person"
                  name="login"
                  label="Login"
                  type="text"
                ></v-text-field>
                <v-text-field
                  @keyup.enter="submit"
                  v-model="password"
                  prepend-icon="lock"
                  name="password"
                  label="Password"
                  id="password"
                  type="password"
                ></v-text-field>
              </v-form>
              <div v-if="loginError">
                <v-alert
                  :value="loginError"
                  transition="fade-transition"
                  type="error"
                >
                  Incorrect email or password
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right"
                ><router-link to="/recover-password"
                  >Forgot your password?</router-link
                ></v-flex
              >
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content> -->
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";
import { appName } from "@/env";
import { readLoginError } from "@/store/main/getters";
import { dispatchLogIn } from "@/store/main/actions";

@Component
export default class Login extends Vue {
  public email: string = "";
  public password: string = "";
  public appName = appName;

  public get loginError() {
    return readLoginError(this.$store);
  }

  public submit() {
    dispatchLogIn(this.$store, {
      username: this.email,
      password: this.password,
    });
  }
}
</script>

<style></style>
