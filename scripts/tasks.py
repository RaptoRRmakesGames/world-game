
class TaskManager:
    
    def __init__(self) -> None:
        self.tasks = {}
        
    def bind(self,key, fun, args=[]):
        self.tasks[key] = (fun, args )
        
    def do_binds(self,event):
        self.tasks[event.key][0](*self.tasks[event.key][1]) if event.key in self.tasks.keys() else 0 