from transformers import AutoConfig, AutoTokenizer


def is_model_on_hub(
        model_name: str, revision: str, token: str = None, trust_remote_code=False, test_tokenizer=False) -> tuple[
        bool, str]:
    try:
        config = AutoConfig.from_pretrained(model_name, revision=revision,
                                            trust_remote_code=trust_remote_code, token=token)
        if test_tokenizer:
            try:
                tk = AutoTokenizer.from_pretrained(model_name, revision=revision,
                                                   trust_remote_code=trust_remote_code, token=token)
            except ValueError as e:
                return (
                    False,
                    f"uses a tokenizer which is not in a transformers release: {e}",
                    None
                )
            except Exception as e:
                return (False, "'s tokenizer cannot be loaded. Is your tokenizer class in a stable transformers release, and correctly configured?", None)
        return True, None, config

    except ValueError:
        return (
            False,
            "needs to be launched with `trust_remote_code=True`. For safety reason, we do not allow these models to be automatically submitted to the leaderboard.",
            None
        )

    except Exception as e:
        return False, "was not found on hub!", None
