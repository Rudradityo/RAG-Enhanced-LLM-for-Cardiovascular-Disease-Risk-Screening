import streamlit as st
import requests

# Inject CSS
st.markdown(
    """
    <style>
        
    .stTextArea textarea {
        min-height: 60px;
        line-height: 1.5;
        box-sizing: border-box;
        resize: vertical; /* Allow vertical resizing */
        padding-top: 5px; /* Add top padding to the textarea */
        padding-bottom: 5px; /* Add bottom padding to the textarea */
    }
    .stTextArea {
        height: auto !important;
    }
    .stTextArea textarea::placeholder {
        color: #aaa; /* Lighter gray for placeholder */
        font-size: 0.9em; /* Slightly smaller font for placeholder */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Cardiovascular Disease Risk Screener")

# Disclaimer
welcome_message_html = """
<div style="padding: 1px 0;">
    <p style="font-style: italic; margin-bottom: 2px;">This tool is for screening purposes only and does not provide a diagnosis.</p>
    <p style="font-style: italic;">Consult with a healthcare professional for further evaluation.</p>
</div>
"""

st.markdown(welcome_message_html, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
st.subheader("Patient Case Details")
st.write("Please enter the patient's case details below and click **Submit** to receive risk screening result.")

# Placeholder Text
patient_case_details_placeholder = "A 50-year-old male with a height of 168 cm and weight of 62.0 kg has a systolic blood pressure of 110 mm Hg and diastolic blood pressure of 80 mm Hg. His cholesterol level is normal, and glucose is normal. He does not smoke, does not consume alcohol, and is physically active."


if "user_input" not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area(
    label="patient_case_details",
    placeholder=patient_case_details_placeholder,
    value=st.session_state.user_input,
    key="patient_case_details", # Give the text area a unique key
    label_visibility="collapsed"
    )



if st.button("Submit"):  # The submit button

    prompt = st.session_state.user_input # Get the value from the text area

    if prompt: # Check if the prompt is not empty
        
        print(f"Prompt in app.py:\n{prompt}\n")
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Send input to FastAPI endpoint
        try:
            response = requests.post("http://127.0.0.1:8000/process/", json={"query": prompt}, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            response_data = response.json()
            
            print(f"Response Data in app.py:\n{response_data}\n")
            
            assistant_response = response_data.get("response", "No response received from the API.")
        except requests.exceptions.RequestException as e:
            assistant_response = f"Error communicating with the API: {e}"
            st.error(assistant_response)  # Display the error in Streamlit

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
        print(f"Assistant Response in app.py:\n{assistant_response}\n")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})