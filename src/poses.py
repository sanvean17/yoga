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


# ------------------------------------------------------------ v2 additions
def legs_long_bent():
    return side((0, 10), 92, armN=((24, 22), -1), armF=((22, 22), -1),
                legN=((64, 6), 1), legF=((63, 6), 1), footN=80, footF=80)


def seated_twist():
    f, _ = back((0, 15), 90, head=90, gaze=0,
                armR=((36, 5), -1), armL=((30, 16), -1), **_cross_legs())
    f.arrow([(-20, 44), (20, 50)], bulge=-10)
    _dl(f, (44, -10), "D", C["R"])
    _dl(f, (-44, -10), "I", C["L"])
    return f


def wrists():
    f = side((0, 10), 90, armN=((50, 60), -1), armF=((48, 60), -1),
             legN=('A', -6, 188), legF=('A', -2, 186), footN=180, footF=180)
    f.items.append((6, '<circle cx="54" cy="-60" r="9" fill="none" stroke="#6b7785" '
                       'stroke-width="2.4" stroke-dasharray="40 16"/>'))
    f.arrow([(46, 67), (47, 70)], bulge=0)
    f._track((64, 72), (44, 48))
    return f


def step_back_knee(right=True):
    """Hands on the floor, one foot stepped back WITH THAT KNEE ON THE FLOOR.
    right=True: right (near) leg back. right=False: left (far) leg back."""
    back_leg = ('A', -141, 180)
    front_leg = ((40, 4), 1)
    if right:
        return side((4, 30), 22, head=22, face=-10,
                    armN=((53, 1), -1), armF=((51, 1), -1),
                    legF=front_leg, footF=-2, legN=back_leg, footN=180, sideN=R, sideF=L)
    return side((4, 30), 22, head=22, face=-10,
                armN=((53, 1), -1), armF=((51, 1), -1),
                legN=front_leg, footN=-2, legF=back_leg, footF=180, sideN=R, sideF=L)


def half_lift_thighs(flip=False):
    return side((-8, 78), 22, head=18, face=-20,
                armN=((7, 47), -1), armF=((5, 47), -1),
                legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4, flip=flip)


def downdog_walk():
    return side((0, 70), -52, head=-62, face=-140,
                armN=((58, 1), -1), armF=((56, 1), -1),
                legN=((-22, 8), 1), legF=((-26, 8), 1), footN=-45, footF=-45,
                extra=[("arrow", [(-40, 20), (-14, 20)], 0)])


def ragdoll():
    return side((-2, 78), -70, curve=4, head=-84, face=-170, legs_behind=True, head_top=True,
                armN=((30, 22), -1), armF=((4, 22), 1),
                legN=((-4, 4), 1), legF=((-6, 4), 1), footN=-4, footF=-4,
                extra=[("arrow", [(-18, 40), (-26, 40)], 0), ("arrow", [(38, 40), (46, 40)], 0)])


def seated_fold():
    return side((0, 10), 58, curve=4, head=45, face=10,
                armN=((44, 26), -1), armF=((42, 26), -1),
                legN=((62, 6), 1), legF=((61, 6), 1), footN=80, footF=80)


def lie_down():
    """transition: from sitting, hands behind, lowering onto the back."""
    return side((0, 10), 150, head=160, face=60,
                armN=((-30, 3), 1), armF=((-32, 3), 1),
                legN=((50, 5), 1), legF=((48, 5), 1), footN=-2, footF=-2,
                extra=[("arrow", [(-22, 50), (-44, 26)], 6)])


def wipers(to_right=True):
    """Lying on the back, feet on the floor wide apart; the knees swing
    from side to side (double arrow over the knees)."""
    f = supine_knees()
    f.arrow([(14, 58), (38, 58)], bulge=8)
    f.arrow([(38, 58), (14, 58)], bulge=8)
    f._track((10, 70))
    return f


ALL.update({
    "legs_long_bent": legs_long_bent, "seated_twist": seated_twist, "wrists": wrists,
    "step_back_R_knee": step_back_knee, "step_back_L_knee": lambda: step_back_knee(False),
    "half_lift_thighs": half_lift_thighs, "downdog_walk": downdog_walk, "ragdoll": ragdoll,
    "seated_fold": seated_fold, "lie_down": lie_down, "wipers": wipers,
})


def seated_catcow(round_back=False):
    """Side view seated cross-legged, hands on knees: spine rounds or opens."""
    if round_back:
        return side((0, 10), 92, curve=8, head=55, face=-30,
                    armN=((30, 14), -1), armF=((28, 14), -1),
                    legN=('A', -6, 188), legF=('A', -2, 186), footN=180, footF=180)
    return side((0, 10), 88, curve=-5, head=100, face=15,
                armN=((30, 14), -1), armF=((28, 14), -1),
                legN=('A', -6, 188), legF=('A', -2, 186), footN=180, footF=180)


def leg_stretch():
    """Lying on the back, one leg up, hands holding behind the thigh,
    other knee bent with the foot on the floor."""
    return side((0, 9.5), 180, head=180, face=90,
                armN=((12, 40), 1), armF=((10, 40), 1),
                legN=((10, 76), 1), footN=10,
                legF=((34, 5), 1), footF=-2)


ALL.update({"seated_cow": seated_catcow, "seated_cat": lambda: seated_catcow(True), "leg_stretch": leg_stretch})


# ------------------------------------------------------- seniors: chair / wall
CHAIR = "#a07c52"


def chair(f, x0, back_left=True, seat_y=44, depth=38):
    """Side-view chair. Seat from x0 to x0+depth; backrest on the left
    (back_left) or right end of the seat. Drawn behind the person."""
    xb = x0 if back_left else x0 + depth
    xf = x0 + depth if back_left else x0
    tilt = -3 if back_left else 3
    pts = [
        f"M{x0},{-seat_y} L{x0 + depth},{-seat_y}",
        f"M{xf},{-seat_y} L{xf},0", f"M{xb},{-seat_y} L{xb},0",
        f"M{xb},{-seat_y} L{xb + tilt},{-(seat_y + 46)}",
    ]
    for d_ in pts:
        f.items.append((-1, f'<path d="{d_}" stroke="{CHAIR}" stroke-width="4.5" stroke-linecap="round" fill="none"/>'))
    f._track((x0 - 4, 0), (x0 + depth + 4, seat_y + 48))


def wall(f, x, h=150):
    f.items.append((-1, f'<rect x="{x}" y="{-h}" width="7" height="{h}" fill="#d9cfbf"/>'))
    f._track((x, 0), (x + 7, h))


def chair_sit(variant="neutral"):
    """Seated on a chair, side view facing right, feet flat, hands on thighs."""
    curve, head, face = {"neutral": (0, 90, True), "cat": (8, 58, -30), "cow": (-5, 100, 15)}[variant]
    f = side((0, 48), 90 if variant == "neutral" else (92 if variant == "cat" else 88), curve=curve, head=head, face=face,
             armN=((30, 52), -1), armF=((28, 52), -1),
             legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0)
    chair(f, -10, back_left=True)
    return f


def chair_hamstring():
    """On a chair, right leg stretched forward heel on the floor, chest forward."""
    f = side((0, 48), 62, curve=3, head=50, face=0,
             armN=((34, 46), -1), armF=((30, 50), -1),
             legN=((74, 6), 1), footN=80, legF=('A', 2, -88), footF=0, sideN=R, sideF=L)
    chair(f, -10, back_left=True)
    return f


def chair_knee():
    """On a chair, hugging one knee toward the chest."""
    f = side((0, 48), 92, head=90,
             armN=((30, 74), 1), armF=((28, 74), 1),
             legN=('A', 40, -70), footN=-10, legF=('A', 2, -88), footF=0, sideN=R, sideF=L)
    chair(f, -10, back_left=True)
    return f


def dog_chair():
    """Standing, hands on the chair back, back long and horizontal."""
    f = side((0, 80), -2, head=-8, face=-60,
             armN=((97, 88), -1), armF=((95, 88), -1),
             legN=((2, 4), 1), legF=((0, 4), 1), footN=-4, footF=-4)
    chair(f, 100, back_left=True)
    return f


def lunge_chair(right_back=True):
    """High lunge holding the chair back: one foot stepped back, heel up."""
    sN, sF = (R, L) if right_back else (L, R)
    f = side((0, 66), 90, head=90,
             armN=((38, 88), -1), armF=((36, 88), -1),
             legN=((-50, 10), -1), footN=-40,      # near = back leg
             legF=((30, 4), 1), footF=-2, sideN=sN, sideF=sF)
    chair(f, 40, back_left=True)
    return f


def wide_stance():
    """Back view: feet wide apart, hands on hips (before Warrior II)."""
    f, _ = back((0, 72), 90, armR=((11, 80), 1), armL=((-11, 80), -1),
                legR=((44, 4), 1), legL=((-44, 4), -1), footR=(0, 10), footL=(180, 10))
    _dl(f, (46, -12), "D", C["R"])
    _dl(f, (-46, -12), "I", C["L"])
    return f


def tree_wall():
    f = tree(True, True)
    wall(f, -48)
    return f


def stand_heart_chair():
    f = tadasana_heart()
    chair(f, 40, back_left=True)
    return f


def arms_up_chair():
    f = arms_up()
    chair(f, 40, back_left=True)
    return f


ALL.update({
    "chair_sit": chair_sit, "chair_cat": lambda: chair_sit("cat"), "chair_cow": lambda: chair_sit("cow"),
    "chair_hamstring": chair_hamstring, "chair_knee": chair_knee, "dog_chair": dog_chair,
    "lunge_chair_R": lunge_chair, "lunge_chair_L": lambda: lunge_chair(False), "wide_stance": wide_stance,
    "tree_wall": tree_wall, "heart_chair": stand_heart_chair, "arms_up_chair": arms_up_chair,
})


def stand_hold():
    """Standing tall, both hands on the chair back."""
    f = side((0, 81.5), 90, armN=((38, 88), -1), armF=((36, 88), -1),
             legN=((1, 4), 1), legF=((-1, 4), 1), footN=-4, footF=-4)
    chair(f, 40, back_left=True)
    return f


def heel_raise():
    f = side((0, 88), 90, armN=((38, 92), -1), armF=((36, 92), -1),
             legN=((2, 12), 1), legF=((0, 12), 1), footN=-60, footF=-60,
             extra=[("arrow", [(-14, 40), (-14, 64)], 0)])
    chair(f, 40, back_left=True)
    return f


ALL.update({"stand_hold": stand_hold, "heel_raise": heel_raise})


# ------------------------------------------------- warriors with a chair (back view)
def chair_front(f, x0, w=30, seat=44, top=88):
    """Chair seen from the front/back (back views): legs, seat, backrest."""
    for d_ in [f"M{x0},{-seat} L{x0 + w},{-seat}", f"M{x0},0 L{x0},{-top}", f"M{x0 + w},0 L{x0 + w},{-top}",
               f"M{x0},{-top} L{x0 + w},{-top}", f"M{x0},{-(top - 14)} L{x0 + w},{-(top - 14)}"]:
        f.items.append((-1, f'<path d="{d_}" stroke="{CHAIR}" stroke-width="4" stroke-linecap="round" fill="none"/>'))
    f._track((x0 - 3, 0), (x0 + w + 3, top + 3))


def _hip_hand(P, tor, side_sign):
    """target for a hand resting on the hip (elbow out)."""
    perp = d(tor - 90)
    return add(add(P, perp, 11 * side_sign), d(tor), 8)


def w2_chair(right=True):
    s = 1 if right else -1
    P = (12 * s, 54)
    front_hand = ((78 * s, 88), -1 if right else 1)
    hip = (_hip_hand(P, 90, -s), -1 if right else 1)
    f, _ = back(P, 90, gaze=0 if right else 180,
                armR=front_hand if right else hip, armL=hip if right else front_hand,
                legR=((58, 4), 1) if right else ((56, 4), -1),
                legL=((-56, 4), 1) if right else ((-58, 4), -1),
                footR=(0, 12) if right else (-20, 7), footL=(200, 7) if right else (180, 12))
    chair_front(f, 72 if right else -102)
    _dl(f, (60, -12), "D", C["R"]); _dl(f, (-58, -12), "I", C["L"])
    return f


def rev_chair(right=True):
    s = 1 if right else -1
    P = (12 * s, 54)
    tor = 90 + 12 * s
    neck = add(P, d(tor), T)
    perp = d(tor - 90)
    shoR, shoL = add(neck, perp, 14), add(neck, perp, -14)
    hipR, hipL = add(P, perp, 8), add(P, perp, -8)
    up_sho = shoR if right else shoL
    top = (add(up_sho, d(90 + 12 * s), 50), -1 if right else 1)
    back_ankle, back_hip = ((-56, 4), hipL) if right else ((56, 4), hipR)
    slide = add(back_hip, (back_ankle[0] - back_hip[0], back_ankle[1] - back_hip[1]), 0.24)
    f, _ = back(P, tor, head=tor, gaze=tor + 15 * s,
                armR=top if right else (slide, -1), armL=(slide, 1) if right else top,
                legR=((58, 4), 1) if right else ((56, 4), -1),
                legL=((-56, 4), 1) if right else ((-58, 4), -1),
                footR=(0, 12) if right else (-20, 7), footL=(200, 7) if right else (180, 12))
    chair_front(f, 72 if right else -102)
    _dl(f, (60, -12), "D", C["R"]); _dl(f, (-58, -12), "I", C["L"])
    return f


def sa_chair(right=True):
    s = 1 if right else -1
    P = (6 * s, 44)
    tor = 90 - 45 * s
    rest = ('A', -90 - 5 * s, 185 if right else -5)
    hip = (_hip_hand(P, tor, -s), 1 if right else -1)
    f, _ = back(P, tor, head=tor + 10 * s, gaze=90 - 15 * s,
                armR=rest if right else hip, armL=hip if right else rest,
                legR=((60, 4), 1) if right else ((64, 4), -1),
                legL=((-64, 4), 1) if right else ((-60, 4), -1),
                footR=(0, 12) if right else (-20, 7), footL=(200, 7) if right else (180, 12))
    chair_front(f, 74 if right else -104)
    _dl(f, (62, -12), "D", C["R"]); _dl(f, (-62, -12), "I", C["L"])
    return f


def wide_chair(right=True):
    f = wide_stance()
    chair_front(f, 58 if right else -88)
    return f


ALL.update({
    "w2c_R": w2_chair, "w2c_L": lambda: w2_chair(False), "revc_R": rev_chair, "revc_L": lambda: rev_chair(False),
    "sac_R": sa_chair, "sac_L": lambda: sa_chair(False), "widec_R": wide_chair, "widec_L": lambda: wide_chair(False),
})


# ------------------------------------------------------------- course 2: everything on a chair
STOOL = "#c2a27c"


def _stool(f, half=24, seat=44):
    for d_ in [f"M{-half},{-seat} L{half},{-seat}", f"M{-half + 2},{-seat} L{-half + 2},0", f"M{half - 2},{-seat} L{half - 2},0"]:
        f.items.append((-1, f'<path d="{d_}" stroke="{STOOL}" stroke-width="4" stroke-linecap="round" fill="none"/>'))
    f._track((-half - 3, 0), (half + 3, seat + 3))


def chair_back(torso=90, head=None, gaze=None, armR=None, armL=None, legs="normal", colored=True, arrows=None):
    """Seated on a chair, seen from BEHIND (chair drawn as a stool so it does not hide the back).
    legs: 'normal' | 'warrior_R' | 'warrior_L' | 'tree_R' | 'tree_L'."""
    P = (0, 52)
    f, j = back(P, torso, head=head, gaze=gaze, armR=armR, armL=armL, colored=colored, arrows=arrows)
    cR = C["R"] if colored else C["body"]
    cL = C["L"] if colored else C["body"]
    shapes = {
        "normal": ([(8, 50), (13, 44), (13, 5), (13, 4)], [(-8, 50), (-13, 44), (-13, 5), (-13, 4)]),
        "warrior_R": ([(8, 50), (40, 45), (44, 5), (55, 4)], [(-8, 50), (-62, 7), (-68, 3)]),
        "warrior_L": ([(8, 50), (62, 7), (68, 3)], [(-8, 50), (-40, 45), (-44, 5), (-55, 4)]),
        "tree_R": ([(8, 50), (36, 38), (-6, 12), (-14, 9)], [(-8, 50), (-13, 44), (-13, 5), (-13, 4)]),
        "tree_L": ([(8, 50), (13, 44), (13, 5), (13, 4)], [(-8, 50), (-36, 38), (6, 12), (14, 9)]),
    }
    r, l = shapes[legs]
    f.line(r, cR, layer=1)
    f.line(l, cL, layer=1)
    _stool(f, half=20 if legs == "normal" else 16)
    if colored:
        if legs.startswith("tree"):
            _dl(f, (26, -12), "D", C["R"]); _dl(f, (-26, -12), "I", C["L"])
        else:
            _dl(f, (r[-1][0] + 4, -12), "D", C["R"])
            _dl(f, (l[-1][0] - 4, -12), "I", C["L"])
    return f, j


def _sho(torso, side):
    neck = add((0, 52), d(torso), T)
    return add(neck, d(torso - 90), 14 * side)


def chair_breath_arms():
    """seated, arms rising out to the sides (back view)."""
    f, _ = chair_back(90, armR=((52, 128), -1), armL=((-52, 128), 1), colored=False,
                      arrows=[([(62, 92), (58, 124)], 6), ([(-62, 92), (-58, 124)], -6)])
    return f


def chair_sidebend(right_arm_up=True):
    s = 1 if right_arm_up else -1
    tor = 90 + 14 * s
    up = _sho(tor, s)
    armup = (add(up, d(90 + 28 * s), 48), -s)
    armdown = ((-30 * s, 40), s)
    f, _ = chair_back(tor, head=tor + 6 * s, armR=armup if right_arm_up else armdown,
                      armL=armdown if right_arm_up else armup)
    return f


def chair_twist():
    f, _ = chair_back(90, head=90, gaze=0, armR=((30, 70), -1), armL=((14, 48), -1),
                      arrows=[([(-20, 82), (20, 88)], -10)])
    return f


def chair_w2(right=True):
    s = 1 if right else -1
    shoR, shoL = _sho(90, 1), _sho(90, -1)
    f, _ = chair_back(90, gaze=0 if right else 180,
                      armR=((shoR[0] + 50, shoR[1]), -1), armL=((shoL[0] - 50, shoL[1]), 1),
                      legs="warrior_R" if right else "warrior_L")
    return f


def chair_rev(right=True):
    s = 1 if right else -1
    tor = 90 + 10 * s
    up = _sho(tor, s)
    top = (add(up, d(90 + 12 * s), 50), -s)
    low = ((-40 * s, 30), s)
    f, _ = chair_back(tor, gaze=tor + 15 * s, armR=top if right else low, armL=low if right else top,
                      legs="warrior_R" if right else "warrior_L")
    return f


def chair_sa(right=True):
    s = 1 if right else -1
    tor = 90 - 35 * s
    up = _sho(tor, -s)
    top = (add(up, d(90 - 30 * s), 50), s)
    rest = ('A', -90 - 10 * s, 180 + 15 * s if right else -15)
    f, _ = chair_back(tor, head=tor + 10 * s, gaze=90 - 15 * s,
                      armR=rest if right else top, armL=top if right else rest,
                      legs="warrior_R" if right else "warrior_L")
    return f


def chair_tree(right=True):
    f, _ = chair_back(90, armR=((3, 88), 1), armL=((-3, 88), -1), legs="tree_R" if right else "tree_L")
    return f


def chair_arms_up():
    f = chair_sit()
    f2 = side((0, 48), 90, head=95, armN=((5, 148), -1), armF=((2, 148), -1),
              legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0,
              extra=[("arrow", [(24, 100), (24, 130)], 0)])
    chair(f2, -10, back_left=True)
    return f2


def chair_fold():
    f = side((0, 48), 35, curve=6, head=-10, face=-60,
             armN=((38, 14), 1), armF=((36, 14), 1),
             legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0)
    chair(f, -10, back_left=True)
    return f


def chair_lean():
    f = side((0, 48), 60, head=55, face=0,
             armN=((32, 50), -1), armF=((30, 50), -1),
             legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0)
    chair(f, -10, back_left=True)
    return f


def chair_march():
    f = side((0, 48), 92, head=90,
             armN=((2, 46), -1), armF=((0, 46), -1),
             legN=('A', 25, -80), footN=0, legF=('A', 2, -88), footF=0, sideN=R, sideF=L,
             extra=[("arrow", [(52, 58), (52, 78)], 0)])
    chair(f, -10, back_left=True)
    return f


def chair_relax():
    f = side((-4, 48), 98, head=80, face=-40,
             armN=((28, 50), -1), armF=((26, 50), -1),
             legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0)
    chair(f, -10, back_left=True)
    return f


def chair_ankles():
    f = side((0, 48), 90, armN=((30, 52), -1), armF=((28, 52), -1),
             legN=('A', 0, -60), footN=-10, legF=('A', 2, -88), footF=0, sideN=R, sideF=L)
    f.items.append((6, '<circle cx="58" cy="-20" r="7" fill="none" stroke="#6b7785" stroke-width="2.2" stroke-dasharray="30 14"/>'))
    f._track((66, 28))
    chair(f, -10, back_left=True)
    return f


ALL.update({
    "c_breath": chair_breath_arms, "c_side_R": chair_sidebend, "c_twist": chair_twist,
    "c_w2_R": chair_w2, "c_w2_L": lambda: chair_w2(False), "c_rev_R": chair_rev, "c_rev_L": lambda: chair_rev(False),
    "c_sa_R": chair_sa, "c_sa_L": lambda: chair_sa(False), "c_tree_R": chair_tree, "c_tree_L": lambda: chair_tree(False),
    "c_arms_up": chair_arms_up, "c_fold": chair_fold, "c_lean": chair_lean, "c_march": chair_march,
    "c_relax": chair_relax, "c_ankles": chair_ankles,
})


def chair_neck():
    f, _ = chair_back(90, head=62, armR=((20, 46), -1), armL=((-20, 46), 1))
    f.arrow([(-14, 144), (8, 138)], bulge=-6)
    return f


def chair_shoulders():
    f, _ = chair_back(90, armR=((20, 46), -1), armL=((-20, 46), 1), colored=False)
    for x in (-14, 14):
        f.items.append((6, f'<circle cx="{x}" cy="-110" r="11" fill="none" stroke="#6b7785" '
                           f'stroke-width="2.4" stroke-dasharray="44 12"/>'))
    return f


def chair_wrists():
    f = side((0, 48), 90, armN=((50, 96), -1), armF=((48, 96), -1),
             legN=('A', 0, -90), legF=('A', 2, -88), footN=0, footF=0)
    f.items.append((6, '<circle cx="54" cy="-96" r="9" fill="none" stroke="#6b7785" stroke-width="2.4" stroke-dasharray="40 16"/>'))
    f._track((66, 108))
    chair(f, -10, back_left=True)
    return f


ALL.update({"c_neck": chair_neck, "c_shoulders": chair_shoulders, "c_wrists": chair_wrists})
