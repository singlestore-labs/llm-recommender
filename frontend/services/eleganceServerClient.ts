import { createEleganceServerClient } from "@singlestore/elegance-sdk/server";

export const eleganceServerClient = createEleganceServerClient("mysql", {
  connection: {
    host: process.env.SINGLESTORE_WORKSPACE_HOST,
    user: process.env.SINGLESTORE_WORKSPACE_USERNAME,
    password: process.env.SINGLESTORE_WORKSPACE_PASSWORD,
    database: process.env.DB_NAME,
  },
  ai: {
    openai: {
      apiKey: process.env.OPENAI_API_KEY,
    },
  },
});
