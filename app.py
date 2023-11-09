import argparse
from fuzzywuzzy import fuzz
import pandas as pd


# Function to read CSV from Google Drive URL
def read_csv_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    return pd.read_csv(url)

# The similarity is calculated by fuzz ratio
def calculate_similarity(query, text):
    return fuzz.ratio(query.lower(), text.lower())


# Search tool logic
def search_tool(query, n, merged_df):
    results = []

    for index, row in merged_df.iterrows():
        # Offer similarity just calcualted as a place holder
        offer_similarity = calculate_similarity(query, row["OFFER"])
        category_similarity = calculate_similarity(query, row["PRODUCT_CATEGORY"])
        brand_similarity = calculate_similarity(query, row["BRAND"])
        retailer_similarity = calculate_similarity(query, row["RETAILER"])

        # The similary will be calculated based on the category, brand and retailer
        max_similarity = max(category_similarity, brand_similarity, retailer_similarity)

        results.append(
            {
                "Offer": row["OFFER"],
                "Retailer": row["RETAILER"],
                "Category": row["PRODUCT_CATEGORY"],
                "Brand": row["BRAND"],
                "Search Score": max_similarity
            }
        )

    # Sort results by max similarity
    results = sorted(results, key=lambda x: x["Search Score"], reverse=True)

    for result in results[:n]:
        print(f"Search Score: {result['Search Score']}")
        print(f"Offer: {result['Offer']}")
        print(f"Retailer: {result['Retailer']}")
        print(f"Category: {result['Category']}")
        print(f"Brand: {result['Brand']}")
        print("\n---\n")


def main():
    parser = argparse.ArgumentParser(description="Search tool CLI")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("top_n", type=int, help="Shwoing top N results")

    args = parser.parse_args()

    # Load the data
    # Google Drive file IDs for CSVs
    categories_file_id = "1SR6oGRnB4ULk9umnxZztHYKiHDI-VSag"
    offers_file_id = "18krLxNoBx9wFgtkXZiyL9Oh8B6w1hN40"
    brands_file_id = "1hPCAp4xx4PaDG_OLTJhYlhICc4WdgbDy"

    # Read CSVs from Google Drive URLs
    categories_df = read_csv_from_drive(categories_file_id)
    offers_df = read_csv_from_drive(offers_file_id)
    brands_df = read_csv_from_drive(brands_file_id)

    # Merge datasets
    merged_df = pd.merge(
        offers_df, brands_df, how="left", left_on="BRAND", right_on="BRAND"
    )
    merged_df = pd.merge(
        merged_df,
        categories_df,
        how="left",
        left_on="BRAND_BELONGS_TO_CATEGORY",
        right_on="PRODUCT_CATEGORY",
    )
    merged_df.drop(labels=["RECEIPTS", "CATEGORY_ID"], axis=1, inplace=True)
    merged_df.fillna(value="None", inplace=True)

    # Run the search tool
    search_tool(args.query, args.top_n, merged_df)


if __name__ == "__main__":
    main()
