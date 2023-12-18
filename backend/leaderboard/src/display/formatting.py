def model_hyperlink(link, model_name):
    return f'<a target="_blank" href="{link}" style="color: var(--link-text-color); text-decoration: underline;text-decoration-style: dotted;">{model_name}</a>'


def make_clickable_model(model_name):
    link = f"https://huggingface.co/{model_name}"

    details_model_name = model_name.replace("/", "__")
    details_link = f"https://huggingface.co/datasets/open-llm-leaderboard/details_{details_model_name}"

    return model_hyperlink(link, model_name) + "  " + model_hyperlink(details_link, "📑")


def make_model_link(model_name):
    link = f"https://huggingface.co/{model_name}"
    return link


def has_no_nan_values(df, columns):
    return df[columns].notna().all(axis=1)
