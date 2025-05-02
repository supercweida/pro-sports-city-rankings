import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("league_rankings/nfl_rankings.csv")
df["Region"] = df["Region"].replace({"Tampa": "Tampa Bay"})

# Map region to state
region_states = {
    "Boston": "MA",
    "Kansas City": "MO",
    "Pittsburgh": "PA",
    "Oakland/San Francisco": "CA",
    "Green Bay": "WI",
    "Baltimore": "MD",
    "Dallas": "TX",
    "Miami": "FL",
    "Indianapolis": "IN",
    "Denver": "CO",
    "New York": "NY",
    "Philadelphia": "PA",
    "Los Angeles": "CA",
    "New Orleans": "LA",
    "Chicago": "IL",
    "Seattle": "WA",
    "Tampa Bay": "FL",
    "Washington DC": "DC",
    "Cincinnati": "OH",
    "Minneapolis": "MN",
    "Charlotte": "NC",
    "Atlanta": "GA",
    "Phoenix": "AZ",
    "Detroit": "MI",
    "Buffalo": "NY",
    "Cleveland": "OH",
    "Houston": "TX",
    "Jacksonville": "FL",
    "Las Vegas": "NV",
    "Nashville": "TN",
    "San Diego": "CA",
    "St. Louis": "MO",
    "Newark": "NJ"
}

df["State"] = df["Region"].replace(region_states)

# Choropleth map
fig = px.choropleth(
    df,
    locations="State",
    locationmode="USA-states",
    color="Total Score",
    hover_name="Region",
    hover_data=["Total Score", "Averaged Score"],
    color_continuous_scale="Viridis",
    scope="usa",
    title="🏈 NFL Regional Rankings by U.S. State"
)

fig.update_layout(
    geo=dict(showlakes=True, lakecolor="lightblue"),
    title_font_size=24,
    margin={"r":0,"t":40,"l":0,"b":0}
)

# Streamlit UI
st.title("NFL Rankings Choropleth Map")
st.plotly_chart(fig, use_container_width=True)
