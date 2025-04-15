import time
from string import ascii_letters as al
import pygame
from bazui.ui.widget import Widget
from bazui.ui.link import get

class SingleLineText(Widget):
    def __init__(self, pos, size, name, app, **kwargs):
        super().__init__(pos, size, name, app)

        # customisable attributes
        self.text = ""
        self.font = pygame.font.Font()
        self.text_color = (255, 255, 255)
        self.size_auto_fit = False
        self.editable = False
        self.selectable = False
        self.cursor_pos = 0
        self.cursor_color = (255, 255, 255)
        self.selection_color = "#264F78"
        self.redo_stack_max_size = self.app.app_state.redo_stack_max_size
        self.undo_stack_max_size = self.app.app_state.undo_stack_max_size
        self.on_change = None

        self.background_color = (0, 0, 0, 0)
        self.on_drag = self.base_comportment_when_dragged

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"SingleLineText has no attribute {key}")

        # forced attributes
        self.has_surface = True
        self.surface = pygame.Surface(get(self.size), pygame.SRCALPHA)
        self._background_color = self.background_color
        self.can_be_dragged = self.selectable
        self.repeatable_event = None
        self.repeatable_first_activated = 0
        self.repeatable_last_activated = 0
        self.text_render = None
        self.undo_stack = []
        self.redo_stack = []
        self.selection_start = None
        self.selection_end = None
        self.time_at_update = 0
        self.previous_text = self.text


        # initialize attributes
        self._text_setup()

    def _text_setup(self):
        self.set_text(self.text)
        self.cursor_pos = len(self.text)

    def set_text(self, text):
        self.text = text
        if self.size_auto_fit:
            self.size = self.font.size(self.text)[0], self.size[1] # add space to render cursor on last char
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.build_text_render()
        self.time_at_update = time.time()

    def build_text_render(self):
        self.text_render = self.font.render(self.text, True, self.text_color)

    def handle_event(self, event, is_under_parent=True):
        return_code = super().handle_event(event, is_under_parent)

        if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
            self.cursor_pos = self.mouse_to_cursor(event.pos)
            self.time_at_update = time.time()
            self.reset_selection()
            return 1

        if event.type == pygame.MOUSEBUTTONDOWN and self.selection_start is not None:
            if not self.rect.collidepoint(event.pos):
                self.reset_selection()

        if self.editable:

            if event.type == pygame.KEYUP:
                if self.repeatable_event and self.repeatable_event.key == event.key:
                    self.repeatable_event = None
                    self.repeatable_first_activated = 0
                    self.repeatable_last_activated = 0

            if event.type == pygame.KEYDOWN and self.selected:
                if (pygame.key.get_mods() & pygame.KMOD_SHIFT) and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if event.key == pygame.K_LEFT: # CTRL + SHIFT + LEFT (select word to the left)
                        if self.selection_start is None:
                            self.selection_start = self.cursor_pos
                        self.cursor_pos = self.crtl_get_prec()
                        self.selection_end = self.cursor_pos
                        self.set_repeatable(event)
                    if event.key == pygame.K_RIGHT: # CTRL + SHIFT + RIGHT (select word to the right)
                        if self.selection_start is None:
                            self.selection_start = self.cursor_pos
                        self.cursor_pos = self.ctrl_get_next()
                        self.selection_end = self.cursor_pos
                        self.set_repeatable(event)
                elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_LEFT: # SHIFT + LEFT (select to the left)
                        if self.selection_start is None:
                            self.selection_start = self.cursor_pos
                        self.cursor_pos -= 1
                        self.bound_cursor()
                        self.selection_end = self.cursor_pos
                        self.set_repeatable(event)
                    if event.key == pygame.K_RIGHT: # SHIFT + RIGHT (select to the right)
                        if self.selection_start is None:
                            self.selection_start = self.cursor_pos
                        self.cursor_pos += 1
                        self.bound_cursor()
                        self.selection_end = self.cursor_pos
                        self.set_repeatable(event)
                    if event.unicode not in ['¨', '^', '']: # SHIFT + ANY (maj + char)
                        self.write(event.unicode)
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1
                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.key == pygame.K_z: # CTRL + Z (undo)
                        self.undo()
                    if event.key == pygame.K_y: # CTRL + Y (redo)
                        self.redo()
                    if event.key == pygame.K_a: # CTRL + A (select all)
                        self.selection_start = 0
                        self.selection_end = len(self.text)
                        self.cursor_pos = len(self.text)
                        self.set_repeatable(event)
                    if event.key == pygame.K_LEFT: # CTRL + LEFT (move cursor to the left by word)
                        self.cursor_pos = self.crtl_get_prec()
                        self.set_repeatable(event)
                    if event.key == pygame.K_RIGHT: # CTRL + RIGHT (move cursor to the right by word)
                        self.cursor_pos = self.ctrl_get_next()
                        self.set_repeatable(event)
                    if event.key == pygame.K_BACKSPACE: # CTRL + BACKSPACE (delete word to the left)
                        start = self.crtl_get_prec()
                        end = self.cursor_pos
                        self.delete_group(start, end)
                        self.set_repeatable(event)
                    if event.key == pygame.K_DELETE: # CTRL + DELETE (delete word to the right)
                        start = self.cursor_pos
                        end = self.ctrl_get_next()
                        self.delete_group(start, end)
                        self.set_repeatable(event)
                else:
                    if event.key == pygame.K_BACKSPACE: # BACKSPACE
                        self.delete()
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1
                    elif event.key == pygame.K_DELETE: # DELETE
                        self.suppress()
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1
                    elif event.key == pygame.K_RETURN: # ENTER
                        return 1
                    elif event.key == pygame.K_LEFT and self.editable: # LEFT
                        self.cursor_pos -= 1
                        self.bound_cursor()
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1
                    elif event.key == pygame.K_RIGHT and self.editable: # RIGHT
                        self.cursor_pos += 1
                        self.bound_cursor()
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1
                    if event.unicode not in ['¨', '^', '']: # ANY (char)
                        self.write(event.unicode)
                        self.reset_selection()
                        self.set_repeatable(event)
                        return 1

        return return_code

    def write(self, text_input):
        if self.selection_start is not None:
            start = min(self.selection_start, self.selection_end)
            end = max(self.selection_start, self.selection_end)
            self.delete_group(start, end)
            self.reset_selection()
        text = self.text[:self.cursor_pos] + text_input + self.text[self.cursor_pos:]
        self.cursor_pos += len(text_input)
        self.set_text(text)

    def delete(self):
        if self.selection_start is not None:
            start = min(self.selection_start, self.selection_end)
            end = max(self.selection_start, self.selection_end)
            self.delete_group(start, end)
            self.reset_selection()
            return
        if self.cursor_pos == 0:
            return
        text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
        self.cursor_pos -= 1
        self.set_text(text)

    def suppress(self):
        if self.selection_start is not None:
            start = min(self.selection_start, self.selection_end)
            end = max(self.selection_start, self.selection_end)
            self.delete_group(start, end)
            self.reset_selection()
            return
        if self.cursor_pos == len(self.text):
            return
        text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
        self.set_text(text)

    def mouse_to_cursor(self, pos):
        relative_pos = (pos[0] - get(self.pos)[0], pos[1] - get(self.pos)[1])
        for i in range(len(self.text) + 1):
            diff = self.font.size(self.text[:i])[0] - relative_pos[0]
            if diff >= 0:

                diff_prev = self.font.size(self.text[:i - 1])[0] - relative_pos[0]
                ret = i
                if abs(diff_prev) < abs(diff):
                    ret = i - 1
                ret = max(0, min(ret, len(self.text)))
                return ret

        return len(self.text)

    def set_repeatable(self, event):
        if self.repeatable_event != event:
            self.repeatable_event = event
            self.repeatable_first_activated = time.time()
            self.repeatable_last_activated = time.time()

            if event is not None:
                self.save_state_to_stack()

    def update(self):
        if self.repeatable_event:
            if time.time() - self.repeatable_last_activated > 0.04 and time.time() - self.repeatable_first_activated > 0.5:
                self.repeatable_last_activated = time.time()
                self.handle_event(self.repeatable_event, is_under_parent=False)
        super().update()

        if self.text != self.previous_text:
            self.previous_text = self.text
            if self.on_change:
                self.on_change(self.text)

    def access_surface(self):
        # clear surface
        super().access_surface()
        # render selection
        if self.selection_start is not None:
            sel_min = min(self.selection_start, self.selection_end)
            sel_max = max(self.selection_start, self.selection_end)
            sel_rect = pygame.Rect(self.font.size(self.text[:sel_min])[0], 0, self.font.size(self.text[sel_min:sel_max])[0], get(self.size)[1])
            pygame.draw.rect(self.surface, self.selection_color, sel_rect)
        # render cursor
        if self.selected and self.editable:
            # draw cursor
            if (time.time() - self.time_at_update) % 1 < 0.5:
                pygame.draw.rect(self.surface, self.cursor_color, (self.font.size(self.text[:self.cursor_pos])[0], 0, 2, get(self.size)[1]))
        # render text
        self.surface.blit(self.text_render, (0, 0))

        return self.surface

    def save_state_to_stack(self):
        self.undo_stack.append((self.text, self.cursor_pos, self.selection_start, self.selection_end))

        if len(self.undo_stack) > self.undo_stack_max_size:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append((self.text, self.cursor_pos, self.selection_start, self.selection_end))
            new_text, self.cursor_pos, self.selection_start, self.selection_end = self.undo_stack.pop()
            self.set_text(new_text)

            if len(self.redo_stack) > self.redo_stack_max_size:
                self.redo_stack.pop(0)

            self.bound_cursor()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append((self.text, self.cursor_pos, self.selection_start, self.selection_end))
            new_text, self.cursor_pos, self.selection_start, self.selection_end = self.redo_stack.pop()
            self.set_text(new_text)

            if len(self.undo_stack) > self.undo_stack_max_size:
                self.undo_stack.pop(0)

            self.bound_cursor()

    def bound_cursor(self):
        self.cursor_pos = max(0, min(self.cursor_pos, len(self.text)))

    def crtl_get_prec(self)-> int:
        """Finds the precedent word-space transition in the text.

        Returns:
            int: The index of the precedent word transition.
        """

        if self.cursor_pos == 0:
            return 0

        obj_pos = max(0, self.cursor_pos - 1)
        while not(self.text[obj_pos] in al and self.text[obj_pos - 1] not in al) and obj_pos > 0:
            obj_pos -= 1

        return obj_pos

    def ctrl_get_next(self)-> int:
        """Finds the next word-space transition in the text.

        Returns:
            int: The index of the next word transition.
        """

        if self.cursor_pos >= len(self.text) - 1:
            return len(self.text)

        obj_pos = min(self.cursor_pos + 1, len(self.text))
        while not(self.text[obj_pos] not in al and self.text[obj_pos - 1] in al) and obj_pos < len(self.text) - 1:
            obj_pos += 1

        return obj_pos

    def delete_group(self, start, end):
        """Deletes a group of characters from the text.

        Args:
            start (int): The start index of the group.
            end (int): The end index of the group.
        """

        text = self.text[:start] + self.text[end:]
        self.cursor_pos = start
        self.set_text(text)

    def reset_selection(self):
        self.selection_start = None
        self.selection_end = None

    def base_comportment_when_dragged(self):
        mouse_pos = self.app.app_state.mouse_pos
        crt_cursor_pos = self.mouse_to_cursor(mouse_pos)
        if self.selection_start is None:
            self.selection_start = self.cursor_pos
        self.cursor_pos = crt_cursor_pos
        self.selection_end = self.cursor_pos
        self.time_at_update = time.time()


class MultiLineText(SingleLineText):
    def __init__(self, pos, size, name, app, **kwargs):
        self.line_spacing = 0
        self.paragraph_spacing = 0
        self.max_lines = None
        super().__init__(pos, size, name, app, **kwargs)


    def decompose_text(self):
        """Break self.text into display lines, handling wrapping."""
        raw_lines = self.text.split("\n")
        max_width = get(self.size)[0]
        result_lines = []

        for raw_line in raw_lines:

            if raw_line == "":
                result_lines.append(Line("", starts_paragraph=True))
                continue

            words = raw_line.split(" ")
            current_line = ""
            is_first = True
            is_word_break = False

            while words:
                word = words[0]
                test_line = current_line + (" " if current_line else "") + word
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                    words.pop(0)
                else:
                    if current_line == "":
                        # word too long to fit alone — set as much of it as possible
                        # find the longest prefix that fits
                        for i in range(len(word), 0, -1):
                            test_line = word[:i]
                            if self.font.size(test_line)[0] <= max_width:
                                break
                        current_line = word[:i]
                        words[0] = word[i:]  # put the rest back in the list
                        result_lines.append(Line(current_line, starts_paragraph=is_first, is_word_break=is_word_break))
                        is_word_break = True
                    else:
                        result_lines.append(Line(current_line, starts_paragraph=is_first, is_word_break=is_word_break))
                        is_word_break = False
                    current_line = ""
                    is_first = False

            if current_line:
                result_lines.append(Line(current_line, starts_paragraph=is_first, is_word_break=is_word_break))

        return result_lines

    def text_pos_to_line_pos(self, pos):
        """Convert character index `pos` in self.text to (line_index, in_line_pos)."""
        if not self.lines:
            return 0, 0

        current_pos = 0

        for i, line in enumerate(self.lines):
            line_len = len(line.text)
            if line.is_word_break:
                current_pos -= 1 # there was no character between lines
            if pos <= current_pos + line_len:
                return i, pos - current_pos
            current_pos += line_len + 1 # +1 for the '\n' character or the space separator


        # Clamp to end
        last_line = len(self.lines) - 1
        return last_line, len(self.lines[last_line].text)

    def line_pos_to_text_pos(self, line_idx, in_line_pos):
        """Convert (line, col) back to char index in full self.text"""
        pos = 0
        for i in range(line_idx):
            pos += len(self.lines[i].text) + 1 # +1 for the '\n' character or the space separator
            if self.lines[i].is_word_break:
                pos -= 1
        if self.lines[line_idx].is_word_break:
            pos -= 1
        return pos + in_line_pos

    def line_pos_to_px_pos(self, line_pos):
        """Converts a line position to a pixel position.

        Args:
            line_pos (int): The line position.

        Returns:
            int: The pixel position.
        """

        line_px_pos = 0
        for i in range(line_pos):
            if self.lines[i].starts_paragraph:
                line_px_pos += self.paragraph_spacing
            else:
                line_px_pos += self.line_spacing
            line_px_pos += self.font.get_height()

        if self.lines[line_pos].starts_paragraph:
            line_px_pos += self.paragraph_spacing
        else:
            line_px_pos += self.line_spacing
        return line_px_pos

    def set_text(self, text):
        self.text = text
        self.bound_text_to_max_lines()
        self.lines = self.decompose_text()
        if self.size_auto_fit:
            self.size = get(self.size[0]), self.line_pos_to_px_pos(len(self.lines)-1) + self.font.get_height() + self.paragraph_spacing
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.build_text_render()
        self.time_at_update = time.time()

    def build_text_render(self):
        self.text_render = [self.font.render(line.text, True, self.text_color) for line in self.lines]

    def access_surface(self):

        # clear surface
        Widget.access_surface(self)
        # render selection
        if self.selection_start is not None:
            sel_min = min(self.selection_start, self.selection_end)
            sel_max = max(self.selection_start, self.selection_end)

            start_line_pos, start_char_pos = self.text_pos_to_line_pos(sel_min)
            end_line_pos, end_char_pos = self.text_pos_to_line_pos(sel_max)
            start_line_px_pos = self.line_pos_to_px_pos(start_line_pos)
            end_line_px_pos = self.line_pos_to_px_pos(end_line_pos)
            # draw selection rect
            if start_line_pos == end_line_pos:
                sel_rect = pygame.Rect(self.font.size(self.lines[start_line_pos].text[:start_char_pos])[0], start_line_px_pos, self.font.size(self.lines[start_line_pos].text[start_char_pos:end_char_pos])[0], self.font.get_height())
                pygame.draw.rect(self.surface, self.selection_color, sel_rect)
            else:
                # draw selection rect for first line
                sel_rect = pygame.Rect(self.font.size(self.lines[start_line_pos].text[:start_char_pos])[0], start_line_px_pos, self.font.size(self.lines[start_line_pos].text[start_char_pos:])[0], self.font.get_height())
                pygame.draw.rect(self.surface, self.selection_color, sel_rect)
                # draw selection rect for last line
                sel_rect = pygame.Rect(0, end_line_px_pos, self.font.size(self.lines[end_line_pos].text[:end_char_pos])[0], self.font.get_height())
                pygame.draw.rect(self.surface, self.selection_color, sel_rect)
                # draw selection rect for middle lines
                for i in range(start_line_pos + 1, end_line_pos):
                    sel_rect = pygame.Rect(0, self.line_pos_to_px_pos(i), get(self.size)[0], self.font.get_height())
                    pygame.draw.rect(self.surface, self.selection_color, sel_rect)

        # render cursor
        if self.selected and self.editable:
            # draw cursor
            if (time.time() - self.time_at_update) % 1 < 0.5:
                line_pos, char_pos = self.text_pos_to_line_pos(self.cursor_pos)
                line_px_pos = self.line_pos_to_px_pos(line_pos)
                pygame.draw.rect(self.surface, self.cursor_color, (self.font.size(self.lines[line_pos].text[:char_pos])[0], line_px_pos, 2, self.font.get_height()))
        # render text
        for i, _ in enumerate(self.lines):
            line_pos = self.line_pos_to_px_pos(i)
            self.surface.blit(self.text_render[i], (0, line_pos))

        return self.surface

    def mouse_to_cursor(self, pos):
        """Converts a mouse position to a cursor position.

        Args:
            pos (tuple): The mouse position.

        Returns:
            int: The cursor position.
        """

        relative_pos = (pos[0] - get(self.pos)[0], pos[1] - get(self.pos)[1])
        # line position
        line_pos = 0
        for i in range(len(self.lines)):
            line_px_pos = self.line_pos_to_px_pos(i)
            if relative_pos[1] < line_px_pos:
                break
            line_pos = i
        # if the line position is out of range, set it to the last line
        if line_pos >= len(self.lines):
            line_pos = len(self.lines) - 1
        # if the line position is negative, set it to the first line
        if line_pos < 0:
            line_pos = 0
        # character position
        char_pos = 0
        line_text = self.lines[line_pos].text
        for i in range(len(line_text) + 1):
            diff = self.font.size(line_text[:i])[0] - relative_pos[0]
            if diff >= 0:

                diff_prev = self.font.size(line_text[:i - 1])[0] - relative_pos[0]
                ret = i
                if abs(diff_prev) < abs(diff):
                    ret = i - 1
                char_pos = max(0, min(ret, len(line_text)))
                return self.line_pos_to_text_pos(line_pos, char_pos)
        return self.line_pos_to_text_pos(line_pos, len(line_text))

    def handle_event(self, event, is_under_parent=True):
        return_code = super().handle_event(event, is_under_parent)
        
        if self.editable:

            if event.type == pygame.KEYDOWN and self.selected:

                if event.key == pygame.K_RETURN:
                    self.write("\n")
                    self.reset_selection()
                    self.set_repeatable(event)
                    return 1

        return return_code

    def bound_text_to_max_lines(self):
        """Adjusts the text to fit within the maximum number of lines."""
        if self.max_lines is not None:
            lines = self.text.split("\n")
            if len(lines) > self.max_lines:
                self.text = "\n".join(lines[:self.max_lines])
                self.bound_cursor()


class Line:
    def __init__(self, text, starts_paragraph=False, is_word_break=False):
        self.text = text
        self.starts_paragraph = starts_paragraph
        self.is_word_break = is_word_break
