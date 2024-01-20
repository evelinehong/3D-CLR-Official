import json
import numpy as np
import os
from collections import defaultdict
import random
from tqdm import tqdm

scenes = json.load(open("two_rooms.json"))

concepts = json.load(open("new_concepts3_all_concepts_replace.json"))

temps = [i for i in range(100)]
template_dict = np.array([0 for i in range(100)])
concept_dict = [dict() for i in range(100)]
per_answer_dict = [dict() for i in range(100)]

for scene_id in tqdm(scenes):
    ques = []
    if "result" in scene_id: continue
    if "recal" in scene_id: continue
    if "wow" in scene_id: continue
    print (scene_id)

    room_id1 = scene_id.split("_")[0] + "_" + scene_id.split("_")[1]
    room_id2 = scene_id.split("_")[0] + "_" + scene_id.split("_")[2]

    objects1 = json.load(open('./new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis/%s.json'%room_id1))
    objects2 = json.load(open('./new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis/%s.json'%room_id2))
    relationships1 = json.load(open('./new_single_room_relationships_replace_nofilterdetected_all_concepts_replace/%s.json'%room_id1))
    relationships2 = json.load(open('./new_single_room_relationships_replace_nofilterdetected_all_concepts_replace/%s.json'%room_id2))

    house_id = scene_id.split("_")[0]
    house_json = os.path.join("room_bboxes_revised_axis", house_id+".json")
    house = json.load(open(house_json))
    room1_bbox = house[scene_id.split("_")[1]]
    room2_bbox = house[scene_id.split("_")[2]]
    room1_size = (room1_bbox[1][0] - room1_bbox[0][0]) * (room1_bbox[1][1] - room1_bbox[0][1])
    room2_size = (room2_bbox[1][0] - room2_bbox[0][0]) * (room2_bbox[1][1] - room2_bbox[0][1])

    if room1_size > room2_size:
        larger = "1"
    else:
        larger = "2"

    obj_count1 = defaultdict(int)
    obj_ids1 = defaultdict(list)

    obj_count2 = defaultdict(int)
    obj_ids2 = defaultdict(list)

    for (j,obj) in enumerate(objects1):
        obj_count1[obj['class_name']] += 1
        obj_ids1[obj['class_name']].append(j)

    for (j,obj) in enumerate(objects2):
        obj_count2[obj['class_name']] += 1
        obj_ids2[obj['class_name']].append(j)

    l = list(obj_count1.items())
    random.shuffle(l)
    obj_count1 = dict(l)

    l = list(obj_count2.items())
    random.shuffle(l)
    obj_count2 = dict(l)

    temp = "Are there <R> <S>s in the room with <S2> than the other?"

    find = False
    
    for obj in obj_count1:
        if obj in obj_count2:
            for obj2 in obj_count1: 
                if obj == obj2: continue
                if not obj2 in obj_count2:
                    if obj_count1[obj] > obj_count2[obj]:   
                        if random.random() > 0.5:
                            que = temp.replace("<R>", "more").replace("<S>", obj).replace("<S2>", obj2)
                            ans = True
                            ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "more"]}) 
                        else:
                            que = temp.replace("<R>", "fewer").replace("<S>", obj).replace("<S2>", obj2)
                            ans = True
                            ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "fewer"]})

                        # find = True
                        # break
                        print (scene_id, que, ans)

                    if obj_count1[obj] < obj_count2[obj]:   
                        if random.random() > 0.5:
                            que = temp.replace("<R>", "fewer").replace("<S>", obj).replace("<S2>", obj2)
                            ans = True
                            ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "fewer"]}) 
                        else:
                            que = temp.replace("<R>", "more").replace("<S>", obj).replace("<S2>", obj2)
                            ans = True
                            ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "more"]})

                        # find = True
                        # break
    

    #     # if find: break
    # if room1_size / room2_size > 1.5 or room2_size / room1_size > 1.5:
    #     temp = "Are there <R> <S>s in the <R2> room than the other?"

    #     find = False
        
    #     for obj in obj_count1:
    #         if obj in obj_count2:
    #             for obj2 in obj_count1: 
    #                 if obj == obj2: continue
    #                 # if not obj2 in obj_count2:
    #                 if larger == "1": rel = "larger"
    #                 else: rel = "smaller"

    #                 if obj_count1[obj] > obj_count2[obj]:   
    #                     if random.random() > 0.5:
    #                         que = temp.replace("<R>", "more").replace("<S>", obj).replace("<R2>", rel)
    #                         ans = True
    #                         ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "more"]}) 
    #                     else:
    #                         que = temp.replace("<R>", "fewer").replace("<S>", obj).replace("<R2>", rel)
    #                         ans = True
    #                         ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "fewer"]})

    #                     # find = True
    #                     # break

    #                 if obj_count1[obj] < obj_count2[obj]:   
    #                     if random.random() > 0.5:
    #                         que = temp.replace("<R>", "fewer").replace("<S>", obj).replace("<R2>", rel)
    #                         ans = True
    #                         ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "fewer"]}) 
    #                     else:
    #                         que = temp.replace("<R>", "more").replace("<S>", obj).replace("<R2>", rel)
    #                         ans = True
    #                         ques.append({"question": que, "answer": ans, "scene_id": scene_id, "family_id": [3], "template": 0, "concept": [obj, obj2, "more"]})

    #                     # find = True
    #                     # break

    #     # if find: break

    # l = list(obj_count1.items())
    # random.shuffle(l)
    # obj_count1 = dict(l)

    # l = list(obj_count2.items())
    # random.shuffle(l)
    # obj_count2 = dict(l)

    # temp = "How many rooms have <S>s?"
    # count = False

    # for concept in concepts:
    #     ans = 0
    #     if concept in obj_count1:
    #         ans += 1
    #     if concept in obj_count2:
    #         ans += 1
    #     que = temp.replace("<S>", concept)
        
    #     ques.append({"question": que, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "template": 1, "copncept": [concept]}) 

    #     # if (not count):
    #     #     if not ans in per_answer_dict[6]:
    #     #         per_answer_dict[6][ans] = 1
    #     #         ques.append({"question": que, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "template": 1}) 
    #     #         count = True

    #     #     else:
    #     #         per_answer_dict[6] = dict(sorted(per_answer_dict[6].items(), key=lambda item: item[1]))
    #     #         # if ans != list(per_answer_dict[4].keys())[-1]:
                    
    #     #         answer_counts_sorted = sorted(per_answer_dict[6].values())

    #     #         median_count = answer_counts_sorted[len(answer_counts_sorted) // 2]
    #     #         median_count = max(median_count, 5)

    #     #         try:
    #     #             if per_answer_dict[6][ans] > answer_counts_sorted[-2]:
    #     #                 continue
    #     #         except:
    #     #             pass
    #     #         if per_answer_dict[6][ans] > 1.5 * median_count:
    #     #             continue
    #     #         if per_answer_dict[6][ans] > 2 * answer_counts_sorted[0]:
    #     #             continue 

    #     #         per_answer_dict[6][ans] += 1
    #     #         ques.append({"question": que, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "template": 1})
    #     #         count = True 

    #     # if count: continue 

    # # temp = "Is there a room that has <S>s?"

    # # for (k,que) in enumerate(ques):
    # #     ques[k]["room_type"] = "two_rooms"

    # # # with open("all_questions3/%s"%scene_id, "w") as f1:
    # # #     json.dump(ques, f1)       
    # # 

    # temp = "How many rooms have <S> <R> the <S2>?"
    # rel_list1 = []
    # rel_list2 = []
    # rel_dict = defaultdict(list)

    # for rel in ['top', 'above', 'below', 'inside', 'close']:

    #     if not rel in relationships1: continue

    #     true_count = 0
    #     false_count = 0  

    #     for obj2 in obj_count1:
    #         rel_count = defaultdict(int)
    #         find = 0
    #         obj_name = ''

    #         o2s = obj_ids1[obj2]

    #         for o1 in objects1:                         
    #             ob1 = o1['id']
    #             for o2 in o2s:
    #                 o2 = objects1[o2]['id']
                    
    #                 if [ob1, str(o2)] in relationships1[rel]:
    #                     # rel_dict
    #                     # rel_list1.append(o1['class_name'] + obj2)
    #                     if not "1" in rel_dict[o1['class_name'] + "%" + obj2 + "%" + rel]:
    #                         rel_dict[o1['class_name'] + "%" + obj2 + "%" + rel].append("1")

    # for rel in ['top', 'above', 'below', 'inside', 'close']:
    #     if not rel in relationships2: continue

    #     true_count = 0
    #     false_count = 0        

    #     for obj2 in obj_count2:
    #         rel_count = defaultdict(int)
    #         find = 0
    #         obj_name = ''

    #         o2s = obj_ids2[obj2]

    #         for o1 in objects2:                         
    #             ob1 = o1['id']
    #             for o2 in o2s:
    #                 o2 = objects2[o2]['id']

    #                 if [ob1, str(o2)] in relationships2[rel]:
    #                     if not "2" in rel_dict[o1['class_name'] + "%" + obj2 + "%" + rel]:
    #                         rel_dict[o1['class_name'] + "%" + obj2 + "%" + rel].append("2")
    #                     # rel_list2.append(o1['class_name'] + obj2)

    # for key, lis in rel_dict.items():
    #     rel2 = rel
    #     obj1, obj2, rel = key.split("%")
    #     rel2 = rel
    #     if rel == 'close': rel2 = 'close to'
    #     if rel == 'top': rel2 = 'on top of '

    #     que = temp.replace("<S>", obj1).replace("<S2>", obj2).replace("<R>", rel2)
    #     ans = len(lis)




    

