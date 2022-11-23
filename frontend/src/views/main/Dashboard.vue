<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
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
    </v-card>
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

  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'First Name',
      sortable: true,
      value: 'firs_name',
      align: 'left',
    },
    {
      text: 'Last Name',
      sortable: true,
      value: 'last_name',
      align: 'left',
    },
  ];

  public firstName = '';
  public userList: any = [];

  get users() {
    this.userList = readAdminUsers(this.$store);
    console.log(this.userList);

    return this.userList;
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public filterUserList() {
    // this.users = this.users.filter(u => u.first_name.includes(this.firstName));
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
