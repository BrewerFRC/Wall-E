class Action:

    def __init__(self, run, time=None, trigger=None):
        self.run = run
        self.time = time
        self.trigger = trigger
        self.complete = False

    # If the action has completed.  Flag must be set by the provided run function.
    def complete():
        return self.complete

    # Resets the action complete flag.
    def setReady():
        self.complete = True
