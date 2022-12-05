<template>
  <div class="container-fluid">
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
                      autocomplete="off"
                    />
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="field">
                  <label class="label">Search By DOB</label>
                  <div class="control">
                    <input
                      type="date"
                      class="input"
                      id="searchByDob"
                      v-model="dob"
                      autocomplete="off"
                    />
                  </div>
                </div>
              </div>
              <div class="col d-flex align-items-end">
                <button class="button is-link" @click="filterOffenders" style="max-width: 120px;" :disabled="!lastName">
                  <i class="material-icons">search</i> Search
                </button>
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
import { readOffenders } from "@/store/main/getters";
import { readAdminUsers } from "@/store/admin/getters";
import { dispatchGetUsers } from "@/store/admin/actions";
import { dispatchSearchOffenders } from "@/store/main/actions";
import { IOffenders, IUserProfile } from "@/interfaces";

@Component
export default class Dashboard extends Vue {
  firstName = "";
  lastName = "";
  dob?: Date;

  users: IUserProfile[] = [];
  filteredList: IUserProfile[] = [];
  showList = false;

  offenders: IOffenders[] = [];

  public async created() {
    await dispatchGetUsers(this.$store);
    this.users = readAdminUsers(this.$store);
    this.filteredList = this.users.slice();
    this.showList = this.filteredList.length > 0;
  }

  async filterOffenders() {
    let query = '?last=' + this.lastName;
    if (this.firstName) {
      query += '&first=' + this.firstName;
    }
    if (this.dob) {
      const strDob = new Date(this.dob).toLocaleDateString('en-US');
      query += '&dob=' + strDob;
    }

    console.log(query);
    
    await dispatchSearchOffenders(this.$store, { query: query });
    this.offenders = readOffenders(this.$store);
    console.log(this.offenders);
    
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
