import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Bharat - Civic Companion", page_icon="🇮🇳", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #FF9933; text-align: center; font-weight: bold; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #138808; text-align: center; margin-bottom: 2rem; }
    .category-card { background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #e9ecef; transition: all 0.3s; }
    .category-card:hover { border-color: #FF9933; background: #fff3e0; }
    .selected-card { background: #e8f5e9; border-color: #138808; }
    .footer { text-align: center; color: gray; font-size: 0.85rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# --- ISSUE CATEGORIES & PROMPTS ---
issue_categories = {
    "🏗️ Infrastructure": {
        "issues": ["Potholes & Roads", "Street Lights", "Bridges & Flyovers", "Footpaths", "Public Parks"],
        "prompt": "You are an infrastructure expert for Indian cities. Help citizens report and track issues related to roads, streetlights, and public spaces. Guide them to municipal corporation portals."
    },
    "🗑️ Sanitation": {
        "issues": ["Garbage Collection", "Drainage & Sewage", "Public Toilets", "Street Cleaning", "Mosquito Menace"],
        "prompt": "You are a sanitation expert. Help citizens report garbage, drainage, and sewage issues. Guide them to municipal health departments and explain waste segregation rules."
    },
    "💧 Water Supply": {
        "issues": ["No Water Supply", "Low Pressure", "Contaminated Water", "Water Tanker", "Pipeline Leakage"],
        "prompt": "You are a water utilities expert. Help citizens report water issues, book tankers, and check water quality. Guide them to local water boards."
    },
    " Electricity": {
        "issues": ["Power Cuts", "High Bills", "Meter Issues", "New Connection", "Voltage Problems"],
        "prompt": "You are an electricity services expert. Help citizens report outages, dispute bills, and apply for connections. Guide them to local discoms."
    },
    "🚗 Traffic & Transport": {
        "issues": ["Traffic Violations", "Public Transport", "Parking Problems", "Accident Reporting", "Challan Disputes"],
        "prompt": "You are a traffic and transport expert. Help citizens report violations, public transport issues, and guide them to traffic police and RTO portals."
    },
    "🛡️ Safety & Security": {
        "issues": ["Theft & Burglary", "Women Safety", "Cyber Crime", "Domestic Violence", "Harassment"],
        "prompt": "You are a public safety expert. Help citizens report crimes and get emergency assistance. Guide them to police portals and women helplines (1091, 181). Prioritize emergency contacts."
    },
    "🌳 Environment": {
        "issues": ["Air Pollution", "Noise Pollution", "Illegal Encroachment", "Tree Cutting", "Industrial Waste"],
        "prompt": "You are an environmental expert. Help citizens report pollution and environmental violations. Guide them to State Pollution Control Boards."
    },
    "🏥 Health Services": {
        "issues": ["Hospital Services", "Vaccination", "Ayushman Bharat", "Medicine Availability", "Ambulance"],
        "prompt": "You are a public health expert. Help citizens access government hospitals, Ayushman Bharat benefits, and emergency medical services (108)."
    },
    "🎓 Education": {
        "issues": ["School Admissions", "Scholarships", "Mid-Day Meal", "School Infrastructure", "Teacher Complaints"],
        "prompt": "You are an education expert. Help citizens with school admissions, scholarships, and RTE Act information. Guide them to state education departments."
    },
    "🌾 Agriculture": {
        "issues": ["PM-KISAN", "Crop Insurance", "Irrigation Issues", "Subsidies & Loans", "MSP Information"],
        "prompt": "You are an agriculture expert. Help farmers access PM-KISAN, crop insurance (PMFBY), and subsidies. Guide them to agriculture department portals."
    },
    "🏠 Housing & Property": {
        "issues": ["Building Permissions", "Property Tax", "Rent Agreement", "Illegal Construction", "Land Disputes"],
        "prompt": "You are a housing and property expert. Help citizens with building permissions, property tax, and rent agreements. Guide them to municipal and revenue departments."
    },
    " Documents & IDs": {
        "issues": ["Aadhaar Card", "PAN Card", "Passport", "Voter ID", "Driving License"],
        "prompt": "You are a government documentation expert. Help citizens with Aadhaar, PAN, passport, voter ID, and driving license. Guide them to UIDAI, NSDL, Passport Seva, NVSP, and Sarathi portals."
    }
}

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": " नमस्ते! Welcome to **Smart Bharat**! I'm your AI civic companion.\n\nI can help you:\n• Report public issues (potholes, garbage, water)\n• Navigate government services (Aadhaar, PAN, Passport)\n• File and track complaints\n\nSelect a category below or just type your question!"}
    ]

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

if "quick_action_query" not in st.session_state:
    st.session_state.quick_action_query = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    language = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "हिंदी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)", "मराठी (Marathi)"]
    )
    
    st.divider()
    
    if st.session_state.selected_category:
        st.success(f"**Active Category:**\n{st.session_state.selected_category}")
        if st.button("🔄 Clear Category", use_container_width=True):
            st.session_state.selected_category = None
            st.session_state.quick_action_query = ""
            st.rerun()
    else:
        st.info("No specific category selected.")
        
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_action_query = ""
        st.rerun()

# --- MAIN HEADER ---
st.markdown('<div class="main-header">🇮🇳 Smart Bharat</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Civic Companion</div>', unsafe_allow_html=True)

# --- CATEGORY SELECTION UI ---
st.subheader(" Select Issue Category")
cols = st.columns(4)
category_keys = list(issue_categories.keys())

for idx, col in enumerate(cols):
    with col:
        for i in range(3):
            cat_idx = idx * 3 + i
            if cat_idx < len(category_keys):
                cat_name = category_keys[cat_idx]
                
                if st.button(cat_name, key=f"cat_{cat_idx}", use_container_width=True):
                    st.session_state.selected_category = cat_name
                    st.session_state.quick_action_query = ""
                    st.rerun()

# --- SUB-ISSUE QUICK ACTIONS ---
if st.session_state.selected_category:
    st.divider()
    selected_cat = st.session_state.selected_category
    cat_data = issue_categories[selected_cat]
    
    st.subheader(f" Quick Actions for {selected_cat}")
    sub_cols = st.columns(min(len(cat_data['issues']), 5))
    
    for idx, issue in enumerate(cat_data['issues']):
        with sub_cols[idx % len(sub_cols)]:
            if st.button(issue, key=f"issue_{idx}", use_container_width=True):
                st.session_state.quick_action_query = f"I am facing an issue with {issue}. How do I report this and get it resolved?"
                st.rerun()

# --- GEMINI API SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash') 
except KeyError:
    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets! Please add it in the app settings.")
    st.stop()

# --- CHAT INTERFACE ---
st.divider()
st.subheader("💬 Chat with Civic Assistant")

# 1. Display all previous messages first
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle Quick Action Input (Pre-filled)
if st.session_state.quick_action_query:
    st.info("📝 **Quick Action:** Edit the message below if needed, then click Send!")
    
    user_input = st.text_input(
        "Your Message:",
        value=st.session_state.quick_action_query,
        label_visibility="collapsed",
        key="qa_text_input"
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("➤ Send", use_container_width=True, type="primary", key="btn_send_qa"):
            if user_input.strip():
                # Show user message immediately
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # Show AI thinking and response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("🤔 *Thinking...*")
                    
                    try:
                        # Build prompt
                        if st.session_state.selected_category:
                            base_prompt = issue_categories[st.session_state.selected_category]['prompt']
                        else:
                            base_prompt = "You are a helpful civic assistant for Indian citizens."
                        
                        transparency_rules = """
                        TRANSPARENCY RULES:
                        1. ALWAYS state the exact OFFICIAL GOVERNMENT FEE (or explicitly state if it is FREE).
                        2. ALWAYS provide the exact official government website link.
                        3. Provide the exact official timeline.
                        4. For complaints, guide them to use the CPGRAMS portal.
                        """
                        
                        inclusion_rules = """
                        DIGITAL INCLUSION RULES:
                        1. Avoid heavy bureaucratic jargon.
                        2. Break down complex processes into small steps.
                        3. If language is not English, respond in that language.
                        """
                        
                        full_prompt = f"{base_prompt}\n\n{transparency_rules}\n\n{inclusion_rules}\n\nLanguage: {language}\n\nQuery: {user_input}"
                        
                        # Generate response
                        chat = model.start_chat(history=[])
                        response = chat.send_message(full_prompt)
                        
                        # Show response
                        message_placeholder.markdown(response.text)
                        
                        # Save to history
                        st.session_state.messages.append({"role": "user", "content": user_input})
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        
                        # Clear the quick action query
                        st.session_state.quick_action_query = ""
                        
                        # CRITICAL FIX: Rerun the app to move the input bar to the bottom
                        st.rerun()
                        
                    except Exception as e:
                        message_placeholder.error(f"Error: {e}")

    with col2:
        if st.button(" Cancel", use_container_width=True, key="btn_cancel_qa"):
            st.session_state.quick_action_query = ""
            st.rerun()

# 3. Handle Regular Chat Input (Only shows if no Quick Action is pending)
else:
    if prompt := st.chat_input("Ask about government services, file a complaint, or get help..."):
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Show AI thinking and response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 *Thinking...*")
            
            try:
                # Build prompt
                if st.session_state.selected_category:
                    base_prompt = issue_categories[st.session_state.selected_category]['prompt']
                else:
                    base_prompt = "You are a helpful civic assistant for Indian citizens."
                
                transparency_rules = """
                TRANSPARENCY RULES:
                1. ALWAYS state the exact OFFICIAL GOVERNMENT FEE (or explicitly state if it is FREE).
                2. ALWAYS provide the exact official government website link.
                3. Provide the exact official timeline.
                4. For complaints, guide them to use the CPGRAMS portal.
                """
                
                inclusion_rules = """
                DIGITAL INCLUSION RULES:
                1. Avoid heavy bureaucratic jargon.
                2. Break down complex processes into small steps.
                3. If language is not English, respond in that language.
                """
                
                full_prompt = f"{base_prompt}\n\n{transparency_rules}\n\n{inclusion_rules}\n\nLanguage: {language}\n\nQuery: {prompt}"
                
                # Generate response
                chat = model.start_chat(history=[])
                response = chat.send_message(full_prompt)
                
                # Show response
                message_placeholder.markdown(response.text)
                
                # Save to history
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                message_placeholder.error(f"Error: {e}")

# --- FOOTER ---
st.markdown("""
<div class="footer">
<b>Smart Bharat Initiative</b> | Promoting Transparency, Accessibility & Digital Inclusion<br>
Built with ❤️ for Devengers PromptWars 2026 | Powered by Google Gemini
</div>
""", unsafe_allow_html=True)
