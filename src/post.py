class Post:

    def __init__(self, user, text, points, replies, time) -> None:
        self.user = user #user object that created reply
        self.text = text #text of the reply
        self.points = points #updoots and whatnot
        self.replies = replies #list of all replies to the post
        self.time = time #time that post was posted (prob in EST)