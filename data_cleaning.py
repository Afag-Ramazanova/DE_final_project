# %%
import pandas as pd

# %%
combined_df_no_na = pd.read_csv(r"data/amazon_products_dataset.csv")

# %%
combined_df_no_na

# %%
combined_df_no_na["ratings"] = pd.to_numeric(
    combined_df_no_na["ratings"], errors="coerce"
)
combined_df_no_na["no_of_ratings"] = pd.to_numeric(
    combined_df_no_na["no_of_ratings"], errors="coerce"
)
combined_df_no_na["discount_price"] = pd.to_numeric(
    combined_df_no_na["discount_price"].str.replace(r"[^\d.]", "", regex=True),
    errors="coerce",
)
combined_df_no_na["actual_price"] = pd.to_numeric(
    combined_df_no_na["actual_price"].str.replace(r"[^\d.]", "", regex=True),
    errors="coerce",
)

# %%
combined_df_no_na

# %%
combined_df_no_na.to_csv(r"data/cleaned_amazon_products_dataset.csv", index=False)

# %%
