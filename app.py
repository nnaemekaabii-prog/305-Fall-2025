import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Poverty & Millionaire Dashboard", layout="wide")
st.title("Poverty & Millionaire Analytics Dashboard")

# Upload Excel File
file = st.file_uploader("Upload povertymillionaires.xlsx", type=["xlsx"])
if file is None:
    st.stop()

# Load and clean
df = pd.read_excel(file)
df = df.rename(columns={
    "State": "state",
    "Number in Poverty": "poverty",
    "Number of Millionaires": "millionaires",
    "State Popiulation": "population"
})

# Calculated fields
df["millionaire_density"] = df["millionaires"] / df["population"]
df["poverty_rate"] = df["poverty"] / df["population"]

# State abbreviations
state_abbrev = {
    "AL": "AL", "AK": "AK", "AZ": "AZ", "AR": "AR", "CA": "CA",
    "CO": "CO", "CT": "CT", "DE": "DE", "FL": "FL", "GA": "GA",
    "HI": "HI", "IA": "IA", "ID": "ID", "IL": "IL", "IN": "IN",
    "KS": "KS", "KY": "KY", "LA": "LA", "MA": "MA", "MD": "MD",
    "ME": "ME", "MI": "MI", "MN": "MN", "MO": "MO", "MS": "MS",
    "MT": "MT", "NC": "NC", "ND": "ND", "NE": "NE", "NH": "NH",
    "NJ": "NJ", "NM": "NM", "NV": "NV", "NY": "NY", "OH": "OH",
    "OK": "OK", "OR": "OR", "PA": "PA", "RI": "RI", "SC": "SC",
    "SD": "SD", "TN": "TN", "TX": "TX", "UT": "UT", "VA": "VA",
    "VT": "VT", "WA": "WA", "WI": "WI", "WV": "WV", "WY": "WY"
}
df["abbr"] = df["state"].map(state_abbrev)

# Tabs
tab1, tab2, tab3 = st.tabs([
    "Poverty vs Millionaires",
    "Millionaire Density Map",
    "Poverty Rate"
])

# ---------------- Q1 ----------------
with tab1:
    st.subheader("Poverty vs Millionaires (Selected States)")

    states = st.multiselect(
        "Select States",
        df["state"].unique(),
        df["state"].unique()[:5]
    )
    
    data = df[df["state"].isin(states)]

    x = np.arange(len(data))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x - width/2, data["poverty"], width, label="Poverty")
    ax.bar(x + width/2, data["millionaires"], width, label="Millionaires")
    ax.set_xticks(x)
    ax.set_xticklabels(data["state"])
    ax.set_title("Poverty vs Millionaires")
    ax.legend()
    st.pyplot(fig)

    st.write("**Interpretation:** Most states have far more people in poverty than millionaires, showing large wealth gaps.")

# ---------------- Q2 ----------------
with tab2:
    st.subheader("Millionaire Density Map")

    fig = px.choropleth(
        df,
        locations="abbr",
        locationmode="USA-states",
        color="millionaire_density",
        hover_data=["state", "population", "millionaires", "millionaire_density"],
        color_continuous_scale="Blues",
        scope="usa"
    )
    fig.update_layout(title="Millionaire Density by State")
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        "**Interpretation:** Millionaire density is highest in coastal and Northeastern states, "
        "while Southern and Midwestern states show generally lower concentrations."
    )

# ---------------- Q3 ----------------
with tab3:
    st.subheader("Poverty Rate by State")

    sorted_df = df.sort_values("poverty_rate", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(7, 12))
    ax2.barh(sorted_df["state"], sorted_df["poverty_rate"] * 100)
    ax2.set_title("Poverty Rate (%) by State")
    ax2.invert_yaxis()
    st.pyplot(fig2)

    st.write(
        "**Interpretation:** Some states carry a much heavier poverty burden than others, "
        "indicating differences in regional economic well-being."
    )
