<template>
  <div>
    <nav class="navbar is-link" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link class="navbar-item" :to="{ name: 'main-dashboard' }" tag="button">
          <i class="material-icons mr-3">dashboard</i>
          <strong style="color: white">Project SOR</strong>
        </router-link>

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="dropdown">
              <button class="button is-link is-inverted is-outlined" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="material-icons mr-2">manage_accounts</i> My Account
              </button>
              <ul class="dropdown-menu" style="left: -60px">
                <li>
                  <router-link class="dropdown-item" :to="{ name: 'main-profile-view' }" tag="button">
                    <i class="material-icons mr-1">person</i> Profile
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" :to="{ name: 'main-profile-edit' }" tag="button">
                    <i class="material-icons mr-1">edit</i> Edit Profile
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" :to="{ name: 'main-profile-password' }" tag="button">
                    <i class="material-icons mr-1">vpn_key</i> Change Password
                  </router-link>
                </li>
                <li v-show="hasAdminAccess"><hr class="dropdown-divider" /></li>
                <li v-show="hasAdminAccess">
                  <router-link class="dropdown-item" :to="{ name: 'main-admin-users' }" tag="button">
                    <i class="material-icons mr-1">group</i> Manage Users
                  </router-link>
                </li>
                <li v-show="hasAdminAccess">
                  <router-link class="dropdown-item" :to="{ name: 'main-admin-users-create' }" tag="button">
                    <i class="material-icons mr-1">person_add</i> Create User
                  </router-link>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <a class="dropdown-item" @click="logout"> <i class="material-icons mr-1">close</i> Logout </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

import { appName } from "@/env";
import { readDashboardMiniDrawer, readDashboardShowDrawer, readHasAdminAccess } from "@/store/main/getters";
import { commitSetDashboardShowDrawer, commitSetDashboardMiniDrawer } from "@/store/main/mutations";
import { dispatchUserLogOut } from "@/store/main/actions";

const routeGuardMain = async (to, from, next) => {
  if (to.path === "/main") {
    next("/main/dashboard");
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(this.$store, !readDashboardShowDrawer(this.$store));
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(this.$store, !readDashboardMiniDrawer(this.$store));
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>
<style>
.dropdown-item .material-icons {
  position: relative;
  top: 5px;
}
</style>
