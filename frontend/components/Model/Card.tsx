import { HTMLAttributes, ReactNode } from "react";
import Link from "next/link";

import { ComponentProps, Model } from "@/types";
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

export type CardModel = Omit<Model, "readme"> & { description?: ReactNode };

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
  return (
    <Card {...props} className={cn(className)}>
      <CardHeader className="border-b-0">
        <ModelHeader
          repo_id={repo_id}
          author={author}
          name={name}
          link={link}
          likes={likes}
          downloads={downloads}
          headingProps={{ size: "sm" }}
        />
      </CardHeader>
      <CardContent className="flex flex-col">
        {description ? <p>{description}</p> : null}
      </CardContent>
      <CardFooter className="gap-4">
        <ModelResults
          className="flex-1 py-2 text-xs"
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
        <Button asChild className="ml-auto h-auto p-0" variant="link">
          <Link href={`/models/${encodeURIComponent(id)}`} target="_blank">
            View details
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
