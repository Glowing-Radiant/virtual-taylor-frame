# Interactive Tutorial Mode - User Guide

## Overview

The Virtual Taylor Frame now includes an Interactive Tutorial Mode designed to teach mathematics to visually impaired students in a progressive, intuitive manner. The tutorials cover basic to intermediate math concepts suitable for primary and intermediate class students (ages 6-14).

## Getting Started

### Launching Tutorial Mode

1. Start the Virtual Taylor Frame application:
   ```bash
   python "virtual taylor frame.py"
   ```

2. At the main menu, navigate using the **Up** and **Down** arrow keys:
   - Normal Mode: Traditional grid workspace
   - Tutorial Mode: Interactive guided lessons
   - Exit: Close the application

3. Press **Enter** to select "Tutorial Mode"

### Selecting a Tutorial

1. Choose a difficulty level:
   - **Easy**: For primary students (ages 6-10)
   - **Medium**: For upper primary students (ages 10-12)
   - **Hard**: For intermediate students (ages 12-14)

2. Navigate tutorials using **Up** and **Down** arrows
3. Press **Enter** to start a tutorial
4. Press **Escape** to go back

## Tutorial Structure

### Easy Level (Primary - Ages 6-10)

#### Tutorial 1: Single Digit Addition
- **Objective**: Learn to add single-digit numbers
- **Topics**: 2+3, 4+5, 7+2, 6+6
- **Skills**: Basic addition, counting up, doubles
- **Challenges**: 4

#### Tutorial 2: Single Digit Subtraction
- **Objective**: Learn to subtract single-digit numbers
- **Topics**: 8-3, 9-4, 7-7, 10-6
- **Skills**: Basic subtraction, counting down, zero concept
- **Challenges**: 4

#### Tutorial 3: Multiplication Basics
- **Objective**: Introduction to multiplication
- **Topics**: 2×3, 3×4, 2×5, 4×3
- **Skills**: Repeated addition, times tables (2s and 3s)
- **Challenges**: 4

### Medium Level (Upper Primary - Ages 10-12)

#### Tutorial 4: Two Digit Addition
- **Objective**: Learn to add two-digit numbers
- **Topics**: 12+15, 23+34, 28+17, 46+39
- **Skills**: Place value, carrying, regrouping
- **Challenges**: 4

#### Tutorial 5: Two Digit Subtraction
- **Objective**: Learn to subtract two-digit numbers
- **Topics**: 45-23, 67-34, 52-28, 81-47
- **Skills**: Place value, borrowing, regrouping
- **Challenges**: 4

#### Tutorial 6: Multiplication Tables
- **Objective**: Practice larger multiplication
- **Topics**: 5×6, 7×4, 8×6, 9×7
- **Skills**: Times tables up to 10, mental math tricks
- **Challenges**: 4

### Hard Level (Intermediate - Ages 12-14)

#### Tutorial 7: Mixed Operations
- **Objective**: Combine different operations
- **Topics**: 5+3×2, 10-4+6, 15-2×3, 4×5-8
- **Skills**: Order of operations basics, left-to-right evaluation
- **Challenges**: 4

#### Tutorial 8: Order of Operations (PEMDAS)
- **Objective**: Learn proper operation order
- **Topics**: (3+2)×4, 2×(8-3), 20-(4+6), 3×4+(10-2)
- **Skills**: Parentheses first, PEMDAS rule
- **Challenges**: 4

#### Tutorial 9: Division Basics
- **Objective**: Introduction to division
- **Topics**: 10÷2, 15÷3, 24÷4, 36÷6
- **Skills**: Equal grouping, division as reverse multiplication
- **Challenges**: 4

## How to Use Tutorials

### During a Tutorial

1. **Listen to the Question**: Each challenge is read aloud with clear instructions
2. **Work Through the Problem**: Use the grid for step-by-step calculations - work can span multiple rows
3. **Enter Your Answer**: Place your final answer anywhere on the grid
4. **Check Your Answer**: Press **Ctrl+Enter** to submit - the system will scan the entire grid for your answer
5. **Get Hints**: Press **F6** if you need help (available after 2 attempts)
6. **Try Again**: If incorrect, listen to the feedback and try again
7. **Move Forward**: Complete all challenges to finish the tutorial

### Working on the Grid

The Virtual Taylor Frame is designed for **step-by-step calculation**:
- You can use multiple rows to show your work
- Write intermediate calculations on different rows
- Place your final answer on any row
- The system will find your answer wherever it is on the grid
- Example for "28 + 17":
  ```
  Row 0:   28
  Row 1: + 17
  Row 2: ----
  Row 3:   45  ← Answer found here
  ```

### Tutorial Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Navigate the grid |
| **0-9, +, -, ×, ÷, (, )** | Enter math expressions |
| **Ctrl+Enter** | Check your answer |
| **F6** | Request a hint (Tutorial Mode) |
| **F1** | Show help |
| **Backspace** | Delete |
| **Escape** | Exit tutorial (return to menu) |

### Feedback System

The tutorial provides three types of feedback:

1. **Correct Answer**:
   - Positive audio cue (content sound)
   - Encouraging message
   - Explanation of the solution
   - Automatically moves to next challenge

2. **Incorrect Answer (1st attempt)**:
   - Negative audio cue (empty sound)
   - "Not quite. Try again!" message
   - Opportunity to try again

3. **Incorrect Answer (2nd+ attempt)**:
   - Negative audio cue
   - Automatic hint provided
   - Example: "Hint: Think: If you have 2 apples and get 3 more, how many do you have?"

### Hints System

- Hints are **context-specific** to each challenge
- Available after **2 unsuccessful attempts**
- Can be manually requested with **F6**
- Provide **guidance without revealing the answer**
- Designed to help you think through the problem
- Examples:
  - "Think: If you have 2 apples and get 3 more, how many do you have?"
  - "Do what's inside parentheses first."
  - "When ones add up to more than 10, carry to the tens place."

## Tips for Students

### For Beginners (Easy Level)
- Take your time with each problem
- Use the hint system when you're stuck
- Count on your fingers if it helps
- Practice the easier tutorials multiple times
- Listen carefully to the explanations

### For Intermediate Learners (Medium Level)
- Break down problems into smaller steps
- Remember place value (ones, tens)
- Practice carrying and borrowing
- Try to solve without hints first
- Review explanations even when correct

### For Advanced Students (Hard Level)
- Remember PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction)
- Do operations in the correct order
- Check your work before submitting
- Try different strategies
- Challenge yourself to use fewer hints

## Tips for Educators/Parents

### Teaching Strategies
1. **Start Easy**: Begin with single-digit operations, even if the student seems ready for more
2. **Encourage Repetition**: Mastery comes from practice; it's okay to repeat tutorials
3. **Praise Effort**: Acknowledge attempts, not just correct answers
4. **Use Hints Wisely**: Let students struggle a bit before offering hints
5. **Discuss Explanations**: After each answer, discuss why it's correct
6. **Set Goals**: Complete one tutorial per session, or aim for fewer hints needed

### Accessibility Features
- **Full keyboard navigation**: No mouse required
- **Audio feedback**: All interactions have sound cues
- **Screen reader compatible**: Works with NVDA, JAWS, etc.
- **Clear speech**: Questions and feedback are read aloud
- **Tactile learning**: Students physically enter answers on the grid

### Progress Tracking
- Each tutorial shows progress (Challenge X of Y)
- Completion messages celebrate achievement
- Students can repeat tutorials to improve
- Encourage moving to harder levels gradually

## Troubleshooting

### Common Issues

**Q: I can't hear the speech output**
- Ensure your screen reader (NVDA, JAWS) is running
- Check that cytolk is properly installed
- Verify system audio is not muted

**Q: The hints aren't helping**
- Try reading the question again carefully
- Use a calculator or paper to work through the problem
- Ask an educator/parent for additional explanation
- Consider trying an easier tutorial first

**Q: How do I exit a tutorial?**
- Press **Escape** to return to the tutorial menu
- Press **Escape** again to return to main menu

**Q: Can I save my progress?**
- Tutorial progress is per-session only
- You can complete tutorials multiple times
- Each tutorial session is independent

## Technical Details

### File Structure
- `tutorial_system.py`: Core tutorial framework
- `virtual taylor frame.py`: Main application with tutorial integration
- Tutorial data is embedded in the code (not external files)

### Adding Custom Tutorials
Educators can extend the tutorial system by editing `tutorial_system.py`:

```python
# Example: Adding a new tutorial
tutorial = Tutorial(
    "My Custom Tutorial",
    "Description of what students will learn",
    "easy"  # or "medium" or "hard"
)

tutorial.add_challenge(Challenge(
    "What is 1 + 1?",  # Question
    "2",                # Answer
    "One plus one",     # Hint (optional)
    "1 + 1 = 2"        # Explanation (optional)
))

self.tutorials.append(tutorial)
```

## Feedback and Contributions

This tutorial system is open source and welcomes contributions. If you:
- Find bugs or issues
- Have suggestions for new tutorials
- Want to improve existing content
- Have accessibility feedback

Please open an issue or pull request on the project repository.

## Credits

Tutorial system developed as part of the Virtual Taylor Frame project to make mathematics education more accessible for visually impaired students.

---

*Last Updated: 2026-02-17*
