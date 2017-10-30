# 3DPerception

## Problem Definition

   Perception is an essential element of robotics. Sensing the environment is important for robotic decision making. The 3D Perception Problem for the 3rd Udacity project, challenged our robots to sense the a variety of object in a tabletop scenery.
   
## Exercises 1, 2 & 3

   Using RGB-D Cameras, a hybrid sensor, point clouds of the tabletop scenery were established. To highlight the important section, that being the objects on the table top, different filtering techniques (Voxel,Pass Through & RANSAC) were applied to the point clouds. Objects were segmented through a Euclidean clustering algorithm 

### Euclidean Clustering
![Euclidean Clustering](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/EuclideanClustering.PNG)

and then recognized through an SVM image classifier.

## Perception Project

Below are screen shots of RViz with the identifiers.

### Test World 1 100%Correctly Identified
![Test World 1](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld1.PNG)

### Test World 2 80% Correctly Identified
![Test World 2](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld2Front2.PNG)

### Test World 2 Side View
![Test World 2 Sive View](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld2-2.PNG)

### Test World 3 75% Correctly Identified
![Test World 3](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld3Front2.PNG)

### Test World 3 Side View
![Test World 3 Side View](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/FinalProjectWorld3-2.PNG) 



A problem that I had was choosing  a minimal cluster size for the Euclidean Clustering Algorithm. I found that in order to correctly recognize smaller objects I needed to pick a smaller sample size, however than the left output box would be recognized another object and then classified. With more time I could filter out that section of the point cloud, to avoid it being inncorrectly classified.