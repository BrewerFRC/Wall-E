def update():
    for a in actions:
        if a.isRunning():
            a.update()
    time++

class Action:
    
    def __init__(self):
