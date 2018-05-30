import time

emotions = {}
class Emotion:
    def __init__(self, time=None, trigger=None):
        self.actions = []
        self.runtime = []

    def addAction(self, action):
        self.actions.append(action)

    def run(self):
        global time
        self.runtime = []
        self.startTime = time.time()
        for a in self.actions:
            runtime.append(a)

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

    def isRunning(self):
        return len(self.runtime > 0)
    def complete(self):
        return not isRunning()
    def setReady():
        pass
