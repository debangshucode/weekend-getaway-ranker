import pandas as pd

df = pd.read_csv("data/travel_places.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


def rank_destinations(source_city, top_n=5):
    city_df = df.loc[df["city"].str.lower() == source_city.lower()].copy()


    if city_df.empty:
        raise ValueError(f"No destinations found for city: {source_city}")

    # Normalize values
    city_df["rating_norm"] = (
        city_df["google_review_rating"]
        / city_df["google_review_rating"].max()
    )

    city_df["popularity_norm"] = (
        city_df["number_of_google_review_in_lakhs"]
        / city_df["number_of_google_review_in_lakhs"].max()
    )

    city_df["time_norm"] = 1 - (
        city_df["time_needed_to_visit_in_hrs"]
        / city_df["time_needed_to_visit_in_hrs"].max()
    )

    city_df["fee_norm"] = 1 - (
        city_df["entrance_fee_in_inr"]
        / city_df["entrance_fee_in_inr"].max()
    )

    city_df["final_score"] = (
        0.4 * city_df["rating_norm"]
        + 0.3 * city_df["popularity_norm"]
        + 0.2 * city_df["time_norm"]
        + 0.1 * city_df["fee_norm"]
    )

    return city_df.sort_values("final_score", ascending=False).head(top_n)

if __name__ == "__main__":
    # ---- Sample Output for Submission ----
    sample_cities = ["Kolkata", "Delhi", "Mumbai"]

    display_cols = [
        "name",
        "google_review_rating",
        "number_of_google_review_in_lakhs",
        "time_needed_to_visit_in_hrs",
        "entrance_fee_in_inr",
        "final_score",
    ]

    for city in sample_cities:
        print("\n" + "=" * 70)
        print(f"Top weekend getaways from {city}")
        print("=" * 70)

        try:
            result = rank_destinations(city)
            print(result[display_cols].round(2).to_string(index=False))
        except ValueError as e:
            print(e)

    # ---- Interactive Mode ----
    while True:
        print("\n" + "-" * 70)
        user_city = input(
            "Enter a city name to get weekend getaways "
            "(or type 'exit' to quit): "
        ).strip()

        if user_city.lower() in ["exit", "quit", "close"]:
            print("Exiting Weekend Getaway Ranker. Goodbye 👋")
            break

        try:
            result = rank_destinations(user_city)
            print("\n" + "=" * 70)
            print(f"Top weekend getaways from {user_city}")
            print("=" * 70)
            print(result[display_cols].round(2).to_string(index=False))
        except ValueError as e:
            print(e)
