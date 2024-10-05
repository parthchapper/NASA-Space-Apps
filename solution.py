import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file named 'test.csv' in the same folder
file_name = '/Users/parth/Desktop/GCSC CS/my progectes/NASA Space apps/Seismic Graph/test.csv'
data = pd.read_csv(file_name)

# Define columns (adjust to match your dataset)
time_column = 'time_rel(sec)'
velocity_column = 'velocity(m/s)'

# Set short-term and long-term window sizes (in seconds or data points)
sta_window = 5  # Short-Term Average window
lta_window = 15  # Long-Term Average window
threshold = 3.0  # Define the threshold for detecting seismic events

# Calculate STA (Short-Term Average) and LTA (Long-Term Average)
data['STA'] = data[velocity_column].rolling(window=sta_window, min_periods=1).mean()
data['LTA'] = data[velocity_column].rolling(window=lta_window, min_periods=1).mean()

# Calculate STA/LTA ratio
sta_lta_ratio = data['STA'] / data['LTA']

# Normalize STA/LTA ratio to avoid extreme values
sta_lta_ratio_normalized = (sta_lta_ratio - sta_lta_ratio.mean()) / sta_lta_ratio.std()

# Detect seismic events where STA/LTA ratio exceeds the threshold
seismic_events = data[time_column][sta_lta_ratio_normalized > threshold]

# Plotting the STA/LTA ratio
plt.figure(figsize=(10, 6))

# Plot the STA/LTA ratio for data below the threshold
below_threshold = sta_lta_ratio_normalized <= threshold
plt.plot(data[time_column][below_threshold], sta_lta_ratio_normalized[below_threshold], label='STA/LTA Below Threshold', color='blue')

# Plot the STA/LTA ratio for seismic events (above the threshold)
above_threshold = sta_lta_ratio_normalized > threshold
plt.plot(data[time_column][above_threshold], sta_lta_ratio_normalized[above_threshold], label='STA/LTA Above Threshold', color='green')

# Mark the seismic events
plt.scatter(seismic_events, [threshold] * len(seismic_events), color='red', label='Seismic Events', zorder=5)

# Add the threshold line
plt.axhline(y=threshold, color='gray', linestyle='--', label='Threshold')

# Set y-axis limits to zoom in and focus on relevant data
plt.ylim(-5, 5)

# Add labels and title
plt.title('Seismic Event Detection using STA/LTA')
plt.xlabel('Time (seconds)')
plt.ylabel('STA/LTA Ratio (Normalized)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
