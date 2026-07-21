# Virtual Taylor Frame

Virtual Taylor Frame is a Python-based interactive grid application designed to simulate a physical Taylor Frame, which is commonly used in mathematics education for visually impaired students. This program provides an accessible, digital version of the Taylor Frame experience.

## Features

- Interactive 18x25 grid, though the nvgt version lets you Customize the grid size.  
- **New: Interactive Tutorial Mode** with progressive math lessons for primary and intermediate students
- Keyboard navigation
- Text-to-speech feedback
- Sound effects for different actions
- Auto-shift, smart delete, and fast move options
- Save/load and text export (manual)
- Compatibility with screen readers (using cytolk)

## Tutorial Mode

The Virtual Taylor Frame now includes an **Interactive Tutorial Mode** designed specifically for visually impaired students learning mathematics, built as a **progressive game system**: levels unlock one at a time, mastery earns star ratings, and progress is saved between sessions.

> Tutorial Mode and the game system described below are currently **Python-only**. The NVGT build (`virtual_taylor_frame.nvgt`) is a plain grid workspace without tutorials, save/load, or hints.

### Difficulty Levels
- **Easy (Primary Level)**: Single digit addition, subtraction, and basic multiplication
- **Medium (Upper Primary)**: Two-digit arithmetic and multiplication tables
- **Hard (Intermediate)**: Mixed operations, order of operations (PEMDAS), and division

### Tutorial Features
- Step-by-step guided challenges
- Intelligent hint system (available after 2 attempts)
- Encouraging audio feedback
- **Randomized challenges** - each playthrough generates fresh numbers, so replaying a tutorial isn't just re-typing the same answers
- **Locked progression** - tutorials unlock one at a time in order; finish one to open the next, like levels in a game
- **Star ratings (1-3 stars)** - based on how many attempts/hints a tutorial took, encouraging replay for mastery
- **Persistent progress** - completion, best stars, and unlocked levels are saved to `~/.virtual_taylor_frame/progress.json` and reloaded automatically next time you launch the app
- 9 tutorials spanning primary through intermediate math

### Available Tutorials
1. **Single Digit Addition** - Basic addition of two single-digit numbers
2. **Single Digit Subtraction** - Basic subtraction, including the "anything minus itself is zero" case
3. **Multiplication Basics** - Introduction to the 2, 3, and 4 times tables
4. **Two Digit Addition** - Addition with and without carrying
5. **Two Digit Subtraction** - Subtraction with and without borrowing
6. **Multiplication Tables** - Practice up to 10x10
7. **Mixed Operations** - Combine addition, subtraction, and multiplication
8. **Order of Operations** - Learn PEMDAS with parentheses
9. **Division Basics** - Division that always divides evenly

Tutorials unlock in the order listed above - complete one to unlock the next.

## Requirements

- Python 3.x
- pygame
- numpy
- cytolk

None of the Above is required if you want to run the NVGT version. 
however, you should have nvgt installed. 

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries:
   ```
   pip install pygame numpy cytolk
   ```
3. Download the `virtual_taylor_frame.py` file and the sound files (`empty.wav`, `content.wav`, `move.wav`) to the same directory.

## Usage
###python. 
Run the program by executing the following command in the terminal:

```
python "virtual taylor frame.py"
```

On startup, you will be presented with a main menu to choose between:
- **Normal Mode**: Traditional grid-based math workspace
- **Tutorial Mode**: Guided interactive lessons
- **Exit**: Close the application

### Tutorial Mode Usage

1. Select "Tutorial Mode" from the main menu
2. Choose a difficulty level (Easy, Medium, or Hard)
3. Select a specific tutorial from the list - locked tutorials announce what to complete first, and unlocked ones announce your best star rating
4. Follow the audio instructions for each challenge
5. **Work through the problem step-by-step** on the grid
6. Type your answer anywhere on the grid (the system scans all rows)
7. Press **Ctrl+Enter** to check your answer
8. Press **F6** if you need a hint (provides guidance without revealing the answer - using a hint lowers your star rating for that run)
9. Complete all challenges to finish the tutorial, earn 1-3 stars, and unlock the next one in the sequence

**Note**: The grid supports multi-row calculations. You can show your work across multiple rows, and the system will find your answer wherever you place it.

**Note**: Every playthrough generates new numbers for each challenge, so replaying a tutorial for a better star rating is never the same problem set twice.

When saving or loading, the app prompts for a filename. Saving writes both a `.vtf` (JSON) file and a `.txt` export with the same base name.

### nvgt. 
make sure you have nvgt installed, then type. 

```
nvgt virtual_taylor_frame.nvgt
```



## Controls

- Arrow keys: Move cursor
- Alt + Arrows (Up/Down): Read previous/next content line (skips empty rows)
- Alt + L: Read current line
- Enter: Move to next stack
- **Ctrl + Enter: Evaluate math expression or check tutorial answer**
- Ctrl + Arrow keys: Snap to content
- Shift + Down: Move to next stack
- Home/End: Move to start/end of row
- Ctrl + Home/End: Move to start/end of grid
- Ctrl + PageUp/PageDown: Move to top/bottom of column
- Backspace: Delete content
- Ctrl + Backspace: Clear entire grid
- Escape: Exit program (with confirmation)
- F1: Show help message
- F2: Toggle auto-shift cursor
- F3: Toggle smart delete
- F4: Toggle fast move
- F5: Resize grid
- **F6: Get hint (Tutorial Mode only)**
- Ctrl + S: Save (writes .vtf and .txt)
- Ctrl + O: Load (.vtf)
- Ctrl + E: Export text (.txt)


### Special Characters

- '()[]{}': Spoken as "left/right paren/bracket/brace"
- '-': Spoken as "minus"
- '^': Spoken as "power"
- '*': Spoken as "times"


## Contributing

Contributions to improve the Virtual Taylor Frame are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
