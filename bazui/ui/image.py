import pygame
from ui.widget import Widget
from ui.link import get

class Image(Widget):
    def __init__(self, pos, size, name, app, image, **kwargs):
        super().__init__(pos, size, name, app)
        self.image = image

        # customizable attributes
        self.im_sizing = "fitmin"   # image sizing (stretch, fitmin, fitmax, fixed)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Image has no attribute {key}")

        # forced attributes
        self.has_surface = True
        self.r_image = self.image # the image to be rendered
        self.render_method = self.blit_image

        self._image_setup()


    def _image_setup(self):
        self.surface = pygame.Surface(get(self.size), pygame.SRCALPHA)

    def blit_image(self, _):
        desired_size = None
        if self.im_sizing == "stretch":
            desired_size = get(self.size)
        elif self.im_sizing == "fitmin":
            # fit the image to the widget size, keeping the aspect ratio
            desired_size = get(self.size)
            image_ratio = self.image.get_width() / self.image.get_height()
            widget_ratio = desired_size[0] / desired_size[1]
            if image_ratio > widget_ratio:
                desired_size = (desired_size[0], int(desired_size[0] / image_ratio))
            else:
                desired_size = (int(desired_size[1] * image_ratio), desired_size[1])
        elif self.im_sizing == "fitmax":
            # fit the image to the widget size, keeping the aspect ratio
            desired_size = get(self.size)
            image_ratio = self.image.get_width() / self.image.get_height()
            widget_ratio = desired_size[0] / desired_size[1]
            if image_ratio < widget_ratio:
                desired_size = (desired_size[0], int(desired_size[0] / image_ratio))
            else:
                desired_size = (int(desired_size[1] * image_ratio), desired_size[1])
        elif self.im_sizing == "fixed":
            self.r_image = self.image
        else:
            raise ValueError(f"Invalid image sizing method: {self.im_sizing}.")

        if desired_size and desired_size != self.r_image.get_size():
            self.r_image = pygame.transform.scale(self.image, desired_size)

        im_pos = (get(self.size)[0] / 2 - self.r_image.get_width() / 2, get(self.size)[1] / 2 - self.r_image.get_height() / 2)
        self.surface.blit(self.r_image, im_pos)
