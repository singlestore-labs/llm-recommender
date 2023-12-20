import { Override } from "./helpers";

export type ComponentProps<
  T extends object | keyof JSX.IntrinsicElements = object,
  K extends object = object
> = Override<T extends keyof JSX.IntrinsicElements ? JSX.IntrinsicElements[T] : T, K>;

export type PropsByValues<T extends Record<any, any>, O extends keyof T = ""> = (
  props?: Partial<T>
) => Partial<Omit<T, O>>;

export type TextElements = "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "p" | "span";

export type Message = {
  id: number;
  content: string;
  author: string;
};
