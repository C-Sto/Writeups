from PIL import Image
import sys

if len(sys.argv) != 2:
    print 'usage: ./unhide.py [in_img]'
    sys.exit(0)

# load in the image
in_img = Image.open(sys.argv[1])
in_pixels = in_img.convert('RGB')  # get the RGB's
in_l = in_img.load()
width, height = in_img.size
rev_o_a = []

# since we don't know the size of the hidden data, take it all. We can see the plaintext that stops making sense
for i in range(0, width*height):
    temp_x = i % width
    temp_y = i / width
    r, g, b = in_pixels.getpixel((temp_x, temp_y))
    # we only care about the r value, let's step by step reverse the encode process
    r_from_int = bin(r)[2:]
    # we know that the last two bits are the two bits that are encode the data, so we take those, and store them
    last_two_bits = r_from_int[-2:]
    rev_o_a.append(last_two_bits)

# from this point, the start of bit_list is the equivalent of o_a in the original process
rev_o = "".join(rev_o_a)  # this is the equiv of o

rev_d = ''  # this is the equiv of d

for i in range(0, len(rev_o), 8):
    rev_d += chr(int(rev_o[i:i+8], 2))

rev_d_clear = ""

for c in range(0,len(rev_d), 2):  # since the encode is a simple compression thing, just do the opposite
    if not rev_d[c].isdigit():
        # undoubtedly will hit a point that we don't care about anymore. Let's avoid that.
        break
    rev_d_clear += rev_d[c+1] * int(rev_d[c])

print rev_d_clear
