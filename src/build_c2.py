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
          "[DP]": ("vs", "DE PIE", "DEBOUT"), "[SU]": ("vf", "EN EL SUELO", "AU SOL")}
    for k, (c, les, lfr) in VB.items():
        h = h.replace(k, f'<span class="vb {c}"><span class="vl">{les if L == "es" else lfr}</span>')
    for k in ("[/C]", "[/CP]", "[/S]", "[/DP]", "[/SU]"):
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
# COURSE 2 (v2) · new exercises · every card shows BOTH versions:
#   chair (main text, everyone) + standing [DP] or floor [SU] (coloured block)
# ===================================================================

LBL = {"S": ("SILLA", "CHAISE", "lc"), "P": ("DE PIE", "DEBOUT", "lp"), "F": ("SUELO", "SOL", "lf")}


def card2(chair_pose, alt_pose, alt, name, badge, text, mh=19):
    """two figures side by side: chair version + standing ('P') or floor ('F') version."""
    def one(p, k):
        es_, fr_, c = LBL[k]
        return (f'<div class="f2">{fig(p, max_w=30, max_h=mh * 1.15, cap=0.14)}'
                f'<span class="fl {c}">{es_ if L == "es" else fr_}</span></div>')
    b = f' <span class="badge b-n">{T(badge)}</span>' if badge else ""
    return (f'<div class="qc c2"><div class="qf row2">{one(chair_pose, "S")}{one(alt_pose, alt)}</div>'
            f'<div class="qt"><div class="qn">{T(name)}{b}</div><div class="qcue">{T(text)}</div></div></div>')


def part(n, es_t, fr_t):
    return (f'<div class="part"><span>{"PARTE" if L == "es" else "PARTIE"} {n}</span>'
            f'{es_t if L == "es" else fr_t}</div>')


P_ALL = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 2 · guion de la profesora · 1 hora · todo se puede hacer en la silla" if L == "es"
     else "Cours 2 · version française · même ordre et mêmes numéros que la version espagnole") +
    '</div><h1>' + ("Yoga suave · silla, de pie o suelo" if L == "es" else "Yoga doux · chaise, debout ou sol") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="fl lc">SILLA</span> = para todos · <span class="fl lp">DE PIE</span> <span class="fl lf">SUELO</span> = opciones'
     if L == "es" else
     '<span class="fl lc">CHAISE</span> = pour tous · <span class="fl lp">DEBOUT</span> <span class="fl lf">SOL</span> = options') +
    '</div></div>',
    note("texte normal = <b>version chaise, pour tout le monde</b> (même ceux qui ne peuvent pas se lever). Blocs bleus "
         "« DE PIE » et verts « EN EL SUELO » = options pour les plus mobiles. Chaise stable, sans accoudoirs ni roulettes, "
         "pieds à plat. <b>Aucune rétention de souffle.</b> Une respiration de silence après chaque phrase. "
         "En retard : saute O (genou levé) ou N (déesse). Jamais la relaxation."),
    band(1, ("Bienvenida", "Accueil"), "0:00 – 0:03"),
    grid([card2("chair_sit", "tadasana", "P", ("Cada uno elige", "Chacun choisit"), None, (
        "Hola a todos, bienvenidos. Hoy hacemos ejercicios nuevos. Todo se puede hacer sentados en la silla; quien "
        "quiera y pueda, tendrá opciones de pie o en el suelo. La silla siempre está bien. Nos sentamos un poco hacia "
        "delante, sin apoyar la espalda, pies bien apoyados a la anchura de las caderas. Espalda larga, hombros relajados. "
        "**Nada debe doler.** Si algo no se siente bien, paramos y descansamos.",
        "Bonjour à tous, bienvenue. Aujourd’hui on fait des exercices nouveaux. Tout peut se faire assis sur la chaise ; "
        "ceux qui veulent et qui peuvent auront des options debout ou au sol. La chaise, c’est toujours bien. On s’assoit "
        "un peu vers l’avant, sans s’appuyer au dossier, pieds bien posés largeur de hanches. Dos long, épaules détendues. "
        "**Rien ne doit faire mal.** Si quelque chose ne va pas, on s’arrête et on se repose."))], cols=1),
    band(2, ("Respiración de inicio", "Respiration du début"), "0:03 – 0:09"),
    grid([
        card2("r_chair", "r_floor", "F", ("A · Respirar en las costillas", "A · Respirer dans les côtes"), ("6 resp.", "6 resp."), (
            "Cerramos los ojos si queréis. Colocamos las manos a los lados de las costillas. Inhalamos por la nariz y "
            "sentimos cómo las costillas empujan suavemente las manos hacia fuera. Exhalamos despacio y las costillas "
            "vuelven. Sin forzar. ((6 respiraciones))",
            "On ferme les yeux si vous voulez. On pose les mains sur les côtés des côtes. On inspire par le nez et on sent "
            "les côtes pousser doucement les mains vers l’extérieur. On expire lentement et les côtes reviennent. Sans "
            "forcer. ((6 respirations))")),
        card2("c_arms_up", "arms_up", "P", ("B · Brazos delante y arriba", "B · Bras devant et en haut"), ("5 veces", "5 fois"), (
            "Abrimos los ojos. Inhalamos y subimos los brazos por delante, despacio, hasta donde es cómodo. Exhalamos y "
            "los bajamos despacio por delante. El movimiento dura lo mismo que la respiración. ((5 veces))",
            "On ouvre les yeux. On inspire et on monte les bras par l’avant, lentement, jusqu’où c’est confortable. On "
            "expire et on les baisse lentement par l’avant. Le mouvement dure autant que la respiration. ((5 fois))")),
    ]),
    band(3, ("Calentamiento", "Échauffement"), "0:09 – 0:20"),
    grid([
        card2("n_chair", "n_stand", "P", ("C · Mirar a los lados", "C · Regarder sur les côtés"), ("3 por lado", "3 par côté"), (
            "Espalda larga. Exhalamos y giramos la cabeza despacio para mirar a la derecha. Inhalamos, al centro. "
            "Exhalamos, miramos a la izquierda. Inhalamos, al centro. Movimiento pequeño, sin forzar.",
            "Dos long. On expire et on tourne lentement la tête pour regarder à droite. On inspire, au centre. On expire, "
            "on regarde à gauche. On inspire, au centre. Petit mouvement, sans forcer.")),
        card2("e_chair", "e_stand", "P", ("D · Codos que se abren", "D · Coudes qui s’ouvrent"), ("5 veces", "5 fois"), (
            "Las manos detrás de la cabeza, o en los hombros. Inhalamos y abrimos los codos hacia los lados: el pecho se "
            "abre. Exhalamos y juntamos los codos delante. ((5 veces))",
            "Les mains derrière la tête, ou sur les épaules. On inspire et on ouvre les coudes sur les côtés : la poitrine "
            "s’ouvre. On expire et on rapproche les coudes devant. ((5 fois))")),
        card2("a_chair", "a_stand", "P", ("E · Círculos de brazos", "E · Cercles de bras"), ("5 + 5", "5 + 5"), (
            "Brazos abiertos a los lados, a la altura de los hombros, o más bajos. Pequeños círculos hacia delante… y "
            "hacia atrás. Si se cansan, bajamos los brazos y descansamos.",
            "Bras ouverts sur les côtés, à hauteur d’épaules, ou plus bas. Petits cercles vers l’avant… et vers l’arrière. "
            "S’ils fatiguent, on baisse les bras et on se repose.")),
        card2("c_wrists", "fing_stand", "P", ("F · Manos y dedos", "F · Mains et doigts"), ("5 + 5", "5 + 5"), (
            "Brazos delante, codos doblados. Tocamos cada dedo con el pulgar, uno por uno, y volvemos. Después abrimos "
            "bien las manos y cerramos los puños, suavemente. ((5 veces))",
            "Bras devant, coudes pliés. On touche chaque doigt avec le pouce, un par un, et on revient. Puis on ouvre bien "
            "les mains et on ferme les poings, doucement. ((5 fois))")),
        card2("heeltoe_chair", "toes_stand", "P", ("G · Talones y puntas", "G · Talons et pointes"), ("8 veces", "8 fois"), (
            "Pies en el suelo. Subimos las puntas de los pies; bajamos. Subimos los talones; bajamos. ((8 veces)) "
            "[DP]Las manos en el respaldo o en la pared: subimos los talones despacio y bajamos.[/DP]",
            "Pieds au sol. On monte les pointes des pieds ; on redescend. On monte les talons ; on redescend. ((8 fois)) "
            "[DP]Les mains sur le dossier ou au mur : on monte les talons doucement et on redescend.[/DP]")),
        card2("c_march", "march_stand", "P", ("H · Marcha con brazos", "H · Marche avec les bras"), ("16 pasos", "16 pas"), (
            "Levantamos una rodilla y la otra, como si camináramos, y los brazos se mueven como al caminar. Despacio. "
            "((16 pasos)) [DP]Marchamos en el sitio, una mano en la silla o en la pared si hace falta.[/DP]",
            "On lève un genou puis l’autre, comme si on marchait, et les bras bougent comme en marchant. Doucement. "
            "((16 pas)) [DP]On marche sur place, une main sur la chaise ou au mur si besoin.[/DP]")),
    ]),
    part(1, "Posturas · en la silla o de pie · 0:20 – 0:40", "Postures · sur la chaise ou debout · 0:20 – 0:40"),
    band(4, ("Estirar y abrir", "Étirer et ouvrir"), "0:20 – 0:28"),
    grid([
        card2("p_chair", "p_stand", "P", ("I · La palmera", "I · Le palmier"), ("3 resp./lado", "3 resp./côté"), (
            "Inhalamos y subimos los dos brazos; podemos juntar las manos arriba. Exhalamos y nos inclinamos un poco a la "
            "izquierda, como una palmera con el viento. ((3 resp.)) Inhalamos, al centro. Exhalamos, a la derecha. "
            "((3 resp.)) Si cuesta, una sola mano arriba y la otra en el asiento.",
            "On inspire et on monte les deux bras ; on peut joindre les mains en haut. On expire et on se penche un peu à "
            "gauche, comme un palmier dans le vent. ((3 resp.)) On inspire, au centre. On expire, à droite. ((3 resp.)) "
            "Si c’est difficile, une seule main en haut, l’autre sur le siège.")),
        card2("g_chair", "g_stand", "P", ("J · Brazos de águila", "J · Bras d’aigle"), ("3 resp./lado", "3 resp./côté"), (
            "Brazos delante. Cruzamos el brazo derecho por encima del izquierdo, doblamos los codos y acercamos las "
            "palmas. O simplemente nos abrazamos: manos en los hombros. Inhalamos, subimos un poco los codos. "
            "((3 resp.)) Cambiamos de brazo.",
            "Bras devant. On croise le bras droit par-dessus le gauche, on plie les coudes et on rapproche les paumes. "
            "Ou simplement on se fait un câlin : mains sur les épaules. On inspire, on monte un peu les coudes. "
            "((3 resp.)) On change de bras.")),
        card2("chest_chair", "chest_stand", "P", ("K · Abrir el pecho", "K · Ouvrir la poitrine"), ("3 resp.", "3 resp."), (
            "Las manos atrás, en el borde del asiento o en el respaldo. Inhalamos: el pecho sube y se abre, los hombros "
            "van atrás. Miramos al frente. ((3 resp.)) Exhalamos, soltamos. "
            "[DP]De pie: las manos juntas detrás de la espalda, o en la parte baja de la espalda.[/DP]",
            "Les mains derrière, sur le bord du siège ou sur le dossier. On inspire : la poitrine monte et s’ouvre, les "
            "épaules vont en arrière. Regard devant. ((3 resp.)) On expire, on relâche. "
            "[DP]Debout : les mains jointes derrière le dos, ou sur le bas du dos.[/DP]")),
        card2("chair_cat", "cat", "F", ("Gato-vaca (repaso)", "Chat-vache (rappel)"), ("4 veces", "4 fois"), (
            "Manos en las rodillas. Inhalamos, abrimos el pecho. Exhalamos, redondeamos la espalda. ((4 veces)) "
            "[SU]A cuatro apoyos, si las rodillas están cómodas.[/SU]",
            "Mains sur les genoux. On inspire, on ouvre la poitrine. On expire, dos rond. ((4 fois)) "
            "[SU]À quatre pattes, si les genoux sont à l’aise.[/SU]")),
    ]),
    band(5, ("Fuerza y equilibrio", "Force et équilibre"), "0:28 – 0:40"),
    note("pour le côté droit : <b>chaise — jambe droite pliée</b>. Debout, la chaise ou le mur à côté de la jambe avant. "
         "Démontre en miroir."),
    grid([
        card2("w1_chair", "w1_stand", "P", ("L · Guerrero I", "L · Guerrier I"), ("3 resp./lado", "3 resp./côté"), (
            "Sentados en el borde, un poco de lado. La pierna derecha delante, rodilla encima del tobillo. La pierna "
            "izquierda se estira atrás, con la punta del pie en el suelo. Inhalamos, brazos arriba, o manos en la cintura. "
            "((3 resp.)) Cambiamos de lado. "
            "[DP]Un paso largo atrás con el pie izquierdo, rodilla derecha doblada, una mano en la silla si hace falta.[/DP]",
            "Assis au bord, un peu de côté. La jambe droite devant, genou au-dessus de la cheville. La jambe gauche "
            "s’allonge en arrière, pointe du pied au sol. On inspire, bras en haut, ou mains sur la taille. ((3 resp.)) "
            "On change de côté. [DP]Un grand pas en arrière avec le pied gauche, genou droit plié, une main sur la chaise "
            "si besoin.[/DP]")),
        card2("t_chair", "t_stand", "P", ("M · Triángulo", "M · Triangle"), ("3 resp./lado", "3 resp./côté"), (
            "Piernas separadas, pie derecho hacia fuera. Inhalamos, brazos a los lados. Exhalamos: nos inclinamos a la "
            "derecha, mano derecha en el muslo o la rodilla, brazo izquierdo arriba. ((3 resp.)) Cambiamos de lado. "
            "[DP]Piernas estiradas y separadas; la mano de abajo entre la cintura y la rodilla, nunca empuja.[/DP]",
            "Jambes écartées, pied droit vers l’extérieur. On inspire, bras sur les côtés. On expire : on se penche à "
            "droite, main droite sur la cuisse ou le genou, bras gauche en haut. ((3 resp.)) On change de côté. "
            "[DP]Jambes tendues et écartées ; la main du bas entre la taille et le genou, elle ne pousse jamais.[/DP]")),
        card2("d_chair", "d_stand", "P", ("N · La diosa", "N · La déesse"), ("4 resp.", "4 resp."), (
            "Piernas bien separadas, puntas de los pies un poco hacia fuera, rodillas en la misma dirección. Brazos en "
            "forma de cactus: codos a la altura de los hombros, manos arriba. Inhalamos, abrimos el pecho. ((4 resp.)) "
            "[DP]Pies separados, rodillas un poco dobladas, sin bajar mucho.[/DP]",
            "Jambes bien écartées, pointes des pieds un peu vers l’extérieur, genoux dans la même direction. Bras en "
            "cactus : coudes à hauteur d’épaules, mains en haut. On inspire, on ouvre la poitrine. ((4 resp.)) "
            "[DP]Pieds écartés, genoux un peu pliés, sans descendre beaucoup.[/DP]")),
        card2("knee_chair", "knee_stand", "P", ("O · Rodilla arriba", "O · Genou levé"), ("3 resp./lado", "3 resp./côté"), (
            "Manos a los lados del asiento. Levantamos la rodilla derecha un poco y la sostenemos. Miramos un punto fijo. "
            "((3 resp.)) Bajamos y cambiamos. "
            "[DP]Una mano en la silla o en la pared. Levantamos la rodilla, solo un poco. Si perdemos el equilibrio, no "
            "pasa nada.[/DP]",
            "Mains sur les côtés du siège. On soulève un peu le genou droit et on le tient. Regard sur un point fixe. "
            "((3 resp.)) On repose et on change. [DP]Une main sur la chaise ou au mur. On lève le genou, juste un peu. Si "
            "on perd l’équilibre, ce n’est pas grave.[/DP]")),
    ]),
    part(2, "En la silla o en el suelo · 0:40 – 1:00", "Sur la chaise ou au sol · 0:40 – 1:00"),
    band(6, ("Caderas y espalda", "Hanches et dos"), "0:40 – 0:48"),
    note("ceux qui vont au sol descendent doucement, une main sur la chaise. Les autres restent assis."),
    grid([
        card2("fig4_chair", "fig4_floor", "F", ("P · El número 4", "P · Le chiffre 4"), ("4 resp./lado", "4 resp./côté"), (
            "Apoyamos el tobillo derecho sobre la rodilla izquierda, el pie flexionado para proteger la rodilla. Espalda "
            "larga; si es cómodo, nos inclinamos un poco. ((4 resp.)) Cambiamos. Si no es cómodo, el pie derecho se queda "
            "en el suelo, delante del izquierdo. "
            "[SU]Tumbados, pie izquierdo en el suelo: tobillo derecho sobre la rodilla izquierda.[/SU]",
            "On pose la cheville droite sur le genou gauche, pied fléchi pour protéger le genou. Dos long ; si c’est "
            "confortable, on se penche un peu. ((4 resp.)) On change. Si ce n’est pas confortable, le pied droit reste au "
            "sol, devant le gauche. [SU]Allongés, pied gauche au sol : cheville droite sur le genou gauche.[/SU]")),
        card2("c_fold", "seated_fold", "F", ("Q · Dejarse caer hacia delante", "Q · Se laisser tomber en avant"), ("4 resp.", "4 resp."), (
            "Pies separados. Exhalamos: el pecho baja hacia los muslos, los brazos cuelgan, la cabeza relajada. "
            "((4 resp.)) Inhalamos y subimos muy despacio; la cabeza sube la última. Si nos mareamos, bajamos menos. "
            "[SU]Sentados, piernas delante, rodillas dobladas; el pecho un poco hacia delante.[/SU]",
            "Pieds écartés. On expire : la poitrine descend vers les cuisses, les bras pendent, tête relâchée. ((4 resp.)) "
            "On inspire et on remonte très lentement ; la tête monte en dernier. Si la tête tourne, on descend moins. "
            "[SU]Assis, jambes devant, genoux pliés ; la poitrine un peu vers l’avant.[/SU]")),
        card2("c_twist", "twist_R", "F", ("R · Torsión", "R · Torsion"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda en la rodilla derecha, mano derecha en el respaldo. Inhalamos, espalda larga. Exhalamos y "
            "giramos a la derecha. ((3 resp.)) Cambiamos. "
            "[SU]Tumbados, brazos en cruz: rodillas juntas a la derecha, miramos a la izquierda.[/SU]",
            "Main gauche sur le genou droit, main droite sur le dossier. On inspire, dos long. On expire, on tourne à "
            "droite. ((3 resp.)) On change. [SU]Allongés, bras en croix : genoux serrés à droite, regard à gauche.[/SU]")),
    ]),
    band(7, ("Relajación · 5 minutos", "Relaxation · 5 minutes"), "0:48 – 0:54"),
    grid([card2("c_relax", "savasana", "F", ("Relajación", "Relaxation"), ("5 min", "5 min"), (
        "Nos sentamos atrás, la espalda apoyada en el respaldo. Pies en el suelo, un poco separados. Manos sobre los "
        "muslos, palmas hacia arriba. La barbilla baja un poco. Cerramos los ojos. "
        "[SU]Tumbados boca arriba; si es más cómodo, rodillas dobladas.[/SU]"
        "Sentimos el peso del cuerpo: los pies pesan en el suelo… las piernas pesan… los brazos pesan… los hombros "
        "bajan… la cara se suaviza. Con cada exhalación, soltamos un poco más. ((5 minutos de silencio)) "
        "[T] Movemos los dedos. Abrimos los ojos. Desde el suelo: giramos a la derecha y nos sentamos despacio.",
        "On s’assoit au fond, dos contre le dossier. Pieds au sol, un peu écartés. Mains sur les cuisses, paumes vers le "
        "haut. Le menton descend un peu. On ferme les yeux. [SU]Allongés sur le dos ; si c’est plus confortable, genoux "
        "pliés.[/SU]On sent le poids du corps : les pieds sont lourds sur le sol… les jambes sont lourdes… les bras sont "
        "lourds… les épaules descendent… le visage s’adoucit. À chaque expiration, on relâche un peu plus. "
        "((5 minutes de silence)) [T] On bouge les doigts. On ouvre les yeux. Depuis le sol : on roule à droite et on "
        "s’assoit doucement."), mh=17)], cols=1),
    band(8, ("Respiración final y cierre", "Respiration finale et clôture"), "0:54 – 1:00"),
    grid([
        card2("chair_sit", "seated_cross", "F", ("S · Labios como para soplar", "S · Lèvres comme pour souffler"), ("6 veces", "6 fois"), (
            "Inhalamos por la nariz… dos, tres. Exhalamos despacio por la boca, con los labios casi cerrados, como para "
            "apagar una vela muy despacio… cuatro, cinco, seis. ((6 veces))",
            "On inspire par le nez… deux, trois. On expire lentement par la bouche, lèvres presque fermées, comme pour "
            "éteindre une bougie très doucement… quatre, cinq, six. ((6 fois))")),
        card2("chair_sit", "seated_cross", "F", ("T · La abeja «mmm»", "T · L’abeille « mmm »"), ("4 veces", "4 fois"), (
            "Inhalamos por la nariz. Exhalamos con la boca cerrada, haciendo un sonido suave: «mmmm», como una abeja. "
            "Sentimos la vibración. ((4 veces)) Después, manos delante del pecho: gracias por practicar conmigo. Namasté.",
            "On inspire par le nez. On expire bouche fermée, avec un son doux : « mmmm », comme une abeille. On sent la "
            "vibration. ((4 fois)) Puis mains devant la poitrine : merci d’avoir pratiqué avec moi. Namasté.")),
    ]),
    band(9, ("Si sobra tiempo · opciones", "S’il reste du temps · options"), "+2 – 8 min", opt=True),
    note("U et V avant la relaxation ; W pour les plus mobiles."),
    grid([
        card2("c_wrists", "fing_stand", "P", ("U · Despertar el cuerpo", "U · Réveiller le corps"), ("1 min", "1 min"), (
            "Con las manos, damos golpecitos suaves: brazos, hombros, piernas. Después frotamos las manos y las ponemos "
            "sobre los ojos.",
            "Avec les mains, on tapote doucement : bras, épaules, jambes. Puis on frotte les mains et on les pose sur les "
            "yeux.")),
        card2("c_march", "march_stand", "P", ("V · Apretar y soltar", "V · Serrer et relâcher"), ("3 veces", "3 fois"), (
            "Inhalamos y apretamos suavemente puños, brazos y piernas. Exhalamos y lo soltamos todo. ((3 veces))",
            "On inspire et on serre doucement poings, bras et jambes. On expire et on relâche tout. ((3 fois))")),
        card2("chair_sit", "stand_hold", "P", ("W · Levantarse y sentarse", "W · Se lever, s’asseoir"), ("3–5 veces", "3–5 fois"), (
            "Empujamos los pies contra el suelo y apretamos los muslos tres segundos, sin levantarnos. "
            "[DP]Pies firmes, manos en los muslos: nos levantamos despacio y nos sentamos despacio.[/DP]",
            "On pousse les pieds contre le sol et on serre les cuisses trois secondes, sans se lever. "
            "[DP]Pieds bien posés, mains sur les cuisses : on se lève doucement et on se rassoit doucement.[/DP]")),
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
body { font-size:10pt; line-height:1.2; } .qcue { font-size:10pt; } .qn { font-size:10.4pt; }
.qc.c2 { flex-direction:column; } .qf.row2 { flex-direction:row; gap:3mm; justify-content:center; width:100%; align-items:flex-end; }
.f2 { display:flex; flex-direction:column; align-items:center; gap:.4mm; }
.fl { font-size:6.6pt; font-weight:700; color:#fff; border-radius:1mm; padding:0 1.2mm; letter-spacing:.04em; }
.lc { background:#a07c52; } .lp { background:#4a6fa5; } .lf { background:#3f8a5a; }
.qgrid .qc { break-inside: avoid; } .qband { break-after: avoid; } .pm { break-after: avoid; }
"""

body = "".join(P_ALL)
title = "Yoga · clase 2 (ES)" if L == "es" else "Yoga · cours 2 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase2_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
