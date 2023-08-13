class PointData:
    def __init__(self, point_id, frame, x, y, state):
        self.point_id = point_id
        self.frame = frame
        self.x = x
        self.y = y
        self.state = state
        self.photo = None
        self.points_by_frame = {frame: (x, y, state)}

    def add_frame_point(self, frame, x, y, state):
        self.points_by_frame[frame] = (x, y, state)
