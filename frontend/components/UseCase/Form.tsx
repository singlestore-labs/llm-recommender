"use client";

import { useRef } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { SendHorizontal } from "lucide-react";
import * as z from "zod";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormField,
  FormItem,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { Textarea, TextareaProps } from "@/components/ui/textarea";
import { cn } from "@/utils";

export const useCaseFormSchema = z.object({
  prompt: z.string().min(16).max(1024),
});

export type UseCaseFormSchema = z.infer<typeof useCaseFormSchema>;

export type UseCaseFormProps = {
  className?: string;
  isDisabled?: boolean;
  onSubmit?: SubmitHandler<UseCaseFormSchema>;
};

export function UseCaseForm({
  className,
  isDisabled,
  onSubmit,
}: UseCaseFormProps) {
  const buttonRef = useRef<HTMLButtonElement | null>(null);

  const form = useForm<UseCaseFormSchema>({
    resolver: zodResolver(useCaseFormSchema),
    defaultValues: { prompt: "" },
  });

  const handleSubmit: SubmitHandler<UseCaseFormSchema> = (values, event) => {
    event?.preventDefault();
    onSubmit?.(values, event);
  };

  const handleTextareaKeyDown: TextareaProps["onKeyDown"] = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      buttonRef.current?.click();
    }
  };

  return (
    <Card className={cn("w-full overflow-hidden", className)}>
      <CardContent className="p-0">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="relative">
            <FormField
              control={form.control}
              name="prompt"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Textarea
                      className="resize-none rounded-none border-none bg-none py-4 pl-6 pr-[calc(theme(spacing.6)+3.25rem)] text-lg focus-visible:ring-0 focus-visible:ring-offset-0"
                      rows={4}
                      placeholder="Which model to choose for chatbot development?"
                      onKeyDown={handleTextareaKeyDown}
                      autoFocus
                      {...field}
                      disabled={isDisabled}
                    />
                  </FormControl>
                  <FormMessage className="px-6 pb-4 pt-2" />
                </FormItem>
              )}
            />
            <Button
              ref={buttonRef}
              type="submit"
              className="group absolute bottom-4 right-4 ml-auto"
              disabled={isDisabled}
            >
              <SendHorizontal className="w-5 transition group-active:translate-x-1" />
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
