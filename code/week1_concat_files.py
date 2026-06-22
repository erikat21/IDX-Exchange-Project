import pandas as pd
import glob

# Load, combine, and filter Listing files
all_listing_files = sorted(glob.glob("data/CRMLSListing*.csv"))

listing_chunks = []
total_row_count_before_concat = 0

for file in all_listing_files:
    df = pd.read_csv(file)
    
    # If '_filled' is in the filename, keep all rows but drop the last 2 columns
    if "_filled" in file: df = df.iloc[:, :-2]
    
    total_row_count_before_concat += len(df)

    listing_chunks.append(df)

combined_listings = pd.concat(listing_chunks, ignore_index=True)
total_row_count_after_concat = len(combined_listings)
print(f"Row count before concatenation: {total_row_count_before_concat}, Row count after concatenation: {total_row_count_after_concat}")

filtered_listings = combined_listings[combined_listings['PropertyType'] == 'Residential']

print(f"Row count after filtering: {len(filtered_listings)}")

filtered_listings.to_csv('output/listing.csv', index=False)


# Load, combine, filter Sold files
all_sold_files = sorted(glob.glob("data/CRMLSSold*.csv"))

sold_chunks = []
total_row_count_before_concat = 0

for file in all_sold_files:
    df = pd.read_csv(file)
    
    # If '_filled' is in the filename, keep all rows but drop the last 2 columns
    if "_filled" in file: df = df.iloc[:, :-2]
    
    total_row_count_before_concat += len(df)

    sold_chunks.append(df)

combined_sold = pd.concat(sold_chunks, ignore_index=True)
total_row_count_after_concat = len(combined_sold)
print(f"Row count before concatenation: {total_row_count_before_concat}, Row count after concatenation: {total_row_count_after_concat}")

filtered_sold = combined_sold[combined_sold['PropertyType'] == 'Residential']

print(f"Row count after filtering: {len(filtered_sold)}")

filtered_sold.to_csv('output/sold.csv', index=False)

# # Load, combine, filter Listing files
# feb_listing = pd.read_csv('data/CRMLSListing202602.csv')
# mar_listing = pd.read_csv('data/CRMLSListing202603.csv')
# apr_listing = pd.read_csv('data/CRMLSListing202604.csv')
# may_listing = pd.read_csv('data/CRMLSListing202605.csv')
# # check each months row counts
# print(f"Feb Rows: {len(feb_listing)}, Mar Rows: {len(mar_listing)}, Apr Rows: {len(apr_listing)}, May Rows: {len(may_listing)}")

# listing = pd.concat([feb_listing, mar_listing, apr_listing, may_listing])
# # check that the same amount of rows are in the combined dataset
# print(f"Total listing rows for past 4 months: {len(listing)}")

# filtered_listing = listing[listing['PropertyType'] == 'Residential']
# # check amount of rows after filtering to make sure its filtered
# print(f"Total listing rows for past 4 months after filtering for residential properties: {len(filtered_listing)}")

# # save to output csv
# filtered_listing.to_csv('output/listing.csv', index=False)

# # Load, combine, filter Sold files
# feb_sold = pd.read_csv('data/CRMLSSold202602.csv')
# mar_sold = pd.read_csv('data/CRMLSSold202603.csv')
# apr_sold = pd.read_csv('data/CRMLSSold202604.csv')
# may_sold = pd.read_csv('data/CRMLSSold202605.csv')
# # check each months row counts
# print(f"Feb Rows: {len(feb_sold)}, Mar Rows: {len(mar_sold)}, Apr Rows: {len(apr_sold)}, May Rows: {len(may_sold)}")

# sold = pd.concat([feb_sold, mar_sold, apr_sold, may_sold])
# # check that the same amount of rows are in the combined dataset
# print(f"Total sold rows for past 4 months: {len(sold)}")

# filtered_sold = sold[sold['PropertyType'] == 'Residential']
# # check amount of rows after filtering to make sure its filtered
# print(f"Total sold rows for past 4 months after filtering for residential properties: {len(filtered_sold)}")

# # save to output csv
# filtered_sold.to_csv('output/sold.csv', index=False)