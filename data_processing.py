import pandas as pd
import streamlit as st
from ast import literal_eval

# Optional plotting (safe import)
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    PLOT_AVAILABLE = True
except Exception:
    PLOT_AVAILABLE = False


# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(dataset_path):
    try:
        df = pd.read_csv(dataset_path, low_memory=False)
        return df
    except pd.errors.EmptyDataError:
        st.error("Dataset file is empty.")
    except pd.errors.ParserError:
        st.error("Error parsing dataset.")
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
    return None


# =========================
# HELPERS
# =========================
def extract_primary_category(product_category_tree):
    try:
        data = literal_eval(str(product_category_tree))
        if isinstance(data, list) and len(data) > 0:
            return data[0].split(">>")[0].strip()
    except Exception:
        pass
    return None


def extract_primary_image(image_str):
    try:
        data = literal_eval(str(image_str))
        if isinstance(data, list) and len(data) > 0:
            return data[0]
    except Exception:
        pass
    return ""


def determine_gender(product_name, description):
    text = f"{str(product_name).lower()} {str(description).lower()}"

    if any(k in text for k in ['women','woman','female','girls','ladies']):
        return "Women"
    elif any(k in text for k in ['men','man','male','boys','gentlemen']):
        return "Men"
    return "Unisex"


# =========================
# PREPROCESS
# =========================
def preprocess_data(df):
    if df is None:
        return None

    df = df.copy()

    # Safe column handling
    required_cols = [
        'product_category_tree',
        'image',
        'product_name',
        'description',
        'retail_price',
        'discounted_price'
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # Feature extraction
    df['primary_category'] = df['product_category_tree'].apply(extract_primary_category)
    df['primary_image_link'] = df['image'].apply(extract_primary_image)
    df['gender'] = df.apply(
        lambda x: determine_gender(x['product_name'], x['description']), axis=1
    )

    # Select columns safely
    columns = [
        'pid', 'product_url', 'product_name', 'primary_category',
        'retail_price', 'discounted_price', 'primary_image_link',
        'description', 'brand', 'gender'
    ]

    for col in columns:
        if col not in df.columns:
            df[col] = None

    refined_df = df[columns]

    # Clean numeric
    refined_df['retail_price'] = pd.to_numeric(refined_df['retail_price'], errors='coerce')
    refined_df['discounted_price'] = pd.to_numeric(refined_df['discounted_price'], errors='coerce')

    refined_df = refined_df.dropna(
        subset=['primary_category', 'retail_price', 'discounted_price']
    )

    return refined_df


# =========================
# ANALYSIS (SAFE VERSION)
# =========================
def display_data_analysis(refined_df):

    if refined_df is None or refined_df.empty:
        st.warning("No data available for analysis.")
        return

    st.header("📊 Data Analysis")

    if not PLOT_AVAILABLE:
        st.warning("Seaborn/Matplotlib not available. Skipping charts.")
        return

    try:
        top_categories = refined_df['primary_category'].value_counts().nlargest(10).index
        df_top = refined_df[refined_df['primary_category'].isin(top_categories)]

        # BOXPLOT
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='retail_price', y='primary_category', data=df_top, ax=ax)
        ax.set_title('Price Distribution')
        st.pyplot(fig)

        # DISCOUNT HISTOGRAM
        refined_df['discount_percentage'] = (
            (refined_df['retail_price'] - refined_df['discounted_price'])
            / refined_df['retail_price']
        ) * 100

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(refined_df['discount_percentage'].dropna(), bins=30, ax=ax)
        ax.set_title('Discount Distribution')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error generating charts: {e}")