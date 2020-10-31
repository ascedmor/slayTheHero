QUIT_EVENT = 0
KEYDOWN_EVENT = 1
KEYUP_EVENT = 2
BUTTON_CLICKED_EVENT = 3
UPDATE_EVENT = 4
UPDATE_FPS_EVENT = 5
TOGGLE_FULLSCREEN_EVENT = 6
UPDATE_MOUSE_EVENT = 7
PAUSE_GAME_EVENT = 8
LOAD_ROOM_EVENT = 9
MAIN_LOOP_EVENT = 10

class Event:
    def __init__(self, event_object, event_type, id):
        self.event_object = event_object
        self.event_type = event_type
        self.id = id

class EventSystem:
    def __init__(self):
        self.event_handlers = {}
        self.event_queue = []
        self.running = False

    def add_event_type(self, event_type):
        self.event_handlers[event_type] = {}

    def add_event_handler(self, event_type, event_id, function):
        if event_type in self.event_handlers:
            self.event_handlers[event_type][event_id] = function

    def FireEvent(self, event_object, event_type, event_id):
        self.event_queue.append(Event(event_object, event_type, event_id))

    def do_event(self, event):
        if self.running:
            self.event_handlers[event.event_type][event.id](event)

    def process(self):
        if len(self.event_queue)>0:
            event = self.event_queue.pop(0)
            self.do_event(event)

    def on_close(self):
        self.running = False
        self.event_queue.clear()
