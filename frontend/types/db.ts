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
  readme: string;
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
