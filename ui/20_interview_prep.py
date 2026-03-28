import streamlit as st
from ml.src.interview_data import get_suggested_questions

st.set_page_config(page_title="Interview Prep", page_icon="👔", layout="wide")

st.title("👔 Interview Preparation System")
st.markdown("Sharpen your knowledge with curated interview questions and expert-verified answers designed for elite data roles.")

c1, c2 = st.columns([1, 2], gap="large")

with c1:
    st.subheader("Session Settings")
    role = st.selectbox("Target Role", ["Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer"])
    diff = st.radio("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)
    
    # Reset limit on new fetch
    if st.button("Fetch New Questions 🔄", type="primary", use_container_width=True):
        with st.spinner("Extracting elite question pool..."):
            questions = get_suggested_questions(role, diff)
            st.session_state.interview_questions = questions
            st.session_state.current_role = role
            st.session_state.current_diff = diff
            st.session_state.display_limit = 3 # Initial limit

with c2:
    if "interview_questions" not in st.session_state:
        # Default load
        st.session_state.interview_questions = get_suggested_questions("Data Scientist", "Medium")
        st.session_state.current_role = "Data Scientist"
        st.session_state.current_diff = "Medium"
        st.session_state.display_limit = 3

    qs = st.session_state.interview_questions
    limit = st.session_state.display_limit
    
    st.subheader(f"Results: {st.session_state.current_role} [{st.session_state.current_diff}]")
    
    # Display subset of questions
    for i in range(min(len(qs), limit)):
        item = qs[i]
        with st.container(border=True):
            st.markdown(f"**Q{i+1}: {item['question']}**")
            with st.expander("👁️ View Expert Answer"):
                st.info(item['answer'])
                
    # Show More Button
    if limit < len(qs):
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load More Questions ➕", key="load_more", use_container_width=True):
            st.session_state.display_limit += 3
            st.rerun()
                
    st.divider()
    st.markdown("#### 💡 Pro Tip: STAR Method")
    st.write("When answering behavioral or scenario-based questions (Medium/Hard), use the **Situation, Task, Action, Result** framework to provide structured, data-driven responses.")

with st.sidebar:
    st.divider()
    st.subheader("Resource Deep Dives")
    st.markdown("""
    - [Explainability (SHAP)](/AI_Explainability)
    - [Market Comparison](/Trend_Comparison)
    - [Ethical AI Limits](/Ethical_AI_&_Limits)
    """)
