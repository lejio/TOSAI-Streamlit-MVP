import streamlit as st
import json
from src.parser import Parser

# Load the JSON data (Replace with actual file loading if needed)
json_data = {
  "privacyAgreement": {
    "id": "privacy_agreement",
    "category": "Privacy Agreement",
    "componentType": "section",
    "children": [
      {
        "id": "personal_information_collection",
        "category": "Personal Information Collection",
        "componentType": "section",
        "children": [
          {
            "id": "registration",
            "category": "Registration",
            "componentType": "checkboxGroup",
            "children": [
              { "id": "email", "category": "Email", "componentType": "checkbox" },
              { "id": "username", "category": "Username", "componentType": "checkbox" },
              { "id": "password", "category": "Password", "componentType": "checkbox" }
            ]
          },
          {
            "id": "personal_details",
            "category": "Personal Details",
            "componentType": "checkboxGroup",
            "children": [
              { "id": "dob", "category": "Date of Birth", "componentType": "checkbox" },
              { "id": "phone", "category": "Phone Number", "componentType": "checkbox" },
              { "id": "address", "category": "Address", "componentType": "checkbox" }
            ]
          },
          {
            "id": "payment_subscription",
            "category": "Payment/Subscription",
            "componentType": "sliderGroup",
            "children": [
              {
                "id": "credit_card",
                "category": "Credit Card",
                "componentType": "slider",
                "options": [
                  "I do not want to share my card details",
                  "I will share my card details but do not want them stored",
                  "I will share my card details, but only the last 4 digits should be stored",
                  "I am okay with my full card details being stored"
                ]
              }
            ]
          },
          {
            "id": "regulation",
            "category": "Regulation",
            "componentType": "checkboxGroup",
            "children": [
              {
                "id": "identification_document",
                "category": "Identification Document",
                "componentType": "checkbox"
              }
            ]
          },
          {
            "id": "providing_service",
            "category": "Providing Service",
            "componentType": "sliderGroup",
            "children": [
              {
                "id": "location",
                "category": "Location",
                "componentType": "slider",
                "options": [
                  "Do not share my location",
                  "Share an approximate location",
                  "Share my precise location but ask every time",
                  "Always share my precise location"
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "personal_information_usage",
        "category": "Personal Information Usage",
        "componentType": "section",
        "children": [
          {
            "id": "providing_service_usage",
            "category": "Providing Service",
            "componentType": "checkboxGroup",
            "children": [
              { "id": "administering_website", "category": "Administering Website", "componentType": "checkbox" },
              { "id": "communication", "category": "Communication", "componentType": "checkbox" }
            ]
          },
          {
            "id": "trackers",
            "category": "Trackers",
            "componentType": "checkboxGroup",
            "children": [
              { "id": "third_party_cookies", "category": "3rd Party Cookies", "componentType": "checkbox" },
              { "id": "cookies", "category": "Cookies", "componentType": "checkbox" },
              { "id": "web_beacons", "category": "Web Beacons", "componentType": "checkbox" }
            ]
          },
          {
            "id": "personalization",
            "category": "Personalization",
            "componentType": "checkbox"
          },
          {
            "id": "advertisement",
            "category": "Advertisement",
            "componentType": "checkbox"
          }
        ]
      }
    ]
  }
}


# Initialize session state for form persistence
if "pref_tree" not in st.session_state:
    st.session_state.pref_tree = {}

# Recursive function to render form elements from JSON
def render_form(data, form_values):
    """Recursively render form elements from JSON"""
    
    # Render headers ONLY for sections and groups
    if data["componentType"] in ["section", "checkboxGroup", "sliderGroup"]:
        st.subheader(data["category"])  

    if "children" in data:
        for child in data["children"]:
            render_form(child, form_values)  # Recursively render children

    elif "componentType" in data:
        # Only render the input element, NOT a subheader
        key = f"pref_{data['id']}"

        if data["componentType"] == "checkbox":
            form_values[data["id"]] = st.checkbox(
                data["category"],
                value=st.session_state.pref_tree.get(data["id"], False),
                key=key
            )

        elif data["componentType"] == "slider":
            form_values[data["id"]] = st.select_slider(
                data["category"],
                options=data["options"],
                value=st.session_state.pref_tree.get(data["id"], data["options"][0]),
                key=key
            )


st.title("TOSAI MVP 1")

with st.form("user_prefs_form"):
    pref_tree = {}
    render_form(json_data["privacyAgreement"], pref_tree)
    
    submitted = st.form_submit_button("Save Preferences")

    if submitted:
        st.session_state.pref_tree = pref_tree  # Persist choices
        st.json(pref_tree)  # Show output inside form

devTxt = st.text(json.dumps(pref_tree, indent=2))

txt = st.text_area("Paste legal document", height=1000)

if st.button("Parse"):

  if txt:
    parser = Parser()
    parsed_data = parser.parse_text(txt)

    st.json(parsed_data)
  else:
    st.error("Please paste a legal document to parse.")

st.divider()