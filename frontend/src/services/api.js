
const API_URL = "http://127.0.0.1:8001";

export async function apiRequest(endpoint, method = "GET", data = null, token = null) {
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  if (token) {
    options.headers["token"] = token;
  }

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(API_URL + endpoint, options);

  const result = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(result.detail || "Something went wrong");
  }

  return result;
}

export function getToken() {
  return localStorage.getItem("access_token");
}

export function saveTokens(accessToken, refreshToken) {
  localStorage.setItem("access_token", accessToken);
  localStorage.setItem("refresh_token", refreshToken);
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");
  localStorage.removeItem("role");
}
