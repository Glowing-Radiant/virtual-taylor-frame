# Virtual Taylor Frame

Virtual Taylor Frame is a Python-based interactive grid application designed to simulate a physical Taylor Frame, which is commonly used in mathematics education for visually impaired students. This program provides an accessible, digital version of the Taylor Frame experience.

## Features

- Interactive 18x25 grid, though the nvgt version lets you Customize the grid size.  
- Keyboard navigation
- Text-to-speech feedback
- Sound effects for different actions
- Auto-shift, smart delete, and fast move options
- Compatibility with screen readers (using cytolk)

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
python virtual_taylor_frame.py
```

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
- Ctrl + Enter: Evaluate math expression
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


### Special Characters

- '()[]{}': Spoken as "left/right paren/bracket/brace"
- '-': Spoken as "minus"
- '^': Spoken as "power"
- '*': Spoken as "times"


## Contributing

Contributions to improve the Virtual Taylor Frame are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
