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

The Virtual Taylor Frame now includes an **Interactive Tutorial Mode** designed specifically for visually impaired students learning mathematics. The tutorials provide:

### Difficulty Levels
- **Easy (Primary Level)**: Single digit addition, subtraction, and basic multiplication
- **Medium (Upper Primary)**: Two-digit arithmetic and multiplication tables
- **Hard (Intermediate)**: Mixed operations, order of operations (PEMDAS), and division

### Tutorial Features
- Step-by-step guided challenges
- Intelligent hint system (available after 2 attempts)
- Encouraging audio feedback
- Progressive difficulty
- 9 complete tutorials with 36 total challenges

### Available Tutorials
1. **Single Digit Addition** - Learn basic addition (2+3, 5+4, etc.)
2. **Single Digit Subtraction** - Practice subtraction (8-3, 9-4, etc.)
3. **Multiplication Basics** - Introduction to multiplication tables
4. **Two Digit Addition** - Advanced addition with carrying
5. **Two Digit Subtraction** - Subtraction with borrowing
6. **Multiplication Tables** - Practice up to 10x10
7. **Mixed Operations** - Combine different operations
8. **Order of Operations** - Learn PEMDAS with parentheses
9. **Division Basics** - Introduction to division

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
3. Select a specific tutorial from the list
4. Follow the audio instructions for each challenge
5. Type your answer in the grid
6. Press **Ctrl+Enter** to check your answer
7. Press **F6** if you need a hint (after 2 attempts)
8. Complete all challenges to finish the tutorial

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
