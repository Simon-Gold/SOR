<template>
  <div class="container-fluid overflow-hidden">
    <div class="row vh-100 overflow-auto">
      <div class="col-12 col-sm-3 col-xl-2 px-sm-2 px-0 bg-dark d-flex sticky-top">
        <div class="d-flex flex-sm-column flex-row flex-grow-1 align-items-center align-items-sm-start px-3 pt-2 text-white">
          <div>
            <a href="/" class="d-flex align-items-center pb-sm-3 mb-md-0 me-md-auto text-white text-decoration-none">
              <span class="fs-5">S<span class="d-none d-sm-inline">OR</span></span>
            </a>
            <ul
              class="nav nav-pills flex-sm-column flex-row flex-nowrap flex-shrink-1 flex-sm-grow-0 flex-grow-1 mb-sm-auto mb-0 justify-content-center align-items-center align-items-sm-start"
              id="menu"
            >
              <li class="nav-item">
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-dashboard' }" tag="button">
                  <i class="material-icons mr-1">home</i><span class="ms-1 d-none d-sm-inline">Home</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-view' }" tag="button">
                  <i class="material-icons mr-1">person</i> <span class="ms-1 d-none d-sm-inline">Profile</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-edit' }" tag="button">
                  <i class="material-icons mr-1">edit</i> <span class="ms-1 d-none d-sm-inline">Edit Profile</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-password' }" tag="button">
                  <i class="material-icons mr-1">vpn_key</i> <span class="ms-1 d-none d-sm-inline">Change Password</span>
                </router-link>
              </li>
              <li class="dropdown" v-show="hasAdminAccess">
                <a href="#" class="nav-link dropdown-toggle px-sm-0 px-1" id="dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="material-icons mr-1">settings</i><span class="ms-1 d-none d-sm-inline">Admin</span>
                </a>
                <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdown">
                  <li>
                    <router-link class="dropdown-item" :to="{ name: 'main-admin-users' }" tag="button">
                      <i class="material-icons mr-1">group</i> <span class="ms-1 d-none d-sm-inline">Manage Users</span>
                    </router-link>
                  </li>
                  <li>
                    <hr class="dropdown-divider" />
                  </li>
                  <li>
                    <router-link class="dropdown-item" :to="{ name: 'main-admin-users-create' }" tag="button">
                      <i class="material-icons mr-1">person_add</i> <span class="ms-1 d-none d-sm-inline">Create User</span>
                    </router-link>
                  </li>
                </ul>
              </li>
              <li>
                <a class="nav-link px-sm-0 px-2" @click="logout">
                  <i class="material-icons mr-1">close</i> <span class="ms-1 d-none d-sm-inline">Logout</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col d-flex flex-column h-sm-100">
        <main class="row overflow-auto">
          <router-view></router-view>
        </main>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { appName } from "@/env";
import { readHasAdminAccess } from "@/store/main/getters";
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
  top: 7px;
}
.nav-link .material-icons {
  position: relative;
  top: 7px;
}
.nav-link {
  color: inherit;
}
@media (min-width: 576px) {
  .h-sm-100 {
    height: 100% !important;
  }
}
</style>
