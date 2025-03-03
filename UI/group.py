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
