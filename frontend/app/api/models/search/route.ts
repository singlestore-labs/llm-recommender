import { NextRequest, NextResponse } from "next/server";

import type { Model } from "@/types";
import { eleganceServerClient } from "@/services/eleganceServerClient";

type _Model = Omit<Model, "readme">;

export type SearchModels = (_Model & { description?: string })[];

export async function POST(request: NextRequest) {
  try {
    const {
      body: { prompt },
    } = await request.json();

    if (!prompt) {
      return NextResponse.json("prompt field is required", { status: 400 });
    }

    const searchResults = await eleganceServerClient.controllers.vectorSearch<
      {
        id: number;
        model_repo_id: string;
        text: string;
        similarity: number;
      }[]
    >({
      collection: "model_embeddings",
      embeddingField: "embedding",
      query: prompt,
      limit: 5,
    });

    const searchResultsRepoIds = searchResults
      .map(({ model_repo_id }) => `'${model_repo_id}'`)
      .join(",");

    const searchModels = await eleganceServerClient.controllers.findMany<
      _Model[]
    >({
      collection: "models",
      columns: [
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
        "downloads",
        "likes",
        "still_on_hub",
      ],
      where: `repo_id IN (${searchResultsRepoIds})`,
      extra: `ORDER BY FIELD(repo_id, ${searchResultsRepoIds})`,
    });

    let models: SearchModels = [];

    for await (const [i, searchModel] of searchModels.entries()) {
      const searchResult = searchResults[i].text;

      const description =
        (await eleganceServerClient.controllers.createChatCompletion({
          systemRole: `
            In the role of the LLM Recommender, furnish a brief text description (maximum 192 chars),
            illustrating why this LLM aligns well with the user's use case.
            Emphasize its strengths, capabilities, and distinguishing features.
            Please craft your response in a descriptive format without mentioning
            the model's name or including links.
          `,
          prompt: `The user use case: ${prompt}. The most appropriate model is: ${searchResult}`,
        })) ?? "";

      models.push({ ...searchModel, description });
    }

    return NextResponse.json(models);
  } catch (error: any) {
    return NextResponse.json(error, { status: error.status });
  }
}
