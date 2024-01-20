import json
import numpy as np
import os
from collections import defaultdict
from tqdm import tqdm
from plyfile import PlyData, PlyElement
import math

scenes = os.listdir("new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis")

def inside_p(v, box2):
    #print(v, box2)
    if v[0] < box2[0][0] or v[0] > box2[1][0]: return False
    if v[1] < box2[0][1] or v[1] > box2[1][1]: return False
    if v[2] < box2[0][2] or v[2] > box2[1][2]: return False
    return True

def useful_f(fac):
    fvs = fac['vertex_indices']
    for _ in range(4):
        if fvs[_] not in ver_map.keys(): return False
    return True

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return v1_u, v2_u, np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def boxes_distance(A_min, A_max, B_min, B_max):
    delta1 = A_min - B_max
    delta2 = B_min - A_max
    u = np.max(np.array([np.zeros(len(delta1)), delta1]), axis=0)
    v = np.max(np.array([np.zeros(len(delta2)), delta2]), axis=0)
    dist = np.linalg.norm(np.concatenate([u, v]))
    return dist

for scene_id in tqdm(scenes):
    
    # if scene_id in os.listdir("new_per_room_relationships"):
    #     continue

    # jsn_file = './new_single_room_bboxes2/%s'%scene_id
    # jsn_file = './per_room_bboxes_/%s'%scene_id
    jsn_file = 'new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis/%s'%scene_id
    # if not ("00820" in scene_id and "_2" in scene_id): continue

    objs = json.load(open(jsn_file))

    all_relationships = defaultdict(list)

    for (j,obj) in enumerate(objs):

        for (k,obj2) in enumerate(objs):
            if j == k: continue

            if obj['class_name'] == obj2['class_name']: continue

            rel = []

            if (obj['bbox'][0][2] - obj2['bbox'][1][2]) < 0.075 and (obj['bbox'][0][2] - obj2['bbox'][1][2]) > -0.075 and obj['bbox'][0][0] > obj2['bbox'][0][0] -0.05 and obj['bbox'][1][0] < obj2['bbox'][1][0] + 0.05 and obj['bbox'][0][1] > obj2['bbox'][0][1] - 0.05 and obj['bbox'][1][1] < obj2['bbox'][1][1] + 0.05:
                rel.append('top')

            elif obj['bbox'][0][2] > obj2['bbox'][0][2] and obj['bbox'][1][2] > obj2['bbox'][1][2] and min(abs(obj['bbox'][0][0] - obj2['bbox'][0][0]), abs(obj['bbox'][1][0] - obj2['bbox'][1][0]), abs(obj['bbox'][1][0] - obj2['bbox'][0][0]), abs(obj['bbox'][0][0] - obj2['bbox'][1][0])) < 0.5  and min(abs(obj['bbox'][0][1] - obj2['bbox'][0][1]), abs(obj['bbox'][1][1] - obj2['bbox'][1][1]), abs(obj['bbox'][1][1] - obj2['bbox'][0][1]), abs(obj['bbox'][0][1] - obj2['bbox'][1][1])) < 0.5:             
                rel.append('above')

            elif obj['bbox'][0][2] < obj2['bbox'][0][2] and obj['bbox'][1][2] < obj2['bbox'][1][2]  and min(abs(obj['bbox'][0][0] - obj2['bbox'][0][0]), abs(obj['bbox'][1][0] - obj2['bbox'][1][0]), abs(obj['bbox'][1][0] - obj2['bbox'][0][0]), abs(obj['bbox'][0][0] - obj2['bbox'][1][0])) < 0.5  and min(abs(obj['bbox'][0][1] - obj2['bbox'][0][1]), abs(obj['bbox'][1][1] - obj2['bbox'][1][1]), abs(obj['bbox'][1][1] - obj2['bbox'][0][1]), abs(obj['bbox'][0][1] - obj2['bbox'][1][1])) < 0.5:
                
                rel.append('below')

            elif obj['bbox'][0][0] > obj2['bbox'][0][0] and obj['bbox'][1][0] < obj2['bbox'][1][0] and obj['bbox'][0][1] > obj2['bbox'][0][1] and obj['bbox'][1][1] < obj2['bbox'][1][1] and obj['bbox'][0][2] > obj2['bbox'][0][2] and obj['bbox'][1][2] < obj2['bbox'][1][2]:
                rel.append('inside')
            

            if rel != 'inside' and rel != 'top':
                if obj['class_name'] == obj2['class_name']: continue

                if boxes_distance(np.array(obj2['bbox'][0][:2]), np.array(obj2['bbox'][1][:2]), np.array(obj['bbox'][0][:2]), np.array(obj['bbox'][1][:2])) < 0.5:
                    
                    rel.append('close')

                # size1 = obj["sizes"][0] * obj["sizes"][1] * obj["sizes"][2] 
                # size2 = obj2["sizes"][0] * obj2["sizes"][1] * obj2["sizes"][2] 

                # if size1 > size2 and size1 / 2 < size2:
                #     rel.append('larger')

                # if size2 > size1 and size2 / 2 < size1:
                #     rel.append('smaller')

            if len(rel):
                for r in rel:
                    all_relationships[r].append((obj['id'], obj2['id']))
        
            # if rel == 'close':
            #     ver_map = dict()
            #     ply_vertex = []
            #     NNV = 0

            #     for ii, v in enumerate(plydata['vertex']):
            #         if inside_p(v, obj['bbox']) or inside_p(v, obj2['bbox']):
            #             ply_vertex.append(v)
            #             ver_map[ii] = NNV
            #             NNV += 1

            #     ply_vertex = np.array(
            #             ply_vertex, 
            #             dtype=[('x','f4'),('y','f4'),('z','f4'),('nx','f4'),('ny','f4'),('nz','f4'),('red','u1'),('green','u1'),('blue','u1')]
            #         )

            #     ply_face = [f for f in plydata['face'] if useful_f(f)]
                
            #     nply_face = []
            #     for ii,_ in enumerate(ply_face):
            #         dat = []
            #         #print(ply_face[i]['vertex_indices'])
            #         for j in range(4):
            #             vid = ply_face[ii]['vertex_indices'][j]
            #             dat.append(ver_map[vid])
            #         dat = ((dat[0],dat[1],dat[2],dat[3]),ply_face[ii]['object_id'])

            #         nply_face.append(dat)
            #     ply_face = np.array(nply_face, dtype=ply_face[0].dtype)

            #     ply = PlyData([
            #         PlyElement.describe(ply_vertex, 'vertex'),
            #         PlyElement.describe(ply_face, 'face')
            #     ], text=True)

            #     ply.write('%s/boxes/%s_%s_%s.ply'%(scene_id, rel, obj['class_name'], obj2['class_name']))

    for (j,obj) in enumerate(objs):
        for (k,obj2) in enumerate(objs):
            for (l, obj3) in enumerate(objs):
                
                rel = []

                if j == k or j == l or k == l or obj['class_name'] == obj2['class_name'] or obj2['class_name'] == obj3['class_name'] or obj['class_name'] == obj3['class_name']: 
                    continue  

                if (obj['id'], obj2['id']) in all_relationships['top'] or (obj['id'], obj2['id']) in all_relationships['inside'] or (obj['id'], obj3['id']) in all_relationships['top'] or (obj['id'], obj3['id']) in all_relationships['inside'] or (obj3['id'], obj2['id']) in all_relationships['top'] or (obj3['id'], obj2['id']) in all_relationships['inside']  or (obj2['id'], obj3['id']) in all_relationships['top'] or (obj2['id'], obj3['id']) in all_relationships or (obj3['id'], obj['id']) in all_relationships['top'] or (obj3['id'], obj['id']) in all_relationships['inside'] or (obj2['id'], obj['id']) in all_relationships['top'] or (obj2['id'], obj['id']) in all_relationships['inside']:
                    continue

                

                if ((obj2['bbox'][0][0] - obj['bbox'][0][0]) * (obj3['bbox'][0][0] - obj2['bbox'][0][0])) > 0 and ((obj2['bbox'][0][1] - obj['bbox'][0][1]) * (obj3['bbox'][0][1] - obj2['bbox'][0][1])) > 0 and ((obj2['bbox'][1][0] - obj['bbox'][1][0]) * (obj3['bbox'][1][0] - obj2['bbox'][1][0])) > 0 and ((obj2['bbox'][1][1] - obj['bbox'][1][1]) * (obj3['bbox'][1][1] - obj2['bbox'][1][1])) > 0:
                    
                    rel.append('between')

                rel_pos1 = np.array(obj2['bbox'][0][:2]) - np.array(obj['bbox'][0][:2])
                rel_pos2 = np.array(obj3['bbox'][0][:2]) - np.array(obj['bbox'][0][:2])

                dis1 = boxes_distance(np.array(obj2['bbox'][0][:2]), np.array(obj2['bbox'][1][:2]), np.array(obj['bbox'][0][:2]), np.array(obj['bbox'][1][:2]))
                dis2 = boxes_distance(np.array(obj3['bbox'][0][:2]), np.array(obj3['bbox'][1][:2]), np.array(obj['bbox'][0][:2]), np.array(obj['bbox'][1][:2]))
                # if np.sum(rel_pos1 ** 2) > np.sum(rel_pos2 ** 2) + 1.0:
                #     rel.append('further')

                # if np.sum(rel_pos1 ** 2) < np.sum(rel_pos2 ** 2) - 1.0:
                #     rel.append('closer')
                if dis1 > dis2 + 1.0: rel.append('further')
                if dis1 < dis2 - 1.0: rel.append('closer')


                unit_v1, unit_v2, angle = angle_between(rel_pos1, rel_pos2)

                if angle > 1.57:
                    continue

                rot_mat = np.array([[unit_v1[1], unit_v1[0]],
                            [-unit_v1[0], unit_v1[1]]])

                if not np.sum((unit_v1 @ rot_mat - np.array([0,1])) ** 2) < 0.0001:
                    continue 
                new_v2 = unit_v2 @ rot_mat

                if new_v2[0] > 0.5:
                    
                    rel.append("right")
                elif new_v2[0] < -0.5:
                    rel.append("left")

                if len(rel):
                    for r in rel:
                        all_relationships[r].append((obj['id'], obj2['id'], obj3['id']))

                # if len(rel):
                #     ver_map = dict()
                #     ply_vertex = []
                #     NNV = 0

                #     for ii, v in enumerate(plydata['vertex']):
                #         if inside_p(v, obj['bbox']) or inside_p(v, obj2['bbox']) or inside_p(v, obj3['bbox']):
                #             ply_vertex.append(v)
                #             ver_map[ii] = NNV
                #             NNV += 1

                #     ply_vertex = np.array(
                #             ply_vertex, 
                #             dtype=[('x','f4'),('y','f4'),('z','f4'),('nx','f4'),('ny','f4'),('nz','f4'),('red','u1'),('green','u1'),('blue','u1')]
                #         )

                #     ply_face = [f for f in plydata['face'] if useful_f(f)]
                    
                #     nply_face = []
                #     for ii,_ in enumerate(ply_face):
                #         dat = []
                #         #print(ply_face[i]['vertex_indices'])
                #         for j in range(4):
                #             vid = ply_face[ii]['vertex_indices'][j]
                #             dat.append(ver_map[vid])
                #         dat = ((dat[0],dat[1],dat[2],dat[3]),ply_face[ii]['object_id'])

                #         nply_face.append(dat)
                #     ply_face = np.array(nply_face, dtype=ply_face[0].dtype)

                #     ply = PlyData([
                #         PlyElement.describe(ply_vertex, 'vertex'),
                #         PlyElement.describe(ply_face, 'face')
                #     ], text=True)

                #     ply.write('%s/boxes/%s_%s_%s_%s.ply'%(scene_id, rel, obj['class_name'], obj2['class_name'], obj3['class_name']))                    

        rel_file = 'new_single_room_relationships_replace_nofilterdetected_all_concepts_replace/%s'%scene_id
        with open(rel_file, "w") as f2:
            json.dump(all_relationships, f2)           


