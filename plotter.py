from mpl_toolkits.basemap import Basemap
import sqlite3
import os
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(dir_path, 'data.db'))
cursor = db.cursor()

'''
Sometimes the aircraft data provided by Whazzup is empty.
If the data is empty, it throws an error in the program.
This should clear any empty cells.
'''
cursor.execute('DELETE FROM plots WHERE lat IS NULL OR lat = \'\';')
db.commit()

cursor.execute('SELECT DISTINCT vid FROM plots;')
vids = [x[0] for x in cursor.fetchall()]

lat = []
lon = []

map = Basemap(projection='cyl',resolution='c')

map.drawmapboundary(fill_color='#424242')
map.fillcontinents(color='#636363')

for vid in vids:
    cursor.execute('SELECT lat, lon FROM plots WHERE vid = ?;', (vid,))
    plots = cursor.fetchall()
    for plot in plots:
        try:
            cross_meridian = abs(plot[1]) + abs(lon[-1])
            delta_lon = abs(abs(plot[1]) - abs(lon[-1]))
            delta_lat = abs(abs(plot[0]) - abs(lat[-1]))
        except IndexError:
            cross_meridian = False
            delta_lon = False
            delta_lat = False

        if (cross_meridian) > 358 or (delta_lon > 0.5) or (delta_lat > 0.5):
            map.plot(lon, lat, marker=None,color='deepskyblue',linewidth=0.2)
            lat = []
            lon = []

        lat.append(plot[0])
        lon.append(plot[1])
    map.plot(lon, lat, marker=None,color='deepskyblue',linewidth=0.2)
    lat = []
    lon = []

plt.show()

db.close()
