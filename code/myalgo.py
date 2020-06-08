"""
Zuyue Fu

"""

import numpy as np
import constant

"""
    add edge to matching from edges. 
    
    @arguments: 
    edges: set of edges (list of lists)
    matching: current matching (list of sets)
    vertices: current vertex covering (set)
    m: size of all edges
    n: size of all nodes
    
"""

def greedy(edges, matching, vertices, m, n):
    # loop through all edges
    for e in edges:
        if len(matching) >= constant.PROPORTION * m:
            break
        # process the current edge
        cur = {e[0], e[1]}

        if not (e[0] in vertices) and not (e[1] in vertices) and e[0]!=e[1]:
            # end vertices not covered, add to matching
            matching.append(cur)
            vertices.add(e[0])
            vertices.add(e[1])




# find augmenting path for graph incuded by edges w.r.t. matching

def find_aug_path(edges, matching, vertices, m, n):
    mm = len(edges) # size of available edges
    st = [-1] # start edge in the aug path
    for e in edges: # search for edge that has uncovered vertex
        if (e[0] not in vertices) or (e[1] not in vertices):
            st = e
            break

    # cannot find uncovered vertex, return
    if st[0] == -1:
        return

    # find augmenting path: 

    # st uncovered 
    if st[0] not in vertices and st[1] not in vertices:
        matching.append(set(st))
        vertices.add(st[0])
        vertices.add(st[1])
        return 
    elif st[0] not in vertices:
        prevnode = st[0]
        curnode = st[1]
    else:
        prevnode = st[1]
        curnode = st[0]

    snode = prevnode # this is the starting point of the augmenting path

    visited = [False for _ in range(n)]

    wl = [[curnode, 0, [{snode, curnode}]]] # with level: even -> not in matching; odd -> in matching

    visited[prevnode] = True


    # bfs
    while len(wl) > 0:
        prevnode, curlevel, traj = wl.pop()
        visited[prevnode] = True
        for e in edges:
            if prevnode not in e:
                continue
            if visited[e[0]] and visited[e[1]]:
                continue

            # curlevel is even: not in matching, we need in matching
            if (curlevel % 2 == 0) and (set(e) not in matching):
                continue

            # curlevel is odd: in matching, we need not in matching
            if (curlevel % 2 == 1) and (set(e) in matching):
                continue


            # pick the current node
            curnode = e[0]
            if curnode == prevnode:
                curnode = e[1]

            traj.append({prevnode, curnode})

            # find an augmenting path: sym diff and then return 
            if curlevel % 2 == 1 and curnode not in vertices:
                vertices.add(curnode)
                vertices.add(snode)
                for j in range(len(traj)):
                    if j % 2 == 0:
                        continue
                    for i in range(len(matching)):
                        if matching[i] == traj[j]:
                            matching[i] = traj[j+1]

                matching.append(traj[0])
                # print(len(matching))
                return 0


            wl.append([curnode, curlevel+1, traj])

    return 1 # not find 



def algo(edges, matching, vertices, m, n):
    flag = 0
    while flag == 0:
        flag = find_aug_path(edges, matching, vertices, m, n)



# test code
if __name__ == '__main__':
    edges = [[0,1],[1,2],[2,3]]
    matching = [{1,2}] # list of sets
    vertices = {1,2}
    m = 3
    n = 4
    find_aug_path(edges, matching, vertices, m, n)

    print(matching)

