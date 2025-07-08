import pandas as pd
from sklearn.datasets import load_wine

wine_data = load_wine()

# Convert data to pandas dataframe
wine_df = pd.DataFrame(wine_data.data, columns=wine_data.feature_names)

# Add the target label
wine_df["target"] = wine_data.target

# Take a preview
print(wine_df.head())