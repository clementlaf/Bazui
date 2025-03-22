import time
from string import ascii_letters as al
import pygame
from ui.widget import Widget
from ui.link import get

class SingleLineText(Widget):
    def __init__(self, pos, size, name, **kwargs):
        # attributes
        self.text = ""
        self.font = pygame.font.Font()
        self.text_color = (255, 255, 255)
        self.size_auto_fit = False
        self.editable = False
        self.has_cursor = True
        self.cursor_pos = 0
        self.cursor_color = (50, 0, 100)
        self.redo_stack_max_size = 20
        self.undo_stack_max_size = 20

        # modified default attributes
        self.background_color = (0, 0, 0, 0)

        super().__init__(pos, size, name, **kwargs)

        # forced attributes
        self.has_surface = True
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._background_color = self.background_color
        self.repeatable_event = None
        self.repeatable_first_activated = 0
        self.repeatable_last_activated = 0
        self.text_render = None
        self.undo_stack = []
        self.redo_stack = []
        self.selection_start = None  # selection end is always cursor_pos


        # initialize attributes
        self._text_setup()

    def _text_setup(self):
        self.set_text(self.text)
        self.cursor_pos = len(self.text)

    def set_text(self, text):
        self.text = text
        if self.size_auto_fit:
            self.size = self.font.size(self.text + ' ')[0], self.size[1] # add space to render cursor on last char
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.build_text_render()

    def build_text_render(self):
        self.text_render = self.font.render(self.text, True, self.text_color)

    def handle_event(self, event, is_under_parent=True):
        return_code = super().handle_event(event, is_under_parent)

        if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
            self.cursor_pos = self.mouse_to_cursor(event.pos)
            self.build_text_render()
            return 1

        if event.type == pygame.KEYUP:
            if self.repeatable_event and self.repeatable_event.key == event.key:
                self.repeatable_event = None
                self.repeatable_first_activated = 0
                self.repeatable_last_activated = 0

        if event.type == pygame.KEYDOWN and self.selected and self.editable:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if event.key == pygame.K_z:
                    self.undo()
                if event.key == pygame.K_y:
                    self.redo()
                if event.key == pygame.K_LEFT:
                    self.cursor_pos = self.crtl_get_prec()
                    self.set_repeatable(event)
                if event.key == pygame.K_RIGHT:
                    self.cursor_pos = self.ctrl_get_next()
                    self.set_repeatable(event)
                if event.key == pygame.K_BACKSPACE:
                    start = self.crtl_get_prec()
                    end = self.cursor_pos
                    self.delete_group(start, end)
                    self.set_repeatable(event)
                if event.key == pygame.K_DELETE:
                    start = self.cursor_pos
                    end = self.ctrl_get_next()
                    self.delete_group(start, end)
                    self.set_repeatable(event)
            else:
                if event.key == pygame.K_BACKSPACE:
                    self.delete()
                    self.set_repeatable(event)
                    return 1
                elif event.key == pygame.K_DELETE:
                    self.suppress()
                    self.set_repeatable(event)
                    return 1
                elif event.key == pygame.K_RETURN:
                    return 1
                elif event.key == pygame.K_LEFT and self.has_cursor:
                    self.cursor_pos -= 1
                    self.bound_cursor()
                    self.set_repeatable(event)
                    return 1
                elif event.key == pygame.K_RIGHT and self.has_cursor:
                    self.cursor_pos += 1
                    self.bound_cursor()
                    self.set_repeatable(event)
                    return 1
                if event.unicode not in ['¨', '^']:
                    self.write(event.unicode)
                    self.set_repeatable(event)
                    return 1


        return return_code

    def write(self, text_input):
        text = self.text[:self.cursor_pos] + text_input + self.text[self.cursor_pos:]
        self.cursor_pos += len(text_input)
        self.set_text(text)

    def delete(self):
        if self.cursor_pos == 0:
            return
        text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
        self.cursor_pos -= 1
        self.set_text(text)

    def suppress(self):
        if self.cursor_pos == len(self.text):
            return
        text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
        self.set_text(text)

    def mouse_to_cursor(self, pos):
        relative_pos = (pos[0] - get(self.pos)[0], pos[1] - get(self.pos)[1])
        for i in range(len(self.text) + 1):
            if self.font.size(self.text[:i])[0] > relative_pos[0]:
                return i - 1
        return len(self.text)

    def set_repeatable(self, event):
        if self.repeatable_event != event:
            self.repeatable_event = event
            self.repeatable_first_activated = time.time()
            self.repeatable_last_activated = time.time()

            self.save_state_to_stack()

    def update(self):
        if self.repeatable_event:
            if time.time() - self.repeatable_last_activated > 0.05 and time.time() - self.repeatable_first_activated > 0.5:
                self.repeatable_last_activated = time.time()
                self.handle_event(self.repeatable_event, is_under_parent=False)
        super().update()

    def access_surface(self):
        # clear surface
        if self.background_color:
            self.surface.fill(self._background_color)
        # render cursor
        if self.selected:
            pygame.draw.rect(self.surface, self.cursor_color, (self.font.size(self.text[:self.cursor_pos])[0], 0, self.font.get_height()//2, self.size[1]))
        # render text
        self.surface.blit(self.text_render, (0, 0))

        return self.surface

    def save_state_to_stack(self):
        self.undo_stack.append((self.text, self.cursor_pos))

        if len(self.undo_stack) > self.undo_stack_max_size:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append((self.text, self.cursor_pos))
            new_text, self.cursor_pos = self.undo_stack.pop()
            self.set_text(new_text)

            if len(self.redo_stack) > self.redo_stack_max_size:
                self.redo_stack.pop(0)

            self.bound_cursor()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append((self.text, self.cursor_pos))
            new_text, self.cursor_pos = self.redo_stack.pop()
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

        obj_pos = self.cursor_pos - 1
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

        obj_pos = self.cursor_pos + 1
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
