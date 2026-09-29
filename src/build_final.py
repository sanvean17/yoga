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
    for k, (es, fr, c) in TOKENS.items():
        h = h.replace(k, f'<span class="it {c}">{es if L == "es" else fr}</span>')
    return h


def rich_fr(t):
    import html as H
    t = H.escape(t, quote=False)
    t = re.sub(r"\(\(([^)]*)\)\)", r'<span class="pause">\1</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return SIDE_FR.sub(lambda m: f'<span class="{"sr" if m.group(1).startswith("dr") else "sl"}">{m.group(1)}</span>', t)


def card(poses, name, badge, text, mh=16, mw=24, row=False):
    figs = "".join(fig(p, max_w=mw, max_h=mh, cap=0.115) for p in poses)
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

# =================================================================== PAGE 1
p1 = [
    '<div class="top"><div><div class="kick">' +
    ("Guion de la profesora · 1 hora · principiantes · se lee en voz alta" if L == "es"
     else "Version française du guion · même ordre, même numéros que la version espagnole") +
    '</div><h1>' + ("Yoga para principiantes" if L == "es" else "Yoga pour débutants") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b>" +
    (" del alumno" if L == "es" else " de l’élève") + '<br>' +
    ('<span class="inh"><i>▲</i>Inhalamos</span> <span class="exh"><i>▼</i>Exhalamos</span>'
     if L == "es" else '<span class="inh"><i>▲</i>Inspire</span> <span class="exh"><i>▼</i>Expire</span>') +
    ' · <span class="pause">' + ("gris = pausa" if L == "es" else "gris = pause") + '</span></div></div>',
    note("lis lentement ; démontre en miroir mais <b>dis</b> le côté écrit. ≈ 60 min. En retard : saute la ronde 3 ou "
         "l’arbre, <b>jamais Savasana (4–5 min)</b>. En avance : section 13 « Si sobra tiempo »."),
    band(1, ("Bienvenida y cómo sentarnos", "Accueil et comment s’asseoir"), "0:00 – 0:05"),
    grid([
        card(["seated_cross", "legs_long_bent", "kneeling"], ("Sentarnos", "S’asseoir"), None, (
            "Hola a todos, bienvenidos. Me llamo ___. Es una clase para principiantes: vamos a ir despacio. "
            "Nos sentamos de la forma más cómoda: piernas cruzadas; piernas estiradas con las rodillas un poco "
            "dobladas; o sobre los talones, si es cómodo para las rodillas. Manos sobre los muslos, espalda larga, "
            "hombros relajados. [F] Podéis cambiar de posición cuando queráis.",
            "Bonjour à tous, bienvenue. Je m’appelle ___. C’est un cours pour débutants : on va doucement. "
            "On s’assoit le plus confortablement : jambes croisées ; jambes allongées, genoux un peu pliés ; ou sur "
            "les talons si c’est confortable pour les genoux. Mains sur les cuisses, dos long, épaules détendues. "
            "[F] Vous pouvez changer de position quand vous voulez."), mh=12, row=True),
        card(["child"], ("Qué vamos a hacer", "Ce qu’on va faire"), None, (
            "Hoy vamos a intentar coordinar el movimiento con la respiración. Muchas veces inhalaremos para crecer "
            "o abrir el cuerpo, y exhalaremos para bajar o entrar suavemente en una postura. No buscamos una postura "
            "perfecta. Cada cuerpo es diferente. **Nada debe doler.** Si algo no se siente bien, paramos y "
            "descansamos. Podéis volver a la **postura del niño** cuando queráis.",
            "Aujourd’hui on va essayer de coordonner le mouvement et la respiration. Souvent on inspirera pour "
            "grandir ou ouvrir le corps, et on expirera pour descendre ou entrer doucement dans une posture. On ne "
            "cherche pas la posture parfaite. Chaque corps est différent. **Rien ne doit faire mal.** Si quelque "
            "chose ne va pas, on s’arrête et on se repose. Vous pouvez revenir à la **posture de l’enfant** quand "
            "vous voulez.")),
    ]),
    band(2, ("Respiración", "Respiration"), "0:05 – 0:08"),
    grid([card(["seated_cross"], ("Respiración tranquila", "Respiration tranquille"), RESP(5), (
        "[D] Sentados. Cerramos los ojos si queréis. Colocamos una mano en el abdomen y otra en el pecho. "
        "Inhalamos lentamente por la nariz y dejamos que el abdomen y las costillas se expandan suavemente. "
        "Exhalamos y dejamos que vuelvan. Sin forzar. Inhalamos… dos, tres, cuatro. Exhalamos… dos, tres, cuatro. "
        "((5 respiraciones)) [F] Si contar resulta incómodo, respiramos sin contar. "
        "[T] Manos a los muslos, abrimos los ojos despacio.",
        "[D] Assis. On ferme les yeux si vous voulez. Une main sur le ventre, l’autre sur la poitrine. On inspire "
        "lentement par le nez et on laisse le ventre et les côtes s’ouvrir doucement. On expire et on les laisse "
        "revenir. Sans forcer. On inspire… deux, trois, quatre. On expire… deux, trois, quatre. ((5 respirations)) "
        "[F] Si compter gêne, on respire sans compter. [T] Mains sur les cuisses, on ouvre les yeux doucement."))],
         cols=1),
    band(3, ("Calentamiento sentado", "Échauffement assis"), "0:08 – 0:15"),
    grid([
        card(["seated_neck"], ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), (
            "Espalda larga. Exhalamos: oreja derecha hacia el hombro derecho; el hombro izquierdo baja. ((3 resp.)) "
            "Inhalamos, al centro. Exhalamos: oreja izquierda al hombro izquierdo. ((3 resp.)) Inhalamos, al centro. "
            "[F] Movimiento pequeño, sin tirar con la mano.",
            "Dos long. On expire : oreille droite vers l’épaule droite ; l’épaule gauche descend. ((3 resp.)) "
            "On inspire, au centre. On expire : oreille gauche vers l’épaule gauche. ((3 resp.)) On inspire, au centre. "
            "[F] Petit mouvement, sans tirer avec la main.")),
        card(["seated_shoulders"], ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), (
            "Inhalamos, subimos los hombros hacia las orejas. Exhalamos, atrás y abajo. Cinco círculos hacia "
            "atrás… cinco hacia delante. [F] Círculos pequeños. [T] Hombros quietos y relajados.",
            "On inspire, épaules vers les oreilles. On expire, en arrière et en bas. Cinq cercles vers l’arrière… "
            "cinq vers l’avant. [F] Petits cercles. [T] Épaules immobiles et détendues.")),
        card(["sidebend_R"], ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda al suelo, junto a la cadera. Inhalamos, brazo derecho arriba. Exhalamos, nos "
            "inclinamos a la izquierda; los dos glúteos en el suelo. ((3 resp.)) Al centro y cambiamos: mano "
            "derecha al suelo, brazo izquierdo arriba, hacia la derecha. [F] Poco, mano en la cintura.",
            "Main gauche au sol près de la hanche. On inspire, bras droit en haut. On expire, on se penche à gauche ; "
            "les deux fesses au sol. ((3 resp.)) Au centre et on change : main droite au sol, bras gauche en haut, "
            "vers la droite. [F] Un peu seulement, main sur la taille.")),
        card(["seated_twist"], ("Torsión sentada", "Torsion assise"), ("2 resp./lado", "2 resp./côté"), (
            "Mano izquierda sobre la rodilla derecha, mano derecha en el suelo detrás. Inhalamos y alargamos la "
            "espalda. Exhalamos y giramos suavemente hacia la derecha. No forzamos. ((2 resp.)) Volvemos al centro "
            "y cambiamos de lado. [F] Giramos poco; el cuello no hace fuerza.",
            "Main gauche sur le genou droit, main droite au sol derrière. On inspire, on allonge le dos. On expire, "
            "on tourne doucement vers la droite. On ne force pas. ((2 resp.)) Retour au centre, on change de côté. "
            "[F] On tourne peu ; le cou ne force pas.")),
        card(["wrists"], ("Muñecas", "Poignets"), ("5 + 5", "5 + 5"), (
            "Extendemos los brazos delante y hacemos círculos suaves con las muñecas. ((5)) Cambiamos de "
            "dirección. ((5)) [F] Codos un poco doblados. [T] Nos ponemos de rodillas, mirando hacia delante.",
            "On tend les bras devant et on fait des cercles doux avec les poignets. ((5)) On change de sens. ((5)) "
            "[F] Coudes un peu pliés. [T] On se met à genoux, face à l’avant.")),
        card(["tabletop"], ("Cuatro apoyos", "Quatre pattes"), RESP(2), (
            "Manos debajo de los hombros, dedos abiertos. Rodillas debajo de las caderas. Empeines en el suelo. "
            "Espalda larga como una mesa, miramos entre las manos. [F] Esterilla doblada bajo las rodillas.",
            "Mains sous les épaules, doigts écartés. Genoux sous les hanches. Dessus des pieds au sol. Dos long comme "
            "une table, regard entre les mains. [F] Tapis plié sous les genoux.")),
    ]),
    band(4, ("Vaca-gato · niño · perro boca abajo", "Vache-chat · enfant · chien tête en bas"), "0:15 – 0:21"),
    grid([
        card(["cow", "cat"], ("Vaca / gato", "Vache / chat"), ("5 veces", "5 fois"), (
            "Solo se mueve la espalda. **Vaca:** inhalamos, baja el abdomen, pecho delante, miramos un poco arriba. "
            "**Gato:** exhalamos, empujamos el suelo, redondeamos la espalda, miramos al ombligo. "
            "[F] Movimiento pequeño. [T] Espalda plana.",
            "Seul le dos bouge. **Vache :** on inspire, le ventre descend, poitrine en avant, regard un peu en haut. "
            "**Chat :** on expire, on pousse le sol, dos rond, regard vers le nombril. [F] Petit mouvement. "
            "[T] Dos plat."), mh=11),
        card(["child"], ("Postura del niño", "Posture de l’enfant"), RESP(3), (
            "Dedos gordos juntos, rodillas un poco separadas. Exhalamos, caderas hacia los talones. Brazos largos, "
            "frente al suelo. ((3 resp.)) [F] Frente sobre los puños. Es nuestra postura de descanso. "
            "[T] Inhalamos, volvemos a cuatro apoyos.",
            "Gros orteils joints, genoux un peu écartés. On expire, hanches vers les talons. Bras longs, front au "
            "sol. ((3 resp.)) [F] Front sur les poings. C’est notre posture de repos. [T] On inspire, retour à "
            "quatre pattes.")),
    ]),
    strip([("child", ("Niño", "Enfant"), None), ("tabletop", ("Cuatro apoyos", "Quatre pattes"), "inh"),
           ("tabletop_toes", ("Puntas de los pies", "Pointe des pieds"), None),
           ("downdog_lift", ("Caderas arriba y atrás", "Hanches haut et arrière"), "exh"),
           ("downdog", ("Perro boca abajo", "Chien tête en bas"), ("3–5 resp.", "3–5 resp."))], 0.12),
    grid([card(["downdog"], ("Perro boca abajo", "Chien tête en bas"), ("3–5 resp.", "3–5 resp."), (
        "Apoyamos las puntas de los pies en el suelo. Presionamos bien las manos. Exhalamos y llevamos las caderas "
        "hacia arriba y hacia atrás. Doblamos las rodillas todo lo que necesitemos: lo importante es alargar la "
        "espalda. Los talones no necesitan tocar el suelo. Relajamos la cabeza y el cuello. ((3–5 resp.)) "
        "[F] Si necesitamos descansar, rodillas al suelo y postura del niño.",
        "On pose la pointe des pieds au sol (orteils retournés). On appuie bien les mains. On expire, hanches vers le "
        "haut et l’arrière. On plie les genoux autant qu’il faut : l’important est d’allonger le dos. Les talons "
        "n’ont pas besoin de toucher le sol. Tête et cou détendus. ((3–5 resp.)) [F] Pour se reposer, genoux au "
        "sol et posture de l’enfant."))], cols=1),
]

# =================================================================== PAGE 2
SUN = [
    ("tadasana_heart", ("1 Corazón", "1 Cœur"), "exh"), ("arms_up", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("fold", ("3 Flexión", "3 Flexion"), "exh"),
    (("half_lift", "half_lift_thighs"), ("4 Espinillas / muslos", "4 Tibias / cuisses"), "inh"),
    ("step_back_R_knee", ("5 Pie D atrás, rodilla", "5 Pied D arrière, genou"), "exh"),
    ("plank_knees", ("6 Dos rodillas", "6 Deux genoux"), "inh"), ("prone", ("7 Al suelo", "7 Au sol"), "exh"),
    ("cobra", ("8 Cobra suave", "8 Cobra douce"), "inh"), ("tabletop", ("9 Cuatro apoyos", "9 Quatre pattes"), "inh"),
    ("downdog", ("10 Perro", "10 Chien"), ("3 resp.", "3 resp.")),
    ("half_lift_thighs", ("11 Caminamos", "11 On marche"), "inh"), ("fold", ("12 Flexión", "12 Flexion"), "exh"),
    ("arms_up", ("13 Subimos", "13 On remonte"), "inh"), ("tadasana_heart", ("14 Corazón", "14 Cœur"), "exh"),
]
R1 = [
    (1, ("**Corazón.** Pies a la anchura de las caderas, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Pieds largeur de hanches, paumes jointes devant la poitrine. On expire.")),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos. Hombros lejos de las orejas. "
         "[F] Solo hasta donde es cómodo.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte. Épaules loin des oreilles. "
         "[F] Seulement jusqu’où c’est confortable.")),
    (3, ("**Flexión.** Exhalamos: doblamos las rodillas, el pecho baja hacia los muslos. Cabeza relajada.",
         "**Flexion.** On expire : genoux pliés, la poitrine descend vers les cuisses. Tête relâchée.")),
    (4, ("**Media elevación.** Inhalamos, alargamos la espalda. Manos en las espinillas o en los muslos, justo por "
         "encima de las rodillas; no directamente sobre las rodillas. Miramos al suelo.",
         "**Demi-flexion.** On inspire, on allonge le dos. Mains sur les tibias ou sur les cuisses, juste au-dessus "
         "des genoux ; pas directement sur les genoux. Regard au sol.")),
    (5, ("**Pie derecho atrás.** Exhalamos: manos al suelo, llevamos el pie derecho atrás y apoyamos la rodilla "
         "derecha en el suelo.",
         "**Pied droit derrière.** On expire : mains au sol, le pied droit recule et on pose le genou droit au sol.")),
    (6, ("**Dos rodillas.** Inhalamos. Llevamos el pie izquierdo atrás y apoyamos también la rodilla izquierda. Ahora "
         "tenemos las dos rodillas en el suelo. Hombros encima de las muñecas, cuerpo largo desde la cabeza hasta "
         "las rodillas.",
         "**Deux genoux.** On inspire. Le pied gauche recule et on pose aussi le genou gauche. Les deux genoux sont "
         "au sol. Épaules au-dessus des poignets, corps long de la tête aux genoux.")),
    (7, ("**Bajamos.** Exhalamos, doblamos los codos cerca del cuerpo y bajamos lentamente hasta tumbarnos boca abajo.",
         "**On descend.** On expire, coudes pliés près du corps, on descend lentement jusqu’à être à plat ventre.")),
    (8, ("**Cobra suave.** Inhalamos. Empeines en el suelo, codos cerca del cuerpo. Elevamos suavemente el pecho; no "
         "necesitamos subir mucho. La pelvis y las piernas se quedan en el suelo. Hombros lejos de las orejas, cuello "
         "largo. Exhalamos y bajamos.",
         "**Cobra douce.** On inspire. Dessus des pieds au sol, coudes près du corps. On soulève doucement la poitrine ; "
         "pas besoin de monter haut. Bassin et jambes restent au sol. Épaules loin des oreilles, cou long. On expire, "
         "on redescend.")),
    (9, ("**Cuatro apoyos.** Manos debajo de los hombros. Inhalamos, empujamos el suelo y volvemos a cuatro apoyos. "
         "[F] Pasamos por la postura del niño.",
         "**Quatre pattes.** Mains sous les épaules. On inspire, on pousse le sol, retour à quatre pattes. "
         "[F] On passe par la posture de l’enfant.")),
    (10, ("**Perro boca abajo.** Puntas de los pies. Exhalamos, caderas arriba y atrás, rodillas dobladas. ((3 resp.))",
          "**Chien tête en bas.** Pointe des pieds. On expire, hanches en haut et en arrière, genoux pliés. ((3 resp.))")),
    (11, ("**Caminamos hacia las manos.** Rodillas dobladas, miramos entre las manos, pasos pequeños. Inhalamos: "
          "espalda larga, manos en espinillas o muslos.",
          "**On marche vers les mains.** Genoux pliés, regard entre les mains, petits pas. On inspire : dos long, "
          "mains sur tibias ou cuisses.")),
    (12, ("**Flexión.** Exhalamos, torso relajado.", "**Flexion.** On expire, buste relâché.")),
    (13, ("**Subimos.** Inhalamos: rodillas dobladas, subimos despacio, brazos arriba. [F] Manos en las caderas.",
          "**On remonte.** On inspire : genoux pliés, on remonte doucement, bras en haut. [F] Mains sur les hanches.")),
    (14, ("**Corazón.** Exhalamos, manos delante del pecho. ((1 resp.))",
          "**Cœur.** On expire, mains devant la poitrine. ((1 resp.))")),
]
p2 = [
    band(5, ("Flexión relajada · montaña", "Flexion relâchée · montagne"), "0:21 – 0:24"),
    strip([("downdog", ("Perro", "Chien"), None), ("downdog_walk", ("Caminamos", "On marche"), None),
           ("fold", ("Flexión relajada", "Flexion relâchée"), ("4–5 resp.", "4–5 resp.")),
           ("roll_up", ("Subimos despacio", "On remonte"), "inh"), ("tadasana", ("Montaña", "Montagne"), RESP(3))], 0.12),
    grid([
        card(["fold"], ("Flexión relajada", "Flexion relâchée"), ("4–5 resp.", "4–5 resp."), (
            "[D] Perro boca abajo. Doblamos las rodillas, miramos entre las manos y caminamos con pasos pequeños hacia "
            "delante. Doblamos bien las rodillas y dejamos caer el torso sobre los muslos. Cabeza y cuello "
            "completamente relajados. Podemos coger los codos y balancearnos suavemente. ((4–5 resp.)) "
            "[T] Soltamos los brazos. Rodillas dobladas, barbilla hacia el pecho. Inhalamos y subimos despacio. "
            "La cabeza sube la última.",
            "[D] Chien tête en bas. Genoux pliés, regard entre les mains, on marche à petits pas vers l’avant. On plie "
            "bien les genoux et le buste tombe sur les cuisses. Tête et cou complètement relâchés. On peut attraper les "
            "coudes et se balancer doucement. ((4–5 resp.)) [T] On lâche les bras. Genoux pliés, menton vers la "
            "poitrine. On inspire et on remonte doucement. La tête monte en dernier.")),
        card(["tadasana"], ("Montaña", "Montagne"), RESP(3), (
            "Pies paralelos a la anchura de las caderas, peso repartido. Rodillas sueltas, hombros relajados, brazos a "
            "los lados. Miramos al frente. ((3 resp.)) [F] Pies más separados. "
            "[T] Manos al pecho: empezamos el saludo al sol.",
            "Pieds parallèles largeur de hanches, poids réparti. Genoux souples, épaules détendues, bras le long du "
            "corps. Regard devant. ((3 resp.)) [F] Pieds plus écartés. [T] Mains à la poitrine : on commence la "
            "salutation au soleil.")),
    ]),
    band(6, ("Saludo al sol · Ronda 1: muy despacio · pie derecho", "Salutation au soleil · Ronde 1 : très lent · pied droit"),
         "0:24 – 0:29"),
    strip(SUN[:7], 0.105), strip(SUN[7:], 0.105),
    steps(R1),
    '<div class="rt">' + T(("[T] Repetimos con el otro pie.", "[T] On recommence avec l’autre pied.")) + "</div>",
]

# =================================================================== PAGE 3
R2 = [
    (1, ("Corazón. Esta vez empezamos con el pie izquierdo.", "Cœur. Cette fois on commence avec le pied gauche.")),
    (2, ("Inhalamos, brazos arriba.", "On inspire, bras en haut.")),
    (3, ("Exhalamos, flexión, rodillas dobladas.", "On expire, flexion, genoux pliés.")),
    (4, ("Inhalamos, espalda larga: espinillas o muslos.", "On inspire, dos long : tibias ou cuisses.")),
    (5, ("Exhalamos, pie izquierdo atrás, rodilla izquierda al suelo.", "On expire, pied gauche derrière, genou gauche au sol.")),
    (6, ("Inhalamos, pie derecho atrás, dos rodillas al suelo.", "On inspire, pied droit derrière, deux genoux au sol.")),
    (7, ("Exhalamos, codos cerca, bajamos al suelo.", "On expire, coudes près du corps, au sol.")),
    (8, ("Inhalamos, cobra suave. Exhalamos, bajamos.", "On inspire, cobra douce. On expire, on descend.")),
    (9, ("Inhalamos, cuatro apoyos.", "On inspire, quatre pattes.")),
    (10, ("Exhalamos, perro boca abajo. ((3 resp.))", "On expire, chien tête en bas. ((3 resp.))")),
    (11, ("Caminamos. Inhalamos, espalda larga.", "On marche. On inspire, dos long.")),
    (12, ("Exhalamos, flexión.", "On expire, flexion.")),
    (13, ("Inhalamos, subimos, brazos arriba.", "On inspire, on remonte, bras en haut.")),
    (14, ("Exhalamos, corazón.", "On expire, cœur.")),
]
R3 = [
    (1, ("Exhalamos… corazón.", "On expire… cœur.")), (2, ("Inhalamos… brazos arriba.", "On inspire… bras en haut.")),
    (3, ("Exhalamos… flexión.", "On expire… flexion.")), (4, ("Inhalamos… espalda larga.", "On inspire… dos long.")),
    (5, ("Exhalamos… pie derecho atrás, rodilla al suelo.", "On expire… pied droit derrière, genou au sol.")),
    (6, ("Inhalamos… pie izquierdo atrás, dos rodillas.", "On inspire… pied gauche derrière, deux genoux.")),
    (7, ("Exhalamos… bajamos al suelo.", "On expire… au sol.")),
    (8, ("Inhalamos… cobra suave.", "On inspire… cobra douce.")),
    (9, ("Exhalamos… bajamos. Inhalamos… cuatro apoyos.", "On expire… on descend. On inspire… quatre pattes.")),
    (10, ("Exhalamos… perro boca abajo. Nos quedamos aquí. ((3 resp. → flow))",
          "On expire… chien tête en bas. On reste ici. ((3 resp. → flow))")),
]


def flow(right):
    k = "R" if right else "L"
    dog = "downdog" if right else "downdog_L"
    a, b = ("D", "I") if right else ("I", "D")
    fa, fb = ("D", "G") if right else ("G", "D")
    frames = [(dog, ("Perro", "Chien"), None), (f"lunge_{k}", (f"Pie {a} delante", f"Pied {fa} devant"), "exh"),
              (f"lunge_rise_{k}", (f"Pie {b} gira · subimos", f"Pied {fb} tourne · on monte"), "inh"),
              (f"w2_{k}", ("Guerrero II", "Guerrier II"), RESP(3)), (f"rev_{k}", ("Inverso", "Inversé"), RESP(3)),
              (f"sa_{k}", ("Ángulo lateral", "Angle latéral"), RESP(3)), (f"w2_{k}", ("Guerrero II", "Guerrier II"), "inh"),
              (f"lunge_{k}", ("Manos al suelo", "Mains au sol"), "exh"),
              (dog, (f"Pie {a} atrás · perro", f"Pied {fa} arrière · chien"), RESP(3))]
    return strip(frames, 0.098)


FLOW_R = [
    (1, ("**Perro boca abajo.** Empezamos desde aquí. Inhalamos y miramos entre las manos.",
         "**Chien tête en bas.** On part d’ici. On inspire, regard entre les mains.")),
    (2, ("**Pie derecho delante.** Exhalamos: el pie derecho entre las manos, rodilla derecha encima del tobillo. "
         "[F] Rodilla izquierda al suelo y ayudamos al pie con la mano derecha.",
         "**Pied droit devant.** On expire : le pied droit entre les mains, genou droit au-dessus de la cheville. "
         "[F] Genou gauche au sol, on aide le pied avec la main droite.")),
    (3, ("**Subimos.** Giramos el pie izquierdo hacia fuera y apoyamos todo el pie. Inhalamos: subimos el torso, manos "
         "en las caderas. [F] Pies más separados hacia los lados.",
         "**On se redresse.** On tourne le pied gauche vers l’extérieur, tout le pied au sol. On inspire : buste "
         "redressé, mains sur les hanches. [F] Pieds plus écartés sur les côtés.")),
    (4, ("**Guerrero II.** Exhalamos: brazos en cruz, brazo derecho delante. Pecho hacia el lado largo de la esterilla. "
         "Rodilla derecha encima del tobillo, hacia el segundo dedo del pie: no cae hacia dentro. Pierna izquierda "
         "fuerte. Miramos la mano derecha. ((3 resp.)) [F] Pies más cerca o rodilla menos doblada; manos en las caderas.",
         "**Guerrier II.** On expire : bras en croix, bras droit devant. Poitrine vers le grand côté du tapis. Genou "
         "droit au-dessus de la cheville, vers le 2e orteil : il ne tombe pas vers l’intérieur. Jambe gauche forte. "
         "Regard sur la main droite. ((3 resp.)) [F] Pieds plus proches ou genou moins plié ; mains sur les hanches.")),
    (5, ("**Guerrero inverso.** Rodilla derecha doblada. Mano izquierda muy ligera sobre la pierna izquierda, sin peso. "
         "Inhalamos: brazo derecho arriba y un poco atrás. ((3 resp.)) [F] Nos inclinamos menos.",
         "**Guerrier inversé.** Genou droit plié. Main gauche très légère sur la jambe gauche, sans poids. On inspire : "
         "bras droit en haut et un peu en arrière. ((3 resp.)) [F] On se penche moins.")),
    (6, ("**Ángulo lateral.** Inhalamos, al centro. Exhalamos: antebrazo derecho sobre el muslo derecho. Brazo izquierdo "
         "arriba o por encima de la oreja. Pecho abierto. ((3 resp.)) [F] Mano izquierda en la cadera.",
         "**Angle latéral.** On inspire, au centre. On expire : avant-bras droit sur la cuisse droite. Bras gauche en "
         "haut ou au-dessus de l’oreille. Poitrine ouverte. ((3 resp.)) [F] Main gauche sur la hanche.")),
    (7, ("**Guerrero II.** Inhalamos: empujamos con el pie izquierdo, subimos al centro, brazos en cruz.",
         "**Guerrier II.** On inspire : on pousse sur le pied gauche, on remonte, bras en croix.")),
    (8, ("**Manos al suelo.** Exhalamos: manos a cada lado del pie derecho, talón izquierdo arriba. "
         "[F] Rodilla izquierda al suelo.",
         "**Mains au sol.** On expire : mains de chaque côté du pied droit, talon gauche levé. [F] Genou gauche au sol.")),
    (9, ("**Pie derecho atrás · perro.** Exhalamos: pie derecho atrás, caderas arriba. ((3 resp.)) [F] Postura del niño. "
         "[T] Mismo camino con la pierna izquierda.",
         "**Pied droit derrière · chien.** On expire : pied droit derrière, hanches en haut. ((3 resp.)) [F] Enfant. "
         "[T] Même chemin avec la jambe gauche.")),
]
FLOW_L = [
    (1, ("Perro. Inhalamos, miramos entre las manos.", "Chien. On inspire, regard entre les mains.")),
    (2, ("Exhalamos: **pie izquierdo** entre las manos. [F] Rodilla derecha al suelo.",
         "On expire : **pied gauche** entre les mains. [F] Genou droit au sol.")),
    (3, ("Giramos el pie derecho, apoyamos todo el pie. Inhalamos, subimos.", "On tourne le pied droit, tout le pied au sol. On inspire, on monte.")),
    (4, ("Exhalamos: **Guerrero II**, brazo izquierdo delante, rodilla izquierda sobre el tobillo. ((3 resp.))",
         "On expire : **Guerrier II**, bras gauche devant, genou gauche au-dessus de la cheville. ((3 resp.))")),
    (5, ("**Inverso:** mano derecha ligera en la pierna. Inhalamos, brazo izquierdo arriba. ((3 resp.))",
         "**Inversé :** main droite légère sur la jambe. On inspire, bras gauche en haut. ((3 resp.))")),
    (6, ("Exhalamos: **ángulo lateral**, antebrazo izquierdo sobre el muslo. ((3 resp.))",
         "On expire : **angle latéral**, avant-bras gauche sur la cuisse. ((3 resp.))")),
    (7, ("Inhalamos: Guerrero II.", "On inspire : Guerrier II.")),
    (8, ("Exhalamos: manos al suelo junto al pie izquierdo.", "On expire : mains au sol près du pied gauche.")),
    (9, ("Pie izquierdo atrás: perro. ((3 resp.)) [T] Caminamos a las manos. Inhalamos y subimos despacio: montaña.",
         "Pied gauche derrière : chien. ((3 resp.)) [T] On marche vers les mains. On inspire, on remonte doucement : montagne.")),
]
p3 = [
    '<div class="two">'
    '<div class="rnd">' + band("6b", ("Ronda 2 · pie izquierdo", "Ronde 2 · pied gauche"), "0:29 – 0:31") +
    steps(R2) + "</div>"
    '<div class="rnd">' + band("6c", ("Ronda 3 · 1 movimiento = 1 respiración", "Ronde 3 · 1 mouvement = 1 respiration"),
                               "0:31 – 0:34", opt=True) +
    note("si tu sautes la ronde 3 : à l’étape 10 de la ronde 2, reste en chien et enchaîne le flow.") +
    steps(R3) + "</div></div>",
    band(7, ("Flow de pie · lado derecho", "Flow debout · côté droit"), "0:34 – 0:39"),
    note("face à eux, montre avec ta jambe <b>gauche</b> quand tu dis <b class='sr'>derecha</b>."),
    flow(True), steps(FLOW_R),
    band(8, ("Flow de pie · lado izquierdo", "Flow debout · côté gauche"), "0:39 – 0:44"),
    flow(False), steps(FLOW_L, cols=2),
]

# =================================================================== PAGE 4
p4 = [
    band(9, ("Árbol", "Arbre"), "0:44 – 0:47", opt=True),
    grid([card(["tree_R_easy", "tree_R"], ("Árbol", "Arbre"), ("3 resp./lado", "3 resp./côté"), (
        "Miramos un punto fijo. Peso al pie izquierdo. Podemos dejar los dedos del pie derecho en el suelo y apoyar el "
        "talón en el tobillo. O el pie en la pantorrilla: **nunca sobre la rodilla.** Manos al pecho. ((3 resp.)) "
        "Cambiamos de lado. [F] Una mano en la pared. [T] Doblamos las rodillas, manos al suelo, nos sentamos.",
        "Regard sur un point fixe. Poids sur le pied gauche. On peut laisser les orteils du pied droit au sol et poser "
        "le talon sur la cheville. Ou le pied sur le mollet : **jamais sur le genou.** Mains à la poitrine. "
        "((3 resp.)) On change de côté. [F] Une main contre le mur. [T] Genoux pliés, mains au sol, on s’assoit."),
        mh=19, row=True)], cols=1),
    band(10, ("Sentados · mariposa · flexión suave", "Assis · papillon · flexion douce"), "0:47 – 0:53"),
    grid([
        card(["butterfly"], ("Mariposa", "Papillon"), ("3–4 resp.", "3–4 resp."), (
            "Plantas de los pies juntas, rodillas hacia los lados; alejamos los pies si hace falta. Inhalamos, "
            "alargamos la espalda. Exhalamos, nos inclinamos un poco, sin forzar. [F] No empujamos las rodillas.",
            "Plantes des pieds jointes, genoux sur les côtés ; on éloigne les pieds si besoin. On inspire, on allonge "
            "le dos. On expire, on se penche un peu, sans forcer. [F] On ne pousse pas les genoux.")),
        card(["seated_fold"], ("Flexión sentada suave", "Flexion assise douce"), ("4–5 resp.", "4–5 resp."), (
            "Piernas delante, rodillas dobladas. Inhalamos, espalda larga. Exhalamos, el pecho un poco hacia delante. "
            "Manos sobre muslos o piernas: no necesitamos tocar los pies. [F] Más rodillas dobladas. "
            "[T] Inhalamos, subimos. Manos detrás y bajamos despacio boca arriba.",
            "Jambes devant, genoux pliés. On inspire, dos long. On expire, la poitrine un peu vers l’avant. Mains sur "
            "les cuisses ou les jambes : pas besoin de toucher les pieds. [F] Plier plus les genoux. [T] On inspire, "
            "on remonte. Mains derrière, on descend doucement sur le dos.")),
    ]),
    band(11, ("Tumbados · rodillas al pecho · limpiaparabrisas · torsión", "Allongés · genoux poitrine · essuie-glaces · torsion"),
         "0:53 – 0:56"),
    grid([
        card(["knees_chest"], ("Rodillas al pecho", "Genoux poitrine"), RESP(3), (
            "Una rodilla hacia el pecho y después la otra. Abrazamos suavemente las piernas, hombros relajados. "
            "[F] Cogemos detrás de los muslos. [T] Pies al suelo, un poco separados.",
            "Un genou vers la poitrine, puis l’autre. On serre doucement les jambes, épaules détendues. "
            "[F] On tient l’arrière des cuisses. [T] Pieds au sol, un peu écartés.")),
        card(["wipers"], ("Limpiaparabrisas", "Essuie-glaces"), ("4–6 veces", "4–6 fois"), (
            "Dejamos caer lentamente las rodillas hacia la derecha y después hacia la izquierda, como un "
            "limpiaparabrisas. Suavemente, sin forzar. [T] Rodillas juntas, brazos en cruz.",
            "On laisse tomber lentement les genoux à droite puis à gauche, comme un essuie-glace. Doucement, sans "
            "forcer. [T] Genoux serrés, bras en croix.")),
        card(["twist_R"], ("Torsión", "Torsion"), ("3 resp./lado", "3 resp./côté"), (
            "Exhalamos, rodillas hacia la derecha; miramos a la izquierda si es cómodo. ((3 resp.)) Inhalamos, al "
            "centro. Cambiamos de lado. [F] Rodillas solo un poco.",
            "On expire, genoux à droite ; regard à gauche si c’est confortable. ((3 resp.)) On inspire, au centre. "
            "On change de côté. [F] Genoux juste un peu.")),
    ], cols=3),
    band(12, ("Savasana · 4–5 min mínimo · y cierre", "Savasana · 4–5 min minimum · et clôture"), "0:56 – 1:01"),
    grid([
        card(["savasana"], ("Savasana", "Savasana"), ("4–5 min", "4–5 min"), (
            "Nos tumbamos boca arriba. Piernas relajadas, pies sueltos. Brazos un poco separados, palmas hacia arriba. "
            "[F] Rodillas dobladas y pies en el suelo. Cerramos los ojos. Relajamos los pies… las piernas… el "
            "abdomen… los hombros… la cara. ((4–5 min de silencio)) [T] Movemos dedos, giramos a la derecha, nos "
            "sentamos despacio; la cabeza sube la última.",
            "On s’allonge sur le dos. Jambes détendues, pieds relâchés. Bras un peu écartés, paumes vers le haut. "
            "[F] Genoux pliés, pieds au sol. On ferme les yeux. On relâche les pieds… les jambes… le ventre… les "
            "épaules… le visage. ((4–5 min de silence)) [T] On bouge les doigts, on roule à droite, on s’assoit "
            "doucement ; la tête en dernier."), mh=11),
        card(["seated_cross"], ("Cierre", "Clôture"), None, (
            "Manos delante del pecho. Observamos cómo nos sentimos, sin juzgar. Gracias por practicar conmigo. Namasté.",
            "Mains devant la poitrine. On observe comment on se sent, sans juger. Merci d’avoir pratiqué avec moi. "
            "Namasté.")),
    ]),
    band(13, ("Si sobra tiempo · opciones suaves", "S’il reste du temps · options douces"), "+2 – 6 min", opt=True),
    note("à placer <b>avant Savasana</b> (A, B) ou <b>juste avant la clôture</b> (C). Choisis-en une, deux ou trois."),
    grid([
        card(["seated_cow", "seated_cat"], ("A · Vaca-gato sentados", "A · Vache-chat assis"), ("5 veces", "5 fois"), (
            "Sentados, manos en las rodillas. Inhalamos, abrimos el pecho. Exhalamos, redondeamos la espalda y miramos "
            "al ombligo. [F] Movimiento pequeño.",
            "Assis, mains sur les genoux. On inspire, on ouvre la poitrine. On expire, dos rond, regard vers le "
            "nombril. [F] Petit mouvement."), mh=12, row=True),
        card(["leg_stretch"], ("B · Estiramiento de pierna", "B · Étirement de jambe"), ("5 resp./lado", "5 resp./côté"), (
            "Tumbados, pie izquierdo en el suelo. Subimos la pierna derecha y la cogemos detrás del muslo, rodilla un "
            "poco doblada. ((5 resp.)) Cambiamos de pierna. [F] Rodilla más doblada.",
            "Allongés, pied gauche au sol. On monte la jambe droite et on la tient derrière la cuisse, genou un peu "
            "plié. ((5 resp.)) On change de jambe. [F] Genou plus plié."), mh=14),
        card(["seated_cross"], ("C · Respiración final", "C · Respiration finale"), ("6 veces", "6 fois"), (
            "Sentados cómodos, ojos cerrados. Inhalamos por la nariz… dos, tres, cuatro. Exhalamos despacio… dos, "
            "tres, cuatro, cinco, seis. Sin forzar. [F] Si cuesta, exhalamos solo hasta cuatro.",
            "Assis confortablement, yeux fermés. On inspire par le nez… deux, trois, quatre. On expire lentement… "
            "deux, trois, quatre, cinq, six. Sans forcer. [F] Si c’est difficile, on expire seulement sur quatre.")),
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
pages = [p1, p2, p3, p4]
body = "".join(f'<div class="pg">{"".join(p)}</div>' for p in pages)
title = "Yoga · guion (ES)" if L == "es" else "Yoga · guion (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_guion_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
