import sqlite3
import os
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Database setup
dir_path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(dir_path, 'data.db'))
cursor = db.cursor()

'''
Map setup 
llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon are the lat/lon values of
the lower left and upper right corners of the map.
'''
map = Basemap(projection='cyl',
              resolution='c',
              llcrnrlat=-90,
              urcrnrlat=90,
              llcrnrlon=-180,
              urcrnrlon=180)
map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)

def get_sublist(plots):
    '''
    "I'm sorry but that code is monstrous and out of control. It needs to be
    exterminated."
    There are probably better ways to solve this.
    '''
    current = []
    plots = iter(plots)
    try:
        while True:
            try:
                current.append(next(plots))
                if ((abs(abs(current[-1][0]) - abs(current[-2][0])) > 0.5 ) or
                   ((abs(abs(current[-1][1]) - abs(current[-2][1])) > 0.5 ) or
                   (abs(current[-1][1]) + abs(current[-2][1]) > 359.))):
                    last = current.pop()
                    yield current.copy()
                    current = [last]
                else:
                    pass
            except IndexError:
                pass
    except StopIteration:
        yield current

# Clear any empty data which will cause the program to crash
cursor.execute('DELETE FROM plots WHERE lat IS NULL OR lat = \'\';')
db.commit()

cursor.execute('SELECT DISTINCT vid FROM plots;')
vids = [x[0] for x in cursor.fetchall()]

for vid in vids:
    cursor.execute('SELECT lat, lon, alt FROM plots WHERE vid = ?;', (vid,))
    data = cursor.fetchall()
    data = list(get_sublist(data))

    for seg in data:
        lat, lon, alt = zip(*seg)
        alt = np.array(alt)

        points = np.array([lon, lat]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=plt.get_cmap('autumn'),
                            norm=plt.Normalize(-20., 60000.))
        lc.set_array(alt)
        lc.set_linewidth(0.1)

        plt.gca().add_collection(lc)

db.close()

plt.savefig('output.png', bbox_inches='tight', pad_inches=0, dpi=400)
