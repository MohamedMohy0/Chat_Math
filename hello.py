import streamlit as st

# Set page configuration
st.set_page_config(page_title="Welcome", page_icon="💊")

# Hide Streamlit Default UI (Menu & Footer)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px; /* Adjust spacing between logo and text */
    }
    
    /* Hide Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hide Sidebar Toggle (Arrow) */
    section[data-testid="collapsedControl"], div[aria-label="Toggle sidebar"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 7, 1])  # Create columns to center content
with col2:
    st.markdown('<h1 style="text-align: center; color: black;">Welcome to <span style="color: black;">Chat Math</span></h1>', unsafe_allow_html=True)

with col2:
    st.image("image1.jpg", width=900)  # Adjust width as needed

# "Let's Start" Button (Centered)
st.markdown("<br>", unsafe_allow_html=True)  # Add spacing before button
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    if st.button("Let's Start", help="Click to continue"):
        st.switch_page("pages/app.py")  # Navigate to another page
