import pandas as pd
import matplotlib.pyplot as plt

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
    print(f"{name} has {len(high_missing)} columns that are more than {percent}% null. The columns are: \n{high_missing.round(2)}")
    return high_missing

high_missing_listings = missing_val_analysis(listing_df, 'Listings Dataset', 90)
high_missing_sold = missing_val_analysis(sold_df, "Sold Dataset", 90)
# consider dropping columns with more than 50% missing values unless they are core fields or seem like they could be important

key_fields = ['ClosePrice', "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres", "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]
for col in key_fields:
    plt.hist(sold_df[col].dropna(), bins = 50, color='steelblue')
    plt.title(f"Sold dataset {col} Histogram")
    plt.show()

    plt.boxplot(sold_df[col].dropna())
    plt.title(f"Sold dataset {col} Boxplot")
    plt.show()

    plt.hist(listing_df[col].dropna(), bins = 50, color='steelblue')
    plt.title(f"Listings dataset {col} Histogram")
    plt.show()

    plt.boxplot(listing_df[col].dropna())
    plt.title(f"Listings dataset {col} Boxplot")
    plt.show()

custom_percentiles = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
print(f" Sold dataset key fields percentile summary {sold_df[key_fields].describe(percentiles=custom_percentiles).T.round(2)}")
print(f" Listings dataset key fields percentile summary {listing_df[key_fields].describe(percentiles=custom_percentiles).T.round(2)}")
# need to drop rows with impossible values such as 0's and negatives, the houses cant be on market for 
# negative days and the houses cant have 0 bedrooms etc, the 0 dollar close price could be from houses that 
# havent sold yet so instead of NA its 0, might not need to drop those rows

target_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
listing_distribution_summary = listing_df[target_fields].describe().T
listing_distribution_summary.rename(columns={'50%': 'median'}, inplace= True)
print(f"Listings dataset distribution summary: \n{listing_distribution_summary.round(2)}")
print(f"The average closed price is {listing_distribution_summary.round(2)['mean'][0]} and the median closed price is {listing_distribution_summary.round(2)['median'][0]}")

sold_distribution_summary = sold_df[target_fields].describe().T
sold_distribution_summary.rename(columns={'50%': 'median'}, inplace= True)
print(f"Sold dataset distribution summary: \n{sold_distribution_summary.round(2)}")
print(f"The average closed price is {sold_distribution_summary.round(2)['mean'][0]} and the median closed price is {sold_distribution_summary.round(2)['median'][0]}")
# extreme outliers are most likely not wrong but could be from mansions or expensive areas so, 
# we can keep them for now and maybe remove from analysis later so its not skewed since those properties are more rare,
# the extremely low outliers are most likely wrong though since houses cannot be sold for 0 dollars so those will need to be filtered out


missing_val_analysis(listing_df, 'Listings Dataset', 50)
missing_val_analysis(sold_df, "Sold Dataset", 50)
# can drop all of these columns I think, lots of null and they are not key to analysis most likely

print(f"{round(sum(sold_df['ClosePrice'] > sold_df['ListPrice'])/len(sold_df)*100, 3)}% of houses closed at a higher price than they were listed at.")

print(f"The counties with the highest median close price are: \n{sold_df.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False).head(10)}")
