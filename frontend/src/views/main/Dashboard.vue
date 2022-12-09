<template>
  <div class="container-fluid pt-2">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title text-primary"><i class="material-icons">search</i> Find Offender</h4>
            <div class="row mb-3">
              <div class="col">
                <div class="field">
                  <label class="label">Search By Last Name</label>
                  <div class="control">
                    <input
                      type="text"
                      class="input"
                      id="searchByLName"
                      v-model="lastName"
                      @keyup.enter="searchOffenders"
                      autocomplete="off"
                    />
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="field">
                  <label class="label">Search By First Name</label>
                  <div class="control">
                    <input
                      type="text"
                      class="input"
                      id="searchByFName"
                      v-model="firstName"
                      @keyup.enter="searchOffenders"
                      autocomplete="off"
                    />
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="field">
                  <label class="label">Search By DOB</label>
                  <div class="control">
                    <input type="date" class="input" id="searchByDob" v-model="dob" @keyup.enter="searchOffenders" />
                  </div>
                </div>
              </div>
              <div class="col d-flex align-items-end">
                <button class="button is-link" type="submit" @click="searchOffenders" style="max-width: 120px" :disabled="!lastName">
                  <i class="material-icons">search</i> Search
                </button>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-12 text-center" v-show="spinner">
                <div class="spinner-border" style="width: 3rem; height: 3rem" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div class="col-12" v-if="showList">
                <table class="table table-striped table-hover">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Offender Name</th>
                      <th>Date of Birth</th>
                      <th>Race</th>
                      <th>Sex</th>
                      <th>Height</th>
                      <th>Weight</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(offender, index) in offenders">
                      <td>{{ index + 1 }}</td>
                      <td>{{ offender.names[0].first_name + " " + offender.names[0].middle + " " + offender.names[0].last_name }}</td>
                      <td>{{ offender.dob.month + "/" + offender.dob.day + "/" + offender.dob.year }}</td>
                      <td>{{ offender.demographic.race }}</td>
                      <td>{{ offender.demographic.sex }}</td>
                      <td>{{ offender.demographic.height }}</td>
                      <td>{{ offender.demographic.weight }}</td>
                      <td style="text-align: right">
                        <button class="button is-info is-small" @click="setOffender(offender)">
                          <i class="material-icons">info</i> Go to Detail
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="col-12" v-if="!showList && !spinner">
                <div class="alert alert-info" role="alert">
                  <i class="material-icons">info</i>
                  <span>The offenders to display was not found.</span>
                </div>
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
import { readOffenders } from "@/store/main/getters";
import { dispatchGetOffenders, dispatchSearchOffenders } from "@/store/main/actions";
import { IOffenders } from "@/interfaces";

@Component
export default class Dashboard extends Vue {
  firstName = "";
  lastName = "";
  dob = "";

  showList = false;
  spinner = false;

  offenders: IOffenders[] | undefined;

  query = "";

  async created() {
    this.offenders = [];
    this.showList = false;
    this.spinner = true;
    await dispatchGetOffenders(this.$store).then((data) => {
      this.spinner = false;
      this.offenders = data;
      this.showList = this.offenders !== undefined && this.offenders.length > 0;
    });
  }

  async searchOffenders() {
    if (this.lastName) {
      this.offenders = [];
      this.showList = false;
      this.spinner = true;
      this.query = "";
      this.query = "?last=" + this.lastName;
      if (this.firstName) {
        this.query += "&first=" + this.firstName;
      }
      if (this.dob) {
        const strDob = new Date(this.dob).toLocaleDateString("en-US");
        this.query += "&dob=" + strDob;
      }

      await dispatchSearchOffenders(this.$store, { query: this.query }).then((data) => {
        this.spinner = false;
        this.offenders = data;
        this.showList = this.offenders !== undefined && this.offenders.length > 0;
      });
    } else {
      alert("The last name is required");
    }
  }

  setOffender(data: IOffenders) {
    let hashData = btoa(JSON.stringify(data));
    sessionStorage.setItem("offender", hashData);
    this.$router.push({ name: "main-offender" });
  }
}
</script>
<style>
.alert .material-icons {
  position: relative;
  top: 5px;
  margin-right: 5px;
}
</style>
