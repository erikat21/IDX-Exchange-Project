import pandas as pd

listing_df = pd.read_csv("output/listing.csv")
sold_df = pd.read_csv("output/sold.csv")

# check number of rows and columns for the listings and sold datasets
print(f"The listings dataset has {listing_df.shape[0]} rows, and {listing_df.shape[1]} columns.")
print(f"The sold dataset has {sold_df.shape[0]} rows, and {sold_df.shape[1]} columns.")

# making sure the property type filtering worked properly
print(f"Unique property types in the listings dataset: {listing_df['PropertyType'].unique()}")
print(f"Unique property types in the sold dataset: {sold_df['PropertyType'].unique()}")

def missing_val_analysis(df, name, percent):
    null_counts = df.isnull().sum()
    null_percent = (null_counts/len(df)) * 100
    null_report = pd.DataFrame({
        'Null Count' : null_counts,
        'Null Percentage' : null_percent
    })
    print(f"{name} null report: \n{null_report}")
    high_missing = null_report[null_report['Null Percentage'] > percent]
    print(f"{name} has {len(high_missing)} columns that are more than 90% null. The columns are: \n{high_missing.round(2)}")
    return high_missing

high_missing_listings = missing_val_analysis(listing_df, 'Listings Dataset', 90)
high_missing_sold = missing_val_analysis(sold_df, "Sold Dataset", 90)
# consider dropping columns with more than 50% missing values unless they are core fields or seem like they could be important

key_fields = ['ClosePrice', "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres", "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]


target_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
listing_distribution_summary = listing_df[target_fields].describe().T
listing_distribution_summary.rename(columns={'50%': 'median'}, inplace= True)
print(f"Listings dataset distribution summary: \n{listing_distribution_summary.round(2)}")
sold_distribution_summary = sold_df[target_fields].describe().T
sold_distribution_summary.rename(columns={'50%': 'median'}, inplace= True)
print(f"Sold dataset distribution summary: \n{sold_distribution_summary.round(2)}")

