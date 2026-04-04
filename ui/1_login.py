import streamlit as st
import uuid
import pandas as pd
from api.database import SessionLocal, engine, Base
from api.models import User, ModelLog
from api.security import get_password_hash, verify_password, create_access_token



# Ensure tables exist for standalone testing
Base.metadata.create_all(bind=engine)

st.title("🔐 Authentication Portal")
st.markdown("Please authenticate securely through the unified database bridge.")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login to your account")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.hashed_password):
                st.session_state.logged_in = True
                st.session_state.user_role = user.role
                st.session_state.username = user.username
                st.session_state.user_id = user.id
                st.session_state.token = create_access_token(data={"sub": user.username, "role": user.role})
                st.session_state.last_active = __import__('time').time()
                
                # Log Frontend Login
                login_log = ModelLog(user_id=user.id, action=f"Frontend Login (Role: {user.role})", endpoint="UI/Login")
                db.add(login_log)
                db.commit()
                
                st.success(f"Welcome back, {user.username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
            db.close()

with tab2:
    st.subheader("Create a new account")
    with st.form("register_form"):
        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")
        new_role = "user"
        reg_submit = st.form_submit_button("Register")
        if reg_submit:
            db = SessionLocal()
            existing = db.query(User).filter((User.username == new_user) | (User.email == new_email)).first()
            if existing:
                st.error("Username or email already exists!")
            else:
                u = User(
                    id=str(uuid.uuid4()),
                    username=new_user,
                    email=new_email,
                    hashed_password=get_password_hash(new_pass),
                    role=new_role
                )
                db.add(u)
                db.commit()
                st.success("Account created successfully. Please switch to the Login tab.")
            db.close()
