"use client";

import { HTMLAttributes, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

import { ComponentProps, DB } from "@/types";
import { Markdown } from "@/components/Markdown";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Heading } from "@/components/Heading";
import { ExternalLink } from "@/components/ExternalLink";
import { Button } from "@/components/ui/button";
import { cn } from "@/utils";

export type ModelReadmeProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  Pick<DB.Model, "repo_id"> &
    Pick<DB.ModelReadme, "text"> & {
      expandedClassName?: string;
    }
>;

export function ModelReadme({
  className,
  repo_id,
  text,
  expandedClassName,
  ...props
}: ModelReadmeProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card
      {...props}
      className={cn(
        "flex flex-col",
        className,
        isExpanded && expandedClassName,
      )}
    >
      <CardHeader size="md" className="shrink-0 basis-auto items-start">
        <Heading as="h3" size="md" className="group relative inline-flex">
          Readme
          <ExternalLink
            href={`https://huggingface.co/${repo_id}/blob/main/README.md`}
          />
        </Heading>
      </CardHeader>
      <CardContent
        className={cn(
          "overflow-y-auto overflow-x-hidden py-4",
          isExpanded && "max-h-none",
        )}
      >
        <Markdown>{text}</Markdown>
      </CardContent>
      <CardFooter className="relative h-10 shrink-0 basis-auto border-t p-0">
        <Button
          variant="link"
          className="absolute left-0 top-0 h-full w-full text-muted-foreground hover:text-inherit"
          onClick={() => setIsExpanded((is) => !is)}
        >
          {isExpanded ? <ChevronUp /> : <ChevronDown />}
        </Button>
      </CardFooter>
    </Card>
  );
}
