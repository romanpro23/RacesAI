import json

from function import Line


class Generator:
    start_point: tuple
    frames: list
    rewards: list
    finish: Line

    width: int
    height: int

    def __init__(self, path, width=1024, height=768):
        with open(path, 'r') as file:
            data = json.load(file)

        start_point = data["start"]
        frames_side = data["frames_side"]
        frames_inside = data["frames_inside"]
        rewards = data["reward_lines"]
        finish = data["finish_line"]

        self.width = width
        self.height = height

        self.start_point = (start_point[0], height - start_point[1])

        self.frames = []

        self.__add_frames(frames_inside)
        self.__add_frames(frames_side)

        self.rewards = []
        self.__add_rewards(rewards)

        self.finish = Line((finish[0], self.height - finish[1]), (finish[2], self.height - finish[3]))

    def __add_frames(self, frames):
        for index in range(len(frames)):
            if index < len(frames) - 1:
                self.frames.append(Line((frames[index][0], self.height - frames[index][1]),
                                        (frames[index + 1][0], self.height - frames[index + 1][1])
                                        ))
            else:
                self.frames.append(Line((frames[index][0], self.height - frames[index][1]),
                                        (frames[0][0], self.height - frames[0][1])
                                        ))

    def __add_rewards(self, rewards):
        for reward in rewards:
            self.rewards.append(Line((reward[0], self.height - reward[1]),
                                     (reward[2], self.height - reward[3])))
