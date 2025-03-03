from UI.UIobject import UIobject, link

class Group:
    def __init__(self, objects: list[UIobject]):
        self.objects = objects

    def filter(self, condition_func: callable):
        """filters the objects in the group
        
        Args:
            condition_func (callable): the condition function
        
        Returns:
            Group: the filtered group
        """

        return Group([obj for obj in self.objects if condition_func(obj)])

    def add(self, obj: UIobject):
        """adds an object to the group
        
        Args:
            obj (UIobject): the object to add
        """

        self.objects.append(obj)

    def remove(self, obj: UIobject):
        """removes an object from the group
        
        Args:
            obj (UIobject): the object to remove
        """

        self.objects.remove(obj)
