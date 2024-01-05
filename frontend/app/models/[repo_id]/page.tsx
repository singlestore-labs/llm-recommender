import pick from "lodash.pick";

import { DB } from "@/types";

import { ModelHeader } from "@/components/Model/Header";
import { notFound } from "next/navigation";
import { ModelResults } from "@/components/Model/Results";
import { ModelReadme } from "@/components/Model/Readme";
import { eleganceServerClient } from "@/services/eleganceServerClient";
// import { Card, CardContent, CardHeader } from "@/components/ui/card";
// import { Heading } from "@/components/Heading";

export default async function PageModel({
  params,
}: {
  params: { repo_id: string };
}) {
  const repo_id = decodeURIComponent(params.repo_id);

  const [model, readme_parts] = await Promise.all([
    eleganceServerClient.controllers.findOne<DB.Model>({
      collection: "models",
      where: `repo_id = '${repo_id}'`,
    }),
    eleganceServerClient.controllers.findMany<Pick<DB.ModelReadme, "text">[]>({
      collection: "model_readmes",
      columns: ["text"],
      where: `model_repo_id = '${repo_id}'`,
      extra: "ORDER BY created_at DESC",
    }),
  ]);

  let readme = "";
  if (readme_parts?.length) {
    readme = readme_parts.reduce((acc, curr) => acc + curr.text, "");
    readme = readme.slice(readme.indexOf("#"));
  }

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
        withExternalLink
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
        <div className="relative order-2 w-full max-lg:h-full lg:order-1 lg:min-h-0 lg:w-[calc(theme(width.2/3)-theme(spacing.4))]">
          <ModelReadme
            className="absolute left-0 top-0 max-h-full w-full"
            expandedClassName="static h-auto"
            repo_id={model.repo_id}
            text={readme}
          />
        </div>

        {/* <div className="order-1 w-full lg:order-2 lg:w-[calc(theme(width.1/3)-theme(spacing.4))]">
          <Card>
            <CardHeader size="md">
              <Heading as="h3" size="md">
                X posts
              </Heading>
            </CardHeader>
            <CardContent className="py-4">X posts</CardContent>
          </Card>
        </div> */}
      </div>
    </div>
  );
}
