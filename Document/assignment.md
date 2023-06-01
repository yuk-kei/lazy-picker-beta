# Reading Assignment 02 - Follow-Up

## Graph of 4 nodes and distances/edges

- Map in warehouse:

  <img src="imgs\map_org.png" alt="org" style="zoom:75%;" />

- Positions（Access point of Item: above）:

  - worker 0: (0,0)

  - Item 1: (2，16) Access point: (2, 17)

  - Item 2: (8， 0) Access point: (8, 1)

  - Item 3: (10， 10) Access point: (10, 11)

    

- Edges in the form of Adjacent Matrix:

  |                 | Worker 0 (0,0) | Item 1 (2, 17) | Item 2 (8, 1) | Item 3 (10, 11) |
  | --------------- | -------------- | -------------- | ------------- | --------------- |
  | Worker 0 (0,0)  | \              | 19             | 9             | 21              |
  | Item 1 (2, 17)  | 19             | \              | 22            | 14              |
  | Item 2 (8, 1)   | 9              | 22             | \             | 18              |
  | Item 3 (10, 11) | 21             | 14             | 18            | \               |
  
  
  
- Graph represent: 

  <img src="imgs\TSP GRAPH.png" alt="GRAPH" style="zoom:45%;" />



## Results of each step of being processed through genetic algorithm:

1. Create initial population (10 routes/individuals) by random generated:

   - population0 : [0, 1, 2, 3]

   - population1 : [3, 2, 1, 0]

   - population2 : [2, 0, 3, 1]

   - population3 : [1, 3, 0, 2]

   - population4 : [3, 1, 2, 0]

   - population5 : [2, 3, 1, 0]

   - population6 : [1, 0, 2, 3]

   - population7 : [0, 3, 1, 2]

   - population8 : [2, 1, 3, 0]

   - population9 : [3, 0, 2, 1]

     

2. Provide a list of the population along w/ each "individual" fitness value

   - Compute the fitness value for each individual using the fitness function, which is the total length of the path. The lower the fitness value, the shorter the path.
     - population 1: Calculate path length: 19 + 22 + 18 + 21 = 80
     - population 2: Calculate path length: 21 + 18 + 22 + 19 = 80
     - population 3: Calculate path length: 9 + 14 + 21 + 22 = 66
     - population 4: Calculate path length: 14 + 21 + 19 + 9 = 63
     - population 5: Calculate path length: 21 + 9 + 22 + 14 = 66
     - population 6: Calculate path length: 18 + 14 + 19+ 9 = 60
     - population 7: Calculate path length: 9 + 19 + 18 + 14 = 60
     - population 8: Calculate path length: 21 + 14+ 22 + 9 =80
     - population 9: Calculate path length: 9 + 21 + 14 + 22 = 66
     - population 10: Calculate path length: 21 + 9 + 22 + 14 = 66

   | 0,1,2,3 | 3,2,1,0 | 2,0,3,1 | 1,3,0,2 | 3,1,2,0 | 2,3,1,0 | 1,0,2,3 | 0,3,1,2 | 2,1,3,0 | 3,0,2,1 |
   | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
   | 80      | 80      | 66      | 66      | 66      | 60      | 60      | 66      | 66      | 66      |

   

3. Increase your population to 20 routes/individuals total (5 through crossover, 5 through mutation) & calculate their fitness

   Crossover: 

   - population 1, [0, 1, 2, 3], population 2, [3, 2, 1, 0]
     - Offspring 1: [3, 1, 2, 0], Offspring 2: [0, 2, 1, 3]
   - population2 : [2, 0, 3, 1], population3 : [1, 3, 0, 2]
     - Offspring 3: [2, 3, 0, 1], Offspring 4: [1, 0, 3, 2]
   - population7 : [0 ,3, 1, 2], population10 : [3, 0, 2 ,1]
     - Offspring 5: [3, 0, 1, 2]

   Mutation:

   - Mutated Individual 1: [1, 2, 3, 0] 
   - Mutated Individual 2: [2, 1, 0, 3] 
   - Mutated Individual 3: [0, 1, 3, 2] 
   - Mutated Individual 4: [1, 3, 2, 0] 
   - Mutated Individual 5: [3, 2, 0, 1] 

   | 0,1,2,3 | 3,2,1,0 | 2,0,3,1 | 1,3,0,2 | 3,1,2,0 | 2,3,1,0 | 1,0,2,3 | 0,3,1,2 | 2,1,3,0 | 3,0,2,1 |
   | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
   | 80      | 80      | 66      | 66      | 66      | 60      | 60      | 66      | 66      | 66      |
   | 2,0,3,1 | 0,2,1,3 | 2,3,0,1 | 1,0,3,2 | 3,0,1,2 | 1,2,3,0 | 2,1,0,3 | 0,1,3,2 | 1,3,2,0 | 3,2,0,1 |
   | 66      | 66      | 80      | 80      | 80      | 80      | 80      | 60      | 60      | 60      |

   

4. Select the top 10

   | 0,1,3,2 | 1,3,2,0 | 2,0,3,1 | 1,3,0,2 | 2,3,1,0 | 3,2,0,1 | 1,0,2,3 | 0,2,1,3 | 2,1,3,0 | 3,0,2,1 |
   | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
   | 60      | 60      | 66      | 66      | 60      | 60      | 60      | 66      | 66      | 66      |

5. Repeat the process 2 more times

   1. Increase popularity 2nd:

      crossover: [3,1,0,2], [1,3,2,0] ; [0,3,1,2], [3,1,2,0] ; [3,0,1,2]

      Mutation: [1,2,3,0],  [0,2,3,0], [0,2,3,1], [1,0,3,2], [3,2,0,1]

      | 0,1,3,2 | 1,3,2,0 | 2,0,3,1 | 1,3,0,2 | 2,3,1,0 | 3,2,0,1 | 1,0,2,3 | 0,2,1,3 | 2,1,3,0 | 3,0,2,1 |
      | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
      | 60      | 60      | 66      | 66      | 60      | 60      | 60      | 66      | 66      | 66      |
      | 1,2,3,0 | 2,3,0,1 | 0,2,3,1 | 1,0,3,2 | 3,1,0,2 | 1,3,2,0 | 0,3,1,2 | 3,1,2,0 | 3,2,0,1 | 3,0,1,2 |
      | 80      | 80      | 60      | 80      | 60      | 60      | 66      | 66      | 60      | 80      |

      Select the top 10:

      | 0,1,3,2 | 1,3,2,0 | 0,2,3,1 | 2,3,1,0 | 3,1,0,2 | 3,2,0,1 | 1,0,2,3 | 0,2,1,3 | 2,1,3,0 | 3,0,2,1 |
      | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
      | 60      | 60      | 60      | 60      | 60      | 60      | 60      | 66      | 66      | 66      |

   2. Increase popularity 3nd:

      crossover: [1,0,3,2] [0,3,2,1] ; [2,0,3,1] [0,2,3,1]; [1,2,0,3]

      Mutation:  [2,1,3,0] [0,3,2,1] [0,1,3,2] [2,0,1,3] [3,0,2,1]

      | 0,1,3,2 | 1,3,2,0 | 0,2,3,1 | 2,3,1,0 | 3,1,0,2 | 3,2,0,1 | 1,0,2,3 | 0,2,1,3 | 2,1,3,0 | 3,0,2,1 |
      | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
      | 60      | 60      | 60      | 60      | 60      | 60      | 60      | 66      | 66      | 66      |
      | 1,0,3,2 | 0,3,2,1 | 2,0,3,1 | 0,2,3,1 | 1,2,0,3 | 2,1,3,0 | 0,3,2,1 | 0,1,3,2 | 2,0,1,3 | 3,0,2,1 |
      | 80      | 80      | 66      | 60      | 66      | 66      | 80      | 66      | 60      | 66      |

      Select the top 10: 

      | 0,1,3,2 | 1,3,2,0 | 0,2,3,1 | 2,3,1,0 | 3,1,0,2 | 3,2,0,1 | 1,0,2,3 | 2,0,1,3 | 2,1,3,0 | 3,0,2,1 |
      | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
      | 60      | 60      | 60      | 60      | 60      | 60      | 60      | 60      | 66      | 66      |

   

6. Output your best result

   0, 1, 3, 2, which is (0,0) --> (2, 17) --> (10, 11) --> (8, 1) --> (0,0), total length: 60



##  Result (graph) of each step of being process through a single application of nearest neighbor:

1. start with any random vertex, highlight it with ''🔵'

   ``` python
   start_index = random.randint(0, nums_of_vertexes - 1)
   ```

   

   Random vertex: Item 3 (10, 11) 

   <img src="imgs\random_start.png" style="zoom:70%;" />

2. find an edge which gives the minimum distance between the current vertex & an unvisited node - highlight that & make the visited node the current one

   ``` python
    def iterate(curr_vertex):
   
        curr_index = curr_vertex.index
        # find an edge with the minimum weight
        next_min_weight = float("inf")
        min_edge = None
        min_index = 0
        for (i, edge) in enumerate(adjacent_map[curr_index]):
            if edge is not None and edge.weight < next_min_weight and not self.visited[i]:
               next_min = edge.weight
               min_edge = edge
               min_index = i
        # set the min edge to the next vertex
        self.color_edge(min_edge)
        self.result.append(min_edge)
   
        # set the current vertex as visited
        visited[curr_index] = True
   
        return vertexes[next_index]
   ```

   

   (10, 11) --> (2, 17)

   <img src="imgs\random_1.png" style="zoom:70%;" />

3. Repeat until all vertices are visited at least once

   ``` python
   while len(result) < nums_of_vertexes - 1:
        curr_vertex = iterate(curr_vertex)
   ```

   

   1. (2, 17) --> (0, 0)

      <img src="imgs\random_2.png" style="zoom:70%;" />

   2. (0, 0) --> (8, 1)

      <img src="imgs\random_3.png" style="zoom:70%;" />

      

   3. (8, 1) --> (10, 11)

      <img src="imgs\random_4.png" style="zoom:70%;" />

   4. End

      (10, 11) --> (2, 17) --> (0, 0) --> (8, 1) --> (10, 11)

      3 --> 1 --> 0 --> 2 --> 3

      total length: 60

4. Final route generated by the nearest neighbor(Same route but reset the start to worker node)

   ``` python
   for i in range(len.result):
   	if result[i].start_node.index == 0: #(result are list of edges)
   		start_index = i
       	break
   ```

   

   <img src="imgs\random_5.png" style="zoom:70%;" />