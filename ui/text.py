import pygame
from ui.widget import Widget
from ui.link import get
import time

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

        super().__init__(pos, size, name, **kwargs)

        # forced attributes
        self.has_surface = True
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._background_color = self.background_color
        self.background_color = None # widget background color fills the surface (and erases text)
        self.repeatable_event = None
        self.repeatable_first_activated = 0
        self.repeatable_last_activated = 0


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
        self.build_surface()

    def build_surface(self):
        self.surface.fill(self._background_color)

        # render cursor
        if self.selected:
            # render rect
            pygame.draw.rect(self.surface, self.cursor_color, (self.font.size(self.text[:self.cursor_pos])[0], 0, self.font.get_height()//2, self.size[1]))
        # render text
        self.surface.blit(self.font.render(self.text, True, self.text_color), (0, 0))

    def handle_event(self, event, is_under_parent=True):
        return_code = super().handle_event(event, is_under_parent)

        if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
            self.cursor_pos = self.mouse_to_cursor(event.pos)
            self.build_surface()
            return 1

        if event.type == pygame.KEYUP:
            if self.repeatable_event and self.repeatable_event.key == event.key:
                self.repeatable_event = None
                self.time_since_repeatable_first_activated = 0
                self.time_since_repeatable_last_activated = 0

        if event.type == pygame.KEYDOWN and self.selected and self.editable:
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
                self.cursor_pos = max(0, self.cursor_pos)
                self.set_repeatable(event)
                self.build_surface()
                return 1
            elif event.key == pygame.K_RIGHT and self.has_cursor:
                self.cursor_pos += 1
                self.cursor_pos = min(len(self.text), self.cursor_pos)
                self.set_repeatable(event)
                self.build_surface()
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

    def update(self):
        if self.repeatable_event:
            if time.time() - self.repeatable_last_activated > 0.03 and time.time() - self.repeatable_first_activated > 0.5:
                self.repeatable_last_activated = time.time()
                self.handle_event(self.repeatable_event, is_under_parent=False)
        super().update()
