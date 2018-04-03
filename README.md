History Map
=======

<img src="https://i.imgur.com/N9h5yGJ.png" width="800">

A simple set of scripts for creating flight path maps, sourcing data from the IVAO network (VATSIM data could be used with a little modification). This project  was inspired by [NATS Airspace+](https://www.nats.aero/news/videos-imagery/airspace-plus-videos/) and [VATSIM Mobile Monitor](https://vatmm.org/).

 1. `downloader.py` Gathers data every 15 seconds from the IVAO network and stores it in a database for later use.
 2. `plotter.py` Creates a flight path map. Outputs the result as `output.png`.

 Please note: running `plotter.py` can take some time to execute.

## Installing requirements ##
Most of the required packages for these scripts can be downloaded using `pip`. You may have to [manually install](https://matplotlib.org/basemap/users/installing.html) the `basemap` package. If you're using Windows, there may be an [easier solution](https://stackoverflow.com/a/31713592).
