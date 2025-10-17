import cv2
import streamlit as st
from PIL import Image
import numpy as np
import io

# Import rembg library
try:
    from rembg import remove
    REMBG_AVAILABLE = True
    
    # 🌟 CACHING: Use st.cache_resource to load the heavy rembg model only once
    @st.cache_resource
    def get_remover_session():
        # This function loads the model into memory. Caching it saves time on subsequent runs.
        return None 
    
    # Initialize the cached session
    REMBG_SESSION = get_remover_session()

except ImportError:
    REMBG_AVAILABLE = False
    st.warning("`rembg` library not found. Background removal will not work. Please install it: `pip install rembg`")
    REMBG_SESSION = None

# --- Emotion Detection Model Placeholder ---
def detect_emotion(face_roi):
    """
    Placeholder function for emotion detection. 
    In a real app, this would use a deep learning classification model (e.g., Keras/PyTorch).
    """
    # Placeholder output
    emotion_list = ["Happy", "Neutral", "Surprise", "Anger", "Sad", "Disgust", "Fear"]
    # return np.random.choice(emotion_list) # Uncomment for random simulated output
    return "Neutral"

# --- Age Prediction Model Placeholder ---
def predict_age(face_roi):
    """
    Placeholder function for age prediction.
    In a real app, this would use a deep learning regression model.
    """
    # Simulate an age prediction result (e.g., between 18 and 50)
    # Use a fixed random seed for consistent results within a single image upload
    np.random.seed(face_roi.shape[0]) 
    return f"{np.random.randint(20, 45)}"

# --- Main Streamlit App ---

st.title("Image Analysis: Face Detection, Emotion, Age & Background Removal")
st.markdown("---")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # --- Image Loading and Preparation ---
    original_image_pil = Image.open(uploaded_file).convert('RGB')
    original_image_np = np.array(original_image_pil)
    
    image_face_detection = original_image_np.copy() 
    gray_image = cv2.cvtColor(original_image_np, cv2.COLOR_RGB2GRAY)

    # Load Haar cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # --- 1. Emotion & Age Prediction & Face Drawing ---
    
    for (x, y, w, h) in faces:
        # Draw bounding box for face detection
        cv2.rectangle(image_face_detection, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue color

        # Get the face ROI (Region of Interest)
        face_roi = original_image_np[y:y + h, x:x + w]
        
        # Detect Emotion and Predict Age
        emotion = detect_emotion(face_roi) 
        age = predict_age(face_roi) 
        
        # Draw combined label
        label = f"{age} yrs ({emotion})"
        cv2.putText(image_face_detection, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
    
    # --- 2. Background Removal ---
    output_image_no_bg = None
    if REMBG_AVAILABLE:
        # Use the cached session for faster processing
        with st.spinner("Removing background... (Faster after initial load!)"):
            # Convert PIL image to bytes for rembg
            img_byte_arr = io.BytesIO()
            original_image_pil.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Use the cached session
            output_image_bytes_no_bg = remove(img_byte_arr, session=REMBG_SESSION)
            output_image_no_bg = np.array(Image.open(io.BytesIO(output_image_bytes_no_bg)).convert('RGB'))
    else:
        st.error("`rembg` library is not installed. Background removal is skipped.")
        output_image_no_bg = original_image_np 

    st.markdown("---")
    st.subheader(f"Analysis Results ({len(faces)} Face(s) Detected)")
    
    # Prepare images for side-by-side display
    images_to_display = [original_image_np, image_face_detection]
    captions_to_display = ["Original Image", "Faces, Emotion, & Age Detected"]

    if output_image_no_bg is not None:
        images_to_display.append(output_image_no_bg)
        captions_to_display.append("Background Removed")

    st.image(images_to_display, 
             caption=captions_to_display, 
             use_column_width=True)

    if not REMBG_AVAILABLE:
        st.info("To get actual background removal, please install `rembg` using `pip install rembg` in your terminal.")
