#!/usr/bin/env python3
"""Test script for tutorial system"""

import random

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

    assert len(easy) == 4, "Should have 4 easy tutorials (including the Getting Started orientation)"
    assert len(medium) == 3, "Should have 3 medium tutorials"
    assert len(hard) == 3, "Should have 3 hard tutorials"

    order = library.get_progression_order()
    assert order[0] == "basics_intro", "The orientation tutorial should be first, so it's always unlocked"
    print("✓ Getting Started orientation is first in the progression order")

    return library

def test_tutorial_content(library):
    """Test that each tutorial's generated challenges are well-formed"""
    tutorials = library.get_all_tutorials()
    rng = random.Random(1)

    for i, tutorial in enumerate(tutorials):
        challenges = tutorial.generate_challenges(rng)
        print(f"\nTutorial {i+1}: {tutorial.title} ({tutorial.difficulty}) [id={tutorial.id}]")
        print(f"  Description: {tutorial.description}")
        print(f"  Challenges: {len(challenges)}")

        assert len(challenges) == tutorial.challenge_count, \
            f"Tutorial {tutorial.title} should generate {tutorial.challenge_count} challenges"

        for j, challenge in enumerate(challenges):
            print(f"    Challenge {j+1}: {challenge.question}")
            print(f"      Answer: {challenge.answer}")
            if challenge.hint:
                print(f"      Hint: {challenge.hint[:50]}...")

            # The generated answer must always satisfy its own check
            assert challenge.check_answer(challenge.answer), \
                f"Challenge answer check failed for: {challenge.question}"

    print("\n✓ All tutorial content verified")

def test_challenge_generation_varies(library):
    """Test that regenerating a tutorial can produce different challenges"""
    tutorial = library.get_tutorial_by_id("easy_addition")

    seen_question_sets = set()
    for seed in range(10):
        challenges = tutorial.generate_challenges(random.Random(seed))
        seen_question_sets.add(tuple(c.question for c in challenges))

    assert len(seen_question_sets) > 1, \
        "Regenerating a tutorial's challenges should produce variety across playthroughs"
    print("✓ Tutorial regeneration produces varied challenges")

def test_basics_intro_is_fixed(library):
    """The orientation tutorial teaches the interface, not math - it should
    present the same walkthrough every time rather than varying like the
    randomly-generated math tutorials do"""
    tutorial = library.get_tutorial_by_id("basics_intro")

    seen_question_sets = set()
    for seed in range(5):
        challenges = tutorial.generate_challenges(random.Random(seed))
        seen_question_sets.add(tuple(c.question for c in challenges))

    assert len(seen_question_sets) == 1, \
        "Getting Started should present the same fixed walkthrough on every playthrough"
    print("✓ Getting Started orientation is a fixed, non-random walkthrough")

def test_progression_order(library):
    """Test that the progression order covers every tutorial exactly once"""
    order = library.get_progression_order()
    all_ids = [t.id for t in library.get_all_tutorials()]

    assert sorted(order) == sorted(all_ids), "Progression order should include every tutorial id"
    assert len(order) == len(set(order)), "Progression order should not contain duplicates"
    print(f"✓ Progression order covers all {len(order)} tutorials")

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

    # Test that requesting a hint marks it used (feeds star scoring)
    challenge4 = Challenge("What is 1 + 1?", "2", "Add one and one")
    assert not challenge4.hint_used, "Hint should not be marked used before it's requested"
    challenge4.get_hint()
    assert challenge4.hint_used, "Requesting a hint should mark it used"
    print("✓ Hint usage tracking works correctly")

def test_tutorial_progression():
    """Test tutorial progression"""
    tutorial = Tutorial("test_tutorial", "Test Tutorial", "A test", "easy")

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

def test_star_scoring():
    """Test that compute_stars rewards clean, hint-free solves"""
    tutorial = Tutorial("test_stars", "Star Test", "A test", "easy")

    # Perfect run: every challenge solved first try, no hints
    for _ in range(4):
        c = Challenge("Q", "A")
        c.check_answer("A")  # attempts=1
        tutorial.add_challenge(c)
    assert tutorial.compute_stars() == 3, "Flawless run should earn 3 stars"

    # Struggling run: every challenge took many attempts and used a hint
    tutorial2 = Tutorial("test_stars2", "Star Test 2", "A test", "easy")
    for _ in range(4):
        c = Challenge("Q", "A")
        c.check_answer("wrong")
        c.check_answer("wrong")
        c.check_answer("A")
        c.get_hint()
        tutorial2.add_challenge(c)
    assert tutorial2.compute_stars() == 1, "Struggling run should earn 1 star"

    print("✓ Star scoring rewards clean solves and reflects struggling runs")

def main():
    print("=" * 60)
    print("Testing Virtual Taylor Frame Tutorial System")
    print("=" * 60)

    try:
        library = test_tutorial_library()
        test_tutorial_content(library)
        test_challenge_generation_varies(library)
        test_basics_intro_is_fixed(library)
        test_progression_order(library)
        test_challenge_behavior()
        test_tutorial_progression()
        test_star_scoring()

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
