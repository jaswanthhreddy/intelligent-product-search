import streamlit as st


def display_product_recommendation(refined_df):
    """
    Stable recommendation system with dropdown-based UI.
    """

    st.header("🛍️ Product Recommendation")

    if refined_df is None or refined_df.empty:
        st.warning("No data available.")
        return

    # =========================
    # PREPARE DROPDOWN VALUES
    # =========================
    categories = sorted(
        refined_df["primary_category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    brands = sorted(
        refined_df["brand"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    # =========================
    # INPUTS (DROPDOWN UI)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox("Product Category", categories)

    with col2:
        brand = st.selectbox("Product Brand", ["All"] + brands)

    max_price = st.slider(
        "Maximum Price",
        min_value=int(refined_df["discounted_price"].min()),
        max_value=int(refined_df["discounted_price"].max()),
        value=1000
    )

    # =========================
    # BUTTON
    # =========================
    if st.button("Get Recommendations"):

        results = refined_df.copy()

        # Category filter (exact match)
        results = results[
            results["primary_category"] == category
        ]

        # Brand filter
        if brand != "All":
            results = results[
                results["brand"] == brand
            ]

        # Price filter
        results = results[
            results["discounted_price"] <= max_price
        ]

        # =========================
        # OUTPUT
        # =========================
        if results.empty:
            st.warning("No matching products found.")
            return

        st.subheader("Recommended Products")

        for _, row in results.head(10).iterrows():

            col1, col2 = st.columns([1, 3])

            # IMAGE
            with col1:
                img = row.get("primary_image_link", "")
                if isinstance(img, str) and img.startswith("http"):
                    st.image(img, width=200)
                else:
                    st.image(
                        "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
                        use_container_width=True
                    )

            # DETAILS
            with col2:
                name = row.get("product_name", "No Name")
                price = row.get("discounted_price", 0)

                try:
                    price = float(price)
                except:
                    price = 0

                st.markdown(f"### {name}")
                st.write(f"💰 Price: ₹{round(price, 2)}")
                st.write(f"🏷️ Brand: {row.get('brand', 'Unknown')}")
                st.write(f"📂 Category: {row.get('primary_category', 'Unknown')}")
                st.write(f"👤 Gender: {row.get('gender', 'Unisex')}")

            st.markdown("---")