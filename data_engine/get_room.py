import os
import re
import copy
import json
import random
import numpy as np

import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

scenes = ['0']#os.listdir('.')

def get_pts(stg):
    lis = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", stg)
    return np.array(lis, dtype=float)

pre_dir = './data/scene_datasets/hm3d_semantic/'

train_scene_ids = [
    "00009-vLpv2VX547B",
    "00016-qk9eeNeR4vw",
    "00017-oEPjPNSPmzL",
    "00022-gmuS7Wgsbrx",
    "00025-ixTj1aTMup2",
    "00031-Wo6kuutE9i7",
    "00034-6imZUJGRUq4",
    "00035-3XYAD64HpDr",
    "00043-Jfyvj3xn2aJ",
    "00055-HxmXPBbFCkH",
    "00057-1UnKg1rAb8A",
    "00062-ACZZiU6BXLz",
    "00081-5biL7VEkByM",
    "00099-226REUyJh2K",
    "00105-xWvSkKiWQpC",
    "00109-GTV2Y73Sn5t",
    "00135-HeSYRw7eMtG",
    "00141-iigzG1rtanx",
    "00150-LcAd9dhvVwh",
    "00166-RaYrxWt5pR1",
    "00179-MVVzj944atG",
    "00203-VoVGtfYrpuQ",
    "00205-NEVASPhcrxR",
    "00207-FRQ75PjD278",
    "00217-qz3829g1Lzf",
    "00222-g8Xrdbe9fir",
    "00234-nACV8wLu1u5",
    "00238-j6fHrce9pHR",
    "00241-h6nwVLpAKQz",
    "00250-U3oQjwTuMX8",
    "00251-wsAYBFtQaL7",
    "00254-YMNvYDhK8mB",
    "00255-NGyoyh91xXJ",
    "00263-GGBvSFddQgs",
    "00267-gQ3xxshDiCz",
    "00294-PPTLa8SkUfo",
    "00307-vDfkYo5VqEQ",
    "00323-yHLr6bvWsVm",
    "00324-DoSbsoo4EAg",
    "00326-u9rPN5cHWBg",
    "00327-xgLmjqzoAzF",
    "00366-fxbzYAGkrtm",
    "00386-b3WpMbPFB6q",
    "00388-pcpn6mFqFCg",
    "00404-QN2dRqwd84J",
    "00410-v7DzfFFEpsD",
    "00414-77mMEyxhs44",
    "00422-8wJuSPJ9FXG",
    "00440-wPLokgvCnuk",
    "00463-URjpCob8MGw",
    "00466-xAHnY3QzFUN",
    "00475-g7hUFVNac26",
    "00476-NtnvZSMK3en",
    "00495-CQWES1bawee",
    "00506-QVAA6zecMHu",
    "00508-4vwGX7U38Ux",
    "00525-iKFn6fzyRqs",
    "00529-W9YAR9qcuvN",
    "00537-oahi4u45xMf",
    "00538-3CBBjsNkhqW",
    "00541-FnDDfrBZPhh",
    "00546-nS8T59Aw3sf",
    "00560-gjhYih4upQ9",
    "00569-YJDUB7hWg9h",
    "00582-TYDavTf8oyy",
    "00591-JptJPosx1Z6",
    "00592-CthA7sQNTPK",
    "00606-W16Bm4ysK8v",
    "00626-XiJhRLvpKpX",
    "00643-ggNAcMh8JPT",
    "00657-TSJmdttd2GV",
    "00669-DNWbUAJYsPy",
    "00680-YmWinf3mhb5",
    "00706-YHmAkqgwe2p",
    "00723-hWDDQnSDMXb",
    "00732-Z2DQddYp1fn",
    "00733-GtM3JtRvvvR",
    "00744-1S7LAXRdDqK",
    "00750-E1NrAhMoqvB",
    "00758-HfMobPm86Xn"
]

for scene_id in train_scene_ids: #os.listdir(pre_dir + 'pts'):
    #if scene_id in ['walls', 'parse.py', 'apartment_0', 'crops', 'bboxes', 'get_bbox.py', 'get_crop.py', 'frl_apartment_4', 'frl_apartment_3']: continue
    #if scene_id == 'apartment_0': continue
    #scene_id = scene_id[:-4]
    print(scene_id)
    #if '00009' not in scene_id: continue

    #if os.path.exists('./crops/{}'.format(scene_id)):
    #    os.system('rm -rf ./crops/{}'.format(scene_id))
    #os.system('mkdir ./crops/{}'.format(scene_id))

    col_file = pre_dir + 'pts/{}.txt'.format(scene_id)
    seg_file = pre_dir + '{}/{}.semantic.txt'.format(scene_id, scene_id[6:])
    if not os.path.exists(seg_file):
        seg_file = pre_dir + '{}/{}.semantic.txt'.format(scene_id, scene_id[6:])

    with open(col_file) as fi:
        col_map = fi.readlines()
    with open(seg_file) as fi:
        seg_map = fi.readlines()[1:]

    seg2col = dict()
    for item in seg_map:
        sp = 0
        while item[sp]!='\"': sp += 1
        seg2col[item[sp:-1]] = item[sp-7:sp-1]

    col2pts = dict()
    for item in col_map:
        if item[:6] not in col2pts.keys():
            col2pts[item[:6]] = [get_pts(item[7:])]
        else:
            col2pts[item[:6]].append(get_pts(item[7:]))
    for ky in col2pts.keys():
        col2pts[ky] = np.array(col2pts[ky])

    floor_verticles = None
    flag = None
    for seg in seg2col.keys():
        
        if "\"floor\"" in seg or "\"ceiling\"" in seg:
            if seg2col[seg] not in col2pts.keys(): continue
            #cur_layer_0 = col2pts[seg2col[seg]][:,0].reshape(-1)
            cur_layer_1 = col2pts[seg2col[seg]][:,1].reshape(-1)
            cur_layer_2 = col2pts[seg2col[seg]][:,2].reshape(-1)
            print(seg)
            #print(cur_layer_0.mean(), cur_layer_0.max(), cur_layer_0.min())
            print(cur_layer_1.mean(), cur_layer_1.max(), cur_layer_1.min())
            print(cur_layer_2.mean(), cur_layer_2.max(), cur_layer_2.min())
            if flag is None:
                if cur_layer_1.max()-cur_layer_1.min()<cur_layer_2.max()-cur_layer_2.min(): flag=1
                else: flag = 2
            if flag == 2:
                if cur_layer_2.max() - cur_layer_2.min() > 0.7: continue
            
                if floor_verticles is None:
                    floor_verticles = [cur_layer_2.min()] * 50 + [cur_layer_2.max()] * 50 #cur_layer
                else:
                # print(floor_verticles.shape)
                # print(col2pts[seg2col[seg]].shape)
                # print(col2pts[seg2col[seg]][:,2])
                    floor_verticles = floor_verticles + [cur_layer_2.min()] * 50 + [cur_layer_2.max()] * 50
            elif flag == 1:
                if cur_layer_1.max() - cur_layer_1.min() > 0.7: continue
                if floor_verticles is None:
                    floor_verticles = [cur_layer_1.min()] * 50 + [cur_layer_1.max()] * 50
                else:
                    floor_verticles = floor_verticles + [cur_layer_1.min()] * 50 + [cur_layer_1.max()] * 50
    print(flag)
            #floor_verticles = np.concatenate([floor_verticles, cur_layer], -1)
    #print(floor_verticles)
    #print(floor_verticles.shape)
    #np.expand_dims(floor_verticles, -1)
    #floor_verticles = floor_verticles.unsqueeze(1)
    floor_verticles = np.array(floor_verticles).reshape(-1, 1)
    N_floor_vertices = floor_verticles.shape[0]
    #print(floor_verticles)
    print(floor_verticles.shape, 'floor vertex')
    db = DBSCAN(eps=0.3, min_samples=10).fit(floor_verticles)
    labels = np.array(db.labels_)
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print(n_clusters_,'floors')

    height = dict()
    means = []
    for cluster_id in range(n_clusters_):
        heis = np.array([_ for _, lbl in zip(floor_verticles, labels) if lbl == cluster_id])
        height[cluster_id] = (heis.min(), heis.max(), heis.mean())
        means.append(heis.mean())
    print(means) 
    id = [_ for _ in range(n_clusters_)]
    for ii in range(n_clusters_ - 1):
        for jj in range(n_clusters_ - ii - 1):
            if means[id[jj]] > means[id[jj+1]]:
                tmp = id[jj]
                id[jj] = id[jj+1]
                id[jj+1] = tmp
    id1 = [_ for _ in range(n_clusters_)]
    for ii in range(n_clusters_):
        id1[id[ii]] = ii
    #[id[_] for _ in range(n_clusters_)]
    # id = id1
    print(id, id1)
    bbox_height = dict()
    for ii in range(n_clusters_):
        if flag == 2:
            if id1[ii] + 1 >= n_clusters_: continue
            low = height[ii][0]
            #print(ii, id1[ii], id)
            high = height[id[id1[ii]+1]][0]
        elif flag == 1:
            if id1[ii] == 0: continue
            low = height[id[id1[ii]-1]][1]
            high = height[ii][1]
        men = (high + low) * 0.5
        #men = height[ii][0], height[id[id1[ii]-1]][1]
        bbox_height[ii] = (low, high) #height[ii][0], height[id[id1[ii]-1]][1])

    print(bbox_height)
 
    def find_lbl(h):
        near = 0
        for i, ver in enumerate(floor_verticles):
            if abs(floor_verticles[near] - h) > abs(ver - h):
                near = i
        return labels[near]

    all_rooms = dict()
    for seg in seg2col.keys():
        if "\"floor\"" in seg:
            if seg2col[seg] not in col2pts.keys(): continue
            room_id = seg[8:]
            cur_pts = col2pts[seg2col[seg]]
            if flag == 2:
                label_id = find_lbl(cur_pts[0][2])#where(floor_verticles == cur_pts[0][1])[0]
            elif flag == 1:
                label_id = find_lbl(cur_pts[0][1])
            #if len(label_id) == 0: continue
            hei_id = label_id #labels[np.where(floor_verticles == cur_pts[0][1])[0][0]]
            if hei_id not in bbox_height.keys(): continue
            #print(cur_pts[0][2], hei_id)
            #print(bbox_height[hei_id])
            hei0, hei1 = bbox_height[hei_id][0], bbox_height[hei_id][1]
            if flag == 2:
                room_box = [[cur_pts[:,0].min(), cur_pts[:,1].min(), hei0],[cur_pts[:,0].max(), cur_pts[:,1].max(), hei1]]
            elif flag == 1:
                room_box = [[cur_pts[:,0].min(), hei0, cur_pts[:,2].min()], [cur_pts[:,0].max(), hei1, cur_pts[:,2].max()]]
            all_rooms[room_id] = room_box
    jsn_rooms = json.dumps(all_rooms, skipkeys=True)
    jsn_file = pre_dir + 'bboxes/{}.json'.format(scene_id)
    with open(jsn_file, 'w') as fo:
        fo.write(jsn_rooms)
    print(jsn_rooms)
