#!/usr/bin/env python3
"""Test script for tutorial system"""

from tutorial_system import TutorialLibrary, Tutorial, Challenge

def test_tutorial_library():
    """Test that tutorial library is created correctly"""
    library = TutorialLibrary()
    tutorials = library.get_all_tutorials()
    
    print(f"✓ Tutorial library created with {len(tutorials)} tutorials")
    
    # Check we have tutorials for each difficulty
    easy = library.get_tutorials_by_difficulty("easy")
    medium = library.get_tutorials_by_difficulty("medium")
    hard = library.get_tutorials_by_difficulty("hard")
    
    print(f"✓ Easy tutorials: {len(easy)}")
    print(f"✓ Medium tutorials: {len(medium)}")
    print(f"✓ Hard tutorials: {len(hard)}")
    
    assert len(easy) == 3, "Should have 3 easy tutorials"
    assert len(medium) == 3, "Should have 3 medium tutorials"
    assert len(hard) == 3, "Should have 3 hard tutorials"
    
    return library

def test_tutorial_content(library):
    """Test tutorial content and structure"""
    tutorials = library.get_all_tutorials()
    
    for i, tutorial in enumerate(tutorials):
        print(f"\nTutorial {i+1}: {tutorial.title} ({tutorial.difficulty})")
        print(f"  Description: {tutorial.description}")
        print(f"  Challenges: {len(tutorial.challenges)}")
        
        assert len(tutorial.challenges) > 0, f"Tutorial {tutorial.title} has no challenges"
        
        for j, challenge in enumerate(tutorial.challenges):
            print(f"    Challenge {j+1}: {challenge.question}")
            print(f"      Answer: {challenge.answer}")
            if challenge.hint:
                print(f"      Hint: {challenge.hint[:50]}...")
            
            # Test answer checking
            assert challenge.check_answer(challenge.answer), \
                f"Challenge answer check failed for: {challenge.question}"
    
    print("\n✓ All tutorial content verified")

def test_challenge_behavior():
    """Test challenge behavior"""
    challenge = Challenge("What is 2 + 2?", "4", "Add 2 and 2 together")
    
    # Test correct answer
    assert challenge.check_answer("4"), "Should accept correct answer"
    print("✓ Correct answer accepted")
    
    # Test incorrect answer
    assert not challenge.check_answer("5"), "Should reject incorrect answer"
    print("✓ Incorrect answer rejected")
    
    # Test normalized answers (with spaces)
    challenge2 = Challenge("What is 10?", "10")
    assert challenge2.check_answer(" 10 "), "Should handle whitespace"
    print("✓ Whitespace normalization works")
    
    # Test hint system
    challenge3 = Challenge("Hard question", "42", "Think about life")
    challenge3.attempts = 1
    assert not challenge3.needs_hint(), "Should not need hint after 1 attempt"
    challenge3.attempts = 2
    assert challenge3.needs_hint(), "Should need hint after 2 attempts"
    print("✓ Hint system works correctly")

def test_tutorial_progression():
    """Test tutorial progression"""
    tutorial = Tutorial("Test Tutorial", "A test", "easy")
    
    tutorial.add_challenge(Challenge("Q1", "A1"))
    tutorial.add_challenge(Challenge("Q2", "A2"))
    tutorial.add_challenge(Challenge("Q3", "A3"))
    
    assert tutorial.current_challenge == 0, "Should start at challenge 0"
    assert not tutorial.is_complete(), "Should not be complete initially"
    
    current, total = tutorial.get_progress()
    assert current == 0 and total == 3, "Progress should be 0 of 3"
    
    tutorial.next_challenge()
    assert tutorial.current_challenge == 1, "Should move to challenge 1"
    
    tutorial.next_challenge()
    tutorial.next_challenge()
    assert tutorial.is_complete(), "Should be complete after all challenges"
    
    print("✓ Tutorial progression works correctly")

def main():
    print("=" * 60)
    print("Testing Virtual Taylor Frame Tutorial System")
    print("=" * 60)
    
    try:
        library = test_tutorial_library()
        test_tutorial_content(library)
        test_challenge_behavior()
        test_tutorial_progression()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
