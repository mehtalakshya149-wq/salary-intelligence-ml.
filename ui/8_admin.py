import streamlit as st
import pandas as pd
from api.database import SessionLocal
from api.models import User, ModelLog, SalaryPrediction

st.title("⚙️ Secure Admin Terminal")

if st.session_state.get("user_role") != "admin":
    st.error("ACCESS DENIED: Role elevation required.")
    st.stop()
    
st.markdown("System identity, user auditing, and historical metrics portal.")

try:
    db = SessionLocal()
    users = db.query(User).all()

    st.subheader(f"Registered Members Network")
    users_data = [{"UUID Vector": str(u.id)[:8]+"...","Username": u.username, "Email": u.email, "Clearance": u.role, "Timestamp": str(u.created_at).split(".")[0]} for u in users]
    st.dataframe(pd.DataFrame(users_data), use_container_width=True)

    st.markdown("---")
    st.subheader("🗑️ User Management")
    with st.expander("Remove / Delete an Account"):
        # Prevent admin from deleting themselves to avoid locking out the system
        candid_users = [u.username for u in users if u.username != st.session_state.username]
        if candid_users:
            user_to_delete = st.selectbox("Select User to Delete", candid_users)
            st.warning(f"Warning: Deleting **{user_to_delete}** is permanent and cannot be undone.")
            if st.button("Permanently Delete User", type="primary"):
                u_del = db.query(User).filter(User.username == user_to_delete).first()
                if u_del:
                    db.delete(u_del)
                    db.commit()
                    st.success(f"User '{user_to_delete}' has been permanently deleted.")
                    import time
                    time.sleep(1.5)
                    st.rerun()
        else:
            st.info("No other users available to delete.")
    st.markdown("---")

    st.subheader("Global Prediction Historical Audit")
    preds = db.query(SalaryPrediction).order_by(SalaryPrediction.created_at.desc()).limit(20).all()
    if preds:
        pred_data = [
            {
                "Member": p.user.username if p.user else p.user_id,
                "Query": p.job_title,
                "Lvl": p.experience_level,
                "Final Avg ($)": f"${p.predicted_average:,.0f}",
                "Confidence": f"{p.confidence_score}%",
                "Timestamp": str(p.created_at).split(".")[0]
            } for p in preds
        ]
        st.dataframe(pd.DataFrame(pred_data), use_container_width=True)
    else:
        st.info("No prediction traces recorded structurally through Postgres yet.")
        
    db.close()
except Exception as e:
    st.error(f"Fatal PostgreSQL ORM Binding Error: {e}")
