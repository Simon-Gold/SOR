<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title text-primary">
              Users
              <small style="font-size: 50%"><i>via bootstrap css</i></small>
            </h4>
            <div class="row">
              <div class="col mb-3">
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
            <hr />
            <div class="row">
              <div class="col-12" v-if="showList">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Email</th>
                      <th>First Name</th>
                      <th>Last Name</th>
                      <th>Username</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(user, index) in filteredList">
                      <td>{{ index + 1 }}</td>
                      <td>{{ user.email }}</td>
                      <td>{{ user.first_name }}</td>
                      <td>{{ user.last_name }}</td>
                      <td>{{ user.username }}</td>
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
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { readUserProfile } from "@/store/main/getters";
import { readAdminUsers } from "@/store/admin/getters";
import { dispatchGetUsers } from "@/store/admin/actions";
import { dispatchSearchOffenders } from "@/store/main/actions";
import { IUserProfile } from "@/interfaces";

@Component
export default class Dashboard extends Vue {
  firstName = "";
  users: IUserProfile[] = [];
  filteredList: IUserProfile[] = [];
  showList = false;

  public async created() {
    await dispatchGetUsers(this.$store);
    this.users = readAdminUsers(this.$store);
    this.filteredList = this.users.slice();
    this.showList = this.filteredList.length > 0;

    const data = await dispatchSearchOffenders(this.$store, { query: '?last=jo' });
    console.log(data);
    
  }

  filter() {
    if (this.firstName) {
      this.filteredList = this.users.filter((u) => u.first_name.toLowerCase().indexOf(this.firstName.toLowerCase()) > -1);
    } else {
      this.filteredList = this.users.slice();
    }
    this.showList = this.filteredList.length > 0;
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
