import json
import sys
import re
from operator import add
import numpy as np

class WasteMetric:
    """Calculates waste metric and makes one swap two swap recommendations for a given file"""


    def isInvalid(self,d):
        """Determines whether a list of strings is valid or not"""
        validBatch = {'10C','10D','10H','10S', '2C', '2D', '2H', '2S', '3C', '3D',
                      '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C',
                      '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                      '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH',
                      'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS'}


        if(len(d) != 52 or validBatch != set(d)):
            return True
        else:
            return False

    def wmDiff(self, s1, s2):
        """Calculates the waste difference between two strings"""
        baseDiff = (abs(int(s1[0:-1]) - int(s2[0:-1])))
        reds = {'H', 'D'}
        blacks = {'S', 'C'}
        if(s1[-1] == s2[-1]):
            return baseDiff
        elif((s1[-1] in reds and s2[-1] in reds)
             or
             (s1[-1] in blacks and s2[-1] in blacks)):
            return 2*baseDiff
        else:
            return 3*baseDiff

    def listWasteMetric(self, lst):
        """Converts alphabets like AJQK to their corresponding ranks and calculates the waste difference"""
        wm = []
        ranked = list(map(lambda x:re.sub('[JQK]', '10', x), lst))
        ranked = list(map(lambda x:re.sub('A', '1', x), ranked))
        ranked2 = ranked[1:]
        ranked2.append(ranked[-1])
        zpd = list(zip(ranked, ranked2))
        wm = [self.wmDiff(t[0], t[1]) for t in zpd]
        return (ranked, wm)

    def oneSwap(self,lst):
        """Returns all the values needed for a one swap recommendation"""
        ranked, wm = self.listWasteMetric(lst)
        wm2 = wm[1:]
        wm2.append(wm[-1])
        wm3 = list(map(add,wm,wm2))
        mx_indx = np.argmax(wm3)

        min_wm_sum = 100000000
        min_wm = []
        min_tmp_list = []

        swap1 = ranked[mx_indx+1]
        swap2 = ""
        for i in range(len(lst)):
            tmp_lst = lst.copy()
            tmp_lst[i] = ranked[mx_indx+1]
            tmp_lst[mx_indx+1] = lst[i]
            _, tmp_wm = self.listWasteMetric(tmp_lst)
            waste = sum(tmp_wm)
            if waste < min_wm_sum:
                min_wm_sum = waste
                min_tmp_list = tmp_lst
                swap2 = lst[i]
                min_wm = tmp_wm

        return (min_tmp_list, wm, min_wm_sum, swap1, swap2)

    def twoSwap(self, lst):
        """Returns all the values needed for a two swap recommendation"""
        ranked, wm, min_wm_sum, swap1, swap2 = self.oneSwap(lst)
        _, _,       min_wm_sum_2, swap3, swap4 = self.oneSwap(ranked)
        return (swap1, swap2, swap3, swap4 , sum(wm), min_wm_sum_2)



def main():
    wmObj = WasteMetric()

    with open(sys.argv[2],'r') as f:
        d=json.load(f)
        if(sys.argv[1] == "is-invalid-batch"):
            invld = wmObj.isInvalid(d)
            if invld:
                print(f"{sys.argv[2]} is INVALID")
            else:
                print(f"{sys.argv[2]} is VALID")
        elif(sys.argv[1] == "waste-metric"):
            _, wm = wmObj.listWasteMetric(d)
            print(f"Waste metric for batch {sys.argv[2]} is {sum(wm)}")
        elif(sys.argv[1] == "one-swap-recommendation"):
            _, wm, min_wm_sum, swap1, swap2 = wmObj.oneSwap(d)
            print(f'By swapping {swap1} and {swap2}, you could reduce waste metric from {sum(wm)} to {min_wm_sum}.')
        elif(sys.argv[1] == "two-swap-recommendation"):
            swap1, swap2, swap3, swap4 , wm_sum, min_wm_sum_2 = wmObj.twoSwap(d)
            print(f'By swapping {swap1} and {swap2}, then swapping {swap3} and {swap4}, you could reduce waste metric from {wm_sum} to {min_wm_sum_2}.')

if  __name__ =='__main__':main()
