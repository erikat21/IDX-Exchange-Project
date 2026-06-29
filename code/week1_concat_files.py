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

