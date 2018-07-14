import time

emotions = {}
class Emotion:
    def __init__(self, time=None, trigger=None):
        self.actions = []
        self.runtime = []
        self.time = time
        self.trigger = trigger

    # Adds an action to this emotion
    def addAction(self, action):
        self.actions.append(action)

    # Populates the emotion runtime, enables update process.
    def run(self):
        if complete():
            global time
            self.runtime = []
            self.startTime = time.time()
            for a in self.actions:
                runtime.append(a)

    # Handles action progression and completion.  Should be run on each main loop.
    def update(self):
        global time
        if self.isRunning():
            for a in self.runtime:
                if a.time:
                    if time.time() >= a.time:
                        a.run()
                elif a.trigger:
                    if a.trigger.complete():
                        a.run()
                else:
                    a.run()

                if a.complete():
                    a.reset()
                    self.runtime.remove(a)

    # If the emotion still has unexecuted actions during this run.
    def isRunning(self):
        return len(self.runtime > 0)
    # If the emotion has no remaining unexecuted actions.
    def complete(self):
        return not self.isRunning()
    # Dummy method to enable emotion-action ambiguity.
    def reset():
        pass
