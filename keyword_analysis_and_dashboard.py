import json
import streamlit as st
from keybert import KeyBERT
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import matplotlib.pyplot as plt

# data loading
@st.cache_data
def load_data(path="classified_reddit.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# init model
kw_model = KeyBERT(model="all-MiniLM-L6-v2")
sentiment_analyzer = SentimentIntensityAnalyzer()

# preparing & filtering
for post in data:
    text = f"{post.get('title', '')} {post.get('selftext', '')}".strip()
    post["full_text"] = text
    post["sentiment"] = sentiment_analyzer.polarity_scores(text)["compound"]

# streamlit sidebar
st.title("📉 OTT Journey Pain Point Dashboard")
st.sidebar.header("🔎 Filter by Journey Stage")

all_stages = sorted(set(p.get("journey_stage", "Unknown") for p in data if p.get("journey_stage")))
selected_stage = st.sidebar.selectbox("Select a Journey Stage", all_stages)

# post filter
filtered_posts = [
    p for p in data
    if p.get("journey_stage") == selected_stage and
       p["sentiment"] <= -0.2 and
       len(p["full_text"]) > 20
]

st.markdown(f"**Total Negative Posts in {selected_stage}:** {len(filtered_posts)}")

if not filtered_posts:
    st.warning("No negative posts found for this stage.")
    st.stop()

# keyword extraction
combined_text = " ".join([p["full_text"] for p in filtered_posts])
keywords = kw_model.extract_keywords(
    combined_text,
    keyphrase_ngram_range=(1, 3),
    stop_words="english",
    top_n=10
)

# table
st.subheader("📌 Top Pain Point Keywords")
st.dataframe(keywords, use_container_width=True)

# bar chart
st.subheader("📊 Keyword Importance Score")

terms = [kw[0] for kw in keywords]
scores = [kw[1] for kw in keywords]

fig, ax = plt.subplots()
ax.barh(terms[::-1], scores[::-1], color='firebrick')
ax.set_xlabel("Relevance Score")
ax.set_title(f"Top Pain Keywords – {selected_stage}")
st.pyplot(fig)