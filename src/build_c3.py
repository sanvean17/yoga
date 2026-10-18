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


def part(n, es_t, fr_t):
    return (f'<div class="part"><span>{"PARTE" if L == "es" else "PARTIE"} {n}</span>'
            f'{es_t if L == "es" else fr_t}</div>')


def para(es_t, fr_t):
    return f'<div class="cue1">{T((es_t, fr_t))}</div>'



# ===================================================================
# COURSE 3 · same format as course 2 · sun salutation evolves (warrior I inside)
# ===================================================================
_card2 = card2


def card2(*a, **k):
    k.setdefault('mh', 17)
    return _card2(*a, **k)


SUN_SEAT = [
    ("chair_sit", ("1 Corazón", "1 Cœur"), "exh"), ("c_arms_up", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("c_hinge", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("w1_chair_prep", ("5 Pierna I atrás", "5 Jambe G arrière"), "exh"),
    ("w1_chair", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("chair_sit", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STAND = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("arms_up_chair", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("hinge", ("3 Flexión", "3 Flexion"), "exh"), (("dog_chair", "half_lift_thighs"), ("4 Espalda larga", "4 Dos long"), "inh"),
    ("lunge_chair_L", ("5 Pie I atrás", "5 Pied G arrière"), "exh"),
    ("w1_stand", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("heart_chair", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STEPS = [
    (1, ("**Corazón.** Espalda larga, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Dos long, paumes jointes devant la poitrine. On expire.")),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos, hasta donde es cómodo.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte, jusqu’où c’est confortable.")),
    (3, ("**Flexión.** Exhalamos: nos inclinamos desde las caderas, manos en los muslos, la espalda larga. "
         "[MC]Si estamos cómodos, soltamos más: la cabeza cuelga.[/MC]",
         "**Flexion.** On expire : on se penche depuis les hanches, mains sur les cuisses, le dos long. "
         "[MC]Si on est à l’aise, on relâche davantage : la tête pend.[/MC]")),
    (4, ("**Espalda larga.** Inhalamos: subimos un poco, la espalda plana como una mesa. Miramos al suelo. "
         "[DP]Manos en el respaldo, caminamos un poco atrás; o manos en los muslos.[/DP]",
         "**Dos long.** On inspire : on remonte un peu, le dos plat comme une table. Regard au sol. "
         "[DP]Mains sur le dossier, on recule un peu ; ou mains sur les cuisses.[/DP]")),
    (5, ("**NUEVO · Pierna izquierda atrás.** Exhalamos: subimos el torso; giramos un poco en la silla y la pierna "
         "izquierda va atrás, al lado de la silla, la punta del pie apoyada. Manos en el muslo derecho. "
         "[DP]El pie izquierdo da un paso atrás, rodilla derecha un poco doblada, una mano en la silla.[/DP]",
         "**NOUVEAU · Jambe gauche en arrière.** On expire : on redresse le buste ; on tourne un peu sur la chaise et la "
         "jambe gauche va en arrière, à côté de la chaise, la pointe du pied posée. Mains sur la cuisse droite. "
         "[DP]Le pied gauche recule d’un pas, genou droit un peu plié, une main sur la chaise.[/DP]")),
    (6, ("**NUEVO · Guerrero I.** Inhalamos: subimos los brazos, o uno solo si la otra mano está en la silla. "
         "((2 resp.))",
         "**NOUVEAU · Guerrier I.** On inspire : on monte les bras, ou un seul si l’autre main est sur la chaise. "
         "((2 resp.))")),
    (7, ("**Corazón.** Exhalamos: bajamos los brazos, la pierna vuelve, manos delante del pecho. ((1 resp.)) "
         "La ronda siguiente, con la otra pierna.",
         "**Cœur.** On expire : on descend les bras, la jambe revient, mains devant la poitrine. ((1 resp.)) "
         "La ronde suivante, avec l’autre jambe.")),
]

P_ALL = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 3 · guion de la profesora · 1 hora · de pie, en la silla o en el suelo" if L == "es"
     else "Cours 3 · version française · même ordre que la version espagnole") +
    '</div><h1>' + ("Yoga suave · cada uno a su manera" if L == "es" else "Yoga doux · chacun à sa façon") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="fl lc">SILLA</span> <span class="fl lp">DE PIE CON APOYO</span> <span class="fl lf">SUELO</span> <span class="fl lx">MÁS COMPLETO</span>'
     if L == "es" else
     '<span class="fl lc">CHAISE</span> <span class="fl lp">DEBOUT AVEC APPUI</span> <span class="fl lf">SOL</span> <span class="fl lx">PLUS COMPLET</span>') +
    '</div></div>',
    band(1, ("Bienvenida · las reglas", "Accueil · les règles"), "0:00 – 0:04"),
    note("<b>avant de commencer</b> : chaises solides, sans roulettes ; pour le debout, chaise contre le mur pour qu’elle ne "
         "glisse pas. Demande aux nouveaux : <b>ostéoporose ?</b> → pas de dos rond profond ni de torsion forte, on plie depuis "
         "les hanches, dos long. <b>Prothèse de hanche ?</b> → si elle est récente ou si on lui a dit de ne pas croiser les "
         "jambes : pas de jambes croisées (chiffre 4), genoux écartés, genou poitrine doux. <b>Tension ou vertiges ?</b> → la "
         "tête ne descend pas plus bas que le cœur ; on remonte lentement."),
    grid([card2("chair_sit", "tadasana", "P", ("Cada uno a su manera", "Chacun à sa façon"), None, (
        "Hola a todos, bienvenidos de nuevo. Como siempre, en cada ejercicio os enseñaré todas las opciones: **en la "
        "silla, de pie o en el suelo**. Todo se puede hacer en la silla, y también podemos mezclar: una parte en la silla, "
        "otra de pie, otra en el suelo. Cada uno elige lo que mejor le va hoy. **Sin presión: ninguna opción es mejor que "
        "otra.** De pie, no dudéis en usar la silla para apoyaros. "
        "Lo más importante: **no forzamos nunca. Escuchamos nuestro cuerpo.** Si algo duele o no es posible, no pasa nada: "
        "descansamos. Vamos despacio; así es como mejoramos, poco a poco. **Mejor menos amplitud que hacer demasiado.** "
        "Hoy retomamos lo que ya conocemos y añadimos algunas cosas nuevas.",
        "Bonjour à tous, rebienvenue. Comme toujours, à chaque exercice je vous montrerai toutes les options : **sur la "
        "chaise, debout ou au sol**. Tout peut se faire sur la chaise, et on peut aussi mélanger : une partie sur la chaise, "
        "une autre debout, une autre au sol. Chacun choisit ce qui lui convient le mieux aujourd’hui. **Aucune pression : "
        "aucune option n’est meilleure qu’une autre.** Debout, n’hésitez pas à utiliser la chaise pour vous appuyer. "
        "Le plus important : **on ne force jamais. On écoute son corps.** Si quelque chose fait mal ou n’est pas possible, ce "
        "n’est pas grave : on se repose. On y va lentement ; c’est comme ça qu’on progresse, petit à petit. **Mieux vaut "
        "moins d’amplitude que d’en faire trop.** Aujourd’hui on reprend ce qu’on connaît déjà et on ajoute quelques "
        "nouveautés."))], cols=1),
    band(2, ("Respiración de inicio", "Respiration du début"), "0:04 – 0:10"),
    grid([
        card2("r_chair", "r_floor", "F", ("Respiración en tres partes", "Respiration en trois parties"), ("5 resp.", "5 resp."), (
            "Cerramos los ojos si queréis. Una mano en el abdomen. Inhalamos: el abdomen se llena suavemente… las "
            "costillas se abren… el pecho sube un poco. Exhalamos despacio: el pecho, las costillas, el abdomen. Como una "
            "ola. Sin forzar. ((5 respiraciones))",
            "On ferme les yeux si vous voulez. Une main sur le ventre. On inspire : le ventre se remplit doucement… les côtes "
            "s’ouvrent… la poitrine monte un peu. On expire lentement : la poitrine, les côtes, le ventre. Comme une vague. "
            "Sans forcer. ((5 respirations))")),
        card2("c_breath", "arms_up", "P", ("Brazos y respiración", "Bras et respiration"), ("5 veces", "5 fois"), (
            "Inhalamos por la nariz y abrimos o subimos los brazos, despacio. Exhalamos y los bajamos lentamente. El "
            "movimiento dura lo mismo que la respiración. ((5 veces)) Los brazos suben solo hasta donde es cómodo.",
            "On inspire par le nez et on ouvre ou on monte les bras, lentement. On expire et on les redescend lentement. Le "
            "mouvement dure autant que la respiration. ((5 fois)) Les bras montent seulement jusqu’où c’est confortable.")),
    ]),
    band(3, ("Calentamiento · en la silla, de pie o en el suelo", "Échauffement · sur la chaise, debout ou au sol"), "0:10 – 0:20"),
    note("on reprend le cou, les épaules, l’inclinaison et la torsion. <b>Nouveau</b> : la marche et les talons, qui "
         "réveillent les jambes et les chevilles pour l’arbre."),
    grid([
        card2("c_neck", "seated_neck", "F", ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), (
            "Exhalamos: oreja derecha hacia el hombro derecho. ((3 resp.)) Al centro, y al otro lado. Después giramos la "
            "cabeza despacio: miramos a la derecha… a la izquierda. Movimiento pequeño.",
            "On expire : oreille droite vers l’épaule droite. ((3 resp.)) Au centre, puis de l’autre côté. Puis on tourne la "
            "tête lentement : on regarde à droite… à gauche. Petit mouvement.")),
        card2("c_shoulders", "seated_shoulders", "F", ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), (
            "Inhalamos, subimos los hombros. Exhalamos, atrás y abajo. Cinco círculos hacia atrás… cinco hacia delante.",
            "On inspire, on monte les épaules. On expire, en arrière et en bas. Cinq cercles vers l’arrière… cinq vers l’avant.")),
        card2("sh_chair", "sh_stand", "P", ("Estirar los hombros", "Étirer les épaules"), ("3 resp./lado", "3 resp./côté"), (
            "El brazo derecho cruza delante del pecho; la mano izquierda lo acerca suavemente, por encima del codo. Hombros "
            "bajos. ((3 resp.)) Cambiamos de brazo.",
            "Le bras droit croise devant la poitrine ; la main gauche le rapproche doucement, au-dessus du coude. Épaules "
            "basses. ((3 resp.)) On change de bras.")),
        card2("c_march", "march_stand", "P", ("Nuevo · La marcha", "Nouveau · La marche"), ("10 + 10", "10 + 10"), (
            "Sentados al borde, espalda larga. Levantamos un pie un poco… lo bajamos; el otro. Como si camináramos. Los brazos "
            "se balancean si queréis. ((10 pasos)) Después, un poco más rápido, sin prisa. [DP]De pie, una mano en el "
            "respaldo: marchamos en el sitio; las rodillas suben solo un poco.[/DP]",
            "Assis au bord, dos long. On lève un pied un peu… on le pose ; l’autre. Comme si on marchait. Les bras se "
            "balancent si vous voulez. ((10 pas)) Puis un peu plus vite, sans se presser. [DP]Debout, une main sur le dossier : "
            "on marche sur place ; les genoux montent seulement un peu.[/DP]")),
        card2("heeltoe_chair", "heel_raise", "P", ("Nuevo · Talones y puntas", "Nouveau · Talons et pointes"), ("8 veces", "8 fois"), (
            "Sentados: subimos los talones, las puntas de los pies se quedan en el suelo… bajamos. Después al revés: subimos "
            "las puntas, los talones se quedan. ((8 veces)) [DP]De pie, las dos manos en el respaldo: inhalamos, subimos los "
            "talones despacio; exhalamos, bajamos despacio.[/DP]",
            "Assis : on monte les talons, les pointes des pieds restent au sol… on redescend. Puis l’inverse : on monte les "
            "pointes, les talons restent. ((8 fois)) [DP]Debout, les deux mains sur le dossier : on inspire, on monte les "
            "talons doucement ; on expire, on redescend doucement.[/DP]")),
        card2("c_wrists", "wrists", "F", ("Muñecas y tobillos", "Poignets et chevilles"), ("5 + 5", "5 + 5"), (
            "Círculos con las muñecas, cinco hacia cada lado. Abrimos y cerramos las manos. Después levantamos un poco un pie: "
            "círculos con el tobillo. Cambiamos de pie.",
            "Cercles avec les poignets, cinq de chaque côté. On ouvre et on ferme les mains. Puis on soulève un peu un pied : "
            "cercles avec la cheville. On change de pied.")),
        card2("c_side_R", "sidebend_R", "F", ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), (
            "Antebrazo izquierdo en el reposabrazos. Inhalamos, brazo derecho arriba. Exhalamos, nos inclinamos a la "
            "izquierda. ((3 resp.)) Cambiamos. [SU]Mano izquierda en el suelo, junto a la cadera.[/SU]",
            "Avant-bras gauche sur l’accoudoir. On inspire, bras droit en haut. On expire, on se penche à gauche. "
            "((3 resp.)) On change. [SU]Main gauche au sol, près de la hanche.[/SU]")),
        card2("c_twist", "seated_twist", "F", ("Torsión sentados", "Torsion assise"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda en la rodilla derecha, mano derecha en el reposabrazos derecho. Inhalamos, espalda larga. "
            "Exhalamos, giramos a la derecha, sin forzar. ((3 resp.)) Cambiamos. [SU]Mano derecha en el suelo, detrás.[/SU]",
            "Main gauche sur le genou droit, main droite sur l’accoudoir droit. On inspire, dos long. On expire, on tourne à "
            "droite, sans forcer. ((3 resp.)) On change. [SU]Main droite au sol, derrière.[/SU]")),
        card2("chair_cat", "cat", "F", ("Gato-vaca", "Chat-vache"), ("5 veces", "5 fois"), (
            "Manos en las rodillas. Inhalamos, abrimos el pecho. Exhalamos, redondeamos un poco la espalda. "
            "[SU]A cuatro apoyos, si las rodillas están cómodas.[/SU]",
            "Mains sur les genoux. On inspire, on ouvre la poitrine. On expire, on arrondit un peu le dos. [SU]À quatre "
            "pattes, si les genoux sont à l’aise.[/SU]")),
    ], cols=3),
    part(1, "De pie o en la silla · 0:20 – 0:44", "Debout ou sur la chaise · 0:20 – 0:44"),
    band(4, ("Recordamos las tres posiciones", "On se rappelle les trois positions"), "0:20 – 0:22"),
    note("rappel rapide, on les connaît déjà : montre-toi de profil et fais-les essayer une fois. Rappel : « fermer le "
         "livre » (mains dans le pli des hanches) aide à trouver le dos long."),
    grid([
        card3("c_hinge", "hinge", "fold", ("1 · Flexión", "1 · Flexion"), None, (
            "Rodillas un poco dobladas. Nos inclinamos hacia delante **desde las caderas**, manos en los muslos. La espalda "
            "queda larga. [MC]Si estamos cómodos, soltamos más: la cabeza y los brazos cuelgan.[/MC]",
            "Genoux légèrement pliés. On se penche en avant **depuis les hanches**, mains sur les cuisses. Le dos reste "
            "long. [MC]Si on est à l’aise, on relâche davantage : la tête et les bras pendent.[/MC]")),
        card2("c_lean", "half_lift_thighs", "P", ("2 · Espalda larga", "2 · Dos long"), None, (
            "Manos en los muslos. Nos inclinamos desde las caderas y la espalda queda plana, como una mesa. Como si "
            "cerráramos un libro. Miramos al suelo.",
            "Mains sur les cuisses. On se penche depuis les hanches et le dos reste plat, comme une table. Comme si on "
            "fermait un livre. Regard au sol.")),
        card2("chair_sit", "dog_chair", "P", ("3 · Manos en el apoyo", "3 · Mains sur l’appui"), None, (
            "Sentados: manos en las rodillas. [DP]Manos en el respaldo o en la pared, a la altura de las caderas; caminamos "
            "atrás hasta que la espalda queda larga.[/DP]",
            "Assis : mains sur les genoux. [DP]Mains sur le dossier ou au mur, à hauteur des hanches ; on recule jusqu’à avoir "
            "le dos long.[/DP]")),
    ], cols=3),
    '<div class="keep2">',
    band(5, ("Saludo al sol · con el guerrero I · 3 o 4 rondas", "Salutation au soleil · avec le guerrier I · 3 ou 4 rondes"), "0:22 – 0:31"),
    note("<b>comment la faire évoluer</b> : on garde la même base et on change <b>une seule chose</b> par semaine. Cette "
         "semaine, les étapes 5 et 6 deviennent le <b>Guerrier I</b> (qu’ils connaissent déjà). Ronde 1 : comme la semaine "
         "dernière (jambe devant / pied arrière), pour se rappeler. Rondes 2 et 3 : avec le Guerrier I, jambe gauche en "
         "arrière puis jambe droite. Ronde 4 (optionnelle) : un mouvement par respiration, sans pause. "
         "<b>Semaines suivantes</b> : tenir 3 resp. dans le Guerrier I ; puis remplacer le Guerrier I par le Guerrier II ; "
         "puis enchaîner Guerrier I → Guerrier II dans la même ronde."),
    '<div class="sl2">' + ("SENTADOS" if L == "es" else "ASSIS") + '</div>' + strip(SUN_SEAT, 0.13) +
    '<div class="sl2">' + ("DE PIE" if L == "es" else "DEBOUT") + '</div>' + strip(SUN_STAND, 0.13) + '</div>',
    steps(SUN_STEPS),
    band(6, ("Guerrero I, guerrero inverso y diosa", "Guerrier I, guerrier inversé et déesse"), "0:31 – 0:40"),
    note("deux postures qu’on répète (Guerrier I, déesse) et <b>une nouvelle</b> : le guerrier inversé. <b>Avec "
         "accoudoirs</b> : ils s’assoient tout au bord, devant les accoudoirs. Côté droit d’abord, puis gauche. Debout : "
         "chaise ou mur à côté de la jambe avant."),
    grid([
        card2("w1_chair", "w1_stand", "P", ("Guerrero I · lo mantenemos", "Guerrier I · on le tient"), ("4 resp./lado", "4 resp./côté"), (
            "Ya lo conocemos; hoy lo mantenemos un poco más. Al borde de la silla, giramos un poco hacia la izquierda. Pie "
            "derecho delante, rodilla encima del tobillo. La pierna izquierda atrás, al lado de la silla, la punta del pie "
            "apoyada. Inhalamos, brazos arriba o manos en la cintura. ((4 resp.)) Cambiamos de lado. [DP]Un paso largo atrás "
            "con el pie izquierdo, rodilla derecha doblada, una mano en la silla si hace falta.[/DP] [MC]El pie de atrás un "
            "poco más lejos; las palmas se juntan arriba.[/MC]",
            "On le connaît déjà ; aujourd’hui on le tient un peu plus. Au bord de la chaise, on tourne un peu vers la gauche. "
            "Pied droit devant, genou au-dessus de la cheville. La jambe gauche en arrière, à côté de la chaise, la pointe du "
            "pied posée. On inspire, bras en haut ou mains sur la taille. ((4 resp.)) On change de côté. [DP]Un grand pas en "
            "arrière avec le pied gauche, genou droit plié, une main sur la chaise si besoin.[/DP] [MC]Le pied arrière un peu "
            "plus loin ; les paumes se rejoignent en haut.[/MC]")),
        card2("c_rev_R", "revc_R", "P", ("Nuevo · Guerrero inverso", "Nouveau · Guerrier inversé"), ("3 resp./lado", "3 resp./côté"), (
            "**Cómo entramos:** como el guerrero II de la semana pasada. Al borde de la silla, la pierna derecha se abre hacia "
            "la derecha, rodilla encima del tobillo; la pierna izquierda se estira atrás y a la izquierda. Brazos en cruz. "
            "Inhalamos: la palma derecha mira al techo y el brazo derecho sube; la mano izquierda baja y descansa en la "
            "pierna izquierda, sin apoyar peso. El lado derecho se estira. ((3 resp.)) Exhalamos, brazos en cruz. Cambiamos de "
            "lado. [DP]Pies separados, pie derecho hacia fuera, rodilla derecha doblada encima del tobillo; la mano "
            "izquierda puede quedarse en la silla. No echamos el cuerpo atrás: el pecho se abre hacia arriba.[/DP]",
            "**Comment on entre :** comme le guerrier II de la semaine dernière. Au bord de la chaise, la jambe droite "
            "s’ouvre vers la droite, genou au-dessus de la cheville ; la jambe gauche s’allonge en arrière et à gauche. Bras "
            "en croix. On inspire : la paume droite regarde le plafond et le bras droit monte ; la main gauche descend et se "
            "pose sur la jambe gauche, sans appuyer. Le côté droit s’étire. ((3 resp.)) On expire, bras en croix. On change "
            "de côté. [DP]Pieds écartés, pied droit vers l’extérieur, genou droit plié au-dessus de la cheville ; la main "
            "gauche peut rester sur la chaise. On ne se jette pas en arrière : la poitrine s’ouvre vers le haut.[/DP]")),
        card2("d_chair", "d_stand", "P", ("Diosa · con movimiento", "Déesse · avec mouvement"), ("4 veces + 3 resp.", "4 fois + 3 resp."), (
            "Al borde de la silla, piernas bien separadas, puntas de los pies hacia fuera, rodillas en la misma dirección. "
            "Brazos en cactus. **Hoy añadimos movimiento:** exhalamos, los codos se juntan delante de la cara; inhalamos, "
            "abrimos en cactus y el pecho se abre. ((4 veces)) Después nos quedamos en cactus. ((3 resp.)) "
            "[DP]Pies separados, rodillas un poco dobladas, una mano en la silla si hace falta. Exhalamos, doblamos un poco "
            "más las rodillas; inhalamos, las estiramos sin bloquearlas. Sin bajar mucho.[/DP]",
            "Au bord de la chaise, jambes bien écartées, pointes des pieds vers l’extérieur, genoux dans la même direction. "
            "Bras en cactus. **Aujourd’hui on ajoute du mouvement :** on expire, les coudes se rejoignent devant le visage ; "
            "on inspire, on ouvre en cactus et la poitrine s’ouvre. ((4 fois)) Puis on reste en cactus. ((3 resp.)) "
            "[DP]Pieds écartés, genoux un peu pliés, une main sur la chaise si besoin. On expire, on plie un peu plus les "
            "genoux ; on inspire, on les allonge sans les bloquer. Sans descendre beaucoup.[/DP]")),
    ], cols=3),
    band(7, ("Equilibrio · el árbol", "Équilibre · l’arbre"), "0:40 – 0:44"),
    note("le pied ne se pose <b>jamais contre le genou</b> : cheville, mollet ou cuisse. Fixer un point immobile au sol, "
         "deux mètres devant. Si quelqu’un vacille : il repose le pied, c’est normal, on recommence."),
    grid([card3("c_tree_R", "tree_wall", "tree_R", ("Árbol · tres niveles", "Arbre · trois niveaux"), ("3 resp./lado", "3 resp./côté"), (
        "Miramos un punto fijo en el suelo. **En la silla:** al borde, espalda larga. Abrimos la rodilla derecha hacia fuera "
        "y apoyamos la planta del pie derecho contra la pierna izquierda, en el tobillo o en la pantorrilla. Manos juntas "
        "delante del pecho. ((3 resp.)) Cambiamos. "
        "[DP]Una mano en la silla o en la pared. El talón derecho sobre el tobillo izquierdo, los dedos del pie se quedan "
        "en el suelo, como una pata de cabra. La rodilla derecha se abre hacia fuera. La otra mano en el pecho, si "
        "queremos.[/DP]"
        "[MC]Sin apoyo: el pie sube a la pantorrilla o al muslo, nunca contra la rodilla. Manos al pecho o brazos arriba, "
        "como ramas.[/MC]",
        "On regarde un point fixe au sol. **Sur la chaise :** au bord, dos long. On ouvre le genou droit vers l’extérieur et "
        "on pose la plante du pied droit contre la jambe gauche, sur la cheville ou le mollet. Mains jointes devant la "
        "poitrine. ((3 resp.)) On change. "
        "[DP]Une main sur la chaise ou au mur. Le talon droit sur la cheville gauche, les orteils restent au sol, comme une "
        "béquille. Le genou droit s’ouvre vers l’extérieur. L’autre main sur la poitrine, si on veut.[/DP]"
        "[MC]Sans appui : le pied monte au mollet ou à la cuisse, jamais contre le genou. Mains à la poitrine ou bras en haut, "
        "comme des branches.[/MC]"))], cols=1),
    '<div style="break-before:page"></div>',
    part(2, "En la silla o en el suelo · 0:44 – 1:00", "Sur la chaise ou au sol · 0:44 – 1:00"),
    band(8, ("Estiramientos · en la silla o en el suelo", "Étirements · sur la chaise ou au sol"), "0:44 – 0:51"),
    note("on en reprend certains et on mélange : <b>nouveaux</b> = flexion jambes longues et « brazo y pierna » (à quatre "
         "pattes). Ordre au sol : assis → sur le dos → à quatre pattes → l’enfant → sur le dos pour la relaxation. Ceux qui "
         "vont au sol descendent doucement, une main sur la chaise. Tu choisis selon le temps. Ostéoporose : dans la flexion "
         "et l’enfant, on descend peu, dos long. Prothèse récente ou consigne de ne pas croiser : pas de chiffre 4."),
    grid([
        card2("chair_sit", "butterfly", "F", ("Mariposa", "Papillon"), ("4 resp.", "4 resp."), (
            "Rodillas separadas, manos en los muslos. Inhalamos, espalda larga. Exhalamos, nos inclinamos un poco. "
            "[SU]Sentados en el suelo, plantas de los pies juntas; no empujamos las rodillas.[/SU]",
            "Genoux écartés, mains sur les cuisses. On inspire, dos long. On expire, on se penche un peu. "
            "[SU]Assis au sol, plantes des pieds jointes ; on ne pousse pas les genoux.[/SU]")),
        card2("c_hinge", "seated_fold", "F", ("Nuevo · Flexión piernas largas", "Nouveau · Flexion jambes longues"), ("4 resp.", "4 resp."), (
            "Al borde de la silla, las dos piernas un poco estiradas delante, talones en el suelo, rodillas un poco dobladas. "
            "Inhalamos: espalda larga. Exhalamos: nos inclinamos desde las caderas, manos en los muslos o en las rodillas. "
            "((4 resp.)) Subimos despacio. [SU]Sentados, piernas delante, rodillas dobladas tanto como haga falta. Nos "
            "inclinamos desde las caderas, espalda larga, manos en las piernas. Luego nos tumbamos boca arriba, rodillas "
            "dobladas.[/SU]",
            "Au bord de la chaise, les deux jambes un peu allongées devant, talons au sol, genoux un peu pliés. On inspire : "
            "dos long. On expire : on se penche depuis les hanches, mains sur les cuisses ou les genoux. ((4 resp.)) On "
            "remonte doucement. [SU]Assis, jambes devant, genoux pliés autant qu’il faut. On se penche depuis les hanches, "
            "dos long, mains sur les jambes. Puis on s’allonge sur le dos, genoux pliés.[/SU]")),
        card2("chair_cat", "pelvis_f", "F", ("Balanceo de la pelvis", "Bascule du bassin"), ("6 veces", "6 fois"), (
            "Sentados, manos en las rodillas. Exhalamos y redondeamos un poco la espalda baja; inhalamos y la arqueamos un poco. "
            "Movimiento pequeño. [SU]Tumbados, rodillas dobladas: exhalamos, la espalda baja se apoya en el suelo; inhalamos, "
            "se separa un poco.[/SU]",
            "Assis, mains sur les genoux. On expire et on arrondit un peu le bas du dos ; on inspire et on le creuse un peu. "
            "Petit mouvement. [SU]Allongés, genoux pliés : on expire, le bas du dos se pose au sol ; on inspire, il se décolle "
            "un peu.[/SU]")),
        card2("c_lean", "bridge", "F", ("El puente", "Le pont"), ("4 veces", "4 fois"), (
            "Levantarse de la silla: pies firmes, nos inclinamos un poco hacia delante, empujamos los pies y nos ponemos "
            "de pie; nos sentamos despacio. Manos en los reposabrazos si hace falta. ((4 veces)) "
            "Si no podemos levantarnos: empujamos suavemente los pies en el suelo y apretamos las piernas y los glúteos, "
            "sin bloquear la respiración. ((3 resp.)) Soltamos. [SU]Tumbados, rodillas dobladas, pies separados como las "
            "caderas. Inhalamos: empujamos los pies y subimos un poco las caderas. Exhalamos: bajamos despacio.[/SU]",
            "Se lever de la chaise : pieds bien posés, on se penche un peu en avant, on pousse dans les pieds et on se met "
            "debout ; on se rassoit doucement. Mains sur les accoudoirs si besoin. ((4 fois)) "
            "Si on ne peut pas se lever : on pousse doucement les pieds dans le sol et on contracte les jambes et les "
            "fessiers, sans bloquer la respiration. ((3 resp.)) On relâche. [SU]Allongés, genoux pliés, pieds écartés "
            "largeur de hanches. On inspire : on pousse dans les pieds et on monte un peu les hanches. On expire : on "
            "redescend doucement.[/SU]")),
        card2("chair_knee", "knees_chest", "F", ("Rodilla al pecho", "Genou poitrine"), ("3 resp./lado", "3 resp./côté"), (
            "Abrazamos la rodilla derecha, espalda larga. ((3 resp.)) Cambiamos. [SU]Tumbados: las dos rodillas al pecho; "
            "nos balanceamos un poco.[/SU]",
            "On serre le genou droit, dos long. ((3 resp.)) On change. [SU]Allongés : les deux genoux à la poitrine ; on se "
            "balance un peu.[/SU]")),
        card2("fig4_chair", "fig4_floor", "F", ("El número 4", "Le chiffre 4"), ("4 resp./lado", "4 resp./côté"), (
            "Tobillo derecho sobre la rodilla izquierda, pie flexionado. Si no es cómodo, el pie se queda en el suelo. "
            "((4 resp.)) Cambiamos. [SU]Tumbados, pie izquierdo en el suelo.[/SU]",
            "Cheville droite sur le genou gauche, pied fléchi. Si ce n’est pas confortable, le pied reste au sol. "
            "((4 resp.)) On change. [SU]Allongés, pied gauche au sol.[/SU]")),
        card2("chair_hamstring", "leg_stretch", "F", ("Estirar la pierna", "Étirer la jambe"), ("4 resp./lado", "4 resp./côté"), (
            "Pierna derecha estirada delante, talón en el suelo. Exhalamos, el pecho un poco hacia delante. ((4 resp.)) "
            "Cambiamos. [SU]Tumbados: cogemos la pierna detrás del muslo, rodilla doblada.[/SU]",
            "Jambe droite allongée devant, talon au sol. On expire, la poitrine un peu vers l’avant. ((4 resp.)) On change. "
            "[SU]Allongés : on tient la jambe derrière la cuisse, genou plié.[/SU]")),
        card2("c_twist", "twist_R", "F", ("Torsión tumbada", "Torsion allongée"), ("4 resp./lado", "4 resp./côté"), (
            "Mano izquierda en el reposabrazos derecho. Inhalamos: espalda larga. Exhalamos: giramos suavemente a la "
            "derecha. ((4 resp.)) Cambiamos. [SU]Tumbados, brazos en cruz: rodillas juntas a la derecha, la cabeza puede "
            "mirar a la izquierda. ((4 resp.)) Cambiamos.[/SU]",
            "Main gauche sur l’accoudoir droit. On inspire : dos long. On expire : on tourne doucement vers la droite. "
            "((4 resp.)) On change. [SU]Allongés, bras en croix : genoux serrés à droite, la tête peut regarder à gauche. "
            "((4 resp.)) On change.[/SU]")),
        card2("c_side_R", "banana_f", "F", ("Inclinación lateral · la banana", "Inclinaison latérale · la banane"), ("4 resp./lado", "4 resp./côté"), (
            "Mano izquierda en el reposabrazos, brazo derecho arriba. Exhalamos: nos inclinamos hacia la izquierda. "
            "((4 resp.)) Cambiamos. [SU]Tumbados, brazos por encima de la cabeza. Llevamos los pies y las manos un poco "
            "hacia la izquierda: el cuerpo hace una banana. ((4 resp.)) Cambiamos. Luego nos ponemos a cuatro patas, "
            "despacio, pasando por el lado.[/SU]",
            "Main gauche sur l’accoudoir, bras droit en haut. On expire : on s’incline vers la gauche. ((4 resp.)) On "
            "change. [SU]Allongés, bras au-dessus de la tête. On emmène les pieds et les mains un peu vers la gauche : le "
            "corps fait une banane. ((4 resp.)) On change. Puis on se met à quatre pattes, doucement, en passant par le "
            "côté.[/SU]")),
        card2("legext_c", "bird_dog", "F", ("Nuevo · Brazo y pierna", "Nouveau · Bras et jambe"), ("3 veces/lado", "3 fois/côté"), (
            "Sentados al borde, espalda larga. Inhalamos: estiramos la pierna derecha delante y subimos el brazo izquierdo "
            "delante o arriba. Exhalamos: bajamos. ((3 veces)) Cambiamos: pierna izquierda y brazo derecho. "
            "[SU]A cuatro patas, manos debajo de los hombros, rodillas debajo de las caderas. Inhalamos: el brazo derecho "
            "va delante y la pierna izquierda atrás, a la altura que podamos; o solo el brazo, o solo la pierna. Exhalamos: "
            "volvemos. Si molestan las rodillas, nos quedamos en la silla. Luego: el niño.[/SU]",
            "Assis au bord, dos long. On inspire : on allonge la jambe droite devant et on monte le bras gauche devant ou en "
            "haut. On expire : on redescend. ((3 fois)) On change : jambe gauche et bras droit. [SU]À quatre pattes, mains "
            "sous les épaules, genoux sous les hanches. On inspire : le bras droit va devant et la jambe gauche en arrière, à "
            "la hauteur qu’on peut ; ou seulement le bras, ou seulement la jambe. On expire : on revient. Si les genoux "
            "gênent, on reste sur la chaise. Puis : l’enfant.[/SU]")),
        card2("child_chair", "child", "F", ("Descanso: el niño", "Repos : l’enfant"), ("5 resp.", "5 resp."), (
            "Pies separados, manos en los muslos. Exhalamos: nos inclinamos un poco, espalda larga, y descansamos. ((5 resp.)) "
            "Subimos despacio. [MC]Si estamos cómodos, el pecho baja sobre los muslos y la cabeza descansa; subimos muy "
            "despacio, la cabeza la última.[/MC] [SU]Rodillas en el suelo, caderas hacia los talones, frente al suelo o "
            "sobre los puños. Luego nos tumbamos boca arriba para la relajación.[/SU]",
            "Pieds écartés, mains sur les cuisses. On expire : on se penche un peu, dos long, et on se repose. ((5 resp.)) On "
            "remonte doucement. [MC]Si on est à l’aise, la poitrine descend sur les cuisses et la tête se repose ; on remonte "
            "très lentement, la tête en dernier.[/MC] [SU]Genoux au sol, hanches vers les talons, front au sol ou sur les "
            "poings. Puis on s’allonge sur le dos pour la relaxation.[/SU]")),
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
        "s’assoit doucement."), mh=12)], cols=1),
    band(10, ("Respiración final y cierre", "Respiration finale et clôture"), "0:56 – 1:00"),
    grid([
        card2("chair_sit", "seated_cross", "F", ("Exhalación un poco más larga", "Expiration un peu plus longue"), ("6 veces", "6 fois"), mh=13, text=(
            "Ojos cerrados. Inhalamos despacio por la nariz… dos, tres, cuatro. Exhalamos despacio… dos, tres, cuatro, cinco, "
            "seis. Sin forzar: si cuesta, exhalamos hasta cinco. Sin retener el aire. ((6 veces))",
            "Yeux fermés. On inspire lentement par le nez… deux, trois, quatre. On expire lentement… deux, trois, quatre, cinq, "
            "six. Sans forcer : si c’est difficile, on expire sur cinq. Sans retenir l’air. ((6 fois))")),
        card2("chair_sit", "seated_cross", "F", ("Contar hacia atrás y cierre", "Compter à l’envers et clôture"), ("10 resp.", "10 resp."), mh=13, text=(
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
.menu { border:1.5px solid #a07c52; background:#faf5ee; border-radius:2mm; padding:1.5mm 2.5mm; margin:1.5mm 0; break-inside:avoid; }
.mt { font-weight:700; font-size:11pt; color:#6b4a24; }
.mw { font-size:9.4pt; color:#5a3f1f; margin:.6mm 0 1.4mm; }
.mg { display:grid; grid-template-columns:1fr 1fr 1fr; gap:1.6mm 3mm; }
.mi { display:flex; align-items:center; gap:2mm; font-size:9.4pt; line-height:1.18; background:#fff; border-radius:1.5mm; padding:1mm 1.5mm; }
.mi .f2 { flex:0 0 auto; }
.keep2 { break-inside: avoid; } .qgrid .qc { break-inside: avoid; } .qband { break-after: avoid; } .pm { break-after: avoid; } .part { break-after: avoid; }
"""

body = "".join(P_ALL)
title = "Yoga · clase 3 (ES)" if L == "es" else "Yoga · cours 3 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase3_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
