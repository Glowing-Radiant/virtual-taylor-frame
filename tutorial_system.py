# Tutorial System for Virtual Taylor Frame
# Provides interactive math lessons for visually impaired students

import random


class Challenge:
    """A single math challenge within a tutorial"""

    def __init__(self, question, answer, hint=None, explanation=None):
        self.question = question
        self.answer = str(answer).strip()
        self.hint = hint
        self.explanation = explanation
        self.attempts = 0
        self.max_attempts = 3
        self.hint_used = False

    def check_answer(self, user_answer):
        """Check if the user's answer is correct"""
        self.attempts += 1
        # Normalize the answer (remove spaces, handle different formats)
        normalized_user = str(user_answer).strip().replace(" ", "")
        normalized_correct = self.answer.replace(" ", "")
        return normalized_user == normalized_correct

    def get_hint(self):
        """Get a hint for this challenge"""
        self.hint_used = True
        return self.hint if self.hint else "Think carefully about the problem."

    def needs_hint(self):
        """Check if a hint should be offered"""
        return self.attempts >= 2 and self.hint is not None


class Tutorial:
    """A tutorial made up of freshly-generated challenges each playthrough"""

    def __init__(self, tutorial_id, title, description, difficulty,
                 challenge_generator=None, challenge_count=4):
        self.id = tutorial_id
        self.title = title
        self.description = description
        self.difficulty = difficulty  # "easy", "medium", "hard"
        self.challenge_generator = challenge_generator
        self.challenge_count = challenge_count
        self.challenges = []
        self.current_challenge = 0

    def add_challenge(self, challenge):
        """Add a challenge to this tutorial (manual/test construction)"""
        self.challenges.append(challenge)

    def generate_challenges(self, rng=None):
        """(Re)generate this tutorial's challenges, resetting progress.

        Called at the start of every playthrough so replaying a tutorial
        presents fresh numbers instead of the same fixed problems.
        """
        if self.challenge_generator is not None:
            rng = rng or random.Random()
            self.challenges = self.challenge_generator(rng, self.challenge_count)
        self.current_challenge = 0
        return self.challenges

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

    def compute_stars(self):
        """Rate mastery of the just-completed run as 1-3 stars.

        Each challenge scores 3 (solved first try, no hint), 2 (solved
        within 2 attempts or used one hint), or 1 (struggled more than
        that). The tutorial's stars are the rounded average, clamped to
        [1, 3]. Meaningful once is_complete() is True.
        """
        if not self.challenges:
            return 0
        total = 0
        for challenge in self.challenges:
            if challenge.attempts <= 1 and not challenge.hint_used:
                total += 3
            elif challenge.attempts <= 2 and not challenge.hint_used:
                total += 2
            else:
                total += 1
        stars = round(total / len(self.challenges))
        return max(1, min(3, stars))


def _sample_until(rng, make, predicate, max_tries=500):
    """Rejection-sample from `make(rng)` until `predicate` holds."""
    candidate = None
    for _ in range(max_tries):
        candidate = make(rng)
        if predicate(candidate):
            return candidate
    return candidate


# ---------------------------------------------------------------------------
# Orientation tutorial: introduces the frame's own controls, not math
# ---------------------------------------------------------------------------

def _gen_basics_intro(rng, count):
    """Fixed, non-random walkthrough of the frame's core controls.

    Unlike the math generators, this always returns the same sequence -
    it's teaching the interface itself, so there's nothing to randomize.
    `rng` and `count` are accepted only to match the challenge_generator
    signature every other tutorial uses.
    """
    return [
        Challenge(
            "Welcome to the Virtual Taylor Frame! This grid is where you write "
            "numbers and math, one character per cell. Let's start simple: type "
            "the number 5, then press Control plus Enter to check your answer.",
            "5",
            "Press the 5 key, then hold Control and press Enter.",
            "Every key you press fills the current cell, and the frame speaks "
            "each character back to you as you type."
        ),
        Challenge(
            "Notice how the cursor moved to the right by itself after you typed? "
            "That's Auto-shift, and you can turn it on or off anytime with F2. "
            "Let's use it: type 12, then press Control plus Enter.",
            "12",
            "Type 1, then 2. With auto-shift on, you don't need to press the "
            "right arrow key in between.",
            "12 = 12. With auto-shift on, typing several digits in a row "
            "automatically advances the cursor for you, just like writing on paper."
        ),
        Challenge(
            "You can also move the cursor yourself. Type 1, then press the Right "
            "Arrow key twice to leave a gap, then type 2. Press Control plus "
            "Enter when you're ready.",
            "12",
            "Type 1, tap the right arrow key twice, then type 2.",
            "Even with a gap between them, the frame reads 1 and 2 together as "
            "12. Manual navigation lets you space things out however you like."
        ),
        Challenge(
            "Mistakes are easy to fix. Type 9, press Backspace to delete it, "
            "then type 8 and press Control plus Enter.",
            "8",
            "Backspace clears whatever is in the current cell.",
            "Backspace deletes the current cell. Turn on Smart Delete with F3 "
            "and Backspace will also hop back to erase the previous cell when "
            "the current one is already empty - handy for quick corrections."
        ),
        Challenge(
            "You can always ask the frame to read things back to you: Alt plus "
            "L reads the whole current line. For now, type 3, then press "
            "Control plus Enter to finish this one.",
            "3",
            "Type 3, then Control+Enter. Try Alt+L first just to hear how it works.",
            "Alt+L reads the current row, and F1 opens a full list of every "
            "keyboard shortcut whenever you need a reminder."
        ),
        Challenge(
            "Outside of tutorials, you can do math right on the grid. Type 2+2 "
            "exactly like that, then press Control plus Enter to finish this "
            "tutorial.",
            "2+2",
            "Type the characters 2, plus, 2 - it doesn't need to be solved for "
            "this exercise.",
            "In Normal Mode, pressing Control+Enter on a row like 2+2 evaluates "
            "it instantly and writes = 4 right after it. Give it a try once you "
            "leave tutorial mode!"
        ),
    ]


# ---------------------------------------------------------------------------
# Easy tutorials (primary level)
# ---------------------------------------------------------------------------

def _gen_easy_addition(rng, count):
    challenges = []
    for _ in range(count):
        a = rng.randint(1, 9)
        b = rng.randint(1, 9)
        challenges.append(Challenge(
            f"What is {a} + {b}?",
            a + b,
            f"If you have {a} things and get {b} more, how many do you have?",
            f"{a} + {b} = {a + b}."
        ))
    return challenges


def _gen_easy_subtraction(rng, count):
    challenges = []
    for i in range(count):
        # Guarantee one "subtract from itself" example to teach the zero concept.
        force_zero = count >= 3 and i == 2
        a = rng.randint(3, 10)
        b = a if force_zero else rng.randint(1, a - 1)
        answer = a - b
        if b == a:
            hint = "When you take away the same number, what's left?"
            explanation = f"{a} - {b} = {answer}. Subtracting a number from itself always gives zero!"
        else:
            hint = f"If you have {a} things and take away {b}, how many are left?"
            explanation = f"{a} - {b} = {answer}."
        challenges.append(Challenge(f"What is {a} - {b}?", answer, hint, explanation))
    return challenges


def _gen_easy_multiplication(rng, count):
    factors = [2, 3, 4]
    challenges = []
    for _ in range(count):
        a = rng.choice(factors)
        b = rng.randint(2, 6)
        challenges.append(Challenge(
            f"What is {a} x {b}?",
            a * b,
            f"{a} times {b} means adding {a} to itself {b} times.",
            f"{a} x {b} = {a * b}."
        ))
    return challenges


# ---------------------------------------------------------------------------
# Medium tutorials (upper primary level)
# ---------------------------------------------------------------------------

def _gen_two_digit_addends(rng, carry):
    def make(r):
        return r.randint(10, 89), r.randint(10, 89)

    def predicate(pair):
        a, b = pair
        ones_sum = (a % 10) + (b % 10)
        return (ones_sum >= 10) == carry

    return _sample_until(rng, make, predicate)


def _gen_medium_addition(rng, count):
    challenges = []
    for i in range(count):
        carry = i >= count // 2
        a, b = _gen_two_digit_addends(rng, carry)
        answer = a + b
        if carry:
            hint = "When the ones digits add up to 10 or more, carry to the tens place."
            explanation = f"{a} + {b} = {answer}. You handled carrying correctly!"
        else:
            hint = "Add the ones first, then the tens."
            explanation = f"{a} + {b} = {answer}."
        challenges.append(Challenge(f"What is {a} + {b}?", answer, hint, explanation))
    return challenges


def _gen_two_digit_minuend_subtrahend(rng, borrow):
    def make(r):
        a = r.randint(20, 89)
        b = r.randint(10, a - 1)
        return a, b

    def predicate(pair):
        a, b = pair
        return ((a % 10) < (b % 10)) == borrow

    return _sample_until(rng, make, predicate)


def _gen_medium_subtraction(rng, count):
    challenges = []
    for i in range(count):
        borrow = i >= count // 2
        a, b = _gen_two_digit_minuend_subtrahend(rng, borrow)
        answer = a - b
        if borrow:
            hint = "When the ones digit is smaller, borrow from the tens place."
            explanation = f"{a} - {b} = {answer}. You handled borrowing perfectly!"
        else:
            hint = "Subtract the ones first, then the tens."
            explanation = f"{a} - {b} = {answer}."
        challenges.append(Challenge(f"What is {a} - {b}?", answer, hint, explanation))
    return challenges


def _gen_medium_multiplication(rng, count):
    challenges = []
    for _ in range(count):
        a = rng.randint(4, 10)
        b = rng.randint(4, 10)
        challenges.append(Challenge(
            f"What is {a} x {b}?",
            a * b,
            f"{a} times {b} means adding {a} to itself {b} times.",
            f"{a} x {b} = {a * b}."
        ))
    return challenges


# ---------------------------------------------------------------------------
# Hard tutorials (intermediate level)
# ---------------------------------------------------------------------------

def _mixed_template_add_mul(rng):
    a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    answer = a + b * c
    return (f"What is {a} + {b} x {c}?", answer,
            "Remember: do multiplication before addition!",
            f"{a} + {b} x {c} = {answer}. Multiplication comes before addition!")


def _mixed_template_sub_add(rng):
    a = rng.randint(10, 20)
    b = rng.randint(1, min(9, a - 1))
    c = rng.randint(1, 9)
    answer = a - b + c
    return (f"What is {a} - {b} + {c}?", answer,
            "When operations are the same level, work left to right.",
            f"{a} - {b} + {c} = {answer}. Great job with left-to-right operations!")


def _mixed_template_sub_mul(rng):
    b, c = rng.randint(2, 5), rng.randint(2, 5)
    a = rng.randint(b * c, b * c + 15)
    answer = a - b * c
    return (f"What is {a} - {b} x {c}?", answer,
            "Which operation should you do first?",
            f"{a} - {b} x {c} = {answer}. You remembered to multiply first!")


def _mixed_template_mul_sub(rng):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    c = rng.randint(1, a * b)
    answer = a * b - c
    return (f"What is {a} x {b} - {c}?", answer,
            "Think about order of operations.",
            f"{a} x {b} - {c} = {answer}. You've mastered mixed operations!")


_MIXED_TEMPLATES = [
    _mixed_template_add_mul,
    _mixed_template_sub_add,
    _mixed_template_sub_mul,
    _mixed_template_mul_sub,
]


def _gen_hard_mixed_operations(rng, count):
    templates = list(_MIXED_TEMPLATES)
    rng.shuffle(templates)
    challenges = []
    for i in range(count):
        question, answer, hint, explanation = templates[i % len(templates)](rng)
        challenges.append(Challenge(question, answer, hint, explanation))
    return challenges


def _pemdas_template_paren_add_mul(rng):
    a, b, c = rng.randint(1, 9), rng.randint(1, 9), rng.randint(2, 9)
    answer = (a + b) * c
    return (f"What is ({a} + {b}) x {c}?", answer,
            "Do what's inside parentheses first.",
            f"({a} + {b}) x {c} = {answer}. Parentheses come first!")


def _pemdas_template_mul_paren_sub(rng):
    b = rng.randint(3, 9)
    c = rng.randint(1, b - 1)
    a = rng.randint(2, 9)
    answer = a * (b - c)
    return (f"What is {a} x ({b} - {c})?", answer,
            "Solve inside the parentheses before multiplying.",
            f"{a} x ({b} - {c}) = {answer}. Perfect!")


def _pemdas_template_sub_paren_add(rng):
    b, c = rng.randint(1, 9), rng.randint(1, 9)
    a = rng.randint(b + c, b + c + 15)
    answer = a - (b + c)
    return (f"What is {a} - ({b} + {c})?", answer,
            "What should you calculate first?",
            f"{a} - ({b} + {c}) = {answer}. Excellent work!")


def _pemdas_template_mul_add_paren_sub(rng):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    d = rng.randint(1, 9)
    c = rng.randint(d, d + 9)
    answer = a * b + (c - d)
    return (f"What is {a} x {b} + ({c} - {d})?", answer,
            "Use PEMDAS: parentheses first, then multiplication, then addition.",
            f"{a} x {b} + ({c} - {d}) = {answer}. You've mastered order of operations!")


_PEMDAS_TEMPLATES = [
    _pemdas_template_paren_add_mul,
    _pemdas_template_mul_paren_sub,
    _pemdas_template_sub_paren_add,
    _pemdas_template_mul_add_paren_sub,
]


def _gen_hard_order_of_operations(rng, count):
    templates = list(_PEMDAS_TEMPLATES)
    rng.shuffle(templates)
    challenges = []
    for i in range(count):
        question, answer, hint, explanation = templates[i % len(templates)](rng)
        challenges.append(Challenge(question, answer, hint, explanation))
    return challenges


def _gen_hard_division(rng, count):
    challenges = []
    for _ in range(count):
        b = rng.randint(2, 9)
        k = rng.randint(2, 9)
        a = b * k
        challenges.append(Challenge(
            f"What is {a} / {b}?",
            k,
            f"How many groups of {b} fit into {a}?",
            f"{a} / {b} = {k}. Division is splitting equally!"
        ))
    return challenges


class TutorialLibrary:
    """Library of all available tutorials, in canonical progression order"""

    def __init__(self):
        self.tutorials = []
        self._create_tutorials()

    def _create_tutorials(self):
        """Create all tutorials, in the order students should play them"""
        self.tutorials.append(Tutorial(
            "basics_intro", "Getting Started",
            "Learn the frame's own controls: typing, auto-shift, navigation, "
            "delete, and reading things back.",
            "easy", _gen_basics_intro, 6
        ))
        self.tutorials.append(Tutorial(
            "easy_addition", "Single Digit Addition",
            "Learn to add single digit numbers. Place your answer in the grid and press Ctrl+Enter to check.",
            "easy", _gen_easy_addition, 4
        ))
        self.tutorials.append(Tutorial(
            "easy_subtraction", "Single Digit Subtraction",
            "Learn to subtract single digit numbers.",
            "easy", _gen_easy_subtraction, 4
        ))
        self.tutorials.append(Tutorial(
            "easy_multiplication", "Multiplication Basics",
            "Learn multiplication with small times tables (2 to 4).",
            "easy", _gen_easy_multiplication, 4
        ))
        self.tutorials.append(Tutorial(
            "medium_addition", "Two Digit Addition",
            "Learn to add two-digit numbers, including carrying.",
            "medium", _gen_medium_addition, 4
        ))
        self.tutorials.append(Tutorial(
            "medium_subtraction", "Two Digit Subtraction",
            "Learn to subtract two-digit numbers, including borrowing.",
            "medium", _gen_medium_subtraction, 4
        ))
        self.tutorials.append(Tutorial(
            "medium_multiplication", "Multiplication Tables",
            "Practice multiplication up to 10.",
            "medium", _gen_medium_multiplication, 4
        ))
        self.tutorials.append(Tutorial(
            "hard_mixed", "Mixed Operations",
            "Practice problems with addition, subtraction, and multiplication together.",
            "hard", _gen_hard_mixed_operations, 4
        ))
        self.tutorials.append(Tutorial(
            "hard_pemdas", "Order of Operations",
            "Learn PEMDAS: Parentheses, Exponents, Multiplication/Division, Addition/Subtraction.",
            "hard", _gen_hard_order_of_operations, 4
        ))
        self.tutorials.append(Tutorial(
            "hard_division", "Division Basics",
            "Learn to divide numbers evenly.",
            "hard", _gen_hard_division, 4
        ))

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

    def get_tutorial_by_id(self, tutorial_id):
        """Get a specific tutorial by its stable id"""
        for tutorial in self.tutorials:
            if tutorial.id == tutorial_id:
                return tutorial
        return None

    def get_progression_order(self):
        """Get tutorial ids in the fixed order students unlock them"""
        return [t.id for t in self.tutorials]
