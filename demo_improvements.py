#!/usr/bin/env python3
"""
Demonstration of improved tutorial features:
1. Multi-row answer detection
2. Improved hints that don't reveal answers
3. Progressive game system: randomized challenges, stars, locked levels
"""

import os
import random
import tempfile

from progress_store import ProgressStore
from tutorial_system import TutorialLibrary

def show_improvements():
    """Show the key improvements made to the tutorial system"""

    print("=" * 70)
    print(" " * 15 + "TUTORIAL SYSTEM IMPROVEMENTS")
    print("=" * 70)

    library = TutorialLibrary()
    rng = random.Random(7)  # fixed seed so this demo's output is reproducible

    print("\n## IMPROVEMENT 1: Multi-Row Answer Detection")
    print("-" * 70)
    print("The system now scans the ENTIRE GRID for answers, not just row 0.")
    print("This supports step-by-step calculation - the core purpose of the app!")
    print("\nExample: Student solving 28 + 17")
    print("┌─────────────────────────────────┐")
    print("│ Row 0:   28                     │  ← Work shown")
    print("│ Row 1: + 17                     │  ← Work shown")
    print("│ Row 2: ----                     │  ← Work shown")
    print("│ Row 3:   45                     │  ← Answer found here! ✓")
    print("└─────────────────────────────────┘")
    print("\nThe system will find '45' on row 3 and mark it correct!")
    
    print("\n## IMPROVEMENT 2: Better Hints (Don't Reveal Answers)")
    print("-" * 70)
    print("Hints now provide GUIDANCE without revealing the complete solution.\n")

    # Show examples from each difficulty level
    easy_tutorial = library.get_tutorial(0)  # Addition
    medium_tutorial = library.get_tutorial(3)  # Two-digit addition
    hard_tutorial = library.get_tutorial(6)  # Mixed operations

    easy_tutorial.generate_challenges(rng)
    medium_tutorial.generate_challenges(rng)
    hard_tutorial.generate_challenges(rng)

    print("### Easy Level Example")
    print(f"Challenge: {easy_tutorial.challenges[1].question}")
    print(f"OLD Hint: 'Count up: 4, then add 1, 2, 3, 4, 5 more numbers.'")
    print(f"          ^ Reveals intermediate steps")
    print(f"NEW Hint: '{easy_tutorial.challenges[1].hint}'")
    print(f"          ^ Guides without revealing\n")
    
    print("### Medium Level Example")
    print(f"Challenge: {medium_tutorial.challenges[2].question}")
    print(f"OLD Hint: 'Ones: 8 + 7 = 15 (carry the 1). Tens: 20 + 10 + 10 = 40. Total: 45.'")
    print(f"          ^ Shows complete calculation")
    print(f"NEW Hint: '{medium_tutorial.challenges[2].hint}'")
    print(f"          ^ Strategic guidance only\n")
    
    print("### Hard Level Example")
    print(f"Challenge: {hard_tutorial.challenges[0].question}")
    print(f"OLD Hint: 'Multiply first! 3 x 2 = 6, then 5 + 6 = 11.'")
    print(f"          ^ Solves the entire problem")
    print(f"NEW Hint: '{hard_tutorial.challenges[0].hint}'")
    print(f"          ^ Teaches the principle\n")
    
    print("\n## IMPROVEMENT 3: Progressive Game System")
    print("-" * 70)
    print("Challenges are now randomly generated each playthrough (not the same")
    print("4 fixed problems forever), tutorials are locked until the previous one")
    print("in the sequence is completed, and finishing one earns 1-3 stars based")
    print("on how many attempts/hints it took.\n")

    order = library.get_progression_order()
    # Illustrative only - a throwaway path so this demo never touches the real save file
    demo_store = ProgressStore(path=os.path.join(tempfile.mkdtemp(), "demo_progress.json"))

    print(f"Progression order ({len(order)} tutorials): {' -> '.join(order)}")
    print(f"Tutorial '{order[0]}' unlocked at the start: {demo_store.is_unlocked(order[0], order)}")
    print(f"Tutorial '{order[1]}' unlocked before completing '{order[0]}': "
          f"{demo_store.is_unlocked(order[1], order)}")

    print("\n" + "=" * 70)
    print("These improvements make the tutorial system more pedagogical")
    print("and better aligned with step-by-step learning!")
    print("=" * 70)

if __name__ == "__main__":
    show_improvements()
