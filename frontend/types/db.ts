export type Model = {
  id: number;
  name: string;
  author: string;
  repo_id: string;
  score: number;
  arc: number;
  hellaswag: number;
  mmlu: number;
  truthfulqa: number;
  winogrande: number;
  gsm8k: number;
  link: string;
  downloads: number;
  likes: number;
  still_on_hub: number;
  created_at: number;
};

export type ModelReadme = {
  id: number;
  model_repo_id: Model["repo_id"];
  text: string;
  clean_text: string;
};

export type ModelRedditPost = {
  id: number;
  model_repo_id: string;
  post_id: string;
  title: string;
  clean_text: string;
  link: string;
  created_at: number;
};

export type ModelGitHubRepo = {
  id: number;
  model_repo_id: string;
  repo_id: string;
  name: string;
  description: string;
  clean_readme: string;
  link: string;
  created_at: string;
};

export type ModelResults = Record<
  Extract<
    keyof Model,
    | "score"
    | "arc"
    | "hellaswag"
    | "mmlu"
    | "truthfulqa"
    | "winogrande"
    | "gsm8k"
  >,
  number
>;

export type WithSimilarity<T extends object> = T & { similarity: number };
