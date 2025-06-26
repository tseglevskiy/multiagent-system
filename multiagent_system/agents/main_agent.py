"""
Main Agent - Orchestrates the word guessing game between thinking and guessing agents.

This agent uses an LLM to:
1. Coordinate the game flow between agents
2. Manage game state and attempt counting
3. Relay messages between thinking and guessing agents
4. Determine game outcomes (win/lose)
5. Provide game summaries and feedback
"""

from typing import Dict, Any, List
from strands import Agent, tool


class MainAgent:
    """LLM-powered main agent that orchestrates the word guessing game."""
    
    def __init__(self, model=None, port: int = 9000):
        self.port = port
        self.game_active = False
        self.attempts_used = 0
        self.max_attempts = 20
        self.game_history = []
        self.current_game_log = []
        
        # System prompt for the main agent
        system_prompt = """You are the Main Agent orchestrating a word guessing game between two other AI agents:

GAME SETUP:
- ThinkingAgent: Selects a secret animal or plant word and answers yes/no questions
- GuessingAgent: Asks strategic questions and makes guesses to find the word
- You coordinate between them and manage the game

GAME RULES:
- Maximum 20 attempts total (questions + guesses combined)
- Each question or guess counts as 1 attempt
- Questions answered with "yes", "no", or "not applicable"
- Game ends when: word is guessed correctly, or 20 attempts are used

YOUR RESPONSIBILITIES:
1. Start new games by informing both agents
2. Relay questions from GuessingAgent to ThinkingAgent
3. Relay answers from ThinkingAgent back to GuessingAgent
4. Keep accurate count of attempts used
5. Determine when game ends (win/lose)
6. Provide clear game status updates
7. Summarize game results

COMMUNICATION STYLE:
- Be clear and professional
- Keep accurate attempt counts
- Announce game state changes
- Provide helpful summaries
- Maintain game flow smoothly

Current status: No game in progress."""

        # Create tools for the agent
        self.tools = [
            self._create_start_game_tool(),
            self._create_relay_question_tool(),
            self._create_relay_guess_tool(),
            self._create_get_status_tool(),
            self._create_end_game_tool()
        ]
        
        # Create the Strands agent with LLM
        self.agent = Agent(
            name="MainAgent",
            description="I orchestrate the word guessing game between thinking and guessing agents",
            system_prompt=system_prompt,
            model=model,
            tools=self.tools
        )
    
    def _create_start_game_tool(self):
        """Create tool for starting a new game."""
        @tool
        def start_new_game() -> str:
            """Start a new word guessing game.
            
            Returns:
                Game start announcement and instructions
            """
            self.game_active = True
            self.attempts_used = 0
            self.current_game_log = []
            
            return """🎮 NEW WORD GUESSING GAME STARTED!

📋 GAME RULES:
- ThinkingAgent has selected a secret animal or plant
- GuessingAgent will ask yes/no questions and make guesses
- Maximum 20 attempts total (questions + guesses)
- Each question or guess counts as 1 attempt

🎯 OBJECTIVE: Guess the secret word within 20 attempts!

Status: Game active, 0/20 attempts used
Ready for the first question or guess!"""
        
        return start_new_game
    
    def _create_relay_question_tool(self):
        """Create tool for relaying questions between agents."""
        @tool
        def relay_question(question: str, answer: str = None) -> str:
            """Relay a question from GuessingAgent to ThinkingAgent or relay the answer back.
            
            Args:
                question: The question being asked
                answer: The answer from ThinkingAgent (if relaying back)
                
            Returns:
                Formatted relay message
            """
            if not self.game_active:
                return "❌ No game in progress. Start a new game first."
            
            if self.attempts_used >= self.max_attempts:
                return "❌ Game over - maximum attempts reached!"
            
            if answer is None:
                # Relaying question to ThinkingAgent
                self.attempts_used += 1
                remaining = self.max_attempts - self.attempts_used
                
                self.current_game_log.append({
                    "attempt": self.attempts_used,
                    "type": "question",
                    "content": question,
                    "answer": None
                })
                
                return f"📤 QUESTION #{self.attempts_used}: {question}\n⏳ Waiting for ThinkingAgent's response...\n📊 Attempts remaining: {remaining}"
            
            else:
                # Relaying answer back to GuessingAgent
                if self.current_game_log:
                    self.current_game_log[-1]["answer"] = answer
                
                remaining = self.max_attempts - self.attempts_used
                return f"📥 ANSWER: {answer}\n📊 Attempts used: {self.attempts_used}/{self.max_attempts} | Remaining: {remaining}"
        
        return relay_question
    
    def _create_relay_guess_tool(self):
        """Create tool for relaying guesses between agents."""
        @tool
        def relay_guess(guess: str, result: str = None) -> str:
            """Relay a guess from GuessingAgent to ThinkingAgent or relay the result back.
            
            Args:
                guess: The word being guessed
                result: The result from ThinkingAgent (correct/incorrect)
                
            Returns:
                Formatted relay message and game outcome if applicable
            """
            if not self.game_active:
                return "❌ No game in progress. Start a new game first."
            
            if self.attempts_used >= self.max_attempts:
                return "❌ Game over - maximum attempts reached!"
            
            if result is None:
                # Relaying guess to ThinkingAgent
                self.attempts_used += 1
                remaining = self.max_attempts - self.attempts_used
                
                self.current_game_log.append({
                    "attempt": self.attempts_used,
                    "type": "guess",
                    "content": guess,
                    "result": None
                })
                
                return f"🎯 GUESS #{self.attempts_used}: '{guess}'\n⏳ Waiting for ThinkingAgent's confirmation...\n📊 Attempts remaining: {remaining}"
            
            else:
                # Relaying result back
                if self.current_game_log:
                    self.current_game_log[-1]["result"] = result
                
                if result.lower() == "correct":
                    self.game_active = False
                    return f"""🎉 GAME WON! 
                    
✅ Correct guess: '{guess}'
🏆 Game completed in {self.attempts_used}/{self.max_attempts} attempts
🎊 Congratulations to GuessingAgent!

Game ended successfully."""
                
                else:
                    remaining = self.max_attempts - self.attempts_used
                    if remaining == 0:
                        self.game_active = False
                        return f"""😞 GAME OVER!
                        
❌ Incorrect guess: '{guess}'
📊 All {self.max_attempts} attempts used
🎯 The GuessingAgent was unable to find the word
                        
Game ended - better luck next time!"""
                    
                    return f"❌ Incorrect guess: '{guess}'\n📊 Attempts used: {self.attempts_used}/{self.max_attempts} | Remaining: {remaining}"
        
        return relay_guess
    
    def _create_get_status_tool(self):
        """Create tool for getting current game status."""
        @tool
        def get_game_status() -> str:
            """Get detailed current game status.
            
            Returns:
                Comprehensive game status report
            """
            if not self.game_active:
                return "🔴 No game in progress\n\nUse start_new_game to begin a new word guessing game."
            
            remaining = self.max_attempts - self.attempts_used
            
            status = f"""🎮 GAME STATUS REPORT
            
🟢 Game: Active
📊 Attempts: {self.attempts_used}/{self.max_attempts} used
⏳ Remaining: {remaining} attempts
            
📝 RECENT ACTIVITY:"""
            
            # Show last 3 attempts
            recent_log = self.current_game_log[-3:] if len(self.current_game_log) > 3 else self.current_game_log
            
            for entry in recent_log:
                if entry["type"] == "question":
                    status += f"\n  Q{entry['attempt']}: {entry['content']}"
                    if entry["answer"]:
                        status += f" → {entry['answer']}"
                else:  # guess
                    status += f"\n  G{entry['attempt']}: '{entry['content']}'"
                    if entry["result"]:
                        status += f" → {entry['result']}"
            
            return status
        
        return get_game_status
    
    def _create_end_game_tool(self):
        """Create tool for ending the current game."""
        @tool
        def end_game(reason: str = "Manual termination") -> str:
            """End the current game.
            
            Args:
                reason: Reason for ending the game
                
            Returns:
                Game end summary
            """
            if not self.game_active:
                return "No active game to end."
            
            self.game_active = False
            self.game_history.append({
                "attempts_used": self.attempts_used,
                "game_log": self.current_game_log.copy(),
                "end_reason": reason
            })
            
            return f"""🔚 GAME ENDED
            
Reason: {reason}
Attempts used: {self.attempts_used}/{self.max_attempts}
Total questions: {len([x for x in self.current_game_log if x['type'] == 'question'])}
Total guesses: {len([x for x in self.current_game_log if x['type'] == 'guess'])}

Game session completed."""
        
        return end_game
    
    def process_request(self, request: str) -> str:
        """Process a request using the LLM agent."""
        return self.agent(request)
    
    def get_game_history(self) -> List[Dict]:
        """Get the complete game history."""
        return self.game_history
    
    def start_server(self):
        """Start the agent server (placeholder for A2A integration)."""
        print(f"MainAgent server starting on port {self.port}")
        print("Ready to orchestrate word guessing games!")
