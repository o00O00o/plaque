import os
import json
import numpy as np
import matplotlib.pyplot as plt
from utils import set_seed
from datasets import process_label


if __name__ == "__main__":
    seed = 57
    set_seed(57)
    data_path = '/Users/gaoyibo/Datasets/plaque_data_whole_new'

    case_list = sorted(os.listdir(data_path))  # 病例列表
    case_list = [os.path.join(data_path, case) for case in case_list]

    try:
        with open('failed_branches.json', 'r') as f:
            json_dict = json.load(f)
            failed_branch_list = json_dict['failed_branches']  # 没有通过检测的branch
            print('failed branch num in the dataset: {}'.format(len(failed_branch_list)))
    except IOError:
        print('failed_branches.json not found.')

    branch_dict = {}
    for case_path in case_list:
        branch_list = os.listdir(case_path)
        for branch_id in branch_list:
            branch_path = os.path.join(case_path, str(branch_id))

            if branch_path in failed_branch_list:  # 排除没有通过检测的branch
                continue

            json_path = os.path.join(branch_path, 'plaque.json')

            try:
                with open(json_path, 'r') as f:
                    dict = json.load(f)
                    if len(dict['plaques']) != 0:  # 如果相应branch不是正常的，则得到segmentlabel
                        branch_dict[branch_path] = process_label(dict['plaques'])
            except IOError:
                print("plaque json file not found.")

    seg_len_list = []
    for value in list(branch_dict.values()):
        for item in value:
            seg_len_list.append(len(item[1]))

    seg_len_list = np.array(sorted(seg_len_list))
    print('max plaque seg length: ' + str(seg_len_list.max()))  # 107
    print('min plaque seg length: ' + str(seg_len_list.min()))  # 2
    print('avg plaque seg length: ' + str(seg_len_list.mean()))  # 16.6
    print('std plaque seg length: ' + str(seg_len_list.std()))  # 12.6

    unique, counts = np.unique(seg_len_list, return_counts=True)
    plt.bar(unique, counts)
    plt.show()
