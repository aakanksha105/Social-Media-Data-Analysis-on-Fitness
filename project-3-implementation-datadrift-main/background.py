from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Words to include in the word cloud (subreddits which we used in our project)
words = """
politics PoliticalDiscussion uspolitics democrats AskTrumpSupporters congress fitness bodyweightfitness HealthyFood 
nutrition exercise loseit gainit running yoga crossfit flexibility strength_training xxfitness
"""

# Create a WordCloud instance
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis"
).generate(words)

# Save the word cloud image
output_path = "static/wordcloud.png"  
wordcloud.to_file(output_path)
print(f"Word cloud saved at {output_path}")

# Display the word cloud
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
