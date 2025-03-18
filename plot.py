import json
import pandas as pd
import matplotlib.pyplot as plt

# Sample output from the /requests endpoint read from insert.json
data = open('insert.json').read()
data = json.loads(data)

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=['ID', 'Message', 'Hostname'])

# Count the occurrences of each hostname
hostname_counts = df['Hostname'].value_counts()

# Plot the data
hostname_counts.plot(kind='bar', color='skyblue')
plt.title('Requests per Hostname')
plt.xlabel('Hostname')
plt.ylabel('Number of Requests')
plt.show()
# - HAP not working
# - pod porbs due to replicas are sufficient
# - dbs are not able to handle the load for write operations
# - resources are not sufficient which causes the pod to crash OOM
