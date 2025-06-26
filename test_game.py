#!/usr/bin/env python3
"""
Simple test script for the word guessing game.
This script tests the basic functionality without requiring full LLM setup.
"""

import sys
import os

# Add the project to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_agent_imports():
    """Test that all agent classes can be imported."""
    try:
        from multiagent_system.agents.main_agent import MainAgent
        from multiagent_system.agents.thinking_agent import ThinkingAgent
        from multiagent_system.agents.guessing_agent import GuessingAgent
        print("✅ All agent classes imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_game_controller_import():
    """Test that the game controller can be imported."""
    try:
        from multiagent_system.game_controller import WordGuessingGame
        print("✅ Game controller imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Game controller import error: {e}")
        return False

def test_basic_agent_creation():
    """Test basic agent creation without LLM."""
    try:
        from multiagent_system.agents.main_agent import MainAgent
        from multiagent_system.agents.thinking_agent import ThinkingAgent
        from multiagent_system.agents.guessing_agent import GuessingAgent
        
        # Create agents without LLM model (will use default)
        main_agent = MainAgent(model=None)
        thinking_agent = ThinkingAgent(model=None)
        guessing_agent = GuessingAgent(model=None)
        
        print("✅ All agents created successfully")
        print(f"   - MainAgent: {main_agent.agent.name}")
        print(f"   - ThinkingAgent: {thinking_agent.agent.name}")
        print(f"   - GuessingAgent: {guessing_agent.agent.name}")
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Multi-Agent Word Guessing Game")
    print("=" * 40)
    
    tests = [
        test_agent_imports,
        test_game_controller_import,
        test_basic_agent_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n🔍 Running {test.__name__}...")
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The game structure is ready.")
        print("\n🚀 Next steps:")
        print("   1. Configure your LLM provider (AWS Bedrock, OpenAI, etc.)")
        print("   2. Set up environment variables in .env file")
        print("   3. Run: uv run multiagent play")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
