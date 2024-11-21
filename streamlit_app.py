import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
import json

# Initialize session state for document structure
if 'document_structure' not in st.session_state:
    st.session_state.document_structure = {
        "INTRODUZIONE": ["Management Summary", "Policy | Sistema Normativo Introduzione"],
        "LINEE FONDAMENTALI": {
            "A.1 PRINCIPI DI RIFERIMENTO": [
                "Principi di riferimento del Sistema Normativo",
                "Policy | Sistema Normativo Linee Fondamentali"
            ],
            "A.2 ARCHITETTURA E STRUMENTI": [
                "Policy | Sistema Normativo Linee Fondamentali"
            ]
        }
    }

# Function to convert the nested dictionary to a list for AgGrid
def dict_to_list(structure, parent=""):
    rows = []
    for key, value in structure.items():
        if isinstance(value, dict):
            rows.append({"Section": parent + key, "Type": "Section"})
            rows.extend(dict_to_list(value, parent + key + " > "))
        else:
            for para in value:
                rows.append({"Section": parent + key, "Type": "Paragraph", "Content": para})
    return rows

# Function to display the document structure using AgGrid
def display_structure_grid(structure):
    data = dict_to_list(structure)
    df = pd.DataFrame(data)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False, sortable=True, filter=True)
    gridOptions = gb.build()
    
    st.subheader("📑 Document Structure")
    AgGrid(
        df,
        gridOptions=gridOptions,
        height=400,
        update_mode=GridUpdateMode.NO_UPDATE,
        allow_unsafe_jscode=True,
    )

# Function to edit the document structure
def edit_structure_ui(structure, parent_key=""):
    updated_structure = {}
    for key, value in structure.items():
        if isinstance(value, dict):
            with st.expander(f"✏️ Edit Section: {parent_key}{key}", expanded=False):
                updated_structure[key] = edit_structure_ui(value, parent_key=f"{parent_key}{key} > ")
        else:
            with st.container():
                st.markdown(f"### 📝 Edit Section: {parent_key}{key}")
                paragraphs = list(value)  # Make a copy to avoid mutation issues
                for i, paragraph in enumerate(paragraphs):
                    col1, col2, col3 = st.columns([6, 1, 1])
                    with col1:
                        updated_paragraph = st.text_input(
                            f"Paragraph {i+1}",
                            value=paragraph,
                            key=f"{parent_key}{key}-para-{i}"
                        )
                        paragraphs[i] = updated_paragraph
                    with col2:
                        if st.button(f"🗑️ Remove", key=f"remove-{parent_key}{key}-{i}"):
                            paragraphs.pop(i)
                            st.experimental_rerun()
                    with col3:
                        if st.button(f"🤖 AI Suggest", key=f"ai-{parent_key}{key}-{i}"):
                            ai_prompt = st.text_input(
                                f"Enter AI Prompt for {key} - Paragraph {i+1}",
                                key=f"ai_prompt-{parent_key}{key}-{i}"
                            )
                            if ai_prompt:
                                # Placeholder for AI logic
                                ai_response = f"AI Response to '{ai_prompt}'"
                                paragraphs[i] = ai_response
                                st.success(f"AI suggested: {ai_response}")
                if st.button(f"➕ Add Paragraph to {key}", key=f"add-{parent_key}{key}"):
                    paragraphs.append("New Paragraph")
                updated_structure[key] = paragraphs
    return updated_structure

# Function to add a new section
def add_section_ui():
    with st.form(key='add_section_form'):
        st.subheader("➕ Add New Section")
        new_section_name = st.text_input("Section Name", key="new_section_name")
        parent_section = st.selectbox(
            "Select Parent Section (optional)",
            options=[""] + list(st.session_state.document_structure.keys()),
            key="parent_section_select",
            help="Leave blank to add a top-level section."
        )
        submit = st.form_submit_button("Add Section")
        if submit:
            if new_section_name.strip() == "":
                st.error("Section name cannot be empty.")
            else:
                if parent_section:
                    if parent_section in st.session_state.document_structure:
                        st.session_state.document_structure[parent_section][new_section_name] = []
                        st.success(f"Section '{new_section_name}' added under '{parent_section}'!")
                    else:
                        st.error("Selected parent section does not exist.")
                else:
                    st.session_state.document_structure[new_section_name] = []
                    st.success(f"Top-level section '{new_section_name}' added!")
                st.experimental_rerun()

# Function to save the document structure to a JSON file
def save_document():
    with st.spinner("Saving document structure..."):
        try:
            with open("document_structure.json", "w", encoding='utf-8') as f:
                json.dump(st.session_state.document_structure, f, ensure_ascii=False, indent=4)
            st.success("📂 Document structure saved successfully!")
        except Exception as e:
            st.error(f"Error saving document: {e}")

# Function to load the document structure from a JSON file
def load_document():
    try:
        with open("document_structure.json", "r", encoding='utf-8') as f:
            st.session_state.document_structure = json.load(f)
        st.success("📂 Document structure loaded successfully!")
    except FileNotFoundError:
        st.error("No saved document structure found.")
    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please check the file format.")
    except Exception as e:
        st.error(f"Error loading document: {e}")

# Streamlit App Layout
st.set_page_config(page_title="📄 Enhanced Document Editing App", layout="wide")
st.title("📄 Enhanced Document Editing App")

# Main Navigation using Tabs
tabs = st.tabs(["View Document", "Edit Document", "Add Section", "Save Document", "Load Document"])

with tabs[0]:
    display_structure_grid(st.session_state.document_structure)

with tabs[1]:
    st.header("✏️ Edit Document Structure")
    with st.form(key='edit_form'):
        st.session_state.document_structure = edit_structure_ui(st.session_state.document_structure)
        submit_button = st.form_submit_button(label='Save Changes')
        if submit_button:
            st.success("📂 Document structure updated successfully!")

with tabs[2]:
    add_section_ui()

with tabs[3]:
    save_document()

with tabs[4]:
    load_document()

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    /* Header */
    .css-1aumxhk {
        font-size: 2rem;
        text-align: center;
        color: #4B7BEC;
    }
    /* Buttons */
    .stButton>button {
        color: white;
        background-color: #4B7BEC;
    }
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #4B7BEC;
    }
    </style>
    """, unsafe_allow_html=True)
