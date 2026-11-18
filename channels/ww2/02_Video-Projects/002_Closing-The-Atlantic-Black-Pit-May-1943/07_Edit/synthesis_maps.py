#!/usr/bin/env python3
import detection_maps as dm
import bridge_maps as bm
if __name__=='__main__':
 dm.SPECS={'L039':bm.S['L039']};dm.render=bm.render;dm.main()
