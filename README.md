History Map
=======
A simple set of scripts for creating flight path maps, sourcing data from the IVAO network.

 1. `downloader.py` Gathers data every 15 seconds from the IVAO network and stores it in a database for later use.
 2. `plotter.py` Creates a flight path map.

## Installing requirements ##
Most of the required packages for these scripts can be downloaded using `pip`. You may have to [manually install](https://matplotlib.org/basemap/users/installing.html) the `basemap` package. If you're using Windows, there may be an [easier solution](https://stackoverflow.com/a/31713592).
