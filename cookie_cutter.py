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
	corners = []
	faces = []
	# add corner vertices
	corners.append((0, 0, 0))
	corners.append((w, 0, 0))
	corners.append((w, h, 0))
	corners.append((0, h, 0))
	corners.append((0, 0, t))
	corners.append((w, 0, t))
	corners.append((w, h, t))
	corners.append((0, h, t))
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

	# map corner indices to corner locations
	faces = [(corners[i], corners[j], corners[k]) for (i,j,k) in faces]

	# create mesh of other points:
	heightmap = {}
	for xi in xrange(div_w + 1):
		x = w * (float(xi) / float(div_w))
		px = int(im_w * (float(xi) / float(div_w)))
		if px >= im_w:
			px = im_w-1
		for yi in xrange(div_h + 1):
			y = h * (float(yi) / float(div_h))
			py = int(im_h * (float(yi) / float(div_h)))

			if py >= im_h:
				py = im_h-1
			# depth is based on rgb
			z = t
			r,g,b = blurred.getpixel((px,py))
			light = (r + g + b) / 3.0
			if light > 128:
				z = t - d

			heightmap[(xi,yi)] = z

	def get_heightmapped_point(xi, yi):
		x = w * (float(xi) / float(div_w))
		y = h * (float(yi) / float(div_h))
		z = heightmap[(xi, yi)]
		return (x, y, z)

	# add faces for all those points:
	for xi in xrange(div_w):
		for yi in xrange(div_h):
			bl = get_heightmapped_point(xi, yi)
			tl = get_heightmapped_point(xi, yi+1)
			br = get_heightmapped_point(xi+1, yi)
			tr = get_heightmapped_point(xi+1, yi+1)
			# add 2 triangles
			faces.append((bl, br, tr))
			faces.append((tr, tl, bl))
	return faces

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
		faces = create_cookie_cutter_box_mesh(img, width, height, thickness, sink, x_res, y_res)

		outfile = "output.stl" if len(argv) < 3 else argv[2]
		print "ASCII writing to", outfile
		from stl import Binary_STL_Writer, ASCII_STL_Writer
		with open(outfile, "w") as fp:
			writer = ASCII_STL_Writer(fp)
			writer.add_faces(faces)
			writer.close()
