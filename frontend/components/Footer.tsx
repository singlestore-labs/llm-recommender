import { ComponentProps } from "@/types";
import { cn } from "@/utils";
import Link from "next/link";

export type FooterProps = ComponentProps<"footer">;

export function Footer({ className, ...props }: FooterProps) {
  return (
    <footer {...props} className={cn("flex items-center justify-center py-8 text-center", className)}>
      <p className="text-muted-foreground">
        Built with ❤️ on{" "}
        <Link href="https://www.singlestore.com/" target="_blank" className="underline hover:text-zinc-800">
          SingleStoreDB
        </Link>{" "}
        Free Shared Tier and{" "}
        <Link href="https://vercel.com/home" target="_blank" className="underline hover:text-zinc-800">
          Vercel
        </Link>
      </p>
    </footer>
  );
}
