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
# COURSE 2 · everyone can do the CHAIR version (main text).
# Coloured blocks: [DP] standing (chair, wall or no support) · [SU] on the floor.
# ===================================================================


def part(n, es_t, fr_t):
    return (f'<div class="part"><span>{"PARTE" if L == "es" else "PARTIE"} {n}</span>'
            f'{es_t if L == "es" else fr_t}</div>')


p1 = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 2 · guion de la profesora · 1 hora · todo se puede hacer sentado en una silla" if L == "es"
     else "Cours 2 · version française · même ordre et mêmes numéros que la version espagnole") +
    '</div><h1>' + ("Yoga suave en silla" if L == "es" else "Yoga doux sur chaise") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="vb vs inl"><span class="vl">DE PIE</span></span> <span class="vb vf inl"><span class="vl">EN EL SUELO</span></span>'
     if L == "es" else
     '<span class="vb vs inl"><span class="vl">DEBOUT</span></span> <span class="vb vf inl"><span class="vl">AU SOL</span></span>') +
    ' · <span class="pause">' + ("gris = pausa" if L == "es" else "gris = pause") + '</span></div></div>',
    note("le texte normal = <b>version assise sur chaise, pour tout le monde</b>. Blocs bleus « DE PIE » et verts "
         "« EN EL SUELO » = options pour les plus mobiles : tu les proposes, ils choisissent. Une chaise par personne. "
         "Pas de rétention de souffle. Prends ton temps : laisse 1 respiration de silence après chaque phrase. "
         "En retard : saute le 6 (arbre) ou la ronde 3. Jamais la relaxation."),
    band(1, ("Bienvenida", "Accueil"), "0:00 – 0:04"),
    grid([card(["chair_sit"], ("Sentados en la silla", "Assis sur la chaise"), None, (
        "Hola a todos, bienvenidos otra vez. Hoy hacemos toda la clase sentados en la silla. Quien quiera y pueda, "
        "tendrá también opciones de pie o en el suelo; pero la silla siempre está bien. Nos sentamos un poco hacia "
        "delante, sin apoyar la espalda. Pies bien apoyados en el suelo, a la anchura de las caderas. Rodillas encima "
        "de los tobillos. Manos sobre los muslos, espalda larga, hombros relajados. Recordad: **nada debe doler**. "
        "Si algo no se siente bien, paramos y descansamos.",
        "Bonjour à tous, bienvenue à nouveau. Aujourd’hui on fait tout le cours assis sur la chaise. Ceux qui veulent "
        "et qui peuvent auront aussi des options debout ou au sol ; mais la chaise, c’est toujours bien. On s’assoit un "
        "peu vers l’avant, sans s’appuyer au dossier. Pieds bien posés au sol, largeur de hanches. Genoux au-dessus des "
        "chevilles. Mains sur les cuisses, dos long, épaules détendues. Rappel : **rien ne doit faire mal**. Si quelque "
        "chose ne va pas, on s’arrête et on se repose."))], cols=1),
    band(2, ("Respiración de inicio", "Respiration du début"), "0:04 – 0:10"),
    grid([
        card(["chair_sit"], ("A · Sentir la respiración", "A · Sentir la respiration"), ("6 resp.", "6 resp."), (
            "Cerramos los ojos si queréis. Una mano en el abdomen y otra en el pecho. Inhalamos lentamente por la nariz "
            "y dejamos que el abdomen y las costillas se expandan suavemente. Exhalamos despacio y dejamos que vuelvan. "
            "Sin forzar. Inhalamos… dos, tres, cuatro. Exhalamos… dos, tres, cuatro. ((6 respiraciones))",
            "On ferme les yeux si vous voulez. Une main sur le ventre, l’autre sur la poitrine. On inspire lentement par "
            "le nez et on laisse le ventre et les côtes s’ouvrir doucement. On expire lentement et on les laisse revenir. "
            "Sans forcer. On inspire… deux, trois, quatre. On expire… deux, trois, quatre. ((6 respirations))")),
        card(["c_breath"], ("B · Brazos y respiración", "B · Bras et respiration"), ("5 veces", "5 fois"), (
            "Abrimos los ojos. Brazos a los lados. Inhalamos y subimos los brazos por los lados, despacio. Exhalamos y "
            "los bajamos despacio. El movimiento dura lo mismo que la respiración. ((5 veces)) Los brazos suben solo "
            "hasta donde es cómodo; pueden quedarse a la altura de los hombros.",
            "On ouvre les yeux. Bras le long du corps. On inspire et on monte les bras sur les côtés, lentement. On expire "
            "et on les baisse lentement. Le mouvement dure autant que la respiration. ((5 fois)) Les bras montent "
            "seulement jusqu’où c’est confortable ; ils peuvent rester à hauteur d’épaules.")),
    ]),
    band(3, ("Calentamiento en la silla", "Échauffement sur la chaise"), "0:10 – 0:22"),
    grid([
        card(["c_neck"], ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), (
            "Espalda larga. Exhalamos: oreja derecha hacia el hombro derecho. ((3 resp.)) Inhalamos, al centro. "
            "Exhalamos: oreja izquierda hacia el hombro izquierdo. ((3 resp.)) Al centro. Después, la barbilla baja "
            "despacio hacia el pecho y vuelve. ((3 veces)) Movimiento pequeño.",
            "Dos long. On expire : oreille droite vers l’épaule droite. ((3 resp.)) On inspire, au centre. On expire : "
            "oreille gauche vers l’épaule gauche. ((3 resp.)) Au centre. Puis le menton descend doucement vers la "
            "poitrine et revient. ((3 fois)) Petit mouvement.")),
        card(["c_shoulders"], ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), (
            "Inhalamos, subimos los hombros hacia las orejas. Exhalamos, atrás y abajo. Cinco círculos hacia atrás… "
            "cinco hacia delante. Círculos pequeños.",
            "On inspire, épaules vers les oreilles. On expire, en arrière et en bas. Cinq cercles vers l’arrière… cinq "
            "vers l’avant. Petits cercles.")),
        card(["c_wrists"], ("Manos y muñecas", "Mains et poignets"), ("5 + 5", "5 + 5"), (
            "Brazos delante, codos un poco doblados. Abrimos bien las manos… cerramos los puños, suavemente. ((5 veces)) "
            "Después, círculos con las muñecas, cinco hacia cada lado.",
            "Bras devant, coudes un peu pliés. On ouvre bien les mains… on ferme les poings, doucement. ((5 fois)) "
            "Puis des cercles avec les poignets, cinq de chaque côté.")),
        card(["c_ankles"], ("Tobillos y pies", "Chevilles et pieds"), ("5 + 5", "5 + 5"), (
            "Levantamos un poco el pie derecho: círculos con el tobillo, cinco hacia cada lado. Cambiamos de pie. "
            "Después, con los dos pies en el suelo: subimos los talones… y subimos las puntas. ((5 veces)) "
            "El talón puede quedarse en el suelo.",
            "On soulève un peu le pied droit : cercles avec la cheville, cinq de chaque côté. On change de pied. Puis, "
            "les deux pieds au sol : on monte les talons… puis les pointes. ((5 fois)) Le talon peut rester au sol.")),
        card(["c_march"], ("Marcha sentados", "Marche assise"), ("10 pasos", "10 pas"), (
            "Manos a los lados del asiento. Levantamos la rodilla derecha un poco, bajamos; la rodilla izquierda, bajamos. "
            "Como si camináramos, despacio. ((10 pasos)) Espalda larga, respiración tranquila. Levantamos poco los pies "
            "si hace falta.",
            "Mains sur les côtés du siège. On monte un peu le genou droit, on redescend ; le genou gauche, on redescend. "
            "Comme si on marchait, lentement. ((10 pas)) Dos long, respiration tranquille. On soulève peu les pieds si "
            "besoin.")),
        card(["c_side_R"], ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda en el borde del asiento, o el brazo cuelga al lado de la silla. Inhalamos, brazo derecho "
            "arriba. Exhalamos, nos inclinamos a la izquierda. ((3 resp.)) Al centro y cambiamos de lado. Si hace falta, "
            "la mano de arriba en la cintura.",
            "Main gauche sur le bord du siège, ou le bras pend à côté de la chaise. On inspire, bras droit en haut. "
            "On expire, on se penche à gauche. ((3 resp.)) Au centre et on change de côté. Si besoin, la main du haut "
            "sur la taille.")),
        card(["c_twist"], ("Torsión", "Torsion"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda por fuera de la rodilla derecha; mano derecha en el respaldo. Inhalamos, espalda larga. "
            "Exhalamos y giramos suavemente hacia la derecha; la cabeza sigue, sin forzar el cuello. ((3 resp.)) "
            "Al centro y cambiamos: mano derecha en la rodilla izquierda, mano izquierda en el respaldo.",
            "Main gauche à l’extérieur du genou droit ; main droite sur le dossier. On inspire, dos long. On expire, on "
            "tourne doucement vers la droite ; la tête suit, sans forcer le cou. ((3 resp.)) Au centre et on change : "
            "main droite sur le genou gauche, main gauche sur le dossier.")),
        card(["chair_cow", "chair_cat"], ("Vaca-gato", "Vache-chat"), ("5 veces", "5 fois"), (
            "Manos en las rodillas. Inhalamos: abrimos el pecho y miramos un poco arriba. Exhalamos: redondeamos la "
            "espalda y miramos al ombligo. ((5 veces)) Movimiento pequeño.",
            "Mains sur les genoux. On inspire : on ouvre la poitrine, regard un peu en haut. On expire : dos rond, regard "
            "vers le nombril. ((5 fois)) Petit mouvement."), row=True, mh=14),
    ]),
]

SUN = [
    ("chair_sit", ("1 Manos al corazón", "1 Mains au cœur"), "exh"), ("c_arms_up", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("c_fold", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("c_fold", ("5 Flexión", "5 Flexion"), "exh"), ("c_arms_up", ("6 Subimos, brazos arriba", "6 On remonte, bras en haut"), "inh"),
    ("chair_sit", ("7 Manos al corazón", "7 Mains au cœur"), "exh"),
]
SUN_STEPS = [
    (1, ("**Corazón.** Sentados, espalda larga, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Assis, dos long, paumes jointes devant la poitrine. On expire.")),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos. Hasta donde es cómodo.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte. Jusqu’où c’est confortable.")),
    (3, ("**Flexión.** Exhalamos: bajamos los brazos y llevamos el pecho hacia los muslos; las manos se deslizan por "
         "las piernas. La cabeza relajada. Solo un poco, si hace falta.",
         "**Flexion.** On expire : on baisse les bras et la poitrine va vers les cuisses ; les mains glissent sur les "
         "jambes. Tête relâchée. Juste un peu, si besoin.")),
    (4, ("**Espalda larga.** Inhalamos: manos en los muslos o en las rodillas, alargamos la espalda hacia delante, "
         "miramos al suelo.",
         "**Dos long.** On inspire : mains sur les cuisses ou les genoux, on allonge le dos vers l’avant, regard au sol.")),
    (5, ("**Flexión.** Exhalamos, volvemos a bajar el pecho.", "**Flexion.** On expire, la poitrine redescend.")),
    (6, ("**Subimos.** Inhalamos: subimos despacio con la espalda larga, brazos arriba. La cabeza sube la última.",
         "**On remonte.** On inspire : on remonte doucement dos long, bras en haut. La tête monte en dernier.")),
    (7, ("**Corazón.** Exhalamos, manos delante del pecho. ((1 resp.))",
         "**Cœur.** On expire, mains devant la poitrine. ((1 resp.))")),
]

p2 = [
    part(1, "En la silla · con opciones de pie · 0:22 – 0:40", "Sur la chaise · avec options debout · 0:22 – 0:40"),
    band(4, ("Saludo al sol en la silla · 3 rondas", "Salutation au soleil sur chaise · 3 rondes"), "0:22 – 0:28"),
    note("ronde 1 très lente, avec tout le texte ; ronde 2 juste les mots en gras + Inhalamos/Exhalamos ; ronde 3 "
         "un mouvement par respiration (optionnelle)."),
    strip(SUN, 0.17), steps(SUN_STEPS),
    '<div class="cue1">' + T((
        "[DP]Quien quiera, puede hacerlo de pie, delante de su silla o de la pared: las manos en el respaldo, en la pared "
        "o en los muslos en los pasos 3 a 5; y caminamos un poco hacia atrás para alargar la espalda.[/DP]",
        "[DP]Ceux qui veulent peuvent le faire debout, devant leur chaise ou le mur : les mains sur le dossier, au mur ou "
        "sur les cuisses aux étapes 3 à 5 ; et on recule un peu pour allonger le dos.[/DP]")) + "</div>",
    band(5, ("Guerreros en la silla", "Guerriers sur la chaise"), "0:28 – 0:37"),
    note("assis tout au bord de la chaise. Côté droit : la jambe droite s’ouvre sur le côté, genou plié ; la jambe gauche "
         "s’allonge en arrière/côté, pied au sol. Face à eux, montre en miroir."),
    strip([("chair_sit", ("Al borde", "Au bord"), None), ("c_w2_R", ("Guerrero II", "Guerrier II"), RESP(3)),
           ("c_rev_R", ("Inverso", "Inversé"), RESP(3)), ("c_sa_R", ("Ángulo lateral", "Angle latéral"), RESP(3)),
           ("c_w2_R", ("Guerrero II", "Guerrier II"), "inh"), ("chair_sit", ("Pies al centro", "Pieds au centre"), "exh")], 0.13),
    steps([
        (1, ("**Al borde de la silla.** Nos sentamos en el borde. Giramos un poco hacia la derecha: la pierna derecha se "
             "abre hacia el lado, rodilla doblada encima del tobillo. La pierna izquierda se estira hacia atrás y al lado, "
             "el pie apoyado en el suelo.",
             "**Au bord de la chaise.** On s’assoit au bord. On tourne un peu vers la droite : la jambe droite s’ouvre sur "
             "le côté, genou plié au-dessus de la cheville. La jambe gauche s’allonge vers l’arrière et le côté, pied au "
             "sol.")),
        (2, ("**Guerrero II.** Inhalamos: brazos en cruz, a la altura de los hombros. Miramos la mano derecha. "
             "((3 resp.)) Si se cansan los brazos, manos en la cintura.",
             "**Guerrier II.** On inspire : bras en croix, à hauteur d’épaules. Regard sur la main droite. ((3 resp.)) "
             "Si les bras fatiguent, mains sur la taille.")),
        (3, ("**Guerrero inverso.** Mano izquierda sobre el muslo izquierdo. Inhalamos: brazo derecho arriba, solo un "
             "poco hacia atrás. ((3 resp.))",
             "**Guerrier inversé.** Main gauche sur la cuisse gauche. On inspire : bras droit en haut, juste un peu en "
             "arrière. ((3 resp.))")),
        (4, ("**Ángulo lateral.** Exhalamos: antebrazo derecho sobre el muslo derecho. Brazo izquierdo arriba, o mano en "
             "la cintura. ((3 resp.))",
             "**Angle latéral.** On expire : avant-bras droit sur la cuisse droite. Bras gauche en haut, ou main sur la "
             "taille. ((3 resp.))")),
        (5, ("**Volvemos.** Inhalamos, subimos. Exhalamos: los pies vuelven al centro. Nos sentamos bien. "
             "[T] Mismo camino hacia la izquierda.",
             "**On revient.** On inspire, on remonte. On expire : les pieds reviennent au centre. On se rassoit bien. "
             "[T] Même chemin vers la gauche.")),
    ]),
    '<div class="cue1">' + T((
        "[DP]De pie, como en la clase anterior: la silla o la pared al lado de la pierna que se dobla. Pies separados, "
        "pie derecho hacia fuera, rodilla derecha encima del tobillo; la mano derecha en el respaldo si hace falta.[/DP]",
        "[DP]Debout, comme au cours précédent : la chaise ou le mur à côté de la jambe qui se plie. Pieds écartés, pied "
        "droit vers l’extérieur, genou droit au-dessus de la cheville ; la main droite sur le dossier si besoin.[/DP]")) + "</div>",
]

p3 = [
    strip([("chair_sit", ("Al borde", "Au bord"), None), ("c_w2_L", ("Guerrero II", "Guerrier II"), RESP(3)),
           ("c_rev_L", ("Inverso", "Inversé"), RESP(3)), ("c_sa_L", ("Ángulo lateral", "Angle latéral"), RESP(3)),
           ("chair_sit", ("Pies al centro", "Pieds au centre"), "exh")], 0.13),
    steps([
        (1, ("Al borde. La pierna izquierda se abre al lado, rodilla doblada; la derecha se estira atrás.",
             "Au bord. La jambe gauche s’ouvre sur le côté, genou plié ; la droite s’allonge en arrière.")),
        (2, ("Inhalamos: **Guerrero II**, brazos en cruz, miramos la mano izquierda. ((3 resp.))",
             "On inspire : **Guerrier II**, bras en croix, regard sur la main gauche. ((3 resp.))")),
        (3, ("**Inverso:** mano derecha en el muslo derecho, brazo izquierdo arriba. ((3 resp.))",
             "**Inversé :** main droite sur la cuisse droite, bras gauche en haut. ((3 resp.))")),
        (4, ("Exhalamos: **ángulo lateral**, antebrazo izquierdo sobre el muslo izquierdo. ((3 resp.))",
             "On expire : **angle latéral**, avant-bras gauche sur la cuisse gauche. ((3 resp.))")),
        (5, ("Inhalamos, subimos. Exhalamos, pies al centro.", "On inspire, on remonte. On expire, pieds au centre.")),
    ], cols=2),
    band(6, ("Árbol en la silla", "Arbre sur la chaise"), "0:37 – 0:40", opt=True),
    grid([card(["c_tree_R"], ("Árbol", "Arbre"), ("3 resp./lado", "3 resp./côté"), (
        "Sentados. Apoyamos el talón derecho en el tobillo izquierdo; la rodilla derecha se abre hacia el lado. Manos "
        "delante del pecho, o brazos arriba. Miramos un punto fijo. ((3 resp.)) Cambiamos de lado. "
        "[DP]De pie, una mano en la silla o en la pared: talón derecho en el tobillo izquierdo, o el pie en la "
        "pantorrilla. Nunca sobre la rodilla.[/DP]",
        "Assis. On pose le talon droit sur la cheville gauche ; le genou droit s’ouvre sur le côté. Mains devant la "
        "poitrine, ou bras en haut. Regard sur un point fixe. ((3 resp.)) On change de côté. "
        "[DP]Debout, une main sur la chaise ou au mur : talon droit sur la cheville gauche, ou le pied sur le mollet. "
        "Jamais sur le genou.[/DP]"), mh=17)], cols=1),
    part(2, "En la silla · con opciones en el suelo · 0:40 – 1:00", "Sur la chaise · avec options au sol · 0:40 – 1:00"),
    band(7, ("Caderas, piernas y espalda", "Hanches, jambes et dos"), "0:40 – 0:47"),
    note("ceux qui vont au sol : ils descendent doucement, une main sur la chaise. Les autres restent assis."),
    grid([
        card(["chair_sit"], ("Mariposa", "Papillon"), ("4 resp.", "4 resp."), (
            "Rodillas separadas, pies en el suelo, manos en los muslos. Inhalamos, espalda larga. Exhalamos, nos "
            "inclinamos un poco hacia delante, sin forzar. ((4 resp.)) "
            "[SU]Plantas de los pies juntas, rodillas hacia los lados; no empujamos las rodillas.[/SU]",
            "Genoux écartés, pieds au sol, mains sur les cuisses. On inspire, dos long. On expire, on se penche un peu vers "
            "l’avant, sans forcer. ((4 resp.)) [SU]Plantes des pieds jointes, genoux sur les côtés ; on ne pousse pas les "
            "genoux.[/SU]"), mh=16),
        card(["chair_hamstring"], ("Estiramiento de pierna", "Étirement de jambe"), ("4 resp./lado", "4 resp./côté"), (
            "Estiramos la pierna derecha delante, talón en el suelo. Inhalamos, espalda larga. Exhalamos, el pecho un poco "
            "hacia delante; manos en el muslo. ((4 resp.)) Cambiamos de pierna. "
            "[SU]Piernas delante, rodillas dobladas; el pecho un poco hacia delante.[/SU]",
            "On allonge la jambe droite devant, talon au sol. On inspire, dos long. On expire, la poitrine un peu vers "
            "l’avant ; mains sur la cuisse. ((4 resp.)) On change de jambe. "
            "[SU]Jambes devant, genoux pliés ; la poitrine un peu vers l’avant.[/SU]"), mh=16),
        card(["chair_knee"], ("Rodilla al pecho", "Genou poitrine"), ("3 resp./lado", "3 resp./côté"), (
            "Abrazamos la rodilla derecha y la acercamos un poco al pecho. Espalda larga. ((3 resp.)) Cambiamos. "
            "Si cuesta, cogemos detrás del muslo. "
            "[SU]Tumbados: rodillas al pecho; después, rodillas a la derecha y a la izquierda, como un limpiaparabrisas.[/SU]",
            "On serre le genou droit et on le rapproche un peu de la poitrine. Dos long. ((3 resp.)) On change. Si c’est "
            "difficile, on tient l’arrière de la cuisse. "
            "[SU]Allongés : genoux à la poitrine ; puis genoux à droite et à gauche, comme un essuie-glace.[/SU]"), mh=16),
        card(["c_twist"], ("Torsión suave", "Torsion douce"), ("3 resp./lado", "3 resp./côté"), (
            "Como al principio: mano izquierda en la rodilla derecha, mano derecha en el respaldo. Exhalamos y giramos a la "
            "derecha. ((3 resp.)) Cambiamos de lado. "
            "[SU]Tumbados, brazos en cruz: rodillas juntas a la derecha, miramos a la izquierda. Cambiamos.[/SU]",
            "Comme au début : main gauche sur le genou droit, main droite sur le dossier. On expire, on tourne à droite. "
            "((3 resp.)) On change de côté. [SU]Allongés, bras en croix : genoux serrés à droite, regard à gauche. "
            "On change.[/SU]"), mh=16),
    ]),
]

p4 = [
    band(8, ("Relajación en la silla · 5 minutos", "Relaxation sur la chaise · 5 minutes"), "0:47 – 0:53"),
    note("<b>savasana sur chaise</b> : dos contre le dossier, pieds à plat un peu écartés, mains sur les cuisses paumes "
         "vers le haut, menton légèrement baissé. Ne jamais raccourcir. Lis lentement, avec de longues pauses."),
    grid([card(["c_relax", "savasana"], ("Relajación", "Relaxation"), ("5 min", "5 min"), (
        "Nos sentamos atrás, con la espalda apoyada en el respaldo. Pies en el suelo, un poco separados. Manos sobre los "
        "muslos, palmas hacia arriba. La barbilla baja un poco. Cerramos los ojos. "
        "[SU]Tumbados boca arriba, piernas relajadas, brazos un poco separados; si es más cómodo, rodillas dobladas.[/SU]"
        "Dejamos que la silla nos sostenga. Relajamos los pies… las piernas… las caderas… el abdomen… el pecho… los "
        "hombros… los brazos… las manos… el cuello… la cara. La respiración es natural. No hay nada que hacer. Solo "
        "descansar. ((5 minutos de silencio)) [T] Poco a poco, movemos los dedos de las manos y de los pies. Abrimos los "
        "ojos. Desde el suelo: giramos a la derecha y nos sentamos despacio.",
        "On s’assoit au fond, le dos contre le dossier. Pieds au sol, un peu écartés. Mains sur les cuisses, paumes vers "
        "le haut. Le menton descend un peu. On ferme les yeux. "
        "[SU]Allongés sur le dos, jambes détendues, bras un peu écartés ; si c’est plus confortable, genoux pliés.[/SU]"
        "On laisse la chaise nous porter. On relâche les pieds… les jambes… les hanches… le ventre… la poitrine… les "
        "épaules… les bras… les mains… le cou… le visage. La respiration est naturelle. Rien à faire. Juste se reposer. "
        "((5 minutes de silence)) [T] Petit à petit, on bouge les doigts et les orteils. On ouvre les yeux. Depuis le "
        "sol : on roule à droite et on s’assoit doucement."), mh=15, row=True)], cols=1),
    band(9, ("Respiración final", "Respiration finale"), "0:53 – 0:58"),
    grid([
        card(["chair_sit"], ("A · Exhalación larga", "A · Expiration longue"), ("6 veces", "6 fois"), (
            "Sentados, espalda larga. Inhalamos por la nariz… dos, tres, cuatro. Exhalamos despacio por la nariz… dos, "
            "tres, cuatro, cinco, seis. Sin forzar: si cuesta, exhalamos hasta cuatro. ((6 veces))",
            "Assis, dos long. On inspire par le nez… deux, trois, quatre. On expire lentement par le nez… deux, trois, "
            "quatre, cinq, six. Sans forcer : si c’est difficile, on expire sur quatre. ((6 fois))")),
        card(["chair_sit"], ("B · Suspiro", "B · Soupir"), ("3 veces", "3 fois"), (
            "Inhalamos por la nariz. Exhalamos por la boca, despacio, con un suspiro: «aaah». Soltamos los hombros. "
            "((3 veces)) Después, las manos en el corazón y tres respiraciones tranquilas.",
            "On inspire par le nez. On expire par la bouche, lentement, avec un soupir : « aaah ». On relâche les épaules. "
            "((3 fois)) Puis les mains sur le cœur et trois respirations tranquilles.")),
    ]),
    band(10, ("Cierre", "Clôture"), "0:58 – 1:00"),
    grid([card(["chair_sit"], ("Cierre", "Clôture"), None, (
        "Juntamos las manos delante del pecho. Observamos cómo nos sentimos ahora, sin juzgar. Gracias por practicar "
        "conmigo. Namasté.",
        "Mains jointes devant la poitrine. On observe comment on se sent maintenant, sans juger. Merci d’avoir pratiqué "
        "avec moi. Namasté."), mh=13)], cols=1),
    band(11, ("Si sobra tiempo · opciones", "S’il reste du temps · options"), "+2 – 8 min", opt=True),
    note("A et B avant la relaxation ; C juste après la respiration de départ ou avant la relaxation."),
    grid([
        card(["c_wrists"], ("A · Masaje de manos", "A · Massage des mains"), ("1 min", "1 min"), (
            "Frotamos las manos. Con el pulgar derecho, masajeamos la palma izquierda, despacio, y cada dedo. "
            "Cambiamos de mano.",
            "On frotte les mains. Avec le pouce droit, on masse la paume gauche, lentement, et chaque doigt. "
            "On change de main.")),
        card(["c_march"], ("B · Apretar y soltar", "B · Serrer et relâcher"), ("3 veces", "3 fois"), (
            "Inhalamos y apretamos suavemente los puños, los brazos y las piernas. Exhalamos y lo soltamos todo. "
            "((3 veces))",
            "On inspire et on serre doucement les poings, les bras et les jambes. On expire et on relâche tout. "
            "((3 fois))")),
        card(["stand_hold"], ("C · Levantarse y sentarse", "C · Se lever, s’asseoir"), ("3–5 veces", "3–5 fois"), (
            "Sentados: empujamos los pies contra el suelo y apretamos los muslos tres segundos, sin levantarnos. "
            "[DP]Pies firmes, manos en los muslos: nos levantamos despacio y nos sentamos despacio.[/DP]",
            "Assis : on pousse les pieds contre le sol et on serre les cuisses trois secondes, sans se lever. "
            "[DP]Pieds bien posés, mains sur les cuisses : on se lève doucement et on se rassoit doucement.[/DP]")),
    ], cols=3),
]


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
body { font-size:10.6pt; line-height:1.24; } .qcue { font-size:10.6pt; } .qn { font-size:11pt; }
"""

pages = [p1, p2, p3, p4]
body = "".join(f'<div class="pg">{"".join(p)}</div>' for p in pages)
title = "Yoga · clase 2 (ES)" if L == "es" else "Yoga · cours 2 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase2_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
