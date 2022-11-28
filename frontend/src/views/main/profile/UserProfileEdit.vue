<template>
  <v-container fluid>

    <div class="container">
      <div class="row">
        <div class="col-12">
          <h6 class="m-0">Edit User Profile</h6>
        </div>
      </div>
      <hr>
      <div class="row ">
        <div class="col-12">
          <div class="field">
            <label class="label">First Name</label>
            <div class="control">
              <input class="input" :class="{'is-danger': showFNError}" type="text" v-model="firstName" @input="checkFN" placeholder="Enter First Name">
            </div>
            <p class="help is-danger" v-if="showFNError">Please enter first name</p>
          </div>
          <div class="field">
            <label class="label">Last Name</label>
            <div class="control">
              <input class="input" :class="{'is-danger': showFNError}" type="text" v-model="lastName" @input="checkLN" placeholder="Enter last name">
            </div>
            <p class="help is-danger" v-if="showLNError">Please enter last name</p>
          </div>
          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left has-icons-right">
              <input class="input" :class="{'is-danger': showFNError}" type="email" v-model="email" @input="checkEmail" placeholder="Enter email address">
              <span class="icon is-small is-left">
                <i class="material-icons">mail</i>
              </span>
              <span class="icon is-small is-right" v-if="showEmailError">
                <i class="material-icons">warning</i>
              </span>
            </div>
            <p class="help is-danger"  v-if="showEmailError">{{emailErrorMessage}}</p>
          </div>
        </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-12 text-right">
          <div class="buttons" style="justify-content: flex-end;">
            <button class="button is-dark" @click="cancel">Cancel</button>
            <button class="button is-warning" @click="reset">Reset</button>
            <button class="button is-success" @click="submit" :disabled="!valid">Save</button>
          </div>
        </div>
      </div>
    </div>


    <!-- <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit User Profile</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="First Name" v-model="firstName" required></v-text-field>
            <v-text-field label="Last Name" v-model="lastName" required></v-text-field>
            <v-text-field label="E-mail" type="email" v-model="email" v-validate="'required|email'" data-vv-name="email"
              :error-messages="errors.collect('email')" required></v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
          Save
        </v-btn>
      </v-card-actions>
    </v-card> -->
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfileUpdate } from '@/interfaces';
import { readUserProfile } from '@/store/main/getters';
import { dispatchUpdateUserProfile } from '@/store/main/actions';

@Component
export default class UserProfileEdit extends Vue {
  public valid = true;
  public firstName: string = '';
  public lastName: string = '';
  public email: string = '';

  public showFNError: boolean = false;
  public showLNError: boolean = false;
  public showEmailError: boolean = false;
  public emailErrorMessage: string = '';
  public regex = new RegExp('/^\S+@\S+\.\S+$/', 'gi');

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
        this.emailErrorMessage = 'This email address invalid';
      } else {
        this.showEmailError = false;
      }
    } else {
      this.showEmailError = true;
      this.emailErrorMessage = 'Please enter email address';
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
    if ((this.$refs.form as any).validate()) {
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
      this.$router.push('/main/profile');
    }
  }
}
</script>
