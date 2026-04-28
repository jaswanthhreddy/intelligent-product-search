# Intelligent Product Search & Recommendation System

An end-to-end data-driven product discovery system that replicates the core functionality of modern e-commerce platforms. This project enables efficient product search, advanced filtering, and rule-based recommendations using structured data processing techniques.

---

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://intelligent-search.streamlit.app/)

---

## System Architecture

<p align="center">
  <img src="assets/architecture.png" alt="System Architecture" width="900"/>
</p>

```
                ┌────────────────────┐
                │   User Interface   │
                │   (Streamlit UI)   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Query Handling   │
                │ (Search / Filters) │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Data Processing    │
                │ - Cleaning         │
                │ - Feature Extract  │
                │ - Category Parsing │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Recommendation     │
                │ Engine             │
                │ - Category match   │
                │ - Brand filter     │
                │ - Price filter     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Results Rendering  │
                │ (Cards + Images)   │
                └────────────────────┘
```

---

## Key Features

### Search Engine

* Keyword-based product search
* Case-insensitive matching
* Robust handling of missing values

### Filtering System

* Price range filtering using slider
* Category-based filtering
* Brand-based filtering
* Sidebar-driven user interaction

### Recommendation Engine

* Category-aware filtering
* Brand-based refinement
* Budget-constrained recommendations
* Top-N product suggestions

### Product Insights

* Product image display
* Name and pricing information
* Brand and category details
* Gender classification
* Exact rating values from dataset

### User Interface

* Dark mode support
* Responsive layout
* Clean product card design
* Sidebar navigation

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Techniques Used

* Feature engineering
* Text parsing (AST-based extraction)
* String matching and filtering
* Data cleaning pipelines

---

## Project Structure

```
intelligent-product-search/
│
├── app.py
├── data_processing.py
├── recommendation.py
├── requirements.txt
├── flipkart_com-ecommerce_sample.csv
├── assets/
│   └── architecture.png
└── README.md
```

---

## Installation

```bash
git clone https://github.com/jaswanthreddy/intelligent-product-search.git
cd intelligent-product-search

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

---

## Dataset Overview

The dataset includes:

* Product names
* Category hierarchy
* Pricing (retail and discounted)
* Brand information
* Product descriptions
* Image URLs
* Ratings

---

## Core Components

### Data Processing Module

* Extracts primary category
* Parses image URLs
* Handles missing values
* Derives additional features (e.g., gender classification)

### Search Engine

* Implements string-based filtering
* Ensures safe handling of null values

### Recommendation Engine

* Multi-criteria filtering based on:

  * Category
  * Brand
  * Price constraints

---

## Use Cases

* E-commerce product search systems
* Recommendation engine prototypes
* Data science portfolio projects
* Applied machine learning pipelines

---

## Future Improvements

* Semantic search using transformer-based models
* Machine learning-based recommendation system 
* Personalized recommendations
* Database integration (SQL/NoSQL)
* Scalable cloud deployment

---

## Author

Jaswanth Reddy Bandi

---

## License

This project is intended for educational and demonstration purposes.
