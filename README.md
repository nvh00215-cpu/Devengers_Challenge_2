# 🇮 Smart Bharat – AI-Powered Civic Companion


---

## 🎯 1. Chosen Vertical
**Civic Technology & Digital Governance (Smart India Initiative)**  
Smart Bharat is designed around the persona of an **Intelligent Civic Companion** for Indian citizens. It directly addresses the challenge of digital exclusion and bureaucratic complexity by providing instant, multilingual, and transparent guidance for government services, public issue reporting, and civic document navigation.

---

## 🧠 2. Approach and Logic
The solution is built on a **Dynamic Context-Aware Prompt Routing** architecture:

- **Category-Based Persona Injection:** The app features 12 civic verticals (Infrastructure, Sanitation, Documents & IDs, etc.). When a user selects a category, a specialized "Expert Persona" system prompt is dynamically injected into the AI context.
- **Rule-Enforced Prompt Engineering:** Every query is wrapped with strict transparency and inclusion rules:
  - ✅ Always state official government fees (or explicitly mark as FREE)
  - ✅ Always provide direct official portal links (UIDAI, Passport Seva, CPGRAMS)
  - ✅ Provide exact legal timelines & helpline numbers
  - ✅ Avoid bureaucratic jargon; explain terms simply
- **Multilingual Routing Logic:** The user's language preference is passed as a system constraint, forcing the AI to generate responses entirely in the selected regional language while maintaining accuracy.
- **Fallback Logic:** If no category is selected, the AI defaults to a general civic assistant persona with broad government service knowledge.

---

## ⚙️ 3. How the Solution Works
### 🔄 User Flow
1. **Category Selection:** User picks a civic issue category from the grid UI.
2. **Quick Action Trigger:** Clicking a sub-issue (e.g., "High Bills") pre-fills the chat input with a structured query.
3. **Context Assembly:** On submission, the app combines:
   - User's query
   - Category-specific expert prompt
   - Transparency & inclusion rules
   - Language preference
4. **AI Generation:** The assembled context is sent to the Google Gemini API via `google-generativeai`.
5. **Response Rendering:** The AI returns a step-by-step guide, official links, fee breakdowns, and complaint tracking steps, displayed in a clean chat interface.

### 🏗️ Technical Architecture
- **Frontend:** Streamlit (Python) for rapid, responsive, and accessible UI
- **AI Engine:** Google Gemini 3.5 Flash (`gemini-3.5-flash`) for ultra-low latency and high-efficiency inference
- **State Management:** `st.session_state` handles chat history, category selection, and quick-action pre-filling
- **Security:** API keys are strictly managed via `st.secrets` (environment variables) and never hardcoded

---

## 📝 4. Assumptions Made
1. **User Capability:** Assumes users have basic internet access and a device capable of running a modern web browser.
2. **Informational Scope:** The app acts as a **guidance advisor**, not an official government transaction portal. It directs users to verified portals rather than processing applications directly.
3. **API Stability:** Assumes the Google Gemini API remains active and rate limits are within standard free-tier allowances.
4. **Language Coverage:** Multilingual support covers major Indian languages; niche dialects may default to English or Hindi for accuracy.
5. **Real-Time Data:** Government fees, timelines, and portal links are based on current public information; users are advised to verify via official sources.

---

## 🛡️ Evaluation Focus Alignment
| Criteria          | Implementation                                                                 |
|-------------------|--------------------------------------------------------------------------------|
| **Code Quality**  | Modular structure, clear separation of UI/logic/API, well-commented functions  |
| **Security**      | Zero hardcoded secrets; keys injected via `st.secrets`; input sanitization     |
| **Efficiency**    | `gemini-3.5-flash` for optimal speed/cost; minimal dependencies; lazy loading  |
| **Testing**       | Manually validated across all 12 categories, multilingual outputs, and edge cases (empty input, API errors) |
| **Accessibility** | High-contrast UI, mobile-responsive layout, jargon-free prompts, 6-language support |

---

## ️ Tech Stack & Dependencies
- **Language:** Python 3.11
- **Framework:** Streamlit `1.36.0`
- **AI SDK:** `google-generativeai==0.8.4`
- **Deployment:** Streamlit Community Cloud
- **Model:** `gemini-3.5-flash`

---

## 🏃 How to Run Locally
```bash
# 1. Clone the repository
git clone [GitHub Repo Link]
cd smart-bharat

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key to Streamlit secrets
# Create ~/.streamlit/secrets.toml and add:
# GEMINI_API_KEY = "your_api_key_here"

# 5. Run the app
streamlit run app.py
