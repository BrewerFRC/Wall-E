import time

emotions = {}
class Emotion:
    def __init__(self, time=None, trigger=None):
        self.actions = []
        self.runtime = []

    # Adds an action to this emotion
    def addAction(self, action):
        self.actions.append(action)

    # Populates the emotion runtime, enables update process.
    def run(self):
        global time
        self.runtime = []
        self.startTime = time.time()
        for a in self.actions:
            runtime.append(a)

    # Handles action progression and completion.  Should be run on each main loop.
    def update(self):
        global time
        if len(self.runtime) > 0:
            for a in self.runtime:
                if a.ready():
                    if a.time:
                        if time.time() >= a.time:
                            a.run()
                    elif a.trigger:
                        if a.trigger.complete():
                            a.run()
                    else:
                        a.run()
                if a.complete():
                    self.runtime.remove(a)
                    a.setReady()

    # If the emotion still has unexecuted actions during this run.
    def isRunning(self):
        return len(self.runtime > 0)
    # If the emotion has no remaining unexecuted actions.
    def complete(self):
        return not isRunning()
    # Dummy method to enable emotion-action ambiguity.
    def setReady():
        pass
