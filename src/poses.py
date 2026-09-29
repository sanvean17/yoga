"""Library of poses used in the class. Each function returns a Fig.

Side views face +x (front of the mat on the right of the page) unless
flip=True. Back views show the student from behind, so the student's
RIGHT (orange) is on the right of the drawing.
"""
from figures import side, back, add, d, C, T, NECK, UA, FA

R, L, N = "R", "L", "N"

# --------------------------------------------------------------- standing
def tadasana(flip=False):
    return side((0, 81.5), 90, armN=((2, 83), -1), armF=((-1, 83), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip)


def tadasana_heart(flip=False):
    return side((0, 81.5), 90, armN=((13, 113), -1), armF=((11, 113), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip)


def arms_up(flip=False):
    return side((0, 81.5), 90, head=93, armN=((7, 181), -1), armF=((3, 181), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip,
                extra=[("arrow", [(24, 118), (24, 158)], 0)])


def fold(flip=False):
    return side((-2, 78), -68, curve=4, head=-82, face=-170, legs_behind=True, head_top=True,
                armN=((26, 2), 1), armF=((23, 2), 1),
                legN=((-4, 4), 1), legF=((-6, 4), 1), footN=-4, footF=-4, flip=flip)


def half_lift(flip=False):
    return side((-8, 77), -4, head=4, face=-25,
                armN=((13, 42), -1), armF=((11, 42), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip)


def roll_up(flip=False):
    return side((-6, 79), 35, curve=7, head=-10, face=-60,
                armN=((20, 50), -1), armF=((18, 50), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip,
                extra=[("arrow", [(58, 70), (40, 112)], -8)])


# ------------------------------------------------------ sun salutation floor
def step_back_right():
    """Hands on the floor, RIGHT foot stepped back (right = near side = orange)."""
    return side((2, 35), 24, head=24, face=-10,
                armN=((53, 3), -1), armF=((51, 3), -1),
                legF=((40, 4), 1), footF=-2,
                legN=((-70, 11), -1), footN=-35, sideN=R, sideF=L)


def plank():
    return side((13, 33), 20, head=20, face=-20,
                armN=((62, 3), -1), armF=((60, 3), -1),
                legN=((-60, 9), -1), legF=((-62, 9), -1), footN=-40, footF=-40)


def plank_knees():
    return side((16.6, 24), 30, head=30, face=-10,
                armN=((61, 3), -1), armF=((59, 3), -1),
                legN=((-56, 4), 1), legF=((-58, 4), 1), footN=180, footF=180)


def prone():
    return side((0, 8), 1.5, head=0, face=-80,
                armN=((44, 3), -1), armF=((42, 3), -1), head_top=True,
                legN=((-77, 6), -1), legF=((-78, 6), -1), footN=182, footF=182)


def cobra():
    return side((0, 7), 28, curve=-3, head=48, face=22,
                armN=((47, 3), -1), armF=((45, 3), -1),
                legN=((-77, 6), -1), legF=((-78, 6), -1), footN=183, footF=183)


def updog():
    return side((0, 20), 42, curve=-3, head=62, face=38,
                armN=((40, 3), -1), armF=((38, 3), -1),
                legN=((-77, 7), -1), legF=((-78, 7), -1), footN=185, footF=185)


# -------------------------------------------------------------- all fours
def _knees(ankle_y=6, foot=180):
    return dict(legN=((-37, ankle_y), -1), legF=((-39, ankle_y), -1), footN=foot, footF=foot)


def tabletop(toes=False):
    k = _knees(12, -80) if toes else _knees()
    return side((0, 47), 4, head=2, face=-55,
                armN=((50, 1), -1), armF=((48, 1), -1), **k)


def cat():
    return side((0, 47), 4, curve=9, head=-60, face=-110,
                armN=((50, 1), -1), armF=((48, 1), -1), **_knees(),
                extra=[("arrow", [(10, 76), (38, 76)], -8)])


def cow():
    return side((0, 47), 4, curve=-7, head=35, face=30,
                armN=((50, 1), -1), armF=((48, 1), -1), **_knees(),
                extra=[("arrow", [(10, 22), (38, 22)], 8)])


def child():
    return side((-36, 20), -5, curve=6, head=-25, face=-110, head_top=True, legs_behind=True,
                armN=((64, 3), 1), armF=((62, 3), 1),
                legN=((-38, 5), 1), legF=((-40, 5), 1), footN=180, footF=180)


def downdog(flip=False, sideN=N, sideF=N):
    return side((0, 70), -44.4, head=-60, face=-140,
                armN=((72, 1), -1), armF=((70, 1), -1),
                legN=((-46, 10), 1), legF=((-48, 10), 1), footN=-48, footF=-48,
                sideN=sideN, sideF=sideF, flip=flip)


def downdog_lift(flip=False):
    """tabletop -> dog: arrow shows hips going up and back."""
    f = downdog(flip=flip)
    sx = -1 if flip else 1
    f.arrow([(24 * sx, 44), (0, 82)], bulge=10 * sx)
    return f


# ---------------------------------------------------------- flow, side view
def lunge(flip=False):
    """Front (near) foot between the hands. Right side: flip=False."""
    near, far = (L, R) if flip else (R, L)
    return side((0, 34), 25, head=25, face=0,
                armN=((53, 3), -1), armF=((50, 3), -1),
                legN=((41, 4), 1), footN=-2,
                legF=((-70, 11), -1), footF=-35, sideN=near, sideF=far, flip=flip)


def lunge_rise(flip=False):
    """Back heel down, torso comes up: transition lunge -> Warrior II."""
    near, far = (L, R) if flip else (R, L)
    return side((0, 50), 90, head=90, face=True,
                armN=((5, 52), -1), armF=((2, 52), -1),
                legN=((44, 4), 1), footN=-2,
                legF=((-62, 4), -1), footF=-20, sideN=near, sideF=far, flip=flip,
                extra=[("arrow", [(-22, 110), (-22, 140)], 0)])


# -------------------------------------------------------------- back views
def _dl(f, p, t, col):
    f.label(p, t, col)


def warrior2(right=True):
    s = 1 if right else -1
    P = (12 * s, 54)
    f, j = back(P, 90, gaze=0 if right else 180,
                armR=((12 * s + 64, 104), -1),
                armL=((12 * s - 64, 104), 1),
                legR=((58, 4), 1) if right else ((56, 4), -1),
                legL=((-56, 4), 1) if right else ((-58, 4), -1),
                footR=(0, 12) if right else (-20, 7),
                footL=(200, 7) if right else (180, 12))
    _dl(f, (60, -12), "D", C["R"])
    _dl(f, (-58, -12), "I", C["L"])
    return f


def reverse_warrior(right=True):
    s = 1 if right else -1
    P = (12 * s, 54)
    tor = 90 + 22 * s
    neck = add(P, d(tor), T)
    perp = d(tor - 90)
    shoR, shoL = add(neck, perp, 14), add(neck, perp, -14)
    hipR, hipL = add(P, perp, 8), add(P, perp, -8)
    if right:
        up = (shoR, 112)
        back_ankle, back_hip = (-56, 4), hipL
    else:
        up = (shoL, 68)
        back_ankle, back_hip = (56, 4), hipR
    top = (add(up[0], d(up[1]), 50), -1)
    slide = add(back_hip, (back_ankle[0] - back_hip[0], back_ankle[1] - back_hip[1]), 0.22)
    f, _ = back(P, tor, head=tor + 8 * s, gaze=tor + 25 * s,
                armR=top if right else (slide, -1),
                armL=(slide, 1) if right else top,
                legR=((58, 4), 1) if right else ((56, 4), -1),
                legL=((-56, 4), 1) if right else ((-58, 4), -1),
                footR=(0, 12) if right else (-20, 7),
                footL=(200, 7) if right else (180, 12))
    _dl(f, (60, -12), "D", C["R"])
    _dl(f, (-58, -12), "I", C["L"])
    return f


def side_angle(right=True):
    s = 1 if right else -1
    P = (6 * s, 44)
    tor = 90 - 45 * s
    neck = add(P, d(tor), T)
    perp = d(tor - 90)
    shoR, shoL = add(neck, perp, 14), add(neck, perp, -14)
    top_sho = shoL if right else shoR
    top = (add(top_sho, d(90 - 40 * s), 50), -1 if right else 1)
    # upper arm down onto the thigh, forearm lying along the thigh toward the hip
    rest = ('A', -90 - 5 * s, 185 if right else -5)
    f, _ = back(P, tor, head=tor + 10 * s, gaze=90 - 15 * s,
                armR=rest if right else top,
                armL=top if right else rest,
                legR=((60, 4), 1) if right else ((64, 4), -1),
                legL=((-64, 4), 1) if right else ((-60, 4), -1),
                footR=(0, 12) if right else (-20, 7),
                footL=(200, 7) if right else (180, 12))
    _dl(f, (62, -12), "D", C["R"])
    _dl(f, (-62, -12), "I", C["L"])
    return f


def tree(right_foot_up=True, easy=False):
    s = 1 if right_foot_up else -1   # s=+1: stand on LEFT leg, right foot up
    P = (0, 81.5)
    stand = ((-8 * s + 0, 4), 1)
    if easy:
        lift = ((-3 * s, 9), 1 if right_foot_up else -1)
    else:
        lift = ((-4 * s, 30), 1 if right_foot_up else -1)
    heart_bend_R, heart_bend_L = -1, 1
    f, _ = back(P, 90,
                armR=((3, 114), -heart_bend_R), armL=((-3, 114), -heart_bend_L),
                legR=lift if right_foot_up else stand,
                legL=stand if right_foot_up else lift,
                footR=(205, 7) if right_foot_up else (-90, 3),
                footL=(-90, 3) if right_foot_up else (-25, 7))
    _dl(f, (24, -12), "D", C["R"])
    _dl(f, (-24, -12), "I", C["L"])
    return f


# ------------------------------------------------------------------ seated
def _cross_legs():
    return dict(legR=('A', -8, 186), legL=('A', 188, -6), footR=(186, 6), footL=(-6, 6))


def seated_cross(head=90, arrows=None, colored=False):
    f, _ = back((0, 15), 90, head=head, armR=((31, 18), -1), armL=((-31, 18), 1),
                colored=colored, arrows=arrows, **_cross_legs())
    return f


def seated_neck():
    f = seated_cross(head=62, colored=True)
    f.arrow([(-14, 106), (8, 100)], bulge=-6)
    _dl(f, (44, -10), "D", C["R"])
    _dl(f, (-44, -10), "I", C["L"])
    return f


def seated_shoulders():
    f = seated_cross()
    for x in (-14, 14):
        f.items.append((6, f'<circle cx="{x}" cy="-72" r="11" fill="none" stroke="#6b7785" '
                           f'stroke-width="2.4" stroke-dasharray="44 12"/>'))
        f.arrow([(x - 9, 77), (x - 11, 69)], bulge=-2)
    return f


def seated_sidebend(right_arm_up=True):
    s = 1 if right_arm_up else -1
    tor = 90 + 14 * s
    neck = add((0, 15), d(tor), T)
    perp = d(tor - 90)
    shoR, shoL = add(neck, perp, 14), add(neck, perp, -14)
    if right_arm_up:
        up = ((add(shoR, d(118), 48)), -1)
        down = ((-40, 5), 1)
        armR, armL = up, down
    else:
        up = ((add(shoL, d(62), 48)), 1)
        down = ((40, 5), -1)
        armR, armL = down, up
    f, _ = back((0, 15), tor, head=tor + 6 * s, armR=armR, armL=armL, **_cross_legs())
    _dl(f, (44, -10), "D", C["R"])
    _dl(f, (-44, -10), "I", C["L"])
    return f


def seated_legs_long():
    return side((0, 10), 92, armN=((25, 14), -1), armF=((23, 14), -1),
                legN=((77, 8), 1), legF=((76, 8), 1), footN=82, footF=82)


def kneeling():
    return side((-8, 13), 90, armN=((16, 17), -1), armF=((14, 17), -1),
                legN=((-8, 4), 1), legF=((-10, 4), 1), footN=180, footF=180)


def butterfly(lean=False):
    tor = 90
    f, _ = back((0, 15), tor, armR=((10, 11), -1), armL=((-10, 11), 1), colored=False,
                legR=('A', -12, 172), legL=('A', 192, 8), footR=(-95, 5), footL=(-85, 5))
    return f


# ------------------------------------------------------------------ lying
def supine_knees(arrow=False):
    ex = [("arrow", [(-10, 48), (-10, 70)], 0)] if arrow else None
    return side((0, 9.5), 180, head=180, face=90,
                armN=((-4, 5), 1), armF=((-6, 5), 1),
                legN=((36, 5), 1), legF=((34, 5), 1), footN=-2, footF=-2, extra=ex)


def bridge():
    return side((-10, 40), 216.5, curve=-3, head=180, face=90,
                armN=((-2, 5), -1), armF=((-4, 5), -1),
                legN=((32, 5), 1), legF=((30, 5), 1), footN=-2, footF=-2,
                extra=[("arrow", [(-10, 50), (-10, 72)], 0)])


def knees_chest():
    return side((0, 9.5), 180, head=180, face=90,
                armN=((-10, 38), 1), armF=((-12, 38), 1),
                legN=('A', 122, -12), legF=('A', 124, -14), footN=-60, footF=-60)


def twist(to_right=True):
    """Top view (seen from above), lying face up, head on the LEFT.
    Seen like this the student's RIGHT side is at the BOTTOM of the drawing
    (colours and D / I labels make it explicit)."""
    if to_right:
        legR, legL = ('A', -84, -4), ('A', -78, 2)
        fR, fL = (-4, 9), (2, 9)
    else:
        legR, legL = ('A', 78, -2), ('A', 84, 4)
        fR, fL = (-2, 9), (4, 9)
    f, _ = back((0, 0), 180, face_up=True, gaze=90 if to_right else -90,
                armR=((-52, -64), 1), armL=((-52, 64), -1),
                legR=legR, legL=legL, footR=fR, footL=fL)
    _dl(f, (-68, -62), "D", C["R"])
    _dl(f, (-68, 62), "I", C["L"])
    f.top_mat = (-80, -74, 72, 74)
    return f


def savasana():
    f, _ = back((0, 0), 180, face_up=True, colored=False,
                armR=((-6, -30), 1), armL=((-6, 30), -1),
                legR=((76, -18), 1), legL=((76, 18), -1),
                footR=(-30, 9), footL=(30, 9))
    f.top_mat = (-78, -38, 94, 38)
    return f


ALL = {
    "tadasana": tadasana, "tadasana_heart": tadasana_heart, "arms_up": arms_up,
    "fold": fold, "half_lift": half_lift, "roll_up": roll_up,
    "step_back_right": step_back_right, "plank": plank, "plank_knees": plank_knees,
    "prone": prone, "cobra": cobra, "updog": updog,
    "tabletop": tabletop, "tabletop_toes": lambda: tabletop(True), "cat": cat, "cow": cow,
    "child": child, "downdog": downdog, "downdog_lift": downdog_lift,
    "lunge_R": lunge, "lunge_rise_R": lunge_rise,
    "lunge_L": lambda: lunge(True), "lunge_rise_L": lambda: lunge_rise(True),
    "downdog_L": lambda: downdog(True),
    "w2_R": warrior2, "rev_R": reverse_warrior, "sa_R": side_angle,
    "w2_L": lambda: warrior2(False), "rev_L": lambda: reverse_warrior(False),
    "sa_L": lambda: side_angle(False),
    "tree_R": tree, "tree_R_easy": lambda: tree(True, True), "tree_L": lambda: tree(False),
    "seated_cross": seated_cross, "seated_neck": seated_neck,
    "seated_shoulders": seated_shoulders, "sidebend_R": seated_sidebend,
    "sidebend_L": lambda: seated_sidebend(False),
    "legs_long": seated_legs_long, "kneeling": kneeling, "butterfly": butterfly,
    "supine_knees": supine_knees, "bridge": bridge, "knees_chest": knees_chest,
    "twist_R": twist, "twist_L": lambda: twist(False), "savasana": savasana,
}
