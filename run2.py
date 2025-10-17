import streamlit as st
import spacy
from spacy import displacy

# --- Configuration/Setup ---
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()
st.title("spaCy Named Entity Recognition (NER)")

# --- Input Widget ---
# Create a text area and store its content in session state
input_text = st.text_area(
    "Enter text for NER:",
    key='text_area',
    height=200,
    value="Apple is looking at buying U.K. startup, for $1 billion." # Optional: default text
)

# --- NER Logic (Your Snippet) ---
text = st.session_state.get('text_area', '') # Now this will have text from the widget

if text.strip():
    doc = nlp(text)

    # Display entities with colors using displaCy HTML
    html = displacy.render(doc, style="ent", jupyter=False)
    st.write("**Detected Entities:**", unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)

    # Optional: show entity table
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if entities:
        st.markdown("**Entity Table:**")
        st.table(entities)
    else:
        st.info("No named entities found in the provided text.")

else:
    # This message only appears if the text area is empty
    st.info("Paste or select some text to see NER results.")