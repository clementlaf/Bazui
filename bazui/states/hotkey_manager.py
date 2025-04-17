import pygame

MOD_KEYS = {
    "ctrl": pygame.KMOD_CTRL,
    "shift": pygame.KMOD_SHIFT,
    "alt": pygame.KMOD_ALT,
}

def normalize_mod(mod):
    normalized = 0
    if mod & (pygame.KMOD_LCTRL | pygame.KMOD_RCTRL):
        normalized |= pygame.KMOD_CTRL
    if mod & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
        normalized |= pygame.KMOD_SHIFT
    if mod & (pygame.KMOD_LALT | pygame.KMOD_RALT):
        normalized |= pygame.KMOD_ALT
    return normalized

def parse_shortcut(shortcut):
    """Parse a shortcut string into a key and modifier keys.

    Args:
        shortcut (str): The shortcut string, e.g. "ctrl+shift+a".

    Returns:
        tuple: A tuple containing the key and modifier keys.
    """
    parts = shortcut.split("+")
    mods=0
    key = None
    for part in parts:
        if part in MOD_KEYS:
            mods |= MOD_KEYS[part]
        else:
            key = getattr(pygame, f"K_{part}", None)
            if key is None:
                raise ValueError(f"Invalid key: {part}")
    if key is None:
        raise ValueError("No key specified in shortcut")
    print(f"Parsed shortcut: {shortcut} -> key: {key}, mods: {mods}")
    return key, mods

class HotkeyManager:
    def __init__(self):
        self._bindings = []

    def bind(self, shortcut, callback=None):
        key, mods = parse_shortcut(shortcut)
        self._bindings.append((key, mods, callback))

    def handle_events(self, event):
        if event.type != pygame.KEYDOWN:
            return
        norm_mod = normalize_mod(event.mod)
        for key, required_mods, callback in self._bindings:
            if event.key == key and (norm_mod & required_mods) == required_mods:
                if callback:
                    callback()
