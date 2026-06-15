import streamlit as st
import yaml
import os
import datetime
import shutil

# Basic Config
st.set_page_config(page_title="CVFoundry-Lite", page_icon="📄", layout="wide")

# Constants
CANONICAL_FILE = "CVFoundry-Lite-Canonical.yml"
BACKUP_DIR = "tmp/backups"
TEMPLATES = [f for f in os.listdir(".") if f.endswith(".j2")]

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_file(filepath):
    ensure_backup_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{os.path.basename(filepath)}.{timestamp}.bak")
    shutil.copy2(filepath, backup_path)
    return backup_path

# UI Header
st.title("📄 CVFoundry-Lite")
st.markdown("**Lightweight Markdown/Jinja-based Resume Generator**")

# Layout: About First, Tabs Second
tab_about, tab_workbench, tab_templates, tab_deconstructor = st.tabs(["About", "Workbench", "Templates", "Deconstructor"])

with tab_about:
    st.header("About this Foundry")
    st.markdown("""
    **What this Foundry does:**
    CVFoundry-Lite is a streamlined framework for maintaining a single "canonical" representation of a professional profile (in YAML), and then rendering it out to various tailored formats using Jinja2 templates.

    **What goes in and what comes out:**
    - **In:** `CVFoundry-Lite-Canonical.yml` (Your single source of truth for your resume)
    - **In:** `.j2` templates for specific outputs (e.g., standard resume, one-pager)
    - **Out:** Rendered `.html` and `.md` outputs tailored to specific roles.

    **Who uses it and when:**
    Users who want a fully version-controllable, plain-text resume that can be easily customized without maintaining multiple separate word documents.

    **How to run it locally:**
    Use `python CVFoundry-Lite-Build.py` or run `build.sh`.

    **Where outputs are written:**
    Outputs are typically written to the root directory as `.html` files.
    """)

with tab_workbench:
    st.header("Workbench: Edit Canonical CV")
    st.markdown("Modify the single source of truth for your professional profile.")
    
    if os.path.exists(CANONICAL_FILE):
        with open(CANONICAL_FILE, "r") as f:
            current_content = f.read()
            
        edit_mode = st.toggle("Enable Editing", value=False, help="Unlock the canonical CV for editing. Will create a backup on save.")
        
        if edit_mode:
            new_content = st.text_area("Canonical YAML", value=current_content, height=600)
            if st.button("Save Changes", type="primary"):
                try:
                    # Validate YAML
                    yaml.safe_load(new_content)
                    
                    # Backup and save
                    backup_path = backup_file(CANONICAL_FILE)
                    with open(CANONICAL_FILE, "w") as f:
                        f.write(new_content)
                        
                    st.success(f"Saved successfully! Backup created at `{backup_path}`")
                    st.toast("Canonical CV updated!")
                except yaml.YAMLError as exc:
                    st.error(f"Invalid YAML format. Please fix errors before saving.\n\nError details: {exc}")
        else:
            st.code(current_content, language="yaml")
    else:
        st.error(f"Canonical file `{CANONICAL_FILE}` not found.")

with tab_templates:
    st.header("Templates")
    st.markdown("View available Jinja2 (`.j2`) templates.")
    
    if TEMPLATES:
        selected_template = st.selectbox("Select a template to view:", TEMPLATES)
        if selected_template and os.path.exists(selected_template):
            with open(selected_template, "r") as f:
                template_content = f.read()
            st.code(template_content, language="jinja2")
    else:
        st.info("No Jinja2 templates found in the repository.")

with tab_deconstructor:
    st.header("Template Deconstructor (Beta)")
    st.markdown("Provide a sample resume format you like, and we will deconstruct it to generate a new `.j2` template.")
    
    sample_text = st.text_area("Paste sample resume text/markdown here:", height=300, help="Paste the text of the resume you want to mimic.")
    template_name = st.text_input("New Template Name", value="Custom-Template")
    
    if st.button("Generate Template", type="primary"):
        if not sample_text.strip():
            st.error("Please provide some sample text to deconstruct.")
        else:
            st.info("This feature is currently a placeholder. In the future, this will dispatch a request to Prompt-Foundry or LLM-Registry to analyze the sample text and synthesize a working Jinja2 (`.j2`) layout mimicking the structure, using `CVFoundry-Lite-Canonical.yml` data fields.")
            
            # Placeholder for saving
            demo_j2_path = f"{template_name}.j2"
            with open(demo_j2_path, "w") as f:
                f.write("{# Auto-generated template based on sample #}\n<html>\n<body>\n  <h1>{{ personal.name }}</h1>\n  <!-- Generated layout goes here -->\n</body>\n</html>")
            st.success(f"Generated placeholder template `{demo_j2_path}`. You can now use this as a `--template` argument in the builder.")
