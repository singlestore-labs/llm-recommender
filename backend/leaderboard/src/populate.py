import pandas as pd

from src.display.formatting import has_no_nan_values
from src.display.utils import AutoEvalColumn, baseline_row
from src.leaderboard.filter_models import filter_models
from src.leaderboard.read_evals import get_raw_eval_results


def get_leaderboard_df(results_path: str, requests_path: str, cols: list, benchmark_cols: list) -> pd.DataFrame:
    raw_data = get_raw_eval_results(results_path, requests_path)
    all_data_json = [v.to_dict() for v in raw_data]
    all_data_json.append(baseline_row)
    filter_models(all_data_json)

    df = pd.DataFrame.from_records(all_data_json)
    df = df.sort_values(by=[AutoEvalColumn.average.name], ascending=False)
    df = df[cols].round(decimals=2)

    # filter out if any of the benchmarks have not been produced
    df = df[has_no_nan_values(df, benchmark_cols)]
    return df
