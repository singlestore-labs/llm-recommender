import os

# clone / pull the lmeh eval data
H4_TOKEN = os.environ.get("H4_TOKEN", None)

REPO_ID = "HuggingFaceH4/open_llm_leaderboard"
QUEUE_REPO = "open-llm-leaderboard/requests"
RESULTS_REPO = "open-llm-leaderboard/results"

DATA_PATH = os.getenv("HF_HOME", "./backend/leaderboard/data")

EVAL_REQUESTS_PATH = os.path.join(DATA_PATH, "eval-queue")
EVAL_RESULTS_PATH = os.path.join(DATA_PATH, "eval-results")

PATH_TO_COLLECTION = "open-llm-leaderboard/llm-leaderboard-best-models-652d6c7965a4619fb5c27a03"
