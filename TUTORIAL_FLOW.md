# Tutorial Mode Flow

This document describes the user flow through the Tutorial Mode.

## Main Menu Flow

```
┌─────────────────────────────────┐
│  Virtual Taylor Frame Startup   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│        Main Menu                │
│                                 │
│  1. Normal Mode                 │
│  2. Tutorial Mode  ◄────────┐   │
│  3. Exit                    │   │
└────────────┬────────────────┘   │
             │                    │
             ▼                    │
┌─────────────────────────────────┐
│    Tutorial Difficulty Menu     │
│                                 │
│  1. Easy Tutorials              │
│  2. Medium Tutorials            │
│  3. Hard Tutorials              │
│  4. Back to Main Menu           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│    Tutorial Selection           │
│                                 │
│  Easy:                          │
│  1. Single Digit Addition       │
│     (Not yet completed)         │
│  2. Single Digit Subtraction    │
│     (Locked - finish #1 first)  │
│  3. Multiplication Basics       │
│     (Locked - finish #2 first)  │
│  4. Back                        │
│                                 │
│  Locked entries announce what   │
│  to finish first instead of     │
│  starting when selected.        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│    Tutorial Challenge Screen    │
│                                 │
│  Challenge 1 of 4               │
│  "What is 2 + 3?"               │
│                                 │
│  Grid: [ ] [ ] [ ] [ ] ...      │
│  User types answer: 5           │
│                                 │
│  Ctrl+Enter: Check Answer       │
│  F6: Get Hint                   │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ CORRECT  │  │INCORRECT │
│          │  │          │
│ Audio ♪  │  │ Audio ♪  │
│ "Good!"  │  │ "Try     │
│          │  │  again"  │
└────┬─────┘  └────┬─────┘
     │             │
     │             ▼
     │        ┌─────────────┐
     │        │ After 2     │
     │        │ attempts:   │
     │        │ Show Hint   │
     │        └─────┬───────┘
     │              │
     │              ▼
     │         (Try Again)
     │
     ▼
┌─────────────────────────────────┐
│    Next Challenge               │
│                                 │
│  Challenge 2 of 4               │
│  "Good! Now try: 4 + 5"         │
└────────────┬────────────────────┘
             │
             ▼
           (Repeat)
             │
             ▼
┌─────────────────────────────────┐
│    Tutorial Complete!           │
│                                 │
│  "Congratulations!"             │
│  "You completed Single Digit    │
│   Addition and earned 3 of 3    │
│   stars!"                       │
│                                 │
│  Progress saved to disk.        │
│  If this was the last locked    │
│  tutorial before the next one:  │
│  "New tutorial unlocked:        │
│   Single Digit Subtraction!"    │
│                                 │
│  Press any key to continue      │
└────────────┬────────────────────┘
             │
             ▼
   Back to Tutorial Selection
   (level-select, ready to pick
    the next unlocked tutorial)
```

## Tutorial Structure

Numbers below are examples of each tutorial's style/range - every playthrough
generates new random challenges, so the exact problems shown differ each time.

### Easy Level (Ages 6-10)
```
Tutorial 1: Single Digit Addition
├── Challenge 1: 2 + 3 = ?
├── Challenge 2: 4 + 5 = ?
├── Challenge 3: 7 + 2 = ?
└── Challenge 4: 6 + 6 = ?

Tutorial 2: Single Digit Subtraction
├── Challenge 1: 8 - 3 = ?
├── Challenge 2: 9 - 4 = ?
├── Challenge 3: 7 - 7 = ?
└── Challenge 4: 10 - 6 = ?

Tutorial 3: Multiplication Basics
├── Challenge 1: 2 × 3 = ?
├── Challenge 2: 3 × 4 = ?
├── Challenge 3: 2 × 5 = ?
└── Challenge 4: 4 × 3 = ?
```

### Medium Level (Ages 10-12)
```
Tutorial 4: Two Digit Addition
├── Challenge 1: 12 + 15 = ?
├── Challenge 2: 23 + 34 = ?
├── Challenge 3: 28 + 17 = ? (with carrying)
└── Challenge 4: 46 + 39 = ? (with carrying)

Tutorial 5: Two Digit Subtraction
├── Challenge 1: 45 - 23 = ?
├── Challenge 2: 67 - 34 = ?
├── Challenge 3: 52 - 28 = ? (with borrowing)
└── Challenge 4: 81 - 47 = ? (with borrowing)

Tutorial 6: Multiplication Tables
├── Challenge 1: 5 × 6 = ?
├── Challenge 2: 7 × 4 = ?
├── Challenge 3: 8 × 6 = ?
└── Challenge 4: 9 × 7 = ?
```

### Hard Level (Ages 12-14)
```
Tutorial 7: Mixed Operations
├── Challenge 1: 5 + 3 × 2 = ?
├── Challenge 2: 10 - 4 + 6 = ?
├── Challenge 3: 15 - 2 × 3 = ?
└── Challenge 4: 4 × 5 - 8 = ?

Tutorial 8: Order of Operations (PEMDAS)
├── Challenge 1: (3 + 2) × 4 = ?
├── Challenge 2: 2 × (8 - 3) = ?
├── Challenge 3: 20 - (4 + 6) = ?
└── Challenge 4: 3 × 4 + (10 - 2) = ?

Tutorial 9: Division Basics
├── Challenge 1: 10 ÷ 2 = ?
├── Challenge 2: 15 ÷ 3 = ?
├── Challenge 3: 24 ÷ 4 = ?
└── Challenge 4: 36 ÷ 6 = ?
```

## Key Features

### Hint System
```
Attempt 1: ✗ Wrong → "Not quite. Try again!"
Attempt 2: ✗ Wrong → "Hint: [Context-specific guidance]"
Attempt 3+: ✗ Wrong → Same hint repeated
Any time: Press F6 → Manual hint request
```

### Audio Feedback
```
Move cursor        → Move sound (♪)
Correct answer     → Content sound (♪♪) + "Correct!"
Incorrect answer   → Empty sound (♪) + "Try again"
Tutorial complete  → "Congratulations! ... earned N of 3 stars." + optional
                      "New tutorial unlocked: ..." message
```

### Accessibility Features
```
✓ Full keyboard navigation (no mouse required)
✓ Screen reader compatible (cytolk integration)
✓ Audio cues for all actions
✓ Clear spoken questions and answers
✓ Tactile grid for entering answers
```

### Progressive Game System
```
✓ Randomized challenges — fresh numbers every playthrough
✓ Locked levels — complete a tutorial to unlock the next one in sequence
✓ Star ratings (1-3) — based on attempts/hints used per challenge
✓ Persistent save — progress written to ~/.virtual_taylor_frame/progress.json
```

## Command Summary

| Action | Key | Available When |
|--------|-----|----------------|
| Navigate menus | Up/Down arrows | Menus |
| Select option | Enter | Menus |
| Go back | Escape | Anytime |
| Move in grid | Arrow keys | Tutorial challenge |
| Type answer | 0-9, +, -, ×, ÷, etc. | Tutorial challenge |
| Check answer | Ctrl+Enter | Tutorial challenge |
| Get hint | F6 | Tutorial challenge |
| Show help | F1 | Anytime |

## Tutorial Progression

Progression is **enforced**, not just suggested: tutorials unlock one at a
time in this fixed order, and a locked tutorial cannot be started until the
previous one is completed at least once.

```
easy_addition → easy_subtraction → easy_multiplication
    → medium_addition → medium_subtraction → medium_multiplication
    → hard_mixed → hard_pemdas → hard_division
```

1. **Start with Easy**: Master single-digit operations
2. **Move to Medium**: Build on basics with larger numbers
3. **Advance to Hard**: Learn complex operations and rules

Each unlocked tutorial can be replayed as many times as needed for mastery -
every replay generates new random challenges, and only your best star rating
is kept.
