from ui2.attributes import FIXED, FIT, GROW, Padding, minmax
from ui2.vector2D import Vector2D as v

class UIElement:
    def __init__(self, parent):
        self.position = v(0, 0)
        self.size = v(0, 0)

        self.parent = parent
        self.children = []

        self.layout = 0 # 0 = horizontal, 1 = vertical

        self.padding = Padding()
        self.child_gap = 0

        self.sizing = (FIT(), FIT())

    ### Layout ###

    def initialize_sizes(self):
        for axis, sizing in enumerate(self.sizing):
            if isinstance(sizing, FIXED):
                self.size[axis] = sizing()
            elif isinstance(sizing, FIT):
                self.size[axis] = 0
            elif isinstance(sizing, GROW):
                self.size[axis] = 0

    def fit_sizing(self, axis):
        for child in self.children:
            child.fit_sizing(axis)
        
        sizing = self.sizing[axis]
        if isinstance(sizing, FIT):
            self.fit(axis)
            self.size[axis] = minmax(self.size[axis], sizing.min, sizing.max)

    def fit(self, axis):
        if self.layout == axis:
            self.size[axis] += sum(self.padding.on_axis(axis))
            self.size[axis] += max(self.child_gap * (len(self.children) - 1), 0)
            for child in self.children:
                self.size[axis] += child.size[axis]
        else:
            self.size[axis] += sum(self.padding.on_axis(axis))
            max_child_size = max(child.size[axis] for child in self.children)
            self.size[axis] += max_child_size

    def grow_and_shrink_childs(self, axis):
        if self.layout == axis:
            current_size = sum(self.padding.on_axis(axis)) + max(self.child_gap * (len(self.children) - 1), 0) + sum(child.size[axis] for child in self.children)
            remaining_size = self.size[axis] - current_size
            if remaining_size > 0:
                self.grow_childs_along_axis(axis, remaining_size)
            elif remaining_size < 0:
                self.shrink_childs_along_axis(axis, remaining_size)
        else:
            self.grow_childs_against_axis(self)

        for child in self.children:
            child.grow_and_shrink_sizing(axis)

    def grow_childs_along_axis(self, remaining_size):
        growables = [child for child in self.children if isinstance(child.sizing[self.layout], GROW)]
        while remaining_size > 0:
            smallest = growables[0].size[self.layout]
            second_smallest = float("inf")
            width_to_add = remaining_size
            for child in growables:
                if child.size[self.layout] < smallest:
                    second_smallest = smallest
                    smallest = child.size[self.layout]
                if child.size[self.layout] > smallest:
                    second_smallest = min(second_smallest, child.size[self.layout])
                    width_to_add = second_smallest - smallest
            
            width_to_add = min(width_to_add, remaining_size / len(growables))

            for child in growables:
                previous_width = child.size[self.layout]
                if child.size[self.layout] == smallest:
                    child.size[self.layout] += width_to_add
                    if child.size[self.layout] >= child.sizing[self.layout].max:
                        growables.remove(child)
                    remaining_size -= (child.size[self.layout] - previous_width)

    def shrink_childs_along_axis(self, remaining_size):
        shrinkables = [child for child in self.children if isinstance(child.sizing[self.layout], GROW)]
        while remaining_size < 0:
            largest = shrinkables[0].size[self.layout]
            second_largest = 0
            width_to_add = remaining_size
            for child in shrinkables:
                if child.size[self.layout] > largest:
                    second_largest = largest
                    largest = child.size[self.layout]
                if child.size[self.layout] > largest:
                    second_largest = max(second_largest, child.size[self.layout])
                    width_to_add = second_largest - largest
            
            width_to_add = max(width_to_add, remaining_size / len(shrinkables))

            for child in shrinkables:
                previous_width = child.size[self.layout]
                if child.size[self.layout] == largest:
                    child.size[self.layout] += width_to_add
                    if child.width <= child.sizing[self.layout].min:
                        shrinkables.remove(child)
                    remaining_size -= (child.size[self.layout] - previous_width)

    def grow_childs_against_axis(self):
        growables = [child for child in self.children if isinstance(child.sizing[self.layout], GROW)]
        for child in growables:
            child.size[1-self.layout] = self.size[1-self.layout] - sum(self.padding.on_axis(1-self.layout))

    ### Drawing ###

    def draw(self, screen):
