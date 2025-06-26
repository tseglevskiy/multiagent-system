"""
Guessing Agent - Uses LLM to ask strategic questions and make guesses.

This agent uses an LLM to:
1. Ask strategic yes/no questions to narrow down possibilities
2. Make educated guesses based on received answers
3. Keep track of previous questions and answers
4. Optimize strategy within the 20-attempt limit
"""

from typing import Dict, Any, List
from strands import Agent, tool


class GuessingAgent:
    """LLM-powered agent that asks questions and tries to guess the word."""
    
    def __init__(self, model=None, port: int = 9002):
        self.port = port
        self.game_active = False
        self.attempts_used = 0
        self.max_attempts = 20
        self.conversation_history = []
        
        # System prompt for the guessing agent
        system_prompt = """You are the Guessing Agent in a word guessing game. Your goal is to guess a secret animal or plant word in 20 attempts or less.

GAME RULES:
- The Thinking Agent has selected a common animal or plant
- You can ask yes/no questions OR make direct guesses
- Each question or guess counts as 1 attempt
- You have maximum 20 attempts total
- Questions will be answered with "yes", "no", or "not applicable"

STRATEGY TIPS:
- Start with broad categories: "Is it an animal?" "Is it a plant?"
- Then narrow down: "Is it a mammal?" "Is it a tree?" "Is it large?"
- Ask about characteristics: "Does it have fur?" "Does it have leaves?"
- Make educated guesses when you have enough information
- Keep track of all previous answers to avoid contradictions

IMPORTANT:
- Always be strategic with your questions
- Don't waste attempts on obvious or redundant questions
- When confident, make a direct guess
- Remember all previous answers when forming new questions

Current game status: No game in progress."""

        # Create tools for the agent
        self.tools = [
            self._create_ask_question_tool(),
            self._create_make_guess_tool(),
            self._create_get_status_tool(),
            self._create_start_game_tool()
        ]
        
        # Create the Strands agent with LLM
        self.agent = Agent(
            name="GuessingAgent",
            description="I ask strategic questions and try to guess the secret word",
            system_prompt=system_prompt,
            model=model,
            tools=self.tools
        )
    
    def _create_start_game_tool(self):
        """Create tool for acknowledging game start."""
        @tool
        def acknowledge_new_game() -> str:
            """Acknowledge that a new game has started.
            
            Returns:
                Confirmation and readiness to start guessing
            """
            self.game_active = True
            self.attempts_used = 0
            self.conversation_history = []
            return "Great! I'm ready to start guessing. Let me think of a good first question..."
        
        return acknowledge_new_game
    
    def _create_ask_question_tool(self):
        """Create tool for asking questions."""
        @tool
        def ask_question(question: str) -> str:
            """Ask a yes/no question about the secret word.
            
            Args:
                question: A strategic yes/no question
                
            Returns:
                Formatted question ready to send
            """
            if not self.game_active:
                return "No game in progress"
            
            if self.attempts_used >= self.max_attempts:
                return "No attempts remaining"
            
            self.attempts_used += 1
            remaining = self.max_attempts - self.attempts_used
            
            return f"QUESTION (Attempt {self.attempts_used}/{self.max_attempts}): {question} [Remaining attempts: {remaining}]"
        
        return ask_question
    
    def _create_make_guess_tool(self):
        """Create tool for making word guesses."""
        @tool
        def make_guess(word: str) -> str:
            """Make a direct guess of the secret word.
            
            Args:
                word: The word you think is the answer
                
            Returns:
                Formatted guess ready to send
            """
            if not self.game_active:
                return "No game in progress"
            
            if self.attempts_used >= self.max_attempts:
                return "No attempts remaining"
            
            self.attempts_used += 1
            remaining = self.max_attempts - self.attempts_used
            
            return f"GUESS (Attempt {self.attempts_used}/{self.max_attempts}): Is it '{word}'? [Remaining attempts: {remaining}]"
        
        return make_guess
    
    def _create_get_status_tool(self):
        """Create tool for getting game status."""
        @tool
        def get_game_status() -> str:
            """Get the current game status and attempt count.
            
            Returns:
                Current game status with attempt information
            """
            if not self.game_active:
                return "No game in progress"
            
            remaining = self.max_attempts - self.attempts_used
            return f"Game active - Used {self.attempts_used}/{self.max_attempts} attempts. {remaining} attempts remaining."
        
        return get_game_status
    
    def record_answer(self, question: str, answer: str):
        """Record a question and its answer for strategy."""
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "attempt": self.attempts_used
        })
    
    def process_request(self, request: str) -> str:
        """Process a request using the LLM agent."""
        return self.agent(request)
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history for analysis."""
        return self.conversation_history
    
    def start_server(self):
        """Start the agent server (placeholder for A2A integration)."""
        print(f"GuessingAgent server starting on port {self.port}")
        print("Ready to ask questions and make guesses!")
