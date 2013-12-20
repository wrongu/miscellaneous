from PIL import Image, ImageFilter
from sys import argv

def create_cookie_cutter_box_mesh(img, width, height, thickness, depression, div_w, div_h):
	blurred = img.filter(ImageFilter.BLUR)
	im_w, im_h = img.size
	w = width
	h = height
	t = thickness
	d = depression
	space_w = width / div_w
	space_h = height / div_h
	# initialize points and faces
	pts = []
	faces = []
	# add corner vertices
	pts.append((0, 0, 0))
	pts.append((w, 0, 0))
	pts.append((w, h, 0))
	pts.append((0, h, 0))
	pts.append((0, 0, t))
	pts.append((w, 0, t))
	pts.append((w, h, t))
	pts.append((0, h, t))
	# bottom
	faces.append((0,1,2))
	faces.append((0,2,3))
	# front
	faces.append((0,1,5))
	faces.append((0,5,4))
	# left
	faces.append((3,0,4))
	faces.append((3,4,7))
	# back
	faces.append((7,6,3))
	faces.append((3,6,2))
	# right
	faces.append((2,5,1))
	faces.append((2,6,5))
	# # create mesh of other points:
	# for xi in range(div_w + 1):
	# 	x = w * (float(xi) / float(div_w))
	# 	px = int(im_w * (float(xi) / float(div_w)))
	# 	if px >= im_w:
	# 		px = im_w-1
	# 	for yi in range(div_h + 1):
	# 		y = h * (float(yi) / float(div_h))
	# 		py = int(im_h * (float(yi) / float(div_h)))

	# 		if py >= im_h:
	# 			py = im_h-1
	# 		# depth is based on rgb
	# 		z = t
	# 		r,g,b = blurred.getpixel((px,py))
	# 		light = (r + g + b) / 3.0
	# 		if light > 128:
	# 			z = t - d

	# 		pts.append((x, y, z))

	# # add faces for all those points

	# def grid_to_pt_number(grid_x, grid_y):
	# 	return 8 + div_h * grid_x + grid_y

	# for xi in range(div_w):
	# 	for yi in range(div_h):
	# 		bl = grid_to_pt_number(xi, yi)
	# 		tl = grid_to_pt_number(xi, yi+1)
	# 		br = grid_to_pt_number(xi+1, yi)
	# 		tr = grid_to_pt_number(xi+1, yi+1)
	# 		# add 2 triangles
	# 		faces.append((bl, br, tr))
	# 		faces.append((tr, tl, bl))

	return pts, faces

if __name__ == '__main__':
	if len(argv) > 1:
		img = Image.open(argv[1])
		# img.show()
		# raw_input()
		width = 3.0
		height = 2.0
		thickness = 0.25
		sink = 0.125
		x_res = 300
		y_res = 200
		print "creating mesh"
		pts, faces = create_cookie_cutter_box_mesh(img, width, height, thickness, sink, x_res, y_res)
		print "mapping mesh"
		mapped_faces = [(pts[i], pts[j], pts[k]) for i,j,k in faces]

		outfile = "output.stl" if len(argv) < 3 else argv[2]
		print "ASCII writing to", outfile
		from stl import Binary_STL_Writer, ASCII_STL_Writer
		with open(outfile, "wb") as fp:
			writer = ASCII_STL_Writer(fp)
			writer.add_faces(mapped_faces)
			writer.close()
