import { useEffect, useRef } from "react";

import { CardModel, ModelCard } from "./Card";
import { ComponentProps } from "@/types";
import { cn } from "@/utils";

export type ModelListProps = ComponentProps<
  "ul",
  { models: CardModel[]; scrollToFirst?: boolean }
>;

export function ModelList({
  children,
  className,
  models,
  scrollToFirst,
  ...props
}: ModelListProps) {
  const firstModelRef = useRef<HTMLLIElement | null>(null);

  useEffect(() => {
    if (firstModelRef.current && scrollToFirst) {
      firstModelRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [models, scrollToFirst]);

  return (
    <>
      <ul {...props} className={cn("flex w-full flex-col gap-4", className)}>
        {models.map((model, i) => {
          const isFirst = i === 0;
          return (
            <li
              key={model.id}
              ref={isFirst ? firstModelRef : null}
              className={cn("w-full max-w-full", isFirst && "scroll-mt-4")}
            >
              <ModelCard {...model} />
            </li>
          );
        })}
      </ul>
      {children}
    </>
  );
}
