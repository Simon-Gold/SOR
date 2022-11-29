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
                      <tr v-for="user, index in users">
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

  get users() {
    return readAdminUsers(this.$store);
  }

  created() {
     this.filterList = readAdminUsers(this.$store);
     console.log(this.filterList);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public filterUserList() {
    this.filterList = this.filterList.filter(u => u.first_name.indexOf(this.firstName) > -1);
    
    // filtering worked but the change was not reflected in the table
  }

  get greetedUser() {
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
