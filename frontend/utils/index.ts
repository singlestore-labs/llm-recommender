import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import util from "util";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function inspect(data: any) {
  console.log(
    util.inspect(data, { showHidden: false, depth: null, colors: true }),
  );
}
