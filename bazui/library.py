import threading
import queue
import pygame


class ImageLibrary:
    def __init__(self):
        self._resources = {}
        self._load_queue = queue.Queue()
        self._lock = threading.Lock()
        self._loading_thread = threading.Thread(target=self._background_image_loader, daemon=True)
        self._loading_thread.start()

    def _background_image_loader(self):
        while True:
            im_data = self._load_queue.get()
            if im_data is None:
                break
            try:
                path = im_data["path"]
                name = im_data["name"]
                image = pygame.image.load(path).convert_alpha()
                with self._lock:
                    self._resources[name] = image
            except Exception as e:
                print(f"Error loading {path}: {e}")
            finally:
                self._load_queue.task_done()

    def load_async(self, file_list: list[dict["name": str, "path": str]]):
        """Load images asynchronously."""
        for el in file_list:
            if el.get("name") not in self:
                self._load_queue.put(el)

    def __setitem__(self, name, image):
        """Set an object in the library.

        Args:
            name (str): The name of the object.
            image (object): The object to be stored.
        """
        self.load_async([{"name": name, "path": image}])

    def __getitem__(self, name):
        """Get an object from the library.

        Args:
            name (str): The name of the object.

        Returns:
            object: The object. If not found, returns None.
        """
        return self._resources.get(name, None)

    def __contains__(self, name):
        """Check if an object is in the library.

        Args:
            name (str): The name of the object.

        Returns:
            bool: True if the object is in the library, False otherwise.
        """
        return name in self._resources

    def __delitem__(self, name):
        """Delete an object from the library.

        Args:
            name (str): The name of the object.
        """
        if name in self._resources:
            del self._resources[name]

    def __repr__(self):
        """Get a string representation of the library.

        Returns:
            str: The string representation of the library.
        """
        return f"ImageLibrary({len(self._resources)} items) \n" + "\n".join(self._resources.keys())