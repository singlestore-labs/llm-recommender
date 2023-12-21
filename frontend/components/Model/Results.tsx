import { HTMLAttributes } from "react";
import { ComponentProps, ModelResults as TModelResults } from "@/types";
import { Heading } from "@/components/Heading";
import { Card } from "@/components/ui/card";
import { cn } from "@/utils";

export type ModelResultsProps = ComponentProps<
  HTMLAttributes<HTMLDivElement>,
  { results: TModelResults }
>;

const resultsTitleMap: Record<keyof TModelResults, string> = {
  score: "Average",
  arc: "ARC",
  hellaswag: "HellaSwag",
  mmlu: "MMLU",
  truthfulqa: "TruthfulQA",
  winogrande: "Winograde",
  gsm8k: "GSM8K",
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
          ([key, value]) => (
            <li
              key={key}
              className="flex flex-1 flex-col items-center justify-center text-center first:border-l-0 lg:border-l"
            >
              <Heading className="text-lg">{resultsTitleMap[key]}</Heading>
              <p className="text-lg">{value}</p>
            </li>
          ),
        )}
      </ul>
    </Card>
  );
}
