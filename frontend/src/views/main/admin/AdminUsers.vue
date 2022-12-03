<template>
  <div class="container">
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
          <div class="col-12" v-if="showList">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Email</th>
                  <th>Username</th>
                  <th>Created Date</th>
                  <th>Updated Date</th>
                  <th>İs Active</th>
                  <th>İs Superuser</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredList">
                  <td>{{ user.first_name }}</td>
                  <td>{{ user.last_name }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ formatDate(user.created_date) }}</td>
                  <td>{{ formatDate(user.updated_date) }}</td>
                  <td>
                    <i v-if="user.is_active" class="material-icons">check</i>
                  </td>
                  <td>
                    <i v-if="user.is_superuser" class="material-icons">check</i>
                  </td>
                  <td>
                    <router-link
                      :to="{
                        name: 'main-admin-users-edit',
                        params: { id: user.id },
                      }"
                      tag="button"
                    >
                      <button class="button is-info is-small">
                        <i class="material-icons">edit</i>
                      </button>
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="col-12" v-else>
            <div class="alert alert-info" role="alert">
              <i class="material-icons">info</i>
              <span>The user to display was not found.</span>
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
import { IUserProfile } from "@/interfaces";
import { readAdminUsers } from "@/store/admin/getters";
import { dispatchGetUsers } from "@/store/admin/actions";

@Component
export default class AdminUsers extends Vue {
  firstName = "";
  users: IUserProfile[] = [];
  filteredList: IUserProfile[] = [];
  showList = false;

  public async created() {
    await dispatchGetUsers(this.$store);
    this.users = readAdminUsers(this.$store);
    this.filteredList = this.users.slice();
    this.showList = this.filteredList.length > 0;
  }

  filter() {
    if (this.firstName) {
      this.filteredList = this.users.filter((u) => u.first_name.toLowerCase().indexOf(this.firstName.toLowerCase()) > -1);
    } else {
      this.filteredList = this.users.slice();
    }
    this.showList = this.filteredList.length > 0;
  }

  formatDate(value: any) {
    if (value) {
      const date = new Date(value);
      return date.toLocaleDateString("en-US") + " " + date.toLocaleTimeString("en-US");
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
</style>
