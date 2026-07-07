import pandas as pd
from week2_eda import missing_val_analysis

listing_df = pd.read_csv("output/listing.csv")
sold_df = pd.read_csv("output/sold.csv")

# make dates into pandas datetime 
date_col = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate',
'ContractStatusChangeDate']
listing_df[date_col] = listing_df[date_col].apply(pd.to_datetime, errors = 'coerce')
sold_df[date_col] = sold_df[date_col].apply(pd.to_datetime, errors = 'coerce')

# print(missing_val_analysis(listing_df, 'Listings Dataset', 50).index.drop(['CloseDate', 'ClosePrice', 'BuyerOfficeName', 'BuyerAgentMlsId']))
# print(missing_val_analysis(sold_df, 'Sold Dataset', 50).index)

remove_listing_col = missing_val_analysis(listing_df, 'Listings Dataset', 50).index.drop(['CloseDate', 'ClosePrice', 'BuyerOfficeName', 'BuyerAgentMlsId', 'PurchaseContractDate'])
remove_sold_col = missing_val_analysis(sold_df, 'Sold Dataset', 50).index

# dropped unnecessary columns and columns with more than 50% null values except for some key columns 
sold_df = sold_df.drop(columns=remove_sold_col)
sold_df = sold_df.drop(columns=['ListAgentFullName', 'HighSchoolDistrict', 'ListAgentEmail'])
listing_df = listing_df.drop(columns=remove_listing_col)
listing_df = listing_df.drop(columns=['ListAgentFullName', 'HighSchoolDistrict', 'ListAgentEmail'])

print(sold_df.columns[sold_df.isnull().any()])
print(sold_df.columns[sold_df.isnull().sum() == 0])
print(listing_df.columns[listing_df.isnull().any()])
print(listing_df.columns[listing_df.isnull().sum() == 0])
# imputting values can skew analysis so leaving null values as is, consider dropping them during analysis so for now I'll keep it

print(sold_df.info())
print(listing_df.info())
# data types seem to be correct, Levels could be changed to numeric for analysis but for tableau filtering object is better and we have stories which is numeric

validation_rules = {
    'ClosePrice': lambda x: x <= 0,
    'ListPrice': lambda x: x <= 0,
    'OriginalListPrice': lambda x: x <= 0,
    'LivingArea': lambda x: x <= 0,
    #'LotSizeAcres': lambda x: x <= 0,
    #'LotSizeSquareFeet': lambda x: x <= 0,
    'DaysOnMarket': lambda x: x < 0,
    'BedroomsTotal': lambda x: x < 0,
    'BathroomsTotalInteger': lambda x: x < 0,
    'MainLevelBedrooms': lambda x: x < 0,
    'ParkingTotal': lambda x: x < 0,
    'GarageSpaces': lambda x: x < 0,
    'AssociationFee': lambda x: x < 0,
    'YearBuilt': lambda x: (x > 2026) | (x < 1800),
    'Latitude': lambda x: (x > 90) | (x < -90),
    'Longitude': lambda x: (x > 180) | (x < -180),
    'Stories': lambda x: x <= 0,
    #'LotSizeArea': lambda x: x <= 0
}

# Checking Sold dataset invalid rows
invalid_summary = {}
for col, rule in validation_rules.items():
    if col in sold_df.columns:
        invalid_summary[col] = rule(sold_df[col]).sum()
print(invalid_summary)
# drop rows with invalid information except for lotsize columns

cutoff_date = pd.Timestamp('2026-05-31')
future_closes = sold_df[sold_df['CloseDate'] > cutoff_date]
print(len(future_closes))
# no close dates in the future

invalid_mask = pd.Series(False, index=sold_df.index)
for col, rule in validation_rules.items():
    if col in sold_df.columns:
        invalid_mask |= rule(sold_df[col])
# drop invalid rows and check row counts
print(len(sold_df))
sold_df = sold_df.loc[~invalid_mask].copy()
print(len(sold_df))

# Checking Listings dataset invalid rows 
invalid_summary = {}
for col, rule in validation_rules.items():
    if col in listing_df.columns:
        invalid_summary[col] = rule(listing_df[col]).sum()
print(invalid_summary)
# drop rows with invalid information except for lotsize columns

cutoff_date = pd.Timestamp('2026-05-31')
future_closes = listing_df[listing_df['CloseDate'] > cutoff_date]
print(len(future_closes))
# 726 close dates in the future

invalid_mask = pd.Series(False, index = listing_df.index)
for col, rule in validation_rules.items():
    if col in listing_df.columns:
        invalid_mask |= rule(listing_df[col])
# drop invalid rows and check row counts
print(len(listing_df))
listing_df = listing_df.loc[~invalid_mask].copy()
print(len(listing_df))

# Check date consistency 
sold_df['listing_after_close_flag'] = sold_df['CloseDate'] < sold_df['ListingContractDate']
print(f"Sold dataset has {sold_df['listing_after_close_flag'].sum()} rows with listing dates after the close date")
sold_df['purchase_after_close_flag'] = sold_df['CloseDate'] < sold_df['PurchaseContractDate']
print(f"Sold dataset has {sold_df['purchase_after_close_flag'].sum()} rows with purchase dates after the close date")
sold_df['negative_timeline_flag'] = sold_df['PurchaseContractDate'] < sold_df['ListingContractDate']
print(f"Sold dataset has {sold_df['listing_after_close_flag'].sum()} rows with listing dates after the purchase date")

listing_df['listing_after_close_flag'] = listing_df['CloseDate'] < listing_df['ListingContractDate']
print(f"Listings dataset has {listing_df['listing_after_close_flag'].sum()} rows with listing dates after the close date")
listing_df['purchase_after_close_flag'] = listing_df['CloseDate'] < listing_df['PurchaseContractDate']
print(f"Listings dataset has {listing_df['purchase_after_close_flag'].sum()} rows with purchase dates after the close date")
listing_df['negative_timeline_flag'] = listing_df['PurchaseContractDate'] < listing_df['ListingContractDate']
print(f"Listing dataset has {listing_df['listing_after_close_flag'].sum()} rows with listing dates after the purchase date")

# Check longitude/latitude consistency
 