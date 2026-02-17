#!/usr/bin/env python3
"""
Demo script showing the tutorial system in action (text-only mode)
This demonstrates the tutorial flow without requiring pygame/cytolk
"""

from tutorial_system import TutorialLibrary

def print_separator(char='=', length=60):
    """Print a separator line"""
    print(char * length)

def demo_tutorial(tutorial):
    """Demonstrate a tutorial in text mode"""
    print_separator()
    print(f"TUTORIAL: {tutorial.title}")
    print(f"Difficulty: {tutorial.difficulty.upper()}")
    print(f"Description: {tutorial.description}")
    print_separator()
    
    for i, challenge in enumerate(tutorial.challenges, 1):
        print(f"\nChallenge {i}/{len(tutorial.challenges)}:")
        print(f"  Question: {challenge.question}")
        print(f"  Expected Answer: {challenge.answer}")
        if challenge.hint:
            print(f"  Hint Available: {challenge.hint[:60]}...")
        if challenge.explanation:
            print(f"  Explanation: {challenge.explanation}")
        print()

def main():
    """Run the demo"""
    print("\n")
    print_separator('*', 70)
    print(" " * 15 + "VIRTUAL TAYLOR FRAME")
    print(" " * 10 + "Interactive Tutorial System Demo")
    print_separator('*', 70)
    
    # Create the tutorial library
    library = TutorialLibrary()
    
    print(f"\n✓ Tutorial system loaded with {len(library.get_all_tutorials())} tutorials")
    
    # Show easy tutorials
    print("\n\n")
    print_separator('#', 70)
    print("EASY TUTORIALS (Primary Level - Ages 6-10)")
    print_separator('#', 70)
    
    for tutorial in library.get_tutorials_by_difficulty("easy"):
        demo_tutorial(tutorial)
        print("\n")
    
    # Show medium tutorials
    print("\n")
    print_separator('#', 70)
    print("MEDIUM TUTORIALS (Upper Primary - Ages 10-12)")
    print_separator('#', 70)
    
    for tutorial in library.get_tutorials_by_difficulty("medium"):
        demo_tutorial(tutorial)
        print("\n")
    
    # Show hard tutorials
    print("\n")
    print_separator('#', 70)
    print("HARD TUTORIALS (Intermediate - Ages 12-14)")
    print_separator('#', 70)
    
    for tutorial in library.get_tutorials_by_difficulty("hard"):
        demo_tutorial(tutorial)
        print("\n")
    
    print_separator('*', 70)
    print(" " * 20 + "END OF DEMO")
    print_separator('*', 70)
    print("\nTo use the interactive tutorials:")
    print("1. Run: python 'virtual taylor frame.py'")
    print("2. Select 'Tutorial Mode' from the main menu")
    print("3. Choose a difficulty level")
    print("4. Select a tutorial and start learning!")
    print("\nNote: Full version requires pygame, numpy, and cytolk for audio feedback.")
    print()

if __name__ == "__main__":
    main()
