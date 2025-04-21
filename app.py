import streamlit as st
from openai import OpenAI

st.title("🧪 Test Version – Updated via GitHub")

# Secure API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Sidebar ---
st.sidebar.title("📚 Legal Categories")
category = st.sidebar.selectbox("Choose a category:", [
    "Real Property Law",
    "Corporation Law",
    "Immigration Law",
    "Family Law",
    "Will & Trust"
    "Litigation documents"
])

# --- Document Selection Based on Category ---
if category == "Real Property Law":
    doc_type = st.selectbox("Select document type:", ["Contract of Sale-Cooperative","Contract of Sale-Condo","Residential Contract of Sale","Rider to Contract of Sale" "Deed of Sale", "Lease Agreement", "Lease Amendment"])
elif category == "Corporation Law":
    doc_type = st.selectbox("Select document type:", ["Operating Agreement","ByLaw", "Article","Shareholder Agreement","Resolution"])
elif category == "Immigration Law":
    doc_type = st.selectbox("Select document type:", ["Visa application","Greencard Application", "Naturalization"])
elif category == "Family Law":
    doc_type = st.selectbox("Select document type:", ["Adoption","Divorce", "Name Change"])
elif category == "Will & Trust":
    doc_type = st.selectbox("Select document type:", ["Last Will and Testament", "Revocable Trust","Revocable Trust", "Healthcare Derivative", "Power of Attorney"])

# --- User Form ---
with st.form("doc_form"):
    name = st.text_input("Client's Full Name")
    address = st.text_input("Client's Address")
    submitted = st.form_submit_button("Generate Document")

# Extra fields based on document type
if doc_type == "Lease Agreement":
    property_address = st.text_input("Property Address")
    term = st.text_input("Lease Term")
    rent = st.text_input("Monthly Rent")
    effective_date = st.text_input("Effective Date")
    governing_law = st.text_input("Governing Law (State or Jurisdiction)")
elif doc_type == "Contract":
    party_a = st.text_input("Party A")
    party_b = st.text_input("Party B")
    agreement_subject = st.text_area("Purpose of Contract")
    effective_date = st.text_input("Effective Date")
    governing_law = st.text_input("Governing Law (State or Jurisdiction)")
elif doc_type == "Last Will and Testment":
    beneficiaries = st.text_area("List of Beneficiaries")
    executor = st.text_input("Executor's Name")
    governing_law = st.text_input("Governing Law (State or Jurisdiction)")

    submitted = st.form_submit_button("Generate Document")

# --- Process & Generate Document ---
if submitted:
    with st.spinner("Generating your legal document..."):

        # Start the prompt
        prompt = f"""
        Please generate a professional {doc_type} in the category of {category}.
        Client Name: {name}
        Client Address: {address}
        """
	    
        # Add more prompt content based on document type
        if doc_type == "Lease Agreement":
            prompt += f"""
            Property Address: {property_address}
            Lease Term: {term}
            Monthly Rent: {rent}
            """
        elif doc_type == "Last Will and Testment":
            prompt += f"""
            Beneficiaries: {beneficiaries}
            Executor: {executor}
            """

        # Call OpenAI API
	    
        response = client.chat.completions.create(
            model="gpt4",
            messages=[
                {"role": "system", "content": "You are a legal assistant generating formal legal documents."},
                {"role": "user", "content": prompt}
            ]
        )

        legal_doc = response.choices[0].message.content

        # Display result
        st.success("✅ Document Ready")
        st.text_area("Legal Document", value=legal_doc, height=400)
