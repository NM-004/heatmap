import pandas as pd
import numpy as np

# Load the data from a CSV file (adjust the path as needed)
data = pd.read_csv('data.csv')

# Convert the 'date' column to datetime (this ensures .dt accessor works)
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Define colors for heatmap based on contribution levels
color_map = {
    0: "#ebedf0",
    1: "#c6e48b",
    2: "#7bc96f",
    3: "#239a3b",
    4: "#196127"
}

# Define bins for contribution levels
bins = [0, 1, 5, 10, 20, 100]
data['color'] = pd.cut(data['contributions'], bins=bins, labels=[0, 1, 2, 3, 4], right=False)
data['color'] = data['color'].fillna(0)  # Default color index for NaN values

# Prepare the HTML table for the heatmap
html_output = '<table role="grid" aria-labelledby="contribution-graph-legend" style="border-collapse: collapse;">\n'
html_output += '  <thead>\n'
html_output += '    <tr style="height: 20px;">\n'
# Header row for days of the week
for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
    html_output += f'      <th style="width: 38px; text-align: center;">{day}</th>\n'
html_output += '    </tr>\n'
html_output += '  </thead>\n'
html_output += '  <tbody>\n'

# Generate the heatmap grid (assuming 52 weeks in a year)
for week in range(52):
    html_output += '    <tr style="height:p38x;">\n'
    for day in range(7):
        # Filter data by week and day
        entry = data.loc[(data['date'].dt.isocalendar().week == week + 1) & (data['date'].dt.weekday == day)]
        
        if not entry.empty:
            # Use the first value, after filling NaN
            color_code = color_map[int(entry['color'].values[0])]
        else:
            color_code = "#ebedf0"  # Default no contributions color

        # Generate a unique ID and date for each cell
        date_str = f"{data['date'].dt.year.min()}-W{week+1}-D{day+1}"
        cell_id = f"contribution-day-{week}-{day}"

        html_output += f'      <td style="background-color:{color_code}; width: 38px; height: 38px;" data-date="{date_str}" id="{cell_id}" class="ContributionCalendar-day"></td>\n'
    html_output += '    </tr>\n'

html_output += '  </tbody>\n'
html_output += '</table>'

# Save the generated HTML to a file (or print to console for copy-paste)
with open('heatmap.md', 'w') as f:
    f.write(html_output)

print("Heatmap HTML table generated and saved to heatmap.html")
