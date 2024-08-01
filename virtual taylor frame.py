import os
import sys
import pygame
import pygame.mixer
import numpy as np
from pygame.math import Vector2
from cytolk import tolk
import traceback
import string

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
                    content+=" times"
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
        Arrow keys: Move cursor.
        Ctrl + Arrow keys: Snap to content.
        Shift + Down: Move to next stack.
        Home/End: Move to start/end of row.
        Ctrl + Home/End: Move to start/end of grid.
        Ctrl + PageUp/PageDown: Move to top/bottom of column.
        Backspace: Delete content.
        Ctrl + Backspace: Clear entire grid.
        """
        self.speak(help_text)
        
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
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.show_help()
                        elif event.key == pygame.K_F2:
                            self.toggle_auto_shift()
                        elif event.key == pygame.K_F3:
                            self.toggle_smart_delete()
                        elif event.key == pygame.K_F4:
                            self.toggle_fast_move()
                        elif event.key == pygame.K_UP:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(0, -1))
                            else:
                                self.move(Vector2(0, -1))
                        elif event.key == pygame.K_DOWN:
                            if self.ctrl_pressed:
                                self.snap_to_content(Vector2(0, 1))
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
                        elif event.unicode in string.printable:
                            self.input_value(event.unicode)
                    elif event.type == pygame.KEYUP:
                        if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                            self.ctrl_pressed = False
                        elif event.key in [pygame.K_LALT, pygame.K_RALT]:
                            self.alt_pressed = False
                        elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            self.shift_pressed = False
                
                if self.fast_move:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.move(Vector2(0, -1))
                    if keys[pygame.K_DOWN]:
                        self.move(Vector2(0, 1))
                    if keys[pygame.K_LEFT]:
                        self.move(Vector2(-1, 0))
                    if keys[pygame.K_RIGHT]:
                        self.move(Vector2(1, 0))
                
                self.draw()
            except Exception as e:
                print(f"An error occurred: {e}")
                print(traceback.format_exc())
                running = False
        
        pygame.quit()

if __name__ == "__main__":
    frame = VirtualTaylorFrame(18, 25)
    frame.run()
