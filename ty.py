import streamlit as st
from openai import OpenAI
import os
from PIL import Image

# Initialize session state for points and credits
if 'points' not in st.session_state:
    st.session_state['points'] = 0
if 'credits' not in st.session_state:
    st.session_state['credits'] = 0

# Set up OpenAI API key
openai.api_key = ''

def save_uploaded_file(uploadedfile):
    try:
        with open(os.path.join("uploaded_images", uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return True
    except Exception as e:
        return False

def generate_description(item_name):
    try:
        response = openai.chat.Completion.create(
          model="gpt-3.5-turbo",  # Adjust this model name as necessary based on availability
          prompt=f"Generate a catchy description for an item named {item_name}, used for selling old furniture and tech.",
          max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Failed to generate description due to error: {str(e)}"

def add_points(action):
    if action == 'list':
        st.session_state.points += 25
    elif action == 'sell':
        st.session_state.points += 50
    elif action == 'buy':
        st.session_state.points += 50
    
    # Update credits if points exceed 500
    if st.session_state.points >= 500:
        st.session_state.credits += 25
        st.session_state.points -= 500

def app_header():
    st.title("EcoFurni - Furniture and Tech Recycling")
    st.write("List your old items, earn points, and get credits!")
    st.write(f"Points: {st.session_state.points}, Credits: ${st.session_state.credits}")

def main():
    app_header()
    with st.form("Item Form"):
        item_name = st.text_input("Item Name")
        item_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
        submit_button = st.form_submit_button("Generate Description")
        
        if submit_button and item_name:
            item_description = generate_description(item_name)
            st.text_area("Item Description", value=item_description, height=150, disabled=True)

        if item_description and item_image and st.button("Save Item"):
            if save_uploaded_file(item_image):
                add_points('list')
                st.success("Item listed successfully!")
            else:
                st.error("Failed to save item.")
    
    # Display all items
    st.subheader("Listed Items")
    for filename in os.listdir("uploaded_images"):
        image_path = os.path.join("uploaded_images", filename)
        image = Image.open(image_path)
        st.image(image, caption=filename.split('.')[0], width=300)
        st.write("---")

if __name__ == "__main__":
    if not os.path.exists('uploaded_images'):
        os.makedirs('uploaded_images')
    main()
