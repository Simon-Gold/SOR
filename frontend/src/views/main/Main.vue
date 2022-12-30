<template>
  <div id="body-pd" class="body body-pd">
    <!-- header -->
    <header class="header body-pd" id="header">
      <div class="header_toggle">
        <i class="fa-solid fa-chevron-left" id="header-toggle" @click="menuClick"></i>
      </div>
      <div class="input-group" style="width: 90%">
          <span class="input-group-text">
            <i class="material-icons">search</i>
          </span>
        <input
          type="text"
          class="form-control text-small"
          placeholder="Search Offender (Exp: doe john 1/22/1985 state:AK in:SOR)"
          aria-label="Search Offender"
          aria-describedby="button-addon"
          v-model="searchText"
          @keypress.enter="$emit('sendSearchText', searchText)"
        />
          <button
            class="input-group-text button is-danger"
            type="button"
            id="button-addon"
            @click="$emit('clearSearchText'), (searchText = '')"
            v-show="searchText"
            >
            <i class="fa-solid fa-xmark p-1"></i>
          </button>
      </div>
      <button
        class="button is-outlined dropdown-toggle"
        role="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        style="max-width: 50px; padding: 0 5px"
      >
        <i class="material-icons">settings</i>
      </button>
      <ul class="dropdown-menu">
        <li>
          <router-link class="dropdown-item" :to="{ name: 'main-profile-view' }">
            <i class="material-icons mr-1">person</i> <span>Profile</span>
          </router-link>
        </li>
        <li>
          <router-link class="dropdown-item" :to="{ name: 'main-profile-edit' }">
            <i class="material-icons mr-1">edit</i> <span>Profile Edit</span>
          </router-link>
        </li>
        <li>
          <router-link class="dropdown-item" :to="{ name: 'main-profile-password' }">
            <i class="material-icons mr-1">vpn_key</i> <span>Change Password</span>
          </router-link>
        </li>
        <li v-show="hasAdminAccess"><hr class="dropdown-divider" /></li>
        <li v-show="hasAdminAccess">
          <router-link class="dropdown-item" :to="{ name: 'main-admin-users' }">
            <i class="material-icons mr-1">group</i> <span>Manage Users</span>
          </router-link>
        </li>
        <li v-show="hasAdminAccess">
          <router-link class="dropdown-item" :to="{ name: 'main-admin-users-create' }">
            <i class="material-icons mr-1">person_add</i> <span>Create User</span>
          </router-link>
        </li>
        <li><hr class="dropdown-divider" /></li>
        <li>
          <a class="dropdown-item" @click="logout"> <i class="material-icons mr-1">close</i> <span>Logout</span> </a>
        </li>
      </ul>
    </header>
    <!-- sidebar -->
    <div class="l-navbar show" id="nav-bar">
      <nav class="nav">
        <div>
          <a href="#" class="nav_logo">
            <i class="fa-solid fa-layer-group nav_logo-icon"></i> <span class="nav_logo-name">ProjectSOR</span>
          </a>
          <div class="nav_list">
            <router-link class="nav_link active" :to="{ name: 'main-dashboard' }">
              <i class="material-icons">person</i> <span class="nav_name">Home</span>
            </router-link>
            <a href="#" class="nav_link" id="user"> <i class="fa-solid fa-hashtag nav_icon"></i> <span class="nav_name">SOR</span> </a>
            <a href="#" class="nav_link" id="mess"> <i class="fa-regular fa-hashtag nav_icon"></i> <span class="nav_name">VOR</span> </a>
          </div>
        </div>
        <a class="nav_link" @click="logout">
          <i class="fa-solid fa-right-from-bracket nav_icon"></i> <span class="nav_name">Logout</span>
        </a>
      </nav>
    </div>
    <!-- main content -->
    <div class="height-100" style="margin-top: 5rem">
      <router-view></router-view>
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
  public searchText = "";
  width = window.innerWidth;

  created() {
    window.addEventListener("resize", this.resizeHandler);
    // handle key press as event listener [1]
    // window.addEventListener('keyup', this.previous);
  }
  previous(event_keypress) {
    // check key code [2]
    // console.log(event_keypress);
  }
  beforeDestroy() {
    // remove listener [3]
    // window.removeEventListener('keyup', this.previous);
  }

  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  }

  resizeHandler(e) {
    this.width = e.target.innerWidth;
  }

  menuClick() {
    const toggle = document.getElementById("header-toggle"),
      nav = document.getElementById("nav-bar"),
      bodypd = document.getElementById("body-pd"),
      headerpd = document.getElementById("header");

    nav?.classList.toggle("show");
    // change icon
    toggle?.classList.toggle("fa-chevron-right");
    // add padding to body
    bodypd?.classList.toggle("body-pd");
    // add padding to header
    headerpd?.classList.toggle("body-pd");
  }

  sideNavListener(event) {
    const showNavbar = (toggleId, navId, bodyId, headerId) => {
      const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId);

      // Validate that all variables exist
      if (toggle && nav && bodypd && headerpd) {
        toggle.addEventListener("click", () => {
          // show navbar
          nav.classList.toggle("show");
          // change icon
          toggle.classList.toggle("fa-chevron-right");
          // add padding to body
          bodypd.classList.toggle("body-pd");
          // add padding to header
          headerpd.classList.toggle("body-pd");
        });
      }
    };

    showNavbar("header-toggle", "nav-bar", "body-pd", "header");

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll(".nav_link");

    function colorLink() {
      if (linkColor) {
        linkColor.forEach((l) => l.classList.remove("active"));
        // this.classList.add("active");
      }
    }
    linkColor.forEach((l) => l.addEventListener("click", colorLink));
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

.input-group-text {
  border: none;
  background: white;
  padding: 0.375rem 0.5rem;
}
/*  */

@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap");

:root {
  --header-height: 3rem;
  --nav-width: 68px;
  --first-color: #183153;
  --first-color-light: #afa5d9;
  --white-color: #f7f6fb;
  --body-font: "Nunito", sans-serif;
  --normal-font-size: 1rem;
  --z-fixed: 100;
}

*,
::before,
::after {
  box-sizing: border-box;
}

.body {
  position: relative;
  margin: var(--header-height) 0 0 0;
  padding: 0 1rem;
  font-family: var(--body-font);
  font-size: var(--normal-font-size);
  transition: 0.5s;
}

a {
  text-decoration: none;
}

h4 {
  color: var(--first-color);
}

.header {
  width: 100%;
  height: var(--header-height);
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  background-color: var(--white-color);
  z-index: var(--z-fixed);
  transition: 0.5s;
  background-color: var(--first-color);
}

.header_toggle {
  color: var(--first-color-light);
  font-size: 1.5rem;
  cursor: pointer;
  position: relative;
  right: 10px;
}

.header_img {
  width: 35px;
  height: 35px;
  display: flex;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
}

.header_img img {
  width: 40px;
}

.l-navbar {
  position: fixed;
  top: 0;
  left: -30%;
  width: var(--nav-width);
  height: 100vh;
  background-color: var(--first-color);
  padding: 0.5rem 1rem 0 0;
  transition: 0.5s;
  z-index: var(--z-fixed);
  -webkit-box-shadow: 4px 0px 4px -4px rgba(0, 0, 0, 1);
  -moz-box-shadow: 4px 0px 4px -4px rgba(0, 0, 0, 1);
  box-shadow: 4px 0px 4px -4px rgba(0, 0, 0, 1);
}

.nav {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.nav_logo,
.nav_link {
  display: grid;
  grid-template-columns: max-content max-content;
  align-items: center;
  column-gap: 1rem;
  padding: 0.5rem 0 0.5rem 1.5rem;
}

.nav_logo {
  margin-bottom: 2rem;
}

.nav_logo-icon {
  font-size: 1.25rem;
  color: var(--white-color);
}

.nav_logo-name {
  color: var(--white-color);
  font-weight: 700;
}

.nav_link {
  position: relative;
  color: var(--first-color-light);
  margin-bottom: 1rem;
  transition: 0.3s;
}

.nav_link:hover {
  color: var(--white-color);
}

.nav_icon {
  font-size: 1.25rem;
}

.show {
  left: 0;
}

.body-pd {
  padding-left: calc(var(--nav-width) + 1rem);
}

.active {
  color: var(--white-color);
}

.active::before {
  content: "";
  position: absolute;
  left: 0;
  width: 8px;
  height: 32px;
  background-color: var(--white-color);
}

.height-100 {
  height: 100vh;
}

@media screen and (min-width: 768px) {
  .body {
    margin: calc(var(--header-height) + 1rem) 0 0 0;
    padding-left: calc(var(--nav-width) + 2rem);
  }

  .header {
    height: calc(var(--header-height) + 1rem);
    padding: 0 2rem 0 calc(var(--nav-width) + 2rem);
  }

  .header_img {
    width: 40px;
    height: 40px;
  }

  .header_img img {
    width: 45px;
  }

  .l-navbar {
    left: 0;
    padding: 1rem 1rem 0 0;
  }

  .show {
    width: calc(var(--nav-width) + 156px);
  }

  .body-pd {
    padding-left: calc(var(--nav-width) + 188px);
  }
}
/* input[type="search"]::-webkit-search-cancel-button {
    -webkit-appearance: searchfield-cancel-button;
  } */
</style>
