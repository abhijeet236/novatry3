import streamlit as st
#login function
def login_process():
    st.title("Login to NOVA")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Implemented authentication with roles
        # admin credentials
        if username == "admin1" and password == "adminpas1":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.success("Logged in as Admin!")
        # user credentials
        elif username == "user1" and password == "userpas1":
            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.success("Logged in as User!")
        else:
            st.error("Invalid credentials, please try again.")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.role}.")
