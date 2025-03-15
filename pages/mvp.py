import streamlit as st
import json
from src.parser import Parser

# Load the JSON data (Replace with actual file loading if needed)
json_data = json.loads(open("config.json").read())

# Initialize session state for form persistence
if "pref_tree" not in st.session_state:
    st.session_state.pref_tree = {}

# Recursive function to render form elements from JSON
def render_form(form, data, form_values, level=0):
    """Recursively render form elements from JSON"""
    
    # Render headers ONLY for sections and groups
    if data["componentType"] in ["section", "checkboxGroup", "sliderGroup"]:
        form.markdown(f"<h{min(6, level+2)}>{data['category']}</h{min(6, level+2)}>", unsafe_allow_html=True, help=data.get("hint", None))

    if "children" in data:
        for child in data["children"]:
            render_form(form, child, form_values, level + 1)  # Recursively render children

    elif "componentType" in data:
        # Only render the input element, NOT a subheader
        key = f"pref_{data['id']}"

        if data["componentType"] == "checkbox":
            form_values[data["id"]] = form.checkbox(
                data["category"],
                value=st.session_state.pref_tree.get(data["id"], False),
                key=key
            )

        elif data["componentType"] == "slider":
            slider = form.select_slider(
                data["category"],
                options=data["options"],
                value=st.session_state.pref_tree.get(data["id"], data["options"][0]),
                key=key
            )
            form_values[data["id"]] = slider

# Add a note to the sidebar
st.sidebar.markdown(
  """
  **Note:** Choose your preferences for each section below where you feel comfortable sharing your data.
  """
)

# set sidebar width
st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: 90%;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("TOSSY")

# description
st.markdown(
    """
    TOSSY is a tool that helps you understand the privacy policies of websites, apps, and other services. 
    It allows you to paste a legal document and parses it to show the key points in the document that differ from your preferences (assumptions and expectations).
    """
)

# with st.sidebar.form("user_prefs_form"):
form = st.sidebar.form("user_prefs_form")
pref_tree = {}
render_form(form, json_data["privacyAgreement"], pref_tree)

submitted = form.form_submit_button("Save Preferences")

if submitted:
    st.session_state.pref_tree = pref_tree  # Persist choices
    st.sidebar.json(pref_tree)  # Show output inside form

# devTxt = st.text(json.dumps(pref_tree, indent=2))

txt = st.text_area("Paste legal document", height=1000)

if st.button("Parse"):

  if txt:
    parser = Parser()
    parsed_data = parser.parse_text(txt)

    st.json(parsed_data)
  else:
    st.error("Please paste a legal document to parse.")

st.divider()