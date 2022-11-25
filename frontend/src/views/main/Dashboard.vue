<template>
  <v-container fluid>
    <span hidden>{{greetedUser}}</span>
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title">Users <small style="font-size: 50%;"><i>via bootstrap css</i></small> </h4>
              <div class="row">
                <div class="col mb-3">
                  <div class="control has-icons-left">
                    <input type="text" class="input" id="searchByFName" v-model="firstName" @change="filterUserList"
                      placeholder="Search By First Name" />
                    <span class="icon is-small is-left">
                      <i class="material-icons">search</i>
                    </span>
                  </div>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col">
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
                      <tr v-for="user, index in filterList">
                        <td>{{ index + 1 }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.first_name }}</td>
                        <td>{{ user.last_name }}</td>
                        <td>{{ user.username }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-text-field label="Search By First Name" v-model="firstName" @change="filterUserList"></v-text-field>
        </template>
        <v-data-table :headers="headers" :items="users">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.email }}</td>
            <td>{{ props.item.first_name }}</td>
            <td>{{ props.item.last_name }}</td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card> -->
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class Dashboard extends Vue {

  public firstName = '';
  public filterList: any;
  public users: any;

  // get users() {
  //   // this.userList = readAdminUsers(this.$store);
  //   // return this.userList;
  //   return readAdminUsers(this.$store);
  // }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public filterUserList() {
    this.filterList = this.users.filter(u => u.first_name.indexOf(this.firstName) > -1);
    
    // filtering worked but the change was not reflected in the table
  }

  get greetedUser() {
    this.users = readAdminUsers(this.$store);
    this.filterList = this.users.slice();
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.first_name || userProfile.last_name) {
        return userProfile.first_name + ' ' + userProfile.last_name;
      } else {
        return userProfile.email;
      }
    }
  }
}
</script>
