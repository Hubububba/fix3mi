import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Interactive Media Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- App Title and Description ---
st.title("📊 Interactive Media Intelligence Dashboard")
st.markdown("Gain insights from your media data by uploading a CSV file below.")

# --- Helper Functions ---

@st.cache_data # Cache the data loading and cleaning to improve performance
def clean_data(uploaded_file):
    """
    Reads an uploaded CSV file, cleans the data, and returns a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(uploaded_file)
        
        # Normalize column names (e.g., "Media Type" -> "mediatype")
        original_cols = df.columns
        df.columns = df.columns.str.strip().str.lower().str.replace(r'\s+', '', regex=True)
        
        # --- Data Validation ---
        required_cols = {'date', 'platform', 'sentiment', 'location', 'engagements', 'mediatype'}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV file is missing required columns. It must contain: Date, Platform, Sentiment, Location, Engagements, Media Type.")
            st.info(f"Detected columns: {', '.join(original_cols)}")
            return None

        # --- Data Cleaning ---
        # Convert 'date' column to datetime objects, coercing errors to NaT
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Fill missing 'engagements' with 0 and convert to numeric
        df['engagements'] = pd.to_numeric(df['engagements'], errors='coerce').fillna(0)
        
        # Drop rows with invalid dates
        cleaned_df = df.dropna(subset=['date']).copy()
        
        if cleaned_df.empty:
            st.warning("No valid data found after cleaning. Please check the 'Date' column format in your CSV.")
            return None
            
        return cleaned_df

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        return None

def get_sentiment_insights(sentiment_counts):
    """Generates insights for the sentiment data."""
    if sentiment_counts.empty:
        return ["No sentiment data available."]
        
    total = sentiment_counts.sum()
    dominant_sentiment = sentiment_counts.index[0]
    dominant_pct = (sentiment_counts.iloc[0] / total) * 100
    
    insights = [
        f"1. The dominant sentiment is **{dominant_sentiment}**, accounting for **{dominant_pct:.1f}%** of mentions. This sets the primary tone of the conversation.",
        "2. By comparing proportions, you can gauge the balance of opinion and determine if your messaging has the desired emotional impact."
    ]
    if len(sentiment_counts) > 1:
        secondary_sentiment = sentiment_counts.index[1]
        insights.insert(1, f"2. **{secondary_sentiment}** is the second most common response, indicating a significant secondary emotion from the audience.")
    
    insights.append("**Recommendation:** If negative sentiment is high, address the root causes. If positive, identify and amplify the content driving it.")
    return insights

def get_engagement_trend_insights(daily_engagements):
    """Generates insights for engagement trends."""
    if daily_engagements.empty:
        return ["No engagement data available."]
        
    peak_date = daily_engagements.idxmax().strftime('%b %d, %Y')
    peak_value = daily_engagements.max()
    low_date = daily_engagements.idxmin().strftime('%b %d, %Y')
    low_value = daily_engagements.min()
    
    insights = [
        f"1. Peak engagement of **{int(peak_value):,}** occurred on **{peak_date}**. Analyze the content posted on this day to identify successful strategies.",
        f"2. The lowest engagement was **{int(low_value):,}** on **{low_date}**. Review this period to find opportunities for improvement.",
        "**Recommendation:** Replicate successful content from peak periods. Analyze and adjust your strategy based on periods of low engagement."
    ]
    return insights

def get_platform_insights(platform_engagements):
    """Generates insights for platform engagement."""
    if platform_engagements.empty:
        return ["No platform data available."]
        
    top_platform = platform_engagements.index[0]
    top_platform_val = platform_engagements.iloc[0]
    
    insights = [
        f"1. **{top_platform}** is the leading platform, generating **{int(top_platform_val):,}** engagements. This channel is your powerhouse for audience interaction.",
    ]
    if len(platform_engagements) > 1:
        second_platform = platform_engagements.index[1]
        second_platform_val = platform_engagements.iloc[1]
        insights.append(f"2. **{second_platform}** shows strong secondary performance with **{int(second_platform_val):,}** engagements, offering an opportunity to diversify your reach.")
        
    insights.append("**Recommendation:** Allocate more resources to leading platforms. Re-evaluate or test new approaches on underperforming channels.")
    return insights
    
def get_media_type_insights(media_type_counts):
    """Generates insights for media type mix."""
    if media_type_counts.empty:
        return ["No media type data available."]

    total = media_type_counts.sum()
    top_media_type = media_type_counts.index[0]
    top_media_type_pct = (media_type_counts.iloc[0] / total) * 100

    insights = [
        f"1. **{top_media_type}** is the most used format, making up **{top_media_type_pct:.1f}%** of your content.",
        "**Recommendation:** Prioritize creating content in the formats your audience engages with most. Experiment with converting high-performing content into different media types."
    ]
    return insights

def get_location_insights(location_engagements):
    """Generates insights for top locations."""
    if location_engagements.empty:
        return ["No location data available."]
        
    top_location = location_engagements.index[0]
    top_location_val = location_engagements.iloc[0]
    
    insights = [
        f"1. **{top_location}** is the top location with **{int(top_location_val):,}** engagements. This region contains your most active audience.",
    ]
    if len(location_engagements) > 1:
        second_location = location_engagements.index[1]
        second_location_val = location_engagements.iloc[1]
        insights.append(f"2. **{second_location}** is another key geographical market. Nurturing this audience could open new growth opportunities.")
        
    insights.append("**Recommendation:** Launch localized campaigns or geo-targeted ads to deepen engagement in top locations.")
    return insights


# --- Main Application ---

# --- Sidebar for File Upload ---
with st.sidebar:
    st.header("📋 Controls")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    st.markdown("---")
    st.info("""
    **Required CSV Columns:**
    - `Date` (e.g., YYYY-MM-DD)
    - `Platform` (e.g., Twitter, Facebook)
    - `Sentiment` (e.g., Positive, Neutral)
    - `Location` (e.g., USA, UK)
    - `Engagements` (e.g., 123)
    - `Media Type` (e.g., Article, Video)
    """)

if uploaded_file is not None:
    df = clean_data(uploaded_file)
    
    if df is not None:
        st.success(f"Successfully loaded and cleaned {len(df)} data entries.")
        st.markdown("---")

        # --- Chart and Insight Display ---
        
        # Row 1: Sentiment and Engagement Trend
        col1, col2 = st.columns((1, 1))
        with col1:
            st.subheader("Sentiment Breakdown")
            sentiment_counts = df['sentiment'].value_counts()
            fig_sentiment = px.pie(
                values=sentiment_counts.values, 
                names=sentiment_counts.index, 
                title='Sentiment Distribution', 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig_sentiment.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_sentiment, use_container_width=True)
            
            with st.expander("View Insights & Recommendations"):
                st.markdown("\n".join(f"- {insight}" for insight in get_sentiment_insights(sentiment_counts)))

        with col2:
            st.subheader("Engagement Trend Over Time")
            daily_engagements = df.groupby(df['date'].dt.date)['engagements'].sum()
            fig_engagement = px.line(
                x=daily_engagements.index, 
                y=daily_engagements.values,
                title='Daily Engagements',
                labels={'x': 'Date', 'y': 'Total Engagements'}
            )
            fig_engagement.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_engagement, use_container_width=True)

            with st.expander("View Insights & Recommendations"):
                st.markdown("\n".join(f"- {insight}" for insight in get_engagement_trend_insights(daily_engagements)))

        st.markdown("---")

        # Row 2: Platform, Media Type, Location
        col3, col4, col5 = st.columns((1, 1, 1))
        with col3:
            st.subheader("Platform Engagements")
            platform_engagements = df.groupby('platform')['engagements'].sum().sort_values(ascending=False)
            fig_platform = px.bar(
                x=platform_engagements.index,
                y=platform_engagements.values,
                title='Engagements by Platform',
                labels={'x': 'Platform', 'y': 'Total Engagements'}
            )
            fig_platform.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_platform, use_container_width=True)
            
            with st.expander("View Insights & Recommendations"):
                 st.markdown("\n".join(f"- {insight}" for insight in get_platform_insights(platform_engagements)))

        with col4:
            st.subheader("Media Type Mix")
            media_type_counts = df['mediatype'].value_counts()
            fig_media = px.pie(
                values=media_type_counts.values,
                names=media_type_counts.index,
                title='Media Type Proportions',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Agsunset
            )
            fig_media.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_media, use_container_width=True)
            
            with st.expander("View Insights & Recommendations"):
                 st.markdown("\n".join(f"- {insight}" for insight in get_media_type_insights(media_type_counts)))

        with col5:
            st.subheader("Top 5 Locations")
            location_engagements = df.groupby('location')['engagements'].sum().sort_values(ascending=False).head(5)
            fig_location = px.bar(
                x=location_engagements.index,
                y=location_engagements.values,
                title='Top 5 Locations by Engagement',
                labels={'x': 'Location', 'y': 'Total Engagements'}
            )
            fig_location.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_location, use_container_width=True)

            with st.expander("View Insights & Recommendations"):
                 st.markdown("\n".join(f"- {insight}" for insight in get_location_insights(location_engagements)))
                 
        st.markdown("---")
        
        # --- Concluding Recommendations ---
        st.header("Concluding Recommendations")
        col6, col7 = st.columns(2)
        with col6:
            st.success("**What's Working**")
            st.markdown("""
            - **High-Engagement Platforms:** Continue investing in your top-performing platforms.
            - **Popular Content Formats:** Double down on creating content in formats that resonate with your audience.
            - **Strong Geographic Reach:** Leverage high engagement in key locations with targeted campaigns.
            """)
        with col7:
            st.warning("**What Needs Improvement**")
            st.markdown("""
            - **Underperforming Platforms:** Re-evaluate your strategy for channels with low engagement.
            - **Negative Sentiment:** Identify and address the root causes of negative feedback promptly.
            - **Engagement Dips:** Analyze periods of low engagement to identify weaknesses and avoid future lulls.
            """)

else:
    st.info("Awaiting for CSV file to be uploaded. Please use the sidebar to upload your data.")
    st.image("https://i.imgur.com/uJ8ENTy.png", caption="Upload a file to get started.")

