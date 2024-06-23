import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file = 'btcdata.csv'
df = pd.read_csv(file, header=None, names=['Timestamp', 'Price', 'Sentiment'])

# Convert the Timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot BTC price on the primary y-axis
ax1.plot(df['Timestamp'], df['Price'], color='blue', marker='o', linestyle='-', label='BTC Price')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Price (USD)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Create a secondary y-axis to plot sentiment scores
ax2 = ax1.twinx()
ax2.plot(df['Timestamp'], df['Sentiment'], color='red', marker='x', linestyle='--', label='Sentiment Score')
ax2.set_ylabel('Sentiment Score', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add titles and legends
plt.title('BTC Price and Reddit Sentiment Over Time')
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))

# Show the plot
plt.xticks(rotation=45)
plt.show()
