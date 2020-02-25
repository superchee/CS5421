########################################################################################
## project2.py - Code template for Project 2 - Functional Dependencies and Normalization 
########################################################################################

## If you need to import library put it below
import copy
import itertools

## Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
    unused_F = copy.copy(F)
    S_closure = copy.copy(S)

    while len(unused_F) > 0:
        bFind = False 
        unused_F_copy = copy.copy(unused_F)
        for per in unused_F:
            if set(per[0]).issubset(S_closure): #add the attributes if X in closure
                S_closure += list( set(per[1]) - set(S_closure) )
                unused_F_copy.remove(per)
                bFind = True
                break
        if bFind == False:
            break #break when no more attributes can be found
        unused_F = copy.copy(unused_F_copy)
    return sorted(S_closure)

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 

    all_closure = []
    candidate_keys = []

    for i in range(1,len(R)+1):
        for itr in list(itertools.combinations(R,i)):
            #check superkeys that are not candidate keys
            if any(set(perList).issubset(list(itr)) for perList in candidate_keys ):
                continue
            temp_closure = closure(R,F,list(itr))
            all_closure.append([list(itr),temp_closure])
            #find candidate keys
            if(len(temp_closure) == len(R)):
                candidate_keys.append(list(itr))
    return sorted(all_closure)
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    #simplify the right hand side
    L_rhs_minimal = simplifyRHS(R, FD)

    #simplify the left hand side (change this part for all minimal covers)
    L_lhs_minimal = simplifyLHS(R, FD, L_rhs_minimal)
    #remove duplicate fd
    #L_lhs_minimal.sort()
    #L_minimal = list(L_lhs_minimal for L_lhs_minimal,_ in itertools.groupby(L_lhs_minimal))

    #simplify the set itself by removing fd that can be derived from the others
    L_minimal = simplifySelf(R,FD,L_lhs_minimal)

    return L_minimal

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.
    '''
    #simplify the right hand side
    L_rhs_minimal = simplifyRHS(R, FD)

    #simplify the left hand side (for each lhs keep all the possible simplified results)
    L_lhs_minimal_o = simplifyLHSALL(R, FD, L_rhs_minimal)

    L_lhs_minimal_o_RD = removeDuplicate2(L_lhs_minimal_o)

    #Cartesian product
    L_lhs_minimal_all = []
    for per in itertools.product(*L_lhs_minimal_o_RD):
        L_lhs_minimal_all.append(list(per))


    #simplify each set itself by removing fd that can be derived from the others
    L_minimal_covers = []

    # for per in L_lhs_minimal_all:
    #     L_minimal_covers.append(simplifySelf(R,FD,per))

    L_lhs_minimal_all_sim = removeDuplicate2(L_lhs_minimal_all)

    for per in L_lhs_minimal_all_sim:
        L_temp = simplifySelfAll(R,FD,per)
        for el in L_temp:
            L_minimal_covers.append(el)

    #remove the duplicate minimal cover
    L_minimal = removeDuplicate2(L_minimal_covers)


    return L_minimal

## Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.
    '''
    #get the closure
    FD_plus = all_closures_self(R,FD)

    #simplify the right hand side
    L_rhs_minimal = simplifyRHS(R, FD_plus)

    #simplify the left hand side (for each lhs keep all the possible simplified results)
    L_lhs_minimal_o = simplifyLHSALL(R, FD_plus, L_rhs_minimal)


    #L_lhs_minimal_o_RD = removeDuplicate(L_lhs_minimal_o)

    #Cartesian product
    L_lhs_minimal_all = []
    for per in itertools.product(*L_lhs_minimal_o):
        temp = removeDuplicate1(list(per))
        L_lhs_minimal_all.append(temp)


    #simplify each set itself by removing fd that can be derived from the others
    L_minimal_covers = []

    # for per in L_lhs_minimal_all:
    #     L_minimal_covers.append(simplifySelf(R,FD,per))

    L_lhs_minimal_all_sim = removeDuplicate2(L_lhs_minimal_all)

    for per in L_lhs_minimal_all_sim:
        L_temp = simplifySelfAll(R,FD,per)
        for el in L_temp:
            L_minimal_covers.append(el)


    #remove the duplicate minimal cover
    L_minimal = removeDuplicate2(L_minimal_covers)

    return L_minimal

## You can add additional functions below

def simplifyRHS(R, FD):
    L_rhs_minimal = []
    for fd in FD:
        lhs = fd[0]
        rhs = fd[1]
        if (len(rhs) > 1):
            for atr in rhs:
                if (not set(atr).issubset(lhs)):
                    L_rhs_minimal.append([lhs, list(atr)])
        else:
            if (not set(rhs).issubset(lhs)):
                L_rhs_minimal.append([lhs, rhs])
    return L_rhs_minimal

def simplifyLHS(R, FD, L_rhs_minimal):
    L_lhs_minimal = []
    for fd in L_rhs_minimal:
        lhs = fd[0]
        rhs = fd[1]
        if (len(lhs) == 1):
            L_lhs_minimal.append([lhs, rhs])
            continue
        bFind = False
        for i in range(1,len(lhs)+1):
            for itr in list(itertools.combinations(lhs,i)):
                if set(rhs).issubset(closure(R,FD,list(itr))):
                    bFind = True
                    L_lhs_minimal.append([list(itr), rhs])

                    break
            if (bFind):#break when find one simplified lhs
                break
        if(not bFind): L_lhs_minimal.append([lhs, rhs])
    return L_lhs_minimal

def simplifyLHSALL(R, FD, L_rhs_minimal):
    L_lhs_minimal = []
    for fd in L_rhs_minimal:
        lhs = fd[0]
        rhs = fd[1]
        temp = []
        if (len(lhs) == 1):
            L_lhs_minimal.append([[lhs, rhs]])
            continue
        bFind = False
        for i in range(1,len(lhs)+1):
            for itr in list(itertools.combinations(lhs,i)):
                if set(rhs).issubset(closure(R,FD,list(itr))):
                    bFind = True
                    if any(set(perList[0]).issubset(list(itr)) for perList in temp ):
                        continue
                    temp.append([list(itr), rhs])
        if(not bFind): 
            L_lhs_minimal.append([[lhs, rhs]])
        else:
            L_lhs_minimal.append(temp)
    return L_lhs_minimal

def simplifySelf(R, FD, L_minimal):
    i = 0
    while i < len(L_minimal):
        fd = L_minimal[i]
        lhs = fd[0]
        rhs = fd[1]
        L_temp = copy.copy(L_minimal)
        L_temp.remove(fd)
        if (set(rhs).issubset(closure(R,L_temp,lhs))):
            L_minimal.remove(fd)
            continue
        else:
            i = i + 1
    return L_minimal

    
def sublist(lst1, lst2):
    for per in lst2:
        if all(i in lst1 for i in per):
            return True
    return False

def simplifySelfAll(R, FD, L_minimal):

    closure_ori = sorted(all_closures_self(R, L_minimal))
    L_sim = []
    for i in range(1,len(L_minimal)):
        for itr in list(itertools.combinations(L_minimal,i)):
            temp_L = sorted(all_closures_self(R,list(itr)))
            if temp_L == closure_ori:
                if sublist(list(itr), L_sim):
                    continue 
                L_sim.append(list(itr))

    if len(L_sim) == 0:
        return L_minimal
    else:
        return L_sim

def all_closures_self(R, F): 

    all_closure = []
    candidate_keys = []

    for i in range(1,len(R)+1):
        for itr in list(itertools.combinations(R,i)):
            #check superkeys that are not candidate keys
            # if any(set(perList).issubset(list(itr)) for perList in candidate_keys ):
            #     continue
            temp_closure = closure(R,F,list(itr))
            all_closure.append([list(itr),temp_closure])
            #find candidate keys
            if(len(temp_closure) == len(R)):
                candidate_keys.append(list(itr))
    return sorted(all_closure)

def removeDuplicate1(L_minimal_covers):
    i = 0
    while i < len(L_minimal_covers):
        bFind = False
        m_cover = L_minimal_covers[i]
        for per in L_minimal_covers[i+1:]:
            if m_cover == per:
                bFind = True
                L_minimal_covers.remove(m_cover)
                break
        if bFind:
            continue
        else:
            i = i+1
    return L_minimal_covers

def removeDuplicate2(L_minimal_covers):
    i = 0
    while i < len(L_minimal_covers):
        bFind = False
        m_cover = L_minimal_covers[i]
        for per in L_minimal_covers[i+1:]:
            if sorted(m_cover) == sorted(per):
                bFind = True
                L_minimal_covers.remove(m_cover)
                break
        if bFind:
            continue
        else:
            i = i+1
    return L_minimal_covers


## Main functions
def main():
    ### Test case from the project
    
    R = ['A', 'B', 'C', 'D']
    FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

    print(closure(R, FD, ['A']))
    print(closure(R, FD, ['A', 'B']))
    print(all_closures(R, FD))

    R = ['A', 'B', 'C', 'D', 'E', 'F']
    FD = [[['A'], ['B', 'C']],[['B'], ['C','D']], [['D'], ['B']],[['A','B','E'], ['F']]]
    print(min_cover(R, FD)) 

    R = ['A', 'B', 'C']
    FD = [[['A', 'B'], ['C']],[['A'], ['B']], [['B'], ['A']]] 
    print(min_covers(R, FD))
    print(all_min_covers(R, FD)) 

    ### Add your own additional test cases if necessary

    ## Tutorial questions
    R = ['A', 'B', 'C', 'D', 'E']
    FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]

    print(min_cover(R, FD))
    print(min_covers(R, FD))
    print(all_min_covers(R, FD))

if __name__ == '__main__':
    main()



