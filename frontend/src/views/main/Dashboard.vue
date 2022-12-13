<template>
  <div class="container-fluid pt-2">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title text-primary" v-if="width > 725"><i class="material-icons">search</i> Search Offender</h4>
            <div class="row mb-3" v-if="width <= 725">
              <div class="accordion" id="searchAccordion">
                <div class="accordion-item">
                  <h2 class="accordion-header" id="headingOne">
                    <button
                      class="accordion-button collapsed"
                      type="button"
                      data-bs-toggle="collapse"
                      data-bs-target="#collapseOne"
                      aria-expanded="true"
                      aria-controls="collapseOne"
                    >
                      <i class="material-icons">search</i> Search Offender
                    </button>
                  </h2>
                  <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#searchAccordion">
                    <div class="accordion-body">
                      <div class="row">
                        <div class="col-12">
                          <div class="field">
                            <label class="label">Last Name</label>
                            <div class="control">
                              <input type="text" class="input" id="searchByLName" v-model="lastName" />
                            </div>
                          </div>
                          <div class="field">
                            <label class="label">First Name</label>
                            <div class="control">
                              <input type="text" class="input" id="searchByFName" v-model="firstName" :disabled="!lastName" />
                            </div>
                          </div>
                          <div class="field">
                            <label class="label">DOB</label>
                            <div class="control">
                              <input type="date" class="input" id="searchByDob" v-model="dob" :disabled="!lastName" />
                            </div>
                          </div>
                        </div>
                        <div class="col-12 d-flex align-items-end">
                          <div class="buttons mt-1 justify-content-end">
                            <button
                              class="button is-danger"
                              data-bs-toggle="collapse"
                              data-bs-target="#collapseOne"
                              @click="clearFilter"
                              v-show="lastName"
                            >
                              Clear Filter
                            </button>
                            <button
                              class="button is-link"
                              data-bs-toggle="collapse"
                              data-bs-target="#collapseOne"
                              @click="searchOffenders"
                              :disabled="!lastName"
                            >
                              Search
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="row mb-3" v-if="width > 725">
              <div class="col-sm-12 col-md-4" :class="{ 'col-lg-4': width < 1200, 'col-lg-3': width >= 1200 }">
                <div class="field">
                  <label class="label">Last Name</label>
                  <div class="control">
                    <input type="text" class="input" id="searchByLName" v-model="lastName" />
                  </div>
                </div>
              </div>
              <div class="col-sm-12 col-md-4" :class="{ 'col-lg-4': width < 1200, 'col-lg-3': width >= 1200 }">
                <div class="field">
                  <label class="label">First Name</label>
                  <div class="control">
                    <input type="text" class="input" id="searchByFName" v-model="firstName" :disabled="!lastName" />
                  </div>
                </div>
              </div>
              <div class="col-sm-12 col-md-4" :class="{ 'col-lg-4': width < 1200, 'col-lg-3': width >= 1200 }">
                <div class="field">
                  <label class="label">DOB</label>
                  <div class="control">
                    <input type="date" class="input" id="searchByDob" v-model="dob" :disabled="!lastName" />
                  </div>
                </div>
              </div>
              <div class="col-sm-12 col-md-12 d-flex align-items-end" :class="{ 'col-lg-12': width < 1200, 'col-lg-3': width >= 1200 }">
                <div class="buttons mt-1 align-items-center" :class="{ 'justify-content-end': width < 1200 }">
                  <button class="button is-link" @click="searchOffenders" :disabled="!lastName">Search</button>
                  <button class="button is-danger" v-show="lastName" @click="clearFilter">Clear Filter</button>
                </div>
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
                <div class="box" :class="{ 'p-0': width <= 725 }" style="overflow: auto; max-height: 750px; min-height: 560px">
                  <div class="card mb-1" v-if="width <= 725" v-for="(offender, index) in tempOffenders">
                    <div class="card-body">
                      <h5 class="card-title text-info">
                        {{ offender.names[0].first_name + " " + offender.names[0].middle + " " + offender.names[0].last_name }}
                      </h5>
                      <hr class="my-1" />
                      <label class="d-block">
                        <strong>DOB:</strong> {{ offender.dob.month + "/" + offender.dob.day + "/" + offender.dob.year }}
                      </label>
                      <label class="d-block"><strong>Address:</strong> {{ offender.addresses[0].line }}</label>
                      <hr class="my-1" />
                      <button class="button is-info is-small" @click="setOffender(offender)" style="float: right">
                        <i class="fa-solid fa-circle-info mr-1"></i> Go Detail
                      </button>
                    </div>
                  </div>
                  <table class="table table-striped table-bordered table-hover" v-if="width > 725">
                    <thead>
                      <tr>
                        <th class="col-3" v-for="header in tableHeader">
                          <span style="width: 98%">{{ header.displayName }}</span>
                          <i class="fa-solid mt-1" :class="header.class" @click="sort(header.propName)"></i>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(offender, index) in tempOffenders">
                        <td>
                          <button type="button" class="btn btn-link" @click="setOffender(offender)">
                            {{ offender.names[0].first_name + " " + offender.names[0].middle + " " + offender.names[0].last_name }}
                          </button>
                        </td>
                        <td>{{ offender.dob.month + "/" + offender.dob.day + "/" + offender.dob.year }}</td>
                        <td>
                          <span class="d-block" v-for="address in offender.addresses"> {{ address.line }}, </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
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
  isSearched = false;

  offenders?: IOffenders[];
  tempOffenders?: IOffenders[];

  query = "";
  offenderPerPage = 6;
  currentPage = 1;
  totalPage? = 0;
  totalOffender? = 0;

  tableHeader: { displayName: string; propName: string; sortType: string; class: string }[] = [
    { displayName: "Offender", propName: "first_name", sortType: "default", class: "fa-sort" },
    { displayName: "DOB", propName: "dob", sortType: "default", class: "fa-sort" },
    { displayName: "Address", propName: "addresses", sortType: "default", class: "fa-sort" },
  ];

  width = window.innerWidth;

  async created() {
    window.addEventListener("resize", this.resizeHandler);
    await this.getOffenders();
  }

  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  }

  resizeHandler(e) {
    this.width = e.target.innerWidth;
  }

  async getOffenders() {
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

  async searchOffenders() {
    if (this.lastName) {
      this.isSearched = true;
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
        this.offenders = data?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
        this.showList = this.offenders !== undefined && this.offenders.length > 0;
        this.totalOffender = this.offenders?.length;
        this.totalPage = Math.ceil((this.totalOffender ? this.totalOffender : 0) / this.offenderPerPage);
        this.filter();
      });
    } else {
      await this.getOffenders();
    }
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

  clearFilter() {
    if (this.isSearched) {
      this.lastName = "";
      this.firstName = "";
      this.dob = "";
      this.getOffenders();
    } else {
      this.lastName = "";
      this.firstName = "";
      this.dob = "";
      this.isSearched = false;
    }
  }

  sort(pName: string) {
    let sortType = "";
    this.tableHeader.forEach((th) => {
      if (pName === th.propName) {
        if (th.sortType === "default") {
          th.sortType = "up";
          th.class = "fa-sort-up";
        } else if (th.sortType === "up") {
          th.sortType = "down";
          th.class = "fa-sort-down";
        } else {
          th.sortType = "default";
          th.class = "fa-sort";
        }
        sortType = th.sortType;
      } else {
        th.sortType = "default";
        th.class = "fa-sort";
      }
    });

    this.offenders = this.offenders?.sort((a, b) => a.names[0].last_name.localeCompare(b.names[0].last_name));

    switch (pName) {
      case "first_name": {
        if (sortType === "up") this.offenders = this.offenders?.sort((a, b) => b.names[0].first_name.localeCompare(a.names[0].first_name));
        else if (sortType === "down")
          this.offenders = this.offenders?.sort((a, b) => a.names[0].first_name.localeCompare(b.names[0].first_name));
        else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
        break;
      }
      case "dob": {
        if (sortType === "up")
          this.offenders = this.offenders?.sort((a, b) => {
            a[`aDate`] = new Date(a.dob.month + "/" + a.dob.day + "/" + a.dob.year);
            b[`bDate`] = new Date(b.dob.month + "/" + b.dob.day + "/" + b.dob.year);
            return b[`bDate`] - a[`aDate`];
          });
        else if (sortType === "down")
          this.offenders = this.offenders?.sort((a, b) => {
            a[`aDate`] = new Date(a.dob.month + "/" + a.dob.day + "/" + a.dob.year);
            b[`bDate`] = new Date(b.dob.month + "/" + b.dob.day + "/" + b.dob.year);
            return a[`bDate`] - b[`aDate`];
          });
        else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
        break;
      }
      case "addresses": {
        if (sortType === "up") this.offenders = this.offenders?.sort((a, b) => b.addresses[0].line.localeCompare(a.addresses[0].line));
        else if (sortType === "down")
          this.offenders = this.offenders?.sort((a, b) => a.addresses[0].line.localeCompare(b.addresses[0].line));
        else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
        break;
      }
      default:
        break;
    }

    this.filter();
  }

  setOffender(data: IOffenders) {
    let hashData = btoa(JSON.stringify(data));
    sessionStorage.setItem("offender", hashData);
    let routeData = this.$router.resolve({ name: "main-offender" });
    window.open(routeData.href, "_blank");
  }
}
</script>
<style>
.alert .material-icons {
  position: relative;
  top: 5px;
  margin-right: 5px;
}
.box .table thead th {
  border-width: 0px 1px 2px;
  color: #fff;
  background-color: #333;
}

.box .table thead th i {
  float: right;
  margin-top: 4px;
  cursor: pointer;
}
</style>
