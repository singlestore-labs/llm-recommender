# LLM Recommender

## Getting Started

1. Sign up for [SingleStore](https://www.singlestore.com/cloud-trial/), create a workspace and database
2. Create a `.env` file based on the `.env.sample` file
3. Set up a `.venv` environment
4. Install the required dependencies from the `requirements.txt`

## Start Development Environment

1. Run the `nodemon app.py` command in the root of the project

## Generating a Leaderboard Dataset

1. Go to `./leaderboard`
2. Run the `app.py` file
3. Copy a `leaderboard.json` file from the `./leaderboard/datasets` to `../frontend/public/datasets`
