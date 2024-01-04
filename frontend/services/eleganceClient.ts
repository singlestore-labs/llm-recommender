import { createEleganceClient } from "@singlestore/elegance-sdk";

const vercelURL =
  process.env.NEXT_PUBLIC_APP_URL ??
  process.env.VERCEL_URL ??
  process.env.NEXT_PUBLIC_VERCEL_URL;

const appURL = vercelURL ? `https://${vercelURL}` : "http://localhost:3000";

export const eleganceClient = createEleganceClient("mysql", {
  baseURL: `${appURL}/api`,
});
