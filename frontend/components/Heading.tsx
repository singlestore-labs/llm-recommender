import { ReactNode } from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/utils";
import { ComponentProps } from "@/types";

const headingVariants = cva("leading-none tracking-tight", {
  variants: {
    size: {
      default: "text-2xl font-semibold",
      hero: "text-4xl font-bold",
      md: "text-xl font-semibold",
      sm: "text-lg font-semibold",
    },
  },
  defaultVariants: {
    size: "default",
  },
});

export type HeadingProps = ComponentProps<
  {
    className?: string;
    children?: ReactNode;
    as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "span" | "p";
  },
  VariantProps<typeof headingVariants>
>;

export function Heading({ className, children, as: As = "span", size }: HeadingProps) {
  return <As className={cn(headingVariants({ size }), className)}>{children}</As>;
}
