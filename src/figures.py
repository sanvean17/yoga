"""Parametric vector yoga figures.

Every figure is built from the same skeleton (fixed bone lengths) so that
proportions stay anatomically coherent. Limbs are placed with two-link
inverse kinematics: we give the target point of the hand / ankle and the
side toward which the elbow / knee bends.

Coordinates: y points UP, ground is y = 0. Angles in degrees, 0 = +x.

Colour convention (used everywhere in the document):
  orange = RIGHT side of the student, blue = LEFT side, dark = neutral.
  In side views the far limbs are drawn in a lighter tint.
"""
import math

T = 50      # pelvis -> shoulder
NECK = 15   # shoulder -> head centre
HEAD_R = 9
UA, FA = 26, 24   # upper arm, forearm
TH, SH = 40, 38   # thigh, shin
FOOT = 12
HIP_HALF = 8      # front/back view half pelvis width
SHO_HALF = 14     # front/back view half shoulder width

C = {
    "body": "#2c3a4b", "body_far": "#aab5c1",
    "R": "#e0701e", "R_far": "#f3bf98",
    "L": "#2f6fd0", "L_far": "#a9c4ee",
    "N": "#2c3a4b", "N_far": "#aab5c1",
}

W_LIMB = 7.5
W_TORSO = 13


def d(a):
    r = math.radians(a)
    return (math.cos(r), math.sin(r))


def add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def ik(p, q, a, b, bend):
    """Joint position of a two-link chain from p toward q.
    bend=+1 puts the joint counter-clockwise of the p->q line, -1 clockwise.
    Returns (joint, end)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    dist = math.hypot(dx, dy)
    dist = max(min(dist, a + b - 0.01), abs(a - b) + 0.01)
    base = math.atan2(dy, dx)
    off = math.acos((a * a + dist * dist - b * b) / (2 * a * dist))
    ang = base + bend * off
    j = (p[0] + a * math.cos(ang), p[1] + a * math.sin(ang))
    # recompute end so bone lengths are exact
    ea = math.atan2(q[1] - j[1], q[0] - j[0])
    e = (j[0] + b * math.cos(ea), j[1] + b * math.sin(ea))
    return j, e


def solve(start, spec, a, b):
    """spec = (target, bend) for IK, or ('A', ang1, ang2) for absolute angles."""
    if spec[0] == 'A':
        j = add(start, d(spec[1]), a)
        return j, add(j, d(spec[2]), b)
    return ik(start, spec[0], a, b, spec[1])


class Fig:
    def __init__(self):
        self.items = []   # (layer, svg)
        self.pts = []
        self.labels = []

    def _track(self, *ps):
        self.pts.extend(ps)

    def line(self, pts, color, w=W_LIMB, layer=1):
        self._track(*pts)
        path = "M" + " L".join(f"{x:.1f},{-y:.1f}" for x, y in pts)
        self.items.append((layer, f'<path d="{path}" fill="none" stroke="{color}" '
                           f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'))

    def curve(self, p0, p1, bulge, color, w=W_TORSO, layer=2):
        """Quadratic curve from p0 to p1 bulging perpendicular (left of p0->p1 if bulge>0)."""
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        c = (mx + nx * bulge * 2, my + ny * bulge * 2)
        self._track(p0, p1, (mx + nx * bulge, my + ny * bulge))
        dpath = f'M{p0[0]:.1f},{-p0[1]:.1f} Q{c[0]:.1f},{-c[1]:.1f} {p1[0]:.1f},{-p1[1]:.1f}'
        # white halo keeps the torso readable where it crosses a limb
        self.items.append((layer, f'<path d="{dpath}" fill="none" stroke="#fff" '
                           f'stroke-width="{w + 5}" stroke-linecap="round"/>'))
        self.items.append((layer, f'<path d="{dpath}" fill="none" stroke="{color}" '
                           f'stroke-width="{w}" stroke-linecap="round"/>'))

    def head(self, c, color=C["body"], layer=3):
        self._track((c[0] - HEAD_R, c[1] - HEAD_R), (c[0] + HEAD_R, c[1] + HEAD_R))
        self.items.append((layer, f'<circle cx="{c[0]:.1f}" cy="{-c[1]:.1f}" r="{HEAD_R}" fill="{color}" '
                           f'stroke="#fff" stroke-width="2.5" paint-order="stroke"/>'))

    def face(self, c, ang):
        """small nose tick showing where the face points (side views)."""
        p = add(c, d(ang), HEAD_R - 1)
        q = add(c, d(ang), HEAD_R + 3.5)
        self.items.append((5, f'<path d="M{p[0]:.1f},{-p[1]:.1f} L{q[0]:.1f},{-q[1]:.1f}" '
                           f'stroke="{C["body"]}" stroke-width="3.2" stroke-linecap="round"/>'))

    def gaze(self, c, ang, length=26):
        """dashed arrow = where the eyes look."""
        p = add(c, d(ang), HEAD_R + 3)
        q = add(p, d(ang), length)
        self._track(q)
        self.items.append((5, f'<path d="M{p[0]:.1f},{-p[1]:.1f} L{q[0]:.1f},{-q[1]:.1f}" '
                           f'stroke="#6b7785" stroke-width="2" stroke-dasharray="3 3" '
                           f'marker-end="url(#gz)"/>'))

    def label(self, p, text, color):
        self._track((p[0] - 6, p[1] - 6), (p[0] + 6, p[1] + 6))
        self.labels.append(f'<text x="{p[0]:.1f}" y="{-p[1]:.1f}" fill="{color}" font-size="15" '
                           f'font-weight="700" text-anchor="middle" dominant-baseline="central" '
                           f'font-family="Atkinson Hyperlegible, sans-serif">{text}</text>')

    def arrow(self, pts, color="#6b7785", layer=6, bulge=0):
        """curved motion arrow (solid), pts = [start, end]."""
        p0, p1 = pts
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1
        c = (mx - dy / L * bulge, my + dx / L * bulge)
        self._track(p0, p1, c)
        self.items.append((layer, f'<path d="M{p0[0]:.1f},{-p0[1]:.1f} Q{c[0]:.1f},{-c[1]:.1f} '
                           f'{p1[0]:.1f},{-p1[1]:.1f}" fill="none" stroke="{color}" stroke-width="2.4" '
                           f'marker-end="url(#mv)"/>'))

    top_mat = None

    def svg(self, scale=1.0, ground=True, pad=8, minw=0, cls="fig", ground_y=0.0, block=False):
        if self.top_mat:
            ground = False
            self._track(self.top_mat[:2], self.top_mat[2:])
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        x0, x1 = min(xs) - pad, max(xs) + pad
        y0, y1 = min(min(ys), ground_y) - pad, max(ys) + pad
        if x1 - x0 < minw:
            extra = (minw - (x1 - x0)) / 2
            x0 -= extra
            x1 += extra
        w, h = x1 - x0, y1 - y0
        body = []
        if ground:
            body.append(f'<rect x="{x0 + 2:.1f}" y="{-ground_y:.1f}" width="{w - 4:.1f}" height="4" '
                        f'rx="2" fill="#d9cfbf"/>')
        if self.top_mat:
            mx0, my0, mx1, my1 = self.top_mat
            body.append(f'<rect x="{mx0}" y="{-my1}" width="{mx1 - mx0}" height="{my1 - my0}" rx="6" '
                        f'fill="#efe7da" stroke="#d9cfbf" stroke-width="2"/>')
        body += [s for _, s in sorted(self.items, key=lambda t: t[0])]
        body += self.labels
        defs = ('<defs><marker id="gz" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" '
                'markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#6b7785"/></marker>'
                '<marker id="mv" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4.5" '
                'markerHeight="4.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#6b7785"/></marker></defs>')
        st = ' style="display:block"' if block else ''
        return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {-y1:.1f} {w:.1f} {h:.1f}" '
                f'width="{w * scale:.1f}" height="{h * scale:.1f}"{st}>{defs}{"".join(body)}</svg>')


# ---------------------------------------------------------------- side view
def side(hip, torso, *, curve=0, head=None, face=True, gaze=None,
         armN=None, armF=None, legN=None, legF=None,
         sideN="N", sideF="N", footN=None, footF=None, flip=False, labels=None, extra=None,
         head_top=False, legs_behind=False):
    """Side view, facing +x (flip=True mirrors to face -x).
    arm/leg = (target, bend). foot = angle of the foot from the ankle.
    sideN / sideF = 'R', 'L' or 'N' (colour of near / far limbs)."""
    f = Fig()
    sx = -1 if flip else 1

    def P(p):
        return (p[0] * sx, p[1])

    def A(a):
        return 180 - a if flip else a

    hipP = hip
    sho = add(hipP, d(torso), T)
    hang = torso if head is None else head
    hc = add(sho, d(hang), NECK)
    colN = C[sideN] if sideN != "N" else C["body"]
    colF = C[sideF + "_far"]

    def limb(start, spec, a, b, col, foot=None):
        j, e = solve(start, spec, a, b)
        pts = [P(start), P(j), P(e)]
        if foot is not None:
            pts.append(P(add(e, d(foot), FOOT)))
        return pts, col

    layers = []
    if legF: layers.append((0, *limb(hipP, legF, TH, SH, colF, footF)))
    if armF: layers.append((0, *limb(sho, armF, UA, FA, C["body_far"])))
    if legN: layers.append((1 if legs_behind else 3, *limb(hipP, legN, TH, SH, colN, footN)))
    if armN: layers.append((4, *limb(sho, armN, UA, FA, C["body"])))
    for layer, pts, col in layers:
        f.line(pts, col, layer=layer)
    # torso: bulge sign relative to hip->shoulder direction; mirrored when flipped
    f.curve(P(hipP), P(sho), curve * (-1 if flip else 1), C["body"], layer=2)
    # neck
    f.line([P(sho), P(add(sho, d(hang), NECK - HEAD_R + 2))], C["body"], w=8, layer=2)
    f.head(P(hc), layer=5 if head_top else 3)
    if face is not False:
        f.face(P(hc), A(hang - 90 if face is True else face))
    if gaze is not None:
        f.gaze(P(hc), A(gaze))
    if labels:
        for p, t, col in labels:
            f.label(P(p), t, col)
    if extra:
        for kind, *args in extra:
            if kind == "arrow":
                pts, bulge = args
                f.arrow([P(pts[0]), P(pts[1])], bulge=bulge * sx)
    return f


# ------------------------------------------------------------ back / front / top view
def back(pelvis, torso=90, *, head=None, gaze=None,
         armR=None, armL=None, legR=None, legL=None, footR=None, footL=None,
         colored=True, labels=True, hands_center=False, arrows=None, lying=False, face_up=False):
    """Viewed from BEHIND the student: the student's right side is on the
    right of the drawing (+x). For lying 'top' views pass face_up=True,
    which mirrors right/left the way you see a person lying face up."""
    f = Fig()
    perp = d(torso - 90)           # toward +x when torso is upright
    if face_up:
        perp = (-perp[0], -perp[1])
    hipR = add(pelvis, perp, HIP_HALF)
    hipL = add(pelvis, perp, -HIP_HALF)
    neck = add(pelvis, d(torso), T)
    shoR = add(neck, perp, SHO_HALF)
    shoL = add(neck, perp, -SHO_HALF)
    hang = torso if head is None else head
    hc = add(neck, d(hang), NECK)
    cR = C["R"] if colored else C["body"]
    cL = C["L"] if colored else C["body"]

    def limb(start, spec, a, b, foot=None, footlen=FOOT):
        j, e = solve(start, spec, a, b)
        pts = [start, j, e]
        if foot is not None:
            ang, ln = foot if isinstance(foot, tuple) else (foot, footlen)
            pts.append(add(e, d(ang), ln))
        return pts

    if legR: f.line(limb(hipR, legR, TH, SH, footR), cR, layer=1)
    if legL: f.line(limb(hipL, legL, TH, SH, footL), cL, layer=1)
    # torso as trapezoid
    f._track(hipR, hipL, shoR, shoL)
    poly = [hipR, shoR, shoL, hipL]
    f.items.append((2, '<path d="M' + " L".join(f"{x:.1f},{-y:.1f}" for x, y in poly) +
                    f' Z" fill="{C["body"]}" stroke="{C["body"]}" stroke-width="6" stroke-linejoin="round"/>'))
    f.line([neck, add(neck, d(hang), NECK - HEAD_R + 2)], C["body"], w=8, layer=2)
    if armR: f.line(limb(shoR, armR, UA, FA), cR, layer=3)
    if armL: f.line(limb(shoL, armL, UA, FA), cL, layer=3)
    f.head(hc)
    if gaze is not None:
        f.gaze(hc, gaze)
    if arrows:
        for pts, bulge in arrows:
            f.arrow(pts, bulge=bulge)
    return f, dict(hipR=hipR, hipL=hipL, shoR=shoR, shoL=shoL, neck=neck, hc=hc)
