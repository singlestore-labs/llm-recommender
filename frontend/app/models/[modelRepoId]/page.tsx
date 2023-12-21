import pick from "lodash.pick";

import { Model } from "@/types";

import { ModelHeader } from "@/components/Model/Header";
import { eleganceClient } from "@/services/eleganceClient";
import { notFound } from "next/navigation";
import { ModelResults } from "@/components/Model/Results";
import { ModelReadme } from "@/components/Model/Readme";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Heading } from "@/components/Heading";

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
    <div className="flex flex-1 flex-col gap-12 pt-12 ">
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
      <div className="flex w-full max-w-full flex-1 flex-wrap items-start gap-8 lg:items-stretch">
        <div className="relative order-2 min-h-[50vh] w-full lg:order-1 lg:min-h-0 lg:w-[calc(theme(width.2/3)-theme(spacing.4))]">
          <ModelReadme
            className="absolute left-0 top-0 h-full w-full"
            expandedClassName="static h-auto"
            repo_id={model.repo_id}
            readme={model.readme.slice(model.readme.indexOf("#"))}
          />
        </div>

        <div className="order-1 w-full lg:order-2 lg:w-[calc(theme(width.1/3)-theme(spacing.4))]">
          <Card>
            <CardHeader size="md">
              <Heading as="h3" size="md">
                X posts
              </Heading>
            </CardHeader>
            <CardContent className="py-4">X posts</CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
