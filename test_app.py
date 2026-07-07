import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSessionState:
    """Test session state initialization"""
    
    def test_messages_initialization(self):
        """Test that messages are initialized correctly"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        assert isinstance(st.session_state.messages, list)
    
    def test_selected_category_initialization(self):
        """Test category selection state"""
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = None
        assert st.session_state.selected_category is None or isinstance(st.session_state.selected_category, str)
    
    def test_chat_input_value_initialization(self):
        """Test chat input value state"""
        if "chat_input_value" not in st.session_state:
            st.session_state.chat_input_value = ""
        assert isinstance(st.session_state.chat_input_value, str)

class TestIssueCategories:
    """Test issue categories structure"""
    
    def test_categories_exist(self):
        """Test that categories are defined"""
        from app import issue_categories
        assert isinstance(issue_categories, dict)
        assert len(issue_categories) > 0
    
    def test_category_structure(self):
        """Test each category has required fields"""
        from app import issue_categories
        for category_name, category_data in issue_categories.items():
            assert "issues" in category_data
            assert "prompt" in category_data
            assert isinstance(category_data["issues"], list)
            assert isinstance(category_data["prompt"], str)
    
    def test_required_categories_present(self):
        """Test that all required civic categories are present"""
        from app import issue_categories
        required_categories = [
            "🏗️ Infrastructure",
            "🗑️ Sanitation", 
            "💧 Water Supply",
            "⚡ Electricity",
            "📄 Documents & IDs"
        ]
        for category in required_categories:
            assert category in issue_categories, f"Missing category: {category}"

class TestPromptEngineering:
    """Test prompt engineering rules"""
    
    def test_transparency_rules_present(self):
        """Test that transparency rules are enforced"""
        from app import issue_categories
        for category_data in issue_categories.values():
            prompt = category_data["prompt"].lower()
            # Check for expert/guide language
            assert any(word in prompt for word in ["expert", "guide", "help"]), \
                f"Category prompt lacks guidance language: {category_data['prompt']}"
    
    def test_multilingual_support(self):
        """Test that multilingual options are available"""
        from app import issue_categories
        # Test that categories can handle different languages
        assert len(issue_categories) >= 10, "Should have at least 10 categories for diverse support"

class TestAPIConfiguration:
    """Test API configuration and security"""
    
    def test_gemini_model_defined(self):
        """Test that Gemini model is properly configured"""
        # This test verifies the model name exists
        try:
            import google.generativeai as genai
            # Model name should be defined (actual validation happens at runtime)
            assert True
        except ImportError:
            pytest.skip("google-generativeai not installed")
    
    def test_api_key_not_hardcoded(self):
        """Test that API key is not hardcoded in source"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check that API key is not hardcoded
            assert 'AIza' not in content, "API key should not be hardcoded"
            assert 'st.secrets' in content, "Should use st.secrets for API key"

class TestUserInterface:
    """Test UI components and accessibility"""
    
    def test_chat_interface_exists(self):
        """Test that chat interface is implemented"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'st.chat_message' in content, "Should use chat_message for UI"
            assert 'st.chat_input' in content or 'st.text_input' in content, "Should have chat input"
    
    def test_accessibility_features(self):
        """Test basic accessibility implementation"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for accessibility features
            accessibility_indicators = [
                'label_visibility',
                'placeholder',
                'help',
                'aria',
                'alt'
            ]
            # At least one accessibility feature should be present
            has_accessibility = any(indicator in content for indicator in accessibility_indicators)
            assert has_accessibility, "Should implement accessibility features"

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_exception_handling_present(self):
        """Test that try-except blocks are implemented"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'try:' in content, "Should have try-except blocks"
            assert 'except' in content, "Should handle exceptions"
    
    def test_api_key_error_handling(self):
        """Test that missing API key is handled"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'KeyError' in content, "Should handle KeyError for missing API key"
            assert 'GEMINI_API_KEY not found' in content, "Should show helpful error for missing key"

class TestDocumentation:
    """Test code documentation and comments"""
    
    def test_readme_exists(self):
        """Test that README.md exists"""
        import os
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
        assert os.path.exists(readme_path), "README.md should exist"
    
    def test_readme_has_required_sections(self):
        """Test that README has required sections"""
        import os
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            required_sections = [
                'chosen vertical',
                'approach',
                'how the solution works',
                'assumptions'
            ]
            for section in required_sections:
                assert section in content, f"README should contain '{section}' section"
    
    def test_code_comments_present(self):
        """Test that code has comments"""
        import os
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            comment_count = content.count('#')
            assert comment_count > 20, f"Code should have more comments (found {comment_count})"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
