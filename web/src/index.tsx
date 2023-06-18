import React from "react";
import "./index.css";
import ReactDOM from "react-dom/client";
import { redirectToLogin } from "./helpers/redirectLogin";
import { dbg } from "./helpers/util";
import { App } from "./App";

/**
 * Rehydrates Spotify access credentials from URL parameters or localStorage.
 * This function is typically called at the root of a React application.
 */
const rehydrateSpotifyAccess = () => {
  // Retrieve URL parameters
  // eslint-disable-next-line no-restricted-globals
  const href = new URLSearchParams(location.search);

  // Extract token, id, and refresh values from URL parameters
  let token = href.get("token"),
    id = href.get("id"),
    refresh = href.get("refresh");

  if (token && id && refresh) {
    // Store token, id, and refresh values in localStorage if they exist in the URL
    // Always update if new ones exist
    localStorage.setItem("token", token);
    localStorage.setItem("id", id);
    localStorage.setItem("refresh", refresh);

    // Remove URL parameters from the current page URL
    window.location.href = window.location.href.split("?")[0];
  } else {
    // If token, id, and refresh values are not present in the URL parameters,
    // attempt to retrieve them from localStorage
    token = localStorage.getItem("token");
    id = localStorage.getItem("id");
    refresh = localStorage.getItem("refresh");

    if (!(token && id && refresh)) {
      // If token, id, and refresh values are not present in localStorage,
      // redirect the user to the login page or perform appropriate error handling
      redirectToLogin();
    }
  }
  // eslint-disable-next-line no-restricted-globals
  dbg(`Token: ${token}, ID: ${id}, Refresh: ${refresh}`);
};

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

rehydrateSpotifyAccess();

// CSSTransitions can't have strict mode
root.render(
  <React.Suspense fallback={<h1>Loading....</h1>}>
    <App />
  </React.Suspense>
);
