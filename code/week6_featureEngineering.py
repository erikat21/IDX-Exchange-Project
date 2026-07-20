import pandas as pd

# load in listing and sold datasets
listing_df = pd.read_csv("output/listing.csv")
sold_df = pd.read_csv("output/sold.csv")

# make dates into pandas datetime 
date_col = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate',
'ContractStatusChangeDate']
listing_df[date_col] = listing_df[date_col].apply(pd.to_datetime, errors = 'coerce')
sold_df[date_col] = sold_df[date_col].apply(pd.to_datetime, errors = 'coerce')
print(listing_df.dtypes)

# print(len(listing_df))
# print(len(sold_df))

# create new column to measure negotiation strength
listing_df['PriceRatio'] = listing_df['ClosePrice']/listing_df['OriginalListPrice']
sold_df['PriceRatio'] = sold_df['ClosePrice']/sold_df['OriginalListPrice']

# create new column to normalize prices across size
listing_df['PricePerSqFt'] = listing_df['ClosePrice']/listing_df['LivingArea']
sold_df['PricePerSqFt'] = sold_df['ClosePrice']/sold_df['LivingArea']

# Already have DaysOnMarket column

# seperate CloseDate into new CloseYear and CloseMonth
listing_df['CloseYear'] = listing_df['CloseDate'].dt.year
listing_df['CloseMonth'] = listing_df['CloseDate'].dt.month
sold_df['CloseYear'] = sold_df['CloseDate'].dt.year
sold_df['CloseMonth'] = sold_df['CloseDate'].dt.month

# new column that measures amount of time from listing date to an accepted offer date
listing_df['ListingToContractDays'] = listing_df['PurchaseContractDate'] - listing_df['ListingContractDate']
sold_df['ListingToContractDays'] = sold_df['PurchaseContractDate'] - sold_df['ListingContractDate']

# new column that measures the escrow and closing period duration
listing_df['ContractToCloseDays'] = listing_df['CloseDate'] - listing_df['PurchaseContractDate']
sold_df['ContractToCloseDays'] = sold_df['CloseDate'] - sold_df['PurchaseContractDate']
