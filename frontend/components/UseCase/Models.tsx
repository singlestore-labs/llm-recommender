import { ComponentProps } from "@/types";
import { cn } from "@/utils";
import { ModelList, ModelListProps } from "@/components/Model/List";
import { Button } from "@/components/ui/button";

export type UseCaseModelsProps = ComponentProps<
  ModelListProps,
  {
    isLoading?: boolean;
    onRenegerateClick?: () => void;
  }
>;

export function UseCaseModels({
  className,
  models,
  isLoading,
  onRenegerateClick,
  ...props
}: UseCaseModelsProps) {
  return (
    <ModelList
      {...props}
      className={cn("flex w-full flex-col", className)}
      models={models}
    >
      {models.length && onRenegerateClick ? (
        <Button
          className="mx-auto mt-6"
          disabled={isLoading}
          onClick={onRenegerateClick}
          isLoading={isLoading}
        >
          Regenerate
        </Button>
      ) : null}
    </ModelList>
  );
}
