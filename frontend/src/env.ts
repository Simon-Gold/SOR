const env = process.env.VUE_APP_ENV;

let envApiAuthURL = '';
let envApiSorURL = '';

if (env === 'production') {
  envApiAuthURL = `https://${process.env.VUE_APP_API_AUTH_URL_PROD}`;
} else if (env === 'staging') {
  envApiAuthURL = `https://${process.env.VUE_APP_API_AUTH_URL_STAG}`;
} else {
  envApiAuthURL = `http://${process.env.VUE_APP_API_AUTH_URL_DEV}`;
  envApiSorURL = `http://${process.env.VUE_APP_API_SOR_URL_DEV}`;
}

export const apiAuthURL = envApiAuthURL;
export const apiSorURL = envApiSorURL;
export const appName = process.env.VUE_APP_NAME;
