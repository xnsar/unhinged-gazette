import streamlit as st
import os
import requests
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="The Unhinged Gazette",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS — Exact Screenshot Match
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=UnifrakturMaguntia&family=IM+Fell+English:ital@0;1&family=Roboto+Condensed:wght@400;700&family=Special+Elite&display=swap');

/* ---- BASE ---- */
html, body, [class*="css"] {
    background-color: #e8e0cc !important;
    color: #1a1208 !important;
}

.stApp {
    background-color: #e8e0cc !important;
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 31px,
        rgba(140,120,80,0.15) 31px,
        rgba(140,120,80,0.15) 32px
    );
}

.block-container {
    padding-top: 0rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ---- HIDE STREAMLIT TOOLBAR (black bar) ---- */
header[data-testid="stHeader"] {
    background-color: #e8e0cc !important;
    height: 0px !important;
    min-height: 0px !important;
    overflow: hidden !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

/* ---- TOP THICK RULE ---- */
.top-rule {
    border: none;
    border-top: 6px solid #1a1208;
    margin: 0 0 0 0;
}

/* ---- DATELINE BAR ---- */
.dateline-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #1a1208;
    border-top: 2px solid #1a1208;
    border-bottom: 2px solid #1a1208;
    padding: 5px 4px;
    margin: 0;
}

/* ---- NAMEPLATE ---- */
.nameplate {
    text-align: center;
    padding: 10px 0 6px 0;
    border-bottom: 1.5px solid #1a1208;
    margin-bottom: 0;
}

.nameplate-title {
    font-family: 'UnifrakturMaguntia', cursive;
    font-size: 72px;
    line-height: 1;
    color: #1a1208;
    margin: 0;
    padding: 0;
}

.nameplate-rule {
    border: none;
    border-top: 1.5px solid #1a1208;
    margin: 6px 0 4px 0;
}

.nameplate-tagline {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: 18px;
    color: #1a1208;
    letter-spacing: 0.5px;
    margin: 4px 0 0 0;
    padding: 0;
}

/* ---- TICKER ---- */
.ticker-wrap {
    background: #1a1208;
    color: #f0ece2;
    display: flex;
    align-items: center;
    overflow: hidden;
    height: 36px;
    margin: 0;
}

.ticker-label {
    background: #c8391a;
    color: #f0ece2;
    font-family: 'Roboto Condensed', sans-serif;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0 14px;
    height: 100%;
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
    white-space: nowrap;
}

.ticker-track {
    display: flex;
    overflow: hidden;
    flex: 1;
    height: 100%;
    align-items: center;
}

.ticker-content {
    font-family: 'Roboto Condensed', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    white-space: nowrap;
    animation: ticker-scroll 35s linear infinite;
    padding-left: 100%;
    color: #f5c842;
}

@keyframes ticker-scroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}

/* ---- SECTION LABELS ---- */
.section-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1a1208;
    color: #f0ece2;
    font-family: 'Roboto Condensed', sans-serif;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 4px 10px;
    margin-bottom: 8px;
}

.dot-red   { width: 8px; height: 8px; border-radius: 50%; background: #c8391a; display: inline-block; flex-shrink: 0; }
.dot-pink  { width: 8px; height: 8px; border-radius: 50%; background: #e0748a; display: inline-block; flex-shrink: 0; }
.icon-sm   { font-size: 11px; }

/* ---- COLUMN HEADERS ---- */
.col-header {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 28px;
    color: #1a1208;
    margin: 4px 0 6px 0;
    line-height: 1.1;
}

.col-rule {
    border: none;
    border-top: 1.5px solid #1a1208;
    margin: 0 0 14px 0;
}

/* ---- SELECTBOX ---- */
div[data-baseweb="select"] > div {
    background: #e8e0cc !important;
    border: 1.5px solid #1a1208 !important;
    border-radius: 0 !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 15px !important;
    color: #1a1208 !important;
    min-height: 46px !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #1a1208 !important;
}

div[data-baseweb="select"] svg {
    color: #1a1208 !important;
    fill: #1a1208 !important;
}

.stSelectbox label {
    font-family: 'Roboto Condensed', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #1a1208 !important;
}

/* ---- TEXTAREA ---- */
.stTextArea textarea {
    font-family: 'Special Elite', monospace !important;
    font-size: 13px !important;
    background: #e8e0cc !important;
    border: 1.5px solid #1a1208 !important;
    border-radius: 0 !important;
    color: #1a1208 !important;
    line-height: 1.75 !important;
}

.stTextArea label {
    font-family: 'Roboto Condensed', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #1a1208 !important;
}

/* ---- BUTTONS ---- */
.stButton > button {
    font-family: 'Roboto Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: #1a1208 !important;
    color: #f0ece2 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 14px 28px !important;
    width: 100% !important;
    min-height: 64px !important;
    transition: background 0.15s !important;
    box-shadow: 3px 3px 0px #a08040 !important;
}

.stButton > button:hover {
    background: #c8391a !important;
    box-shadow: 3px 3px 0px #8a2510 !important;
}

/* ---- OUTPUT CARD ---- */
.output-card {
    background: #ede6d4;
    border: 1.5px solid #1a1208;
    border-left: 5px solid #c8391a;
    padding: 20px 22px;
    font-family: 'Special Elite', monospace;
    font-size: 14px;
    line-height: 1.85;
    color: #1a1208;
    margin-top: 10px;
    box-shadow: 4px 4px 0px #c8b880;
}

/* ---- DIVIDERS ---- */
hr {
    border: none !important;
    border-top: 1px solid #1a1208 !important;
    margin: 16px 0 !important;
}

/* ---- ALERTS ---- */
.stAlert {
    font-family: 'Special Elite', monospace !important;
    border-radius: 0 !important;
}

/* ---- CAPTION ---- */
.stCaption, .stCaption p {
    font-family: 'Roboto Condensed', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #1a1208 !important;
    text-align: center !important;
    display: block !important;
    width: 100% !important;
}

/* ---- TEXTAREA PLACEHOLDER ---- */
.stTextArea textarea::placeholder {
    color: #1a1208 !important;
    opacity: 0.75 !important;
}

/* ---- SPINNER ---- */
.stSpinner > div {
    font-family: 'Special Elite', monospace !important;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# LOAD API KEYS
# -----------------------------
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
news_key = os.getenv("NEWS_API_KEY")
print("GROQ KEY:", groq_key)
client = Groq(api_key=groq_key)


# -----------------------------
# FETCH NEWS
# -----------------------------
def fetch_news(category):
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=in&max=20&apikey={news_key}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])

    titles = []
    full_articles = []
    seen_titles = set()

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        if title in seen_titles:
            continue
        seen_titles.add(title)
        titles.append(title)
        full_articles.append(f"{title}\n\n{description}")
        if len(titles) == 10:
            break

    numbered_titles = [f"{i+1}. {t}" for i, t in enumerate(titles)]
    return numbered_titles, full_articles


# -----------------------------
# PROMPT GENERATOR
# -----------------------------
def generate_prompt(article, mode):
    if mode == "Gen Z":
        return f"""
Rewrite this news article in chaotic Gen Z language.

Rules:
- Keep all facts accurate
- Do not change numbers or names
- Make it brainrotted, use words like skibidi, rizz, no cap, for real
- Highlight key points
- Don't exaggerate or make up any information, keep it factual and precise

Article:
{article}
"""
    elif mode == "Twitter Thread":
        return f"""
Convert this news article into a Twitter thread.

Rules:
- Break it into 5-7 tweets
- Keep facts accurate
- Each tweet should be engaging and short

Article:
{article}
"""
    elif mode == "Meme Mode":
        return f"""
Turn this news article into meme-style commentary.

Rules:
- Keep the facts accurate
- Use internet humor
- Use viral meme phrases
- Use appropriate and contextual emojis
- Actually provide the news as well

Article:
{article}
"""
    elif mode == "Ultra Chaotic":
        return f"""
Rewrite this news article in extremely chaotic internet brainrot style.

Rules:
- Keep all facts accurate — do NOT change numbers or names
- Maximum chaos and absurd humor
- Use dramatic internet tone: ALL CAPS for shocking moments, excessive punctuation, meltdown energy
- Mix Gen Z slang, meme references, dramatic news anchor energy, and unhinged commentary
- React to the news like you just witnessed the most insane thing ever
- Use words like: BROOO, NO WAY, HE'S COOKED, THIS IS WILD, ACTUAL CINEMA, DOWN BAD, SLAY, CAUGHT IN 4K, L BEHAVIOR, W MOVE
- Add chaotic running commentary between facts
- Finish with an unhinged take or prediction

Article:
{article}
"""


# -----------------------------
# MASTHEAD
# -----------------------------
today = datetime.now().strftime("%A, %B %d, %Y").upper()

today_live = datetime.now().strftime("%A, %B %d, %Y").upper()

st.markdown(f"""
<div style="border-top: 1px solid #1a1208; margin-bottom: 0;"></div>
<div class="top-rule"></div>
<div class="dateline-bar">
    <span>EST. 2025 &nbsp;·&nbsp; VOL. I, NO. 1</span>
    <span>{today_live}</span>
    <span>PRICE: YOUR SANITY</span>
</div>
<div class="nameplate">
    <div class="nameplate-title">The Unhinged Gazette</div>
    <hr class="nameplate-rule">
    <div class="nameplate-tagline" style="text-align:center;">"All the news that's fit to brainrot"</div>
</div>
<div class="ticker-wrap">
    <div class="ticker-label"><span class="icon-sm">⚡</span> BREAKING</div>
    <div class="ticker-track">
        <div class="ticker-content">
            AI NOW REWRITES NEWS IN GEN Z &nbsp;·&nbsp;
            TWITTER THREADS CONFIRMED STILL A THING &nbsp;·&nbsp;
            MEME JOURNALISM RISING &nbsp;·&nbsp;
            YOUR DAILY DOSE OF CERTIFIED BRAINROT &nbsp;·&nbsp;
            GROQ GOES BRRR &nbsp;·&nbsp;
            LOCAL MAN RIZZES UP THE ENTIRE NEWS CYCLE &nbsp;·&nbsp;
            SKIBIDI SIGMA COVERAGE IMMINENT &nbsp;·&nbsp;
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# CONTROL PANEL
# -----------------------------
col1, col2, col3 = st.columns([5, 5, 3])

with col1:
    st.markdown('<div class="section-label"><span class="icon-sm">🗂</span> CATEGORY</div>', unsafe_allow_html=True)
    category = st.selectbox(
        "Category",
        ["world", "business", "technology", "sports", "entertainment", "health"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-label"><span class="icon-sm">🔥</span> CHAOS MODE</div>', unsafe_allow_html=True)
    mode = st.selectbox(
        "Chaos Mode",
        ["Gen Z", "Twitter Thread", "Meme Mode", "Ultra Chaotic"],
        label_visibility="collapsed"
    )

with col3:
    st.markdown('<div class="section-label" style="background:transparent;color:transparent;">.</div>', unsafe_allow_html=True)
    fetch_button = st.button("⚡ PULL\nHEADLINES")

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# FETCH ARTICLES
# -----------------------------
if fetch_button:
    titles, articles = fetch_news(category)
    st.session_state["titles"] = titles
    st.session_state["articles"] = articles
    st.markdown(
        f'<p style="font-family:\'Roboto Condensed\', sans-serif; font-weight:700; font-size:12px; letter-spacing:2px; text-transform:uppercase; color:#1a1208; margin: 4px 0 0 2px;">✔ &nbsp;{len(titles)} headlines loaded from the wire — {category.upper()} desk</p>',
        unsafe_allow_html=True
    )


# -----------------------------
# MAIN TWO-COLUMN LAYOUT
# -----------------------------
left, right = st.columns([1, 1], gap="large")


# LEFT — Headlines
with left:
    st.markdown(
        '<div class="section-label"><span class="dot-red"></span> HEADLINES</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="col-header">Today\'s Top Stories</div>', unsafe_allow_html=True)
    st.markdown('<hr class="col-rule">', unsafe_allow_html=True)

    if "titles" in st.session_state:
        selected_index = st.selectbox(
            "Select story",
            range(len(st.session_state["titles"])),
            format_func=lambda x: st.session_state["titles"][x],
            label_visibility="collapsed"
        )
        news_input = st.text_area(
            "Article",
            value=st.session_state["articles"][selected_index],
            height=300,
            label_visibility="collapsed"
        )
    else:
        news_input = st.text_area(
            "Paste article here",
            placeholder="Fetch headlines above — or paste any article directly here...",
            height=300,
            label_visibility="collapsed"
        )


# RIGHT — AI Output
with right:
    label_dot = "dot-pink" if mode == "Twitter Thread" else "dot-red"
    mode_upper = mode.upper()

    st.markdown(
        f'<div class="section-label"><span class="{label_dot}"></span> {mode_upper} OUTPUT</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="col-header">AI Correspondent Dispatch</div>', unsafe_allow_html=True)
    st.markdown('<hr class="col-rule">', unsafe_allow_html=True)

    if st.button("🗞️ UNHINGE THIS ARTICLE"):
        if news_input and news_input.strip():
            prompt = generate_prompt(news_input, mode)
            with st.spinner("Setting the presses to maximum chaos..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    output = response.choices[0].message.content
                    st.markdown(f'<div class="output-card">{output}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Press room error: {e}")
        else:
            st.warning("No article loaded. Fetch headlines or paste one on the left.")


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; font-family:\'Roboto Condensed\', sans-serif; font-weight:700; font-size:13px; letter-spacing:1.5px; text-transform:uppercase; color:#1a1208;">📜 The Unhinged Gazette &nbsp;·&nbsp; Est. 2025 &nbsp;·&nbsp; Brainrot journalism for the chronically online &nbsp;·&nbsp; Not liable for sigma damage &nbsp;·&nbsp; No skibidi journalists were harmed &nbsp;·&nbsp; Rizz-certified reporting &nbsp;·&nbsp; Ohio news free zone &nbsp;·&nbsp; 100% gyatt-approved &nbsp;·&nbsp; Powered by Groq + GNews &nbsp;·&nbsp; Fr fr no cap</p>',
    unsafe_allow_html=True
)