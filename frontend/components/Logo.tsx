import { ElementType } from "react";
import { Defined, ComponentProps } from "@/types";
import { cn } from "@/utils";

import SingleStoreLogo from "@/public/SingleStore.svg";
import SingleStoreLogoFlat from "@/public/SingleStoreFlat.svg";

export type LogoProps = ComponentProps<
  "span",
  { variant?: "1" | "2"; sourceProps?: ComponentProps<"svg"> }
>;

const logoByVariant: Record<Defined<LogoProps["variant"]>, ElementType> = {
  "1": SingleStoreLogo,
  "2": SingleStoreLogoFlat,
};

export function Logo({
  className,
  variant = "1",
  sourceProps,
  ...props
}: LogoProps) {
  const _Logo = logoByVariant[variant];

  return (
    <span {...props} className={cn(className)}>
      <_Logo
        className={cn(
          "h-full w-full [&_[fill]]:fill-current [&_[stroke]]:stroke-current",
          sourceProps,
        )}
      />
    </span>
  );
}
