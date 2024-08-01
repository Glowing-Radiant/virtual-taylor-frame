
# Virtual Taylor Frame

Virtual Taylor Frame is a Python-based interactive grid application designed to simulate a physical Taylor Frame, which is commonly used in mathematics education for visually impaired students. This program provides an accessible, digital version of the Taylor Frame experience.

## Features

- Interactive 18x25 grid
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

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries:
   ```
   pip install pygame numpy cytolk
   ```
3. Download the `virtual_taylor_frame.py` file and the sound files (`empty.wav`, `content.wav`, `move.wav`) to the same directory.

## Usage

Run the program by executing the following command in the terminal:

```
python virtual_taylor_frame.py
```

### Controls

- Arrow keys: Move cursor
- Ctrl + Arrow keys: Snap to content
- Shift + Down: Move to next stack
- Home/End: Move to start/end of row
- Ctrl + Home/End: Move to start/end of grid
- Ctrl + PageUp/PageDown: Move to top/bottom of column
- Backspace: Delete content
- Ctrl + Backspace: Clear entire grid
- F1: Show help message
- F2: Toggle auto-shift cursor
- F3: Toggle smart delete
- F4: Toggle fast move

### Special Characters

- '()[]{}': Spoken as "left/right paren/bracket/brace"
- '-': Spoken as "minus"
- '^': Spoken as "power"
- '*': Spoken as "times"


## Contributing

Contributions to improve the Virtual Taylor Frame are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License
we use MIT license.

