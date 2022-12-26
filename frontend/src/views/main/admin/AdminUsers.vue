<template>
  <div class="container-fluid">
    <div class="card">
      <div class="card-body">
        <div class="card-title d-flex justify-content-between align-items-center">
          <h4 class="text-primary">Manage Users</h4>
          <router-link :to="{ name: 'main-admin-users-create' }" tag="button">
            <button type="button" class="button is-primary" style="max-width: fit-content; float: right">
              <i class="material-icons mr-1">add</i> Crate User
            </button>
          </router-link>
        </div>
        <hr />
        <div class="row">
          <div class="col">
            <div class="field">
              <div class="control has-icons-left">
                <input
                  type="text"
                  class="input"
                  id="searchByFName"
                  v-model="firstName"
                  @input="filter"
                  placeholder="Search By First Name"
                  autocomplete="off"
                />
                <span class="icon is-small is-left">
                  <i class="material-icons">search</i>
                </span>
              </div>
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
            <div class="box" :class="{ 'p-0': width <= 900 }" style="overflow: auto; max-height: 750px; min-height: 560px">
              <div class="card mb-1" v-if="width <= 900" v-for="user in filteredList">
                <div class="card-body">
                  <h5 class="card-title text-info">
                    {{ user.first_name + " " + user.last_name }}
                  </h5>
                  <hr class="my-1" />
                  <label class="d-block"> <strong>Email:</strong> {{ user.email }} </label>
                  <label class="d-block"><strong>Username:</strong> {{ user.username }}</label>
                  <label class="d-block">
                    <span
                      ><strong class="mr-1">İs Active:</strong>
                      <i
                        class="fa-solid mr-2"
                        :class="{ 'fa-circle-xmark text-danger': !user.is_active, 'fa-circle-check text-success': user.is_active }"
                      ></i
                    ></span>
                    <span
                      ><strong class="mr-1">İs Superuser:</strong>
                      <i
                        class="fa-solid mr-2"
                        :class="{ 'fa-circle-xmark text-danger': !user.is_superuser, 'fa-circle-check text-success': user.is_superuser }"
                      ></i
                    ></span>
                  </label>
                  <hr class="my-1" />
                  <div class="buttons" style="justify-content: flex-end;">
                    <button class="button is-danger is-small mr-1 mb-0" @click="deleteUser(user.id)">
                      <i class="material-icons">delete_forever</i>
                    </button>
                    <button class="button is-info is-small mb-0" @click="goEditPage(user.id)">
                      <i class="material-icons">edit</i>
                    </button>
                  </div>
                </div>
              </div>
              <table class="table table-striped table-bordered" v-if="width > 900">
                <thead>
                  <tr>
                    <th>Full Name</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>İs Active</th>
                    <th>İs Superuser</th>
                    <th style="width: 100px"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in filteredList">
                    <td>{{ user.first_name + " " + user.last_name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.username }}</td>
                    <td>
                      <i v-if="user.is_active" class="material-icons">check</i>
                    </td>
                    <td>
                      <i v-if="user.is_superuser" class="material-icons">check</i>
                    </td>
                    <td>
                      <button class="button is-danger is-small mr-1" @click="deleteUser(user.id)">
                        <i class="material-icons">delete_forever</i>
                      </button>
                      <button class="button is-info is-small" @click="goEditPage(user.id)">
                        <i class="material-icons">edit</i>
                      </button>
                      <!-- <router-link :to="{ name: 'main-admin-users-edit', params: { id: user.id } }" tag="button">
                      </router-link> -->
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-12" v-else>
            <div class="alert alert-info" role="alert">
              <i class="material-icons">info</i>
              <span>The user to display was not found.</span>
            </div>
          </div>
        </div>
        <hr />
        <div class="row">
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
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserPageModel, IUserProfile } from "@/interfaces";
import { readAdminUsers } from "@/store/admin/getters";
import { dispatchGetUsers, dispatchDeleteUser } from "@/store/admin/actions";
import { apiAuthURL, apiSorURL } from "@/env";

@Component
export default class AdminUsers extends Vue {
  firstName = "";
  users?: IUserProfile[];
  filteredList?: IUserProfile[];
  showList = false;
  spinner = false;

  totalPages? = 0;
  totalItems? = 0;
  currentPage? = 1;
  pageLimit = 10;
  nextUrl?: string;
  prevUrl?: string;

  width = window.innerWidth;

  async created() {
    window.addEventListener("resize", this.resizeHandler);
    await this.getUsers("");
  }

  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  }

  resizeHandler(e) {
    this.width = e.target.innerWidth;
  }
  async getUsers(url: string) {
    let payload = { url: url };
    this.showList = false;
    this.spinner = true;
    await dispatchGetUsers(this.$store, payload).then((data) => {
      this.spinner = false;
      this.showList = true;
      this.totalItems = data?.total_items;
      this.totalPages = data?.total_pages;
      this.nextUrl = data?.next;
      this.prevUrl = data?.prev;
      this.currentPage = data?.current_page;
      this.users = data?.items;
      this.filteredList = this.users?.slice();
      this.showList = this.filteredList !== undefined && this.filteredList.length > 0;
    });
  }

  async goNext() {
    let next = this.nextUrl ? this.nextUrl : "";
    await this.getUsers(next);
  }

  async goPrev() {
    let prev = this.prevUrl ? this.prevUrl : "";
    await this.getUsers(prev);
  }

  async setCurrentPage(page: number) {
    let query = "?page=" + page;
    let url = `${apiSorURL}/api/v1/offenders/${query}`;
    await this.getUsers(url);
  }

  filter() {
    if (this.firstName) {
      this.filteredList = this.users?.filter((u) => u.first_name.toLowerCase().indexOf(this.firstName.toLowerCase()) > -1);
    } else {
      this.filteredList = this.users?.slice();
    }
    this.showList = this.filteredList !== undefined && this.filteredList.length > 0;
  }

  formatDate(value: any) {
    if (value) {
      const date = new Date(value);
      return date.toLocaleDateString("en-US");
    }
  }

  goEditPage(userid: string) {
    this.$router.push({ name: "main-admin-users-edit", params: { id: userid } });
  }

  async deleteUser(id: string) {
    if (confirm("Are you sure you want to delete this user?")) {
      await dispatchDeleteUser(this.$store, { id: id }).then((data) => {
        alert(data.message);
        this.getUsers("");
      })
    }
  }
}
</script>
<style>
.alert .material-icons {
  position: relative;
  top: 5px;
  margin-right: 5px;
}
button.is-small {
  padding: 0 4px;
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
