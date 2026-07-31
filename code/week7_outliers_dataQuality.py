import pandas as pd

# load in listing and sold datasets
listing_df = pd.read_csv("output/listing.csv")
sold_df = pd.read_csv("output/sold.csv")

target_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']

def iqr(df, fields):
    df_flagged = df.copy()
    
    # Track overall outlier row mask
    any_outlier_mask = pd.Series(False, index=df.index)
    
    for col in fields:
        Q1 = df_flagged[col].quantile(0.25)
        Q3 = df_flagged[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        # Flag specific column outliers 
        flag_col = f"{col}_Outlier_Flag"
        is_outlier = (df_flagged[col] < lower) | (df_flagged[col] > upper)
        df_flagged[flag_col] = is_outlier
        
        # Combine into overall mask
        any_outlier_mask = any_outlier_mask | is_outlier

    # Create clean dataset (rows with no outliers in any target field)
    df_clean = df_flagged[~any_outlier_mask].copy()
    
    return df_flagged, df_clean

listing_flagged, listing_clean = iqr(listing_df, target_fields)
sold_flagged, sold_clean = iqr(sold_df, target_fields)

print(f'Number of rows before filtering the listings dataset: {len(listing_df)}, number of rows after filtering listings dataset: {len(listing_clean)}\n')
print(f'Number of rows before filtering the sold dataset: {len(sold_df)}, number of rows after filtering sold dataset: {len(sold_clean)}\n')

print(f'Median values for the listings dataset before filtering outliers: {listing_df[target_fields].median().to_dict()},\n median values for the listings dataset after filtering out outliers: {listing_clean[target_fields].median().to_dict()}\n')
print(f'Median values for the sold dataset before filtering outliers: {sold_df[target_fields].median().to_dict()},\n median values for the sold dataset after filtering out outliers: {sold_clean[target_fields].median().to_dict()}')

listing_flagged.to_csv("output/listing.csv", index=False)
listing_clean.to_csv("output/listing_clean.csv", index=False)

sold_flagged.to_csv("output/sold.csv", index=False)
sold_clean.to_csv("output/sold_clean.csv", index=False)