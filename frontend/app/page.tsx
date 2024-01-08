"use client";

import { useCallback, useState } from "react";
import { ScanSearch } from "lucide-react";

import { Defined } from "@/types";
import type { SearchModels } from "@/app/api/models/search/route";
import { api } from "@/utils/api";
import { Heading } from "@/components/Heading";
import { UseCaseForm, UseCaseFormProps } from "@/components/UseCase/Form";
import { UseCaseModels, UseCaseModelsProps } from "@/components/UseCase/Models";
import { Dots } from "@/components/Dots";

export default function Home() {
  const [models, setModels] = useState<UseCaseModelsProps["models"]>([]);
  const [isModelsLoading, setIsModelsLoading] = useState(false);

  const getModels = useCallback(async (prompt: string) => {
    try {
      setIsModelsLoading(true);
      const response = await api.post<SearchModels>(`/models/search`, { body: { prompt } });

      const models = response.data.map((model) => {
        const details: UseCaseModelsProps["models"][number]["details"] = [
          { label: "Similarity score", value: model.avgSimilarity.toFixed(4), icon: ScanSearch },
        ];
        return { ...model, details } satisfies UseCaseModelsProps["models"][number];
      });

      setModels(models);
    } catch (error: any) {
      setModels([]);
    } finally {
      setIsModelsLoading(false);
    }
  }, []);

  const handleUseCaseFormSubmit = useCallback<Defined<UseCaseFormProps["onSubmit"]>>(
    (values) => {
      getModels(values.prompt);
    },
    [getModels],
  );

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center pt-16">
      <Dots className="fixed" />

      <Heading as="h2" size="hero" className="text-center leading-normal">
        Find the most appropriate LLM for your use case with the LLM Recommender
      </Heading>

      <UseCaseForm className="mb-24 mt-12" isDisabled={isModelsLoading} onSubmit={handleUseCaseFormSubmit} />

      <UseCaseModels models={models} isLoading={isModelsLoading} scrollToFirst />
    </div>
  );
}
