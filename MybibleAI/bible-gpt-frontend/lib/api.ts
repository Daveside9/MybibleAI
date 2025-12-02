
import { getToken } from "./auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchAuthenticated(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getToken();
  const headers = new Headers(options.headers || {});

  if (token) {
    headers.append("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Optional: Handle token expiration or invalid token,
    // e.g., by redirecting to the login page.
    console.error("Authentication error. Redirecting to login.");
    // This should be handled in the component that calls this function
    // to avoid breaking server-side rendering.
    // For example: router.push('/login');
  }

  return response;
}
