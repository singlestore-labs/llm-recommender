import { ReactNode } from "react";
import Link from "next/link";
import { Download, Heart } from "lucide-react";

import { ComponentProps, Model } from "@/types";

import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Heading } from "@/components/Heading";
import { cn } from "@/utils";

export type ModelDetailsProps = ComponentProps<"div", { model: Model }>;

export function ModelDetails({
  className,
  model,
  ...props
}: ModelDetailsProps) {
  const authorLink = model.link.replace(model.repo_id, model.author);

  return (
    <div {...props} className={cn("w-full max-w-full", className)}>
      <header className="flex items-center justify-between">
        <Heading as="h2">
          <Link
            href={authorLink}
            className="hover:text-muted-foreground"
            target="_blank"
          >
            {model.author}
          </Link>
          /
          <Link
            href={model.link}
            className="hover:text-muted-foreground"
            target="_blank"
          >
            {model.name}
          </Link>
        </Heading>

        <ul className="flex items-center justify-start gap-6">
          <li className="flex items-center justify-center">
            <Details
              triggerChildren={
                <span className="flex items-center justify-start gap-[0.25em]">
                  <Heart className="w-[1.25em]" />
                  <span>{model.likes}</span>
                </span>
              }
            >
              Likes
            </Details>
          </li>
          <li className="flex items-center justify-center">
            <Details
              triggerChildren={
                <span className="flex items-center justify-start gap-[0.25em]">
                  <Download className="w-[1.25em]" />
                  <span>{model.downloads}</span>
                </span>
              }
            >
              Downloads last month
            </Details>
          </li>
        </ul>
      </header>
    </div>
  );
}

function Details({
  triggerChildren,
  children,
}: {
  triggerChildren?: ReactNode;
  children: ReactNode;
}) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger className="hover:cursor-auto">
          {triggerChildren}
        </TooltipTrigger>
        <TooltipContent>{children}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
