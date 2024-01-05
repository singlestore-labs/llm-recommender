"use client";

import { HTMLAttributes, useState } from "react";
import Link from "next/link";

import { ComponentProps, DB } from "@/types";
import { cn } from "@/utils";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ModelHeader } from "./Header";
import { ModelResults } from "./Results";

export type CardModel = DB.Model & { description?: string };

export type ModelCardProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  CardModel
>;

export function ModelCard({
  className,
  id,
  name,
  author,
  repo_id,
  link,
  likes,
  score,
  arc,
  hellaswag,
  mmlu,
  truthfulqa,
  winogrande,
  gsm8k,
  downloads,
  description,
  ...props
}: ModelCardProps) {
  const [isDescExpanded, setIsDescExpanded] = useState(false);

  return (
    <Card {...props} className={cn(className)}>
      <CardHeader className="overflow-auto border-b-0">
        <ModelHeader
          repo_id={repo_id}
          author={author}
          name={name}
          link={link}
          likes={likes}
          downloads={downloads}
          headingProps={{ size: "sm" }}
          className="line-clamp-3 max-md:text-center"
        />
      </CardHeader>
      <CardContent className="relative flex flex-col">
        {description ? (
          <p
            className={cn("cursor-pointer", !isDescExpanded && "line-clamp-3")}
            onClick={() => setIsDescExpanded((is) => !is)}
          >
            {description}
          </p>
        ) : null}
      </CardContent>
      <CardFooter className="gap-4 max-md:flex-col">
        <ModelResults
          className="flex-1 py-2 text-xs max-md:w-full"
          listClassName="gap-0"
          borderClassName="right-0"
          results={{
            score,
            arc,
            hellaswag,
            mmlu,
            truthfulqa,
            winogrande,
            gsm8k,
          }}
        />
        <Button asChild className="ml-auto max-md:w-full">
          <Link href={`/models/${encodeURIComponent(repo_id)}`} target="_blank">
            View details
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
