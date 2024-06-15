import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sys
from datetime import datetime as dt
import calendar as cal

# Lambda functions to convert data
to_float = lambda x: float(x.strip() or np.nan)
to_month = lambda x: dt.strptime(x, "%Y%m%d").month

# Load data from the file specified in the command line argument
# Usecols specifies the columns to read: 1 for date, 35 for avg humidity, 36 for max humidity, 38 for min humidity
months, avg_h, max_h, min_h = np.loadtxt(sys.argv[1], delimiter=',', usecols=(0, 1, 2, 3), unpack=True, converters={0: to_month, 1: to_float, 2: to_float, 3: to_float})

# Mask invalid (NaN) values
max_h = ma.masked_invalid(max_h)
avg_h = ma.masked_invalid(avg_h)
min_h = ma.masked_invalid(min_h)

# Print humidity statistics
print(f"Maximum Humidity: {max_h.max()}")
print(f"Average Humidity: {avg_h.mean()} Std Dev: {avg_h.std()}")
print(f"Minimum Humidity: {min_h.min()}")

# Calculate monthly humidity statistics
monthly_humidity = []
maxes = []
mins = []
month_range = np.arange(int(months.min()), int(months.max()) + 1)

for month in month_range:
    indices = np.where(month == months)
    monthly_humidity.append(avg_h[indices].mean())
    maxes.append(max_h[indices].max())
    mins.append(min_h[indices].min())

# Plot histogram of average humidity
plt.subplot(211)
plt.title("Humidity Histogram")
plt.hist(avg_h.compressed(), 200)

# Plot monthly humidity statistics
ax = plt.subplot(212)
plt.title("Monthly Humidity")
plt.plot(month_range, monthly_humidity, 'bo', label="Average")
plt.plot(month_range, maxes, 'r^', label="Maximum Values")
plt.plot(month_range, mins, 'g>', label="Minimum Values")
ax.set_xticks(month_range)  # Set x-ticks to month range
ax.set_xticklabels([cal.month_abbr[i] for i in month_range])  # Set month abbreviations as x-tick labels
plt.legend(prop={'size': 'x-small'}, loc='best')
ax.set_ylabel('%')
plt.tight_layout()  # Adjust subplots to fit into the figure area.
plt.show()
