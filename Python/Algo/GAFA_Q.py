"""Given an array A and an integer target, 
    find the indices of the two numbers in the array
    whose sum is equal to the given target."""
given_nums = [2, 7, 11, 15]
target = 9

#pour recherche : dictionnaire et tables de Hash 
"""--> répeter : est ce que target-t[i]=x est dans dico ? 
    Si  non ajouter t[i] au dico avec so indice et Si oui ok"""
    
def two_sums(nums,target):
    num_map={}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in num_map:
            return (num_map[complement], i)
        num_map[nums[i]]=i
    return None
print(two_sums(given_nums,target))