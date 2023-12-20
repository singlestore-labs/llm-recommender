import Link from "next/link";

import { ComponentProps } from "@/types";
import { cn } from "@/utils";

import { Button } from "./ui/button";
import { Logo } from "./Logo";

export type HeaderProps = ComponentProps<"header">;

export function Header({ className, ...props }: HeaderProps) {
  return (
    <header {...props} className={cn("flex items-center py-8", className)}>
      <Link href="/" className="flex items-center justify-center">
        <h1 className="text-2xl flex items-center justify-center gap-[0.4em]">
          <Logo variant="1" className="w-[6em] flex-shrink-0" />
          <span className="block h-[1.3335em] w-px bg-current" />
          <span>LLM Recommender</span>
        </h1>
      </Link>

      <Button asChild className="ml-auto">
        <Link href="https://www.singlestore.com/" target="_blank">
          Try Free
        </Link>
      </Button>
    </header>
  );
}
