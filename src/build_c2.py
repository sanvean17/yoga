"""Final teaching script, 4 pages A4, rendered twice:
  python3 build_final.py es  -> ../build/yoga_guion_ES.html  (to read aloud)
  python3 build_final.py fr  -> ../build/yoga_guion_FR.html  (same layout, in French, for the teacher)

Every text is a pair (es, fr). Inline tokens: [D] start position, [F] easier
option, [T] transition to next pose. ((...)) grey pause, **x** bold.
"""
import contextlib
import io
import re
import sys

with contextlib.redirect_stdout(io.StringIO()):
    import build as B
from build import fig, fig_fixed, rich

L = sys.argv[1] if len(sys.argv) > 1 else "es"
I = 0 if L == "es" else 1

TOKENS = {
    "[D]": ("DESDE", "DÉPART", "it-d"),
    "[F]": ("MÁS FÁCIL", "PLUS FACILE", "it-f"),
    "[T]": ("→ SIGUIENTE", "→ SUITE", "it-t"),
}
BR_ES = re.compile(r"\b(Inhalamos|inhalamos|Exhalamos|exhalamos|inhalaremos|exhalaremos|Inhalando|Exhalando)\b")
BR_FR = re.compile(r"\b(on inspire|On inspire|on expire|On expire|inspire|expire|inspirera|expirera)\b")
SIDE_FR = re.compile(r"\b(droite?s?|gauches?)\b")


def T(pair):
    """pick language and render markup."""
    t = pair[I] if isinstance(pair, tuple) else pair
    h = rich(t) if L == "es" else rich_fr(t)
    rx = BR_ES if L == "es" else BR_FR

    def br(m):
        w = m.group(1)
        k = "inh" if "inh" in w.lower() or "inspir" in w.lower() else "exh"
        return f'<span class="{k}"><i>{"▲" if k == "inh" else "▼"}</i>{w}</span>'
    h = rx.sub(br, h)
    h = h.replace("[F] ", "").replace("[F]", "")
    VB = {"[C]": ("vc", "EN LA SILLA", "SUR LA CHAISE"), "[CP]": ("vc", "SILLA O PARED", "CHAISE OU MUR"),
          "[S]": ("vs", "SIN APOYO", "SANS APPUI"),
          "[DP]": ("vs", "DE PIE", "DEBOUT"), "[SU]": ("vf", "EN EL SUELO", "AU SOL"),
          "[MC]": ("vx", "MÁS COMPLETO", "PLUS COMPLET")}
    for k, (c, les, lfr) in VB.items():
        h = h.replace(k, f'<span class="vb {c}"><span class="vl">{les if L == "es" else lfr}</span>')
    for k in ("[/C]", "[/CP]", "[/S]", "[/DP]", "[/SU]", "[/MC]"):
        h = h.replace(k, "</span>")
    for k, (es, fr, c) in TOKENS.items():
        h = h.replace(k, f'<span class="it {c}">{es if L == "es" else fr}</span>')
    return h


def rich_fr(t):
    import html as H
    t = H.escape(t, quote=False)
    t = re.sub(r"\(\(([^)]*)\)\)", r'<span class="pause">\1</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return SIDE_FR.sub(lambda m: f'<span class="{"sr" if m.group(1).startswith("dr") else "sl"}">{m.group(1)}</span>', t)


def card(poses, name, badge, text, mh=20, mw=30, row=False):
    figs = "".join(fig(p, max_w=mw, max_h=mh * 1.2, cap=0.15) for p in poses)
    b = f' <span class="badge b-n">{T(badge)}</span>' if badge else ""
    return (f'<div class="qc"><div class="qf{" row" if row else ""}">{figs}</div>'
            f'<div class="qt"><div class="qn">{T(name)}{b}</div><div class="qcue">{T(text)}</div></div></div>')


def band(num, title, time, opt=False):
    o = f'<span class="opt">{"opcional" if L == "es" else "optionnel"}</span>' if opt else ""
    return (f'<div class="qband"><span class="secn">{num}</span><b>{T(title)}</b>{o}'
            f'<span class="time">{time}</span></div>')


def grid(cards, cols=2):
    return f'<div class="qgrid c{cols}">' + "".join(cards) + "</div>"


def steps(items, cols=1):
    return (f'<ol class="st c{cols}">' + "".join(
        f'<li><span class="nn">{n}</span><span>{T(t)}</span></li>' for n, t in items) + "</ol>")


def note(fr_text):
    """teacher-only note, always in French, grey."""
    return f'<div class="pm"><b>Pour moi</b> (ne pas lire) : {fr_text}</div>'


def strip(frames, scale):
    cells = []
    for i, (p, cap, br) in enumerate(frames):
        if i:
            cells.append('<div class="sarrow">→</div>')
        poses = p if isinstance(p, tuple) else (p,)
        svg = '<span class="sor">/</span>'.join(fig_fixed(x, scale) for x in poses)
        bb = ""
        if br == "inh":
            bb = f'<span class="sb inh"><i>▲</i>{"Inhalamos" if L == "es" else "Inspire"}</span>'
        elif br == "exh":
            bb = f'<span class="sb exh"><i>▼</i>{"Exhalamos" if L == "es" else "Expire"}</span>'
        elif br:
            bb = f'<span class="sb n">{T(br)}</span>'
        cells.append(f'<div class="sf"><div class="sfig">{svg}</div><div class="scap">{T(cap)}</div>{bb}</div>')
    return f'<div class="strip"><div class="srow">{"".join(cells)}</div></div>'


RESP = lambda n: (f"{n} resp.", f"{n} resp.")  # noqa: E731


# ===================================================================
# COURSE 2 (v3) · chairs WITH armrests · every card shows two versions
# ===================================================================
import poses as _poses
_poses.ARM["on"] = True

LBL = {"S": ("SILLA", "CHAISE", "lc"), "P": ("DE PIE", "DEBOUT", "lp"), "F": ("SUELO", "SOL", "lf")}


def card2(a_pose, b_pose, b_kind, name, badge, text, mh=19, a_kind="S"):
    def one(p, k):
        es_, fr_, c = LBL[k]
        return (f'<div class="f2">{fig(p, max_w=30, max_h=mh * 1.15, cap=0.14)}'
                f'<span class="fl {c}">{es_ if L == "es" else fr_}</span></div>')
    import re as _re
    name = tuple(_re.sub(r"^[A-Z] · ", "", x) for x in name)
    b = f' <span class="badge b-n">{T(badge)}</span>' if badge else ""
    return (f'<div class="qc c2"><div class="qf row2">{one(a_pose, a_kind)}{one(b_pose, b_kind)}</div>'
            f'<div class="qt"><div class="qn">{T(name)}{b}</div><div class="qcue">{T(text)}</div></div></div>')


LBL["X"] = ("MÁS COMPLETO", "PLUS COMPLET", "lx")


def card3(a, b, c, name, badge, text, mh=18):
    def one(p, k):
        es_, fr_, cl = LBL[k]
        return (f'<div class="f2">{fig(p, max_w=26, max_h=mh * 1.15, cap=0.14)}'
                f'<span class="fl {cl}">{es_ if L == "es" else fr_}</span></div>')
    b_ = f' <span class="badge b-n">{T(badge)}</span>' if badge else ""
    return (f'<div class="qc c2"><div class="qf row2">{one(a, "S")}{one(b, "P")}{one(c, "X")}</div>'
            f'<div class="qt"><div class="qn">{T(name)}{b_}</div><div class="qcue">{T(text)}</div></div></div>')


def menu_silla():
    items = [
        ("c_march", ("Marcha sentados: un pie, el otro.", "Marche assise : un pied, puis l’autre.")),
        ("legext_c", ("Estiramos una pierna delante y volvemos; derecha, izquierda.", "On tend une jambe devant et on revient ; droite, gauche.")),
        ("heeltoe_chair", ("Talón en el suelo… punta en el suelo.", "Talon au sol… pointe au sol.")),
        ("chair_cat", ("Gato-vaca: pequeños movimientos de la pelvis.", "Chat-vache : petits mouvements du bassin.")),
        ("cactus_c", ("Abrir el pecho, brazos en cactus.", "Ouvrir la poitrine, bras en cactus.")),
        ("c_side_R", ("Inclinación lateral, un lado y el otro.", "Inclinaison latérale, un côté puis l’autre.")),
        ("chair_hamstring", ("Talón delante, el pecho un poco hacia delante.", "Talon devant, la poitrine un peu vers l’avant.")),
        ("fig4_chair", ("El número 4 para la cadera.", "Le chiffre 4 pour la hanche.")),
        ("calf_chair", ("Pierna estirada, puntas del pie hacia nosotros.", "Jambe tendue, pointes du pied vers soi.")),
    ]
    cells = "".join(f'<div class="mi">{fig(p, max_w=18, max_h=13, cap=0.1)}<span>{T(t)}</span></div>' for p, t in items)
    title = ("Menú silla · mientras otros hacen la versión de pie o en el suelo, en la silla podemos hacer:"
             if L == "es" else
             "Menu chaise · pendant que d’autres font la version debout ou au sol, sur la chaise on peut faire :")
    return f'<div class="menu"><div class="mt">{title}</div><div class="mg">{cells}</div></div>'


def part(n, es_t, fr_t):
    return (f'<div class="part"><span>{"PARTE" if L == "es" else "PARTIE"} {n}</span>'
            f'{es_t if L == "es" else fr_t}</div>')


def para(es_t, fr_t):
    return f'<div class="cue1">{T((es_t, fr_t))}</div>'


SUN_SEAT = [
    ("chair_sit", ("1 Corazón", "1 Cœur"), "exh"), ("c_arms_up", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("c_fold", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("chair_hamstring", ("5 Pierna D delante", "5 Jambe D devant"), "exh"),
    ("c_arms_up", ("6 Brazos arriba", "6 Bras en haut"), "inh"), ("chair_sit", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STAND = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("arms_up_chair", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("fold", ("3 Flexión", "3 Flexion"), "exh"), (("dog_chair", "half_lift_thighs"), ("4 Espalda larga", "4 Dos long"), "inh"),
    ("lunge_chair_R", ("5 Pie D atrás", "5 Pied D arrière"), "exh"),
    ("arms_up_chair", ("6 Brazos arriba", "6 Bras en haut"), "inh"), ("heart_chair", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STEPS = [
    (1, ("**Corazón.** Espalda larga, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Dos long, paumes jointes devant la poitrine. On expire.")),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos, hasta donde es cómodo.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte, jusqu’où c’est confortable.")),
    (3, ("**Flexión (posición 1).** Exhalamos: el pecho baja hacia los muslos, la espalda se redondea, la cabeza cuelga. "
         "[DP]Rodillas bien dobladas, manos en las piernas.[/DP]",
         "**Flexion (position 1).** On expire : la poitrine descend vers les cuisses, le dos s’arrondit, la tête pend. "
         "[DP]Genoux bien pliés, mains sur les jambes.[/DP]")),
    (4, ("**Espalda larga (posición 2).** Inhalamos: manos en los muslos, por encima de las rodillas. Subimos un poco: la "
         "espalda plana e inclinada, como una mesa. Miramos al suelo. "
         "[DP]Manos en el respaldo o en la pared, caminamos un poco atrás; o manos en los muslos.[/DP]",
         "**Dos long (position 2).** On inspire : mains sur les cuisses, au-dessus des genoux. On remonte un peu : le dos "
         "plat et incliné, comme une table. Regard au sol. [DP]Mains sur le dossier ou au mur, on recule un peu ; ou mains "
         "sur les cuisses.[/DP]")),
    (5, ("**Pierna derecha delante.** Exhalamos: subimos el torso; estiramos la pierna derecha delante, talón en el "
         "suelo. ((2 resp.)) Inhalamos, el pie vuelve. "
         "[DP]El pie derecho da un paso atrás, talón arriba, una mano en el apoyo; después vuelve.[/DP]",
         "**Jambe droite devant.** On expire : on redresse le buste ; on allonge la jambe droite devant, talon au sol. "
         "((2 resp.)) On inspire, le pied revient. [DP]Le pied droit recule d’un pas, talon levé, une main sur l’appui ; "
         "puis il revient.[/DP]")),
    (6, ("**Brazos arriba.** Inhalamos, subimos los brazos.", "**Bras en haut.** On inspire, on monte les bras.")),
    (7, ("**Corazón.** Exhalamos, manos delante del pecho. ((1 resp.))",
         "**Cœur.** On expire, mains devant la poitrine. ((1 resp.))")),
]

P_ALL = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 2 · guion de la profesora · 1 hora · de pie, en la silla o en el suelo" if L == "es"
     else "Cours 2 · version française · même ordre et mêmes lettres que la version espagnole") +
    '</div><h1>' + ("Yoga suave · cada uno a su manera" if L == "es" else "Yoga doux · chacun à sa façon") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="fl lc">SILLA</span> <span class="fl lp">DE PIE CON APOYO</span> <span class="fl lf">SUELO</span> <span class="fl lx">MÁS COMPLETO</span>'
     if L == "es" else
     '<span class="fl lc">CHAISE</span> <span class="fl lp">DEBOUT AVEC APPUI</span> <span class="fl lf">SOL</span> <span class="fl lx">PLUS COMPLET</span>') +
    '</div></div>',
    note("texte normal = <b>version chaise</b>, faisable par tous. Blocs bleus « DE PIE » / verts « EN EL SUELO » = options. "
         "<b>Chaises avec accoudoirs</b> : on s’assoit au bord, devant les accoudoirs, pour les guerriers ; les accoudoirs "
         "servent d’appui. Pas de respiration du feu ni de rétention (déconseillées : tension, cœur, vertiges). "
         "Groupe hétérogène : propose <b>3 niveaux</b> (chaise / debout avec appui / sol ou plus complet) ; ceux qui restent assis suivent le <b>menu chaise</b> pendant les variantes debout ou au sol. On garde toutes les postures pour tester ; en retard : saute la déesse ou les essuie-glaces. Jamais la relaxation."),
    band(1, ("Bienvenida · las reglas", "Accueil · les règles"), "0:00 – 0:04"),
    grid([card2("chair_sit", "tadasana", "P", ("Cada uno a su manera", "Chacun à sa façon"), None, (
        "Hola a todos, bienvenidos. Hoy todo se puede hacer **de pie, en la silla o en el suelo**: os enseñaré las "
        "opciones y cada uno elige. Lo más importante: **no forzamos nunca. Escuchamos nuestro cuerpo.** Si algo duele o "
        "no es posible, no pasa nada: descansamos, o lo hacemos poco a poco. "
        "La respiración es la clave para soltar y ganar amplitud. La amplitud llega poco a poco, milímetro a milímetro. "
        "No pasa nada si hoy no podemos bajar mucho: no es el objetivo.",
        "Bonjour à tous, bienvenue. Aujourd’hui tout peut se faire **debout, sur la chaise ou au sol** : je vous montrerai "
        "les options et chacun choisit. Le plus important : **on ne force jamais. On écoute son corps.** Si quelque chose "
        "fait mal ou n’est pas possible, ce n’est pas grave : on se repose, ou on y va petit à petit. La respiration est la "
        "clé pour relâcher et gagner en amplitude. L’amplitude vient peu à peu, millimètre par millimètre. Ce n’est pas "
        "grave si aujourd’hui on ne peut pas descendre bas : ce n’est pas le but."))], cols=1),
    band(2, ("Respiración de inicio", "Respiration du début"), "0:04 – 0:10"),
    grid([
        card2("r_chair", "r_floor", "F", ("A · Respiración en tres partes", "A · Respiration en trois parties"), ("5 resp.", "5 resp."), (
            "Cerramos los ojos si queréis. Una mano en el abdomen. Inhalamos: el abdomen se llena suavemente… las "
            "costillas se abren… el pecho sube un poco. Exhalamos despacio: el pecho, las costillas, el abdomen. Como una "
            "ola. Sin forzar. ((5 respiraciones))",
            "On ferme les yeux si vous voulez. Une main sur le ventre. On inspire : le ventre se remplit doucement… les côtes "
            "s’ouvrent… la poitrine monte un peu. On expire lentement : la poitrine, les côtes, le ventre. Comme une vague. "
            "Sans forcer. ((5 respirations))")),
        card2("c_breath", "arms_up", "P", ("B · Brazos y respiración", "B · Bras et respiration"), ("5 veces", "5 fois"), (
            "Inhalamos por la nariz y abrimos o subimos los brazos, despacio. Exhalamos y los bajamos lentamente. El "
            "movimiento dura lo mismo que la respiración. ((5 veces)) Los brazos suben solo hasta donde es cómodo.",
            "On inspire par le nez et on ouvre ou on monte les bras, lentement. On expire et on les redescend lentement. Le "
            "mouvement dure autant que la respiration. ((5 fois)) Les bras montent seulement jusqu’où c’est confortable.")),
    ]),
    band(3, ("Calentamiento · en la silla o en el suelo", "Échauffement · sur la chaise ou au sol"), "0:10 – 0:22"),
    grid([
        card2("c_neck", "seated_neck", "F", ("C · Cuello", "C · Cou"), ("3 resp./lado", "3 resp./côté"), (
            "Exhalamos: oreja derecha hacia el hombro derecho. ((3 resp.)) Al centro, y al otro lado. Después giramos la "
            "cabeza despacio: miramos a la derecha… a la izquierda. Movimiento pequeño.",
            "On expire : oreille droite vers l’épaule droite. ((3 resp.)) Au centre, puis de l’autre côté. Puis on tourne la "
            "tête lentement : on regarde à droite… à gauche. Petit mouvement.")),
        card2("c_shoulders", "seated_shoulders", "F", ("D · Hombros", "D · Épaules"), ("5 + 5", "5 + 5"), (
            "Inhalamos, subimos los hombros. Exhalamos, atrás y abajo. Cinco círculos hacia atrás… cinco hacia delante.",
            "On inspire, on monte les épaules. On expire, en arrière et en bas. Cinq cercles vers l’arrière… cinq vers l’avant.")),
        card2("a_chair", "a_stand", "P", ("E · Círculos de brazos", "E · Cercles de bras"), ("5 + 5", "5 + 5"), (
            "Brazos a los lados, a la altura de los hombros o más bajos. Pequeños círculos hacia delante… hacia atrás. "
            "Después, círculos grandes con un brazo, despacio.",
            "Bras sur les côtés, à hauteur d’épaules ou plus bas. Petits cercles vers l’avant… vers l’arrière. Puis de grands "
            "cercles avec un bras, lentement.")),
        card2("sh_chair", "sh_stand", "P", ("F · Estirar los hombros", "F · Étirer les épaules"), ("3 resp./lado", "3 resp./côté"), (
            "El brazo derecho cruza delante del pecho; la mano izquierda lo acerca suavemente, por encima del codo. Hombros "
            "bajos. ((3 resp.)) Cambiamos de brazo.",
            "Le bras droit croise devant la poitrine ; la main gauche le rapproche doucement, au-dessus du coude. Épaules "
            "basses. ((3 resp.)) On change de bras.")),
        card2("c_wrists", "wrists", "F", ("G · Muñecas y tobillos", "G · Poignets et chevilles"), ("5 + 5", "5 + 5"), (
            "Círculos con las muñecas, cinco hacia cada lado. Después levantamos un poco un pie: círculos con el tobillo. "
            "Cambiamos de pie.",
            "Cercles avec les poignets, cinq de chaque côté. Puis on soulève un peu un pied : cercles avec la cheville. "
            "On change de pied.")),
        card2("c_side_R", "sidebend_R", "F", ("H · Inclinación lateral", "H · Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), (
            "Antebrazo izquierdo en el reposabrazos. Inhalamos, brazo derecho arriba. Exhalamos, nos inclinamos a la "
            "izquierda. ((3 resp.)) Cambiamos. [SU]Mano izquierda en el suelo, junto a la cadera.[/SU]",
            "Avant-bras gauche sur l’accoudoir. On inspire, bras droit en haut. On expire, on se penche à gauche. "
            "((3 resp.)) On change. [SU]Main gauche au sol, près de la hanche.[/SU]")),
        card2("c_twist", "seated_twist", "F", ("I · Torsión sentados", "I · Torsion assise"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda en la rodilla derecha, mano derecha en el reposabrazos derecho. Inhalamos, espalda larga. "
            "Exhalamos, giramos a la derecha. ((3 resp.)) Cambiamos. [SU]Mano derecha en el suelo, detrás.[/SU]",
            "Main gauche sur le genou droit, main droite sur l’accoudoir droit. On inspire, dos long. On expire, on tourne à "
            "droite. ((3 resp.)) On change. [SU]Main droite au sol, derrière.[/SU]")),
        card2("chair_cat", "cat", "F", ("J · Gato-vaca", "J · Chat-vache"), ("5 veces", "5 fois"), (
            "Manos en las rodillas. Inhalamos, abrimos el pecho. Exhalamos, redondeamos la espalda. "
            "[SU]A cuatro apoyos, si las rodillas están cómodas.[/SU]",
            "Mains sur les genoux. On inspire, on ouvre la poitrine. On expire, dos rond. [SU]À quatre pattes, si les genoux "
            "sont à l’aise.[/SU]")),
        card2("chest_chair", "chest_stand", "P", ("K · Abrir el pecho", "K · Ouvrir la poitrine"), ("3 resp.", "3 resp."), (
            "Manos en los reposabrazos. Empujamos suavemente y el pecho se abre hacia delante; hombros atrás. ((3 resp.))",
            "Mains sur les accoudoirs. On pousse doucement et la poitrine s’ouvre vers l’avant ; épaules en arrière. "
            "((3 resp.))")),
    ], cols=3),
    part(1, "De pie o en la silla · 0:22 – 0:44", "Debout ou sur la chaise · 0:22 – 0:44"),
    menu_silla(),
    band(4, ("Antes del saludo: aprendemos tres posiciones", "Avant la salutation : on apprend trois positions"), "0:22 – 0:25"),
    note("explique-les une par une, montre, et laisse-les essayer. <b>« Dos long » ne veut pas dire dos vertical</b> : on se "
         "penche en avant depuis les hanches, dos plat. La dernière fois ils restaient droits."),
    grid([
        card2("c_fold", "fold", "P", ("1 · Flexión", "1 · Flexion"), None, (
            "Dejamos caer el pecho hacia los muslos. La espalda se redondea, la cabeza y los brazos cuelgan. Rodillas "
            "dobladas. Todo está relajado.",
            "On laisse tomber la poitrine vers les cuisses. Le dos s’arrondit, la tête et les bras pendent. Genoux pliés. "
            "Tout est relâché.")),
        card2("c_lean", "half_lift_thighs", "P", ("2 · Espalda larga", "2 · Dos long"), None, (
            "Manos en los muslos, por encima de las rodillas. La espalda **no** está vertical: nos inclinamos hacia delante "
            "desde las caderas y la espalda queda plana, como una mesa. Miramos al suelo.",
            "Mains sur les cuisses, au-dessus des genoux. Le dos n’est **pas** vertical : on se penche en avant depuis les "
            "hanches et le dos reste plat, comme une table. Regard au sol.")),
        card2("chair_sit", "dog_chair", "P", ("3 · Manos en el apoyo", "3 · Mains sur l’appui"), None, (
            "Sentados: manos en las rodillas. [DP]Manos en el respaldo o en la pared, a la altura de las caderas; caminamos "
            "atrás hasta que la espalda queda larga.[/DP]",
            "Assis : mains sur les genoux. [DP]Mains sur le dossier ou au mur, à hauteur des hanches ; on recule jusqu’à avoir "
            "le dos long.[/DP]")),
    ], cols=3),
    band("4b", ("Encontrar la espalda larga · tres maneras", "Trouver le dos long · trois façons"), "", ),
    note("ne cherche pas un dos parfaitement plat : à cet âge c’est souvent impossible. On cherche un dos <b>long</b>. "
         "Montre-toi <b>de profil</b> : d’abord dos rond (« así no »), puis dos long (« así sí »). Plier les genoux et "
         "mettre les mains plus haut sur les cuisses aide beaucoup."),
    grid([
        card2("chair_cat", "chair_cow", "S", ("Gato, vaca… y en medio", "Chat, vache… et au milieu"), None, (
            "Manos en las rodillas. Redondeamos la espalda, como el gato… Ahora la arqueamos, como la vaca… Y nos "
            "quedamos **en el medio**: esto es la espalda larga. No buscamos una espalda perfecta: buscamos una espalda "
            "larga.",
            "Mains sur les genoux. On arrondit le dos, comme le chat… Maintenant on le creuse, comme la vache… Et on reste "
            "**au milieu** : c’est le dos long. On ne cherche pas un dos parfait : on cherche un dos long.")),
        card2("c_lean", "half_lift_thighs", "P", ("Cerrar el libro", "Fermer le livre"), None, (
            "Las manos en el pliegue de las caderas. Nos inclinamos hacia delante como si cerráramos un libro: las manos se "
            "quedan atrapadas. Nos doblamos aquí, no en la espalda. **Enseñamos el collar**: el pecho va hacia delante, "
            "no hacia abajo. Miramos el suelo un metro delante. Rodillas dobladas, manos más arriba en los muslos.",
            "Les mains dans le pli des hanches. On se penche en avant comme si on fermait un livre : les mains se "
            "coincent. On se plie ici, pas dans le dos. **On montre son collier** : la poitrine va vers l’avant, pas vers "
            "le bas. Regard au sol un mètre devant. Genoux pliés, mains plus haut sur les cuisses.")),
        card2("chair_sit", "wall_hinge", "P", ("Con la pared", "Avec le mur"), None, (
            "Sentados: nos sentamos al borde y llevamos el pecho hacia delante, sin redondear. "
            "[DP]De espaldas a la pared, a un palmo. Rodillas un poco dobladas, manos en los muslos. Llevamos el culo hacia "
            "atrás hasta tocar la pared, como si cerráramos la puerta del coche con el culo. La espalda se queda larga. "
            "Volvemos empujando las caderas hacia delante.[/DP]",
            "Assis : on s’assoit au bord et on emmène la poitrine vers l’avant, sans arrondir. [DP]Dos au mur, à une main "
            "du mur. Genoux un peu pliés, mains sur les cuisses. On recule les fesses jusqu’à toucher le mur, comme si on "
            "fermait la portière de la voiture avec les fesses. Le dos reste long. On revient en poussant les hanches vers "
            "l’avant.[/DP]")),
    ], cols=3),
    band(5, ("Saludo al sol · sentados o de pie · 3 rondas", "Salutation au soleil · assis ou debout · 3 rondes"), "0:25 – 0:31"),
    note("ronde 1 lente avec tout le texte, jambe droite ; ronde 2 jambe gauche, moins de mots ; ronde 3 un mouvement par "
         "respiration (optionnelle)."),
    '<div class="keep2"><div class="sl2">' + ("SENTADOS" if L == "es" else "ASSIS") + '</div>' + strip(SUN_SEAT, 0.13) +
    '<div class="sl2">' + ("DE PIE" if L == "es" else "DEBOUT") + '</div>' + strip(SUN_STAND, 0.13) + '</div>',
    steps(SUN_STEPS),
    band(6, ("Guerreros, triángulo y diosa", "Guerriers, triangle et déesse"), "0:31 – 0:40"),
    note("<b>avec accoudoirs</b> : ils s’assoient tout au bord, devant les accoudoirs, pour libérer les jambes. Côté droit "
         "d’abord, puis gauche. Debout : chaise ou mur à côté de la jambe avant."),
    grid([
        card2("w1_chair", "w1_stand", "P", ("L · Guerrero I", "L · Guerrier I"), ("3 resp./lado", "3 resp./côté"), (
            "**Cómo entramos:** nos sentamos al borde, delante de los reposabrazos, y giramos un poco hacia la izquierda. "
            "El pie derecho delante, rodilla encima del tobillo. La pierna izquierda va atrás, al lado de la silla: la "
            "rodilla mira al suelo, la punta del pie apoyada. Inhalamos, brazos arriba o manos en la cintura. ((3 resp.)) "
            "Cambiamos de lado. [DP]Un paso largo atrás con el pie izquierdo, rodilla derecha doblada, una mano en la silla "
            "si hace falta.[/DP]",
            "**Comment on entre :** on s’assoit au bord, devant les accoudoirs, et on tourne un peu vers la gauche. Le pied "
            "droit devant, genou au-dessus de la cheville. La jambe gauche va en arrière, à côté de la chaise : le genou "
            "regarde le sol, la pointe du pied posée. On inspire, bras en haut ou mains sur la taille. ((3 resp.)) On change "
            "de côté. [DP]Un grand pas en arrière avec le pied gauche, genou droit plié, une main sur la chaise si besoin.[/DP]")),
        card2("c_w2_R", "w2c_R", "P", ("M · Guerrero II", "M · Guerrier II"), ("3 resp./lado", "3 resp./côté"), (
            "**Cómo entramos:** al borde de la silla. La pierna derecha se abre hacia la derecha, delante del reposabrazos, "
            "rodilla encima del tobillo. La pierna izquierda se estira hacia atrás y a la izquierda, el pie apoyado. "
            "Inhalamos, brazos en cruz; miramos la mano derecha. ((3 resp.)) Cambiamos de lado. "
            "[DP]Pies separados, pie derecho hacia fuera, rodilla derecha encima del tobillo; mano en la silla si hace "
            "falta.[/DP]",
            "**Comment on entre :** au bord de la chaise. La jambe droite s’ouvre vers la droite, devant l’accoudoir, genou "
            "au-dessus de la cheville. La jambe gauche s’allonge en arrière et à gauche, pied posé. On inspire, bras en "
            "croix ; regard sur la main droite. ((3 resp.)) On change de côté. [DP]Pieds écartés, pied droit vers "
            "l’extérieur, genou droit au-dessus de la cheville ; main sur la chaise si besoin.[/DP]")),
        card2("t_chair", "t_stand", "P", ("N · Triángulo", "N · Triangle"), ("3 resp./lado", "3 resp./côté"), (
            "Desde el Guerrero II sentado, estiramos un poco la rodilla derecha. Exhalamos: nos inclinamos a la derecha; "
            "antebrazo derecho en el muslo o en el reposabrazos; brazo izquierdo arriba. ((3 resp.)) Cambiamos. "
            "[DP]Piernas estiradas; la mano de abajo entre la cintura y la rodilla, nunca empuja.[/DP]",
            "Depuis le Guerrier II assis, on tend un peu le genou droit. On expire : on se penche à droite ; avant-bras droit "
            "sur la cuisse ou sur l’accoudoir ; bras gauche en haut. ((3 resp.)) On change. [DP]Jambes tendues ; la main du "
            "bas entre la taille et le genou, elle ne pousse jamais.[/DP]")),
        card2("d_chair", "d_stand", "P", ("Diosa (extra)", "Déesse (en plus)"), ("4 resp.", "4 resp."), (
            "Al borde de la silla, piernas bien separadas, puntas de los pies hacia fuera, rodillas en la misma dirección. "
            "Brazos en cactus: codos a la altura de los hombros, manos arriba. Inhalamos, abrimos el pecho. ((4 resp.)) "
            "[DP]Pies separados, rodillas un poco dobladas, sin bajar mucho; una mano en la silla si hace falta.[/DP]",
            "Au bord de la chaise, jambes bien écartées, pointes des pieds vers l’extérieur, genoux dans la même direction. "
            "Bras en cactus : coudes à hauteur d’épaules, mains en haut. On inspire, on ouvre la poitrine. ((4 resp.)) "
            "[DP]Pieds écartés, genoux un peu pliés, sans descendre beaucoup ; une main sur la chaise si besoin.[/DP]")),
    ]),
    band(7, ("Equilibrio · elegimos una o dos", "Équilibre · on en choisit une ou deux"), "0:40 – 0:44"),
    note("ne fais pas tous les équilibres : <b>un ou deux par séance</b>, et change d’une semaine à l’autre. Par exemple "
         "cette semaine : un pied devant l’autre + aigle ; une autre semaine : arbre + jambe sur le côté."),
    grid([card3("eagle_c", "eagle_p", "eagle_f", ("Águila · tres niveles", "Aigle · trois niveaux"), ("3 resp./lado", "3 resp./côté"), (
        "**En la silla:** espalda larga; cruzamos una pierna delante de la otra, sin enrollar el pie. Brazos delante: "
        "cruzamos el brazo derecho por encima del izquierdo y doblamos los codos. Si no llegamos, nos abrazamos: las manos en "
        "los hombros. ((3 resp.)) Cambiamos. "
        "[DP]Una mano en la silla o en la pared. Cruzamos un poco una pierna delante de la otra: los dedos del pie cruzado se "
        "quedan en el suelo, como una muleta. Brazos de águila o manos en los hombros.[/DP]"
        "[MC]Doblamos un poco las rodillas y cruzamos el muslo por encima del otro, el pie sin apoyar. No hace "
        "falta enrollar el pie detrás de la pantorrilla.[/MC]",
        "**Sur la chaise :** dos long ; on croise une jambe devant l’autre, sans enrouler le pied. Bras devant : on croise le "
        "bras droit par-dessus le gauche et on plie les coudes. Si on n’y arrive pas, on se fait un câlin : mains sur les "
        "épaules. ((3 resp.)) On change. [DP]Une main sur la chaise ou au mur. On croise un peu une jambe devant l’autre : "
        "les orteils du pied croisé restent au sol, comme une béquille. Bras d’aigle ou mains sur les épaules.[/DP]"
        "[MC]On plie un peu les genoux et on croise la cuisse par-dessus l’autre, pied décollé. Pas besoin "
        "d’enrouler le pied derrière le mollet.[/MC]"))], cols=1),
    grid([
        card2("c_tree_R", "tree_wall", "P", ("O · Árbol", "O · Arbre"), ("3 resp./lado", "3 resp./côté"), (
            "Talón derecho en el tobillo izquierdo, rodilla derecha hacia fuera. Manos al pecho, o brazos arriba como ramas. "
            "Miramos un punto fijo. ((3 resp.)) Cambiamos. [DP]Una mano en la silla o en la pared; dedos del pie en el suelo, o "
            "el pie en la pantorrilla, nunca sobre la rodilla.[/DP]",
            "Talon droit sur la cheville gauche, genou droit vers l’extérieur. Mains à la poitrine, ou bras en haut comme des "
            "branches. Regard sur un point fixe. ((3 resp.)) On change. [DP]Une main sur la chaise ou au mur ; orteils au sol, "
            "ou le pied sur le mollet, jamais sur le genou.[/DP]")),
        card2("knee_chair", "tandem_stand", "P", ("P · Un pie delante del otro", "P · Un pied devant l’autre"), ("4 resp./lado", "4 resp./côté"), (
            "Sentados: levantamos un poco la rodilla derecha y la sostenemos, brazos abiertos para el equilibrio. "
            "((4 resp.)) Cambiamos. [DP]Una mano en la silla o en la pared. El pie derecho justo delante del izquierdo, "
            "como en una línea. Miramos al frente. ((4 resp.)) Cambiamos de pie.[/DP]",
            "Assis : on soulève un peu le genou droit et on le tient, bras ouverts pour l’équilibre. ((4 resp.)) On change. "
            "[DP]Une main sur la chaise ou au mur. Le pied droit juste devant le gauche, comme sur une ligne. Regard devant. "
            "((4 resp.)) On change de pied.[/DP]")),
        card2("side_leg_chair", "side_leg_stand", "P", ("Pierna al lado", "Jambe sur le côté"), ("5 veces/lado", "5 fois/côté"), (
            "Sentados: estiramos la pierna derecha hacia el lado, talón en el suelo, y volvemos. ((5 veces)) Cambiamos. "
            "[DP]De pie detrás de la silla o junto a la pared, una mano apoyada. Levantamos despacio la pierna derecha hacia "
            "el lado, la punta del pie mira al frente, espalda recta. Bajamos despacio.[/DP]",
            "Assis : on allonge la jambe droite sur le côté, talon au sol, et on revient. ((5 fois)) On change. [DP]Debout "
            "derrière la chaise ou près du mur, une main en appui. On lève lentement la jambe droite sur le côté, la pointe "
            "du pied regarde devant, dos droit. On redescend lentement.[/DP]")),
        card2("airplane_chair", "airplane_stand", "P", ("Brazo arriba, pie arriba", "Bras en haut, pied levé"), ("3 resp./lado", "3 resp./côté"), (
            "Sentados: subimos el brazo izquierdo y, a la vez, levantamos un poco el pie izquierdo. Miramos un punto fijo. "
            "((3 resp.)) Cambiamos de lado. [DP]La mano derecha en la silla o en la pared. Subimos el brazo izquierdo; "
            "después levantamos un poco el pie izquierdo. ((3 resp.)) Cambiamos.[/DP]",
            "Assis : on monte le bras gauche et, en même temps, on soulève un peu le pied gauche. Regard sur un point fixe. "
            "((3 resp.)) On change de côté. [DP]La main droite sur la chaise ou au mur. On monte le bras gauche ; puis on "
            "soulève un peu le pied gauche. ((3 resp.)) On change.[/DP]")),
    ]),
    part(2, "En la silla o en el suelo · 0:44 – 1:00", "Sur la chaise ou au sol · 0:44 – 1:00"),
    band(8, ("Caderas, piernas y espalda · estiramientos", "Hanches, jambes et dos · étirements"), "0:44 – 0:51"),
    note("ceux qui vont au sol descendent doucement, une main sur la chaise. Les autres restent assis."),
    grid([
        card2("chair_sit", "butterfly", "F", ("Q · Mariposa", "Q · Papillon"), ("4 resp.", "4 resp."), (
            "Rodillas separadas, manos en los muslos. Inhalamos, espalda larga. Exhalamos, nos inclinamos un poco. "
            "[SU]Plantas de los pies juntas; no empujamos las rodillas.[/SU]",
            "Genoux écartés, mains sur les cuisses. On inspire, dos long. On expire, on se penche un peu. "
            "[SU]Plantes des pieds jointes ; on ne pousse pas les genoux.[/SU]")),
        card2("fig4_chair", "fig4_floor", "F", ("R · El número 4", "R · Le chiffre 4"), ("4 resp./lado", "4 resp./côté"), (
            "Tobillo derecho sobre la rodilla izquierda, pie flexionado. Si no es cómodo, el pie se queda en el suelo. "
            "((4 resp.)) Cambiamos. [SU]Tumbados, pie izquierdo en el suelo.[/SU]",
            "Cheville droite sur le genou gauche, pied fléchi. Si ce n’est pas confortable, le pied reste au sol. "
            "((4 resp.)) On change. [SU]Allongés, pied gauche au sol.[/SU]")),
        card2("chair_hamstring", "leg_stretch", "F", ("S · Estirar la pierna", "S · Étirer la jambe"), ("4 resp./lado", "4 resp./côté"), (
            "Pierna derecha estirada delante, talón en el suelo. Exhalamos, el pecho un poco hacia delante. ((4 resp.)) "
            "Cambiamos. [SU]Tumbados: cogemos la pierna detrás del muslo, rodilla doblada.[/SU]",
            "Jambe droite allongée devant, talon au sol. On expire, la poitrine un peu vers l’avant. ((4 resp.)) On change. "
            "[SU]Allongés : on tient la jambe derrière la cuisse, genou plié.[/SU]")),
        card2("chair_knee", "knees_chest", "F", ("T · Rodilla al pecho", "T · Genou poitrine"), ("3 resp./lado", "3 resp./côté"), (
            "Abrazamos la rodilla derecha, espalda larga. ((3 resp.)) Cambiamos. [SU]Tumbados: las dos rodillas al pecho; "
            "nos balanceamos un poco.[/SU]",
            "On serre le genou droit, dos long. ((3 resp.)) On change. [SU]Allongés : les deux genoux à la poitrine ; on se "
            "balance un peu.[/SU]")),
        card2("chair_sit", "wipers", "F", ("U · Limpiaparabrisas", "U · Essuie-glaces"), ("6 veces", "6 fois"), (
            "Sentados, rodillas juntas: las llevamos un poco a la derecha… y a la izquierda, despacio. "
            "[SU]Tumbados, pies separados: rodillas a la derecha y a la izquierda.[/SU]",
            "Assis, genoux serrés : on les emmène un peu à droite… puis à gauche, lentement. [SU]Allongés, pieds écartés : "
            "genoux à droite et à gauche.[/SU]")),
        card2("cactus_c", "cactus_f", "F", ("Pecho abierto, brazos en cactus", "Poitrine ouverte, bras en cactus"), ("4 resp.", "4 resp."), (
            "Brazos en cactus: codos a la altura de los hombros, manos arriba. Inhalamos, abrimos el pecho y llevamos los codos "
            "un poco atrás. ((4 resp.)) [SU]Tumbados, rodillas dobladas o piernas estiradas: brazos en cactus en el suelo, el "
            "dorso de las manos apoyado.[/SU]",
            "Bras en cactus : coudes à hauteur d’épaules, mains en haut. On inspire, on ouvre la poitrine et on emmène les "
            "coudes un peu en arrière. ((4 resp.)) [SU]Allongés, genoux pliés ou jambes allongées : bras en cactus au sol, le "
            "dos des mains posé.[/SU]")),
        card2("chair_cat", "pelvis_f", "F", ("Balanceo de la pelvis", "Bascule du bassin"), ("6 veces", "6 fois"), (
            "Sentados, manos en las rodillas. Exhalamos y redondeamos un poco la espalda baja; inhalamos y la arqueamos un poco. "
            "Movimiento pequeño. [SU]Tumbados, rodillas dobladas: exhalamos, la espalda baja se apoya en el suelo; inhalamos, "
            "se separa un poco.[/SU]",
            "Assis, mains sur les genoux. On expire et on arrondit un peu le bas du dos ; on inspire et on le creuse un peu. "
            "Petit mouvement. [SU]Allongés, genoux pliés : on expire, le bas du dos se pose au sol ; on inspire, il se décolle "
            "un peu.[/SU]")),
        card2("hug_chair", "hug_floor", "F", ("Abrazar un árbol", "Enlacer un arbre"), ("4 resp.", "4 resp."), (
            "Entrelazamos los dedos y empujamos las palmas hacia delante, como si abrazáramos un árbol grande. La espalda "
            "alta se redondea, la cabeza baja un poco. ((4 resp.)) Soltamos.",
            "On croise les doigts et on pousse les paumes vers l’avant, comme si on enlaçait un grand arbre. Le haut du dos "
            "s’arrondit, la tête descend un peu. ((4 resp.)) On relâche.")),
        card2("calf_chair", "legs_long", "F", ("Pantorrillas", "Mollets"), ("4 resp./lado", "4 resp./côté"), (
            "Pierna derecha estirada delante, talón en el suelo. Subimos las puntas del pie hacia nosotros: se estira la "
            "pantorrilla. ((4 resp.)) Cambiamos. [SU]Sentados, piernas delante: puntas de los pies hacia nosotros.[/SU]",
            "Jambe droite allongée devant, talon au sol. On ramène les pointes du pied vers nous : le mollet s’étire. "
            "((4 resp.)) On change. [SU]Assis, jambes devant : pointes des pieds vers nous.[/SU]")),
        card2("child_chair", "child", "F", ("Descanso: el niño", "Repos : l’enfant"), ("5 resp.", "5 resp."), (
            "Pies separados. Dejamos caer el pecho sobre los muslos y apoyamos los antebrazos o las manos en las piernas. "
            "La cabeza descansa. ((5 resp.)) Subimos despacio, la cabeza la última. "
            "[SU]Postura del niño: rodillas en el suelo, caderas hacia los talones, frente al suelo o sobre los puños.[/SU]",
            "Pieds écartés. On laisse tomber la poitrine sur les cuisses et on pose les avant-bras ou les mains sur les "
            "jambes. La tête se repose. ((5 resp.)) On remonte doucement, la tête en dernier. [SU]Posture de l’enfant : "
            "genoux au sol, hanches vers les talons, front au sol ou sur les poings.[/SU]")),
        card2("c_fold", "twist_R", "F", ("V · Soltar la espalda", "V · Relâcher le dos"), ("4 resp.", "4 resp."), (
            "Exhalamos: dejamos caer el pecho hacia los muslos, brazos colgando. ((4 resp.)) Subimos muy despacio, la cabeza "
            "la última. [SU]Tumbados, brazos en cruz: rodillas juntas a la derecha, a la izquierda.[/SU]",
            "On expire : on laisse tomber la poitrine vers les cuisses, bras pendants. ((4 resp.)) On remonte très "
            "lentement, la tête en dernier. [SU]Allongés, bras en croix : genoux serrés à droite, puis à gauche.[/SU]")),
    ], cols=3),
    band(9, ("Relajación · 5 minutos", "Relaxation · 5 minutes"), "0:51 – 0:56"),
    grid([card2("c_relax", "savasana", "F", ("Relajación", "Relaxation"), ("5 min", "5 min"), (
        "Nos sentamos atrás, espalda en el respaldo, antebrazos en los reposabrazos o manos en los muslos, palmas hacia "
        "arriba. Pies en el suelo. Cerramos los ojos. [SU]Tumbados boca arriba; si es más cómodo, rodillas dobladas.[/SU]"
        "Con cada exhalación, el cuerpo pesa un poco más: los pies… las piernas… los brazos… los hombros… la cara. "
        "((5 minutos de silencio)) [T] Movemos los dedos, abrimos los ojos. Desde el suelo: giramos a la derecha y nos "
        "sentamos despacio.",
        "On s’assoit au fond, dos contre le dossier, avant-bras sur les accoudoirs ou mains sur les cuisses, paumes vers le "
        "haut. Pieds au sol. On ferme les yeux. [SU]Allongés sur le dos ; si c’est plus confortable, genoux pliés.[/SU]"
        "À chaque expiration, le corps devient un peu plus lourd : les pieds… les jambes… les bras… les épaules… le visage. "
        "((5 minutes de silence)) [T] On bouge les doigts, on ouvre les yeux. Depuis le sol : on roule à droite et on "
        "s’assoit doucement."), mh=17)], cols=1),
    band(10, ("Respiración final y cierre", "Respiration finale et clôture"), "0:56 – 1:00"),
    grid([
        card2("chair_sit", "seated_cross", "F", ("Exhalación un poco más larga", "Expiration un peu plus longue"), ("6 veces", "6 fois"), (
            "Ojos cerrados. Inhalamos despacio por la nariz… dos, tres, cuatro. Exhalamos despacio… dos, tres, cuatro, cinco, "
            "seis. Sin forzar: si cuesta, exhalamos hasta cinco. Sin retener el aire. ((6 veces))",
            "Yeux fermés. On inspire lentement par le nez… deux, trois, quatre. On expire lentement… deux, trois, quatre, cinq, "
            "six. Sans forcer : si c’est difficile, on expire sur cinq. Sans retenir l’air. ((6 fois))")),
        card2("chair_sit", "seated_cross", "F", ("X · Contar hacia atrás y cierre", "X · Compter à l’envers et clôture"), ("10 resp.", "10 resp."), (
            "Ojos cerrados. Contamos cada exhalación, en silencio, de diez a uno. Si perdemos la cuenta, volvemos a diez, "
            "sin prisa. Manos delante del pecho: gracias por practicar conmigo. Namasté.",
            "Yeux fermés. On compte chaque expiration, en silence, de dix à un. Si on perd le compte, on revient à dix, sans "
            "se presser. Mains devant la poitrine : merci d’avoir pratiqué avec moi. Namasté.")),
    ]),
]
p1, p2, p3, p4 = P_ALL, [], [], []

CSS = B.CSS + """
@page { margin: 7mm 8mm 8mm 8mm; @top-right { content: none; }
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 7.5pt; } }
body { font-size: 9.2pt; line-height: 1.2; }
.pg { break-before: page; } .pg:first-child { break-before: auto; }
.top { display:flex; justify-content:space-between; align-items:flex-end; gap:4mm; border-bottom:2px solid var(--band); padding-bottom:1mm; }
.top h1 { margin:0; font-size:17pt; color:var(--band); line-height:1.05; }
.kick { font-size:7.8pt; letter-spacing:.05em; text-transform:uppercase; color:var(--muted); }
.leg { font-size:8.3pt; text-align:right; line-height:1.5; }
.pm { font-size:8pt; color:#6b5a2a; background:#f6f3ea; border-left:3px solid #c9b88a; padding:.6mm 2mm; margin:.8mm 0; }
.qband { display:flex; align-items:center; gap:2mm; background:var(--band); color:#fff; border-radius:1.6mm;
         padding:.5mm 2.2mm; margin:1.3mm 0 .8mm; font-size:10.3pt; break-after: avoid; }
.qband .secn { background:#fff; color:var(--band); border-radius:2.5mm; min-width:5.5mm; padding:0 1mm; text-align:center; font-weight:700; font-size:8.8pt; }
.qband b { flex:1; } .qband .time { font-weight:700; white-space:nowrap; }
.qband .sr, .qband .sl { color:#fff; text-decoration: underline; text-decoration-thickness: 2px; }
.qband .opt { background:#fff3; border:1px solid #fff9; border-radius:2mm; padding:0 1.5mm; font-size:8pt; }
.qgrid { display:grid; gap:1mm; } .qgrid.c1 { grid-template-columns:1fr; } .qgrid.c2 { grid-template-columns:1fr 1fr; }
.qgrid.c3 { grid-template-columns:1fr 1fr 1fr; }
.qc { display:flex; gap:1.5mm; align-items:flex-start; background:#f5f7f9; border-radius:1.6mm; padding:.8mm 1.3mm; break-inside:avoid; }
.qf { flex:0 0 auto; display:flex; flex-direction:column; align-items:center; gap:.5mm; min-width:12mm; }
.qf.row { flex-direction:row; align-items:flex-end; }
.qf svg { display:block; }
.qn { font-weight:700; font-size:9.5pt; margin-bottom:.2mm; } .qn .badge { font-size:7.4pt; padding:0 1.2mm; }
.qcue { font-size:9.2pt; }
.it { font-size:6.5pt; font-weight:700; border-radius:1mm; padding:0 1mm; letter-spacing:.03em; white-space:nowrap; vertical-align:1px; }
.it-d { background:#ece7f7; color:#4a3a86; } .it-f { background:#dff3e6; color:#1f6b3d; } .it-t { background:var(--band); color:#fff; }
.strip { margin:.8mm 0; break-inside:avoid; } .srow { display:flex; align-items:flex-end; justify-content:space-between;
  gap:.6mm; background:#f5f7f9; border-radius:1.6mm; padding:.8mm 1.5mm; }
.sf { display:flex; flex-direction:column; align-items:center; text-align:center; min-width:0; }
.sfig { display:flex; align-items:flex-end; gap:.5mm; } .sfig svg { display:block; }
.sor { font-size:8pt; color:var(--muted); align-self:center; }
.scap { font-size:7.3pt; font-weight:700; line-height:1.1; margin-top:.5mm; max-width:24mm; }
.sb { font-size:6.8pt; font-weight:700; border-radius:1mm; padding:0 1mm; margin-top:.3mm; white-space:nowrap; }
.sb.inh { background:var(--inh-bg); } .sb.exh { background:var(--exh-bg); } .sb.n { background:#e6eaef; }
.sb i { font-style:normal; font-size:.75em; }
.sarrow { font-size:10pt; color:var(--band); font-weight:700; align-self:center; padding-bottom:3.5mm; }
ol.st { list-style:none; margin:.8mm 0 0; padding:0; } ol.st.c2 { columns:2; column-gap:4mm; }
ol.st li { display:flex; gap:1.4mm; margin-bottom:.55mm; break-inside:avoid; }
.nn { flex:0 0 4.4mm; height:4.4mm; font-size:7.2pt; border-radius:2.2mm; margin-top:.1mm; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:2mm; }
.rnd .qband { margin-top:.5mm; font-size:9.6pt; }
.rt { margin:.6mm 0; }
"""
CSS += """
.vb { display:block; margin:.6mm 0; padding:.4mm 1.6mm .5mm; border-radius:1.2mm; }
.vc { background:#f4ebdf; border-left:3px solid #a07c52; color:#5a3f1f; }
.vs { background:#e9eef5; border-left:3px solid #6b7f99; color:#2f3e52; }
.vl { font-size:7pt; font-weight:700; letter-spacing:.05em; margin-right:1.5mm; padding:0 1mm; border-radius:1mm;
      color:#fff; vertical-align:1px; }
.vc .vl { background:#a07c52; } .vs .vl { background:#6b7f99; }
body { font-size:10pt; line-height:1.21; } .qcue { font-size:10pt; } .qn { font-size:10.4pt; }
.scap { font-size:8.2pt; max-width:30mm; } .sb { font-size:7.6pt; } .qband { font-size:11pt; }
.nn { flex-basis:5mm; height:5mm; font-size:8pt; } .it { font-size:7pt; }
.part { background:#1d2733; color:#fff; font-weight:700; font-size:10.5pt; border-radius:1.6mm; padding:.6mm 2.5mm; margin:1.5mm 0 .4mm; }
.part span { background:#fff; color:#1d2733; border-radius:1mm; padding:0 1.5mm; margin-right:2mm; font-size:8.5pt; }
"""

CSS += """
.vf { background:#e5f2e8; border-left:3px solid #3f8a5a; color:#1f4d30; } .vf .vl { background:#3f8a5a; }
.vs { background:#e6edf7; border-left:3px solid #4a6fa5; color:#22385a; } .vs .vl { background:#4a6fa5; }
.vb.inl { display:inline-block; padding:0; border:0; background:none; margin:0; }
.cue1 { margin:.6mm 0 1mm; font-size:10.6pt; }
body { font-size:9.6pt; line-height:1.18; } .qcue { font-size:9.6pt; } .qn { font-size:10pt; }
.qc.c2 { flex-direction:column; } .qf.row2 { flex-direction:row; gap:3mm; justify-content:center; width:100%; align-items:flex-end; }
.f2 { display:flex; flex-direction:column; align-items:center; gap:.4mm; }
.fl { font-size:6.4pt; font-weight:700; color:#fff; border-radius:1mm; padding:0 1.2mm; letter-spacing:.04em; }
.lc { background:#a07c52; } .lp { background:#4a6fa5; } .lf { background:#3f8a5a; } .lx { background:#7a4fa0; }
.vx { background:#f1eaf7; border-left:3px solid #7a4fa0; color:#43285c; } .vx .vl { background:#7a4fa0; }
.sl2 { font-size:7.5pt; font-weight:700; color:var(--band); letter-spacing:.08em; margin:.6mm 0 -.4mm; }
.menu { border:1.5px solid #a07c52; background:#faf5ee; border-radius:2mm; padding:1.2mm 2mm; margin:1.2mm 0; break-inside:avoid; }
.mt { font-weight:700; font-size:9.4pt; color:#6b4a24; margin-bottom:1mm; }
.mg { display:grid; grid-template-columns:1fr 1fr 1fr; gap:1mm 3mm; }
.mi { display:flex; align-items:center; gap:1.5mm; font-size:9pt; line-height:1.15; } .mi svg { flex:0 0 auto; }
.keep2 { break-inside: avoid; } .qgrid .qc { break-inside: avoid; } .qband { break-after: avoid; } .pm { break-after: avoid; } .part { break-after: avoid; }
"""

body = "".join(P_ALL)
title = "Yoga · clase 2 (ES)" if L == "es" else "Yoga · cours 2 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase2_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
