import pandas as pd
import matplotlib.pyplot as plt

nfl = pd.read_csv("league_rankings/nfl_rankings.csv")

fig, ax = plt.subplots()
ax.axis('off')

table = ax.table(cellText=nfl.values, colLabels=nfl.columns, loc='center')

# Choose color

header_color = '#2C3E50'      # Deep navy blue
cell_color = '#ECF6FD'        # Very light blue
header_text_color = 'white'

# header_color = '#3A6B35'      # Forest green
# cell_color = '#E9F7EF'        # Mint cream
# header_text_color = 'white'

# header_color = '#7D5A50'      # Cocoa brown
# cell_color = '#F5F0EB'        # Off-white with warmth
# header_text_color = 'white'

# header_color = '#C0392B'      # Strong red
# cell_color = '#FDEDEC'        # Blush pink
# header_text_color = 'white'

# header_color = '#2C3E50'      # Dark gray-blue
# cell_color = '#F2F4F4'        # Soft gray
# header_text_color = 'white'

# Apply colors
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header row
        cell.set_facecolor(header_color)
        cell.get_text().set_color(header_text_color)
        cell.set_text_props(weight='bold')  # Optional: bold header text
    else:
        cell.set_facecolor(cell_color)


plt.show()