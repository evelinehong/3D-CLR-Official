import os
import re
import copy
import json
import random
import numpy as np

from plyfile import PlyData, PlyElement

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

val_scene_ids = [
    "00800-TEEsavR23oF",
    "00802-wcojb4TFT35",
    "00813-svBbv1Pavdk", 
    "00814-p53SfW6mjZe",
    "00820-mL8ThkuaVTM", 
    "00824-Dd4bFSTQ8gi",
    "00829-QaLdnwvtxbs",
    "00832-qyAac8rV8Zk",
    "00835-q3zU7Yy5E5s", 
    "00839-zt1RVoi7PcG",
    "00843-DYehNKdT76V",
    "00848-ziup5kvtCCR",
    "00853-5cdEh9F2hJL",
    "00873-bxsVRursffK",
    "00876-mv2HUxq3B53",
    "00877-4ok3usBNeis",
    "00878-XB4GS9ShBRE",
    "00880-Nfvxx8J5NCo",
    "00890-6s7QHgap2fW",
    "00891-cvZr5TUy5C5"
]

# demo_scene_lis = ['00800-TEEsavR23oF'] 

def get_ply_pts(stg, col):
    lis = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", stg)
    r, g, b = int(col[:2],16)/255., int(col[2:4],16)/255., int(col[4:],16)/255. 
    return (lis[0], lis[1], lis[2], r, g, b) #np.array(lis, dtype=float)
def get_pts(stg, _):
    lis = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", stg)
    return np.array(lis, dtype=float)

lis = val_scene_ids + train_scene_ids

print(lis)

lis = [_ for _ in lis if not os.path.exists('./data/scene_datasets/hm3d_semantic/ply/{}.ply'.format(_))]

print(lis)

for scene_id in lis: #val_scene_ids + train_scene_ids:
    print(scene_id)

    col_file = pre_dir + 'pts/{}.txt'.format(scene_id)
    seg_file = pre_dir + '{}/{}.semantic.txt'.format(scene_id, scene_id[6:])

    with open(col_file) as fi:
        col_map = fi.readlines()
    with open(seg_file) as fi:
        seg_map = fi.readlines()[1:]

    seg2col = dict()
    for item in seg_map:
        sp = 0
        while item[sp]!='\"': sp += 1
        seg2col[item[sp:-1]+'_'+item[:sp-8]] = item[sp-7:sp-1]

    #all_vertices = []
    ano_vertices = []

    col2pts = dict()
    for item in col_map:
    #    all_vertices.append(get_pts(item[7:], item[:6]))
        if item[:6] not in col2pts.keys():
            col2pts[item[:6]] = [get_ply_pts(item[7:], item[:6])]
        else:
            col2pts[item[:6]].append(get_ply_pts(item[7:], item[:6]))

    #cnt, cnt2 = 0, 0
    #all_bboxes = dict()
    for ky in seg2col.keys():
        if seg2col[ky] in col2pts.keys():
            #vers = np.array(col2pts[seg2col[ky]])
            
            #xmn, xmx = vers[:,0].min(), vers[:,0].max()
            #ymn, ymx = vers[:,1].min(), vers[:,1].max()
            #zmn, zmx = vers[:,2].min(), vers[:,2].max()
            #box = [[xmn, ymn, zmn], [xmx, ymx, zmx]]
            #all_bboxes[ky] = box
            #cnt += 1
            if ano_vertices is None:
                ano_vertices = col2pts[seg2col[ky]]
            else:
                ano_vertices = ano_vertices + col2pts[seg2col[ky]]
        #else:
            #cnt2 += 1
            # print(seg2col[ky])
            # A588CF 8D1CFB CCA207 95110C 03B932 9FEBB1 944DA5
    
    #jsn_bboxes = json.dumps(all_bboxes, skipkeys=True)
    #jsn_file = pre_dir + 'all_bboxes/{}.json'.format(scene_id)
    #with open(jsn_file, 'w') as fo:
    #    fo.write(jsn_bboxes)
    #print(jsn_bboxes)

    # exit()
    # all_vertices = np.array(all_vertices, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'f4'), ('green', 'f4'), ('blue', 'f4')])
    ano_vertices = np.array(ano_vertices, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'f4'), ('green', 'f4'), ('blue', 'f4')])
    
    # el_all = PlyElement.describe(all_vertices, 'vertex')
    el_ano = PlyElement.describe(ano_vertices, 'vertex')

    # PlyData([el_all], text=True).write('all.ply')
    PlyData([el_ano], text=True).write('data/scene_datasets/hm3d_semantic/ply/{}.ply'.format(scene_id))

    # for ky in col2pts.keys():
    #     col2pts[ky] = np.array(col2pts[ky])
    
    # print(cnt, cnt2)
    # print(all_vertices.shape, ano_vertices.shape)
    
