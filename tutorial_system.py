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
            "Count up: 4, then add 1, 2, 3, 4, 5 more numbers.",
            "4 + 5 = 9. Great job!"
        ))
        
        tutorial.add_challenge(Challenge(
            "You're doing great! What is 7 + 2?",
            "9",
            "Start from 7 and count up 2 more: 8, 9.",
            "7 + 2 = 9. Excellent work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final question: 6 + 6",
            "12",
            "This is a double! 6 + 6 is the same as 6 times 2.",
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
            "Count down from 9: subtract 1, 2, 3, 4.",
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
            "Start at 10 and count backward 6 times.",
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
            "2 x 3 means 2 + 2 + 2. Add 2, three times.",
            "2 x 3 = 6. That's 2 added 3 times!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Great! Now try: 3 x 4",
            "12",
            "3 x 4 means 3 + 3 + 3 + 3.",
            "3 x 4 = 12. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 2 x 5?",
            "10",
            "Add 2 five times: 2 + 2 + 2 + 2 + 2.",
            "2 x 5 = 10. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 4 x 3",
            "12",
            "4 x 3 means 4 + 4 + 4.",
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
            "Add the ones: 2 + 5 = 7. Add the tens: 10 + 10 = 20. Total: 27.",
            "12 + 15 = 27. Great work with two-digit numbers!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Now try: 23 + 34",
            "57",
            "Ones: 3 + 4 = 7. Tens: 20 + 30 = 50. Total: 57.",
            "23 + 34 = 57. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Here's a tricky one: 28 + 17",
            "45",
            "Ones: 8 + 7 = 15 (carry the 1). Tens: 20 + 10 + 10 = 40. Total: 45.",
            "28 + 17 = 45. You handled carrying correctly!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 46 + 39",
            "85",
            "Ones: 6 + 9 = 15 (carry 1). Tens: 40 + 30 + 10 = 80. Total: 85.",
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
            "Ones: 5 - 3 = 2. Tens: 40 - 20 = 20. Total: 22.",
            "45 - 23 = 22. Great start!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 67 - 34",
            "33",
            "Ones: 7 - 4 = 3. Tens: 60 - 30 = 30. Total: 33.",
            "67 - 34 = 33. Well done!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Here's a challenge with borrowing: 52 - 28",
            "24",
            "Ones: 12 - 8 = 4 (borrowed 1). Tens: 40 - 20 = 20. Total: 24.",
            "52 - 28 = 24. You handled borrowing perfectly!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Last one: 81 - 47",
            "34",
            "Ones: 11 - 7 = 4 (borrowed). Tens: 70 - 40 = 30. Total: 34.",
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
            "5 x 6 = 5 + 5 + 5 + 5 + 5 + 5. Count by 5s: 5, 10, 15, 20, 25, 30.",
            "5 x 6 = 30. Excellent!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 7 x 4?",
            "28",
            "7 x 4 = 7 + 7 + 7 + 7. Or think of it as 4 x 7 = 28.",
            "7 x 4 = 28. Great work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 8 x 6",
            "48",
            "8 x 6 = 8 + 8 + 8 + 8 + 8 + 8. Or 6 x 8 = 48.",
            "8 x 6 = 48. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 9 x 7",
            "63",
            "9 x 7. Tip: 9 x 7 = (10 x 7) - 7 = 70 - 7 = 63.",
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
            "Remember: Multiply first! 3 x 2 = 6, then 5 + 6 = 11.",
            "5 + 3 x 2 = 11. Multiplication comes before addition!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 10 - 4 + 6?",
            "12",
            "Work left to right: 10 - 4 = 6, then 6 + 6 = 12.",
            "10 - 4 + 6 = 12. Great job with left-to-right operations!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 15 - 2 x 3",
            "9",
            "Multiply first: 2 x 3 = 6. Then 15 - 6 = 9.",
            "15 - 2 x 3 = 9. You remembered to multiply first!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 4 x 5 - 8",
            "12",
            "Multiply first: 4 x 5 = 20. Then 20 - 8 = 12.",
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
            "Parentheses first: 3 + 2 = 5. Then 5 x 4 = 20.",
            "(3 + 2) x 4 = 20. Parentheses come first!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 2 x (8 - 3)?",
            "10",
            "Parentheses first: 8 - 3 = 5. Then 2 x 5 = 10.",
            "2 x (8 - 3) = 10. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 20 - (4 + 6)",
            "10",
            "Parentheses first: 4 + 6 = 10. Then 20 - 10 = 10.",
            "20 - (4 + 6) = 10. Excellent work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Challenge: 3 x 4 + (10 - 2)",
            "20",
            "Parentheses first: 10 - 2 = 8. Then multiply: 3 x 4 = 12. Finally: 12 + 8 = 20.",
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
            "10 divided by 2 means: split 10 into 2 equal groups. Each group has 5.",
            "10 / 2 = 5. Division is splitting equally!"
        ))
        
        tutorial.add_challenge(Challenge(
            "What is 15 / 3?",
            "5",
            "15 divided by 3: how many 3s fit into 15? Count: 3, 6, 9, 12, 15. That's 5 threes!",
            "15 / 3 = 5. Perfect!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Try this: 24 / 4",
            "6",
            "24 divided by 4. Think: 4 x ? = 24. The answer is 6!",
            "24 / 4 = 6. Great work!"
        ))
        
        tutorial.add_challenge(Challenge(
            "Final challenge: 36 / 6",
            "6",
            "36 divided by 6. Count by 6s: 6, 12, 18, 24, 30, 36. That's 6 sixes!",
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
