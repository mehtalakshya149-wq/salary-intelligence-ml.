import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Admin Terminal", page_icon="⚙️", layout="wide")

st.title("⚙️ Secure Admin Terminal")

if st.session_state.get("user_role") != "admin":
    st.error("ACCESS DENIED: Role elevation required.")
    st.stop()
    
st.markdown("System identity, user auditing, and historical metrics portal.")

token = st.session_state.token
headers = {"Authorization": f"Bearer {token}"}
base_url = "http://localhost:8000/api/v1/admin"

tab1, tab2, tab3, tab4 = st.tabs(["Identities", "Predictions", "Security Logs", "ML Engine Ops"])

with tab1:
    st.subheader(f"Registered Members Network")
    try:
        res = requests.get(f"{base_url}/users", headers=headers)
        if res.status_code == 200:
            users = res.json()
            users_data = [{"UUID Vector": str(u['id'])[:8]+"...","Username": u['username'], "Email": u['email'], "Clearance": u['role'], "Timestamp": str(u['created_at']).split("T")[0]} for u in users]
            st.dataframe(pd.DataFrame(users_data), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🗑️ User Management")
            with st.expander("Remove / Delete an Account"):
                candid_users = [u['username'] for u in users if u['username'] != st.session_state.username]
                if candid_users:
                    user_to_delete = st.selectbox("Select User to Delete", candid_users)
                    st.warning(f"Warning: Deleting **{user_to_delete}** is permanent and cannot be undone.")
                    if st.button("Permanently Delete User", type="primary"):
                        del_req = requests.delete(f"{base_url}/users/{user_to_delete}", headers=headers)
                        if del_req.status_code == 200:
                            st.success(f"User '{user_to_delete}' has been permanently deleted.")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(del_req.text)
                else:
                    st.info("No other users available to delete.")
        else:
            st.error(f"HTTP Error: {res.text}")
    except Exception as e:
        st.error(f"Cannot connect to admin backend: {e}")

with tab2:
    st.subheader("Global Prediction Historical Audit")
    try:
        res = requests.get(f"{base_url}/predictions", headers=headers)
        if res.status_code == 200:
            preds = res.json()
            if preds:
                pred_data = [
                    {
                        "Member": p['username'],
                        "Query": p['job_title'],
                        "Lvl": p['experience'],
                        "Final Avg ($)": f"${p['predicted_salary']:,.0f}",
                        "Confidence": f"{p['confidence']}%",
                        "Timestamp": str(p['created_at']).replace("T", " ").split(".")[0]
                    } for p in preds
                ]
                st.dataframe(pd.DataFrame(pred_data), use_container_width=True)
            else:
                st.info("No prediction traces recorded structurally through Postgres yet.")
    except Exception as e:
        st.error(f"Connection Failed: {e}")

with tab3:
    st.subheader("System Security & Access Logs")
    try:
        res = requests.get(f"{base_url}/logs", headers=headers)
        if res.status_code == 200:
            logs = res.json()
            if logs:
                log_data = [{
                    "Member": l['username'],
                    "Action": l['action'],
                    "Endpoint": l['endpoint'],
                    "Timestamp": str(l['timestamp']).replace("T", " ").split(".")[0]
                } for l in logs]
                st.dataframe(pd.DataFrame(log_data), use_container_width=True)
            else:
                st.info("No logs present in the database.")
    except Exception as e:
        st.error(f"Log Fetch Failed: {e}")

with tab4:
    st.subheader("Model Lifecycle Management")
    st.markdown("Trigger a background `joblib` regeneration pipeline. This forces the server to re-pull the active database configuration and train a fresh ensemble (Random Forest + Gradient Boosting) using `ml.src.train.run_training()`.")
    
    if st.button("Retrain Complete AI Ensemble 🚀", type="primary"):
        with st.spinner("Dispatching off-thread retraining command via FastAPI..."):
            try:
                res = requests.post(f"{base_url}/retrain", headers=headers)
                if res.status_code == 200:
                    st.success("Retrain routine successfully delegated to background workers! Model artifacts will overwrite invisibly.")
                else:
                    st.error(f"Pipeline error: {res.text}")
            except Exception as e:
                st.error(f"Server offline: {e}")
