import numpy as np

def main():
    a1 = str([[[1, 1, 1, 1], [1, 1, 1, 1]]])
    a2 = str([[[2, 2, 2, 2], [2, 2, 2, 2]], [[2, 2, 2, 2], [2, 2, 2, 2]]])
    a3 = str([[[3, 3, 3, 3], [3, 3, 3, 3]]])
    a4 = str([[[4, 4, 4, 4], [4, 4, 4, 4]]])
    a5 = str([[[5, 5, 5, 5], [5, 5, 5, 5]]])
    a6 = str([[[6, 6, 6, 6], [6, 6, 6, 6]]])
    a7 = str([[[7, 7, 7, 7], [7, 7, 7, 7]]])

    #c= [a1,a2,a3,a4,a5,a6,a7]
    c = [a1,a2,a3,a4,a5,a6,a7]
    f=open('same_scene_masks.txt','w')
    # c=map(lambda x:x+'\n', c)
    for elem in c:
        f.writelines(elem)
        f.writelines('\n')
    f.close()

    # # how to get the masks line by line:
    # import ast
    # a_file = open("same_scene_masks.txt", "r")
    # list_of_lists = []
    # for line in a_file:
    #     original_list = ast.literal_eval(line)
    #     list_of_lists.append(original_list)
    #
    # a_file.close()



if __name__ == "__main__":
    main()