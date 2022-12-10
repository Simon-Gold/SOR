<template>
  <div class="container-fluid pt-2">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title text-primary"><i class="material-icons">search</i> Find Offender</h4>
            <div class="row mb-3">
              <div class="col-sm-12 col-md-4 col-lg-3">
                <div class="field">
                  <label class="label">Last Name</label>
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
              <div class="col-sm-12 col-md-4 col-lg-3">
                <div class="field">
                  <label class="label">First Name</label>
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
              <div class="col-sm-12 col-md-4 col-lg-3">
                <div class="field">
                  <label class="label">DOB</label>
                  <div class="control">
                    <input type="date" class="input" id="searchByDob" v-model="dob" @keyup.enter="searchOffenders" />
                  </div>
                </div>
              </div>
              <div class="col-sm-12 col-md-4 col-lg-3 d-flex align-items-end">
                <button class="button is-link mt-1" type="submit" @click="searchOffenders" style="max-width: 120px" :disabled="!lastName">
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
                <table class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Offender</th>
                      <th>Age</th>
                      <th>Aliases</th>
                      <th>Address</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(offender, index) in tempOffenders">
                      <td style="vertical-align: middle; width: 130px">
                        <button class="button is-info is-small" @click="setOffender(offender)">
                          <i class="material-icons mr-1">logout</i> Go Detail
                        </button>
                      </td>
                      <td>
                        <span class="d-block" v-if="offender.names[0].middle">{{ offender.names[0].middle }},</span>
                        <span class="d-block">{{ offender.names[0].last_name + " " + offender.names[0].first_name }}</span>
                      </td>
                      <td>{{ offender.age }}</td>
                      <td>
                        <span class="d-block" v-if="offender.names.length > 1" v-for="name in offender.names.slice(1)">
                          {{ name.first_name + " " + name.middle + " " + name.last_name }},
                        </span>
                      </td>
                      <td>
                        <span class="d-block" v-for="address in offender.addresses"> {{ address.line }}, </span>
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
            <hr />
            <div class="row">
              <div class="col-12">
                <nav aria-label="Page navigation example">
                  <ul class="pagination justify-content-center">
                    <li class="page-item" :class="{ disabled: currentPage == 1 }">
                      <a class="page-link" @click="prevPage">Previous</a>
                    </li>
                    <li class="page-item" v-for="page in totalPage" :class="{ active: page == currentPage }">
                      <a class="page-link" @click="setCurrentPage(page)">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage == totalPage }">
                      <a class="page-link" @click="nextPage">Next</a>
                    </li>
                  </ul>
                </nav>
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
import { ref } from "vue";

@Component
export default class Dashboard extends Vue {
  firstName = "";
  lastName = "";
  dob = "";
  showList = false;
  spinner = false;

  offenders?: IOffenders[];
  tempOffenders?: IOffenders[];

  query = "";
  offenderPerPage = 3;
  currentPage = 1;
  totalPage? = 0;
  totalOffender? = 0;

  async created() {
    this.offenders = [];
    this.tempOffenders = [];
    this.showList = false;
    this.spinner = true;
    await dispatchGetOffenders(this.$store).then((data) => {
      this.spinner = false;
      this.offenders = data?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
      this.showList = this.offenders !== undefined && this.offenders.length > 0;
      this.totalOffender = this.offenders?.length;
      this.totalPage = Math.ceil((this.totalOffender ? this.totalOffender : 0) / this.offenderPerPage);
      this.filter();
    });
  }

  prevPage() {
    this.currentPage--;
    this.filter();
  }

  nextPage() {
    this.currentPage++;
    this.filter();
  }

  setCurrentPage(pageNumber: number) {
    this.currentPage = pageNumber;
    this.filter();
  }

  filter() {
    this.tempOffenders = this.offenders?.filter((row, index) => {
      let start = (this.currentPage - 1) * this.offenderPerPage;
      let end = this.currentPage * this.offenderPerPage;
      if (index >= start && index < end) return true;
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
