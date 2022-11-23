const env = process.env.VUE_APP_ENV;

let envApiUrl = '';

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_API_URL_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_API_URL_STAG}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_API_URL_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
