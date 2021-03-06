import json
import os
import sys
from glob import glob
from myhmm2order import MyHmm
import random
import numpy as np


def create_param_dict():
    pmat = np.load('../ctfiles/probmat.npy')
    print(pmat)
    #output = {}
 
    model = {'A':{}, 'B':{}, 'pi':{}}
    states = ['UU', 'UP', 'PU', 'PP']
    # setting up model['A']
    for i in range(4):
        key = states[i]
        model['A'][key] = {}
        for j in range(4):
            subkey = states[j]
            model['A'][key][subkey] = pmat[i][j]
            #model['A'][key][subkey] = 0.25

    print('model["A"]')
    print(model['A'])


    emat = np.load('../ctfiles/emprobmat.npy')
    print(emat)
    states2 = ['AA','AC','AG','AU','CA','CC','CG','CU','GA','GC','GG','GU','UA','UC','UG','UU']
    for i in range(4):
        key = states[i]
        model['B'][key] = {}
        for j in range(16):
            subkey = states2[j]
            model['B'][key][subkey] = emat[i][j]
            #model['B'][key][subkey] = 0.0625

    print('model["B"]')
    print(model['B'])


    for i in range(4):
        key = states[i]
        model['pi'][key] = 0.25
        #auxpi = [1,0,0,0]
        #model['pi'][key] = auxpi[i]

    print('model["pi"]')
    print(model['pi'])

    return model
    

def valid_sequence(s):
    if any([c not in ['A', 'C', 'G', 'U'] for c in s]):
        return False
    return True


def get_array(fname):
    sequence = []
    hidden_sequence = []
    f = open('../ctfiles/processed_data/{}.ct'.format(fname), "r")
    if f.mode == "r":
        for line in f:
            arr = line.split()
            for i in range(len(arr[0])):
                    sequence.append(arr[0])
                    hidden_sequence.append(int(arr[1]))
    f.close()

    if not valid_sequence(sequence): return []

    output = []
    i = 0
    while i<len(sequence)-1:
        output.append(sequence[i]+sequence[i+1])
        i = i+2

    return output, hidden_sequence


def main():
    observation_list = []
    actual_hidden_states = []
    fnames = glob('../ctfiles/processed_data/*.ct')
    fnames_list = []
    for fname in fnames[0:16]:

    #for fname in np.random.choice(fnames, 16, replace= False):
    #for fname in fnames[0:1]:

    #for i in np.random.permutation(len(fnames)):
    #    fname = fnames[i]

        print(fname)
        fnames_list.append(fname)
        pfname = fname[26:-3]
        sequence, actual_hidden_state = get_array(pfname)
        
        if len(sequence)>0:

            observation_list.append(sequence)
            #sequence = get_array(pfname, col=1)
            actual_hidden_states.append(actual_hidden_state)

        if len(observation_list)==16: break

    assert len(actual_hidden_states) == len(observation_list)

    #models_dir = os.path.join('.', 'models')
    # sequences

#if __name__ == '__main__':

    model = create_param_dict()

    hmm = MyHmm(model)
    total1 = total2 = 0 # keep tarck of total prob sum to 1
    for iobs,obs in enumerate(observation_list):
        print('\ntraining model on data in file: {}'.format(fnames_list[iobs]))
        p1 = hmm.forward(obs)
        p2 = hmm.backward(obs)
        total1 += p1
        total2 += p2
        print ("Observations = ", obs, " Fwd Prob = ", p1, " Bwd Prob = ", p2, " total_1 = ", total1, " total_2 = ", total2)



    #for i in range(len(observation_list)):
        prob, hidden_state = hmm.viterbi(obs)
        print ("Max Probability = ", prob, "hidden state sequence", hidden_state)

        hidden_array = []
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for i in range(len(hidden_state)):
            string_pairings = hidden_state[i]
            for j in range(len(string_pairings)):
                if string_pairings[j] == 'P':
                    hidden_array.append(1)
                else:
                    hidden_array.append(0)

        print('hidden state is now 1s and 0s')
        print(hidden_array)

        actual_hidden_state = actual_hidden_states[iobs]
        print('actual state ')
        print(actual_hidden_state)

        for j in range(len(hidden_array)):
            if hidden_array[j] == 1 and actual_hidden_state[j] == 1:
                tp += 1
            elif hidden_array[j] == 1 and actual_hidden_state[j] == 0:
                fp += 1
            elif hidden_array[j] == 0 and actual_hidden_state[j] == 1:
                fn += 1
            else:
                tn += 1

        assert tp + fp + fn + tn == len(hidden_array)

        print('tp, fp, fn, tn', tp, fp, fn, tn)
        print("Acc: ", 1.0*(tp+tn)/(tp+fp+fn+tn))
        print("Sen: ", 1.0*tp/(tp+fn))
        print("PPV: ", 1.0*tp/(tp+fp))

  




    



main()
#create_param_dict()



