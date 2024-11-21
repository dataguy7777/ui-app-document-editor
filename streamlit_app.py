import streamlit as st

# Define initial structure
document_structure = {
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

# Function to display document structure
def display_structure(structure, parent_key=""):
    for key, value in structure.items():
        if isinstance(value, dict):  # Section with sub-sections
            with st.expander(f"{parent_key}{key}"):
                display_structure(value, parent_key=f"{parent_key}{key} > ")
        else:  # Paragraphs
            for paragraph in value:
                st.markdown(f"- **{parent_key}{key}**: {paragraph}")

# Function to edit document
def edit_structure(structure, parent_key=""):
    updated_structure = {}
    for key, value in structure.items():
        if isinstance(value, dict):  # Section with sub-sections
            with st.expander(f"Edit {key}"):
                updated_structure[key] = edit_structure(value)
        else:  # Paragraphs
            updated_paragraphs = []
            st.subheader(f"Edit Section: {parent_key}{key}")
            for i, paragraph in enumerate(value):
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    updated_paragraph = st.text_input(
                        f"Edit Paragraph {i+1}", value=paragraph, key=f"{parent_key}{key}-{i}"
                    )
                    updated_paragraphs.append(updated_paragraph)
                with col2:
                    if st.button(f"Remove {i+1}", key=f"remove-{parent_key}{key}-{i}"):
                        updated_paragraphs.pop()
                with col3:
                    if st.button(f"AI Suggest {i+1}", key=f"ai-{parent_key}{key}-{i}"):
                        ai_prompt = st.text_input(
                            f"Enter AI Prompt for {key} - Paragraph {i+1}", value=""
                        )
                        if ai_prompt:
                            updated_paragraphs[i] = f"AI Response to '{ai_prompt}'"  # Placeholder for AI logic
            if st.button(f"Add Paragraph to {key}", key=f"add-{parent_key}{key}"):
                updated_paragraphs.append("New Paragraph")
            updated_structure[key] = updated_paragraphs
    return updated_structure

# Streamlit App
st.title("Document Editing App")
st.sidebar.header("Document Interaction")
action = st.sidebar.radio("Choose Action", ["View Document", "Edit Document", "Add Section"])

if action == "View Document":
    st.header("Document Structure")
    display_structure(document_structure)

elif action == "Edit Document":
    st.header("Edit Document Structure")
    document_structure = edit_structure(document_structure)
    st.success("Document updated successfully!")

elif action == "Add Section":
    st.header("Add New Section")
    new_section = st.text_input("Section Name", key="new-section")
    if new_section and st.button("Add Section"):
        document_structure[new_section] = []
        st.success(f"Section '{new_section}' added!")
