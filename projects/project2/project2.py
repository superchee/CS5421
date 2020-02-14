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
        unused_F_copy = unused_F[:]
        for per in unused_F:
            if set(per[0]).issubset(S_closure): #add the attributes if X in closure
                S_closure += list( set(per[1]) - set(S_closure) )
                unused_F_copy.remove(per)
                bFind = True
                break
        if bFind == False:
            break #break when no more attributes can be found
        unused_F = unused_F_copy[:]
    return S_closure

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
    return all_closure
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    #simplify the right hand side
    L_rhs_minimal = []
    for fd in FD:
        lhs = fd[0]
        rhs = fd[1]
        if (len(rhs) > 1):
            for atr in rhs:
                L_rhs_minimal.append([lhs, list(atr)])
        else:
            L_rhs_minimal.append([lhs, rhs])

    #simplify the left hand side (change this part for all minimal covers)
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
            if (bFind):
                break
        if(not bFind): L_lhs_minimal.append([lhs, rhs])
    #remove duplicate fd
    #L_lhs_minimal.sort()
    #L_minimal = list(L_lhs_minimal for L_lhs_minimal,_ in itertools.groupby(L_lhs_minimal))
    L_minimal = L_lhs_minimal[:]

    #simplify the set itself by removing fd that can be derived from the others
    #for fd in L_minimal:
    while len(L_minimal) > 0:
        bFind = False
        for fd in L_minimal:
            lhs = fd[0]
            rhs = fd[1]
            L_temp = L_minimal[:]
            L_temp.remove(fd)
            if (set(rhs).issubset(closure(R,L_temp,lhs))):
                bFind = True
                L_minimal.remove(fd)
                break
        if bFind == False:
            break

    return L_minimal

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.
    '''
    return []

## Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    '''
    Explain the rationale of the algorithm here.
    '''
    return []

## You can add additional functions below



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



