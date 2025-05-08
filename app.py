import plotly.graph_objects as go
import pandas as pd

df1 = pd.read_csv("league_rankings/nfl_rankings.csv")

# Create plotly tables
fig = go.Figure()

# Add tables for each DataFrame
fig.add_trace(go.Table(
    header=dict(values=list(df1.columns)),
    cells=dict(values=[df1[col] for col in df1.columns])
))

# Update layout to make sure tables are visible
fig.update_layout(
    title="NFL Rankings (Since 1980)",
    height=800,
    showlegend=False
)

# Show the plot
fig.show()
