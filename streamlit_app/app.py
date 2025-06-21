import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Market Basket Analysis Dashboard", layout="wide")
st.title("🧺 Market Basket Analysis (FP-Growth) Dashboard")

# File Uploads
st.sidebar.header("Upload CSV Files")
freq_file = st.sidebar.file_uploader("Upload Frequent Itemsets CSV", type="csv")
assoc_file = st.sidebar.file_uploader("Upload Association Rules CSV", type="csv")

if freq_file:
    freq_df = pd.read_csv(freq_file)
    freq_df["items"] = freq_df["items"].apply(lambda x: x.split(","))
    st.subheader("📦 Frequent Itemsets")
    freq_threshold = st.slider("Minimum Frequency", 1, int(freq_df['freq'].max()), 5)
    st.dataframe(freq_df[freq_df['freq'] >= freq_threshold])

if assoc_file:
    rules_df = pd.read_csv(assoc_file)
    rules_df["antecedent"] = rules_df["antecedent"].apply(lambda x: x.split(","))
    rules_df["consequent"] = rules_df["consequent"].apply(lambda x: x.split(","))
    
    st.subheader("🔗 Association Rules")
    col1, col2 = st.columns(2)
    with col1:
        min_conf = st.slider("Minimum Confidence", 0.0, 1.0, 0.3)
    with col2:
        min_lift = st.slider("Minimum Lift", 0.0, 10.0, 1.0)

    filtered_rules = rules_df[(rules_df['confidence'] >= min_conf) & (rules_df['lift'] >= min_lift)]
    st.dataframe(filtered_rules)

    # Optional: Plot lift vs confidence
    st.subheader("📊 Rule Quality Scatter Plot")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_rules, x='confidence', y='lift', ax=ax)
    st.pyplot(fig)
