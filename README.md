# 3DPerception
## Problem Definition
   Perception is an essential element of robotics. Sensing the environment is important for robotic decision making. The 3D Perception Problem for the 3rd Udacity project, challenged our robots to sense the a variety of object in a tabletop scenery.
## Exercises 1, 2 & 3
Using RGB-D Cameras, a hybrid sensor, point clouds of the tabletop scenery were established. To highlight the important section, that being the objects on the table top, different filtering techniques (Voxel,Pass Through & RANSAC) were applied to the point clouds. Objects were segmented through a Euclidean clustering algorithm 
![Euclidean Clustering]("Photos/EuclideanClustering")
and then recognized through an SVM image classifier.
## Perception Project
![Test World 1]("Photos/FinalProjectWorld1")
![Test World 2]("Photos/FinalProjectWorld2Front")
![Test World 2 Sive View]("Photos/FinalProjectWorld2")
![Test World 3]("Photos/FinalProjectWorld3Front")
![Test World 3 Side View]("Photos/FinalProjectWorld3")