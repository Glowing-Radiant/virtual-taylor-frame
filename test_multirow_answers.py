#!/usr/bin/env python3
"""Test multi-row answer detection for tutorial system"""

import numpy as np
from tutorial_system import Challenge

def test_multirow_answer_detection():
    """Test that answers can be found anywhere on the grid"""
    print("Testing multi-row answer detection...")
    
    # Create a mock grid (18x25)
    rows, cols = 18, 25
    grid = np.full((rows, cols), ' ', dtype=str)
    
    # Create a challenge
    challenge = Challenge("What is 2 + 3?", "5")
    
    # Test 1: Answer in first row
    grid[0] = list("5" + " " * (cols - 1))
    for y in range(rows):
        row_content = "".join(grid[y]).strip()
        if row_content and challenge.check_answer(row_content):
            print(f"✓ Test 1: Found answer '5' in row {y} (first row)")
            break
    
    # Clear grid
    grid = np.full((rows, cols), ' ', dtype=str)
    
    # Test 2: Answer in middle row (after work)
    grid[0] = list("2+3=" + " " * (cols - 4))
    grid[1] = list("5" + " " * (cols - 1))
    found = False
    for y in range(rows):
        row_content = "".join(grid[y]).strip()
        if row_content and challenge.check_answer(row_content):
            print(f"✓ Test 2: Found answer '5' in row {y} (after work on row 0)")
            found = True
            break
    assert found, "Should find answer in row 1"
    
    # Clear grid
    grid = np.full((rows, cols), ' ', dtype=str)
    
    # Test 3: Answer in last row
    grid[17] = list("5" + " " * (cols - 1))
    found = False
    for y in range(rows):
        row_content = "".join(grid[y]).strip()
        if row_content and challenge.check_answer(row_content):
            print(f"✓ Test 3: Found answer '5' in row {y} (last row)")
            found = True
            break
    assert found, "Should find answer in last row"
    
    # Clear grid
    grid = np.full((rows, cols), ' ', dtype=str)
    
    # Test 4: Multi-digit answer with work
    challenge2 = Challenge("What is 23 + 34?", "57")
    grid[0] = list("  23" + " " * (cols - 4))
    grid[1] = list("+ 34" + " " * (cols - 4))
    grid[2] = list("----" + " " * (cols - 4))
    grid[3] = list("  57" + " " * (cols - 4))
    found = False
    for y in range(rows):
        row_content = "".join(grid[y]).strip()
        if row_content and challenge2.check_answer(row_content):
            print(f"✓ Test 4: Found answer '57' in row {y} (after column addition work)")
            found = True
            break
    assert found, "Should find answer '57' in row 3"
    
    # Test 5: Wrong answer should not be found
    grid = np.full((rows, cols), ' ', dtype=str)
    grid[0] = list("2+3" + " " * (cols - 3))
    grid[1] = list("7" + " " * (cols - 1))  # Wrong answer
    found = False
    for y in range(rows):
        row_content = "".join(grid[y]).strip()
        if row_content and challenge.check_answer(row_content):
            found = True
            break
    assert not found, "Should not find incorrect answer"
    print("✓ Test 5: Correctly rejected wrong answer '7'")
    
    print("\n✓ All multi-row answer detection tests passed!")

if __name__ == "__main__":
    test_multirow_answer_detection()
