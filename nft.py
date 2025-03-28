import streamlit as st
import pymongo
import hashlib
import secrets
import datetime
import base64
from PIL import Image
import io
import random
import uuid
import pandas as pd
import time  # Added for delayed redirects
from streamlit_option_menu import option_menu

# Must set page config as the first Streamlit command
st.set_page_config(
    page_title="NFT Nexus | Digital Collectibles Marketplace",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for a more professional look
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #3B82F6;
        --secondary-color: #10B981;
        --dark-bg: #1F2937;
        --card-bg: #ffffff;
        --text-color: #1E293B;
        --light-accent: #F1F5F9;
        --highlight: #3B82F6;
    }

    /* Global styling */
    .main {
        background-color: #F8FAFC;
        color: var(--text-color);
    }
    
    /* Header styling */
    h1 {
        color: #1E293B;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        color: #1E293B;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #3B82F6 0%, #4F46E5 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, #2563EB 0%, #4338CA 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Form field styling */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stFileUploader {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        padding: 12px 16px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* NFT Card styling */
    .nft-card {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
        border: 1px solid #E2E8F0;
        display: flex;
        flex-direction: column;
    }
    
    .nft-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .nft-card-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 12px;
    }
    
    .nft-image-container {
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 100%;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    .nft-owner {
        font-size: 0.875rem;
        color: #6B7280;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .nft-price {
        font-weight: 600;
        color: var(--primary-color);
        font-size: 1.15rem;
        display: flex;
        align-items: center;
        gap: 5px;
        margin: 10px 0;
    }
    
    .nft-description {
        color: #6B7280;
        font-size: 0.875rem;
        margin-bottom: 15px;
        flex-grow: 1;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Marketplace header */
    .marketplace-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .balance-display {
        background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        background-color: #E2E8F0;
        color: #4B5563;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .badge-blue {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    
    .badge-green {
        background-color: #DCFCE7;
        color: #166534;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px;
        background-color: #F1F5F9;
        color: #4B5563;
        font-weight: 500;
        border: none !important;
        padding: 10px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Dataframe styling */
    .dataframe-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Metrics styling */
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Custom flex grid system */
    .flex-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .flex-grid-item {
        flex: 1 1 300px;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
        background-color: #F3F4F6;
    }
    
    /* Navigation menu styling */
    [data-testid="stSidebar"] {
        background-color: white;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
    }
    
    .nav-link {
        display: flex;
        align-items: center;
        padding: 12px 15px;
        margin-bottom: 8px;
        border-radius: 10px;
        text-decoration: none;
        transition: all 0.2s;
    }
    
    .nav-link:hover {
        background-color: #F1F5F9;
    }
    
    .nav-link.active {
        background-color: #EFF6FF;
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Project logo */
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-left: 10px;
    }
    
    /* Smooth font rendering */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# MongoDB Connection Function
@st.cache_resource
def get_database():
    """Connect to MongoDB and return the database instance"""
    try:
        # MongoDB Atlas connection string
        connection_string = "mongodb+srv://nft:nft@web3.tdsyo8p.mongodb.net/?retryWrites=true&w=majority&appName=WEB3"
        client = pymongo.MongoClient(connection_string)
        return client['nft_marketplace_db']
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Initialize database and collections
db = get_database()
if db is not None:
    users_collection = db['users']
    nfts_collection = db['nfts']
    transactions_collection = db['transactions']
    
    # Create indexes for performance
    users_collection.create_index([("username", pymongo.ASCENDING)], unique=True)
    nfts_collection.create_index([("nft_id", pymongo.ASCENDING)], unique=True)
    transactions_collection.create_index([("transaction_id", pymongo.ASCENDING)], unique=True)

# Utility Functions
def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_transaction_hash(buyer, seller, nft_id, price, timestamp):
    """Generate a unique hash for a transaction"""
    data = f"{buyer}{seller}{nft_id}{price}{timestamp}{secrets.token_hex(8)}"
    return hashlib.sha256(data.encode()).hexdigest()

def generate_random_eth_balance():
    """Generate a random ETH balance between 1 and 10 ETH"""
    return round(random.uniform(1.0, 10.0), 4)

def image_to_base64(image_file):
    """Convert an image file to base64 for storage, preserving original format"""
    img = Image.open(image_file)
    
    # Determine the format from the file name or fall back to PNG
    file_format = image_file.type.split('/')[1].upper()
    if file_format not in ['PNG', 'JPEG', 'JPG', 'GIF', 'BMP', 'WEBP']:
        file_format = 'PNG'  # Default to PNG for unsupported formats
        
    # Standardize JPEG naming
    if file_format == 'JPG':
        file_format = 'JPEG'
    
    # Resize image if it's too large (optional)
    max_size = (800, 800)
    img.thumbnail(max_size, Image.LANCZOS)
    
    # Handle transparency for formats that don't support it
    if img.mode == 'RGBA' and file_format == 'JPEG':
        # Convert RGBA to RGB by removing transparency or blending with white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        img = background
    
    buffered = io.BytesIO()
    img.save(buffered, format=file_format)
    return base64.b64encode(buffered.getvalue()).decode(), file_format

def base64_to_image(base64_string, format='JPEG'):
    """Convert base64 string back to an image for display"""
    img_data = base64.b64decode(base64_string)
    return io.BytesIO(img_data)

# Authentication Functions
def signup():
    """Handle user registration"""
    st.title("🖌️ Create Your NFT Account")
    
    with st.form("signup_form"):
        new_username = st.text_input("Username", placeholder="Choose a unique username")
        new_password = st.text_input("Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        signup_button = st.form_submit_button("Sign Up", use_container_width=True)
        
        if signup_button:
            if not new_username or not new_password:
                st.error("Username and password are required.")
                return
                
            if new_password != confirm_password:
                st.error("Passwords do not match.")
                return
                
            # Check if username already exists
            if users_collection.find_one({"username": new_username}):
                st.error("Username already exists. Please choose another.")
                return
                
            # Create new user with random ETH balance
            eth_balance = generate_random_eth_balance()
            new_user = {
                "username": new_username,
                "password": hash_password(new_password),
                "eth_balance": eth_balance,
                "is_admin": False,
                "registration_date": datetime.datetime.now()
            }
            
            users_collection.insert_one(new_user)
            st.success(f"Account created successfully! You've been assigned {eth_balance:.4f} ETH.")
            
            # Auto login after signup
            st.session_state.logged_in = True
            st.session_state.username = new_username
            st.session_state.is_admin = False
            st.session_state.page = 'marketplace'
            st.rerun()

def login():
    """Handle user login"""
    st.title("🔑 Login to NFT Marketplace")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)
        with col2:
            signup_redirect = st.form_submit_button("Create Account", use_container_width=True)
        
        if login_button:
            if not username or not password:
                st.error("Username and password are required.")
                return
                
            # Check credentials
            user = users_collection.find_one({
                "username": username,
                "password": hash_password(password)
            })
            
            if user:
                st.success("Login successful!")
                
                # Set session state
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = user.get('is_admin', False)
                st.session_state.page = 'marketplace'
                st.rerun()
            else:
                st.error("Invalid username or password.")
        
        if signup_redirect:
            st.session_state.page = 'signup'
            st.rerun()

# Admin Functions
def admin_dashboard():
    """Admin dashboard to manage users and increase ETH balances"""
    st.markdown("<h1>⚙️ Admin Control Panel</h1>", unsafe_allow_html=True)
    
    # Admin panel introduction
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); padding: 20px; border-radius: 15px; margin-bottom: 25px; color: white;">
        <h3 style="color: white; margin-top: 0;">Administrator Tools</h3>
        <p>Welcome to the admin panel. Here you can manage users, monitor platform activity, and add ETH to user balances. Remember that as an admin, you can only increase balances to maintain decentralization principles.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different admin functions
    tab1, tab2, tab3 = st.tabs(["👥 User Management", "💰 Add ETH Balance", "📈 Platform Stats"])
    
    # Get all users once for use in all tabs
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))
    
    if not users:
        with tab1, tab2, tab3:
            st.info("No users found in the system.")
        return
    
    # Tab 1: User Management
    with tab1:
        st.subheader("Registered Users")
        
        # Add search filter
        search_term = st.text_input("Search users by username:", placeholder="Enter username...")
        
        filtered_users = users
        if search_term:
            filtered_users = [user for user in users if search_term.lower() in user['username'].lower()]
        
        # Convert to DataFrame for better display
        user_data = []
        for user in filtered_users:
            # Format registration date
            reg_date = user.get('registration_date', datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            
            # User role badge
            role_badge = "<span class='badge' style='background-color: #FEF3C7; color: #92400E;'>Admin</span>" if user.get('is_admin', False) else "<span class='badge badge-blue'>User</span>"
            
            # Format ETH balance
            eth_balance = user.get('eth_balance', 0)
            
            # Add user data
            user_data.append({
                "Username": user['username'],
                "Role": role_badge,
                "ETH Balance": f"{eth_balance:.4f} ETH",
                "Registration Date": reg_date
            })
        
        if user_data:
            df = pd.DataFrame(user_data)
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No users match your search criteria.")
    
    # Tab 2: Add ETH Balance
    with tab2:
        st.subheader("Increase User Balance")
        
        # Better user selection with search
        regular_users = [user for user in users if not user.get('is_admin', False)]
        username_to_update = st.selectbox(
            "Select User to Fund", 
            options=[user['username'] for user in regular_users],
            format_func=lambda x: f"{x} (Current: {next((u['eth_balance'] for u in regular_users if u['username'] == x), 0):.4f} ETH)"
        )
        
        # Get current balance for the selected user
        selected_user = next((user for user in regular_users if user['username'] == username_to_update), None)
        
        if selected_user:
            current_balance = selected_user.get('eth_balance', 0)
            
            # Display current balance prominently
            st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">CURRENT BALANCE</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{current_balance:.4f} ETH</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Amount selection with slider and number input
            st.markdown("<p>Amount to Add (ETH):</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            
            with col1:
                amount_slider = st.slider(
                    "", 
                    min_value=0.1, 
                    max_value=10.0, 
                    value=1.0, 
                    step=0.1
                )
            
            with col2:
                amount_to_add = st.number_input(
                    "", 
                    min_value=0.001, 
                    max_value=100.0, 
                    value=float(amount_slider),
                    step=0.001,
                    format="%.3f"
                )
            
            # Preview new balance
            new_balance = current_balance + amount_to_add
            st.markdown(f"""
            <div style="background-color: #F0FDF4; padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; border: 1px solid #DCFCE7;">
                <div style="font-size: 0.85rem; color: #166534; margin-bottom: 5px;">NEW BALANCE AFTER FUNDING</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #166534;">{new_balance:.4f} ETH</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add transaction note (optional)
            transaction_note = st.text_area(
                "Transaction Note (Optional)", 
                placeholder="Add a note about this transaction (e.g., 'Monthly platform reward')",
                max_chars=200
            )
            
            # Submit button
            if st.button("Fund User Account", use_container_width=True):
                # Update user's ETH balance
                result = users_collection.update_one(
                    {"username": username_to_update},
                    {"$inc": {"eth_balance": amount_to_add}}
                )
                
                if result.modified_count:
                    # Success message
                    st.markdown(f"""
                    <div style="background-color: #DCFCE7; color: #166534; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;">
                        <h3 style="color: #166534;">Transaction Successful! 🎉</h3>
                        <p>Added {amount_to_add:.4f} ETH to {username_to_update}'s balance.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Record this as a transaction
                    transaction = {
                        "transaction_id": generate_transaction_hash("admin", username_to_update, "eth_deposit", amount_to_add, datetime.datetime.now()),
                        "nft_id": "eth_deposit",
                        "seller": "admin",
                        "buyer": username_to_update,
                        "price": amount_to_add,
                        "timestamp": datetime.datetime.now(),
                        "transaction_type": "deposit",
                        "note": transaction_note if transaction_note else "Admin deposit"
                    }
                    transactions_collection.insert_one(transaction)
                else:
                    st.error("Failed to update balance. Please try again.")
        else:
            st.error("User not found. Please select a valid user.")
    
    # Tab 3: Platform Stats
    with tab3:
        st.subheader("Platform Overview")
        
        # Get all NFTs
        all_nfts = list(nfts_collection.find({}, {"_id": 0}))
        
        # Get all transactions
        all_transactions = list(transactions_collection.find({}, {"_id": 0}))
        
        # Calculate platform stats
        total_users = len(users)
        total_nfts = len(all_nfts)
        total_transactions = len(all_transactions)
        listed_nfts = len([nft for nft in all_nfts if nft.get('listed', False)])
        
        purchase_transactions = [t for t in all_transactions if t.get('transaction_type') == 'purchase']
        total_volume = sum(t.get('price', 0) for t in purchase_transactions)
        
        # Calculate average user balance
        total_eth = sum(user.get('eth_balance', 0) for user in users)
        avg_balance = total_eth / total_users if total_users > 0 else 0
        
        # Display stats in a grid
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TOTAL USERS</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{}</div>
            </div>
            """.format(total_users), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TOTAL NFTs</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{}</div>
            </div>
            """.format(total_nfts), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">LISTED NFTs</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{} / {}</div>
            </div>
            """.format(listed_nfts, total_nfts), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TOTAL TRANSACTIONS</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{}</div>
            </div>
            """.format(total_transactions), unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TRADING VOLUME</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{:.4f} ETH</div>
            </div>
            """.format(total_volume), unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">AVG USER BALANCE</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{:.4f} ETH</div>
            </div>
            """.format(avg_balance), unsafe_allow_html=True)
        
        # Add charts for visual representation
        st.subheader("Transaction History")
        
        # Group transactions by day
        if purchase_transactions:
            # Prepare data for chart
            transaction_dates = [t.get('timestamp').date() for t in purchase_transactions]
            date_counts = {}
            date_volumes = {}
            
            for i, date in enumerate(transaction_dates):
                if date in date_counts:
                    date_counts[date] += 1
                    date_volumes[date] += purchase_transactions[i].get('price', 0)
                else:
                    date_counts[date] = 1
                    date_volumes[date] = purchase_transactions[i].get('price', 0)
            
            # Create DataFrame for chart
            chart_data = pd.DataFrame({
                'Date': list(date_counts.keys()),
                'Transactions': list(date_counts.values()),
                'Volume': list(date_volumes.values())
            })
            
            chart_data = chart_data.sort_values('Date')
            
            # Display chart
            st.line_chart(chart_data.set_index('Date')[['Transactions', 'Volume']])

# NFT Marketplace Functions
def list_nft():
    """Interface for users to list a new NFT for sale"""
    st.markdown("<h1>🖼️ Create Your Masterpiece</h1>", unsafe_allow_html=True)
    
    # Show creative introduction
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); padding: 20px; border-radius: 15px; margin-bottom: 25px; color: white;">
        <h3 style="color: white; margin-top: 0;">Transform Your Art Into Blockchain Treasures</h3>
        <p>List your digital creations on our secure NFT marketplace. Set your price, add compelling details, and showcase your work to collectors worldwide.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns layout for form and preview
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("list_nft_form", clear_on_submit=False):
            st.markdown("<h3>NFT Details</h3>", unsafe_allow_html=True)
            
            nft_title = st.text_input("✨ Title", placeholder="Give your NFT a catchy title")
            nft_description = st.text_area("📝 Description", placeholder="Describe your NFT in detail - tell its story", height=120)
            
            # Price with visual slider and number input
            st.markdown("<p>💰 Price (ETH)</p>", unsafe_allow_html=True)
            price_col1, price_col2 = st.columns([3, 1])
            with price_col1:
                price_slider = st.slider("", min_value=0.001, max_value=10.0, value=1.0, step=0.1, format="%.3f")
            with price_col2:
                nft_price = st.number_input("", min_value=0.001, max_value=100.0, value=price_slider, step=0.001, format="%.4f")
            
            # Image upload with preview
            st.markdown("<p>🖼️ NFT Image</p>", unsafe_allow_html=True)
            nft_image = st.file_uploader("", type=["jpg", "jpeg", "png", "gif"])
            
            # Tags (optional feature)
            nft_tags = st.text_input("🏷️ Tags (optional)", placeholder="art, digital, abstract (comma separated)")
            
            # Submit button with enhanced styling
            submit_button = st.form_submit_button("Create NFT", use_container_width=True)
            
            if submit_button:
                if not nft_title or not nft_description or not nft_price or not nft_image:
                    st.error("All fields are required except tags.")
                    return
                
                try:
                    # Convert image to base64
                    image_b64, image_format = image_to_base64(nft_image)
                    
                    # Process tags
                    tags_list = [tag.strip() for tag in nft_tags.split(',')] if nft_tags else []
                    
                    # Create NFT object
                    nft_id = str(uuid.uuid4())
                    new_nft = {
                        "nft_id": nft_id,
                        "title": nft_title,
                        "description": nft_description,
                        "image": image_b64,
                        "image_format": image_format,
                        "price": nft_price,
                        "owner": st.session_state.username,
                        "listed": True,
                        "creation_date": datetime.datetime.now(),
                        "tags": tags_list
                    }
                    
                    # Insert into database
                    nfts_collection.insert_one(new_nft)
                    
                    # Show success message with animation
                    st.markdown("""
                    <div style="background-color: #DCFCE7; color: #166534; padding: 20px; border-radius: 10px; text-align: center;">
                        <h3 style="color: #166534;">NFT Created Successfully! 🎉</h3>
                        <p>Your NFT is now listed on the marketplace.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Record creation as a transaction
                    transaction = {
                        "transaction_id": generate_transaction_hash(st.session_state.username, "marketplace", nft_id, 0, datetime.datetime.now()),
                        "nft_id": nft_id,
                        "seller": "marketplace",
                        "buyer": st.session_state.username,
                        "price": 0,
                        "timestamp": datetime.datetime.now(),
                        "transaction_type": "creation"
                    }
                    transactions_collection.insert_one(transaction)
                    
                except Exception as e:
                    st.error(f"Error listing NFT: {e}")
    
    with col2:
        st.markdown("<h3>Preview</h3>", unsafe_allow_html=True)
        
        # NFT preview card
        preview_container = st.container()
        with preview_container:
            st.markdown("""
            <div class="nft-card" style="min-height: 400px;">
                <div class="nft-card-header">NFT Preview</div>
            """, unsafe_allow_html=True)
            
            # Preview logic
            if 'nft_image' in locals() and nft_image is not None:
                st.image(nft_image, use_column_width=True)
            else:
                st.markdown("""
                <div style="background-color: #F3F4F6; height: 200px; border-radius: 10px; display: flex; justify-content: center; align-items: center; margin-bottom: 15px;">
                    <p style="color: #6B7280;">Image preview will appear here</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Title preview
            title_preview = nft_title if 'nft_title' in locals() and nft_title else "Your NFT Title"
            st.markdown(f"<div style='font-size: 1.25rem; font-weight: 600; margin-bottom: 10px;'>{title_preview}</div>", unsafe_allow_html=True)
            
            # Price preview
            price_preview = nft_price if 'nft_price' in locals() and nft_price else 0.0
            st.markdown(f"<div class='nft-price'>💎 {price_preview:.4f} ETH</div>", unsafe_allow_html=True)
            
            # Owner preview
            st.markdown(f"<div class='nft-owner'>👤 Owner: <span class='badge badge-blue'>{st.session_state.username}</span></div>", unsafe_allow_html=True)
            
            # Description preview
            desc_preview = nft_description if 'nft_description' in locals() and nft_description else "Your description will appear here"
            if len(desc_preview) > 100:
                desc_preview = desc_preview[:100] + "..."
            st.markdown(f"<div class='nft-description'>{desc_preview}</div>", unsafe_allow_html=True)
            
            # Tags preview
            if 'nft_tags' in locals() and nft_tags:
                tag_html = ""
                for tag in nft_tags.split(','):
                    tag = tag.strip()
                    if tag:
                        tag_html += f"<span class='badge' style='margin-right: 5px; margin-bottom: 5px;'>{tag}</span>"
                if tag_html:
                    st.markdown(f"<div style='margin-top: 10px;'>{tag_html}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Marketplace tips
        with st.expander("📚 Tips for Creating Valuable NFTs"):
            st.markdown("""
            - **High-Quality Images**: Upload the highest quality image possible.
            - **Detailed Description**: Tell the story behind your creation.
            - **Fair Pricing**: Research similar NFTs to price competitively.
            - **Effective Tags**: Use relevant tags to help collectors find your work.
            - **Promote Your Work**: Share your NFT on social media to increase visibility.
            """)


def display_nft_marketplace():
    """Display all listed NFTs in a grid layout"""
    st.markdown("<div class='marketplace-header'><h1>🌌 NFT Marketplace</h1></div>", unsafe_allow_html=True)
    
    # Get current user's ETH balance
    user = users_collection.find_one({"username": st.session_state.username})
    if user:
        st.markdown(
            f"<div class='balance-display'>💰 Your Balance: {user['eth_balance']:.4f} ETH</div>",
            unsafe_allow_html=True
        )
    
    # Get all listed NFTs
    listed_nfts = list(nfts_collection.find({"listed": True}))
    
    if not listed_nfts:
        st.info("No NFTs currently listed in the marketplace. Be the first to list one!")
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Grid View", "📋 List View"])
    
    with tab1:
        # Display NFTs in a grid
        cols_per_row = 3
        
        for i in range(0, len(listed_nfts), cols_per_row):
            row_nfts = listed_nfts[i:i+cols_per_row]
            cols = st.columns(cols_per_row)
            
            for j, nft in enumerate(row_nfts):
                with cols[j]:
                    # Create a card-like display for each NFT
                    with st.container():
                        st.markdown(f"""
                        <div class="nft-card">
                            <div class="nft-card-header">{nft['title']}</div>
                        """, unsafe_allow_html=True)
                        
                        # Display image
                        try:
                            img = base64_to_image(nft['image'], nft.get('image_format', 'JPEG'))
                            st.image(img, use_column_width=True)
                        except Exception as e:
                            st.error(f"Could not load image: {e}")
                        
                        # Show badge for ownership
                        owner_badge = "badge badge-green" if nft['owner'] == st.session_state.username else "badge badge-blue"
                        owner_label = "You" if nft['owner'] == st.session_state.username else nft['owner']
                        
                        st.markdown(f"""
                            <div class="nft-price">💎 {nft['price']:.4f} ETH</div>
                            <div class="nft-owner">👤 Owner: <span class="{owner_badge}">{owner_label}</span></div>
                        """, unsafe_allow_html=True)
                        
                        # Show truncated description
                        max_desc_length = 100
                        description = nft['description']
                        if len(description) > max_desc_length:
                            description = description[:max_desc_length] + "..."
                        
                        st.markdown(f"""
                            <div class="nft-description">{description}</div>
                        """, unsafe_allow_html=True)
                        
                        # Only show buy button if not the owner
                        if nft['owner'] != st.session_state.username:
                            if st.button(f"Buy NFT", key=f"buy_{nft['nft_id']}"):
                                purchase_nft(nft)
                        else:
                            st.info("You own this NFT")
    
    with tab2:
        # Create a dataframe for list view
        list_data = []
        for nft in listed_nfts:
            owner_display = "You" if nft['owner'] == st.session_state.username else nft['owner']
            list_data.append({
                "Title": nft['title'],
                "Description": nft['description'][:50] + "..." if len(nft['description']) > 50 else nft['description'],
                "Price (ETH)": f"{nft['price']:.4f}",
                "Owner": owner_display,
                "Listed Date": nft['creation_date'].strftime('%Y-%m-%d'),
                "Action": nft['nft_id']  # We'll use this to create buttons
            })
        
        if list_data:
            df = pd.DataFrame(list_data)
            # Hide the Action column from display but keep it for reference
            display_df = df.drop(columns=["Action"])
            
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(display_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Create action buttons in a separate section
            st.subheader("NFT Actions")
            for i, row in df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{row['Title']} - {row['Price (ETH)']} ETH")
                with col2:
                    nft_id = row['Action']
                    nft = next((n for n in listed_nfts if n['nft_id'] == nft_id), None)
                    if nft and nft['owner'] != st.session_state.username:
                        if st.button(f"Buy", key=f"list_buy_{nft_id}"):
                            purchase_nft(nft)
        else:
            st.info("No NFTs available in the marketplace.")

def purchase_nft(nft):
    """Handle the NFT purchase transaction"""
    # Get buyer's current balance
    buyer = users_collection.find_one({"username": st.session_state.username})
    
    if not buyer:
        st.error("User not found.")
        return
    
    if buyer['eth_balance'] < nft['price']:
        st.error("Insufficient ETH balance to purchase this NFT.")
        return
    
    try:
        # Create transaction
        timestamp = datetime.datetime.now()
        transaction_id = generate_transaction_hash(
            buyer['username'], 
            nft['owner'], 
            nft['nft_id'], 
            nft['price'], 
            timestamp
        )
        
        # Record transaction
        transaction = {
            "transaction_id": transaction_id,
            "nft_id": nft['nft_id'],
            "seller": nft['owner'],
            "buyer": buyer['username'],
            "price": nft['price'],
            "timestamp": timestamp,
            "transaction_type": "purchase"
        }
        
        # Start a session for atomic transaction
        with db.client.start_session() as session:
            with session.start_transaction():
                # 1. Update buyer's balance
                users_collection.update_one(
                    {"username": buyer['username']},
                    {"$inc": {"eth_balance": -nft['price']}},
                    session=session
                )
                
                # 2. Update seller's balance
                users_collection.update_one(
                    {"username": nft['owner']},
                    {"$inc": {"eth_balance": nft['price']}},
                    session=session
                )
                
                # 3. Transfer NFT ownership
                nfts_collection.update_one(
                    {"nft_id": nft['nft_id']},
                    {"$set": {"owner": buyer['username']}},
                    session=session
                )
                
                # 4. Record transaction
                transactions_collection.insert_one(transaction, session=session)
        
        st.success(f"Successfully purchased '{nft['title']}' for {nft['price']} ETH!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Transaction failed: {e}")

def my_nfts():
    """Display NFTs owned by the current user"""
    st.markdown("<h1>🏆 My NFT Collection</h1>", unsafe_allow_html=True)
    
    # Get user's NFTs
    user_nfts = list(nfts_collection.find({"owner": st.session_state.username}))
    
    if not user_nfts:
        st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h3 style="color: #6B7280; font-weight: 500;">Your collection is empty</h3>
            <p style="color: #6B7280;">Visit the marketplace to purchase your first NFT!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a quick link to marketplace
        if st.button("Browse Marketplace", use_container_width=True):
            st.session_state.page = 'marketplace'
            st.rerun()
        return
    
    # Add filter and sort options
    col1, col2 = st.columns(2)
    with col1:
        filter_option = st.selectbox(
            "Filter by:",
            ["All", "Listed", "Not Listed"],
            index=0
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sort by:",
            ["Newest First", "Oldest First", "Price (High to Low)", "Price (Low to High)"],
            index=0
        )
    
    # Apply filters
    if filter_option == "Listed":
        user_nfts = [nft for nft in user_nfts if nft.get('listed', False)]
    elif filter_option == "Not Listed":
        user_nfts = [nft for nft in user_nfts if not nft.get('listed', False)]
    
    # Apply sorting
    if sort_option == "Newest First":
        user_nfts = sorted(user_nfts, key=lambda x: x.get('creation_date', datetime.datetime.min), reverse=True)
    elif sort_option == "Oldest First":
        user_nfts = sorted(user_nfts, key=lambda x: x.get('creation_date', datetime.datetime.min))
    elif sort_option == "Price (High to Low)":
        user_nfts = sorted(user_nfts, key=lambda x: x.get('price', 0), reverse=True)
    elif sort_option == "Price (Low to High)":
        user_nfts = sorted(user_nfts, key=lambda x: x.get('price', 0))
    
    # Display collection stats
    st.markdown("### Collection Statistics")
    stat1, stat2, stat3 = st.columns(3)
    
    with stat1:
        total_value = sum(nft.get('price', 0) for nft in user_nfts)
        st.metric("Total Collection Value", f"{total_value:.4f} ETH")
    
    with stat2:
        listed_count = len([nft for nft in user_nfts if nft.get('listed', False)])
        st.metric("NFTs Listed for Sale", f"{listed_count} / {len(user_nfts)}")
    
    with stat3:
        avg_price = total_value / len(user_nfts) if user_nfts else 0
        st.metric("Average NFT Price", f"{avg_price:.4f} ETH")
    
    st.markdown("### Your NFTs")
    
    # Display user's NFTs in a grid
    cols_per_row = 3
    
    for i in range(0, len(user_nfts), cols_per_row):
        row_nfts = user_nfts[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        
        for j, nft in enumerate(row_nfts):
            with cols[j]:
                with st.container():
                    is_listed = nft.get('listed', False)
                    status_badge = "badge badge-green" if is_listed else "badge badge-blue"
                    status_text = "For Sale" if is_listed else "Not Listed"
                    
                    st.markdown(f"""
                    <div class="nft-card">
                        <div class="nft-card-header">{nft['title']}</div>
                        <div style="position: absolute; top: 15px; right: 15px;">
                            <span class="{status_badge}">{status_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display image
                    try:
                        img = base64_to_image(nft['image'], nft.get('image_format', 'JPEG'))
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Could not load image: {e}")
                    
                    st.markdown(f"""
                        <div class="nft-price">💎 {nft['price']:.4f} ETH</div>
                    """, unsafe_allow_html=True)
                    
                    # Toggle listing status button
                    if st.button(
                        "Unlist from Marketplace" if is_listed else "List on Marketplace", 
                        key=f"toggle_{nft['nft_id']}"
                    ):
                        # Toggle listed status
                        new_status = not is_listed
                        nfts_collection.update_one(
                            {"nft_id": nft['nft_id']},
                            {"$set": {"listed": new_status}}
                        )
                        st.success(f"NFT {'listed' if new_status else 'unlisted'} successfully!")
                        st.rerun()
                    
                    # Show full description
                    with st.expander("View Description"):
                        st.markdown(nft['description'])

def transaction_dashboard():
    """Display all transactions in a transparent dashboard"""
    st.markdown("<h1>📊 Transaction Ledger</h1>", unsafe_allow_html=True)
    
    # Add dashboard introduction
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); padding: 20px; border-radius: 15px; margin-bottom: 25px; color: white;">
        <h3 style="color: white; margin-top: 0;">Blockchain Transparency</h3>
        <p>All transactions on our platform are recorded on this public ledger, ensuring complete transparency and traceability. Each transaction includes a unique hash for verification.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all transactions
    transactions = list(transactions_collection.find({}, {"_id": 0}).sort("timestamp", -1))
    
    if not transactions:
        st.info("No transactions recorded yet.")
        return
    
    # Transaction statistics cards
    st.markdown("<h3>Transaction Overview</h3>", unsafe_allow_html=True)
    
    # Calculate statistics
    purchase_transactions = [t for t in transactions if t.get('transaction_type') == 'purchase']
    total_volume = sum(t['price'] for t in purchase_transactions)
    avg_price = total_volume / len(purchase_transactions) if purchase_transactions else 0
    
    # Create metrics row with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TOTAL TRANSACTIONS</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{}</div>
        </div>
        """.format(len(transactions)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">TRADING VOLUME</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{:.4f} ETH</div>
        </div>
        """.format(total_volume), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">AVERAGE NFT PRICE</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{:.4f} ETH</div>
        </div>
        """.format(avg_price), unsafe_allow_html=True)
    
    with col4:
        latest_time = transactions[0]['timestamp'] if transactions else datetime.datetime.now()
        time_diff = datetime.datetime.now() - latest_time
        time_ago = f"{time_diff.seconds // 60} minutes ago" if time_diff.days == 0 else f"{time_diff.days} days ago"
        
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 5px;">LATEST TRANSACTION</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1E40AF;">{}</div>
        </div>
        """.format(time_ago), unsafe_allow_html=True)
    
    # Filter transactions
    transaction_types = ["All Types"] + list(set(t.get('transaction_type', 'unknown') for t in transactions))
    
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_type = st.selectbox("Filter by transaction type:", transaction_types)
    
    with filter_col2:
        if st.session_state.is_admin:
            show_all = st.checkbox("Show all transactions", value=True)
        else:
            show_mine = st.checkbox("Show only my transactions", value=False)
    
    # Apply filters
    filtered_transactions = transactions
    if selected_type != "All Types":
        filtered_transactions = [t for t in filtered_transactions if t.get('transaction_type') == selected_type]
    
    if not st.session_state.is_admin and show_mine:
        filtered_transactions = [t for t in filtered_transactions if t.get('buyer') == st.session_state.username or t.get('seller') == st.session_state.username]
    
    # Create a more visually appealing transaction table
    st.markdown("<h3>Transaction Records</h3>", unsafe_allow_html=True)
    
    # Create DataFrame for display
    if filtered_transactions:
        # Format the data for better display
        display_data = []
        for t in filtered_transactions:
            # Format timestamp
            formatted_time = t['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Determine transaction type styling
            tx_type = t.get('transaction_type', 'unknown')
            if tx_type == 'purchase':
                type_badge = f"<span class='badge badge-green'>Purchase</span>"
            elif tx_type == 'creation':
                type_badge = f"<span class='badge' style='background-color: #FEF3C7; color: #92400E;'>Creation</span>"
            elif tx_type == 'deposit':
                type_badge = f"<span class='badge' style='background-color: #E0E7FF; color: #3730A3;'>Deposit</span>"
            else:
                type_badge = f"<span class='badge'>{tx_type.capitalize()}</span>"
            
            # Format hash for display (truncated)
            tx_hash = t['transaction_id']
            short_hash = tx_hash[:8] + "..." + tx_hash[-8:]
            
            # Determine if current user is involved
            is_me_buyer = t.get('buyer') == st.session_state.username
            is_me_seller = t.get('seller') == st.session_state.username
            
            buyer_display = f"<span style='color: #3B82F6; font-weight: 600;'>You</span>" if is_me_buyer else t.get('buyer', 'Unknown')
            seller_display = f"<span style='color: #3B82F6; font-weight: 600;'>You</span>" if is_me_seller else t.get('seller', 'Unknown')
            
            display_data.append({
                "Time": formatted_time,
                "Type": type_badge,
                "NFT ID": t.get('nft_id', 'N/A'),
                "Buyer": buyer_display,
                "Seller": seller_display,
                "Amount (ETH)": f"{t.get('price', 0):.4f}",
                "Transaction Hash": f"<span style='font-family: monospace;'>{short_hash}</span>"
            })
        
        # Convert to DataFrame for display
        df = pd.DataFrame(display_data)
        
        # Display the formatted table
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add export option
        export_col1, export_col2 = st.columns([3, 1])
        with export_col2:
            if st.button("Export CSV", use_container_width=True):
                # Create a clean version for export (without HTML)
                export_data = []
                for t in filtered_transactions:
                    export_data.append({
                        "Timestamp": t['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                        "Transaction Type": t.get('transaction_type', 'unknown'),
                        "NFT ID": t.get('nft_id', 'N/A'),
                        "Buyer": t.get('buyer', 'Unknown'),
                        "Seller": t.get('seller', 'Unknown'),
                        "Price (ETH)": t.get('price', 0),
                        "Transaction Hash": t['transaction_id']
                    })
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                
                # Provide download link
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="nft_transactions.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.info("No transactions match your filter criteria.")

# Main Application
def main():
    """Main application function"""
    
    # Check if database is connected
    if db is None:
        st.error("Unable to connect to database. Please check your MongoDB connection.")
        return
    
    # Handle authentication state
    if not st.session_state.logged_in:
        # Display login/signup forms
        if st.session_state.page == 'signup':
            signup()
        else:
            login()
        return
    
    # Sidebar navigation menu (only shown when logged in)
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div class="logo-container">
            <span style="font-size: 32px;">🌌</span>
            <span class="logo-text">NFT Nexus</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-bottom: 20px; display: flex; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; margin-right: 10px;">
                {st.session_state.username[0].upper()}
            </div>
            <div>
                <div style="font-weight: 600; color: #1E293B;">{st.session_state.username}</div>
                <div style="font-size: 0.75rem; color: #6B7280;">{("Admin" if st.session_state.is_admin else "Collector")}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get and display user's ETH balance
        user = users_collection.find_one({"username": st.session_state.username})
        if user:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); padding: 15px; border-radius: 12px; margin-bottom: 25px;">
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); margin-bottom: 5px;">YOUR BALANCE</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">{user['eth_balance']:.4f} ETH</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("<div style='margin-bottom: 10px; font-weight: 600; color: #6B7280; font-size: 0.75rem; letter-spacing: 0.05em;'>NAVIGATION</div>", unsafe_allow_html=True)
        
        # Define menu options and icons
        menu_options = ["Marketplace", "List NFT", "My Collection", "Transactions"]
        menu_icons = ["shop", "upload", "collection", "list-task"]
        
        # Add admin option if user is admin
        if st.session_state.is_admin:
            menu_options.append("Admin")
            menu_icons.append("gear")
        
        # Add logout option
        menu_options.append("Logout")
        menu_icons.append("box-arrow-right")
        
        # Create the navigation menu
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#6B7280", "font-size": "14px"}, 
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "padding": "10px 15px", "border-radius": "10px"},
                "nav-link-selected": {"background-color": "#EFF6FF", "font-weight": "600", "color": "#3B82F6"},
            }
        )
        
        # Filter out None values
        selected = selected or "Marketplace"
        
        # Add version info at the bottom
        st.markdown("""
        <div style="position: absolute; bottom: 20px; left: 20px; font-size: 0.7rem; color: #94A3B8;">
            NFT Nexus v1.0.0
        </div>
        """, unsafe_allow_html=True)
    
    # Page content based on navigation selection
    if selected == "Marketplace":
        display_nft_marketplace()
    elif selected == "List NFT":
        list_nft()
    elif selected == "My Collection":
        my_nfts()
    elif selected == "Transactions":
        transaction_dashboard()
    elif selected == "Admin" and st.session_state.is_admin:
        admin_dashboard()
    elif selected == "Logout":
        # Show a confirmation dialog
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); text-align: center; max-width: 400px; margin: 100px auto;">
            <h2>Confirm Logout</h2>
            <p style="margin: 20px 0;">Are you sure you want to log out from NFT Nexus?</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("Yes, Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.is_admin = False
                st.session_state.page = 'login'
                st.rerun()

# Create Admin User if not exists
def create_admin_if_not_exists():
    """Create an admin user if it doesn't already exist"""
    admin_exists = users_collection.find_one({"is_admin": True})
    
    if not admin_exists and db is not None:
        admin_user = {
            "username": "admin",
            "password": hash_password("admin123"),  # Default password, should be changed
            "eth_balance": 1000.0,  # Give admin a large balance
            "is_admin": True,
            "registration_date": datetime.datetime.now()
        }
        users_collection.insert_one(admin_user)
        print("Admin user created successfully!")

# Run the application
if __name__ == "__main__":
    if db is not None:
        create_admin_if_not_exists()
    main()