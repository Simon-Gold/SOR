<template>
  <div class="container-fluid pt-2">
    <div class="row">
      <div class="col-12">
        <h1 v-if="offender">Hello {{ offender.names[0].first_name }} {{offender.names[0].last_name}}</h1>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { dispatchSearchOffenders } from "@/store/main/actions";
import { IOffenders } from "@/interfaces";

@Component
export default class Offender extends Vue {
  offender: IOffenders | undefined;
  created() {
    let data: any;
    if (sessionStorage.getItem("offender")) {
      data = atob(sessionStorage.getItem('offender') || '{}');
    } else {
      data = '{}';
    }
    this.offender = JSON.parse(data);
    console.log(this.offender);
    sessionStorage.removeItem("offender");
  }
}
</script>
