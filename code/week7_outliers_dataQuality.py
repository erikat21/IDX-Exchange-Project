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
# Number of rows before filtering the listings dataset: 621108, number of rows after filtering listings dataset: 535877

print(f'Number of rows before filtering the sold dataset: {len(sold_df)}, number of rows after filtering sold dataset: {len(sold_clean)}\n')
# Number of rows before filtering the sold dataset: 460641, number of rows after filtering sold dataset: 388990

print(f'Median values for the listings dataset before filtering outliers: {listing_df[target_fields].median().to_dict()},\n median values for the listings dataset after filtering out outliers: {listing_clean[target_fields].median().to_dict()}\n')
# Median values for the listings dataset before filtering outliers: {'ClosePrice': 855000.0, 'LivingArea': 1672.0, 'DaysOnMarket': 11.0},
# median values for the listings dataset after filtering out outliers: {'ClosePrice': 828000.0, 'LivingArea': 1614.0, 'DaysOnMarket': 9.0}

print(f'Median values for the sold dataset before filtering outliers: {sold_df[target_fields].median().to_dict()},\n median values for the sold dataset after filtering out outliers: {sold_clean[target_fields].median().to_dict()}')
# Median values for the sold dataset before filtering outliers: {'ClosePrice': 822000.0, 'LivingArea': 1645.0, 'DaysOnMarket': 19.0},
# median values for the sold dataset after filtering out outliers: {'ClosePrice': 785000.0, 'LivingArea': 1571.0, 'DaysOnMarket': 16.0}
listing_flagged.to_csv("output/listing.csv", index=False)
listing_clean.to_csv("output/listing_clean.csv", index=False)

sold_flagged.to_csv("output/sold.csv", index=False)
sold_clean.to_csv("output/sold_clean.csv", index=False)