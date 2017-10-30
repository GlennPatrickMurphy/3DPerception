# 3DPerception

## Problem Definition

   Perception is an essential element of robotics. Sensing the environment is important for robotic decision making. The 3D Perception Problem for the 3rd Udacity project, challenged our robots to sense the a variety of object in a tabletop scenery.
   
## Exercises 1, 2 & 3

   Using RGB-D Cameras, a hybrid sensor, point clouds of the tabletop scenery were established. To highlight the important section, that being the objects on the table top, different filtering techniques (Voxel,Pass Through & RANSAC) were applied to the point clouds. Objects were segmented through a Euclidean clustering algorithm 

### Euclidean Clustering
![Euclidean Clustering](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/EuclideanClustering.PNG)

and then recognized through an SVM image classifier.

## Perception Project

Using  a linear svm classifier, and  setting the training set sample size in capturefeatures.py to 40, I was able to get an 86% accurate classifier

### SVM Accuracy
![Train_SvmAccuracy](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/Train_SvmAccuracy.PNG)

These confusion matrix show a better visualization of the classifier. The left axis was the sample and right was what the svm classifier predicted. 

### Confusion Matrix 
![ConfusionMatrix](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/ConfusionMatrix.PNG)

### Normalized Confusion Matrix 
![NormalizedConfusionMatrix](https://github.com/GlennPatrickMurphy/3DPerception/blob/master/Photos/NormalizedConfusionMatrix.PNG)

## Main Pipeline

   The code first filters the point cloud data from the RGBD camera.  Unlike in the exercises,  the point cloud contained a level of noize that an outlier filter had to be applied. To reduce the appoint of points, a Voxel Grid Downsampling was applied. To focus on the specific object on the table a Pass Through Filter was applied. To remove the rest of the table, it was modeled as a plane and removed via RANSAC. The extracted outlier, being the objects on the table top where than clustered via Euclidean Clustering. These extracted outlier and inlier (being the table) point cloud were published ROS messages, as well as the new Euclidean Cluster Cloud. 

   The code then begins to take this point cloud information and predict the objects using the already trained svm. A histogram of the clusters are created. The is catagorizing the HSV (Hue,Satruation, Value) of the cluster. HSV was selected as it is more robust with regards to different lighting situations. The histograms look at the color of the cluster and the distrubtion of surface normals to discover the shape of the object. With this information the SVM classifier makes its preditcion and publishes the ROS message.

Below are screen shots of code working in RViz with the identifiers and accuracy of the SVM predicitons.

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