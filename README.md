# The Robot Car Project
## Introduction
  In 2019, we participated in the Zhejiang University Central Control Cup Robot Design Competition, this is our code source during the game.
## Competition theme
Supermarket Robot Challenge: Create a robot and make it a supermarket organizer. During the competition, the robot will complete the “replenishment” operation of 12 specified goods within 12 minutes according to the random list of goods, starting from the “starting area” of the venue. The robot needs to obtain the goods on the platform of the warehouse and Place it in the empty cargo window of the designated shelf, and get 5 points for each correct piece of goods. If you put the wrong shelf or put it into a non-empty cargo window, you will deduct 5 points. The winner is determined based on the total score of the items that the robot correctly placed in the cargo window.
## Module Explanation
Master: the main procedure
1. Arm: The servos controlled by the Raspberry Pi
2. Car: The wheels and the infrared sensors (controlled by Mega 2560)
3. Camera: the camera used to detect objects
4. Other objects: ADTs of real world objects
