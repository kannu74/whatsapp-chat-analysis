import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit theme to dark mode
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stSidebar {
        background-color: #1e1e1e;
    }
    .stTitle, .stHeader {
        color: #bb86fc;
    }
    .stDataFrame {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title('Whatsapp Chat Analyzer')

# File uploading
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = preprocess.preprocess(data)
    
    # Getting unique users
    user_list = df['Sender'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox('Select User', user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(num_links)
        
        # Set dark theme for plots
        plt.style.use("dark_background")
        
        # Monthly timeline
        st.title("Monthly Timeline")
        timeline_df = helper.create_monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(timeline_df['time'], timeline_df['Message'], marker='o', linestyle='-', color='#bb86fc')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.create_daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(daily_timeline['date'], daily_timeline['Message'], marker='o', linestyle='-', color='#03dac6')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Most Busy Day')
            busy_day = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(busy_day.index, busy_day.values, color='#ff0266')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(busy_month.index, busy_month.values, color='#ffde03')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        # Activity heatmap
        st.title("Weekly Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(heatmap, ax=ax, cmap='mako')
        st.pyplot(fig)
        
        # Finding busiest user in group
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, y = helper.find_busiest_user(df)
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.bar(x.index, x.values, color='#6200ea')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            with col2:
                st.dataframe(y)
        
        # Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        
        # Most common words used
        st.title("Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        st.dataframe(most_common_words)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(most_common_words['Word'], most_common_words['Frequency'], color='#03dac6')
        st.pyplot(fig)
        
        # Emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user, df)
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.pie(
                emoji_df['Frequency'], 
                labels=emoji_df['Emoji'], 
                autopct='%1.1f%%',
                textprops={'fontname': 'Segoe UI Emoji'},  # Use system emoji font
                colors=['#bb86fc', '#03dac6', '#ff0266', '#ffde03', '#6200ea']
            )
            st.pyplot(fig)