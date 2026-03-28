import streamlit as st
import uuid
from ml.src.predict import run_prediction
from api.database import SessionLocal
from api.models import SalaryPrediction

st.title("🤖 Salary Prediction Engine")
st.markdown("Use the advanced RandomForest / Gradient Boosting ensemble to calculate highly accurate benchmarks.")

colA, colB = st.columns([1, 2], gap="large")

with colA:
    st.subheader("Job Parameters")
    job_title = st.text_input("Job Title", value="Data Scientist")
    exp = st.selectbox("Experience Level", ["EN", "MI", "SE", "EX"], index=2)
    emp = st.selectbox("Employment Type", ["FT", "PT", "CT", "FL"], index=0)
    loc = st.text_input("Company Location", value="US")
    size = st.selectbox("Company Size", ["S", "M", "L"], index=2)
    rem = st.select_slider("Remote Ratio (%)", options=[0, 50, 100], value=100)
    skills = st.text_input("Core Skills", value="Python, SQL, Machine Learning")
    yr = st.number_input("Work Year", min_value=2020, max_value=2030, value=2024)
    predict_btn = st.button("Predict Salary 🚀", type="primary", use_container_width=True)

with colB:
    st.subheader("Intelligence Output")
    if predict_btn:
        with st.spinner("Running ensemble models..."):
            try:
                inputs = {
                    "job_title": job_title, "experience_level": exp,
                    "employment_type": emp, "company_location": loc,
                    "company_size": size, "remote_ratio": rem,
                    "skills": skills, "work_year": int(yr)
                }
                res = run_prediction(inputs, "ml/config.yaml")

                # Store prediction in DB
                try:
                    db = SessionLocal()
                    from api.models import User
                    u = db.query(User).filter(User.username == st.session_state.username).first()
                    if u:
                        sp = SalaryPrediction(
                            id=str(uuid.uuid4()),
                            user_id=u.id, job_title=job_title, experience_level=exp,
                            company_location=loc, company_size=size, remote_ratio=rem,
                            skills=skills, predicted_average=res['salary']['average'],
                            confidence_score=float(res['confidence']['score'])
                        )
                        db.add(sp)
                        db.commit()
                    db.close()
                except Exception as db_e:
                    st.toast(f"Silent logger warning: {db_e}")

                # Display salary band metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Low Estimate (P10)", f"${res['salary']['min']:,.0f}")
                c2.metric("Median Average", f"${res['salary']['average']:,.0f}")
                c3.metric("High Estimate (P90)", f"${res['salary']['max']:,.0f}")

                # Confidence score as % (explicit cast to avoid numpy float repr)
                score = float(res['confidence']['score'])
                label = res['confidence']['label']

                conf_col1, conf_col2 = st.columns([1, 2])
                with conf_col1:
                    st.metric("Confidence Score", f"{score:.1f}%", delta=label)
                with conf_col2:
                    adj = res['inflation_adjusted']['adjusted']
                    st.success(f"**Inflation Adjusted Projection (2024):** ${adj:,.0f}")

            except Exception as e:
                st.error(f"Prediction failed: Ensure models are thoroughly trained: {e}")
