import numpy as np
import torch
import os
from tqdm import tqdm
import json

import argparse

scenes = os.listdir("./hm3d_LSeg_3d_feature_black/single_room")

color_list = np.array([[1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1], [0,0,0], [1,1,1], [0.5,0,0], [0,0.5,0], [0,0,0.5], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [1, 0.5, 0], [1, 0, 0.5], [0, 1, 0.5], [0, 0.5, 1], [1, 0, 0.5], [0.5, 0, 1], [0.25, 0, 0], [0, 0, 0.25], [0, 0.25, 0], [0.25, 0.25, 0], [0, 0.25, 0.25], [0.25, 0, 0.25], [0.5, 0.25, 0], [0.25, 0.5, 0], [0, 0.25, 0.5], [0, 0.5, 0.25], [0.25, 0, 0.5], [0.5, 0, 0.25], [1, 0.25, 0], [1, 0, 0.25], [0, 1, 0.25], [0, 0.25, 1], [0.25, 0, 1], [1, 0, 0.25]])

#scenes = sorted([os.path.join("logs_sample_single", "custom", file) for file in os.listdir("logs_sample_single/custom")] + [os.path.join("logs_sample_single2", "custom", file) for file in os.listdir("logs_sample_single2/custom")] + [os.path.join("logs_sample_two", "custom", file) for file in os.listdir("logs_sample_two/custom")] + [os.path.join("logs_sample_three", "custom", file) for file in os.listdir("logs_sample_three/custom")] + [os.path.join("logs_whole", "custom", file) for file in os.listdir("logs_whole/custom")])

parser = argparse.ArgumentParser(description='holy shit')
parser.add_argument('--job', default=0, type=int)
args = parser.parse_args()

jobs = 50
ids = (len(scenes) - 1) // jobs + 1
print(args, args.job*ids, min(len(scenes),args.job*ids+ids))

for scene_id in tqdm(scenes[args.job*ids:min(len(scenes),args.job*ids+ids)]):
    #if scene_id == ""
#for scene_id in tqdm(scenes):   
#    if scene_id.replace("_nps.npz", ".ply") in os.listdir("./all_plys2_after_bbox"):
#        print (scene_id)
#        continue
    new_concepts = []
    #room_id = scene_id.split("_")[0]
    #room_id1 = scene_id.split("_")[0] + "_" + scene_id.split("_")[1]
    #room_id2 = scene_id.split("_")[0] + "_" + scene_id.split("_")[2]
    #room_id3 = scene_id.split("_")[0] + "_" + scene_id.split("_")[3]
    print (scene_id)
    try:


        concepts = np.load(os.path.join("all_language_after_bbox", scene_id.replace("_nps.npz", ".npy")))
        #concepts = []; files = []
        #for file in os.listdir("per_room_language"):
        #    if file.startswith(room_id):
        #        concepts.append(np.load(os.path.join("per_room_language", file))); files.append(file)
        #concepts = np.concatenate(concepts)
        # concepts1 = np.load(os.path.join("per_room_language", room_id1+".npy")); concepts2 = np.load(os.path.join("per_room_language", room_id2+".npy")); concepts3 = np.load(os.path.join("per_room_language", room_id3+".npy")); concepts=np.concatenate((concepts1, concepts2, concepts3))
    except:
        print ("bad")
        continue
    language = torch.tensor(concepts).cuda()
    concepts = [];
    try:
       # for file in files:
        concepts = json.load(open(os.path.join("single_room_concepts3_after_bboxes_after_replace", scene_id.replace("_nps.npz", ".json"))));
        concepts += ['ceiling', 'floor', 'wall']
    except:
        continue
    #concepts1 = json.load(open(os.path.join("per_room_concepts", room_id1+".json"))); concepts2 = json.load(open(os.path.join("per_room_concepts", room_id2+".json"))); concepts3 = json.load(open(os.path.join("per_room_concepts", room_id3+".json"))); concepts=concepts1+concepts2+concepts3
    #if len(concepts) == 0:

    #    continue
    #print (concepts)

    try:


        concepts = np.load(os.path.join("all_language_after_bbox", scene_id.replace("_nps.npz", ".npy")))
        #concepts = []; files = []
        #for file in os.listdir("per_room_language"):
        #    if file.startswith(room_id):
        #        concepts.append(np.load(os.path.join("per_room_language", file))); files.append(file)
        #concepts = np.concatenate(concepts)
        # concepts1 = np.load(os.path.join("per_room_language", room_id1+".npy")); concepts2 = np.load(os.path.join("per_room_language", room_id2+".npy")); concepts3 = np.load(os.path.join("per_room_language", room_id3+".npy")); concepts=np.concatenate((concepts1, concepts2, concepts3))
    except:
        print ("bad")
        continue
    language = torch.tensor(concepts).cuda()
    concepts = [];
    try:
       # for file in files:
        concepts = json.load(open(os.path.join("single_room_concepts3_after_bboxes_after_replace", scene_id.replace("_nps.npz", ".json"))));
        concepts += ['ceiling', 'floor', 'wall']
    except:
        continue
    #concepts1 = json.load(open(os.path.join("per_room_concepts", room_id1+".json"))); concepts2 = json.load(open(os.path.join("per_room_concepts", room_id2+".json"))); concepts3 = json.load(open(os.path.join("per_room_concepts", room_id3+".json"))); concepts=concepts1+concepts2+concepts3
    #if len(concepts) == 0:

    #    continue
    #print (concepts)

    try:

        data = np.load(os.path.join("./hm3d_LSeg_3d_feature_black/single_room", scene_id))
        if 'rgb' in data:
            print ('rgb')
            continue
        features = data['features']
        alpha = data['alpha']
    except:
        print ("bad")
        continue
    xyz_min = np.array([0,0,0])
    xyz_max = np.array(alpha.shape)

    xyz = np.stack((alpha > 0.5).nonzero(), -1)
    points = xyz / alpha.shape * (xyz_max - xyz_min) + xyz_min

    alpha =  torch.tensor(alpha).resize((240*240*240))

    b_size = 200000
    top = 0

    features = features.reshape((-1, 512))
    all_features = torch.zeros((features.shape[0], len(concepts)))

    while top < features.shape[0]:
        features2 = torch.tensor(features[top:top+b_size]).cuda()
        features2 = features2 / features2.norm(dim=-1, keepdim=True)
        features2 = features2 @ language.t()

        all_features[top:top+b_size] = features2.cpu()
        top += b_size

    scores = np.argmax(all_features, -1)
    colors = color_list[scores]

    points2 = []
    for point, color in zip(points, colors):
        points2.append("%f %f %f %d %d %d\n"%(point[0], point[1], point[2], int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    #points = np.concatenate((points, colors), axis=-1)
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(points2)
    # pcd.colors = o3d.utility.Vector3dVector(colors)

    # o3d.io.write_point_cloud(os.path.join("./all_plys", scene_id.replace(".json", ".ply")), pcd)
    np.save(os.path.join("all_scores_after_bbox_black", scene_id.replace("_nps.npz", ".npy")), scores)
    file = open(os.path.join("./all_plys2_after_bbox_black", scene_id.replace("_nps.npz", ".ply")),"w")
    file.write('''ply
    format ascii 1.0
    element vertex %d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    %s
    '''%(len(points2),"".join(points2)))
    file.close()

    for j in range(language.shape[0]):
        #print (torch.sum(scores==j))
        if torch.sum(scores == j):
            new_concepts.append(concepts[j])

    with open("./new_concepts2_after_bbox_black/%s"%scene_id.replace("_nps.npz", ".json"), "w") as f:
        json.dump(new_concepts, f)
