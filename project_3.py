#!/usr/bin/env python

# Import modules
import numpy as np
import sklearn
from sklearn.preprocessing import LabelEncoder
import pickle
from sensor_stick.srv import GetNormals
from sensor_stick.features import compute_color_histograms
from sensor_stick.features import compute_normal_histograms
from visualization_msgs.msg import Marker
from sensor_stick.marker_tools import *
from sensor_stick.msg import DetectedObjectsArray
from sensor_stick.msg import DetectedObject
from sensor_stick.pcl_helper import *

import rospy
import tf
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import String
from pr2_robot.srv import *
from rospy_message_converter import message_converter
import yaml


# Helper function to get surface normals
def get_normals(cloud):
    get_normals_prox = rospy.ServiceProxy('/feature_extractor/get_normals', GetNormals)
    return get_normals_prox(cloud).cluster

# Helper function to create a yaml friendly dictionary from ROS messages
def make_yaml_dict(test_scene_num, arm_name, object_name, pick_pose, place_pose):
    yaml_dict = {}
    yaml_dict["test_scene_num"] = test_scene_num.data
    yaml_dict["arm_name"]  = arm_name.data
    yaml_dict["object_name"] = object_name.data
    yaml_dict["pick_pose"] = message_converter.convert_ros_message_to_dictionary(pick_pose)
    yaml_dict["place_pose"] = message_converter.convert_ros_message_to_dictionary(place_pose)
    return yaml_dict

# Helper function to output to yaml file
def send_to_yaml(yaml_filename, dict_list):
    data_dict = {"object_list": dict_list}
    with open(yaml_filename, 'w') as outfile:
        yaml.dump(data_dict, outfile, default_flow_style=False)

# Callback function for your Point Cloud Subscriber
def pcl_callback(pcl_msg):

# Exercise-2 TODOs:

    # TODO: Convert ROS msg to PCL data
    cloud =ros_to_pcl(pcl_msg) #ros_cloud(PointCloud2) 
   
    # TODO: Statistical Outlier Filtering

    # Much like the previous filters, we start by creating a filter object: 
    outlier_filter = cloud.make_statistical_outlier_filter()

    # Set the number of neighboring points to analyze for any given point
    outlier_filter.set_mean_k(200)

    # Set threshold scale factor
    x = 2

    # Any point with a mean distance larger than global (mean distance+x*std_dev) will be considered outlier
    outlier_filter.set_std_dev_mul_thresh(x)

    # Finally call the filter function for magic
    cloud = outlier_filter.filter()

    # TODO: Voxel Grid Downsampling
    # Create a VoxelGrid filter object for our input point cloud
    vox = cloud.make_voxel_grid_filter()

    # Choose a voxel (also known as leaf) size
    LEAF_SIZE = .01

    # Set the voxel (or leaf) size  
    vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

    # Call the filter function to obtain the resultant downsampled point cloud
    cloud_filtered = vox.filter()

    # TODO: PassThrough Filter
    passthrough = cloud_filtered.make_passthrough_filter()

    # Assign axis and range to the passthrough filter object.
    filter_axis = 'z'
    passthrough.set_filter_field_name(filter_axis)
    axis_min = 0.60
    axis_max = 2.
    passthrough.set_filter_limits(axis_min, axis_max)

    # Finally use the filter function to obtain the resultant point cloud. 
    cloud_filtered = passthrough.filter()

    # TODO: RANSAC Plane Segmentation
    # Create the segmentation object
    seg = cloud_filtered.make_segmenter()

    # Set the model you wish to fit 
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)
    max_distance = 0.01
    seg.set_distance_threshold(max_distance)

    # Call the segment function to obtain set of inlier indices and model coefficients
    inliers, coefficients = seg.segment()

    # TODO: Extract inliers and outliers

    extracted_inliers = cloud_filtered.extract(inliers, negative=False)
    extracted_outliers = cloud_filtered.extract(inliers, negative=True)

    # TODO: Euclidean Clustering

  # Euclidean Clustering
    white_cloud = XYZRGB_to_XYZ(extracted_outliers)# Apply function to convert XYZRGB to XYZ
    tree = white_cloud.make_kdtree()
    # Create a cluster extraction object
    ec = white_cloud.make_EuclideanClusterExtraction()
    # Set tolerances for distance threshold 
    # as well as minimum and maximum cluster size (in points)
    # NOTE: These are poor choices of clustering parameters
    # Your task is to experiment and find values that work for segmenting objects.
    ec.set_ClusterTolerance(0.02)
    ec.set_MinClusterSize(120)
    ec.set_MaxClusterSize(5000)
    # Search the k-d tree for clusters
    ec.set_SearchMethod(tree)
    # Extract indices for each of the discovered clusters
    cluster_indices = ec.Extract()

    # TODO: Create Cluster-Mask Point Cloud to visualize each cluster separately
    
    #Assign a color corresponding to each segmented object in scene
    cluster_color = get_color_list(len(cluster_indices))

    color_cluster_point_list = []

    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([white_cloud[indice][0],
                                        white_cloud[indice][1],
                                        white_cloud[indice][2],
                                         rgb_to_float(cluster_color[j])])

    #Create new cloud containing all clusters, each with unique color
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)
    ros_cluster_cloud = pcl_to_ros(cluster_cloud)

    # TODO: Convert PCL data to ROS messages
    
    ros_cloud_objects = pcl_to_ros(extracted_outliers)
    ros_cloud_table = pcl_to_ros(extracted_inliers)

    # TODO: Publish ROS messages
    pcl_objects_pub.publish(ros_cloud_objects)
    pcl_table_pub.publish(ros_cloud_table)
    pcl_cluster_pub.publish(ros_cluster_cloud)

# Exercise-3 TODOs: 

    # Classify the clusters! (loop through each detected cluster one at a time)
    detected_objects_labels = []
    detected_objects = []

    for index, pts_list in enumerate(cluster_indices):
        # Grab the points for the cluster from the extracted outliers (cloud_objects)
        pcl_cluster = extracted_outliers.extract(pts_list)
        # TODO: convert the cluster from pcl to ROS using helper function
	ros_cluster=pcl_to_ros(pcl_cluster)
        # Extract histogram features
        # TODO: complete this step just as is covered in capture_features.py
        chists = compute_color_histograms(ros_cluster, using_hsv=True)
        normals = get_normals(ros_cluster)
        nhists = compute_normal_histograms(normals)
        feature = np.concatenate((chists, nhists))
        # Make the prediction, retrieve the label for the result
        # and add it to detected_objects_labels list
        prediction = clf.predict(scaler.transform(feature.reshape(1,-1)))
        label = encoder.inverse_transform(prediction)[0]
        detected_objects_labels.append(label)

        # Publish a label into RViz
        label_pos = list(white_cloud[pts_list[0]])
        label_pos[2] += .4
        object_markers_pub.publish(make_label(label,label_pos, index))

        # Add the detected object to the list of detected objects.
        do = DetectedObject()
        do.label = label
        do.cloud = ros_cluster
        detected_objects.append(do)

    rospy.loginfo('Detected {} objects: {}'.format(len(detected_objects_labels), detected_objects_labels))

    # Publish the list of detected objects
    # This is the output you'll need to complete the upcoming project!
    detected_objects_pub.publish(detected_objects)

    # Suggested location for where to invoke your pr2_mover() function within pcl_callback()
    # Could add some logic to determine whether or not your object detections are robust
    # before calling pr2_mover()
    try:
        pr2_mover(detected_objects)
    except rospy.ROSInterruptException:
        pass

# function to load parameters and request PickPlace service
def pr2_mover(object_list):
   
    # TODO: Initialize variables
    dict_list=[]
    # TODO: Get/Read parameters
    object_list_param = rospy.get_param('/object_list')
    dropboxes = rospy.get_param('/dropbox')

    # TODO: Parse parameters into individual variables
    object_group = {}
    for object_param in object_list_param:
	object_group[object_param['name']] = object_param['group']

    dropbox_group = {}
    for dropbox in dropboxes:
	dropbox_group[dropbox['group']] = dropbox
	
    # TODO: Rotate PR2 in place to capture side tables for the collision map

    # TODO: Loop through the pick list
    labels = []
    centroids = [] # to be list of tuples (x, y, z)
    for object in object_list:
    	points_arr = ros_to_pcl(object.cloud).to_array()
    	centroid=np.mean(points_arr, axis=0)[:3]
	pick_pose=Pose()
	pick_pose.position.x = float(centroid[0])
        pick_pose.position.y = float(centroid[1])
	pick_pose.position.z = float(centroid[2])

	place_pose = Pose()
        place_position = dropbox_group.get(object_group.get(object.label, 'unknown'), {}).get('position', [0, 0, 0])
        place_pose.position.x = place_position[0]
        place_pose.position.y = place_position[1]
	place_pose.position.z = place_position[2]

	object_name = String()
	object_name.data = str(object.label)

        test_scene_num = Int32()
        test_scene_num.data = 1

        arm_name = String()
        arm_name.data = dropbox_group.get(object_group.get(object.label, 'unknown'), {}).get('name', 'unknown')


        # TODO: Get the PointCloud for a given object and obtain it's centroid

        # TODO: Create 'place_pose' for the object

        # TODO: Assign the arm to be used for pick_place

        # TODO: Create a list of dictionaries (made with make_yaml_dict()) for later output to yaml format
        action = make_yaml_dict(test_scene_num, object_name, arm_name, pick_pose, place_pose)
	dict_list.append(action)
        # Wait for 'pick_place_routine' service to come up
        rospy.wait_for_service('pick_place_routine')

        try:
            pick_place_routine = rospy.ServiceProxy('pick_place_routine', PickPlace)
	    if False:
            	#TODO: Insert your message variables to be sent as a service request
            	resp = pick_place_routine(test_scene_num, object_name, arm_name, pick_pose, place_pose)

            	print ("Response: ",resp.success)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    # TODO: Output your request parameters into output yaml file
    
    send_to_yaml("./output1.yaml", dict_list)

if __name__ == '__main__':

    # TODO: ROS node initialization
    rospy.init_node('clustering',anonymous=True)

    # TODO: Create Subscribers
    pcl_sub=rospy.Subscriber("/pr2/world/points",pc2.PointCloud2,pcl_callback,queue_size=1)

    # TODO: Create Publishers
    pcl_objects_pub = rospy.Publisher("/pcl_objects", PointCloud2, queue_size=1)
    pcl_table_pub = rospy.Publisher("/pcl_table", PointCloud2, queue_size=1)
    pcl_cluster_pub = rospy.Publisher("/pcl_cluster", PointCloud2, queue_size=1)
    # Call them object_markers_pub and detected_objects_pub
    # Have them publish to "/object_markers" and "/detected_objects" with 
    # Message Types "Marker" and "DetectedObjectsArray" , respectively
    object_markers_pub=rospy.Publisher("/object_markers",Marker,queue_size=1)
    detected_objects_pub=rospy.Publisher("/detected_objects",DetectedObjectsArray,queue_size=1)
    # Load Model From disk
    model = pickle.load(open('model.sav', 'rb'))
    clf = model['classifier']
    encoder = LabelEncoder()
    encoder.classes_ = model['classes']
    scaler = model['scaler']

    # Initialize color_list
    get_color_list.color_list = []

    # TODO: Spin while node is not shutdown
    while not rospy.is_shutdown():
    	rospy.spin()
