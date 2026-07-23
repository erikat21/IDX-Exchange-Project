import pandas as pd
import geopandas as gpd

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
listing_df['YrMo'] = listing_df['CloseDate'].dt.to_period('M')

sold_df['CloseYear'] = sold_df['CloseDate'].dt.year
sold_df['CloseMonth'] = sold_df['CloseDate'].dt.month
sold_df['YrMo'] = sold_df['CloseDate'].dt.to_period('M')


# new column that measures amount of time from listing date to an accepted offer date
listing_df['ListingToContractDays'] = (listing_df['PurchaseContractDate'] - listing_df['ListingContractDate']).dt.days
sold_df['ListingToContractDays'] = (sold_df['PurchaseContractDate'] - sold_df['ListingContractDate']).dt.days

# new column that measures the escrow and closing period duration
listing_df['ContractToCloseDays'] = (listing_df['CloseDate'] - listing_df['PurchaseContractDate']).dt.days
sold_df['ContractToCloseDays'] = (sold_df['CloseDate'] - sold_df['PurchaseContractDate']).dt.days

# add school districts 
districts_df = gpd.read_file('data/DistrictAreas.geojson')
unified_districts = districts_df[districts_df['DistrictType'] == 'Unified']

# convert property latitude/longitude into geodataframe, helper function
def add_school_districts(df, lat_col="Latitude", lon_col="Longitude"):
    """Converts lat/lon to points and performs spatial join with unified districts."""
    # Convert Pandas DF to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326",
    )

    # Ensure CRS match
    districts = unified_districts.to_crs(gdf.crs)

    # Perform spatial join
    joined = gpd.sjoin(
        gdf, districts[["DistrictName", "geometry"]], how="left", predicate="within"
    )

    # Return standard DataFrame without spatial helper columns
    return pd.DataFrame(
        joined.drop(columns=["geometry", "index_right"], errors="ignore")
    )

listing_df = add_school_districts(listing_df)
sold_df = add_school_districts(sold_df)

print("Listings columns:", listing_df.columns.tolist())
print("Sold columns:", sold_df.columns.tolist())

# segment analysis 
def summarize_segment(df, group_cols):
    """Generates standard market summary statistics for given grouping columns."""
    summary = (
        df.groupby(group_cols)
        .agg(
            total_listings=("ListingKey", "count"),
            avg_list_price=("ListPrice", "mean"),
            median_list_price=("ListPrice", "median"),
            avg_close_price=("ClosePrice", "mean"),
            median_close_price=("ClosePrice", "median"),
            avg_dom=("DaysOnMarket", "mean"),
            unique_school_districts=("DistrictName", "nunique"),
        )
        .reset_index()
    )

    # Calculate an engineered metric on the aggregate level: Sale-to-List Ratio
    summary["close_to_list_ratio"] = (
        summary["avg_close_price"] / summary["avg_list_price"]
    )

    # Sort by volume to highlight top segments first
    return summary.sort_values(by="total_listings", ascending=False)

# 1. Property Type & SubType (Property Characteristics)
property_segment_listing = summarize_segment(listing_df, ["PropertyType", "PropertySubType"])
property_segment_sold = summarize_segment(sold_df, ["PropertyType", "PropertySubType"])
print(property_segment_listing)
print(property_segment_sold)

# 2. Geography / Location Analysis
location_segment_listing = summarize_segment(listing_df, ["CountyOrParish", "MLSAreaMajor"])
location_segment_sold = summarize_segment(sold_df, ["CountyOrParish", "MLSAreaMajor"])
print(location_segment_listing)
print(location_segment_sold)

# 3. Competitive Intelligence (List Offices & Buyer Offices)
# List Office Market Share
list_office_segment_listing = summarize_segment(listing_df, ["ListOfficeName"])
list_office_segment_sold = summarize_segment(sold_df, ["ListOfficeName"])

# Buyer Office Market Share
buyer_office_segment_listing = summarize_segment(listing_df, ["BuyerOfficeName"])
buyer_office_segment_sold = summarize_segment(sold_df, ["BuyerOfficeName"])

# Co-Broke / Cross-Office Relationships (List Office vs Buyer Office)
office_pairs_segment_listing = summarize_segment(listing_df, ["ListOfficeName", "BuyerOfficeName"])
office_pairs_segment_sold = summarize_segment(sold_df, ["ListOfficeName", "BuyerOfficeName"])

district_segment_listing = summarize_segment(listing_df, ["CountyOrParish", "DistrictName"])
district_segment_sold = summarize_segment(sold_df, ["CountyOrParish", "DistrictName"])

new_metrics = [
    "ListingKey",
    "PriceRatio",
    "PricePerSqFt",
    "DaysOnMarket",
    "YrMo",
    "ListingToContractDays",
    "ContractToCloseDays",
    "DistrictName",
]
print(sold_df[new_metrics].head(10).to_string(index=False))
print(listing_df[new_metrics].head(10).to_string(index=False))
