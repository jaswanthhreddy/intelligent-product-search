import os
os.environ["PANDAS_USE_PYARROW"] = "0"

import streamlit as st
import pandas as pd
from data_processing import load_data, preprocess_data
from recommendation import display_product_recommendation

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Intelligent Search", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def get_data():
    dataset_path = "flipkart_com-ecommerce_sample.csv"
    df = load_data(dataset_path)
    if df is not None:
        return preprocess_data(df)
    return None

df = get_data()

# =========================
# SIDEBAR (UNCHANGED)
# =========================
with st.sidebar:
    st.toggle("🌙 Dark Mode", value=True)

    st.subheader("🔐 Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")

    st.subheader("📝 Register")
    st.text_input("New Username")
    st.text_input("New Password")
    st.button("Register")

    st.subheader("🔎 Filters")

    if df is not None:
        min_price = int(df["discounted_price"].min())
        max_price = int(df["discounted_price"].max())

        selected_price = st.slider(
            "Max Price",
            min_value=min_price,
            max_value=max_price,
            value=max_price
        )

        categories = ["All"] + sorted(df["primary_category"].dropna().unique().tolist())
        selected_category = st.selectbox("Category", categories)

        brands = ["All"] + sorted(df["brand"].dropna().unique().tolist())
        selected_brand = st.selectbox("Brand", brands)
    else:
        selected_price = None
        selected_category = "All"
        selected_brand = "All"

# =========================
# HEADER UI (UNCHANGED)
# =========================
st.markdown(
    """
    <div style="padding:20px; border-radius:12px; 
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color:white; font-size:22px; font-weight:bold;">
    🛍️ Intelligent Product Search & Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("Find exactly what you want, faster.")

# =========================
# NAVIGATION (UNCHANGED)
# =========================
tab = st.radio("", ["🏠 Home", "💬 Chat"], horizontal=True)

# =========================
# HOME TAB (SEARCH UI)
# =========================
if tab == "🏠 Home":

    col1, col2, col3 = st.columns([4, 1, 2])

    with col1:
        query = st.text_input("Search products...")

    with col2:
        search_clicked = st.button("🔍 Search")

    with col3:
        sort_option = st.selectbox(
            "Sort by",
            ["Relevance", "Price: Low to High", "Price: High to Low", "Name A-Z"]
        )

    if df is None:
        st.error("Dataset failed to load.")

    elif search_clicked:

        results = df.copy()

        # 🔍 Search filter
        if query:
            results = results[
                results["product_name"]
                .astype(str)
                .str.lower()
                .str.contains(query.lower(), na=False)
            ]

        # 💰 Price filter
        if selected_price is not None:
            results = results[results["discounted_price"] <= selected_price]

        # 📦 Category filter
        if selected_category != "All":
            results = results[results["primary_category"] == selected_category]

        # 🏷 Brand filter
        if selected_brand != "All":
            results = results[results["brand"] == selected_brand]

        # =========================
        # SORTING LOGIC (UNCHANGED)
        # =========================
        if sort_option == "Price: Low to High":
            results = results.sort_values(by="discounted_price", ascending=True)

        elif sort_option == "Price: High to Low":
            results = results.sort_values(by="discounted_price", ascending=False)

        elif sort_option == "Name A-Z":
            results = results.sort_values(by="product_name", ascending=True)

        if results.empty:
            st.warning("No products found.")
        else:
            st.write(f"Showing {len(results)} products")

            for _, row in results.head(12).iterrows():
                st.markdown("---")

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
                    name = row.get("product_name", "Unknown Product")
                    price = row.get("discounted_price", 0)

                    try:
                        price = float(price)
                    except:
                        price = 0

                    st.subheader(name)
                    st.markdown(f"💰 ₹{price}")

                    # ⭐ FIXED RATING (EXACT VALUE)
                    rating = row.get("overall_rating", "")

                    if rating and str(rating).strip().lower() not in ["", "no rating available", "nan"]:
                        try:
                            rating = float(rating)
                            st.markdown(f"⭐ {rating} / 5")
                        except:
                            st.markdown("⭐ Not Rated")
                    else:
                        st.markdown("⭐ Not Rated")

                    st.markdown("[🛒 Buy Now](#)")

# =========================
# CHAT TAB (UNCHANGED)
# =========================
elif tab == "💬 Chat":
    if df is not None:
        display_product_recommendation(df)
    else:
        st.warning("Dataset not loaded.")