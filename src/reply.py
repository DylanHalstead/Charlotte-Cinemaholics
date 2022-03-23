class Reply:

    def __init__(self, user, parent, text, points, time) -> None:
        self.user = user #user object that created reply
        self.parent = parent #parent post 
        self.text = text #text of the reply
        self.points = points #updoots and whatnots
        self.time = time