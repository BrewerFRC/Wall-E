
emotions = {}
time = 0

def update():
    for e in emotions:
        if e.isRunning():
            e.update()
    time++

class Emotion:
    def __init__(self):
        self.actions = []
        self.runtime = []

    def addAction(self, action):
        self.actions.append(action)

    def run(self):
        global time
        self.runtime = []
        self.startTime = time
        for a in self.actions:
            runtime.append(a)

    def update(self):
        global time
        if len(self.runtime) > 0:
            for a in self.runtime:
                if a.ready():
                    if a.time:
                        pass
                    elif a.trigger:
                        pass
                    else:
                        a.run()
                if a.complete():
                    a.setReady()

    def isRunning(self):
        return len(self.runtime > 0)
    def complete(self):
        return not isRunning()
