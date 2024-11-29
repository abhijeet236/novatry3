import streamlit as st

def display_info():
    st.title("🏢 Welcome to Dive In Data: NOVA")
    st.subheader("Your Intelligent Organizational Chatbot")
    st.markdown("---")

    st.write("""
    Welcome to **NOVA**—the chatbot designed to streamline communication and enhance information access within your organization.
    """)

#subsections
    st.subheader("🔑 Key Features")
    st.write("""
    - **Instant Answers:** Get immediate responses to your queries about HR policies, IT support, and organizational events.
    - **Document Integration:** Upload relevant documents for context-rich answers tailored to your specific needs.
    - **User-Friendly Experience:** Designed for seamless interaction, NOVA ensures that every employee can easily find the information they need.
    - **Secure Access:** Our platform prioritizes security, allowing only registered admins to upload sensitive information while keeping user interactions confidential.
    """)

    st.subheader("🌟 Why Choose NOVA?")
    st.write("""
    NOVA is here to transform how your organization handles inquiries. Empower your teams with quick, accurate answers, and foster a collaborative work environment.
    """)

    st.subheader("👨‍💻 Developed By:")
    st.write("""
    This project is developed by Abhijeet Borate, Mitesh Agrawal, and Sandeep Muttireddy, final year CSEAI students from GHRCEM, Pune.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Footer section with custom styling
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("📧 For inquiries, contact: support@diveindata.com")
    st.write("🔗 Visit our website: [demo-diveindata.com](https://diveindata.com)")
