**Racing car with AI**

Racing is one of the most popular simple 2D games in the world. This work is designed to check whether an agent with artificial intelligence can master this interesting game.

**Creating a gaming environment**

Before I started building the AI ​​for my race, I had to create a learning environment, the game itself.
In the game, I decided to implement all the basic mechanics of racing, such as inertia, acceleration, braking, wheel friction, drifting and car drifting when turning, by creating my own small engine.

I also created a map that consists of a background and lines that limit the track where the car can be and when crossing which the game starts over. 
The goal of the player is to drive the entire distance from start to finish.
The machine is controlled using keys.

![image](https://github.com/romanpro23/RacesAI/assets/87851373/05fb8dd0-2bc3-4143-bd20-0f98d748ac9d)


**Screwing the AI ​​to the car**

I was faced with the task of which optimization method to choose for the agent. I decided to use DQN, briefly about it: 
> Deep Q-Network (DQN) is a powerful algorithm in the field of reinforcement learning. 
> It combines the principles of deep neural networks with Q-learning, enabling agents to learn optimal policies in complex environments.


For effective training, I decided to add temporary reward lines to help the agent understand in which direction it should move. 
The agent sees the environment, which consists of lines with the help of lasers.
It looks like this:

![image](https://github.com/romanpro23/RacesAI/assets/87851373/cdc36330-866c-4fbf-964a-eac4dddd5bdc)

To be more precise, the agent sees the points of intersection of its lasers with the lines that limit the distance, and the input of the neural network is given how far this point is relative to the length of the entire laser. 
The way the machine sees the environment is clearly demonstrated below:

![image](https://github.com/romanpro23/RacesAI/assets/87851373/4d9fc195-c0d8-485a-9bd2-c38e4cd92b42)
![image](https://github.com/romanpro23/RacesAI/assets/87851373/f4fefc60-f5bd-42c5-ac8e-fa9d053cfd89)

**Results**

After starting the training, you can see that our agent, knowing nothing from the beginning, quickly begins to learn and later achieves very good results, easily overcoming the given track. 
You can try to configure the car by changing its parameters in the designer and see how it will learn on your configuration.

The designer of the car and the fields that can be set
'''
def __init__(self,
                 height,
                 width,
                 acceleration=0.05,
                 max_speed=5,
                 maneuverability=3,
                 grip=0.005,
                 brakes=1.5,
                 handbrakes=0.95,
                 back_speed=0.25,
                 drift_control=0.5,
                 color=(255, 0, 0),
                 speed_gearbox=(0.2, 0.4, 0.6, 0.8, 1),
                 length_sensor=50,
                 x=384,
                 y=300):
'''

**Just try it!**


