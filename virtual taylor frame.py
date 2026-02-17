# Python
import os
import sys
import pygame
import pygame.mixer
import numpy as np
from pygame.math import Vector2
from cytolk import tolk
import traceback
import string
import math
import json
from tutorial_system import TutorialLibrary, Tutorial, Challenge


class VirtualTaylorFrame:
    def __init__(self, rows, cols):
        pygame.init()
        pygame.mixer.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = 30
        self.grid = np.full((rows, cols), ' ', dtype=str)
        self.current_pos = Vector2(0, 0)
        self.screen = pygame.display.set_mode((cols * self.cell_size, rows * self.cell_size))
        pygame.display.set_caption("Virtual Taylor Frame")
        self.font = pygame.font.Font(None, 36)
        self.empty_sound = pygame.mixer.Sound(self.resource_path("empty.wav"))
        self.content_sound = pygame.mixer.Sound(self.resource_path("content.wav"))
        self.move_sound = pygame.mixer.Sound(self.resource_path("move.wav"))
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False
        tolk.load()
        self.auto_shift = False
        self.smart_delete = False
        self.fast_move = False
        self.last_move_time = 0
        self.tutorial_mode = False
        self.current_tutorial = None
        self.tutorial_library = TutorialLibrary()
        self.awaiting_tutorial_answer = False


    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def __del__(self):
        tolk.unload()

    def speak(self, text):
        try:
            if text in '()[]{}':
                tolk.speak(self.bracket_to_word(text))
            elif text == '-':
                tolk.speak("minus")
            elif text == '^':
                tolk.speak("power")
            elif text=='*':
                tolk.speak(" times")
            else:
                tolk.speak(str(text))
        except Exception as e:
            print(f"Error in speak: {e}")

    def bracket_to_word(self, bracket):
        bracket_words = {
            '(': 'left paren',
            ')': 'right paren',
            '[': 'left bracket',
            ']': 'right bracket',
            '{': 'left brace',
            '}': 'right brace'
        }
        return bracket_words.get(bracket, bracket)

    def play_sound(self, sound):
        try:
            pygame.mixer.Sound.play(sound)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def move(self, direction):
        new_pos = self.current_pos + direction
        if 0 <= new_pos.x < self.cols and 0 <= new_pos.y < self.rows:
            self.current_pos = new_pos
            self.play_sound(self.move_sound)
            self.play_cell_sound()
            self.speak_cell_content()

    def snap_to_content(self, direction):
        while True:
            new_pos = self.current_pos + direction
            if not (0 <= new_pos.x < self.cols and 0 <= new_pos.y < self.rows):
                break
            if self.grid[int(new_pos.y)][int(new_pos.x)] != ' ':
                self.current_pos = new_pos
                self.play_cell_sound()
                self.speak_content_stack(direction)
                break
            self.current_pos = new_pos

    def read_content_stack(self, direction):
        x, y = int(self.current_pos.x), int(self.current_pos.y)
        content = ''
        for i in range(self.cols):
            cell_content = self.grid[y][i]
            if cell_content != ' ':
                if cell_content in '()[]{}':
                    content += f" {self.bracket_to_word(cell_content)} "
                elif cell_content == '-':
                    content += " minus "
                elif cell_content == '^':
                    content += " power "
                elif cell_content=='*':
                    content += " times"
                else:
                    content += cell_content
            elif content:
                break
        return content.strip()

    def speak_content_stack(self, direction):
        content = self.read_content_stack(direction)
        self.speak(content)

    def input_value(self, value):
        x, y = int(self.current_pos.x), int(self.current_pos.y)
        self.grid[y][x] = value
        self.play_cell_sound()
        self.speak(value)
        if self.auto_shift:
            self.move(Vector2(1, 0))

    def delete_value(self):
        x, y = int(self.current_pos.x), int(self.current_pos.y)
        if self.grid[y][x] != ' ':
            self.grid[y][x] = ' '
            self.play_sound(self.empty_sound)
            self.speak("Deleted")
        elif self.smart_delete:
            self.move(Vector2(-1, 0))
            x, y = int(self.current_pos.x), int(self.current_pos.y)
            if self.grid[y][x] != ' ':
                self.grid[y][x] = ' '
                self.play_sound(self.empty_sound)
                self.speak("Deleted")
            else:
                self.play_sound(self.empty_sound)
                self.speak(",")
        else:
            self.play_sound(self.empty_sound)
            self.speak(",")

    def clear_grid(self):
        self.grid = np.full((self.rows, self.cols), ' ', dtype=str)
        self.play_sound(self.empty_sound)
        self.speak("Grid cleared")

    def play_cell_sound(self):
        x, y = int(self.current_pos.x), int(self.current_pos.y)
        content = self.grid[y][x]
        if content == ' ':
            self.play_sound(self.empty_sound)
        else:
            self.play_sound(self.content_sound)

    def speak_cell_content(self):
        x, y = int(self.current_pos.x), int(self.current_pos.y)
        content = self.grid[y][x]
        if content == ' ':
            self.speak(",")
        else:
            self.speak(content)

    def speak_row(self, row_index):
        if 0 <= row_index < self.rows:
            content = "".join(self.grid[row_index]).strip()
            # Normalize spaces: split by whitespace and join with single space
            cleaned_content = " ".join(content.split())
            if not cleaned_content:
                self.speak("Blank")
            else:
                self.speak(cleaned_content)
        else:
            self.speak("No row")

    def move_to_next_content_row(self, direction):
        # direction: -1 for Up (Previous), 1 for Down (Next)
        start_y = int(self.current_pos.y) + direction
        
        # Determine range based on direction
        if direction > 0:
             search_range = range(start_y, self.rows)
        else:
             search_range = range(start_y, -1, -1)
             
        found = False
        for y in search_range:
            content = "".join(self.grid[y]).strip()
            if content: # Found non-empty row
                self.current_pos.y = y
                self.current_pos.x = 0 # Move to start of line
                self.play_sound(self.move_sound)
                self.speak_row(y)
                found = True
                break
        
        if not found:
            self.speak("No more content")


    def evaluate_row(self):


        y = int(self.current_pos.y)
        row_content = "".join(self.grid[y]).strip()
        
        # Security/Sanity check: only allow safe characters
        allowed = set(string.digits + " .+-*/()^" + string.ascii_letters)
        if not set(row_content).issubset(allowed):
             self.speak("Error: Invalid characters in expression")
             return

        # Prepare expression for Python eval
        expression = row_content.replace("^", "**")
        
        # Support basic math constants/functions in eval context
        context = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        
        try:
            # Evaluate
            result = eval(expression, {"__builtins__": None}, context)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            result_str = f" = {result}"
            
            # Append to grid
            # Find the end of the current content
            end_x = 0
            for x in range(self.cols):
                if self.grid[y][x] != ' ':
                    end_x = x
            
            start_put_x = end_x + 1
            if start_put_x + len(result_str) < self.cols:
                 for i, char in enumerate(result_str):
                     self.grid[y][start_put_x + i] = char
                 
                 self.speak(f"equals {result}")
                 self.play_sound(self.content_sound)
            else:
                self.speak(f"Result is {result}, but no space to write it correctly.")
                
        except Exception as e:
            self.speak("Error evaluating expression")
            print(f"Eval error: {e}")


    def move_to_edge(self, direction):
        if direction.x != 0:
            self.current_pos.x = 0 if direction.x < 0 else self.cols - 1
        else:
            self.current_pos.y = 0 if direction.y < 0 else self.rows - 1
        self.play_sound(self.move_sound)
        self.speak_cell_content()

    def move_down_to_next_stack(self):
        current_x = int(self.current_pos.x)
        current_y = int(self.current_pos.y)
        start_x = 0
        for x in range(self.cols):
            if self.grid[current_y][x] != ' ':
                start_x = x
                break
        new_y = min(current_y + 2, self.rows - 1)
        self.current_pos = Vector2(start_x, new_y)
        self.play_sound(self.move_sound)
        self.speak_cell_content()

    def toggle_auto_shift(self):
        self.auto_shift = not self.auto_shift
        self.speak("Auto shift " + ("on" if self.auto_shift else "off"))

    def toggle_smart_delete(self):
        self.smart_delete = not self.smart_delete
        self.speak("Smart delete " + ("on" if self.smart_delete else "off"))

    def toggle_fast_move(self):
        self.fast_move = not self.fast_move
        self.speak("Fast move " + ("on" if self.fast_move else "off"))

    def show_help(self):
        help_text = """
        F1: Show this help message.
        F2: Toggle auto-shift cursor.
        F3: Toggle smart delete.
        F4: Toggle fast move.
        F5: Resize grid.
        F6: Get hint (Tutorial Mode only).
        Ctrl + S: Save (writes .vtf and .txt).
        Ctrl + O: Load (.vtf).
        Ctrl + E: Export text (.txt).
        Arrow keys: Move cursor.
        Alt + Arrows (Up/Down): Read previous/next content line.
        Alt + L: Read current line.
        Ctrl + Enter: Evaluate math expression or check tutorial answer.
        Enter: Move to next stack (same as Shift + Down).
        Ctrl + Arrow keys: Snap to content.
        Shift + Down: Move to next stack.
        Home/End: Move to start/end of row.
        Ctrl + Home/End: Move to start/end of grid.
        Ctrl + PageUp/PageDown: Move to top/bottom of column.
        Backspace: Delete content.
        Ctrl + Backspace: Clear entire grid.
        Escape: Exit program (with confirmation).
        """
        self.speak(help_text)

    def prompt_text_input(self, prompt_text, spoken_prompt, allow_empty=False):
        input_str = ""
        active = True
        # Reset modifier states so they don't get "stuck" after modal prompts.
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False
        self.speak(spoken_prompt)
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.speak("Canceled.")
                        active = False
                        input_str = ""
                        break
                    elif event.key == pygame.K_RETURN:
                        active = False
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        input_str = input_str[:-1]
                    else:
                        input_str += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                        self.ctrl_pressed = False
                    elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                        self.alt_pressed = False
                    elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                        self.shift_pressed = False
            self.screen.fill((255, 255, 255))
            prompt_surface = self.font.render(prompt_text + input_str, True, (0, 0, 0))
            self.screen.blit(prompt_surface, (20, (self.rows * self.cell_size) // 2))
            pygame.display.flip()

        if input_str == "" and not allow_empty:
            return ""
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False
        return input_str.strip()

    def _derive_save_paths(self, user_path):
        path = user_path.strip().strip("\"")
        base, ext = os.path.splitext(path)
        if ext.lower() in [".vtf", ".txt"]:
            base_path = base
        else:
            base_path = path
        return base_path + ".vtf", base_path + ".txt"

    def _grid_to_text_lines(self):
        lines = []
        for y in range(self.rows):
            line = "".join(self.grid[y]).rstrip()
            lines.append(line)
        return lines

    def save_state(self):
        user_path = self.prompt_text_input(
            "Save base filename (no extension): ",
            "Type a filename to save, then press Enter. Escape cancels."
        )
        if not user_path:
            return
        vtf_path, txt_path = self._derive_save_paths(user_path)
        data = {
            "version": 1,
            "rows": self.rows,
            "cols": self.cols,
            "grid": self._grid_to_text_lines(),
            "cursor": {"x": int(self.current_pos.x), "y": int(self.current_pos.y)}
        }
        try:
            with open(vtf_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=True, indent=2)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self._grid_to_text_lines()))
            self.speak("Saved.")
        except Exception as e:
            self.speak("Error saving file.")
            print(f"Save error: {e}")

    def export_text(self):
        user_path = self.prompt_text_input(
            "Export filename (.txt): ",
            "Type a text filename to export, then press Enter. Escape cancels."
        )
        if not user_path:
            return
        base, ext = os.path.splitext(user_path.strip().strip("\""))
        txt_path = user_path if ext else base + ".txt"
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self._grid_to_text_lines()))
            self.speak("Exported.")
        except Exception as e:
            self.speak("Error exporting file.")
            print(f"Export error: {e}")

    def load_state(self):
        user_path = self.prompt_text_input(
            "Load filename (.vtf): ",
            "Type a filename to load, then press Enter. Escape cancels."
        )
        if not user_path:
            return
        base, ext = os.path.splitext(user_path.strip().strip("\""))
        vtf_path = user_path if ext else base + ".vtf"
        if ext and ext.lower() != ".vtf":
            self.speak("Please load a .vtf file.")
            return
        try:
            with open(vtf_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._apply_loaded_state(data)
            self.speak("Loaded.")
        except Exception as e:
            self.speak("Error loading file.")
            print(f"Load error: {e}")

    def _apply_loaded_state(self, data):
        rows = int(data.get("rows", self.rows))
        cols = int(data.get("cols", self.cols))
        grid_data = data.get("grid", [])
        new_grid = np.full((rows, cols), ' ', dtype=str)

        for y in range(min(rows, len(grid_data))):
            row = grid_data[y]
            if isinstance(row, list):
                row_str = "".join(row)
            else:
                row_str = str(row)
            for x, ch in enumerate(row_str[:cols]):
                new_grid[y][x] = ch

        self.rows = rows
        self.cols = cols
        self.grid = new_grid

        cursor = data.get("cursor", {})
        cx = int(cursor.get("x", 0))
        cy = int(cursor.get("y", 0))
        if 0 <= cx < self.cols and 0 <= cy < self.rows:
            self.current_pos = Vector2(cx, cy)
        else:
            self.current_pos = Vector2(0, 0)

        self.screen = pygame.display.set_mode((self.cols * self.cell_size, self.rows * self.cell_size))

    def prompt_grid_resize(self):
        input_str = ""
        active = True
        prompt_text = "Enter new grid size (rows,cols): "
        # Speak initial prompt message.
        self.speak("Type in the values to resize and hit enter. Press Escape to cancel.")
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.speak("Resizing canceled, returning to main window.")
                        active = False
                        input_str = ""  # Reset input.
                        break
                    elif event.key == pygame.K_RETURN:
                        active = False
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        input_str = input_str[:-1]
                    else:
                        input_str += event.unicode
            self.screen.fill((255, 255, 255))
            prompt_surface = self.font.render(prompt_text + input_str, True, (0, 0, 0))
            self.screen.blit(prompt_surface, (20, (self.rows * self.cell_size) // 2))
            pygame.display.flip()
        # Process the input only if it's not empty.
        if input_str:
            try:
                parts = input_str.split(",")
                if len(parts) == 2:
                    new_rows = int(parts[0].strip())
                    new_cols = int(parts[1].strip())
                    self.rows = new_rows
                    self.cols = new_cols
                    self.grid = np.full((new_rows, new_cols), ' ', dtype=str)
                    self.current_pos = pygame.math.Vector2(0, 0)
                    self.screen = pygame.display.set_mode((new_cols * self.cell_size, new_rows * self.cell_size))
                    self.speak("Grid resized")
                else:
                    self.speak("Invalid input. Grid size not changed.")
            except Exception as e:
                self.speak("Invalid input. Grid size not changed.")
        # Speak a message to indicate returning to the main screen if not canceled explicitly.
        if input_str == "":
            self.speak("Returning to main window.")

    def confirm_exit(self):
        active = True
        options = ["Yes", "No"]
        selected_index = 0
        
        self.speak(f"Do you want to exit? {options[selected_index]}")
        
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_index = 1 - selected_index
                        self.play_sound(self.move_sound)
                        self.speak(options[selected_index])
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0: # Yes
                            pygame.quit()
                            sys.exit()
                        else: # No
                            self.speak("Returning to program")
                            active = False
                    elif event.key == pygame.K_ESCAPE:
                        self.speak("Returning to program")
                        active = False
            
            self.screen.fill((255, 255, 255))
            prompt_text = "Do you want to exit?"
            text_surface = self.font.render(prompt_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, (self.rows * self.cell_size) // 2 - 40))
            
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else (0, 0, 0)
                opt_surface = self.font.render(option, True, color)
                self.screen.blit(opt_surface, (20, (self.rows * self.cell_size) // 2 + i * 40))
                
            pygame.display.flip()

    def show_main_menu(self):
        """Show main menu to choose between Normal and Tutorial mode"""
        active = True
        options = ["Normal Mode", "Tutorial Mode", "Exit"]
        selected_index = 0
        
        self.speak(f"Welcome to Virtual Taylor Frame. Select mode: {options[selected_index]}")
        
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_index = (selected_index + (1 if event.key == pygame.K_DOWN else -1)) % len(options)
                        self.play_sound(self.move_sound)
                        self.speak(options[selected_index])
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:  # Normal Mode
                            self.speak("Starting Normal Mode")
                            self.tutorial_mode = False
                            return True
                        elif selected_index == 1:  # Tutorial Mode
                            self.speak("Entering Tutorial Mode")
                            self.tutorial_mode = True
                            return self.show_tutorial_menu()
                        else:  # Exit
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.screen.fill((255, 255, 255))
            title_text = "Virtual Taylor Frame - Main Menu"
            title_surface = self.font.render(title_text, True, (0, 0, 0))
            self.screen.blit(title_surface, (20, 40))
            
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else (0, 0, 0)
                opt_surface = self.font.render(option, True, color)
                self.screen.blit(opt_surface, (20, 100 + i * 40))
                
            pygame.display.flip()
            
    def show_tutorial_menu(self):
        """Show tutorial selection menu"""
        active = True
        tutorials = self.tutorial_library.get_all_tutorials()
        
        # Group by difficulty
        easy = [i for i, t in enumerate(tutorials) if t.difficulty == "easy"]
        medium = [i for i, t in enumerate(tutorials) if t.difficulty == "medium"]
        hard = [i for i, t in enumerate(tutorials) if t.difficulty == "hard"]
        
        options = ["Easy Tutorials", "Medium Tutorials", "Hard Tutorials", "Back to Main Menu"]
        selected_index = 0
        
        self.speak(f"Tutorial Menu. Select difficulty: {options[selected_index]}")
        
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_index = (selected_index + (1 if event.key == pygame.K_DOWN else -1)) % len(options)
                        self.play_sound(self.move_sound)
                        self.speak(options[selected_index])
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:  # Easy
                            return self.show_tutorial_list(easy, "Easy")
                        elif selected_index == 1:  # Medium
                            return self.show_tutorial_list(medium, "Medium")
                        elif selected_index == 2:  # Hard
                            return self.show_tutorial_list(hard, "Hard")
                        else:  # Back
                            return False
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            self.screen.fill((255, 255, 255))
            title_text = "Tutorial Mode - Select Difficulty"
            title_surface = self.font.render(title_text, True, (0, 0, 0))
            self.screen.blit(title_surface, (20, 40))
            
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else (0, 0, 0)
                opt_surface = self.font.render(option, True, color)
                self.screen.blit(opt_surface, (20, 100 + i * 40))
                
            pygame.display.flip()
            
    def show_tutorial_list(self, tutorial_indices, difficulty_name):
        """Show list of tutorials for a difficulty level"""
        active = True
        tutorials = self.tutorial_library.get_all_tutorials()
        tutorial_list = [tutorials[i] for i in tutorial_indices]
        
        options = [f"{i+1}. {t.title}" for i, t in enumerate(tutorial_list)]
        options.append("Back")
        selected_index = 0
        
        self.speak(f"{difficulty_name} Tutorials. {options[selected_index]}")
        
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_index = (selected_index + (1 if event.key == pygame.K_DOWN else -1)) % len(options)
                        self.play_sound(self.move_sound)
                        if selected_index < len(tutorial_list):
                            self.speak(f"{options[selected_index]}. {tutorial_list[selected_index].description}")
                        else:
                            self.speak(options[selected_index])
                    elif event.key == pygame.K_RETURN:
                        if selected_index < len(tutorial_list):
                            self.current_tutorial = tutorial_list[selected_index]
                            self.start_tutorial()
                            return True
                        else:  # Back
                            return False
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            self.screen.fill((255, 255, 255))
            title_text = f"{difficulty_name} Tutorials"
            title_surface = self.font.render(title_text, True, (0, 0, 0))
            self.screen.blit(title_surface, (20, 40))
            
            y_pos = 100
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else (0, 0, 0)
                opt_surface = self.font.render(option, True, color)
                self.screen.blit(opt_surface, (20, y_pos))
                y_pos += 35
                
            pygame.display.flip()
            
    def start_tutorial(self):
        """Start the selected tutorial"""
        self.clear_grid()
        self.current_pos = Vector2(0, 0)
        self.awaiting_tutorial_answer = False
        
        self.speak(f"Starting tutorial: {self.current_tutorial.title}. {self.current_tutorial.description}")
        pygame.time.wait(1000)
        self.present_next_challenge()
        
    def present_next_challenge(self):
        """Present the next challenge in the tutorial"""
        challenge = self.current_tutorial.get_current_challenge()
        if challenge:
            self.clear_grid()
            self.current_pos = Vector2(0, 0)
            
            current, total = self.current_tutorial.get_progress()
            self.speak(f"Challenge {current + 1} of {total}. {challenge.question}")
            self.awaiting_tutorial_answer = True
        else:
            self.finish_tutorial()
            
    def check_tutorial_answer(self):
        """Check the user's answer for the current challenge"""
        if not self.awaiting_tutorial_answer:
            return
            
        challenge = self.current_tutorial.get_current_challenge()
        if not challenge:
            return
            
        # Scan the entire grid for the answer
        # Students may work through problems step-by-step across multiple rows
        found_answer = None
        for y in range(self.rows):
            row_content = "".join(self.grid[y]).strip()
            if row_content and challenge.check_answer(row_content):
                found_answer = row_content
                break
        
        if not found_answer:
            # Check if there's any content at all
            has_content = False
            for y in range(self.rows):
                if "".join(self.grid[y]).strip():
                    has_content = True
                    break
            
            if not has_content:
                self.speak("Please enter your answer and press Ctrl+Enter to check.")
            else:
                self.play_sound(self.empty_sound)
                if challenge.needs_hint():
                    self.speak("Not quite. Here's a hint: " + challenge.get_hint())
                else:
                    self.speak("Not quite. Try again!")
            return
            
        # Answer found and is correct
        self.play_sound(self.content_sound)
        self.speak("Correct! " + (challenge.explanation if challenge.explanation else "Well done!"))
        pygame.time.wait(2000)
        
        self.current_tutorial.next_challenge()
        self.awaiting_tutorial_answer = False
        
        if not self.current_tutorial.is_complete():
            self.present_next_challenge()
        else:
            self.finish_tutorial()
                
    def offer_hint(self):
        """Offer a hint for the current challenge"""
        if not self.awaiting_tutorial_answer:
            return
            
        challenge = self.current_tutorial.get_current_challenge()
        if challenge:
            hint = challenge.get_hint()
            self.speak("Hint: " + hint)
            
    def finish_tutorial(self):
        """Finish the current tutorial"""
        self.speak(f"Congratulations! You've completed {self.current_tutorial.title}. Press any key to return to the tutorial menu.")
        self.tutorial_mode = False
        self.awaiting_tutorial_answer = False
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    break
                    
        self.show_main_menu()

    def draw(self):

        self.screen.fill((255, 255, 255))
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                if self.grid[y][x] != ' ':
                    text = self.font.render(str(self.grid[y][x]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        current_rect = pygame.Rect(self.current_pos.x * self.cell_size, self.current_pos.y * self.cell_size, 
                                   self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), current_rect, 3)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.confirm_exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.confirm_exit()

                        if event.key == pygame.K_F1:
                            self.show_help()
                        elif event.key == pygame.K_F2:
                            self.toggle_auto_shift()
                        elif event.key == pygame.K_F3:
                            self.toggle_smart_delete()
                        elif event.key == pygame.K_F4:
                            self.toggle_fast_move()
                        elif event.key == pygame.K_F5:
                            self.prompt_grid_resize()
                        elif event.key == pygame.K_F6:
                            if self.tutorial_mode:
                                self.offer_hint()
                        elif event.key == pygame.K_l:
                            if self.alt_pressed:
                                self.speak_row(int(self.current_pos.y))
                        elif event.key == pygame.K_RETURN:
                             if self.ctrl_pressed:
                                 if self.tutorial_mode and self.awaiting_tutorial_answer:
                                     self.check_tutorial_answer()
                                 else:
                                     self.evaluate_row()
                             else:
                                 self.move_down_to_next_stack()
                        elif event.key == pygame.K_UP:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(0, -1))
                            elif self.alt_pressed:
                                self.move_to_next_content_row(-1)
                            else:
                                self.move(Vector2(0, -1))
                        elif event.key == pygame.K_DOWN:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(0, 1))
                            elif self.alt_pressed:
                                self.move_to_next_content_row(1)
                            elif self.shift_pressed:
                                self.move_down_to_next_stack()
                            else:
                                self.move(Vector2(0, 1))


                        elif event.key == pygame.K_LEFT:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(-1, 0))
                            else:
                                self.move(Vector2(-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(1, 0))
                            else:
                                self.move(Vector2(1, 0))
                        elif event.key == pygame.K_s:
                            if self.ctrl_pressed:
                                self.save_state()
                        elif event.key == pygame.K_o:
                            if self.ctrl_pressed:
                                self.load_state()
                        elif event.key == pygame.K_e:
                            if self.ctrl_pressed:
                                self.export_text()
                        elif event.key == pygame.K_HOME:
                            if self.ctrl_pressed:
                                self.move_to_edge(Vector2(-1, -1))
                            else:
                                self.move_to_edge(Vector2(-1, 0))
                        elif event.key == pygame.K_END:
                            if self.ctrl_pressed:
                                self.move_to_edge(Vector2(1, 1))
                            else:
                                self.move_to_edge(Vector2(1, 0))
                        elif event.key == pygame.K_PAGEUP:
                            if self.ctrl_pressed:
                                self.move_to_edge(Vector2(0, -1))
                        elif event.key == pygame.K_PAGEDOWN:
                            if self.ctrl_pressed:
                                self.move_to_edge(Vector2(0, 1))
                        elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                            self.ctrl_pressed = True
                        elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                            self.alt_pressed = True
                        elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            self.shift_pressed = True
                        elif event.key == pygame.K_BACKSPACE:
                            if self.ctrl_pressed:
                                self.clear_grid()
                            else:
                                self.delete_value()
                        elif event.unicode in string.printable and not self.ctrl_pressed and not self.alt_pressed:
                            self.input_value(event.unicode)
                    elif event.type == pygame.KEYUP:
                        if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                            self.ctrl_pressed = False
                        elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                            self.alt_pressed = False
                        elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            self.shift_pressed = False

                if self.fast_move:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_move_time > 100: # 100ms delay
                        keys = pygame.key.get_pressed()
                        moved = False
                        if keys[pygame.K_UP]:
                            self.move(Vector2(0, -1))
                            moved = True
                        if keys[pygame.K_DOWN]:
                            self.move(Vector2(0, 1))
                            moved = True
                        if keys[pygame.K_LEFT]:
                            self.move(Vector2(-1, 0))
                            moved = True
                        if keys[pygame.K_RIGHT]:
                            self.move(Vector2(1, 0))
                            moved = True
                        
                        if moved:
                            self.last_move_time = current_time


                self.draw()
            except Exception as e:
                print(f"An error occurred: {e}")
                print(traceback.format_exc())
                running = False

        pygame.quit()

if __name__ == "__main__":
    frame = VirtualTaylorFrame(18, 25)
    frame.show_main_menu()
    frame.run()
