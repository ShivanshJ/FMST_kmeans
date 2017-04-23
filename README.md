# FMST
Fast Minimum Spanning Tree based on k_means for Big-Data Analytics.
-------------------

There are a number of algorithms that have been proposed in graph theory literature to compute the minimum spanning tree of a given graph.
These include  the  famous Prim’s  and Kruskal’s  algorithm,  among  others.  The  main drawback of these algorithms is their greedy 
nature, which means they cannot be applied to large datasets. It uses K-means to find the MST with a reduced complexity of O(N 1.5 ).
***
The steps of making the MST are as follows:<br/>
aMST_one:
- Making clusters(1) of the data points
- Running an MST algorithm on each of the clusters formed forming subset MSTs for each cluster(2)
- Making a separate MST(3) of the centroids of the clusters
- On adjacent centroid MST edges of (3), joining the subset MSTs in (2) according to the closest point of the adjacent centroid MSTs
<br/><br/>
aMST_two:
- Making clusters(a) considering centroids as - the midpoints of adjacent centorids MST edges of (3)
- Running an MST algorithm on each of the clusters formed forming subset MSTs for each cluster(b)
- Making a separate MST(c) of the centroids of the clusters
- On adjacent centroid MST edges of (c), joining the subset MSTs in (b) according to the closest point of the adjacent centroid MSTs
------
- Combine edges of aMST_one and aMST_two to form a graph
- Run an MST algorithm on this graph

* * *
The code was tested on `Python 2.7.11`.
