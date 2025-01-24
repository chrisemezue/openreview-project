import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Read the CSV file
df = pd.read_csv('/home/mila/c/chris.emezue/naijavoices-research/abraham/data/tts_data_full/all_tts_data.csv')
#breakpoint()
df = df[df['duration']>0]
# Step 2: Group by 'speaker_id' and calculate the sum of 'duration' (in hours) and frequency
grouped = df.groupby('speaker_id').agg(
    duration_hours=('duration', lambda x: x.sum() / 3600),
    frequency=('speaker_id', 'count')
).reset_index()

# Step 3: Merge the 'language' column back (assuming each speaker has one language)
# Keep the first language for each speaker_id
speaker_languages = df.drop_duplicates('speaker_id')[['speaker_id', 'language','phase']]
merged = grouped.merge(speaker_languages, on='speaker_id')

# Step 4: Plot the scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=merged, 
    x='duration_hours', 
    y='frequency', 
    hue='language',
    style='phase', 
    #palette='viridis', 
    s=50
)
# plt.xscale('log')
# plt.yscale('log')
plt.title('Scatterplot of Frequency vs Duration (Log-Scale)', fontsize=14)
plt.xlabel('Total Duration (Hours, Log Scale)', fontsize=12)
plt.ylabel('Frequency (Count, Log Scale)', fontsize=12)
plt.legend(title='Language', fontsize=10, loc='upper right')
#plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('duration_scatterplot.png')
