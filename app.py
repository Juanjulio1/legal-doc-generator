
import streamlit as st
from openai import.
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Legal Document Generator", page_icon="📄")

# Secure API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Sidebar ---
st.sidebar.title("📚 Legal Categories")
category = st.sidebar.radio("Choose a category:", [
    "Real Property Law",
    "Corporation Law",
    "Immigration Law",
    "Family Law",
    "Will & Trust",
    "Litigation documents"
])
# --- Document Selection Based on Category ---
if category == "Contract":
    st.header("You are requesting a tailored contract")
    st.write("Please enter the contract details below.")

    with st.form("contract_form"):
        party_a = st.text_input("Name of Party A")
        party_b = st.text_input("Name of Party B")
        contract_price = st.text_input("Contract Price")
        deadline = st.text_input("Deadline for Performance")
        delivery_place = st.text_input("Delivery Place")
        additional_provisions = st.text_area("Additional Provisions (Optional)")
        submitted = st.form_submit_button("Generate Contract")

    # Prepare prompt with placeholders for missing values
    def placeholder(value, field):
        return value if value.strip() else f"[TO BE FILLED BY CLIENT: {field}]"

    if submitted:
        st.info("Generating your contract document... Please wait.")
        prompt = f"""
        Please draft a professional contract with the following details:
        - Party A: {placeholder(party_a, 'Name of Party A')}
        - Party B: {placeholder(party_b, 'Name of Party B')}
        - Contract Price: {placeholder(contract_price, 'Contract Price')}
        - Deadline for Performance: {placeholder(deadline, 'Deadline for Performance')}
        - Delivery Place: {placeholder(delivery_place, 'Delivery Place')}
        - Additional Provisions: {additional_provisions if additional_provisions.strip() else '[PARTIES MAY ADD EXTRA PROVISIONS HERE]'}
        Please insert [TO BE FILLED BY CLIENT: ____] for any information that is not provided.
        At the end of the contract, include a blank section titled 'Additional Provisions' for parties to handwrite or type more terms.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal assistant generating formal legal documents."},
                {"role": "user", "content": prompt}
            ]
        )

        legal_doc = response.choices[0].message.content

        st.success("✅ Contract Ready")
        st.text_area("Generated Contract", value=legal_doc, height=400)

# You can expand for other categories in a similar way
elif category == "Lease":
    st.header("You are requesting a tailored lease agreement")
    st.write("Please enter the lease details below.")
    # ...form fields and logic similar to above

elif category == "Will":
    st.header("You are requesting a tailored will")
    st.write("Please enter the required details below.")
    # ...form fields and logic similar to above

else:
    st.header("Please select a category to begin.")
