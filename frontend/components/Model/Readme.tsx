"use client";

import { HTMLAttributes, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

import { ComponentProps, Model } from "@/types";
import { Markdown } from "@/components/Markdown";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Heading } from "@/components/Heading";
import { ExternalLink } from "@/components/ExternalLink";
import { Button } from "@/components/ui/button";
import { cn } from "@/utils";

export type ModelReadmeProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  Pick<Model, "repo_id" | "readme">
>;

export function ModelReadme({
  className,
  repo_id,
  readme,
  ...props
}: ModelReadmeProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const _readme = readme.slice(readme.indexOf("#"));

  return (
    <Card {...props} className={cn("relative overflow-hidden", className)}>
      <CardHeader size="md" className="items-start border-b">
        <Heading as="h3" size="md" className="group relative inline-flex">
          Readme
          <ExternalLink
            href={`https://huggingface.co/${repo_id}/blob/main/README.md`}
          />
        </Heading>
      </CardHeader>
      <CardContent
        className={cn(
          "max-h-[32rem] overflow-y-auto overflow-x-hidden py-4",
          isExpanded && "max-h-none",
        )}
      >
        <Markdown className="pb-10">{_readme}</Markdown>
        <Button
          variant="link"
          className="absolute bottom-0 left-0 w-full max-w-full rounded-none border-t bg-white text-muted-foreground hover:text-inherit"
          onClick={() => setIsExpanded((is) => !is)}
        >
          {isExpanded ? <ChevronUp /> : <ChevronDown />}
        </Button>
      </CardContent>
    </Card>
  );
}
