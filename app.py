import streamlit as st
import psycopg2
import bcrypt
import home  

# PostgreSQL Database Connection
DB_PARAMS = {
    "dbname": "stock_login",
    "user": "postgres",
    "password": "1998",
    "host": "localhost",
    "port": "5432"
}

def create_table():
    """Create users table if not exists"""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def register_user(username, password):
    """Register a new user"""
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        st.success("User registered successfully! Please log in.")
    except psycopg2.Error:
        st.error("Username already exists. Try a different one.")
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    """Authenticate user login"""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return True
    return False

def main():
    """Main function"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        st.sidebar.write(f"👤 Logged in as: **{st.session_state['user']}**")

        # ✅ Logout Button
        if st.sidebar.button("🚪 Logout"):
            st.session_state["authenticated"] = False
            st.session_state.pop("user", None)
            st.rerun()

        # ✅ Load home.py after login
        home.show_home_page()
    else:
        st.title("📈 Stock Price Webapp")

        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login to Your Account")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = username
                    st.success(f"Welcome {username}! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

        elif choice == "Register":
            st.subheader("Create a New Account")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if new_password == confirm_password:
                    register_user(new_username, new_password)
                else:
                    st.error("Passwords do not match. Try again.")

if __name__ == "__main__":
    create_table()  # Ensure table is created before running
    main()
