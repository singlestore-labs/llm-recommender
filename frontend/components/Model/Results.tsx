import { HTMLAttributes } from "react";

import { ComponentProps, ModelResults as TModelResults } from "@/types";
import { Heading } from "@/components/Heading";
import { Card } from "@/components/ui/card";
import { ExternalLink } from "@/components/ExternalLink";
import { cn } from "@/utils";

export type ModelResultsProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  { results: TModelResults }
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
  results,
  ...props
}: ModelResultsProps) {
  return (
    <Card {...props} className={cn("overflow-hidden p-4", className)}>
      <ul className="max-lg:grid-auto-fit-[10.75rem] gap-4 max-lg:grid lg:flex">
        {(Object.entries(results) as [keyof TModelResults, number][]).map(
          ([key, value]) => {
            const map = resultsMap[key];
            return (
              <li
                key={key}
                className="group flex flex-1 flex-col items-center justify-center text-center first:border-l-0 lg:border-l"
              >
                <Heading className="text-md relative flex items-center">
                  {map.label}
                  {map.link ? <ExternalLink href={map.link} /> : null}
                </Heading>
                <p className="text-md">{value}</p>
              </li>
            );
          },
        )}
      </ul>
    </Card>
  );
}
