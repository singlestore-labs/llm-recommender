import axios, { AxiosError } from "axios";
import { toast } from "sonner";

export const api = axios.create({ baseURL: "/api" });

api.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = "Unknown error";

    if (error instanceof AxiosError) {
      const { data = {} } = error.response ?? {};

      if (typeof data === "string") {
        message = data;
      }

      if (typeof data === "object" && Object.keys(data).length) {
        if ("message" in data) {
          message = data.message;
        }
      }
    }

    toast.error(message);

    return Promise.reject(error);
  },
);
