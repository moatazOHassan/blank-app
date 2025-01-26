import streamlit as st
from streamlit_drag_and_drop import drag_and_drop
import json

# Initialize session state variables
if 'services' not in st.session_state:
    st.session_state.services = {}
if 'current_service' not in st.session_state:
    st.session_state.current_service = None
if 'workflows' not in st.session_state:
    st.session_state.workflows = {}
if 'forms' not in st.session_state:
    st.session_state.forms = {}
if 'workflow_elements' not in st.session_state:
    st.session_state.workflow_elements = []

# Function to reset session state for new service
def reset_service_state():
    st.session_state.current_service = None
    st.session_state.workflow_elements = []

# Sidebar navigation
st.sidebar.title("Low-Code Studio")
option = st.sidebar.selectbox(
    "Select an option",
    ("Home", "Create Service", "Design Workflow", "Build Form", "View Services")
)

# Home Page
if option == "Home":
    st.title("Welcome to the Low-Code Studio")
    st.write("Use the sidebar to navigate through the studio.")

# Create Service Page
elif option == "Create Service":
    st.title("Create a New Service")

    with st.form("service_form"):
        service_name = st.text_input("Service Name")
        service_description = st.text_area("Service Description")
        submitted = st.form_submit_button("Create Service")

    if submitted:
        if service_name:
            st.session_state.services[service_name] = {
                'description': service_description,
                'workflow': None,
                'form': None
            }
            st.success(f"Service '{service_name}' created successfully.")
            st.session_state.current_service = service_name
        else:
            st.error("Please provide a service name.")

# Design Workflow Page
elif option == "Design Workflow":
    st.title("Design Workflow")

    if st.session_state.services:
        service_names = list(st.session_state.services.keys())
        service_choice = st.selectbox("Select a service to attach the workflow", service_names)
        st.session_state.current_service = service_choice

        st.subheader(f"Designing workflow for '{service_choice}'")

        # Workflow elements
        elements = ["Start", "Task", "Decision", "End"]
        selected_element = st.selectbox("Add Element", elements)
        if st.button("Add Element to Workflow"):
            st.session_state.workflow_elements.append(selected_element)

        # Display current workflow
        st.write("Current Workflow:")
        st.write(" -> ".join(st.session_state.workflow_elements))

        # Save Workflow
        if st.button("Save Workflow"):
            st.session_state.workflows[service_choice] = st.session_state.workflow_elements.copy()
            st.session_state.services[service_choice]['workflow'] = st.session_state.workflow_elements.copy()
            st.success("Workflow saved successfully.")
    else:
        st.warning("No services available. Please create a service first.")

# Build Form Page
elif option == "Build Form":
    st.title("Build Form")

    if st.session_state.services:
        service_names = list(st.session_state.services.keys())
        service_choice = st.selectbox("Select a service to attach the form", service_names)
        st.session_state.current_service = service_choice

        st.subheader(f"Designing form for '{service_choice}'")

        # Form elements
        form_elements = {
            "Text Input": st.text_input,
            "Text Area": st.text_area,
            "Number Input": st.number_input,
            "Date Input": st.date_input,
            "Checkbox": st.checkbox,
            "Select Box": st.selectbox,
            "Slider": st.slider,
        }
        element_types = list(form_elements.keys())
        selected_form_element = st.selectbox("Add Form Element", element_types)
        field_label = st.text_input("Field Label")
        if st.button("Add Element to Form"):
            if 'form_fields' not in st.session_state:
                st.session_state.form_fields = []
            st.session_state.form_fields.append({
                'type': selected_form_element,
                'label': field_label
            })

        # Display current form fields
        st.write("Current Form Fields:")
        for idx, field in enumerate(st.session_state.get('form_fields', [])):
            st.write(f"{idx + 1}. {field['type']} - {field['label']}")

        # Save Form
        if st.button("Save Form"):
            st.session_state.forms[service_choice] = st.session_state.form_fields.copy()
            st.session_state.services[service_choice]['form'] = st.session_state.form_fields.copy()
            st.success("Form saved successfully.")
    else:
        st.warning("No services available. Please create a service first.")

# View Services Page
elif option == "View Services":
    st.title("Available Services")

    if st.session_state.services:
        for service_name, details in st.session_state.services.items():
            st.subheader(service_name)
            st.write(f"**Description:** {details['description']}")
            st.write(f"**Workflow:** {details.get('workflow', 'Not defined')}")
            st.write(f"**Form Fields:**")
            form_fields = details.get('form', [])
            if form_fields:
                for field in form_fields:
                    st.write(f"- {field['type']} - {field['label']}")
            else:
                st.write("Form not defined.")
            st.write("---")
    else:
        st.write("No services have been created yet.")
