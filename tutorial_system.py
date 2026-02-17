# Tutorial System for Virtual Taylor Frame
# Provides interactive math lessons for visually impaired students

import json


class Tutorial:
    """Base class for interactive math tutorials"""
    
    def __init__(self, title, description, difficulty):
        self.title = title
        self.description = description
        self.difficulty = difficulty  # "easy", "medium", "hard"
        self.challenges = []
        self.current_challenge = 0
        self.score = 0
        
    def add_challenge(self, challenge):
        """Add a challenge to this tutorial"""
        self.challenges.append(challenge)
        
    def get_current_challenge(self):
        """Get the current challenge"""
        if self.current_challenge < len(self.challenges):
            return self.challenges[self.current_challenge]
        return None
        
    def next_challenge(self):
        """Move to the next challenge"""
        self.current_challenge += 1
        
    def is_complete(self):
        """Check if all challenges are complete"""
        return self.current_challenge >= len(self.challenges)
        
    def get_progress(self):
        """Get progress as a tuple (current, total)"""
        return (self.current_challenge, len(self.challenges))


class Challenge:
    """A single math challenge within a tutorial"""
    
    def __init__(self, question, answer, hint=None, explanation=None):
        self.question = question
        self.answer = str(answer).strip()
        self.hint = hint
        self.explanation = explanation
        self.attempts = 0
        self.max_attempts = 3
        
    def check_answer(self, user_answer):
        """Check if the user's answer is correct"""
        self.attempts += 1
        # Normalize the answer (remove spaces, handle different formats)
        normalized_user = str(user_answer).strip().replace(" ", "")
        normalized_correct = self.answer.replace(" ", "")
        return normalized_user == normalized_correct
        
    def get_hint(self):
        """Get a hint for this challenge"""
        return self.hint if self.hint else "Think carefully about the problem."
        
    def needs_hint(self):
        """Check if a hint should be offered"""
        return self.attempts >= 2 and self.hint is not None


class TutorialLibrary:
    """Library of all available tutorials"""
    
    def __init__(self):
        self.tutorials = []
        self._create_tutorials()
        
    def _create_tutorials(self):
        """Create all tutorials"""
        # Easy tutorials for primary students
        self._create_easy_addition()
        self._create_easy_subtraction()
        self._create_easy_multiplication()
        
        # Medium tutorials
        self._create_medium_addition()
        self._create_medium_subtraction()
        self._create_medium_multiplication()
        
        # Hard tutorials for intermediate students
        self._create_hard_mixed_operations()
        self._create_hard_order_of_operations()
        self._create_hard_division()
        
    def _create_easy_addition(self):
        """Tutorial 1: Single digit addition"""
        tutorial = Tutorial(
            "Single Digit Addition",
            "Learn to add single digit numbers. Place your answer in the grid and press Ctrl+Enter to check.",
            "easy"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's start simple. What is 2 + 3?",
            "5",
            "Think: If you have 2 apples and get 3 more, how many do you have?",
            "2 + 3 = 5. When you add 2 and 3, you get 5!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Good! Now try: 4 + 5",
            "9",
            "Count up: Start from 4, then count 5 more numbers.",
            "4 + 5 = 9. Great job!"
        ))
        
        tutorial.add_challenge(Challenge(
            "You're doing great! What is 7 + 2?",
            "9",
            "Start from 7 and count up 2 more numbers.",
            "7 + 2 = 9. Excellent work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final question: 6 + 6",
            "12",
            "This is a double! Think about what 6 + 6 means.",
            "6 + 6 = 12. Perfect! You completed single digit addition!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_easy_subtraction(self):
        """Tutorial 2: Single digit subtraction"""
        tutorial = Tutorial(
            "Single Digit Subtraction",
            "Learn to subtract single digit numbers.",
            "easy"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's subtract! What is 8 - 3?",
            "5",
            "If you have 8 cookies and eat 3, how many are left?",
            "8 - 3 = 5. You got it!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Good work! Now try: 9 - 4",
            "5",
            "Count down from 9 by taking away 4.",
            "9 - 4 = 5. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 7 - 7?",
            "0",
            "When you take away the same number, what's left?",
            "7 - 7 = 0. When you subtract a number from itself, you get zero!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Last one: 10 - 6",
            "4",
            "Start at 10 and count backward, taking away 6.",
            "10 - 6 = 4. You've mastered single digit subtraction!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_easy_multiplication(self):
        """Tutorial 3: Simple multiplication"""
        tutorial = Tutorial(
            "Multiplication Basics",
            "Learn multiplication with the 2 and 3 times tables.",
            "easy"
        )
        
        tutorial.add_challenge(Challenge(
            "Multiplication is repeated addition. What is 2 x 3?",
            "6",
            "2 times 3 means adding 2, three times. Try it!",
            "2 x 3 = 6. That's 2 added 3 times!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Great! Now try: 3 x 4",
            "12",
            "3 times 4 means adding 3, four times.",
            "3 x 4 = 12. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 2 x 5?",
            "10",
            "Add 2 to itself five times.",
            "2 x 5 = 10. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 4 x 3",
            "12",
            "4 times 3 means adding 4, three times.",
            "4 x 3 = 12. You've learned the basics of multiplication!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_medium_addition(self):
        """Tutorial 4: Two digit addition"""
        tutorial = Tutorial(
            "Two Digit Addition",
            "Learn to add two-digit numbers.",
            "medium"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's add bigger numbers! What is 12 + 15?",
            "27",
            "Add the ones first, then the tens.",
            "12 + 15 = 27. Great work with two-digit numbers!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Now try: 23 + 34",
            "57",
            "Remember to add ones place first, then tens place.",
            "23 + 34 = 57. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Here's a tricky one: 28 + 17",
            "45",
            "When ones add up to more than 10, carry to the tens place.",
            "28 + 17 = 45. You handled carrying correctly!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 46 + 39",
            "85",
            "Add ones place: if it's more than 10, remember to carry!",
            "46 + 39 = 85. You've mastered two-digit addition!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_medium_subtraction(self):
        """Tutorial 5: Two digit subtraction"""
        tutorial = Tutorial(
            "Two Digit Subtraction",
            "Learn to subtract two-digit numbers.",
            "medium"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's subtract larger numbers. What is 45 - 23?",
            "22",
            "Subtract the ones first, then the tens.",
            "45 - 23 = 22. Great start!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 67 - 34",
            "33",
            "Remember: ones place first, then tens place.",
            "67 - 34 = 33. Well done!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Here's a challenge with borrowing: 52 - 28",
            "24",
            "When ones digit is smaller, you need to borrow from tens.",
            "52 - 28 = 24. You handled borrowing perfectly!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Last one: 81 - 47",
            "34",
            "Check if you need to borrow before subtracting.",
            "81 - 47 = 34. You've mastered two-digit subtraction!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_medium_multiplication(self):
        """Tutorial 6: Larger multiplication"""
        tutorial = Tutorial(
            "Multiplication Tables",
            "Practice multiplication up to 10.",
            "medium"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's practice the 5 times table. What is 5 x 6?",
            "30",
            "Count by 5s six times, or add 5 to itself 6 times.",
            "5 x 6 = 30. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 7 x 4?",
            "28",
            "7 times 4 means adding 7 four times.",
            "7 x 4 = 28. Great work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 8 x 6",
            "48",
            "8 times 6 means adding 8 six times.",
            "8 x 6 = 48. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 9 x 7",
            "63",
            "Tip: Think of (10 x 7) minus 7.",
            "9 x 7 = 63. You've mastered multiplication tables!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_hard_mixed_operations(self):
        """Tutorial 7: Mixed operations"""
        tutorial = Tutorial(
            "Mixed Operations",
            "Practice problems with addition, subtraction, and multiplication together.",
            "hard"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's combine operations! What is 5 + 3 x 2?",
            "11",
            "Remember: Do multiplication before addition!",
            "5 + 3 x 2 = 11. Multiplication comes before addition!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 10 - 4 + 6?",
            "12",
            "When operations are the same level, work left to right.",
            "10 - 4 + 6 = 12. Great job with left-to-right operations!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 15 - 2 x 3",
            "9",
            "Which operation should you do first?",
            "15 - 2 x 3 = 9. You remembered to multiply first!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 4 x 5 - 8",
            "12",
            "Think about order of operations.",
            "4 x 5 - 8 = 12. You've mastered mixed operations!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_hard_order_of_operations(self):
        """Tutorial 8: Order of operations (PEMDAS)"""
        tutorial = Tutorial(
            "Order of Operations",
            "Learn PEMDAS: Parentheses, Exponents, Multiplication/Division, Addition/Subtraction.",
            "hard"
        )
        
        tutorial.add_challenge(Challenge(
            "Let's learn PEMDAS! What is (3 + 2) x 4?",
            "20",
            "Do what's inside parentheses first.",
            "(3 + 2) x 4 = 20. Parentheses come first!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 2 x (8 - 3)?",
            "10",
            "Remember: Solve inside parentheses before multiplying.",
            "2 x (8 - 3) = 10. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 20 - (4 + 6)",
            "10",
            "What should you calculate first?",
            "20 - (4 + 6) = 10. Excellent work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Challenge: 3 x 4 + (10 - 2)",
            "20",
            "Use PEMDAS: Parentheses first, then multiplication, then addition.",
            "3 x 4 + (10 - 2) = 20. You've mastered order of operations!"
        ))
        
        self.tutorials.append(tutorial)
        
    def _create_hard_division(self):
        """Tutorial 9: Division basics"""
        tutorial = Tutorial(
            "Division Basics",
            "Learn to divide numbers evenly.",
            "hard"
        )
        
        tutorial.add_challenge(Challenge(
            "Division is splitting into equal parts. What is 10 / 2?",
            "5",
            "10 divided by 2 means: split 10 into 2 equal groups.",
            "10 / 2 = 5. Division is splitting equally!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 15 / 3?",
            "5",
            "How many groups of 3 fit into 15?",
            "15 / 3 = 5. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 24 / 4",
            "6",
            "Think: 4 times what number equals 24?",
            "24 / 4 = 6. Great work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 36 / 6",
            "6",
            "How many 6s make 36?",
            "36 / 6 = 6. You've learned division basics!"
        ))
        
        self.tutorials.append(tutorial)
        
    def get_tutorials_by_difficulty(self, difficulty):
        """Get all tutorials of a specific difficulty"""
        return [t for t in self.tutorials if t.difficulty == difficulty]
        
    def get_all_tutorials(self):
        """Get all tutorials"""
        return self.tutorials
        
    def get_tutorial(self, index):
        """Get a specific tutorial by index"""
        if 0 <= index < len(self.tutorials):
            return self.tutorials[index]
        return None
