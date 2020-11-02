class EventObject:
    counter=0
    def __init__(self):
        self.id=self.counter
        self.counter+=1
