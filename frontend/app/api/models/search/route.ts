import { NextRequest, NextResponse } from "next/server";
import _groupBy from "lodash.groupby";
import _omit from "lodash.omit";

import type { DB } from "@/types";
import { eleganceServerClient } from "@/services/eleganceServerClient";
import { countTokens } from "@/utils/ai";

export type SearchModels = (DB.Model & { description?: string })[];

const {
  ai,
  controllers: { findMany, findOne, vectorSearch, createChatCompletion },
} = eleganceServerClient;

export async function POST(request: NextRequest) {
  try {
    const {
      body: { prompt },
    } = await request.json();

    if (!prompt) {
      return NextResponse.json("prompt field is required", { status: 400 });
    }

    const promptEmbedding = (await ai.createEmbedding(prompt))[0];

    const [models, modelReadmes, redditPosts, githubRepos] = await Promise.all([
      (async () => {
        return (
          await vectorSearch<DB.WithSimilarity<DB.Model>[]>({
            collection: "models",
            embeddingField: "embedding",
            query: prompt,
            queryEmbedding: promptEmbedding,
            limit: 5,
          })
        ).map((i) => ({ ...i, model_repo_id: i.repo_id }));
      })() as Promise<DB.WithSimilarity<DB.Model & { model_repo_id: DB.Model["repo_id"] }>[]>,
      vectorSearch<DB.WithSimilarity<DB.ModelReadme>[]>({
        collection: "model_readmes",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
      vectorSearch<DB.WithSimilarity<DB.ModelRedditPost>[]>({
        collection: "model_reddit_posts",
        embeddingField: "embedding",
        query: prompt,
        queryEmbedding: promptEmbedding,
        limit: 25,
      }),
      vectorSearch<DB.WithSimilarity<DB.ModelGitHubRepo>[]>({
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
          const totalSimilarity = records.reduce((acc, curr) => acc + curr.similarity, 0);
          const avgSimilarity = records.length > 0 ? totalSimilarity / records.length : 0;
          return { repoId, avgSimilarity };
        }),
      )
    )
      .sort((a, b) => b.avgSimilarity - a.avgSimilarity)
      .slice(0, 5);

    let searchModels: SearchModels = await Promise.all(
      searchResults.map(async (searchResult) => {
        const where = `model_repo_id = '${searchResult.repoId}'`;

        const [model, readmes, redditPosts, githubRepos] = await Promise.all([
          findOne<DB.Model>({
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
          }),

          findMany<Pick<DB.ModelReadme, "clean_text">[]>({
            collection: "model_readmes",
            columns: ["clean_text"],
            where,
          }),

          findMany<Pick<DB.ModelRedditPost, "title" | "clean_text">[]>({
            collection: "model_reddit_posts",
            columns: ["title", "clean_text"],
            where,
          }),

          findMany<Pick<DB.ModelGitHubRepo, "name" | "clean_text">[]>({
            collection: "model_github_repos",
            columns: ["name", "clean_text"],
            where,
          }),
        ]);

        const readme = readmes.reduce((acc, curr) => acc + curr.clean_text, "");
        const github = githubRepos.reduce((acc, curr) => acc + `Repo: ${curr.name}\n${curr.clean_text}`, "");
        const reddit = redditPosts.reduce((acc, curr) => acc + `Post: ${curr.title}\n${curr.clean_text}`, "");
        const description = await createDescriptionCompletion(prompt, model.repo_id, readme, github, reddit);

        return { ...model, description };
      }),
    );

    return NextResponse.json(searchModels);
  } catch (error: any) {
    console.log(error);
    return NextResponse.json(error, {
      status: error.status,
    });
  }
}

async function createDescriptionCompletion(
  prompt: string,
  repoId: string,
  readme: string,
  github: string,
  reddit: string,
) {
  let completion = "";

  const systemRole = `
    In the role of the LLM Recommender, generate a brief text description (maximum 256 chars),
    describing why an LLM aligns well with the user's use case.
    Emphasize an LLM strengths, capabilities, and distinguishing features.
    Please response in a descriptive format.
    Don't include links and an LLM name in your response.
  `.trim();

  let completionPrompt = `
    The user use case: ${prompt}.
    LLM name: ${repoId}.
    LLM description: ${readme}.
    What people build on GitHub using this LLM: ${github}.
    What people share on Reddit about this LLM: ${reddit}.
  `.trim();

  const tokensLimit = 4000 - countTokens(systemRole);

  while (countTokens(completionPrompt) > tokensLimit) {
    completionPrompt = completionPrompt.slice(-1, completionPrompt.lastIndexOf("."));
  }

  completion = (await createChatCompletion({ systemRole, prompt: completionPrompt })) ?? "";

  return completion;
}
