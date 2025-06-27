"""
Game Controller - Orchestrates the word guessing game between all three LLM agents.

This module coordinates the interaction between:
- MainAgent: Game orchestrator and message relay
- ThinkingAgent: Selects word and answers questions
- GuessingAgent: Asks questions and makes guesses
"""

import asyncio
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from strands.models import BedrockModel

# Conditional imports for different providers
try:
    from strands.models.openai import OpenAIModel
except ImportError:
    OpenAIModel = None

try:
    from strands.models.anthropic import AnthropicModel
except ImportError:
    AnthropicModel = None

try:
    from strands.models.ollama import OllamaModel
except ImportError:
    OllamaModel = None
from .agents.main_agent import MainAgent
from .agents.thinking_agent import ThinkingAgent
from .agents.guessing_agent import GuessingAgent

# Load environment variables from .env file
load_dotenv()


class WordGuessingGame:
    """Coordinates the word guessing game between three LLM agents."""
    
    def __init__(self, model_provider: str = "openai", model_config: Dict[str, Any] = None):
        """Initialize the game with three agents.
        
        Args:
            model_provider: LLM provider to use (openai, bedrock, anthropic, ollama)
            model_config: Configuration for the LLM model
        """
        self.model_config = model_config or {}
        self.model = self._create_model(model_provider)
        
        # Initialize the three agents
        self.main_agent = MainAgent(model=self.model, port=9000)
        self.thinking_agent = ThinkingAgent(model=self.model, port=9001)
        self.guessing_agent = GuessingAgent(model=self.model, port=9002)
        
        self.game_active = False
        self.current_game_state = {}
    
    def _create_model(self, provider: str):
        """Create the appropriate model based on provider."""
        if provider == "openai":
            if OpenAIModel is None:
                raise ValueError("OpenAI support not available. Install with: pip install openai")
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider")
            
            return OpenAIModel(
                model_id=self.model_config.get("model_id", "gpt-4"),
                temperature=self.model_config.get("temperature", 0.7),
                max_tokens=self.model_config.get("max_tokens", 1000),
                api_key=api_key
            )
        
        elif provider == "anthropic":
            if AnthropicModel is None:
                raise ValueError("Anthropic support not available. Install with: pip install anthropic")
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic provider")
            
            return AnthropicModel(
                model_id=self.model_config.get("model_id", "claude-3-sonnet-20240229"),
                temperature=self.model_config.get("temperature", 0.7),
                max_tokens=self.model_config.get("max_tokens", 1000),
                api_key=api_key
            )
        
        elif provider == "bedrock":
            return BedrockModel(
                model_id=self.model_config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
                temperature=self.model_config.get("temperature", 0.7),
                max_tokens=self.model_config.get("max_tokens", 1000)
            )
        
        elif provider == "ollama":
            if OllamaModel is None:
                raise ValueError("Ollama support not available. Install Ollama locally")
            
            return OllamaModel(
                host=self.model_config.get("host", "http://localhost:11434"),
                model_id=self.model_config.get("model_id", "llama3"),
                temperature=self.model_config.get("temperature", 0.7)
            )
        
        else:
            raise ValueError(f"Unsupported model provider: {provider}")
    
    def start_new_game(self) -> str:
        """Start a new word guessing game."""
        print("🎮 Starting new word guessing game...")
        
        # 1. Main agent announces new game
        main_response = self.main_agent.process_request("Start a new word guessing game")
        print(f"📢 Main Agent: {main_response}")
        
        # 2. Thinking agent selects a word
        thinking_response = self.thinking_agent.process_request("Start a new game and select a secret animal or plant word")
        print(f"🤔 Thinking Agent: {thinking_response}")
        
        # 3. Guessing agent acknowledges game start
        guessing_response = self.guessing_agent.process_request("A new game has started. Get ready to ask your first strategic question.")
        print(f"🔍 Guessing Agent: {guessing_response}")
        
        self.game_active = True
        return "Game started successfully! All agents are ready."
    
    def play_turn(self) -> Dict[str, str]:
        """Execute one turn of the game."""
        if not self.game_active:
            return {"error": "No active game. Start a new game first."}
        
        print("\n" + "="*50)
        print("🎯 STARTING NEW TURN")
        print("="*50)
        
        # 1. Guessing agent decides on question or guess
        guessing_decision = self.guessing_agent.process_request(
            "Based on what you know so far, ask a strategic yes/no question OR make a direct guess of the word. "
            "Consider all previous answers when forming your question or guess."
        )
        print(f"🔍 Guessing Agent Decision: {guessing_decision}")
        
        # 2. Main agent processes the question/guess
        main_relay = self.main_agent.process_request(f"The guessing agent says: {guessing_decision}")
        print(f"📢 Main Agent Relay: {main_relay}")
        
        # 3. Determine if it's a question or guess and get thinking agent's response
        guessing_text = str(guessing_decision)  # Convert to string
        if "QUESTION" in guessing_text.upper() or "?" in guessing_text:
            # It's a question - get thinking agent's answer
            thinking_response = self.thinking_agent.process_request(
                f"Answer this question about your secret word with only 'yes', 'no', or 'not applicable': {guessing_text}"
            )
            print(f"🤔 Thinking Agent Answer: {thinking_response}")
            
            # Main agent relays the answer back
            main_feedback = self.main_agent.process_request(f"The thinking agent answered: {thinking_response}")
            print(f"📢 Main Agent Feedback: {main_feedback}")
            
            return {
                "type": "question",
                "guessing_agent": guessing_text,
                "thinking_agent": str(thinking_response),
                "main_agent": str(main_feedback)
            }
        
        elif "GUESS" in guessing_text.upper() or "is it" in guessing_text.lower():
            # It's a guess - get thinking agent's confirmation
            thinking_response = self.thinking_agent.process_request(
                f"Someone is guessing your secret word. Respond with 'correct' if they guessed it exactly right, or 'incorrect' if wrong: {guessing_text}"
            )
            print(f"🤔 Thinking Agent Result: {thinking_response}")
            
            # Main agent processes the result
            main_feedback = self.main_agent.process_request(f"The thinking agent says the guess result is: {thinking_response}")
            print(f"📢 Main Agent Feedback: {main_feedback}")
            
            # Check if game ended
            thinking_text = str(thinking_response)  # Convert to string
            main_feedback_text = str(main_feedback)  # Convert to string
            if "correct" in thinking_text.lower():
                self.game_active = False
                print("🎉 GAME WON!")
            elif "GAME OVER" in main_feedback_text or "maximum attempts" in main_feedback_text.lower():
                self.game_active = False
                print("😞 GAME LOST!")
            
            return {
                "type": "guess",
                "guessing_agent": guessing_text,
                "thinking_agent": thinking_text,
                "main_agent": main_feedback_text,
                "game_ended": not self.game_active
            }
        
        else:
            # Unclear input - ask for clarification
            clarification = self.guessing_agent.process_request(
                "Please clearly state either a yes/no QUESTION or make a direct GUESS of the word."
            )
            return {
                "type": "clarification",
                "guessing_agent": str(clarification)
            }
    
    def play_full_game(self, max_turns: int = 20) -> Dict[str, Any]:
        """Play a complete game with automatic turns."""
        if not self.game_active:
            self.start_new_game()
        
        game_log = []
        turn_count = 0
        
        while self.game_active and turn_count < max_turns:
            turn_count += 1
            print(f"\n🔄 TURN {turn_count}")
            
            turn_result = self.play_turn()
            game_log.append({
                "turn": turn_count,
                "result": turn_result
            })
            
            # Check if game ended
            if turn_result.get("game_ended", False):
                break
            
            # Small delay for readability
            import time
            time.sleep(1)
        
        # Get final status
        final_status = self.main_agent.process_request("Provide a final game summary")
        
        return {
            "turns_played": turn_count,
            "game_log": game_log,
            "final_status": final_status,
            "game_completed": not self.game_active
        }
    
    def get_game_status(self) -> str:
        """Get current game status from main agent."""
        return self.main_agent.process_request("What is the current game status?")
    
    def end_game(self) -> str:
        """End the current game."""
        self.game_active = False
        return self.main_agent.process_request("End the current game")


# CLI interface for the game
def main():
    """Main CLI interface for the word guessing game."""
    print("🎮 Word Guessing Game with LLM Agents")
    print("=====================================")
    
    # Initialize game
    game = WordGuessingGame()
    
    while True:
        print("\nOptions:")
        print("1. Start new game")
        print("2. Play one turn")
        print("3. Play full game (auto)")
        print("4. Get game status")
        print("5. End current game")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            result = game.start_new_game()
            print(f"\n{result}")
        
        elif choice == "2":
            if not game.game_active:
                print("No active game. Start a new game first.")
            else:
                turn_result = game.play_turn()
                print(f"\nTurn completed: {turn_result}")
        
        elif choice == "3":
            print("Playing full game automatically...")
            result = game.play_full_game()
            print(f"\nGame completed in {result['turns_played']} turns")
            print(f"Final status: {result['final_status']}")
        
        elif choice == "4":
            status = game.get_game_status()
            print(f"\n{status}")
        
        elif choice == "5":
            result = game.end_game()
            print(f"\n{result}")
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
