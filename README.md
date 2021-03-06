# Marvel Backend APIs

## Summary

This basic Flask server provides the backend APIs for the [Marvel Social Network frontend](https://github.com/Gendo90/marvel_network_frontend). There is only one API currently, which provides the shortest paths data for the [Sankey data visualization](https://marvel-network-frontend.vercel.app/). More APIs that support additional data visualizations are coming soon!

## APIs

* /api/sankey
    * PARAMS:
        * hero1: string (name of "source" hero of sankey)
        * hero2: string (name of "sink" hero of sankey)
    * Example:
        * /api/sankey?hero1=SERAPH&hero2=HOO

## TODO

* Add 3D graph data visualization feature using D3 and additional APIs
    * Include edge weights to show relationship strength
* Bubble chart of heroes and first-degree connections 
    * filterable by # of connections (ranges, max and min)
* Comparison of two or more heroes (maybe a dynamic bar chart of first-deg. connections)
* Community Identification (which community is a hero in?)
* Fix non-connected hero responses for sankey, other APIs


## Technologies Used
* Python
* Flask
* Pandas