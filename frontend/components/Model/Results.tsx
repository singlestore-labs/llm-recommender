import { HTMLAttributes } from "react";

import { ComponentProps, ModelResults as TModelResults } from "@/types";
import { cn } from "@/utils";
import { Heading } from "@/components/Heading";
import { Card } from "@/components/ui/card";
import { ExternalLink } from "@/components/ExternalLink";

export type ModelResultsProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  { results: TModelResults; listClassName?: string; borderClassName?: string }
>;

const resultsMap: Record<
  keyof TModelResults,
  { label: string; link?: string }
> = {
  score: {
    label: "Average",
  },
  arc: {
    label: "ARC",
    link: "https://arxiv.org/abs/1803.05457",
  },
  hellaswag: {
    label: "HellaSwag",
    link: "https://arxiv.org/abs/1905.07830",
  },
  mmlu: {
    label: "MMLU",
    link: "https://arxiv.org/abs/2009.03300",
  },
  truthfulqa: {
    label: "TruthfulQA",
    link: "https://arxiv.org/abs/2109.07958",
  },
  winogrande: {
    label: "Winograde",
    link: "https://arxiv.org/abs/1907.10641",
  },
  gsm8k: {
    label: "GSM8K",
    link: "https://arxiv.org/abs/2110.14168",
  },
};

export function ModelResults({
  className,
  listClassName,
  borderClassName,
  results,
  ...props
}: ModelResultsProps) {
  return (
    <Card
      {...props}
      className={cn("overflow-x-auto overflow-y-hidden py-4", className)}
    >
      <ul
        className={cn(
          "flex w-full max-w-full items-stretch justify-between gap-4",
          listClassName,
        )}
      >
        {(Object.entries(results) as [keyof TModelResults, number][]).map(
          ([key, value], i, arr) => {
            const isLast = !arr[i + 1];
            const map = resultsMap[key];
            return (
              <li
                key={key}
                className="group relative flex flex-1 flex-col items-center justify-center px-4 text-center"
              >
                <Heading
                  as="h6"
                  className="relative flex items-center leading-tight [font-size:inherit]"
                >
                  {map.label}
                  {map.link ? <ExternalLink href={map.link} /> : null}
                </Heading>
                <p>{value}</p>
                {!isLast ? (
                  <span
                    className={cn(
                      "absolute -right-2 top-0 h-full w-px bg-border leading-tight",
                      borderClassName,
                    )}
                  />
                ) : null}
              </li>
            );
          },
        )}
      </ul>
    </Card>
  );
}
