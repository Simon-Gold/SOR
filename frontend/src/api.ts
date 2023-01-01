import { IOffenders, IOffenderPageModel, IUserPageModel } from "./interfaces/index";
import axios from "axios";
import { apiAuthURL, apiSorURL, apiVorURL } from "@/env";
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from "./interfaces";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    return axios.post(
      `${apiAuthURL}/api/v1/tokens/`,
      {},
      {
        auth: {
          username: username,
          password: password,
        },
      }
    );
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiAuthURL}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiAuthURL}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string, url: string) {
    url = url ? url : `${apiAuthURL}/api/v1/users/`;
    return axios.get<IUserPageModel>(url, authHeaders(token));
  },
  async getUser(token: string, userId: string) {
    return axios.get<IUserProfile>(`${apiAuthURL}/api/v1/users/${userId}`, authHeaders(token))
  },
  async updateUser(token: string, userId: string, data: IUserProfileUpdate) {
    return axios.put(`${apiAuthURL}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiAuthURL}/api/v1/users/`, data, authHeaders(token));
  },
  async deleteUser(token: string, userId: string) {
    return axios.delete(`${apiAuthURL}/api/v1/users/${userId}`, authHeaders(token))
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiAuthURL}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiAuthURL}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async search(token: string, query: string, serviceApiURL:string) {
    return axios.get<IOffenders[]>(`${serviceApiURL}/api/v1/search/${query}`, authHeaders(token));
  },
  async getOffenders(token: string, url: string) {
    url = url ? url : `${apiSorURL}/api/v1/offenders/`;
    return axios.get<IOffenderPageModel>(url, authHeaders(token));
  },
};
