import { NextRequest, NextResponse } from "next/server";
import _groupBy from "lodash.groupby";
import _omit from "lodash.omit";

import type { Model } from "@/types";
import { eleganceServerClient } from "@/services/eleganceServerClient";

export type SearchModels = (Omit<Model, "readme"> & { description?: string })[];

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

    const [models, redditPosts, githubRepos] = await Promise.all([
      eleganceServerClient.controllers.vectorSearch<
        {
          id: number;
          model_repo_id: string;
          similarity: number;
        }[]
      >({
        collection: "model_embeddings",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 5,
      }),
      eleganceServerClient.controllers.vectorSearch<
        {
          id: number;
          model_repo_id: string;
          post_id: string;
          title: string;
          text: string;
          link: string;
          created_at: string;
          similarity: number;
        }[]
      >({
        collection: "models_reddit_posts",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
      eleganceServerClient.controllers.vectorSearch<
        {
          id: number;
          model_repo_id: string;
          repo_id: string;
          name: string;
          description: string;
          readme: string;
          link: string;
          created_at: string;
          similarity: number;
        }[]
      >({
        collection: "models_github_repos",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
    ]);

    const [redditPostsGroup, githubReposGroup] = [redditPosts, githubRepos].map(
      (records) => _groupBy(records, "model_repo_id"),
    ) as [
      Record<string, (typeof redditPosts)[number][]>,
      Record<string, (typeof githubRepos)[number][]>,
    ];

    const grouppedSearchResults = _groupBy(
      [...models, ...redditPosts, ...githubRepos],
      "model_repo_id",
    ) as Record<
      string,
      (
        | (typeof models)[number]
        | (typeof redditPosts)[number]
        | (typeof githubRepos)[number]
      )[]
    >;

    const searchResults = (
      await Promise.all(
        Object.entries(grouppedSearchResults).map(async ([repoId, records]) => {
          const { readme, ...model } =
            await eleganceServerClient.controllers.findOne<Model>({
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
                "readme",
              ],
              where: `repo_id = '${repoId}'`,
            });

          const totalSimilarity = records.reduce((acc, curr) => {
            return acc + curr.similarity;
          }, 0);

          const avgSimilarity =
            records.length > 0 ? totalSimilarity / records.length : 0;

          const redditPostsContext =
            redditPostsGroup[repoId]?.reduce(
              (acc, curr) => `${acc}\nReddit Post: ${curr.title}\n${curr.text}`,
              "",
            ) ?? "";

          const githubReposContext =
            githubReposGroup[repoId]?.reduce(
              (acc, curr) =>
                `${acc}\nGitHub Repository: ${curr.name}\n${curr.description}\n${curr.readme}`,
              "",
            ) ?? "";

          return {
            ...model,
            avgSimilarity,
            readme,
            redditPostsContext,
            githubReposContext,
          };
        }),
      )
    )
      .sort((a, b) => b.avgSimilarity - a.avgSimilarity)
      .slice(0, 5);

    let searchModels: SearchModels = await Promise.all(
      searchResults.map(async (searchResult) => {
        let description: string;

        try {
          description =
            (await eleganceServerClient.controllers.createChatCompletion({
              systemRole,
              prompt: `
                The user use case: ${prompt}.
                The most appropriate model is: ${searchResult.repo_id}.
                This model description: ${searchResult.readme}.
                Related GitHub repositories context: ${searchResult.githubReposContext}.
                Related Reddit posts context: ${searchResult.redditPostsContext}.
              `,
            })) ?? "";
        } catch (error) {
          description = "";
        }

        return {
          ..._omit(searchResult, [
            "avgSimilarity",
            "readme",
            "redditPostsContext",
            "githubReposContext",
          ]),
          description,
        };
      }),
    );

    return NextResponse.json(searchModels);
  } catch (error: any) {
    return NextResponse.json(error, { status: error.status });
  }
}
