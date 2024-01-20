import json
import numpy as np
import os
from collections import defaultdict
import random
from tqdm import tqdm

# scenes = json.load(open("single_rooms.json"))
scenes = os.listdir("new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis")
# concepts = json.load(open("concepts.json"))
concepts = json.load(open("new_concepts3_all_concepts_replace.json"))

temps = [i for i in range(100)]
template_dict = np.array([0 for i in range(100)])
concept_dict = [dict() for i in range(100)]
per_answer_dict = [dict() for i in range(100)]

def boxes_distance(A_min, A_max, B_min, B_max):
    delta1 = A_min - B_max
    delta2 = B_min - A_max
    u = np.max(np.array([np.zeros(len(delta1)), delta1]), axis=0)
    v = np.max(np.array([np.zeros(len(delta2)), delta2]), axis=0)
    dist = np.linalg.norm(np.concatenate([u, v]))
    return dist

for scene_id in tqdm(scenes):
    # if not "00820" in scene_id: continue
    if not scene_id in os.listdir('./new_single_room_relationships_replace_nofilterdetected_all_concepts_replace'): continue
    # if scene_id in os.listdir("./all_questions2"): continue
    # if scene_id in os.listdir("./new_all_questions"): continue
    ques = []
    if "result" in scene_id: continue
    if "recal" in scene_id: continue
    # scene_id2 = scene_id.split("_")[0] + "_" + scene_id.split("_")[1]
    # scene_id2 = scene_id.replace(".json", "")
    chosen_temps = temps

    objects = json.load(open('./new_single_room_bboxes_replace_nofilterdetected_all_concepts_replace_revised_axis/%s'%scene_id))
    relationships = json.load(open('./new_single_room_relationships_replace_nofilterdetected_all_concepts_replace/%s'%scene_id))

    obj_count = defaultdict(int)
    obj_ids = defaultdict(list)

    for (j,obj) in enumerate(objects):
        obj_count[obj['class_name']] += 1
        obj_ids[obj['class_name']].append(j)

    # print (obj_count, scene_id)

    # # zero_hop   
 
    if 0 in chosen_temps or 1 in chosen_temps:
        random.shuffle(concepts)

        temps1 = ["Are there any <S>s?", "Is there a <S>?"]
        temps2 = ["How many <S>s are there?", "What number of <S>s are there?"]

        filter = False
        count = False

        for concept in concepts:
        
            prog1 = [["filter", concept], ["exist"]]

            prog2 = [["filter", concept], ["get_instance"], ["count"]]

            temp1 = random.choice(temps1)
            temp2 = random.choice(temps2)
            
            que1 = temp1.replace("<S>", concept)
            que2 = temp2.replace("<S>", concept)

            if concept in obj_count.keys():
                ans1 = True
            else:
                ans1 = False
            
            ans2 = obj_count[concept]

            if 0 in chosen_temps:
                ques.append({"question": que1, "program": prog1, "answer": ans1, "template":0, "scene_id": scene_id, "family_id": [0], "concept": [concept]})
                # if not ans1 in per_answer_dict[0]:
                #     per_answer_dict[0][ans1] = 1

                #     ques.append({"question": que1, "program": prog1, "answer": ans1, "template":0, "scene_id": scene_id, "family_id": [0]})
                #     filter = True
                # else:
                #     per_answer_dict[0] = dict(sorted(per_answer_dict[0].items(), key=lambda item: item[1]))

                #     if ans1 == list(per_answer_dict[0].keys())[0]:
                        
                #         per_answer_dict[0][ans1] += 1


                #         ques.append({"question": que1, "program": prog1, "answer": ans1, "template":0, "scene_id": scene_id, "family_id": [0]})
                #         filter = True
                        

            if 1 in chosen_temps:
                # if not ans2 == 0: 
                ques.append({"question": que2, "program": prog2, "answer": ans2, "template":1, "scene_id": scene_id, "family_id": [1], "concept": [concept]})
                # if not ans2 > 9:     
                #     if not (ans2 in per_answer_dict[1]):
                #         per_answer_dict[1][ans2] = 1
                #         ques.append({"question": que2, "program": prog2, "answer": ans2, "template":1, "scene_id": scene_id, "family_id": [1]})
                #         count = True
                #     else:
                #         per_answer_dict[1] = dict(sorted(per_answer_dict[1].items(), key=lambda item: item[1]))

                #         answer_counts_sorted = sorted(per_answer_dict[1].values())

                #         median_count = answer_counts_sorted[len(answer_counts_sorted) // 2]
                #         median_count = max(median_count, 5)

                #         # try:
                #         #     if per_answer_dict[1][ans2] > answer_counts_sorted[-2]:
                #         #         continue
                #         # except:
                #         #     pass
                #         # if per_answer_dict[1][ans2] > 1.5 * median_count:
                #         #     continue
                #         # if per_answer_dict[1][ans2] > 2 * answer_counts_sorted[0]:
                #         #     continue

                #         # if ans2 != list(per_answer_dict[1].keys())[-1]:
                            
                #         per_answer_dict[1][ans2] += 1
                    
                #         ques.append({"question": que2, "program": prog2, "answer": ans2, "template":1, "scene_id": scene_id, "family_id": [1]})
                #         count = True
                            
                           
    #         # if filter and count:
    #         #     break

    # # one_hop relationship
    # # two-object relationship
    
    if 2 in chosen_temps:
        l = list(obj_count.items())
        random.shuffle(l)
        obj_count = dict(l)

        temp = ["Is the <S> <R> the <S2>?"]

        # rel = "1"
        # rel_cnt = 0
        # while (rel not in relationships) and rel_cnt < 100:
        #     rel = random.choice(['above', 'top', 'below', 'inside', 'close'])
        #     rel_cnt += 1
        # if not rel_cnt > 99:

        for rel in ['above', 'top', 'below', 'inside', 'close']:
            if not rel in relationships:
                continue
            rel2 = rel
            if rel == 'close': rel2 = 'close to'
            if rel == 'top': rel2 = 'on top of '

            true_count = 0
            false_count = 0

            find = False

            for obj1 in obj_count:
                for obj2 in obj_count:
                    if obj1 == obj2: continue
                    if obj_count[obj1] == 1 and obj_count[obj2] == 1:
                        ob1 = objects[obj_ids[obj1][0]]['id']
                        ob2 = objects[obj_ids[obj2][0]]['id']   

                        obb1 = objects[obj_ids[obj1][0]] 
                        obb2 = objects[obj_ids[obj2][0]]   

                        rel3 = rel2
                        if rel in ['top', 'inside', 'close']:
                            if [ob1, ob2] in relationships[rel]:
                                ans = True
                                true_count += 1
                                que = random.choice(temp).replace("<R>", rel2).replace("<S>", obj1).replace("<S2>", obj2)
                                prog = [["filter", obj1], ["filter", obj2], [rel, [0,1]]]

                                ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "concept": [rel3, obj1, obj2]})

                            else:
                                # if not false_count < true_count:
                                #     continue
                                if rel == 'close':
                                    import math
                                    
                                    if math.sqrt(((obb1['bbox'][0][0] + obb1['bbox'][1][0]) / 2 - (obb2['bbox'][0][0] + obb2['bbox'][1][0]) / 2) ** 2 + ((obb1['bbox'][0][1] + obb1['bbox'][1][1]) / 2 - (obb2['bbox'][0][1] + obb2['bbox'][1][1]) / 2) ** 2 + ((obb1['bbox'][0][2] + obb1['bbox'][1][2]) / 2 - (obb2['bbox'][0][2] + obb2['bbox'][1][2]) / 2) ** 2) - (math.sqrt((obb1['bbox'][1][0] - obb1['bbox'][0][0]) / 2 ** 2  + (obb1['bbox'][1][1] - obb1['bbox'][0][1]) / 2 ** 2 + (obb1['bbox'][1][2] - obb1['bbox'][0][2]) / 2 ** 2)) + math.sqrt((obb2['bbox'][1][0] - obb2['bbox'][0][0]) / 2 ** 2  + (obb2['bbox'][1][1] - obb2['bbox'][0][1]) / 2 ** 2 + (obb2['bbox'][1][2] - obb2['bbox'][0][2]) / 2 ** 2) < 1.0:
                                        continue


                                false_count += 1
                                ans = False

                                que = random.choice(temp).replace("<R>", rel2).replace("<S>", obj1).replace("<S2>", obj2)
                                prog = [["filter", obj1], ["filter", obj2], [rel, [0,1]]]    

                                ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "concept": [rel3, obj1, obj2]})             
                            
                        else:
                            if [ob1, ob2] in relationships[rel]:
                                ans = True
                                true_count += 1
                                que = random.choice(temp).replace("<R>", rel2).replace("<S>", obj1).replace("<S2>", obj2)
                                prog = [["filter", obj1], ["filter", obj2], [rel, [0,1]]] 

                                ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "concept": [rel3, obj1, obj2]})

                                if rel == 'above': rel3 = 'below'
                                if rel == 'below': rel3 = 'above'
                                ans = False
                                que = random.choice(temp).replace("<R>", rel3).replace("<S>", obj1).replace("<S2>", obj2)
                                prog = [["filter", obj1], ["filter", obj2], [rel, [0,1]]]          

                                ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2], "concept": [rel3, obj1, obj2]})

                                
                        # if not find:
                        #     if not ans in per_answer_dict[2]:
                        #         per_answer_dict[2][ans] = 1
                        #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})
                        #         find = True

                        #     else:
                        #         per_answer_dict[2] = dict(sorted(per_answer_dict[2].items(), key=lambda item: item[1]))
                        #         if ans != list(per_answer_dict[2].keys())[-1]:
                                    
                        #             per_answer_dict[2][ans] += 1
                        #             find = True

                        #             ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})


    #             # if find:
    #             #     break                             

    l = list(obj_count.items())
    random.shuffle(l)
    obj_count = dict(l)

    if 3 in chosen_temps or 4 in chosen_temps:
        temps1 = ["Is there a <S> <R> the <S2>?", "Are there any <S>s <R> the <S2>?"]
        temps2 = ["How many <S>s are <R> the <S2>?", "What number of <S>s are <R> the <S2>?"]
        temps3 = ["What's <R> the <S2>?", "What object is <R> the <S2>?"]
        filter = False
        count = False
        query = False
        # for rel in ['above']:
        # rel = "1"
        # rel_cnt = 0
        # while (rel not in relationships) and rel_cnt < 100:
        #     rel = random.choice(['above', 'top', 'below', 'inside', 'close'])
        #     rel_cnt += 1
            
        # if not rel_cnt > 99:
        for rel in ['top', 'above', 'below', 'inside', 'close']:
            if not rel in relationships: continue
            rel2 = rel
            if rel == 'close': rel2 = 'close to'
            if rel == 'top': rel2 = 'on top of '

            true_count = 0
            false_count = 0
            
            find2 = False

            for obj2 in obj_count:
                if obj_count[obj2] == 1:
                    rel_count = defaultdict(int)
                    find = 0
                    obj_name = ''

                    o2 = objects[obj_ids[obj2][0]]['id']

                    for o1 in objects:                         
                        ob1 = o1['id']

                        if [ob1, str(o2)] in relationships[rel]:
                            
                            rel_count[o1['class_name']] += 1
                            find += 1
                            obj_name = o1['class_name']

                    for name, cnt in rel_count.items():
                        prog = [["filter", name], ["get_instance"], ["filter", obj2], [rel, [1,2], "count"]]
                        # prog = "count(filter(%s) and filter(%s(%s)))"%(name, rel, obj2)
                        que = random.choice(temps2).replace("<R>", rel2).replace("<S>", name).replace("<S2>", obj2)
                        ans = cnt

                        ques.append({"question": que, "program": prog, "answer": ans, "template":4, "scene_id": scene_id, "family_id": [2], "concept": [rel, name, obj2]}) 

                        # if 4 in chosen_temps and (not count):
                        #     if not ans > 4:
                        #         if not ans in per_answer_dict[4]:
                        #             per_answer_dict[4][ans] = 1
                        #             ques.append({"question": que, "program": prog, "answer": ans, "template":4, "scene_id": scene_id, "family_id": [2]}) 
                        #             find2 = True 
                        #             count = True
                                    
                        #         else:
                        #             # per_answer_dict[4] = dict(sorted(per_answer_dict[4].items(), key=lambda item: item[1]))
                        #             # if ans != list(per_answer_dict[4].keys())[-1]:
                                        
                        #             answer_counts_sorted = sorted(per_answer_dict[4].values())

                        #             median_count = answer_counts_sorted[len(answer_counts_sorted) // 2]
                        #             median_count = max(median_count, 5)

                        #             # try:
                        #             #     if per_answer_dict[4][ans] > answer_counts_sorted[-2]:
                        #             #         continue
                        #             # except:
                        #             #     pass
                        #             # if per_answer_dict[4][ans] > 1.5 * median_count:
                        #             #     continue
                        #             # if per_answer_dict[4][ans] > 2 * answer_counts_sorted[0]:
                        #             #     continue

                        #             per_answer_dict[4][ans] += 1
                        #             ques.append({"question": que, "program": prog, "answer": ans, "template":4, "scene_id": scene_id, "family_id": [2]})  
                        #             find2 = True 
                        #             count = True
                                    

                    for obj1 in obj_count:
                        if rel_count[obj1] != 0:
                            prog = [["filter", obj1], ["get_instance"], ["filter", obj2], [rel, [1,2], "exist"]]
                            que = random.choice(temps1).replace("<R>", rel2).replace("<S>", obj1).replace("<S2>", obj2)
                            # prog = "exist(filter(%s) and filter(%s(%s)))"%(obj1, rel, obj2)
                            ans = True
                            true_count += 1                        
                            
                            ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj2]})

                            # if 3 in chosen_temps and (not filter):
                            #     if not ans in per_answer_dict[3]:
                            #         per_answer_dict[3][ans] = 1
                            #         ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2]})
                            #         find2 = True

                            #         filter = True
                                    
                            #     else:
                            #         per_answer_dict[3] = dict(sorted(per_answer_dict[3].items(), key=lambda item: item[1]))
                            #         if ans != list(per_answer_dict[3].keys())[-1]:
                                        
                            #             per_answer_dict[3][ans] += 1

                            #             ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2]})  
                            #             find2 = True

                            #             filter = True
                                        

                            # ques.append(que)
                            # q_progs.append(prog)
                            # answers.append(ans)    
                        else:
                            # if false_count < true_count:
                            prog = [["filter", obj1], ["get_instance"], ["filter", obj2], [rel, [1,2], "exist"]]
                            # prog = "exist(filter(%s) and filter(%s(%s)))"%(obj1, rel, obj2)
                            ans = False
                            que = random.choice(temps1).replace("<R>", rel2).replace("<S>", obj1).replace("<S2>", obj2)
                            false_count += 1

                            ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj2]})

                            # if 3 in chosen_temps and (not filter):
                            #     if not ans in per_answer_dict[3]:
                            #         per_answer_dict[3][ans] = 1
                            #         ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2]})
                            #         find2 = True

                            #         filter = True
                                    
                            #     else:
                            #         per_answer_dict[3] = dict(sorted(per_answer_dict[3].items(), key=lambda item: item[1]))
                            #         if ans != list(per_answer_dict[3].keys())[-1]:
                                        
                            #             per_answer_dict[3][ans] += 1

                            #             ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2]})  
                            #             find2 = True

                            #             filter = True
                                                                                                           

                    if find == 1:
                        prog = "query(filter(%s(%s)))"%(rel, obj2)
                        que = random.choice(temps3).replace("<R>", rel2).replace("<S2>", obj2)
                        ans = obj_name
                        
                        ques.append({"question": que, "program": prog, "answer": ans, "template":5, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj2]})

                        # if not query:
                        #     ques.append({"question": que, "program": prog, "answer": ans, "template":3, "scene_id": scene_id, "family_id": [2]})
                        #     query = True  

                # if find2 and filter and count and query:
                #     break 

    # # # greater, fewer
    # # l = list(obj_count.items())
    # # random.shuffle(l)
    # # obj_count = dict(l)

    temp = "Is the number of <S1>s <R> than the number of <S2>s?"

    find = False
    for obj1 in obj_count:
        for obj2 in obj_count:
            if obj_count[obj1] > obj_count[obj2]:
                # if random.random() > 0.5:
                que = temp.replace("<S1>", obj1).replace("<S2>", obj2).replace("<R>", "greater")
                ans = True
                prog = "greater_than(filter(%s), filter(%s))"%(obj1, obj2)

                ques.append({"question": que, "program": prog, "answer": ans, "template":6, "scene_id": scene_id, "family_id": [3], "concept": [obj1, obj2, "greater"]})
                # else:
                que = temp.replace("<S1>", obj1).replace("<S2>", obj2).replace("<R>", "fewer")
                ans = False
                prog = "less_than(filter(%s), filter(%s))"%(obj1, obj2)

                ques.append({"question": que, "program": prog, "answer": ans, "template":6, "scene_id": scene_id, "family_id": [3], "concept": [obj1, obj2, "less"]})

                find = True
            # if find: break
            if obj_count[obj1] < obj_count[obj2]:
                # if random.random() > 0.5:
                que = temp.replace("<S1>", obj1).replace("<S2>", obj2).replace("<R>", "greater")
                ans = False
                prog = "greater_than(filter(%s), filter(%s))"%(obj1, obj2)

                ques.append({"question": que, "program": prog, "answer": ans, "template":6, "scene_id": scene_id, "family_id": [3], "concept": [obj1, obj2, "greater"]})
                # else:
                que = temp.replace("<S1>", obj1).replace("<S2>", obj2).replace("<R>", "fewer")
                ans = True
                prog = "less_than(filter(%s), filter(%s))"%(obj1, obj2)

                ques.append({"question": que, "program": prog, "answer": ans, "template":6, "scene_id": scene_id, "family_id": [3], "concept": [obj1, obj2, "less"]})

    # #             find = True

    # #     #     if find: break
    # #     # if find: break            

    # # print (ques)

    # # # three-object relationship 
    # # # between

    l = list(obj_count.items())
    random.shuffle(l)
    obj_count = dict(l)

    temps1 = ["Is there a <S> <R2> the <S2> and <S3>?", "Are there any <S>s <R2> the <S2> and <S3>?"]
    temps2 = ["How many <S>s are <R2> the <S2> and <S3>?", "What number of <S>s are <R2> the <S2> and <S3>?"]
    temps3 = ["What's <R2> the <S2> and <S3>?", "What object is <R2> the <S2> and <S3>?"]

    rel = "between"
    
    from tqdm import tqdm

    between_dict = defaultdict(list)
    try:
        for pairs in relationships[rel]:
            between_dict[str(pairs[0]) + ' ' + str(pairs[2])].append(pairs[1])
    except:
        continue

    count = False
    filter = False
    query = False

    for pairs in relationships[rel]:
        # find_dict = defaultdict(bool)

        for ob in objects:
            if ob['id'] == pairs[0]: o1 = ob; obj1 = o1['class_name']
            if ob['id'] == pairs[2]: o3 = ob; obj3 = o3['class_name']

        # if find_dict[(obj1, obj3)]:
        #     continue

        # find_dict[(obj1, obj3)] = True

        if obj_count[obj1] == 1 and obj_count[obj3] == 1:

            rel_count = defaultdict(int)
            find = 0
            obj_name = ''

            # o1 = obj_ids[obj1][0]
            # o3 = obj_ids[obj3][0]

            for o2 in objects:   
                ob2 = o2['id']

                if str(ob2) in between_dict[str(pairs[0]) + ' ' + str(pairs[2])]:
            #     if [o1, o2, o3] in relationships[rel]:
                    
                    rel_count[o2['class_name']] += 1
                    find += 1
                    obj_name = o2['class_name']

            for name, cnt in rel_count.items():
                
                prog = "count(filter(%s) and filter(%s(%s, %s)))"%(name, rel, obj1, obj3)
                que = random.choice(temps2).replace("<R2>", rel).replace("<S2>", obj1).replace("<S>", name).replace("<S3>", obj3)
                ans = cnt
                
                ques.append({"question": que, "program": prog, "answer": ans, "template":8, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, name, obj3]}) 

                # if (not count) and (not ans > 4):
                #     if not ans in per_answer_dict[6]:
                #         per_answer_dict[6][ans] = 1
                #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]}) 
                #         count = True

                #     else:
                #         per_answer_dict[6] = dict(sorted(per_answer_dict[6].items(), key=lambda item: item[1]))
                #         # if ans != list(per_answer_dict[4].keys())[-1]:
                            
                #         answer_counts_sorted = sorted(per_answer_dict[6].values())

                #         median_count = answer_counts_sorted[len(answer_counts_sorted) // 2]
                #         median_count = max(median_count, 5)

                        # try:
                        #     if per_answer_dict[6][ans] > answer_counts_sorted[-2]:
                        #         continue
                        # except:
                        #     pass
                        # if per_answer_dict[6][ans] > 1.5 * median_count:
                        #     continue
                        # if per_answer_dict[6][ans] > 2 * answer_counts_sorted[0]:
                        #     continue 

                        # per_answer_dict[6][ans] += 1
                        # ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})
                        # count = True  

                # if count:
                #     break

            for obj2 in obj_count:
                if rel_count[obj2] == 0:
                    prog = "exist(filter(%s) and filter(%s(%s, %s)))"%(obj2, rel, obj1, obj3)
                    ans = False
                    que = random.choice(temps1).replace("<R2>", rel).replace("<S2>", obj1).replace("<S>", obj2).replace("<S3>", obj3)
                    
                    ques.append({"question": que, "program": prog, "answer": ans, "template":7, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj2, obj3]}) 

                    # if not filter:
                    #     if not ans in per_answer_dict[7]:
                    #         per_answer_dict[7][ans] = 1

                    #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #         filter = True
                    #     else:
                    #         per_answer_dict[7] = dict(sorted(per_answer_dict[7].items(), key=lambda item: item[1]))
                    #         if ans != list(per_answer_dict[7].keys())[-1]:
                    #             per_answer_dict[7][ans] += 1
                    #             ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #             filter = True                                

                else:
                    que = random.choice(temps1).replace("<R2>", rel).replace("<S2>", obj1).replace("<S>", obj2).replace("<S3>", obj3)
                    prog = "exist(filter(%s) and filter(%s(%s, %s)))"%(obj2, rel, obj1, obj3)
                    ans = True

                    ques.append({"question": que, "program": prog, "answer": ans, "template":7, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj2, obj3]}) 

                    # if not filter:
                    #     if not ans in per_answer_dict[7]:
                    #         per_answer_dict[7][ans] = 1

                    #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #         filter = True                                          
                    #     else:
                    #         per_answer_dict[7] = dict(sorted(per_answer_dict[7].items(), key=lambda item: item[1]))
                    #         if ans != list(per_answer_dict[7].keys())[-1]:
                    #             per_answer_dict[7][ans] += 1
                    #             ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #             filter = True 

                # if filter:
                #     break
            if find == 1:
                prog = "query(filter(%s(%s, %s)))"%(rel, obj1, obj3)
                que = random.choice(temps3).replace("<R2>", rel).replace("<S2>", obj1).replace("<S3>", obj3)
                ans = obj_name

                ques.append({"question": que, "program": prog, "answer": ans, "template":9, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj3]}) 
                query = True 

        # if filter and count and query:
        #     break
            
                    
    # # print (ques)                  

    # # # three-object
    # # # left-right
    # # from tqdm import tqdm

    l = list(obj_count.items())
    random.shuffle(l)
    obj_count = dict(l)

    temps1 = ["Viewing <S2> from <S>, is there a <S3> on the <R3>?"]
    temps2 = ["Viewing <S2> from <S>, How many <S3>s are on the <R3>?"]
    # temps3 = ["Viewing <S2> from <S>, what is on the <R3>?"]

    # rels = ["left", "right"]
    rel = random.choice(["left", "right"])
    
    # from tqdm import tqdm

    between_dict = defaultdict(list)
    try:
        for pairs in relationships[rel]:
            between_dict[str(pairs[0]) + ' ' + str(pairs[1])].append(pairs[2])
    except:
        continue

    count = False
    filter = False

    for pairs in relationships[rel]:
        # find_dict = defaultdict(bool)

        for ob in objects:
            if ob['id'] == pairs[0]: o1 = ob; obj1 = o1['class_name']
            if ob['id'] == pairs[1]: o3 = ob; obj3 = o3['class_name']

        # if find_dict[(obj1, obj3)]:
        #     continue

        # find_dict[(obj1, obj3)] = True

        if obj_count[obj1] == 1 and obj_count[obj3] == 1:

            rel_count = defaultdict(int)
            find = 0
            obj_name = ''

            # o1 = obj_ids[obj1][0]
            # o3 = obj_ids[obj3][0]

            for o2 in objects:   
                ob2 = o2['id']

                if str(ob2) in between_dict[str(pairs[0]) + ' ' + str(pairs[1])]:
            #     if [o1, o2, o3] in relationships[rel]:
                    
                    rel_count[o2['class_name']] += 1
                    # find += 1
                    # obj_name = o2['class_name']

            for name, cnt in rel_count.items():
                
                prog = "count(filter(%s) and filter(%s(%s, %s)))"%(name, rel, obj1, obj3)
                que = random.choice(temps2).replace("<R3>", rel).replace("<S>", obj1).replace("<S2>", obj3).replace("<S3>", name)
                ans = cnt

                ques.append({"question": que, "program": prog, "answer": ans, "template":11, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj3, name]}) 

                # if (not count) and (not ans > 4):
                #     if not ans in per_answer_dict[6]:
                #         per_answer_dict[6][ans] = 1
                #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]}) 
                #         count = True

                #     else:
                #         per_answer_dict[6] = dict(sorted(per_answer_dict[6].items(), key=lambda item: item[1]))
                #         # if ans != list(per_answer_dict[4].keys())[-1]:
                            
                #         answer_counts_sorted = sorted(per_answer_dict[6].values())

                #         median_count = answer_counts_sorted[len(answer_counts_sorted) // 2]
                #         median_count = max(median_count, 5)

                #         # try:
                #         #     if per_answer_dict[6][ans] > answer_counts_sorted[-2]:
                #         #         continue
                #         # except:
                #         #     pass
                #         # if per_answer_dict[6][ans] > 1.5 * median_count:
                #         #     continue
                #         # if per_answer_dict[6][ans] > 2 * answer_counts_sorted[0]:
                #         #     continue 

                #         per_answer_dict[6][ans] += 1
                #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})
                #         count = True  

                # if count:
                #     break

            for obj2 in obj_count:
                if rel_count[obj2] == 0:
                    prog = "exist(filter(%s) and filter(%s(%s, %s)))"%(obj2, rel, obj1, obj3)
                    ans = False
                    que = random.choice(temps1).replace("<R3>", rel).replace("<S>", obj1).replace("<S2>", obj3).replace("<S3>", obj2)
                    
                    ques.append({"question": que, "program": prog, "answer": ans, "template":10, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj3, obj2]})

                    # if not filter:
                    #     if not ans in per_answer_dict[7]:
                    #         per_answer_dict[7][ans] = 1

                    #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #         filter = True
                    #     else:
                    #         per_answer_dict[7] = dict(sorted(per_answer_dict[7].items(), key=lambda item: item[1]))
                    #         if ans != list(per_answer_dict[7].keys())[-1]:
                    #             per_answer_dict[7][ans] += 1
                    #             ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #             filter = True                                

                else:
                    que = random.choice(temps1).replace("<R3>", rel).replace("<S>", obj1).replace("<S2>", obj3).replace("<S3>", obj2)
                    prog = "exist(filter(%s) and filter(%s(%s, %s)))"%(obj2, rel, obj1, obj3)
                    ans = True

                    ques.append({"question": que, "program": prog, "answer": ans, "template":10, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj3, obj2]})

                    # if not filter:
                    #     if not ans in per_answer_dict[7]:
                    #         per_answer_dict[7][ans] = 1

                    #         ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #         filter = True                                          
                    #     else:
                    #         per_answer_dict[7] = dict(sorted(per_answer_dict[7].items(), key=lambda item: item[1]))
                    #         if ans != list(per_answer_dict[7].keys())[-1]:
                    #             per_answer_dict[7][ans] += 1
                    #             ques.append({"question": que, "program": prog, "answer": ans, "template":2, "scene_id": scene_id, "family_id": [2]})   
                    #             filter = True 

        # if filter and count:
        #     break

                # if filter:
                #     break
                    
    # # print (ques)           

    # # further, closer

    rels = ['further', 'closer']
    temp = "Is the <S2> <R> to <S1> than <S3>?"  

    for rel in rels:
        if not rel in relationships: continue
        for pairs in relationships[rel]:
            ob1, ob2, ob3 = pairs

            for ob in objects:
                if ob['id'] == ob1:
                    obj1 = ob['class_name']
                if ob['id'] == ob2:
                    obj2 = ob['class_name']
                if ob['id'] == ob3:
                    obj3 = ob['class_name']
            

            if obj_count[obj1] == 1 and obj_count[obj2] == 1 and obj_count[obj3] == 1:
                que = temp.replace("<R>", rel).replace("<S1>", obj1).replace("<S2>", obj2).replace("<S3>", obj3)
                prog = "%s(distance(%s,%s), distance(%s,%s))"%(rel, obj1, obj2, obj1, obj3)
                ans = True

                ques.append({"question": que, "program": prog, "answer": ans, "template":12, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj1, obj2, obj3]})

                if rel == 'further':
                    rel2 = 'closer'
                else:
                    rel2 = 'further'
                
                que = temp.replace("<R>", rel2).replace("<S1>", obj1).replace("<S2>", obj2).replace("<S3>", obj3)
                prog = "%s(distance(%s,%s), distance(%s,%s))"%(rel2, obj1, obj2, obj1, obj3)
                ans = False

                ques.append({"question": que, "program": prog, "answer": ans, "template":12, "scene_id": scene_id, "family_id": [2], "concept": [rel2, obj1, obj2, obj3]})

#Verified
    rels = ['closer']
    temp = "Is the <S2> <R> to a <S1> than a <S3>?"  

    for rel in rels:
        if not rel in relationships: continue
        for pairs in relationships[rel]:
            ob1, ob2, ob3 = pairs

            for ob in objects:
                if ob['id'] == ob1:
                    obj1 = ob['class_name']
                    bbox = ob['bbox']
                    loc1 = [(bbox[0][0] + bbox[1][0]) / 2, (bbox[0][1] + bbox[1][1] / 2)]
                if ob['id'] == ob2:
                    obj2 = ob['class_name']
                if ob['id'] == ob3:
                    obj3 = ob['class_name']
            

            if obj_count[obj1] == 1:
                distances2 = []
                distances3 = []
                for ob2 in objects:
                    if ob2['class_name'] == obj2:
                        distances2.append(boxes_distance(np.array(ob2['bbox'][0][:2]), np.array(ob2['bbox'][1][:2]), np.array(ob['bbox'][0][:2]), np.array(ob['bbox'][1][:2])))
                        # bbox = ob['bbox']
                        # loc2 = [(bbox[0][0] + bbox[1][0]) / 2, (bbox[0][1] + bbox[1][1] / 2)]
                        # distances2.append((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)
                    if ob2['class_name'] == obj3:
                        distances3.append(boxes_distance(np.array(ob2['bbox'][0][:2]), np.array(ob2['bbox'][1][:2]), np.array(ob['bbox'][0][:2]), np.array(ob['bbox'][1][:2])))
                        # bbox = ob['bbox']
                        # loc2 = [(bbox[0][0] + bbox[1][0]) / 2, (bbox[0][1] + bbox[1][1] / 2)]
                        # distances3.append((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

                dist2 = np.min(np.array(distances2))
                dist3 = np.min(np.array(distances3))

                if abs(dist2 - dist3) < 0.4: continue

                rel = "closer"
                que = temp.replace("<R>", rel).replace("<S1>", obj2).replace("<S2>", obj1).replace("<S3>", obj3)
                prog = "%s(distance(%s,%s), distance(%s,%s))"%(rel, obj1, obj2, obj1, obj3)
                ans = bool(dist2 < dist3)

                ques.append({"question": que, "program": prog, "answer": ans, "template":13, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj2, obj1, obj3]})
    # print (ques)


#Verified
    temp = "How many <S>s are <R2> the <R> <S2>?"

    for rel in ['top', 'above', 'below', 'inside', 'close']:
        rel2 = rel
        if rel == 'close': rel2 = 'close to'
        if rel == 'top': rel2 = 'on top of '

        largest_dict = dict()
        smallest_dict = dict()

        if rel not in relationships: continue

        for pairs in relationships[rel]:
            for ob in objects:
                if ob['id'] == pairs[1]: obj1 = ob
                if ob['id'] == pairs[0]: obj2 = ob

            if obj_count[obj1['class_name']] != 1:
                if not obj1['class_name'] in largest_dict:
                    largest_dict[obj1['class_name']] = defaultdict(int)
                if not obj1['class_name'] in smallest_dict:
                    smallest_dict[obj1['class_name']] = defaultdict(int)

                objs = obj_ids[obj1['class_name']]
                # size = obj1["oriented_bbox"]["abb"]["sizes"][0] * obj1["oriented_bbox"]["abb"]["sizes"][1] * obj1["oriented_bbox"]["abb"]["sizes"][2] 
                size = (obj1['bbox'][1][0] - obj1['bbox'][0][0]) * (obj1['bbox'][1][1] - obj1['bbox'][0][1]) * (obj1['bbox'][1][2] - obj1['bbox'][0][2])

                sizes = []
                for obj in objs:
                    # sizes.append(objects[obj]["oriented_bbox"]["abb"]["sizes"][0] * objects[obj]["oriented_bbox"]["abb"]["sizes"][1] * objects[obj]["oriented_bbox"]["abb"]["sizes"][2])
                    sizes.append((objects[obj]['bbox'][1][0] - objects[obj]['bbox'][0][0]) * (objects[obj]['bbox'][1][1] - objects[obj]['bbox'][0][1]) * (objects[obj]['bbox'][1][2] - objects[obj]['bbox'][0][2]))
                sizes = np.array(sizes)           

                sizes = np.sort(sizes)
                  
                if not sizes[-1] / sizes[-2] > 1.5: continue
                if size == sizes[-1]:
                    largest_dict[obj1['class_name']][obj2['class_name']] += 1


                if not sizes[1] / sizes[0] > 1.5: continue
                if size == sizes[0]:
                    smallest_dict[obj1['class_name']][obj2['class_name']] += 1

        for obj1, dic in largest_dict.items():
            for obj2, cnt in dic.items():
                que = temp.replace("<S>", obj2).replace("<S2>", obj1).replace("<R2>", rel2).replace("<R>", "largest")
                ans = cnt

                ques.append({"question": que, "answer": ans, "template":14, "scene_id": scene_id, "family_id": [2], "concept": [rel, "largest", obj1, obj2]})

        for obj1, dic in smallest_dict.items():
            for obj2, cnt in dic.items():
                que = temp.replace("<S>", obj2).replace("<S2>", obj1).replace("<R2>", rel2).replace("<R>", "smallest")
                ans = cnt
                
                ques.append({"question": que, "answer": ans, "template":14, "scene_id": scene_id, "family_id": [2], "concept": [rel, "smallest", obj1, obj2]})
                         
#Verified
    temp = "How many <S>s are <R2> the <S2> <R> the <S3>?"

    for rel in ['top', 'above', 'below', 'inside', 'close']:
        rel2 = rel
        if rel == 'close': rel2 = 'close to'
        if rel == 'top': rel2 = 'on top of'

        closest_dict = dict()

        if rel not in relationships: continue

        for pairs in relationships[rel]:
            for ob in objects:
                if ob['id'] == pairs[1]: obj1 = ob
                if ob['id'] == pairs[0]: obj2 = ob

            if obj_count[obj1['class_name']] != 1:
                objs = obj_ids[obj1['class_name']]

                for obj3 in obj_count:
                    if not obj_count[obj3] == 1: continue
                    if not (obj1['class_name'], obj3) in closest_dict:
                        closest_dict[(obj1['class_name'], obj3)] = defaultdict(int)

                    obj3 = objects[obj_ids[obj3][0]]
                    sizes = []

                    # size = np.sum((np.array(obj1['bbox'][0][:2]) - np.array(obj3['bbox'][0][:2])) ** 2)
                    size = boxes_distance(np.array(obj3['bbox'][0][:2]), np.array(obj3['bbox'][1][:2]), np.array(obj1['bbox'][0][:2]), np.array(obj1['bbox'][1][:2]))

                    for ob in objs:
                        obj = objects[ob]

                        sizes.append(boxes_distance(np.array(obj3['bbox'][0][:2]), np.array(obj3['bbox'][1][:2]), np.array(obj['bbox'][0][:2]), np.array(obj['bbox'][1][:2])))

                    sizes = np.array(sizes)           

                    sizes = np.sort(sizes)
                  
                    if size == sizes[0] and sizes[1] / sizes[0] > 1.5:
                        closest_dict[(obj1['class_name'], obj3['class_name'])][obj2['class_name']] += 1

        for obj1, dic in closest_dict.items():
            for obj2, cnt in dic.items():
                obj, obj3 = obj1[0], obj1[1]
                que = temp.replace("<S>", obj2).replace("<S2>", obj).replace("<R2>", rel2).replace("<R>", "closest").replace("<S3>", obj3)
                ans = cnt

                ques.append({"question": que, "answer": ans, "template":15, "scene_id": scene_id, "family_id": [2], "concept": [rel, obj, obj2, obj3]})

#Verified
    temp = "Is there a <S> <R2> the <S2> with <S3> <R>?"

    for rel in ['top', 'above', 'below', 'inside', 'close']:
        rel2 = rel

        if rel == 'top': rel2 = 'on top'

        if rel not in relationships: continue

        rel_dict = dict()
        for pairs in relationships[rel]:
            

            for ob in objects:
                if ob['id'] == pairs[1]: obj2 = ob
                if ob['id'] == pairs[0]: obj3 = ob

            if not ((obj2['class_name'], obj3['class_name']) in rel_dict):
                rel_dict[(obj2['class_name'], obj3['class_name'])] = []
            
            if not obj2 in rel_dict[(obj2['class_name'], obj3['class_name'])]:
                rel_dict[(obj2['class_name'], obj3['class_name'])].append(obj2)
        
        for key, value in rel_dict.items():
            if len(value) != 1: continue
            obj2 = value[0]
            obj3 = key[1]

            for rel3 in relationships:
                if not rel3 in ['top', 'above', 'below', 'inside', 'close']: continue
                rel4 = rel3
                if rel3 == 'close': rel4 = 'close to'
                if rel3 == 'top': rel4 = 'on top of'  

                cnt_dict = dict()

                for pairs in relationships[rel3]:
                    for ob in objects:
                        if ob['id'] == pairs[0]: obj1 = ob

                    if not obj1['class_name'] in cnt_dict:
                        cnt_dict[obj1['class_name']] = 0

                    if not pairs[1] == obj2['id']: continue
                    
                    cnt_dict[obj1['class_name']] += 1

                for obj1 in cnt_dict:
                    if obj1 == obj3 or obj2['class_name'] == obj3 or obj1 == obj2['class_name']:
                        continue
                    que = temp.replace("<S>", obj1).replace("<S2>", obj2['class_name']).replace("<S3>", obj3).replace("<R2>", rel4).replace("<R>", rel2)
                    ans = bool(cnt_dict[obj1] > 0)

                    ques.append({"question": que, "answer": ans, "template": 16, "concept": [obj1, obj2['class_name'], obj3, rel3, rel], "scene_id": scene_id})

    for (k,que) in enumerate(ques):
        ques[k]["room_type"] = "single_room"

    with open("new_all_questions/%s"%scene_id, "w") as f1:
        json.dump(ques, f1)                