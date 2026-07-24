#=============================================
# preprocessor.py - Olympics Analysis System
#=============================================

import pandas as pd

def preprocess(df, region_df):
    """Preprocess the Olympics dataset."""
    # Merge with region_df to get country/region names
    df = df.merge(region_df, on='NOC', how='left')

  

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # One-hot encode Medal column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    # Ensure medal columns exist (Gold, Silver, Bronze)
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in df.columns:
            df[medal] = 0

    return df