import api
from mesh import Mesh

segmentation_id  = 47339 ; vx = 11; vy = 14; vz = 14;
task_id = 842341
cell_id = 903

# consensus = Mesh()
# for segment_id in (654, 665, 1009, 1538, 1620, 1621, 1667, 1668, 1680, 1723, 1936, 1960, 2029, 2086, 2146, 2163, 2184, 2196, 2197, 2215, 2231, 2334, 2376, 2419, 2453, 2613):
#   for x in range(2):
#     for y in range(2):
#       for z in range(2):
#         vertex = api.getSegmentMesh(segmentation_id,x,y,z,segment_id);
#         if vertex  != None:
#           consensus.merge( Mesh(vertex))


# consensus.displayStats()
# consensus.dump('consensus.ctm')


overview = Mesh()


for x in range(21,23):
  for y in range(27,29):
    for z in range(26,28):
      vertex = api.getOverviewMesh(cell_id, 0 , x , y, z);

      if vertex  != None:
        print x,y,z
        mesh = Mesh(vertex)
        mesh.scale(0.5,0.5,0.5)
        mesh.move(x * 128, y*128 , z*128)
        overview.merge( mesh )


overview.displayStats()
overview.dump('overview.ctm')