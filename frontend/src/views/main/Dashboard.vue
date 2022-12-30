<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <h4>Offenders List</h4>
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
        <div class="box p-0" style="overflow: auto; max-height: 750px; min-height: 560px">
          <div class="card mb-1" v-if="width <= 725" v-for="(offender, index) in offenders">
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
          <table class="table table-striped table-bordered table-hover mb-0" v-if="width > 725">
            <thead>
              <tr>
                <th class="col-3" v-for="header in tableHeader">
                  <span style="width: 98%">{{ header.displayName }}</span>
                  <!-- <i class="fa-solid mt-1" :class="header.class" @click="sort(header.propName)"></i> -->
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(offender, index) in offenders">
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
      <div class="col-12 my-2" v-if="isError && msgError">
        <div class="card alert alert-danger">
          <div class="card-header">
            <i class="material-icons">error</i>
            {{ msgError["message"] }}
          </div>
          <div class="card-body">
            {{ msgError["description"] }}
          </div>
        </div>
      </div>
      <div class="col-12" v-else-if="!showList && !spinner">
        <div class="alert alert-info" role="alert">
          <i class="material-icons">info</i>
          <span>The offenders to display was not found.</span>
        </div>
      </div>
    </div>
    <hr />
    <div class="row" v-if="!isSearched">
      <div class="col-12">
        <nav aria-label="Page navigation example">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage == 1 }">
              <a class="page-link" @click="goPrev()">Previous</a>
            </li>
            <li class="page-item" v-for="page in totalPages" :class="{ active: page == currentPage }">
              <a class="page-link" @click="setCurrentPage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage == totalPages }">
              <a class="page-link" @click="goNext()">Next</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { readOffenders } from "@/store/main/getters";
import { dispatchGetOffenders, dispatchSearchOffenders } from "@/store/main/actions";
import { IOffenders, IOffenderPageModel } from "@/interfaces";
import { ref } from "vue";
import { apiAuthURL, apiSorURL } from "@/env";

@Component
export default class Dashboard extends Vue {
  firstName = "";
  lastName = "";
  dob = "";
  showList = false;
  spinner = false;
  isSearched = false;
  isError = false;
  msgError = "";

  offenders?: IOffenders[];

  query = "";
  offenderPerPage = 6;
  totalPages? = 0;
  totalItems? = 0;
  currentPage? = 1;
  pageLimit = 10;
  nextUrl?: string;
  prevUrl?: string;

  tableHeader: { displayName: string; propName: string; sortType: string; class: string }[] = [
    { displayName: "Offender", propName: "first_name", sortType: "default", class: "fa-sort" },
    { displayName: "DOB", propName: "dob", sortType: "default", class: "fa-sort" },
    { displayName: "Address", propName: "addresses", sortType: "default", class: "fa-sort" },
  ];

  width = window.innerWidth;

  searchText = "";

  async created() {
    window.addEventListener("resize", this.resizeHandler);

    this.$parent?.$on("sendSearchText", this.searchFromMain);
    this.$parent?.$on("clearSearchText", this.clearFilter);

    await this.getOffenders("");
  }

  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  }

  resizeHandler(e) {
    this.width = e.target.innerWidth;
  }

  async getOffenders(url: string) {
    let payload = { url: url };
    this.offenders = [];
    this.showList = false;
    this.spinner = true;
    await dispatchGetOffenders(this.$store, payload).then((data) => {
      this.spinner = false;
      this.offenders = data?.items?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
      this.showList = this.offenders !== undefined && this.offenders.length > 0;
      this.totalItems = data?.total_items;
      this.totalPages = data?.total_pages;
      this.nextUrl = data?.next;
      this.prevUrl = data?.prev;
      this.currentPage = data?.current_page;
    });
  }

  async goNext() {
    let next = this.nextUrl ? this.nextUrl : "";
    await this.getOffenders(next);
  }

  async goPrev() {
    let prev = this.prevUrl ? this.prevUrl : "";
    await this.getOffenders(prev);
  }

  async setCurrentPage(page: number) {
    let query = "?page=" + page;
    let url = `${apiSorURL}/api/v1/offenders/${query}`;
    await this.getOffenders(url);
  }

  async searchFromMain(event?: any) {
    if (event) {
      this.searchText = event;
      await this.search();
    }
  }

  async search() {
    if (this.searchText) {
      let split = this.searchText.trim().replace(/\s\s+/g, " ").split(" ");
      this.isSearched = true;
      this.offenders = [];
      this.showList = false;
      this.spinner = true;
      this.query = "";
      this.query = "?last=" + split[0];
      if (split[1]) {
        this.query += "&first=" + split[1];
        if (split[2]) {
          this.query += "&dob=" + split[2];
        }
      }
      await dispatchSearchOffenders(this.$store, { query: this.query })
      .then((data) => {
        this.spinner = false;
        this.offenders = data?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
        this.showList = this.offenders !== undefined && this.offenders.length > 0;
        this.totalItems = this.offenders?.length;
        this.totalPages = Math.ceil((this.totalItems ? this.totalItems : 0) / this.offenderPerPage);
        this.isError = false;
      })
      .catch(error =>{
        const error_data = error.response.data;
        if(error_data.code){
          this.isError = true;
          this.msgError = error_data;
          this.showList = false;
          this.spinner = false;
        }
      });
    } else {
      this.getOffenders("");
    }
  }

  async clearFilter() {
    if (this.isSearched) {
      this.lastName = "";
      this.firstName = "";
      this.dob = "";
      this.searchText = "";
      this.isSearched = false;
      this.isError = false;
      await this.getOffenders("");
    } else {
      this.lastName = "";
      this.firstName = "";
      this.dob = "";
      this.searchText = "";
      this.isSearched = false;
    }
  }

  //#region sorting will edit
  // sort(pName: string) {
  //   let sortType = "";
  //   this.tableHeader.forEach((th) => {
  //     if (pName === th.propName) {
  //       if (th.sortType === "default") {
  //         th.sortType = "up";
  //         th.class = "fa-sort-up";
  //       } else if (th.sortType === "up") {
  //         th.sortType = "down";
  //         th.class = "fa-sort-down";
  //       } else {
  //         th.sortType = "default";
  //         th.class = "fa-sort";
  //       }
  //       sortType = th.sortType;
  //     } else {
  //       th.sortType = "default";
  //       th.class = "fa-sort";
  //     }
  //   });

  //   this.offenders = this.offenders?.sort((a, b) => a.names[0].last_name.localeCompare(b.names[0].last_name));

  //   switch (pName) {
  //     case "first_name": {
  //       if (sortType === "up") this.offenders = this.offenders?.sort((a, b) => b.names[0].first_name.localeCompare(a.names[0].first_name));
  //       else if (sortType === "down")
  //         this.offenders = this.offenders?.sort((a, b) => a.names[0].first_name.localeCompare(b.names[0].first_name));
  //       else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
  //       break;
  //     }
  //     case "dob": {
  //       if (sortType === "up")
  //         this.offenders = this.offenders?.sort((a, b) => {
  //           a[`aDate`] = new Date(a.dob.month + "/" + a.dob.day + "/" + a.dob.year);
  //           b[`bDate`] = new Date(b.dob.month + "/" + b.dob.day + "/" + b.dob.year);
  //           return b[`bDate`] - a[`aDate`];
  //         });
  //       else if (sortType === "down")
  //         this.offenders = this.offenders?.sort((a, b) => {
  //           a[`aDate`] = new Date(a.dob.month + "/" + a.dob.day + "/" + a.dob.year);
  //           b[`bDate`] = new Date(b.dob.month + "/" + b.dob.day + "/" + b.dob.year);
  //           return a[`bDate`] - b[`aDate`];
  //         });
  //       else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
  //       break;
  //     }
  //     case "addresses": {
  //       if (sortType === "up") this.offenders = this.offenders?.sort((a, b) => b.addresses[0].line.localeCompare(a.addresses[0].line));
  //       else if (sortType === "down")
  //         this.offenders = this.offenders?.sort((a, b) => a.addresses[0].line.localeCompare(b.addresses[0].line));
  //       else this.offenders = this.offenders?.sort((a, b) => b.created_date.localeCompare(a.created_date, "en-US"));
  //       break;
  //     }
  //     default:
  //       break;
  //   }
  // }
  //#endregion

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
