
import re

from ucca import layer0, layer1, convert, core
from xml.etree.ElementTree import ElementTree, tostring, fromstring
import sys
import operator
import numpy as np
import pickle
import argparse



def get_Hscenes(P):
    """
    P is a ucca passage. Return all the Hscenes in each passage
    """
    nodes = [x for x in P.layer("1").all if x.tag == "FN"]
    H = []
    for n in nodes:
        Hscenes = [e.child for e in n.outgoing if e.tag == 'H' and e.child.is_scene()]
        #Hscenes = [e.child for e in n.outgoing if e.tag == 'H']
        if Hscenes != []:
            H.append(Hscenes)
    H = sum(H,[])
    #print(H)
    y = P.layer("0")
    output = []
    pos_output= []
    for sc in H:
        p = []
        d = sc.get_terminals(False,True)
        for i in list(range(0,len(d))):
            p.append(d[i].position)
        output2 = []
        pos_output2 = []
        for k in p: #TODO: ask Elior: if I want just the position of the word, and not the word itself (to deal with duplicate words) - cab I use just p?
            if(len(output2)) == 0:
                output2.append(str(y.by_position(k)))
                pos_output2.append(k)
            elif str(y.by_position(k)) != output2[-1]: # TODO: ask Elior: why this elif?
                output2.append(str(y.by_position(k)))
                pos_output2.append(k)
        output.append(output2)
        pos_output.append(pos_output2)

    return output, pos_output

def get_EAscenes(P):
    """
    P is a ucca passage. Return all the Escenes and Ascenes in each passage and their corresponding minimal center
    """
    nodes = [x for x in P.layer("1").all if x.tag == "FN"]
    E = []
    C = []
    for n in nodes:
        EAscenes = [e.child for e in n.outgoing if (e.tag == 'E' or e.tag == 'A') and e.child.is_scene()]
        Escenes = [e.child for e in n.outgoing if e.tag == 'E' and e.child.is_scene()]
        Ascenes = [e.child for e in n.outgoing if e.tag == 'A' and e.child.is_scene()]
        if EAscenes != []:
            E.append(EAscenes)
            for pa in EAscenes:
                if pa in Escenes:
                    centers = [e.child for e in n.outgoing if e.tag == 'C' ]# find the minimal center
                    if centers != []:
                        while centers != []:
                            for c in centers:
                                ccenters = [e.child for e in c.outgoing if e.tag == 'C']
                            lcenters = centers
                            centers = ccenters
                        C.append(lcenters)
                    else:
                        C.append(['*'])
                elif pa in Ascenes:
                    scenters = [e.child for e in pa.outgoing if e.tag == 'P' or e.tag == 'S']
                    for scc in scenters:
                        centers = [e.child for e in scc.outgoing if e.tag == 'C']
                        if centers != []:
                            while centers != []:
                                for c in centers:
                                    ccenters = [e.child for e in c.outgoing if e.tag == 'C']
                                lcenters = centers
                                centers = ccenters
                            C.append(lcenters)
                        else:
                            C.append(scenters)





    E = sum(E,[])
    C = sum(C,[])
    y = P.layer("0")
    output1 = []
    center = []
    pos_output1=[]
    pos_center = []

    for sc in E:
        p = []
        d = sc.get_terminals(False,True)
        for i in list(range(0,len(d))):
            p.append(d[i].position)
        output2 = []
        pos_output2 = []
        for k in p:
            if(len(output2)) == 0 or str(y.by_position(k)) != output2[-1]:
                output2.append(str(y.by_position(k)))
                pos_output2.append(k)

        output1.append(output2)
        pos_output1.append(pos_output2)

        #W = ['who','which','that']
        #for v in output1:
        #   u = [ z for z in v if z not in W ]
        #  output.append(u)

    for c in C:
        if c!= '*':
            p = []
            d = c.get_terminals(False,True)
            for i in list(range(0,len(d))):
                p.append(d[i].position)
            output3 = []
            pos_output3 = []
            for k in p:
                if(len(output3)) == 0 or str(y.by_position(k)) != output3[-1]:
                    output3.append(str(y.by_position(k)))
                    pos_output3.append(k)
            center.append(output3)
            pos_center.append(pos_output3)
        else:
            center.append(c)
            pos_center.append([-1]) #TODO: change here also pos_center.append(...)  - ask Elior what is the meaning of c=='*'

    return([output1,center, pos_output1, pos_center])




def get_difference(h1,L2,C2, pos_h1, pos_L2, pos_C2):
    """
    h1 is the parallel Scene (string), L2 is the list of embedded Scenes (string), C2 is the list of string centers.
    For each (l2,c2) in (L2,C2), recursively return L1+c2 without l2 and then l2.
    """
    E2 = []
    pos_E2 = [] # TODO: AVIVSL: added this line

    for c2 in C2:
        if c2 == '*':
            c2 = [['#']]*len(h1) #TODO: ask Elior: what is done here? I seemw like it is not used anywhere... and do something parallel
            pos_c2 = [[-2]]*len(pos_h1) #TODO: AVIVSL: added my code here
    #print(C2)

    for l2 in L2:
        j = L2.index(l2)
        #print(j)
        #print(l2)

        f = []

        if l2 != []:
            for m in range(0,len(h1)):
                if h1[m:m+len(l2)] == l2:
                    f.append([m,len(l2)])

        diff = []
        for i in f:
            d = list(range(i[0],i[0]+i[1]))
            diff.append(d)
        #print(h1)
        #print(diff)

        if diff != []:
            split2 = [element for i, element in enumerate(h1) if i not in diff[0] or element in C2[j]]
            h1 = split2
            # try:
            pos_split2 = [element for i, element in enumerate(pos_h1) if i not in diff[0] or element in pos_C2[j]] # TODO: AVIVSL: added this line
            # except:
            #     print("gotcha")
            pos_h1 = pos_split2 # TODO: AVIVSL: added this line
        else:
            split2 = h1
            pos_split2 = pos_h1 # TODO: AVIVSL: added this line

        m2 = []
        pos_m2 = []  # TODO: AVIVSL: added this line

        W = ['who','which','that'] #TODO: ask Elior - why not also "whose", "where", "when", how, what, why
        u = [ z for z in L2[j] if z not in W ]
        m2.append(u)

        pos_u = [pos_L2[j][index] for index in list(range(len(L2[j]))) if L2[j][index] not in W]  # TODO: AVIVSL: added this line
        pos_m2.append(pos_u) # TODO: AVIVSL: added this line


        if  m2 != [] and diff!=[]:
            E2.append(m2)
            pos_E2.append(pos_m2)  # TODO: AVIVSL: added this line

        asplit2 =[]
        asplit2.append(split2)

        pos_asplit2 =[] # TODO: AVIVSL: added this line
        pos_asplit2.append(pos_split2) # TODO: AVIVSL: added this line


    if L2 != []:
        E2 = sum(E2,[])
        pos_E2 = sum(pos_E2,[]) # TODO: AVIVSL: added this line
        for e in E2:
            asplit2.append(e)
        for e in pos_E2: # TODO: AVIVSL: added this line
            pos_asplit2.append(e) # TODO: AVIVSL: added this line

    else:
        asplit2 = [h1]
        pos_asplit2 = [pos_h1]  # TODO: AVIVSL: added this line

    return asplit2, pos_asplit2 # TODO: AVIVSL: updated this line

def get_passage(P):
    """
   P is a ucca passage. Return the passage as a string.
    """
    root = [x for x in P.layer("1").all if x.tag == "FN" and x.fparent == None]
    #R = []
    #for n in nodes:
    #    root = [e.child for e in n.incoming if e.parent == None]
    #    if root !=[]:
    #       R.append(root[0])
    y = P.layer("0")
    p = []
    d = root[0].get_terminals(False,True)
    for i in list(range(0,len(d))):
        p.append(d[i].position)
    output = []
    for k in p:
        if(len(output)) == 0:
            output.append(str(y.by_position(k)))
        elif str(y.by_position(k)) != output[-1]:
            output.append(str(y.by_position(k)))
    return(output)

def to_word_text(P):
    """Converts from a Passage object to tokenized strings.
    """

    tokens = [x.text for x in sorted(P.layer(layer0.LAYER_ID).words, key=operator.attrgetter('position'))]

    starts = [0, len(tokens)]
    return [' '.join(tokens[starts[i]:starts[i + 1]])
            for i in range(len(starts) - 1)]


def create_same_scene_map_unseg(pos_S1, sent_len):
    same_scene_matrix = np.identity(sent_len)
    for scene in pos_S1:
        for i, elem_i in enumerate(scene):
            for j, elem_j in enumerate(scene[i:]):
                same_scene_matrix[elem_i - 1, elem_j - 1] = 1
                same_scene_matrix[elem_j - 1, elem_i - 1] = 1
    return same_scene_matrix

def create_segments_to_origin_map(sent, origin_sent_len):
    split_sent = sent.split()
    seg_to_origin_map = np.zeros([len(split_sent), origin_sent_len])
    cnt=0
    for i,elem in enumerate(split_sent):
        seg_to_origin_map[i,cnt] = 1
        if not elem.endswith("@@"):
            cnt+=1
    return seg_to_origin_map


def create_same_scene_map_final(xml_string, seg_sentence):
    print("started!")
    xml_object1 = fromstring(xml_string)
    P1 = convert.from_standard(xml_object1)
    L1, pos_L1 = get_Hscenes(P1)
    L2, C2, pos_L2, pos_C2 = get_EAscenes(P1)

    split12 = []
    pos_split12 = []

    sent_len = len([P1.nodes[node] for node in P1.nodes if type(P1.nodes[node]) is layer0.Terminal])
    if L1:
        for i,h in enumerate(L1):
            D1, pos_D1 = get_difference(h, L2, C2, pos_L1[i], pos_L2, pos_C2) # TODO: AVIVSL: updated this line
            split12.append(D1)
            pos_split12.append(pos_D1) # TODO: AVIVSL: added this line
    
        pos_S1 = sum(pos_split12, [])
        same_scene_unseg_map=create_same_scene_map_unseg(pos_S1, sent_len)
    else:
        pos_non_puncts = [(P1.nodes[node].position - 1) for node in P1.nodes if
                      type(P1.nodes[node]) is layer0.Terminal and P1.nodes[node].tag != 'Punctuation']
        same_scene_unseg_map = np.identity(sent_len)
        pos_non_punct_combos = [(a, b) for a in pos_non_puncts for b in pos_non_puncts]
        for combo in pos_non_punct_combos:
            same_scene_unseg_map[combo] = 1

    segmented_to_origin_map = create_segments_to_origin_map(seg_sentence, sent_len)
    same_scene_seg_map = np.matmul(segmented_to_origin_map, same_scene_unseg_map)
    same_scene_seg_map = np.matmul(same_scene_seg_map, np.transpose(segmented_to_origin_map))
    print("finished!")
    # if np.array_equal(same_scene_seg_map ,segmented_to_origin_map):
    #     print("gotcha")
    return str(same_scene_seg_map.tolist())



def main(args):
    ucca_file_path = args.ucca_file #r"/cs/snapless/oabend/lovodkin93/encoder_masking/de-en/same_scene_masks_scripts/ucca_trees/ucca_trees_3_sentences.txt"
    outdir_path = args.outdir #r"same_scene_maps/same_scene_maps.txt"
    seg_sent_file_path = args.seg_sent_file
    f1 = open(ucca_file_path, 'r', encoding='utf-8')
    xmls = f1.read().splitlines()
    xmls = [xml for xml in xmls if xml]
    f1.close()
    f2 = open(seg_sent_file_path, encoding='utf-8')
    seg_sentences = f2.read().splitlines()
    seg_sentences = [seg_sentence for seg_sentence in seg_sentences if seg_sentence]
    f2.close()
    
    import pathos.pools as pp
    p = pp.ProcessPool(1)
    same_scene_maps = p.map(create_same_scene_map_final, xmls, seg_sentences)

    f3 = open(outdir_path, 'w')
    for ss_map in same_scene_maps:
        f3.writelines(ss_map)
        f3.writelines('\n')
    f3.close()
    print("done!")


    # xml_object1 = fromstring(xml_string1)
    # P1 = convert.from_standard(xml_object1)
    # L1, pos_L1 = get_Hscenes(P1)
    # L2, C2, pos_L2, pos_C2 = get_EAscenes(P1)
    # 
    # split12 = []
    # pos_split12 = []
    # for i,h in enumerate(L1):
    #     D1, pos_D1 = get_difference(h, L2, C2, pos_L1[i], pos_L2, pos_C2) # TODO: AVIVSL: updated this line
    #     split12.append(D1)
    #     pos_split12.append(pos_D1) # TODO: AVIVSL: added this line
    # 
    # pos_S1 = sum(pos_split12, [])
    # sent_len = len([ P1.nodes[node] for node in P1.nodes if type( P1.nodes[node]) is layer0.Terminal])
    # same_scene_unseg_map=create_same_scene_map_unseg(pos_S1, sent_len)
    # segmented_to_origin_map=create_segments_to_origin_map(seg_sentence, sent_len)
    # 
    # same_scene_seg_map = np.matmul(segmented_to_origin_map, same_scene_unseg_map)
    # same_scene_seg_map = np.matmul(same_scene_seg_map, np.transpose(segmented_to_origin_map))
    # print("done!")





if __name__ == "__main__":
    desc = "generate same_scene_masks of sentences"
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("--ucca-file", help="path to file with UCCA graphs")
    argparser.add_argument("--seg-sent-file", help="path to file with segmented sentences")
    argparser.add_argument("-o", "--outdir", default=".", help="output file text path")

    main(argparser.parse_args())