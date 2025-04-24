import emoji
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

# Fetch statistics like total messages, words, media, and links
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    
    return (
        df.shape[0],  # Total messages
        df['Message'].str.split().str.len().sum(),  # Total words
        (df['Message'] == '<Media omitted>').sum(),  # Total media messages
        df['Message'].str.contains('http', na=False).sum()  # Total messages with links
    )

# Identify the busiest users in the chat
def find_busiest_user(df):
    user_counts = df['Sender'].value_counts()
    percent_activity = (user_counts / df.shape[0] * 100).round(2)
    return user_counts.head(), percent_activity.reset_index().rename(columns={'index': 'User', 'Sender': 'Activity(%)'})

# Load stopwords from a file and add additional custom stopwords
def load_stopwords():
    with open("hinglish_stopwords.txt", "r", encoding="utf-8") as f:
        return set(f.read().splitlines()).union({
            '','<media','omitted>','<Media omitted>', 'message', 'deleted', 'missed', 'https', 'youtube', 'instagram',
            'www', 'com', 'http', 'bit', 'ly', 'youtu', 'be', 'edited', 'igsh', 'reel', 'video', 'media',
            'image', 'omitted', 'sticker', 'gif', 'file', 'document', 'voice', 'call', 'audio', 'link',
            '<This', 'message', 'was', 'deleted>', 'edited>', 'contact', 'h', 'kr', 'mei', 'ni'
        })

# Generate a WordCloud from messages after removing stopwords
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    df = df.dropna(subset=['Message'])
    stopwords = load_stopwords()
    
    text = ' '.join(df['Message'].astype(str))
    if not text.strip():
        return WordCloud(width=800, height=400, background_color="white").generate("No Data")
    
    return WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color="white", stopwords=stopwords).generate(text)

# Find the most common words used in the chat
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    df = df.dropna(subset=['Message'])
    stopwords = load_stopwords()
    
    words = [word.lower() for msg in df['Message'].astype(str) for word in msg.split() if word.lower() not in stopwords]
    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

# Analyze the most frequently used emojis in messages
def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    
    emojis = [char for msg in df['Message'].astype(str) for char in msg if char in emoji.EMOJI_DATA]
    return pd.DataFrame(Counter(emojis).most_common(10), columns=['Emoji', 'Frequency'])

# Create a timeline showing message activity per month
def create_monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month'])['Message'].count().reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

# Create a timeline showing message activity per day
def create_daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    return df.groupby('date')['Message'].count().reset_index()

# Analyze weekly activity trends
def weekly_activity(selected_user, df):
    return df[df['Sender'] == selected_user]['day_name'].value_counts() if selected_user != 'Overall' else df['day_name'].value_counts()

# Analyze monthly activity trends
def monthly_activity(selected_user, df):
    return df[df['Sender'] == selected_user]['month'].value_counts() if selected_user != 'Overall' else df['month'].value_counts()

# Generate a heatmap showing message activity over the week
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    return df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)
