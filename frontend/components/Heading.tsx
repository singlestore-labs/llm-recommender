import { ReactNode } from "react";

import { cn } from "@/utils";

export type HeadingProps = {
  className?: string;
  children?: ReactNode;
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "span" | "p";
};

export function Heading({
  className,
  children,
  as: As = "span",
}: HeadingProps) {
  return (
    <As
      className={cn(
        "text-2xl font-semibold leading-none tracking-tight",
        className,
      )}
    >
      {children}
    </As>
  );
}
