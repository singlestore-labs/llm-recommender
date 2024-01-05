import { NextRequest, NextResponse } from "next/server";
import _groupBy from "lodash.groupby";
import _omit from "lodash.omit";

import type { DB } from "@/types";
import { eleganceServerClient } from "@/services/eleganceServerClient";

export type SearchModels = (DB.Model & {
  description?: string;
})[];

const systemRole = `
  In the role of the LLM Recommender, furnish a brief text description (maximum 256 chars),
  illustrating why this LLM aligns well with the user's use case.
  Emphasize its strengths, capabilities, and distinguishing features.
  Please craft your response in a descriptive format without mentioning
  the model's name or including links.
`;

export async function POST(request: NextRequest) {
  try {
    const {
      body: { prompt },
    } = await request.json();

    if (!prompt) {
      return NextResponse.json("prompt field is required", { status: 400 });
    }

    const promptEmbedding = (
      await eleganceServerClient.ai.createEmbedding(prompt)
    )[0];

    const [models, modelReadmes, redditPosts, githubRepos] = await Promise.all([
      (async () => {
        return (
          await eleganceServerClient.controllers.vectorSearch<
            DB.WithSimilarity<DB.Model>[]
          >({
            collection: "models",
            embeddingField: "embedding",
            query: prompt,
            queryEmbedding: promptEmbedding,
            limit: 5,
          })
        ).map((i) => ({ ...i, model_repo_id: i.repo_id }));
      })() as Promise<
        DB.WithSimilarity<DB.Model & { model_repo_id: DB.Model["repo_id"] }>[]
      >,
      eleganceServerClient.controllers.vectorSearch<
        DB.WithSimilarity<DB.ModelReadme>[]
      >({
        collection: "model_readmes",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
      eleganceServerClient.controllers.vectorSearch<
        DB.WithSimilarity<DB.ModelRedditPost>[]
      >({
        collection: "model_reddit_posts",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
      eleganceServerClient.controllers.vectorSearch<
        DB.WithSimilarity<DB.ModelGitHubRepo>[]
      >({
        collection: "model_github_repos",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
    ]);

    const grouppedSearchResults = _groupBy(
      [...models, ...modelReadmes, ...redditPosts, ...githubRepos],
      "model_repo_id",
    ) as Record<
      string,
      (
        | (typeof models)[number]
        | (typeof modelReadmes)[number]
        | (typeof redditPosts)[number]
        | (typeof githubRepos)[number]
      )[]
    >;

    const searchResults = (
      await Promise.all(
        Object.entries(grouppedSearchResults).map(async ([repoId, records]) => {
          const totalSimilarity = records.reduce((acc, curr) => {
            return acc + curr.similarity;
          }, 0);

          const avgSimilarity =
            records.length > 0 ? totalSimilarity / records.length : 0;

          return { repoId, avgSimilarity };
        }),
      )
    )
      .sort((a, b) => b.avgSimilarity - a.avgSimilarity)
      .slice(0, 5);

    let searchModels: SearchModels = await Promise.all(
      searchResults.map(async (searchResult) => {
        const model = await eleganceServerClient.controllers.findOne({
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
          where: `repo_id = '${searchResult.repoId}'`,
        });

        let description: string;

        try {
          description = "";
          // description =
          //   (await eleganceServerClient.controllers.createChatCompletion({
          //     systemRole,
          //     prompt: `
          //       The user use case: ${prompt}.
          //       The most appropriate model is: ${searchResult.repo_id}.
          //       This model description: ${searchResult.readme}.
          //       Related GitHub repositories context: ${searchResult.githubReposContext}.
          //       Related Reddit posts context: ${searchResult.redditPostsContext}.
          //     `,
          //   })) ?? "";
        } catch (error) {
          description = "";
        }

        return { ...model, description };
      }),
    );

    return NextResponse.json(searchModels);
  } catch (error: any) {
    return NextResponse.json(error, { status: error.status });
  }
}
