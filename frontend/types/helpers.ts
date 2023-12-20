export type Defined<T> = Exclude<T, undefined>;

export type Override<T extends object, K extends object> = Omit<T, keyof K> & K;

export type AnyObject<T extends Record<PropertyKey, any> = Record<PropertyKey, any>> = T;

export type AnyFunction<T extends (...args: any[]) => any = (...args: any[]) => any> = T;

export type Optional<T extends Record<any, any>, K extends keyof T> = Omit<T, K> & {
  [C in keyof Pick<T, K>]?: T[C];
};

export type PartialDeep<T> = T extends object ? { [P in keyof T]?: PartialDeep<T[P]> } : T;
