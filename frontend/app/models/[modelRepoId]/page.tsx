import pick from "lodash.pick";

import { Model } from "@/types";

import { ModelHeader } from "@/components/Model/Header";
import { eleganceClient } from "@/services/eleganceClient";
import { notFound } from "next/navigation";
import { ModelResults } from "@/components/Model/Results";
import { ModelReadme } from "@/components/Model/Readme";

// http://localhost:3000/models/jondurbin%2Fairoboros-l2-70b-2.2.1

export default async function PageModel({
  params,
}: {
  params: { modelRepoId: string };
}) {
  const modelRepoId = decodeURIComponent(params.modelRepoId);

  const model = await eleganceClient.requests.findOne<Model>({
    collection: "models",
    where: `repo_id = '${modelRepoId}'`,
  });

  if (!model || !Object.keys(model).length) {
    notFound();
  }

  return (
    <div className="flex flex-1 flex-col gap-16 pt-16 ">
      <ModelHeader
        {...pick(model, [
          "repo_id",
          "name",
          "author",
          "link",
          "likes",
          "downloads",
        ])}
      />
      <ModelResults
        results={pick(model, [
          "score",
          "arc",
          "hellaswag",
          "mmlu",
          "truthfulqa",
          "winogrande",
          "gsm8k",
        ])}
      />
      <div className="flex w-full max-w-full flex-1 flex-wrap items-start gap-8">
        <ModelReadme
          className="order-2 w-full lg:order-1 lg:w-[calc(theme(width.2/3)-theme(spacing.4))]"
          repo_id={model.repo_id}
          readme={model.readme}
        />
        <div className="order-1 w-full lg:order-2 lg:w-[calc(theme(width.1/3)-theme(spacing.4))]">
          Side
        </div>
      </div>
    </div>
  );
}
