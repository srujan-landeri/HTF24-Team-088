import streamlit as st
import requests
import validators
from typing import Optional
from urllib.parse import urlencode

def validate_inputs(question: str, url: str) -> tuple[bool, Optional[str]]:
    """Validate user inputs and return (is_valid, error_message)"""
    if not question.strip():
        return False, "Please enter a question"
    if len(question) > 500:
        return False, "Question is too long (max 500 characters)"
    if not url.strip():
        return False, "Please enter a URL"
    if not validators.url(url):
        return False, "Please enter a valid URL"
    return True, None

def main():
    st.set_page_config(
        page_title="Article Q&A System",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom CSS for better styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .success-message {
            padding: 1rem;
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        .error-message {
            padding: 1rem;
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        .stSpinner {
            text-align: center;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Article Q&A System")
    
    with st.form("qa_form"):
        question = st.text_input(
            "Enter your question:",
            max_chars=500,
            help="Ask a specific question about the article content"
        )
        url = st.text_input(
            "Enter the article URL:",
            help="Paste the full URL of the article you want to analyze"
        )
        use_groq = st.checkbox(
            "Use Groq API",
            value=True,
            help="Toggle between Groq (faster) and Ollama (local) processing"
        )
        
        submitted = st.form_submit_button("Get Answer")
        
        if submitted:
            # Validate inputs
            is_valid, error_message = validate_inputs(question, url)
            
            if not is_valid:
                st.error(error_message)
            else:
                with st.spinner("Processing your request... This may take a few moments."):
                    try:
                        # Construct the endpoint URL with query parameters
                        base_url = "http://localhost:8000"
                        endpoint = "/chat_groq" if use_groq else "/chat"
                        params = urlencode({
                            "question": question,
                            "url": url
                        })
                        full_url = f"{base_url}{endpoint}?{params}"
                        
                        # Make the request
                        # Replace the existing request code in the Streamlit app with this:
                        response = requests.post(
                            f"{base_url}{endpoint}",
                            json={
                                "question": question,
                                "url": url
                            },
                            timeout=60
                        )   
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Response generated successfully!")
                            
                            # Display the answer in a nice format
                            st.markdown("### Answer")
                            st.markdown(result["answer"])
                            
                            # Add metadata if available
                            if "metadata" in result:
                                with st.expander("Response Metadata"):
                                    st.json(result["metadata"])
                        else:
                            error_detail = response.json().get("detail", "Unknown error occurred")
                            st.error(f"❌ Error: {error_detail}")
                            
                    except requests.exceptions.Timeout:
                        st.error("⏰ Request timed out. The article might be too long or the server might be busy. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Could not connect to the server. Please check if the API is running on localhost:8000")
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred: {str(e)}")

    # Add helpful information
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Enter your question about the article
        2. Paste the URL of the article you want to analyze
        3. Choose whether to use Groq (cloud API) or Ollama (local processing)
        4. Click 'Get Answer' to receive your response
        
        **Tips:**
        - Make sure the article URL is accessible and contains readable content
        - Be specific with your questions for better results
        - If using Groq, responses will typically be faster but require an API key
        - If using Ollama, processing is done locally but might take longer
        """)
    
    # Add footer
    st.markdown("---")
    st.markdown(
        "Made with ❤️ using Streamlit | "
        "Using Groq and Ollama for text processing | "
        "Powered by FastAPI backend",
        help="Backend running on localhost:8000"
    )

if __name__ == "__main__":
    main()