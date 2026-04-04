import streamlit as st
import requests
from app import page_header

st.set_page_config(page_title="Download Report", page_icon="📄", layout="wide")

page_header("Documentation", "Generate Output Report", "Aggregate your personalized AI predictions into a clean, downloadable PDF report.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to generate a report.")
    st.stop()

st.markdown("### Report Parameters")
st.markdown("Confirm the details you want to inject into your official PDF export.")

# Use defaults aligned to generic examples in case DB history is empty
with st.form("report_form"):
    user_name = st.text_input("Name", value=st.session_state.username)
    job_title = st.text_input("Target Role", value="Data Scientist")
    predicted_salary = st.text_input("Predicted Salary Benchmark", value="$125,000 USD")
    
    # Input CSV styles for lists
    skills_raw = st.text_area("High-ROI Skills (comma separated)", value="Python, SQL, PyTorch, Cloud Architecture")
    roadmap_raw = st.text_area("Career Milestones (comma separated)", value="Master MLOps paradigms, Scale backend architectures, Transition to Lead Data Scientist")
    
    submit = st.form_submit_button("Generate PDF", type="primary")

if submit:
    skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
    roadmap_list = [r.strip() for r in roadmap_raw.split(",") if r.strip()]
    
    payload = {
        "user_name": user_name,
        "job_title": job_title,
        "predicted_salary": predicted_salary,
        "skills": skills_list,
        "roadmap": roadmap_list
    }
    
    with st.spinner("Compiling PDF bytes in-memory via ReportLab..."):
        try:
            # We call the FastAPI backend to securely generate and stream the PDF
            # URL assumes local usage standard for this project (FastAPI on 8000)
            # If standard backend isn't up during Streamlit dev, we fallback to direct function usage.
            
            # For reliability during synchronous Streamlit standalone execution, we'll invoke the python module natively:
            from api.report import create_pdf_report, ReportRequest
            req = ReportRequest(**payload)
            pdf_bytes = create_pdf_report(req).getvalue()
            
            st.success("Report successfully generated!")
            
            st.download_button(
                label="⬇️ Download Official Salary Report (PDF)",
                data=pdf_bytes,
                file_name=f"Career_Report_{user_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error generating PDF report: {e}")
