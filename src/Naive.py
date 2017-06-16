#!/usr/bin/env python3

import data_parser as dp
import gen_len as gl
import argparse 
from math import ceil
import numpy as np

FLAG = None

def average_over_num(feat):

    np_feat = np.reshape(np.array(feat),(-1,FLAG.feat_dim))
    
    ave_num = len(np_feat)
    # print (ave_num)
    sum_up = np.sum(np_feat, axis=0)
    ave = np.divide(sum_up, ave_num)
    k = ave.tolist()
    # print (len(k))

    return ave.tolist()

def naive_encoder(feats, lens):

    NE_feats = []
    dim = FLAG.feat_dim
    for i, feat in enumerate(feats):
        NE_single_feat = []
        single_len = lens[i] 
        one_third = int(ceil(float(single_len)/3))
        two_third =  2*one_third
        NE_single_feat.extend(average_over_num(feat[:one_third*dim]))
        NE_single_feat.extend(average_over_num(feat[one_third*dim:
                                                    two_third*dim]))
        NE_single_feat.extend(average_over_num(feat[two_third*dim:single_len*dim]))
        NE_feats.append(NE_single_feat)
        if dim *3 != len(NE_single_feat):
            print (len(NE_single_feat))
            print ("dimension not the same")
            break
    return NE_feats

def apply_NE(fn):
    '''
    return:
      feats: the feature list
      lab: the label list
    '''
    feats, labs = dp.read_csv_file(fn, delimiter=',')
    lens = gl.gen_len(feats)
    transed_feats = naive_encoder(feats,lens)

    return transed_feats, labs


def main():
    file_list = []
    with open(FLAG.file_scp,'r') as f:
        for line in f:
            file_list.append(line.rstrip())
    
    for i in file_list:
        feat_dic = {}
        feats, labs = apply_NE(i)
        for i, lab in enumerate(labs):
            if lab not in feat_dic:
                feat_dic[lab] = []
            feat_dic[lab].append(feats[i])
        dp.write_feat_in_lab_name(feat_dic,FLAG.out_dir)

    return     

def parse_opt():
    parser = argparse.ArgumentParser(
        description='The naive encoder with concatenation of '
        'front 1/3, mid 1/3 , end 1/3')
    parser.add_argument('file_scp',
        metavar='<the file scp>',
        help='The list of file pointers')
    parser.add_argument('out_dir',
        metavar='<the output directory>',
        help='The output directory')
    parser.add_argument('--feat_dim',type=int,default=39,
        metavar='<--feature dimension>',
        help='The feature dimension')
    return parser


if __name__ == '__main__':
    parser = parse_opt()
    FLAG = parser.parse_args()
    gl.FLAG = FLAG
    main()