import { ElementType, ReactNode } from "react";
import Link from "next/link";
import { Download, Heart } from "lucide-react";

import { ComponentProps, DB } from "@/types";

import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Heading, HeadingProps } from "@/components/Heading";
import { cn } from "@/utils";

export type ModelDetail = { label: string; value: ReactNode; icon?: ElementType };

export type ModelHeaderProps = ComponentProps<
  "div",
  Pick<DB.Model, "repo_id" | "name" | "author" | "link" | "likes" | "downloads"> & {
    headingProps?: HeadingProps;
    details?: ModelDetail[];
  }
>;

export function ModelHeader({
  className,
  repo_id,
  name,
  author,
  link,
  likes,
  downloads,
  headingProps,
  details = [],
  ...props
}: ModelHeaderProps) {
  const authorLink = link.replace(repo_id, author);

  const _details: ModelDetail[] = [
    ...details,
    { label: "Likes", value: likes, icon: Heart },
    { label: "Downloads", value: downloads, icon: Download },
  ];

  return (
    <div {...props} className={cn("w-full max-w-full", className)}>
      <header className="flex flex-col items-center justify-between gap-6 md:flex-row">
        <Heading as="h2" {...headingProps}>
          <Link href={authorLink} className="hover:text-muted-foreground" target="_blank">
            {author}
          </Link>
          /
          <Link href={link} className="hover:text-muted-foreground" target="_blank">
            {name}
          </Link>
        </Heading>

        <ul
          className={cn("flex items-center justify-start gap-[1em]", headingProps?.size === "sm" && "text-md")}
        >
          {_details.map((detail) => (
            <li key={detail.label} className="flex items-center justify-center">
              <Details
                triggerChildren={
                  <span className="flex items-center justify-start gap-[0.25em]">
                    {detail.icon && <detail.icon className="w-[1.25em] text-[1em]" />}
                    <span>{detail.value}</span>
                  </span>
                }
              >
                {detail.label}
              </Details>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

function Details({ triggerChildren, children }: { triggerChildren?: ReactNode; children: ReactNode }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger className="hover:cursor-auto">{triggerChildren}</TooltipTrigger>
        <TooltipContent>{children}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
