import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#gsheets
@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mood Log").sheet1
    return sheet

sheet = connect_to_sheet()

#data load
data = sheet.get_all_records()
df = pd.DataFrame(data)
if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.month
    df["year"] = df["timestamp"].dt.year
else:
    df = pd.DataFrame(columns=["timestamp", "mood", "note", "date", "month", "year"])

page = st.sidebar.radio("Navigate", ["📋 Mood Logger", "📈 Summary Dashboard"])

#mood logger 
if page == "📋 Mood Logger":
    st.title("🧠 Mood of the Queue")

    st.markdown("Log your current mood 👇")
    mood = st.selectbox("Select Mood", ["😊", "😠", "😕", "🎉"])
    note = st.text_input("Optional note")
    if st.button("Submit Mood"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, mood, note])
        st.success("Mood logged!")

# Dashboard
elif page == "📈 Summary Dashboard":
    # Auto-refresh for every 5 sec
    st_autorefresh(interval=5000, key="dashboard_autorefresh")

    st.title("📈 Mood Summary Dashboard")

    if df.empty:
        st.warning("No mood data available.")
    else:
        st.sidebar.header("📅 Filters")
        selected_year = st.sidebar.multiselect("Select Year", sorted(df["year"].unique()))
        selected_month = st.sidebar.multiselect("Select Month", sorted(df["month"].unique()))
        selected_emoji = st.sidebar.multiselect("Select Emoji", df["mood"].unique())

        filtered_df = df.copy()

        if selected_year:
            filtered_df = filtered_df[filtered_df["year"].isin(selected_year)]

        if selected_month:
            filtered_df = filtered_df[filtered_df["month"].isin(selected_month)]

        if selected_emoji:
            filtered_df = filtered_df[filtered_df["mood"].isin(selected_emoji)]

        # Bar Chart by Year
        if not filtered_df.empty:
            summary_counts = filtered_df.groupby(["year", "mood"]).size().reset_index(name="count")
            summary_counts = summary_counts.sort_values("year")
            summary_counts["year"] = summary_counts["year"].astype(str)
            emoji_to_label = {
                "😠": "Angry",
                "😊": "Happy",
                "😕": "Confused",
                "🎉": "Celebration"
            }
            emoji_colors = {
                "😠": "red",
                "😊": "green",
                "😕": "orange",
                "🎉": "blue"
            }
            summary_counts["emotion_label"] = summary_counts["mood"].map(emoji_to_label)
            # Plot chart
            st.subheader("📊 Mood Reactions by Year")
            fig = px.bar(
                summary_counts,
                x="year",
                y="count",
                color="mood",
                text_auto=True,
                color_discrete_map=emoji_colors,
                hover_data={
                    "mood": True,
                    "emotion_label": True,
                    "year": False,
                    "count": True
                },
                labels={
                    "mood": "Mood",
                    "year": "Year",
                    "emotion_label": "Emotion",
                    "count": "Reaction Count"
                },
                title="Mood Reactions by Year"
            )

            fig.update_layout(
                barmode="group",
                xaxis_title="Year",
                yaxis_title="Reaction Count",
                xaxis_type='category'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Word Cloud from Notes
            if not filtered_df["note"].dropna().empty:
                st.subheader("Word Cloud from Notes")
                text_blob = " ".join(filtered_df["note"].dropna().astype(str).tolist())
                wordcloud = WordCloud(width=800, height=300, background_color="black", colormap="Pastel1").generate(text_blob)

                fig_wc, ax = plt.subplots(figsize=(10, 4))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig_wc)
            else:
                st.info("No comments/notes available to generate word cloud.")
        else:
            st.info("No data matches the selected filters.")
