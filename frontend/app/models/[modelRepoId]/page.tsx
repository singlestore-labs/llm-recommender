import { Model } from "@/types";

import { ModelDetails } from "@/components/Model/Details";
import { eleganceClient } from "@/services/eleganceClient";
import { notFound } from "next/navigation";

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
    <div className="flex flex-1 pt-16">
      <ModelDetails model={model} />
    </div>
  );
}
