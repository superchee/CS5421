########################################################################################
## project2.py - Code template for Project 2 - Functional Dependencies and Normalization 
########################################################################################

## If you need to import library put it below


## Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
    return []

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
    return []
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    return []

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



