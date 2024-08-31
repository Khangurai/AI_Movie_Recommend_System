import streamlit as st
import cohere
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from a .env file
    load_dotenv()

    # Get the Cohere API key from the environment variables
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    # Initialize the Cohere client with the API key
    co = cohere.Client(COHERE_API_KEY)

    # Create a toggle switch in the Streamlit app
    on = st.toggle("Prompt type here")

    # Check if 'response_text' and 'translate_toggle' exist in session state
    if 'response_text' not in st.session_state:
        # Initialize 'response_text' in session state if it doesn't exist
        st.session_state.response_text = ''

    if 'translate_toggle' not in st.session_state:
        # Initialize 'translate_toggle' in session state if it doesn't exist
        st.session_state.translate_toggle = False

    def translate_text_except_titles(text):
        import re
        # Find all titles within curly braces in the text (e.g., {Title})
        titles = re.findall(r'\{(.*?)\}', text)
        # Replace titles with placeholders (e.g., {})
        placeholder_text = re.sub(r'\{(.*?)\}', '{}', text)
        # Translate the non-title text from English to Burmese
        translated_text = GoogleTranslator(source='auto', target='my').translate(placeholder_text)
        # Reinsert the original titles into the translated text
        for title in titles:
            translated_text = translated_text.replace('{}', title, 1)
        return translated_text

    # If the toggle switch is turned on
    if on:
        # Create a text area for user input
        prompt = st.text_area("Prompt is activated")

        # Create a container to hold columns
        with st.container():
            # Create two columns side by side
            col1, col2 = st.columns([1, 2])

            with col1:
                # Create a button that, when clicked, generates a recommendation
                if st.button('Show Recommend'):
                    # Generate a response from the Cohere API using the prompt
                    response = co.generate(
                        model='command-xlarge-nightly',
                        prompt=prompt,
                        max_tokens=500,
                        temperature=0.9
                    )

                    # Save the response text to session state
                    st.session_state.response_text = response.generations[0].text

            # Display the response text
            if st.session_state.response_text:
                with col2:
                    # Create a toggle switch to translate the response to Burmese
                    st.session_state.translate_toggle = st.toggle("Translate Burmese",
                                                                  st.session_state.translate_toggle)

                # If the translate toggle is turned on, translate the response
                if st.session_state.translate_toggle:
                    translated_text = translate_text_except_titles(st.session_state.response_text)
                    st.write(translated_text)
                else:
                    # Otherwise, display the response text as is
                    st.write(st.session_state.response_text)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
