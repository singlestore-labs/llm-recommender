"use client";

import { useCallback, useState } from "react";

import { Defined, Model } from "@/types";
import { eleganceClient } from "@/services/eleganceClient";
import { Heading } from "@/components/Heading";
import { UseCaseForm, UseCaseFormProps } from "@/components/UseCase/Form";
import { UseCaseModels, UseCaseModelsProps } from "@/components/UseCase/Models";
import { Dots } from "@/components/Dots";

const modelColumns: Exclude<
  keyof UseCaseModelsProps["models"][number],
  "description"
>[] = [
  "id",
  "name",
  "author",
  "repo_id",
  "score",
  "arc",
  "hellaswag",
  "mmlu",
  "truthfulqa",
  "winogrande",
  "gsm8k",
  "link",
  "likes",
  "downloads",
];

export default function Home() {
  const [models, setModels] = useState<UseCaseModelsProps["models"]>([]);
  const [prompt, setPrompt] = useState("");
  const [isModelsLoading, setIsModelsLoading] = useState(false);

  const getModels = useCallback(async (prompt: string) => {
    try {
      setIsModelsLoading(true);

      const models = await eleganceClient.requests.findMany<
        Pick<Model, (typeof modelColumns)[number]>[]
      >({
        collection: "models",
        columns: modelColumns,
        limit: 5,
      });

      setModels(
        models.map((model) => ({
          ...model,
          description:
            "This model might be useful for your use case because...",
        })),
      );
    } catch (error) {
      console.error(error);
      setModels([]);
    } finally {
      setIsModelsLoading(false);
    }
  }, []);

  const handleUseCaseFormSubmit = useCallback<
    Defined<UseCaseFormProps["onSubmit"]>
  >(
    (values) => {
      setPrompt(values.prompt);
      getModels(values.prompt);
    },
    [getModels],
  );

  const handleRegenerateModelsClick = useCallback<
    Defined<UseCaseModelsProps["onRenegerateClick"]>
  >(() => {
    getModels(prompt);
  }, [prompt, getModels]);

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center pt-16">
      <Dots className="fixed" />

      <Heading as="h2" size="hero" className="text-center leading-normal">
        Find the most appropriate LLM model for your use case with the LLM
        Recommender
      </Heading>

      <UseCaseForm
        className="mb-32 mt-12"
        isDisabled={isModelsLoading}
        onSubmit={handleUseCaseFormSubmit}
      />

      <UseCaseModels
        models={models}
        isLoading={isModelsLoading}
        onRenegerateClick={handleRegenerateModelsClick}
        scrollToFirst
      />
    </div>
  );
}
