# 3DPerception
## Problem Definition
   Perception is an essential element of robotics. Sensing the environment is important for robotic decision making. The 3D Perception Problem for the 3rd Udacity project, challenged our robots to sense the a variety of object in a tabletop scenery.
## Exercises 1, 2 & 3
Using RGB-D Cameras, a hybrid sensor, point clouds of the tabletop scenery were established. To highlight the important section, that being the objects on the table top, different filtering techniques (Voxel,Pass Through & RANSAC) were applied to the point clouds. Objects were segmented through a Euclidean clustering algorithm 
![Euclidean Clustering](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/EuclideanClustering.PNG)
and then recognized through an SVM image classifier.
## Perception Project
![Test World 1](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld1.PNG)
![Test World 2](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld2Front.PNG)
![Test World 2 Sive View](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld2.PNG)
![Test World 3](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld3Front.PNG)
![Test World 3 Side View](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld3.PNG)