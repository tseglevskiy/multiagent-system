"""
Thinking Agent - Uses LLM to select a word and answer questions about it.

This agent uses an LLM to:
1. Select a random animal or plant word
2. Keep the word secret from other agents
3. Answer yes/no questions about the word intelligently
4. Confirm correct guesses
"""

from typing import Dict, Any
from strands import Agent, tool


class ThinkingAgent:
    """LLM-powered agent that thinks of a word and answers questions about it."""
    
    def __init__(self, model=None, port: int = 9001):
        self.port = port
        self.current_word = None
        self.game_active = False
        
        # System prompt for the thinking agent
        system_prompt = """You are the Thinking Agent in a word guessing game. Your role is to:

1. When asked to start a new game, secretly select ONE common animal or plant (like: dog, cat, rose, oak, etc.)
2. Keep this word completely secret - NEVER reveal it directly
3. Answer questions about your word with only "yes", "no", or "not applicable"
4. Be accurate and helpful in your answers
5. When someone guesses your word exactly, confirm if it's correct

IMPORTANT RULES:
- Only answer "yes", "no", or "not applicable" to questions
- Never reveal the word until someone guesses it correctly
- Be consistent with your answers about the same word
- Choose common, well-known animals or plants
- Remember your chosen word throughout the entire game

Current game status: No word selected yet."""

        # Create tools for the agent
        self.tools = [
            self._create_start_game_tool(),
            self._create_answer_question_tool(),
            self._create_check_guess_tool(),
            self._create_get_status_tool()
        ]
        
        # Create the Strands agent with LLM
        self.agent = Agent(
            name="ThinkingAgent",
            description="I think of animals or plants and answer yes/no questions about them",
            system_prompt=system_prompt,
            model=model,
            tools=self.tools
        )
    
    def _create_start_game_tool(self):
        """Create tool for starting a new game."""
        @tool
        def start_new_game() -> str:
            """Start a new game by selecting a secret word.
            
            Returns:
                Confirmation that a new game has started
            """
            self.game_active = True
            return "I have selected a new animal or plant for you to guess! Ask me yes/no questions or make a guess. You have 20 attempts total."
        
        return start_new_game
    
    def _create_answer_question_tool(self):
        """Create tool for answering yes/no questions."""
        @tool
        def answer_question(question: str) -> str:
            """Answer a yes/no question about the secret word.
            
            Args:
                question: A question about the secret word
                
            Returns:
                "yes", "no", or "not applicable"
            """
            if not self.game_active:
                return "not applicable - no game in progress"
            
            # The LLM will handle this through the system prompt
            return f"Question received: {question}"
        
        return answer_question
    
    def _create_check_guess_tool(self):
        """Create tool for checking word guesses."""
        @tool
        def check_guess(guess: str) -> str:
            """Check if the guessed word is correct.
            
            Args:
                guess: The guessed word
                
            Returns:
                "correct" if the guess matches, "incorrect" otherwise
            """
            if not self.game_active:
                return "not applicable - no game in progress"
            
            # The LLM will determine if the guess is correct
            return f"Guess received: {guess}"
        
        return check_guess
    
    def _create_get_status_tool(self):
        """Create tool for getting game status."""
        @tool
        def get_game_status() -> str:
            """Get the current game status.
            
            Returns:
                Current game status
            """
            if self.game_active:
                return "Game is active - I have a word selected and ready for questions"
            else:
                return "No game in progress - use start_new_game to begin"
        
        return get_game_status
    
    def process_request(self, request: str) -> str:
        """Process a request using the LLM agent."""
        return self.agent(request)
    
    def start_server(self):
        """Start the agent server (placeholder for A2A integration)."""
        print(f"ThinkingAgent server starting on port {self.port}")
        print("Ready to think of words and answer questions!")
