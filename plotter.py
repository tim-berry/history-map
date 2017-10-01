import sqlite3
import os
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.collections import LineCollection

# Database setup
dir_path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(dir_path, 'data.db'))
cursor = db.cursor()

# Map setup
map = Basemap(projection='cyl',resolution='c')
map.drawmapboundary(fill_color='#424242')
map.fillcontinents(color='#636363')

# Clear any empty data which will cause the program to crash
cursor.execute('DELETE FROM plots WHERE lat IS NULL OR lat = \'\';')
db.commit()

cursor.execute('SELECT DISTINCT vid FROM plots;')
vids = [x[0] for x in cursor.fetchall()]

for vid in vids:
    cursor.execute('SELECT lat, lon, alt FROM plots WHERE vid = ?;', (vid,))

    lat, lon, alt = zip(*cursor.fetchall())
    alt = np.array(alt)

    if (np.all(np.diff(lat) < 0.5)) and (np.all(np.diff(lat) < 0.5)):
        points = np.array([lon, lat]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=plt.get_cmap('ocean'),
                            norm=plt.Normalize(0, 60000))
        lc.set_array(alt)
        lc.set_linewidth(1)

        plt.gca().add_collection(lc)

plt.show()
db.close()
