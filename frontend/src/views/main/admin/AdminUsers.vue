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
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Email</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Username</th>
                  <th>İs Active</th>
                  <th>İs Superuser</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users">
                  <td>{{ user.id }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.first_name }}</td>
                  <td>{{ user.last_name }}</td>
                  <td>{{ user.username }}</td>
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
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
