# 🧺 Market Basket Analysis (FP-Growth)

This project performs Market Basket Analysis using the FP-Growth algorithm in Databricks, and visualizes the results using a Streamlit dashboard.

## 🔧 Technologies
- Apache Spark (Databricks)
- PySpark FP-Growth
- Streamlit
- Matplotlib / Seaborn / NetworkX

## 📂 Project Structure
- `databricks_notebook.ipynb`: Notebook for data loading, FP-Growth, CSV export, and visualizations
- `streamlit_app/app.py`: Interactive Streamlit dashboard
- `association_rules_sample.csv`, `frequent_itemsets_sample.csv`: Example outputs
- `requirements.txt`: Install required Python libraries

## ▶️ Run Streamlit App

```bash
cd streamlit_app
pip install -r ../requirements.txt
streamlit run app.py

## Do Visit App:marketbaksketanalysis-8gi2o8ogb9p9dwmadtc5le.streamlit.app
