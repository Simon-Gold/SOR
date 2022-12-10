<template>
  <div class="container-fluid overflow-hidden">
    <div class="row vh-100 overflow-auto">
      <div :class="{ 'col-sm-12': width < 670, 'col-sm-3': width > 670 }" class="col-12 col-xl-2 px-sm-2 px-0 bg-dark d-flex sticky-top">
        <div class="d-flex flex-sm-column flex-row flex-grow-1 align-items-center align-items-sm-start pl-3 pt-2 text-white">
          <div style="width: 100%;">
            <a
              href="/"
              class="d-flex align-items-center mb-md-0 me-md-auto text-white text-decoration-none"
              style="border-bottom: 1px solid"
            >
              <span class="fs-5">Project SOR</span>
            </a>
            <ul
              :class="{ 'flex-sm-column': width > 670, 'align-items-sm-start': width > 670 }"
              class="nav nav-pills flex-row flex-nowrap flex-shrink-1 flex-sm-grow-0 flex-grow-1 mb-sm-auto mb-0 justify-content-center align-items-center"
              id="menu"
            >
              <li class="nav-item">
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-dashboard' }" tag="button">
                  <i class="material-icons mr-1">home</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Home</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-view' }" tag="button">
                  <i class="material-icons mr-1">person</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Profile</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-edit' }" tag="button">
                  <i class="material-icons mr-1">edit</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Edit Profile</span>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link px-sm-0 px-2" :to="{ name: 'main-profile-password' }" tag="button">
                  <i class="material-icons mr-1">vpn_key</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Change Password</span>
                </router-link>
              </li>
              <li class="dropdown" v-show="hasAdminAccess">
                <a href="#" class="nav-link dropdown-toggle px-sm-0 px-1" id="dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="material-icons mr-1">settings</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Admin</span>
                </a>
                <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdown">
                  <li>
                    <router-link class="dropdown-item" :to="{ name: 'main-admin-users' }" tag="button">
                      <i class="material-icons mr-1">group</i> <span class="ms-1 d-sm-inline">Manage Users</span>
                    </router-link>
                  </li>
                  <li>
                    <hr class="dropdown-divider" />
                  </li>
                  <li>
                    <router-link class="dropdown-item" :to="{ name: 'main-admin-users-create' }" tag="button">
                      <i class="material-icons mr-1">person_add</i> <span class="ms-1 d-sm-inline">Create User</span>
                    </router-link>
                  </li>
                </ul>
              </li>
              <li>
                <a class="nav-link px-sm-0 px-2" @click="logout">
                  <i class="material-icons mr-1">close</i>
                  <span :class="{ 'd-sm-inline': width > 670 }" class="ms-1 d-none">Logout</span>
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

  width = window.innerWidth;

  created() {
    window.addEventListener("resize", this.resizeHandler);
  }

  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  }

  resizeHandler(e) {
    this.width = e.target.innerWidth;
    // console.log(e.target.innerWidth);
  }

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
