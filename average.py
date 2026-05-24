import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Initialize lists to store formatted timestamps and calculated averages
times = []
averages = []

# Open and parse the data file
with open('datasets-good/inside2_timestamp.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # Match the timestamp and the list inside brackets
        match = re.match(r'^([\d-]+)\s+\[(.*)\]$', line)
        if match:
            # Extract timestamp, replace dashes with colons, and truncate seconds
            timestamp_raw = match.group(1).replace('-', ':')
            timestamp_hm = ':'.join(timestamp_raw.split(':')[:2])  # Keeps only HH:MM
            
            values_str = match.group(2)
            # Convert RSSI entries to floats
            values = [float(x.strip()) for x in values_str.split(';') if x.strip()]
            
            if values:
                avg_rssi = sum(values) / len(values)
                times.append(timestamp_hm)
                averages.append(avg_rssi)

# Convert times to a sequential numeric index for interpolation
x = np.arange(len(times))
y = np.array(averages)

# Generate a denser set of x-points to create a smooth curve
x_smooth = np.linspace(x.min(), x.max(), 300)
spline = make_interp_spline(x, y, k=3)  # k=3 applies a cubic spline
y_smooth = spline(x_smooth)

# Clear any existing plots
plt.clf()

# Plot the smoothed line without markers
plt.plot(x_smooth, y_smooth, color='blue', linewidth=2)

# Set labels and title
plt.title(f'Average RSSI over Time: School')
plt.xlabel('Time')
plt.ylabel('Average RSSI (dBm)')

# Map the numeric indices back to the original HH:MM timestamps for the x-ticks
tick_indices = range(0, len(times), 5)
plt.xticks(tick_indices, [times[i] for i in tick_indices], rotation=45, ha='right')

# Style adjustments
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Save the updated smooth plot
plt.savefig('school.png')