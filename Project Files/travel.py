import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY) 
else:
    st.error("Missing Google API Key.")

def generate_itinerary(destination, days, nights):
    """
    Interfaces with Gemini Pro to generate a travel plan.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Engineering the Prompt for high-quality output
        prompt = f"""
        You are an expert world-travel guide. 
        Create a detailed, day-wise travel itinerary for a trip to {destination}.
        Duration: {days} days and {nights} nights.
        
        Please include:
        1. A catchy title for the trip.
        2. Morning, Afternoon, and Evening activities for each day.
        3. Local dining suggestions (famous dishes or spots).
        4. Important travel tips (weather, transport, or etiquette).
        5. Use Markdown formatting with bold headings and bullet points.
        6. Tourist attractions
        """
        
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

# --- 2. STREAMLIT UI SETUP ---
def main():
    st.set_page_config(page_title="TravelGuideAI", page_icon="✈️")
    
    st.title("🌍 Travel Itinerary Generator")
    st.markdown("Explore with AI: Custom Itineraries for Your Next Journey")

    # Sidebar for additional settings (Expert Tip: Improves UX)
    with st.sidebar:
        st.header("About")
        st.info("This project generates travel itineraries based on the user inputs - destination, number of days and number of nights, the generated itinerary can be downloade as a text document")

    # User Inputs 
    destination = st.text_input("Enter your desired destination:", placeholder="e.g. Hyderabad, Coorg, London")
    days = st.number_input("Number of days:", min_value=1, max_value=30, value=1)
    nights = st.number_input("Number of nights:", min_value=0, max_value=30, value=0)

    #interests = st.text_area("Your Interests (e.g., beaches, food, adventure)")

    # Logic Execution
    if st.button("Generate Itinerary"):
        if destination.strip():
            with st.spinner(f"Mapping out your trip to {destination}..."):
                itinerary = generate_itinerary(destination, days, nights)
                
                st.subheader("Your Personalized Plan")
                # Using st.markdown instead of text_area for better readability
                st.markdown(itinerary)
                
                # Add a download button for the user
                st.download_button(
                    label="Download Itinerary as Text",
                    data=itinerary,
                    file_name=f"Itinerary_{destination}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please enter a destination to proceed.")

if __name__ == "__main__":
    main()