import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Title
st.title("Major Sports League Rankings")

# Sidebar dropdown to select plot
plot_choice = st.selectbox(
    "Choose a League:",
    ["NFL", "MLB", "NBA", "NHL", "MLS"]
)

league_df = pd.read_csv(f'league_rankings/{plot_choice.lower()}_rankings.csv')

# Add sorting functionality
sort_column = st.selectbox(
    "Sort the table by:",
    options=league_df.columns
)

# Sort the DataFrame based on the selected column
league_df_sorted = league_df.sort_values(by=sort_column, ascending=False)

fig, ax = plt.subplots()
ax.axis('off')

table = ax.table(cellText=league_df_sorted.values, colLabels=league_df_sorted.columns, loc='center')

if plot_choice == 'NFL':
    header_color = '#2C3E50'      # Deep navy blue
    cell_color = '#ECF6FD'        # Very light blue
    header_text_color = 'white'
elif plot_choice == 'MLB':
    header_color = '#3A6B35'      # Forest green
    cell_color = '#E9F7EF'        # Mint cream
    header_text_color = 'white'
elif plot_choice == 'NBA':
    header_color = '#7D5A50'      # Cocoa brown
    cell_color = '#F5F0EB'        # Off-white with warmth
    header_text_color = 'white'
elif plot_choice == 'NHL':
    header_color = '#C0392B'      # Strong red
    cell_color = '#FDEDEC'        # Blush pink
    header_text_color = 'white'
elif plot_choice == 'MLS':
    header_color = '#2C3E50'      # Dark gray-blue
    cell_color = '#F2F4F4'        # Soft gray
    header_text_color = 'white'
else:
    header_color = '#2C3E50'      # Deep navy blue
    cell_color = '#ECF6FD'        # Very light blue
    header_text_color = 'white'

# Apply colors
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header row
        cell.set_facecolor(header_color)
        cell.get_text().set_color(header_text_color)
        cell.set_text_props(weight='bold')  # Optional: bold header text
    else:
        cell.set_facecolor(cell_color)

st.subheader(f'{plot_choice}')
st.pyplot(fig)




