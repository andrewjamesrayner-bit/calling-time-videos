import cairo, math, sys
sys.argv = ['x']
import rigmod as R
W, H = 1280, 720
YEL = (1.0, 0.86, 0.1); RED = (0.86, 0.16, 0.12); INK = (0.06, 0.06, 0.06); WHITE = (1, 1, 1)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
# sunburst background
g = cairo.RadialGradient(640, 420, 40, 640, 420, 900)
g.add_color_stop_rgb(0, 1, 0.93, 0.45); g.add_color_stop_rgb(0.45, 0.98, 0.45, 0.1); g.add_color_stop_rgb(1, 0.75, 0.08, 0.05)
c.set_source(g); c.paint()
for k in range(24):
    a = k * 2 * math.pi / 24
    c.move_to(640, 420); c.arc(640, 420, 1100, a, a + 0.11); c.close_path()
    c.set_source_rgba(1, 0.95, 0.5, 0.18); c.fill()

def otext(txt, x, y, size, fill, stroke=INK, sw=14, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.select_font_face("Inter Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    e = c.text_extents(txt); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(txt)
    c.set_source_rgb(*stroke); c.set_line_width(sw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgb(*fill); c.fill(); c.restore()
    return e.width

# departures board (right)
bx, by, bw, bh = 640, 205, 600, 380
c.save(); c.translate(bx + bw / 2, by + bh / 2); c.rotate(0.04); c.translate(-(bx + bw / 2), -(by + bh / 2))
R.rrect(c, bx, by, bw, bh, 18, fill=(0.08, 0.08, 0.1), stroke=INK, lw=12)
R.rrect(c, bx, by, bw, 70, 18, fill=(0.14, 0.14, 0.17))
c.select_font_face("Inter Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
for k, dest in enumerate(["MALAGA", "PALMA", "TENERIFE", "DALAMAN"]):
    yy = by + 120 + k * 70
    c.set_font_size(40); c.set_source_rgb(1, 1, 1); c.move_to(bx + 30, yy + 14); c.show_text(dest)
    c.set_source_rgb(*RED); c.move_to(bx + 340, yy + 14); c.show_text("CANCELLED")
c.set_font_size(30); c.set_source_rgb(1, 0.8, 0.2); c.move_to(bx + 30, by + 46); c.show_text("DEPARTURES")
c.restore()
# big red stamp
c.save(); c.translate(950, 560); c.rotate(-0.12)
R.rrect(c, -250, -78, 500, 156, 20, fill=RED, stroke=WHITE, lw=12)
c.restore()
otext("£200M", 950, 560, 130, WHITE, INK, 10, -0.12)

# shocked holidaymaker with suitcase (left)
R.extras_t[0] = 0
hd = R.man(c, 250, 660, 0.95, R.P(la=(110, 40), ra=(-110, -40)), eyes="wide", brow="raised", mouth="scream")
# sun hat
hx, hy = hd["head"]; print("head", hx, hy)
c.save(); c.translate(hx, hy - 70); c.scale(0.8, 0.8); R.poly(c, [(-150, 20), (150, 20), (90, -10), (-90, -10)], fill=(0.95, 0.85, 0.55), stroke=INK, lw=9)
R.rrect(c, -80, -80, 160, 80, 30, fill=(0.95, 0.85, 0.55), stroke=INK, lw=9); R.rrect(c, -80, -30, 160, 18, 4, fill=RED); c.restore()
# suitcase
R.rrect(c, 360, 580, 160, 120, 16, fill=(0.2, 0.5, 0.85), stroke=INK, lw=10)
R.line(c, [(400, 580), (400, 552), (480, 552), (480, 580)], 12, INK)
R.rrect(c, 380, 615, 120, 24, 6, fill=WHITE)

# headline
otext("WHO KILLED", 640, 70, 110, YEL, INK, 18)
otext("THOMAS COOK?", 640, 170, 110, YEL, INK, 18)
s.write_to_png("thumb_tc.png")
print("ok")
