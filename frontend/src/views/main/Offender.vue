<template>
  <div class="container-fluid pt-2" v-if="offender">
    <div class="row">
      <div class="col-12">
        <h2><i class="material-icons mr-1">person</i> Offender Details</h2>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-12">
        <h3 class="text-primary">{{ offender.names[0].first_name }} {{ offender.names[0].middle }} {{ offender.names[0].last_name }}</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12 col-md-6">
        <div class="card">
          <div class="card-header">Personal Info</div>
          <div class="card-body">
            <table class="table table-striped">
              <tbody>
                <tr>
                  <th style="width: 70px;">Age</th>
                  <th style="width: 10px;">:</th>
                  <td>{{ offender.age }}</td>
                </tr>
                <tr>
                  <th>DOB</th>
                  <th>:</th>
                  <td>{{ offender.dob.month }}/{{ offender.dob.day }}/{{ offender.dob.year }}</td>
                </tr>
                <tr>
                  <th>Sex</th>
                  <th>:</th>
                  <td>{{ offender.demographic.sex }}</td>
                </tr>
                <tr>
                  <th>Race</th>
                  <th>:</th>
                  <td>{{ offender.demographic.race }}</td>
                </tr>
                <tr>
                  <th>Height</th>
                  <th>:</th>
                  <td>{{ offender.demographic.height }}</td>
                </tr>
                <tr>
                  <th>Weight</th>
                  <th>:</th>
                  <td>{{ offender.demographic.weight }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <br />
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="tabs is-boxed mb-0">
            <ul>
              <li :class="{ 'is-active': tabIndex == 0 }">
                <a @click="tabIndex = 0">
                  <span>Addresses</span>
                </a>
              </li>
              <li :class="{ 'is-active': tabIndex == 1 }">
                <a @click="tabIndex = 1">
                  <span>Aliases</span>
                </a>
              </li>
              <li :class="{ 'is-active': tabIndex == 2 }">
                <a @click="tabIndex = 2">
                  <span>Cases</span>
                </a>
              </li>
            </ul>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <div v-if="tabIndex == 0">
                  <table class="table table-borderless">
                    <tbody>
                      <tr v-for="(address, index) in offender.addresses">
                        <th style="width: 105px">Address - {{ index + 1 }}</th>
                        <th style="width: 30px">:</th>
                        <td>{{ address.line }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div v-if="tabIndex == 1">
                  <p v-for="name in offender.names.slice(1)">
                    <i class="fa-regular fa-circle mr-1"></i>
                    <strong>{{ name.first_name + " " + name.middle + " " + name.last_name }}</strong>
                  </p>
                </div>

                <div id="box" v-if="tabIndex == 2">
                  <table class="table table-sm table-bordered table-striped">
                    <thead>
                      <tr>
                        <th>Case Number</th>
                        <th>Charges</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="cs in offender.cases">
                        <td style="vertical-align: middle;">{{ cs.case_number }}</td>
                        <td>
                          <table class="table table-sm table-bordered table-striped mb-0">
                            <thead>
                              <tr>
                                <th>Offense Date</th>
                                <th>Description</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="charge in cs.charges">
                                <td>{{ charge.offense_date }}</td>
                                <td>{{ charge.description }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { dispatchSearchOffenders } from "@/store/main/actions";
import { IOffenders } from "@/interfaces";

@Component
export default class Offender extends Vue {
  offender?: IOffenders;

  tabIndex = 0;

  created() {
    let data: any;
    if (sessionStorage.getItem("offender")) {
      data = atob(sessionStorage.getItem("offender") || "{}");
    } else {
      data = "{}";
      this.$router.push({ name: "main-dashboard" });
    }
    this.offender = JSON.parse(data);
    console.log(this.offender);
    sessionStorage.removeItem("offender");
  }

  setTabIndex(index: number) {}
}
</script>
<style>
.table th,
td {
  vertical-align: middle;
}
#box .table thead th {
  vertical-align: middle;
  color: #fff;
  background-color: #333;
}
</style>
