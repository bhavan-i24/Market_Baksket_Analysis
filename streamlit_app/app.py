import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

st.set_page_config(page_title="Market Basket Analysis", layout="wide")
st.title("🧺 Market Basket Analysis Dashboard")

# Sidebar for file uploads
st.sidebar.header("📂 Upload CSV Files")
itemsets_file = st.sidebar.file_uploader("Upload Frequent Itemsets CSV", type="csv")
rules_file = st.sidebar.file_uploader("Upload Association Rules CSV", type="csv")

# Load dataframes
if itemsets_file and rules_file:
    itemsets_df = pd.read_csv(itemsets_file)
    rules_df = pd.read_csv(rules_file)

    # Convert array-like strings to real lists
    itemsets_df["items"] = itemsets_df["items"].apply(lambda x: x.split(","))
    rules_df["antecedent"] = rules_df["antecedent"].apply(lambda x: x.split(","))
    rules_df["consequent"] = rules_df["consequent"].apply(lambda x: x.split(","))

    # Section: Search box
    st.subheader("🔍 Product Search")
    search_product = st.text_input("Enter a product name (e.g., milk, bread):").strip().lower()

    if search_product:
        # 1. Frequency of the item in itemsets
        count = itemsets_df[itemsets_df["items"].apply(
            lambda items: search_product in [i.strip().lower() for i in items]
        )]["freq"].sum()
        st.write(f"🔢 **'{search_product}' appeared in {int(count)} orders**")

        # 2. Find matching association rules
        matching_rules = rules_df[rules_df["antecedent"].apply(
            lambda items: search_product in [i.strip().lower() for i in items]
        )]

        if not matching_rules.empty:
            st.write("📦 **Frequently bought together with it:**")
            st.dataframe(matching_rules[["consequent", "confidence", "lift"]])
        else:
            st.warning("No strong association rules found for this product.")

    # Section: Show full itemsets
    st.subheader("📦 Frequent Itemsets")
    min_freq = st.slider("Minimum Frequency", 1, int(itemsets_df["freq"].max()), 5)
    st.dataframe(itemsets_df[itemsets_df["freq"] >= min_freq])

    # Section: Association Rules
    st.subheader("🔗 Association Rules")
    col1, col2 = st.columns(2)
    with col1:
        min_conf = st.slider("Minimum Confidence", 0.0, 1.0, 0.3)
    with col2:
        min_lift = st.slider("Minimum Lift", 0.0, 10.0, 1.0)

    filtered_rules = rules_df[(rules_df["confidence"] >= min_conf) & (rules_df["lift"] >= min_lift)]
    st.dataframe(filtered_rules)

    # Scatter Plot: Confidence vs Lift
    st.subheader("📈 Confidence vs Lift")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_rules, x="confidence", y="lift", ax=ax)
    st.pyplot(fig)

    # Network Graph: Top 10 rules
    st.subheader("🕸️ Association Rule Graph (Top 10 Rules)")
    G = nx.DiGraph()
    for _, row in filtered_rules.head(10).iterrows():
        antecedent = ','.join(row['antecedent'])
        consequent = ','.join(row['consequent'])
        G.add_edge(antecedent, consequent, weight=row['confidence'])

    fig2 = plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, edge_color="gray", arrows=True)
    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(fig2)

else:
    st.info("⬅️ Please upload both `frequent_itemsets.csv` and `association_rules.csv` to begin.")
