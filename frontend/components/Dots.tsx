import { ComponentProps } from "@/types";
import { cn } from "@/utils";

export type DotsProps = ComponentProps<"span">;

export function Dots({ className, ...props }: DotsProps) {
  return (
    <span
      {...props}
      className={cn(
        "absolute inset-0 left-0 top-0 -z-10 h-full w-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_60%,transparent_100%)]",
        className,
      )}
    />
  );
}
