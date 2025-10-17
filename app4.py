<<<<<<< HEAD
import streamlit as st
from gtts import gTTS
import os
from textblob import TextBlob
import speech_recognition as sr
from PIL import Image
from deepface import DeepFace

st.set_page_config(layout="wide", page_title="🧠 Unstructured Data Analysis")
st.title("🧠 Unstructured Data Analysis")

tab1, tab2, tab3 = st.tabs(["🖼️ Image Analysis", "🎧 Audio Analysis", "📝 Text Analysis"])

# ---------------- IMAGE ANALYSIS ----------------
with tab1:
    st.header("🖼️ Image Analysis with Face Recognition")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Simple image info
        st.write(f"**Image Size:** {image.size} pixels")
        st.write(f"**Image Format:** {image.format}")
        st.write(f"**Image Mode:** {image.mode}")
        
        # Face recognition
        try:
            analysis = DeepFace.analyze(img_path=uploaded_image, actions=['age','gender','emotion'])
            st.success("✅ Face Analysis Completed!")
            st.write("**Predicted Age:**", analysis['age'])
            st.write("**Predicted Gender:**", analysis['gender'])
            st.write("**Predicted Emotion:**", analysis['dominant_emotion'])
        except Exception as e:
            st.error(f"❌ Error in face analysis: {e}")

# ----------------------------- AUDIO ANALYSIS -----------------------------
with tab2:
    st.header("🎧 Audio Analysis")

    # --- Text to Speech ---
    st.subheader("🗣️ Text to Speech")
    text_input = st.text_area("Enter text to convert to speech:")
    if st.button("Convert to Audio"):
        if text_input.strip():
            tts = gTTS(text_input, lang='en')
            tts_file = "output.mp3"
            tts.save(tts_file)
            st.audio(tts_file, format="audio/mp3")
            st.success("✅ Conversion complete!")
            # Download button
            with open(tts_file, "rb") as f:
                st.download_button("⬇️ Download Audio", f, file_name="output.mp3", mime="audio/mp3")
        else:
            st.warning("Please enter some text.")

    st.markdown("---")

    # --- Speech to Text ---
    st.subheader("🎙️ Speech to Text")
    audio_file = st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"])
    if audio_file:
        recognizer = sr.Recognizer()
        try:
            if audio_file.name.endswith(".mp3"):
                from pydub import AudioSegment
                sound = AudioSegment.from_mp3(audio_file)
                sound.export("temp.wav", format="wav")
                audio_path = "temp.wav"
            else:
                audio_path = audio_file.name
                with open(audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())

            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                text_result = recognizer.recognize_google(audio_data)
                st.success("✅ Audio converted to text successfully!")
                st.text_area("Recognized Text", value=text_result, height=150)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------------------- TEXT ANALYSIS -----------------------------
with tab3:
    st.header("📝 Text Analysis")
    text_for_analysis = st.text_area("Enter text to analyze sentiment:")
    if st.button("Analyze Sentiment"):
        if text_for_analysis.strip():
            blob = TextBlob(text_for_analysis)
            polarity = blob.sentiment.polarity
            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            st.success(f"Sentiment: {sentiment}")
            st.info(f"Polarity Score: {polarity:.2f}")
        else:
            st.warning("Please enter some text.")
=======
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(layout="wide", page_title="Placement Analytics Dashboard")
st.title("Placement Data Analytics Dashboard - B. Ganesh Goud")

# -----------------------------
# 📂 Load CSV
# -----------------------------
csv_path = r"C:\Users\GANESH\Downloads\NNRG_Placement_2018_2025.csv"
df = pd.read_csv(csv_path, encoding='latin1')

# Optional: Show first 5 rows
st.success("✅ Dataset loaded successfully!")
st.write(df.head())

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
years = sorted(df['Year'].unique())
branches = df['Branch'].unique()
employers = df['Name of the Employer'].unique()

selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(years), index=len(years))
selected_branch = st.sidebar.multiselect("Select Branch", branches, default=branches)
selected_employer = st.sidebar.multiselect("Select Employer", employers, default=employers)

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

filtered_df = filtered_df[
    (filtered_df['Branch'].isin(selected_branch)) &
    (filtered_df['Name of the Employer'].isin(selected_employer))
]

# -----------------------------
# Summary Cards
# -----------------------------
total_students = len(filtered_df)
total_branches = filtered_df['Branch'].nunique()
total_recruiters = filtered_df['Name of the Employer'].nunique()

st.markdown("""
<style>
.summary-card {
    background-color: #000000;  /* Black background */
    color: #ffffff;             /* White text */
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
}
.summary-card h3 { 
    margin: 5px 0; 
}
.summary-card p { 
    font-size: 20px; 
    font-weight: bold; 
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='summary-card'><h3>Total Students</h3><p>{total_students}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='summary-card'><h3>Unique Branches</h3><p>{total_branches}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='summary-card'><h3>Total Recruiters</h3><p>{total_recruiters}</p></div>", unsafe_allow_html=True)

st.markdown("---")


# -----------------------------
# Year-wise Line Chart & Bar Chart
# -----------------------------
st.subheader("Year-wise Placement Trends")
col1, col2 = st.columns(2)

# Prepare DataFrame for line/bar chart
year_df = filtered_df['Year'].value_counts().sort_index().reset_index()
year_df.columns = ['Year', 'Placements']

# Line Chart
fig_line = px.line(
    year_df,
    x='Year',
    y='Placements',
    markers=True,
    title="Year-wise Placement Trend",
    line_shape='linear'
)
col1.plotly_chart(fig_line, use_container_width=True)

# Bar Chart
fig_bar = px.bar(
    year_df,
    x='Year',
    y='Placements',
    text='Placements',
    color='Placements',
    title="Year-wise Placement Count",
    color_continuous_scale='Viridis'
)
col2.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# -----------------------------
# Branch-wise Pie Chart & Treemap
# -----------------------------
st.subheader("Branch-wise Placement Overview")
col1, col2 = st.columns(2)

# Pie Chart
branch_counts = filtered_df['Branch'].value_counts().reset_index()
branch_counts.columns = ['Branch', 'Count']
fig_pie = px.pie(
    branch_counts,
    names='Branch',
    values='Count',
    title="Branch-wise Distribution",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
col1.plotly_chart(fig_pie, use_container_width=True)

# Treemap
fig_treemap = px.treemap(
    branch_counts,
    path=['Branch'],
    values='Count',
    title="Branch-wise Placement Treemap",
    color='Count',
    color_continuous_scale='Viridis'
)
col2.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# -----------------------------
# Top 10 Recruiters
# -----------------------------
st.subheader("Top 10 Recruiters")
top_recruiters = filtered_df['Name of the Employer'].value_counts().head(10).reset_index()
top_recruiters.columns = ['Employer', 'Placements']

fig_top = px.bar(
    top_recruiters,
    x='Placements',
    y='Employer',
    color='Placements',
    orientation='h',
    text='Placements',
    title="Top 10 Recruiters",
    color_continuous_scale=px.colors.sequential.Plasma
)
fig_top.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# -----------------------------
# Sunburst Chart: Year → Branch → Employer
# -----------------------------
st.subheader("Placements Hierarchy: Year → Branch → Employer")
fig_sunburst = px.sunburst(
    filtered_df,
    path=['Year', 'Branch', 'Name of the Employer'],
    color='Branch',
    title="Placements: Year → Branch → Employer",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_sunburst.update_layout(margin=dict(t=50, l=25, r=25, b=25), height=800)
st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown("---")

# -----------------------------
# Branch Summary Cards (Colored)
# -----------------------------
st.subheader("🃏 Branch Summary Cards")
num_cols = 5
branches_list = branch_counts['Branch'].tolist()
colors = ['#FFB6C1', '#ADD8E6', '#90EE90', '#FFD700', '#FFA07A', '#87CEFA', '#9370DB', '#F08080', '#20B2AA', '#FF69B4']

for i in range(0, len(branches_list), num_cols):
    cols = st.columns(num_cols)
    for j, branch in enumerate(branches_list[i:i+num_cols]):
        count = branch_counts[branch_counts['Branch']==branch]['Count'].values[0]
        color = colors[j % len(colors)]
        with cols[j]:
            st.markdown(f"""
            <div style="
                background-color: {color};
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
            ">
                <h3 style="color:#000000;">{branch}</h3>
                <p style="font-size:20px; font-weight:bold;">{count} Students</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Full Data Table
# -----------------------------
st.subheader("Full Placement Data")
st.dataframe(filtered_df, use_container_width=True)
>>>>>>> 94556da8235777e8c68de4d8f659702201489b2e
