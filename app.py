import streamlit as st
from openai import OpenAI

# Set up the OpenAI client with your API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app UI
st.title("📄 Legal Document Generator")
st.subheader("Create custom legal documents for your clients")

# Input form
with st.form("legal_form"):
    name = st.text_input("Client's Full Name")
    address = st.text_area("Client's Address")
    request = st.text_area("Describe the legal request (e.g., NDA, lease, etc.)")

    submitted = st.form_submit_button("Generate Document")

if submitted:
    with st.spinner("Generating document..."):
        prompt = f"""
        Please generate a professional legal document.

        Client Name: {name}
        Client Address: {address}
        Request: {request}

        Format with a header, body, and appropriate closing.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        legal_doc = response.choices[0].message.content

        st.success("✅ Document generated!")
        st.markdown("### 📝 Output:")
        st.text_area("Legal Document", value=legal_doc, height=400)
