import Link, { LinkProps } from "next/link";
import { ExternalLink as IconExternalLink } from "lucide-react";

import { ComponentProps } from "@/types";
import { cn } from "@/utils";

export type ExternalLinkProps = ComponentProps<
  LinkProps,
  { className?: string }
>;

export function ExternalLink({ className, ...props }: ExternalLinkProps) {
  return (
    <Link
      {...props}
      target="_blank"
      className={cn(
        "absolute -right-[calc(1em+0.25em)] top-1/2 flex -translate-y-1/2 items-center justify-center text-muted-foreground opacity-0 transition hover:text-inherit group-hover:opacity-100",
        className,
      )}
    >
      <IconExternalLink className="mb-[12.5%] w-[clamp(1rem,1em,1.5rem)]" />
    </Link>
  );
}
