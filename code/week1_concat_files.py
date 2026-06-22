import pandas as pd

# Load, combine, filter Listing files
feb_listing = pd.read_csv('data/CRMLSListing202602.csv')
mar_listing = pd.read_csv('data/CRMLSListing202603.csv')
apr_listing = pd.read_csv('data/CRMLSListing202604.csv')
may_listing = pd.read_csv('data/CRMLSListing202605.csv')
# check each months row counts
print(f"Feb Rows: {len(feb_listing)}, Mar Rows: {len(mar_listing)}, Apr Rows: {len(apr_listing)}, May Rows: {len(may_listing)}")

listing = pd.concat([feb_listing, mar_listing, apr_listing, may_listing])
# check that the same amount of rows are in the combined dataset
print(f"Total listing rows for past 4 months: {len(listing)}")

filtered_listing = listing[listing['PropertyType'] == 'Residential']
# check amount of rows after filtering to make sure its filtered
print(f"Total listing rows for past 4 months after filtering for residential properties: {len(filtered_listing)}")

# save to output csv
filtered_listing.to_csv('output/listing.csv', index=False)

# Load, combine, filter Sold files
feb_sold = pd.read_csv('data/CRMLSSold202602.csv')
mar_sold = pd.read_csv('data/CRMLSSold202603.csv')
apr_sold = pd.read_csv('data/CRMLSSold202604.csv')
may_sold = pd.read_csv('data/CRMLSSold202605.csv')
# check each months row counts
print(f"Feb Rows: {len(feb_sold)}, Mar Rows: {len(mar_sold)}, Apr Rows: {len(apr_sold)}, May Rows: {len(may_sold)}")

sold = pd.concat([feb_sold, mar_sold, apr_sold, may_sold])
# check that the same amount of rows are in the combined dataset
print(f"Total sold rows for past 4 months: {len(sold)}")

filtered_sold = sold[sold['PropertyType'] == 'Residential']
# check amount of rows after filtering to make sure its filtered
print(f"Total sold rows for past 4 months after filtering for residential properties: {len(filtered_sold)}")

# save to output csv
filtered_sold.to_csv('output/sold.csv', index=False)