#!/usr/bin/env python3
"""
Test script to verify fallback logic when Deepseek is not configured
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.deepseek_service import DeepseekAIService
from app.services.ai_service import AIProjectAnalysisService

def test_deepseek_service_states():
    """Test different states of Deepseek service configuration"""
    print("=== TESTING DEEPSEEK SERVICE STATES ===\n")
    
    # Test 1: Current configuration
    print("1. Testing current configuration:")
    current_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"   Current API Key: {current_key}")
    
    deepseek_service = DeepseekAIService()
    print(f"   Is enabled: {deepseek_service.is_enabled()}")
    print(f"   Deepseek enabled: {deepseek_service.deepseek_enabled}")
    print()
    
    # Test 2: No API key
    print("2. Testing with no API key:")
    original_key = os.environ.get("DEEPSEEK_API_KEY")
    if "DEEPSEEK_API_KEY" in os.environ:
        del os.environ["DEEPSEEK_API_KEY"]
    
    deepseek_service_no_key = DeepseekAIService()
    print(f"   Is enabled: {deepseek_service_no_key.is_enabled()}")
    print(f"   Deepseek enabled: {deepseek_service_no_key.deepseek_enabled}")
    print()
    
    # Test 3: Invalid API key
    print("3. Testing with invalid API key:")
    os.environ["DEEPSEEK_API_KEY"] = "invalid-key"
    
    deepseek_service_invalid = DeepseekAIService()
    print(f"   Is enabled: {deepseek_service_invalid.is_enabled()}")
    print(f"   Deepseek enabled: {deepseek_service_invalid.deepseek_enabled}")
    print()
    
    # Test 4: Placeholder API key
    print("4. Testing with placeholder API key:")
    os.environ["DEEPSEEK_API_KEY"] = "sk-or-v1-PLACEHOLDER-GET-FROM-OPENROUTER"
    
    deepseek_service_placeholder = DeepseekAIService()
    print(f"   Is enabled: {deepseek_service_placeholder.is_enabled()}")
    print(f"   Deepseek enabled: {deepseek_service_placeholder.deepseek_enabled}")
    print()
    
    # Restore original key
    if original_key:
        os.environ["DEEPSEEK_API_KEY"] = original_key
    elif "DEEPSEEK_API_KEY" in os.environ:
        del os.environ["DEEPSEEK_API_KEY"]

def test_ai_service_fallback():
    """Test AI service fallback behavior"""
    print("=== TESTING AI SERVICE FALLBACK ===\n")
    
    # Test with current configuration
    print("1. Testing AI service with current configuration:")
    ai_service = AIProjectAnalysisService()
    print(f"   AI enabled: {ai_service.ai_enabled}")
    print(f"   OpenAI enabled: {ai_service.openai_enabled}")
    
    mock_notice = ai_service._generate_mock_data_notice()
    print(f"   Mock data notice: '{mock_notice}'")
    print()
    
    # Test with disabled Deepseek
    print("2. Testing AI service with disabled Deepseek:")
    original_key = os.environ.get("DEEPSEEK_API_KEY")
    os.environ["DEEPSEEK_API_KEY"] = "disabled"
    
    ai_service_disabled = AIProjectAnalysisService()
    print(f"   AI enabled: {ai_service_disabled.ai_enabled}")
    print(f"   OpenAI enabled: {ai_service_disabled.openai_enabled}")
    
    mock_notice_disabled = ai_service_disabled._generate_mock_data_notice()
    print(f"   Mock data notice: '{mock_notice_disabled}'")
    print()
    
    # Restore original key
    if original_key:
        os.environ["DEEPSEEK_API_KEY"] = original_key

def test_mock_data_generation():
    """Test that mock data is generated when AI is disabled"""
    print("=== TESTING MOCK DATA GENERATION ===\n")
    
    # Temporarily disable AI
    original_key = os.environ.get("DEEPSEEK_API_KEY")
    os.environ["DEEPSEEK_API_KEY"] = "disabled"
    
    try:
        ai_service = AIProjectAnalysisService()
        print(f"AI enabled: {ai_service.ai_enabled}")
        
        # Test that mock data notice is generated
        mock_notice = ai_service._generate_mock_data_notice()
        print(f"Mock data notice: '{mock_notice}'")
        
        if mock_notice:
            print("✅ Mock data notice is correctly generated when AI is disabled")
        else:
            print("❌ Mock data notice is NOT generated when AI is disabled")
            
    finally:
        # Restore original key
        if original_key:
            os.environ["DEEPSEEK_API_KEY"] = original_key

def main():
    print("Testing Deepseek AI Fallback Logic")
    print("=" * 50)
    
    test_deepseek_service_states()
    test_ai_service_fallback()
    test_mock_data_generation()
    
    print("Testing completed!")

if __name__ == "__main__":
    main()