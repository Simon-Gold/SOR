import { api } from "@/api";
import { ActionContext } from "vuex";
import { IUserProfileCreate, IUserProfileUpdate } from "@/interfaces";
import { State } from "../state";
import { AdminState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { commitSetUsers, commitSetUser } from "./mutations";
import { dispatchCheckApiError } from "../main/actions";
import { commitAddNotification, commitRemoveNotification } from "../main/mutations";

type MainContext = ActionContext<AdminState, State>;

export const actions = {
  async actionGetUsers(context: MainContext, payload: { url: string }) {
    try {
      const response = await api.getUsers(context.rootState.main.token, payload.url);
      if (response) {
        commitSetUsers(context, response.data.items);
      }

      return response.data;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetUser(context: MainContext, payload: { id: string }) {
    try {
      const response = await api.getUser(context.rootState.main.token, payload.id);
      return response.data;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateUser(context: MainContext, payload: { id: string; user: IUserProfileUpdate }) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateUser(context.rootState.main.token, payload.id, payload.user),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      commitSetUser(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, { content: "User successfully updated", color: "success" });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createUser(context.rootState.main.token, payload),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      commitSetUser(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, { content: "User successfully created", color: "success" });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionDeleteUser(context: MainContext, payload: { id: string }) {
    try {
      const response = (
        await Promise.all([
          api.deleteUser(context.rootState.main.token, payload.id),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ])
      )[0];
      return response.data;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
};

const { dispatch } = getStoreAccessors<AdminState, State>("");

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchGetUser = dispatch(actions.actionGetUser);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchDeleteUser = dispatch(actions.actionDeleteUser);
