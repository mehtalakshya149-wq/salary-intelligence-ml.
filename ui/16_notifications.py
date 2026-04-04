import streamlit as st
import random
import json
import os
from datetime import datetime
from app import page_header
from api.database import SessionLocal
from api.models import Notification, SalaryPrediction, User

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")

page_header("Alerts & AI Insights", "Notification Center", "Personalized skill expansion opportunities and salary growth warnings natively tracking your career profile.")

if not st.session_state.get("logged_in", False):
    st.error("Please login to access notifications.")
    st.stop()

# Resolve user_id from DB if not already cached in session
if not st.session_state.get("user_id"):
    try:
        _db = SessionLocal()
        _user = _db.query(User).filter(User.username == st.session_state.username).first()
        _db.close()
        if _user:
            st.session_state.user_id = _user.id
        else:
            st.error("Could not resolve your user account. Please log out and log back in.")
            st.stop()
    except Exception as _e:
        st.error(f"DB lookup error: {_e}")
        st.stop()

user_id = st.session_state.user_id

col_main, col_btn = st.columns([3, 1])

with col_btn:
    if st.button("AI Opportunity Scan 🤖", use_container_width=True, type="primary"):
        try:
            db = SessionLocal()
            
            # Dynamic Market Cache from ml/market_data.json
            market_data_path = "ml/market_data.json"
            skill_alerts = []
            salary_alerts = []
            last_scan_date = "Unknown"
            
            if os.path.exists(market_data_path):
                with open(market_data_path, "r") as f:
                    data = json.load(f)
                    skill_alerts = [(a["title"], a["message"]) for a in data.get("skill_alerts", [])]
                    salary_alerts = [(a["title"], a["message"]) for a in data.get("salary_alerts", [])]
                    last_scan_date = data.get("metadata", {}).get("last_scan", "Unknown")

            # Fetch existing notification titles to prevent duplicates
            existing_notifs = db.query(Notification.title).filter(Notification.user_id == user_id).all()
            existing_titles = {n[0] for n in existing_notifs}

            # Filter for new alerts only
            available_skill_alerts = [a for a in skill_alerts if a[0] not in existing_titles]
            available_salary_alerts = [a for a in salary_alerts if a[0] not in existing_titles]

            latest_pred = (
                db.query(SalaryPrediction)
                .filter(SalaryPrediction.user_id == user_id)
                .order_by(SalaryPrediction.created_at.desc())
                .first()
            )

            # Generate new notifications
            new_count = 0
            if available_salary_alerts:
                sal_title, sal_msg = random.choice(available_salary_alerts)
                if latest_pred:
                    sal_msg = f"For trailing '{latest_pred.job_title}' roles: " + sal_msg
                db.add(Notification(user_id=user_id, title=sal_title, message=sal_msg))
                new_count += 1

            if available_skill_alerts and (random.choice([True, False]) or not available_salary_alerts):
                sk_title, sk_msg = random.choice(available_skill_alerts)
                db.add(Notification(user_id=user_id, title=sk_title, message=sk_msg))
                new_count += 1

            if new_count == 0:
                st.info(f"Market remains stable since scan on {last_scan_date}. No new unique AI insights found for your profile today.")
            else:
                db.commit()
                st.success(f"Market scan complete! {new_count} new AI insight(s) added based on 2026 data.")
            
            db.close()
            if new_count > 0:
                st.rerun()
        except Exception as e:
            st.error(f"Error generating notifications: {e}")

st.markdown("### Recent Alerts")

try:
    db = SessionLocal()
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    
    for n in notifications:
        n.is_read = bool(n.is_read)

    if not notifications:
        st.info("No active notifications. Run an AI scan to check for immediate market shifts.")
    else:
        unread_count = sum(1 for a in notifications if not a.is_read)
        if unread_count > 0:
            st.markdown(f"**{unread_count} Unread Messages**")

        for alert in notifications:
            cols = st.columns([4, 1])
            with cols[0]:
                if not alert.is_read:
                    with st.container(border=True):
                        st.markdown(f"🔴 **{alert.title}**")
                        st.markdown(f"*{alert.message}*")
                        
                        btn_cols = st.columns([1, 1, 2])
                        if btn_cols[0].button("Mark Read", key=f"read_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _a.is_read = 1
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                        
                        if btn_cols[1].button("🗑️ Delete", key=f"del_unread_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _db_temp.delete(_a)
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                else:
                    with st.container():
                        st.markdown(f"<span style='color:grey'>🔕 {alert.title}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:grey; font-size:14px'>{alert.message}</span>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete", key=f"del_read_{alert.id}"):
                            _db_temp = SessionLocal()
                            _a = _db_temp.query(Notification).get(alert.id)
                            _db_temp.delete(_a)
                            _db_temp.commit()
                            _db_temp.close()
                            st.rerun()
                        st.divider()

    db.close()
except Exception as e:
    st.error(f"Error loading notifications: {e}")
