"""Version 2 of the teaching script: 1 h beginner class, Spanish (Spain),
group language (plural), French translation under every spoken block.

python3 build_v2.py -> ../build/yoga_guion_v2.html ; node print.js ... -> PDF

Spoken-text markup (see build.rich): Inhala/Exhala words and derecha/izquierda
are highlighted automatically; ((...)) = grey stage direction, **x** = bold.
Segment tags: D desde, E entrada, P postura, R respira, F más fácil,
T salida/siguiente, X explico, Z relajación.
"""
import contextlib
import io
import re

with contextlib.redirect_stdout(io.StringIO()):
    import build as B
from build import fig, fig_fixed, rich

BREATH2 = re.compile(r"\b(Inhalamos|inhalamos|Exhalamos|exhalamos|inhalaremos|exhalaremos)\b")


def es(t):
    h = rich(t)

    def br(m):
        w = m.group(1)
        k = "inh" if w.lower().startswith("inh") else "exh"
        a = "▲" if k == "inh" else "▼"
        return f'<span class="{k}"><i>{a}</i>{w}</span>'
    return BREATH2.sub(br, h)


TAGS = {
    "D": ("DESDE", "t-d"), "E": ("ENTRADA", "t-e"), "P": ("POSTURA", "t-p"),
    "R": ("RESPIRA", "t-r"), "F": ("MÁS FÁCIL", "t-f"), "T": ("SALIDA →", "t-t"),
    "X": ("EXPLICO", "t-x"), "Z": ("RELAJACIÓN", "t-x"),
}


def segs(items):
    """items: list of (tag, es, fr). Returns the ES block + the FR block."""
    e = "".join(f'<span class="seg"><span class="tg {TAGS[t][1]}">{TAGS[t][0]}</span>{es(s)}</span> '
                for t, s, _ in items)
    f = " ".join(f'<span class="ftg">{TAGS[t][0].split()[0].lower()}</span>{rich(fr)}' for t, _, fr in items)
    return f'<div class="es">{e}</div><div class="fr"><span class="frl">FR</span>{f}</div>'


def card(figs, name, badges, items, mh=30, mw=40):
    fh = "".join(f'<div class="cf">{fig(p, max_w=mw, max_h=mh if len(figs) == 1 else mh * 0.72, cap=0.24)}'
                 + (f'<div class="fcap">{rich(c)}</div>' if c else "") + "</div>" for p, c in figs)
    bd = "".join(f'<span class="badge b-n">{b}</span>' for b in badges)
    return (f'<div class="card"><div class="cfig"><div class="cname">{rich(name)}</div>{fh}'
            f'<div class="badges">{bd}</div></div><div class="ctext">{segs(items)}</div></div>')


def band(num, title, time, opt=False):
    o = '<span class="opt">opcional</span>' if opt else ""
    return (f'<div class="band"><span class="secn">{num}</span><b>{rich(title)}</b>{o}'
            f'<span class="time">{time}</span></div>')


def note(t):
    return f'<div class="note"><b>Pour moi</b> (ne pas lire) : {t}</div>'


def strip(frames, scale):
    cells = []
    for i, (p, cap, br) in enumerate(frames):
        if i:
            cells.append('<div class="sarrow">→</div>')
        poses = p if isinstance(p, tuple) else (p,)
        svgs = '<span class="sor">o</span>'.join(fig_fixed(x, scale) for x in poses)
        bb = ""
        if br == "inh":
            bb = '<span class="sb inh"><i>▲</i>Inhalamos</span>'
        elif br == "exh":
            bb = '<span class="sb exh"><i>▼</i>Exhalamos</span>'
        elif br:
            bb = f'<span class="sb n">{br}</span>'
        cells.append(f'<div class="sf"><div class="sfig">{svgs}</div><div class="scap">{rich(cap)}</div>{bb}</div>')
    return f'<div class="strip">{"".join(cells)}</div>'


def steps(items, short=False):
    """items: (n, es, fr)"""
    cls = "steps short" if short else "steps"
    if short:
        return (f'<ol class="{cls}">' + "".join(
            f'<li><span class="nn">{n}</span><div><span class="es">{es(e)}</span> '
            f'<span class="fr fri">{rich(f)}</span></div></li>' for n, e, f in items) + "</ol>")
    return (f'<ol class="{cls}">' + "".join(
        f'<li><span class="nn">{n}</span><div><div class="es">{es(e)}</div>'
        f'<div class="fr"><span class="frl">FR</span>{rich(f)}</div></div></li>' for n, e, f in items) + "</ol>")


LQD = '<div class="lqd">LO QUE DIGO <span>· traducción francesa debajo, en gris: no se lee</span></div>'

P = []   # document parts

# =============================================================== HEADER
P.append(
    '<div class="top"><div><div class="kick">Guion de la profesora · clase de 1 hora · principiantes</div>'
    '<h1>Yoga para principiantes</h1></div>'
    '<div class="leg"><b class="sr">naranja = DERECHA</b> · <b class="sl">azul = IZQUIERDA</b> del alumno · '
    'figuras de pie vistas de espaldas<br><span class="inh"><i>▲</i>Inhalamos</span> '
    '<span class="exh"><i>▼</i>Exhalamos</span> · <span class="pause">gris = pausa, no se lee</span></div></div>')
P.append(note(
    "lis l’espagnol à voix haute, lentement ; la ligne FR grise est seulement pour toi. "
    "Démontre en miroir mais <b>dis</b> le côté écrit. Timing total ≈ 61 min : si tu es en retard, "
    "saute la <b>ronde 3</b> ou <b>l’arbre</b>. <b>Jamais Savasana</b> (4–5 min minimum)."))

# =============================================================== 1 INTRO
P += [band(1, "Bienvenida y cómo sentarnos", "0:00 – 0:05"), LQD, card(
    [("seated_cross", "piernas cruzadas"), ("legs_long_bent", "piernas estiradas, rodillas dobladas"),
     ("kneeling", "sobre los talones")], "Sentarnos", [], [
        ("E", "Hola a todos, bienvenidos. Me llamo ___. Es una clase para principiantes: vamos a ir despacio.",
         "Bonjour à tous, bienvenue. Je m’appelle ___. C’est un cours pour débutants : on va doucement."),
        ("P", "Nos sentamos de la forma más cómoda: con las piernas cruzadas; o con las piernas estiradas y las "
              "rodillas un poco dobladas; o sentados sobre los talones, si es cómodo para las rodillas. "
              "Manos sobre los muslos, espalda larga, hombros relajados.",
         "On s’assoit de la façon la plus confortable : jambes croisées ; ou jambes allongées, genoux un peu pliés ; "
         "ou assis sur les talons si c’est confortable pour les genoux. Mains sur les cuisses, dos long, épaules détendues."),
        ("F", "Si en algún momento molesta, podéis cambiar de posición.",
         "Si à un moment ça gêne, vous pouvez changer de position."),
        ("X", "Hoy vamos a intentar coordinar el movimiento con la respiración. Muchas veces inhalaremos para crecer "
              "o abrir el cuerpo, y exhalaremos para bajar o entrar suavemente en una postura. "
              "No buscamos una postura perfecta. Cada cuerpo es diferente. **Nada debe doler.** Si algo no se siente "
              "bien, paramos y descansamos. Podéis volver a la **postura del niño** cuando queráis.",
         "Aujourd’hui on va essayer de coordonner le mouvement et la respiration. Souvent on inspirera pour grandir "
         "ou ouvrir le corps, et on expirera pour descendre ou entrer doucement dans une posture. On ne cherche pas "
         "la posture parfaite. Chaque corps est différent. Rien ne doit faire mal. Si quelque chose ne va pas, on "
         "s’arrête et on se repose. Vous pouvez revenir à la posture de l’enfant quand vous voulez."),
    ], mh=26)]

# =============================================================== 2 BREATH
P += [band(2, "Respiración", "0:05 – 0:08"), card([("seated_cross", None)], "Respiración tranquila", ["5 respiraciones"], [
    ("D", "Seguimos sentados, en la misma posición.", "On reste assis, même position."),
    ("P", "Cerramos los ojos si queréis. Colocamos una mano en el abdomen y otra en el pecho.",
     "On ferme les yeux si vous voulez. Une main sur le ventre, l’autre sur la poitrine."),
    ("R", "Inhalamos lentamente por la nariz y dejamos que el abdomen y las costillas se expandan suavemente. "
          "Exhalamos y dejamos que vuelvan. Sin forzar. Inhalamos… dos, tres, cuatro. Exhalamos… dos, tres, cuatro. "
          "((5 respiraciones))",
     "On inspire lentement par le nez et on laisse le ventre et les côtes s’ouvrir doucement. On expire et on les "
     "laisse revenir. Sans forcer. On inspire… deux, trois, quatre. On expire… deux, trois, quatre."),
    ("F", "Si contar resulta incómodo, respiramos a nuestro ritmo, sin contar.",
     "Si compter gêne, on respire à son rythme, sans compter."),
    ("T", "Bajamos las manos a los muslos y abrimos los ojos despacio.",
     "On pose les mains sur les cuisses et on ouvre les yeux doucement."),
])]

# =============================================================== 3 WARM-UP
P += [band(3, "Calentamiento sentado", "0:08 – 0:15"),
      card([("seated_neck", None)], "Cuello", ["3 resp. por lado"], [
          ("D", "Seguimos sentados, manos sobre los muslos.", "Toujours assis, mains sur les cuisses."),
          ("P", "Alargamos la espalda. Exhalamos e inclinamos la cabeza hacia la derecha: la oreja derecha hacia el "
                "hombro derecho. El hombro izquierdo baja.",
           "On allonge le dos. On expire et on penche la tête à droite : oreille droite vers l’épaule droite. "
           "L’épaule gauche descend."),
          ("R", "Respiramos aquí tres veces. ((3 resp.)) Inhalamos, volvemos al centro. Exhalamos: oreja izquierda "
                "hacia el hombro izquierdo. ((3 resp.)) Inhalamos, al centro.",
           "3 respirations. On inspire, retour au centre. On expire : oreille gauche vers l’épaule gauche. "
           "3 respirations. On inspire, au centre."),
          ("F", "Movimiento pequeño. No tiramos de la cabeza con la mano.",
           "Petit mouvement. On ne tire pas la tête avec la main."),
          ("T", "Dejamos la cabeza en el centro.", "On laisse la tête au centre."),
      ], mh=26),
      card([("seated_shoulders", None)], "Hombros", ["5 + 5 círculos"], [
          ("D", "Sentados, brazos relajados.", "Assis, bras détendus."),
          ("R", "Inhalamos y subimos los hombros hacia las orejas. Exhalamos y los llevamos hacia atrás y hacia abajo. "
                "Cinco círculos hacia atrás… y cinco hacia delante.",
           "On inspire et on monte les épaules vers les oreilles. On expire, on les emmène en arrière et en bas. "
           "Cinq cercles vers l’arrière… et cinq vers l’avant."),
          ("F", "Círculos pequeños, sin prisa.", "Petits cercles, sans se presser."),
          ("T", "Hombros quietos y relajados.", "Épaules immobiles et détendues."),
      ], mh=24),
      card([("sidebend_R", "brazo derecho arriba"), ("sidebend_L", "brazo izquierdo arriba")],
           "Inclinación lateral", ["3 resp. por lado"], [
          ("E", "Apoyamos la mano izquierda en el suelo, junto a la cadera izquierda.",
           "On pose la main gauche au sol, à côté de la hanche gauche."),
          ("P", "Inhalamos y subimos el brazo derecho. Exhalamos y nos inclinamos hacia la izquierda. "
                "Los dos glúteos se quedan en el suelo.",
           "On inspire, on monte le bras droit. On expire, on se penche vers la gauche. Les deux fesses restent au sol."),
          ("R", "Respiramos tres veces. ((3 resp.)) Inhalamos, volvemos al centro; exhalamos, bajamos el brazo. "
                "Cambiamos: mano derecha al suelo, brazo izquierdo arriba, nos inclinamos hacia la derecha. ((3 resp.))",
           "3 respirations. On inspire, retour au centre ; on expire, on baisse le bras. On change : main droite au "
           "sol, bras gauche en haut, on se penche vers la droite."),
          ("F", "Nos inclinamos solo un poco. La mano de arriba puede quedarse en la cintura.",
           "On se penche juste un peu. La main du haut peut rester sur la taille."),
          ("T", "Volvemos al centro y bajamos el brazo.", "Retour au centre, on baisse le bras."),
      ], mh=26),
      card([("seated_twist", None)], "Torsión sentada", ["2 resp. por lado"], [
          ("E", "Colocamos la mano izquierda sobre la rodilla derecha y la mano derecha en el suelo, detrás de nosotros.",
           "Main gauche sur le genou droit, main droite au sol derrière nous."),
          ("P", "Inhalamos y alargamos la espalda. Exhalamos y giramos suavemente hacia la derecha. No forzamos.",
           "On inspire, on allonge le dos. On expire, on tourne doucement vers la droite. On ne force pas."),
          ("R", "Respiramos dos veces. ((2 resp.)) Volvemos al centro y cambiamos de lado: mano derecha sobre la "
                "rodilla izquierda, mano izquierda detrás. Exhalamos y giramos hacia la izquierda. ((2 resp.))",
           "2 respirations. Retour au centre, on change de côté : main droite sur le genou gauche, main gauche "
           "derrière. On expire, on tourne vers la gauche."),
          ("F", "Giramos poco. El cuello no hace fuerza.", "On tourne peu. Le cou ne force pas."),
          ("T", "Volvemos al centro.", "Retour au centre."),
      ], mh=26),
      card([("wrists", None)], "Muñecas", ["5 + 5 círculos"], [
          ("P", "Extendemos los brazos delante, a la altura de los hombros.",
           "On tend les bras devant, à hauteur des épaules."),
          ("R", "Hacemos círculos suaves con las muñecas. ((5 círculos)) Cambiamos de dirección. ((5 círculos))",
           "On fait des cercles doux avec les poignets. On change de sens."),
          ("F", "Si se cansan los brazos, doblamos un poco los codos.",
           "Si les bras fatiguent, on plie un peu les coudes."),
          ("T", "Bajamos los brazos. Descruzamos las piernas, giramos y nos ponemos de rodillas, mirando hacia la "
                "parte delantera de la esterilla.",
           "On baisse les bras. On décroise les jambes, on se tourne et on se met à genoux, face à l’avant du tapis."),
      ], mh=24),
      ]

# =============================================================== 4 ALL FOURS -> DOG
P += [band(4, "Cuatro apoyos · vaca-gato · niño · perro boca abajo", "0:15 – 0:21"),
      card([("tabletop", None)], "Cuatro apoyos", ["2 respiraciones"], [
          ("D", "De rodillas, mirando hacia delante.", "À genoux, face à l’avant."),
          ("E", "Apoyamos las manos justo debajo de los hombros, con los dedos bien abiertos. Rodillas debajo de las "
                "caderas.", "Mains juste sous les épaules, doigts bien écartés. Genoux sous les hanches."),
          ("P", "Los empeines en el suelo. Espalda larga, como una mesa. Miramos al suelo, entre las manos.",
           "Le dessus des pieds au sol. Dos long comme une table. Regard au sol, entre les mains."),
          ("R", "Respiramos aquí dos veces.", "2 respirations."),
          ("F", "Si molestan las rodillas, doblamos la esterilla por la mitad debajo de ellas.",
           "Si les genoux font mal, on plie le tapis en deux sous les genoux."),
          ("T", "Ahora movemos la espalda.", "Maintenant on bouge le dos."),
      ], mh=24),
      card([("cow", "vaca · inhalamos"), ("cat", "gato · exhalamos")], "Vaca y gato", ["5 veces"], [
          ("D", "Desde cuatro apoyos. Manos y rodillas quietas: solo se mueve la espalda.",
           "Depuis quatre pattes. Mains et genoux immobiles : seul le dos bouge."),
          ("R", "**Vaca:** inhalamos, dejamos bajar el abdomen, llevamos el pecho hacia delante y miramos un poco hacia "
                "arriba. **Gato:** exhalamos, empujamos el suelo con las manos, redondeamos la espalda y miramos hacia "
                "el ombligo. Cinco veces, a nuestro ritmo.",
           "Vache : on inspire, le ventre descend, la poitrine va vers l’avant, le regard monte un peu. Chat : on "
           "expire, on pousse le sol, on arrondit le dos, regard vers le nombril. Cinq fois, à notre rythme."),
          ("F", "Movimiento pequeño. El cuello sigue a la espalda, sin forzar.",
           "Petit mouvement. Le cou suit le dos, sans forcer."),
          ("T", "Volvemos a la espalda plana.", "On revient au dos plat."),
      ], mh=24),
      card([("child", None)], "Postura del niño", ["3 respiraciones"], [
          ("D", "Desde cuatro apoyos.", "Depuis quatre pattes."),
          ("E", "Juntamos los dedos gordos de los pies y separamos un poco las rodillas. Exhalamos y llevamos las "
                "caderas hacia los talones.",
           "On rapproche les gros orteils, on écarte un peu les genoux. On expire, les hanches vers les talons."),
          ("P", "Brazos largos delante, la frente en el suelo, hombros relajados.",
           "Bras longs devant, front au sol, épaules détendues."),
          ("R", "Respiramos aquí tres veces.", "3 respirations."),
          ("F", "Si la frente no llega al suelo, la apoyamos sobre los puños. Si las caderas no llegan a los talones, "
                "no pasa nada. Esta es nuestra postura de descanso: podéis volver aquí cuando queráis.",
           "Si le front ne touche pas le sol, on le pose sur les poings. Si les hanches n’arrivent pas aux talons, "
           "ce n’est pas grave. C’est notre posture de repos : vous pouvez y revenir quand vous voulez."),
          ("T", "Inhalamos y volvemos a cuatro apoyos.", "On inspire et on revient à quatre pattes."),
      ], mh=22),
      strip([("child", "Niño", None), ("tabletop", "1 · Cuatro apoyos", "inh"),
             ("tabletop_toes", "2 · Puntas de los pies en el suelo", None),
             ("downdog_lift", "3 · Caderas arriba y atrás", "exh"), ("downdog", "4 · Perro boca abajo", "3–5 resp.")],
            scale=0.19),
      card([("downdog", None)], "Perro boca abajo", ["3 – 5 respiraciones"], [
          ("D", "Desde cuatro apoyos.", "Depuis quatre pattes."),
          ("E", "Apoyamos las puntas de los pies en el suelo. Presionamos bien las manos. Exhalamos y llevamos las "
                "caderas hacia arriba y hacia atrás.",
           "On pose la pointe des pieds (orteils retournés) au sol. On appuie bien les mains. On expire, les hanches "
           "montent vers le haut et l’arrière."),
          ("P", "Doblamos las rodillas todo lo que necesitemos. Lo importante es alargar la espalda. Los talones no "
                "necesitan tocar el suelo. Relajamos la cabeza y el cuello.",
           "On plie les genoux autant qu’il faut. L’important, c’est d’allonger le dos. Les talons n’ont pas besoin "
           "de toucher le sol. Tête et cou détendus."),
          ("R", "Nos quedamos aquí de tres a cinco respiraciones.", "On reste 3 à 5 respirations."),
          ("F", "Si necesitamos descansar, apoyamos las rodillas y volvemos a la postura del niño.",
           "Si on a besoin de se reposer, on pose les genoux et on revient à la posture de l’enfant."),
          ("T", "Ahora vamos a caminar hacia las manos.", "Maintenant on va marcher vers les mains."),
      ], mh=24),
      ]

# =============================================================== 5 FOLD
P += [band(5, "Flexión hacia delante relajada · subir a la montaña", "0:21 – 0:24"),
      strip([("downdog", "Perro", None), ("downdog_walk", "Caminamos hacia delante", None),
             ("fold", "Flexión relajada", "4–5 resp."), ("roll_up", "Subimos despacio", "inh"),
             ("tadasana", "Montaña", "3 resp.")], scale=0.19),
      card([("fold", "rodillas dobladas, torso sobre los muslos")], "Flexión relajada", ["4 – 5 respiraciones"], [
          ("D", "Desde el perro boca abajo.", "Depuis le chien tête en bas."),
          ("E", "Doblamos las rodillas, miramos entre las manos y caminamos con pasos pequeños hacia delante.",
           "On plie les genoux, on regarde entre les mains et on marche à petits pas vers l’avant."),
          ("P", "Pies separados a la anchura de las caderas. Doblamos bien las rodillas y dejamos caer el torso sobre "
                "los muslos. Dejamos la cabeza y el cuello completamente relajados. Podemos coger los codos y "
                "balancearnos suavemente de un lado al otro.",
           "Pieds écartés largeur de hanches. On plie bien les genoux, le buste tombe sur les cuisses. Tête et cou "
           "complètement relâchés. On peut attraper les coudes et se balancer doucement d’un côté à l’autre."),
          ("R", "Nos quedamos aquí cuatro o cinco respiraciones.", "On reste 4 ou 5 respirations."),
          ("F", "Si tira detrás de las piernas, doblamos más las rodillas.",
           "Si ça tire derrière les jambes, on plie plus les genoux."),
          ("T", "Soltamos los brazos. Rodillas dobladas, barbilla ligeramente hacia el pecho. Inhalamos y subimos "
                "despacio. La cabeza sube la última.",
           "On lâche les bras. Genoux pliés, menton légèrement vers la poitrine. On inspire et on remonte doucement. "
           "La tête monte en dernier."),
      ], mh=28),
      card([("tadasana", None)], "Montaña", ["3 respiraciones"], [
          ("D", "Estamos de pie.", "On est debout."),
          ("P", "Pies paralelos, separados a la anchura de las caderas. Repartimos el peso entre los dos pies. "
                "Rodillas sueltas, hombros relajados, brazos a los lados. Miramos al frente.",
           "Pieds parallèles, largeur de hanches. Poids réparti sur les deux pieds. Genoux souples, épaules "
           "détendues, bras le long du corps. Regard devant."),
          ("R", "Respiramos aquí tres veces.", "3 respirations."),
          ("F", "Si nos cuesta el equilibrio, separamos un poco más los pies.",
           "Si l’équilibre est difficile, on écarte un peu plus les pieds."),
          ("T", "Juntamos las manos delante del pecho. Empezamos el saludo al sol.",
           "Mains jointes devant la poitrine. On commence la salutation au soleil."),
      ], mh=28),
      ]

# =============================================================== 6 SUN SALUTATION
SUN1 = [
    ("tadasana_heart", "1 · Manos al corazón", "exh"), ("arms_up", "2 · Brazos arriba", "inh"),
    ("fold", "3 · Flexión", "exh"), (("half_lift", "half_lift_thighs"), "4 · Espinillas o muslos", "inh"),
    ("step_back_R_knee", "5 · Pie D atrás, rodilla D al suelo", "exh"),
    ("plank_knees", "6 · Pie I atrás: dos rodillas", "inh"), ("prone", "7 · Bajamos al suelo", "exh"),
    ("cobra", "8 · Cobra suave", "inh"), ("tabletop", "9 · Cuatro apoyos", "inh"),
    ("downdog", "10 · Perro boca abajo", "3 resp."), ("half_lift_thighs", "11 · Caminamos · espalda larga", "inh"),
    ("fold", "12 · Flexión", "exh"), ("arms_up", "13 · Subimos", "inh"), ("tadasana_heart", "14 · Corazón", "exh"),
]
R1 = [
    (1, "**Manos al corazón.** De pie, pies a la anchura de las caderas. Juntamos las palmas delante del pecho. "
        "Exhalamos.",
     "Mains au cœur. Debout, pieds largeur de hanches. Paumes jointes devant la poitrine. On expire."),
    (2, "**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos. Hombros lejos de las orejas. "
        "No arqueamos la espalda. Si molestan los hombros, subimos solo hasta donde es cómodo.",
     "Bras en haut. On inspire, on ouvre les bras sur les côtés et on les monte. Épaules loin des oreilles. On ne "
     "cambre pas. Si les épaules gênent, on monte seulement jusqu’où c’est confortable."),
    (3, "**Flexión.** Exhalamos: doblamos las rodillas y bajamos el pecho hacia los muslos. Las manos van al suelo o "
        "a las piernas. Cabeza relajada.",
     "Flexion. On expire, on plie les genoux, la poitrine descend vers les cuisses. Mains au sol ou sur les jambes. "
     "Tête relâchée."),
    (4, "**Media elevación.** Inhalamos, alargamos la espalda. Apoyamos las manos en las espinillas o en los muslos, "
        "justo por encima de las rodillas. No apoyamos directamente sobre las rodillas. Miramos al suelo.",
     "Demi-flexion. On inspire, on allonge le dos. Mains sur les tibias ou sur les cuisses, juste au-dessus des "
     "genoux. Pas directement sur les genoux. Regard au sol."),
    (5, "**Pie derecho atrás.** Exhalamos: doblamos las rodillas, apoyamos las manos en el suelo, llevamos el pie "
        "derecho atrás y apoyamos la rodilla derecha en el suelo. Rodilla izquierda encima del tobillo izquierdo.",
     "Pied droit derrière. On expire : genoux pliés, mains au sol, le pied droit recule et on pose le genou droit au "
     "sol. Genou gauche au-dessus de la cheville gauche."),
    (6, "**Dos rodillas en el suelo.** Inhalamos. Después llevamos el pie izquierdo atrás y apoyamos también la "
        "rodilla izquierda. Ahora tenemos las dos rodillas en el suelo. Colocamos los hombros encima de las muñecas "
        "y mantenemos el cuerpo largo desde la cabeza hasta las rodillas.",
     "Deux genoux au sol. On inspire. Puis le pied gauche recule et on pose aussi le genou gauche. Les deux genoux "
     "sont au sol. Épaules au-dessus des poignets, corps long de la tête aux genoux."),
    (7, "**Bajamos.** Exhalamos, doblamos los codos cerca del cuerpo y bajamos lentamente hasta tumbarnos boca abajo.",
     "On descend. On expire, coudes pliés près du corps, on descend lentement jusqu’à être allongé sur le ventre."),
    (8, "**Cobra suave.** Inhalamos. Apoyamos los empeines en el suelo. Mantenemos los codos cerca del cuerpo. "
        "Elevamos suavemente el pecho. No necesitamos subir mucho. La pelvis y las piernas se quedan en el suelo. "
        "Hombros lejos de las orejas, cuello largo. Exhalamos y bajamos.",
     "Cobra douce. On inspire. Dessus des pieds au sol. Coudes près du corps. On soulève doucement la poitrine, pas "
     "besoin de monter haut. Bassin et jambes restent au sol. Épaules loin des oreilles, cou long. On expire, on "
     "redescend."),
    (9, "**Cuatro apoyos.** Colocamos las manos debajo de los hombros. Inhalamos: empujamos el suelo y volvemos a "
        "cuatro apoyos. Si queremos descansar, pasamos por la postura del niño.",
     "Quatre pattes. Mains sous les épaules. On inspire, on pousse le sol et on revient à quatre pattes. Pour se "
     "reposer, on passe par la posture de l’enfant."),
    (10, "**Perro boca abajo.** Apoyamos las puntas de los pies. Exhalamos: caderas arriba y atrás. Rodillas dobladas "
         "si lo necesitamos. ((3 respiraciones)) Si hace falta, rodillas al suelo: postura del niño.",
     "Chien tête en bas. Pointe des pieds au sol. On expire : hanches en haut et en arrière. Genoux pliés si besoin. "
     "3 respirations. Si besoin, genoux au sol : posture de l’enfant."),
    (11, "**Caminamos hacia las manos.** Doblamos las rodillas, miramos entre las manos y caminamos hacia delante. "
         "Inhalamos: espalda larga, manos en las espinillas o en los muslos.",
     "On marche vers les mains. Genoux pliés, regard entre les mains, on avance. On inspire : dos long, mains sur "
     "les tibias ou les cuisses."),
    (12, "**Flexión.** Exhalamos: rodillas dobladas, dejamos caer el torso, cabeza relajada.",
     "Flexion. On expire : genoux pliés, le buste tombe, tête relâchée."),
    (13, "**Subimos.** Inhalamos: rodillas dobladas, subimos despacio con la espalda larga y los brazos arriba. "
         "Si nos mareamos, subimos con las manos en las caderas.",
     "On remonte. On inspire : genoux pliés, on remonte doucement dos long, bras en haut. Si ça tourne, on remonte "
     "les mains sur les hanches."),
    (14, "**Manos al corazón.** Exhalamos: manos delante del pecho. Respiramos una vez. ((1 resp.)) "
         "Repetimos con el otro pie.",
     "Mains au cœur. On expire, mains devant la poitrine. Une respiration. On recommence avec l’autre pied."),
]
R2 = [
    (1, "Manos al corazón. Esta vez empezamos con el pie izquierdo.", "Mains au cœur. Cette fois on commence avec le pied gauche."),
    (2, "Inhalamos, brazos arriba.", "On inspire, bras en haut."),
    (3, "Exhalamos, flexión. Rodillas dobladas.", "On expire, flexion. Genoux pliés."),
    (4, "Inhalamos, espalda larga. Manos en las espinillas o en los muslos.", "On inspire, dos long. Mains sur les tibias ou les cuisses."),
    (5, "Exhalamos, pie izquierdo atrás y rodilla izquierda al suelo.", "On expire, pied gauche derrière, genou gauche au sol."),
    (6, "Inhalamos, pie derecho atrás y rodilla derecha al suelo. Hombros encima de las muñecas.",
     "On inspire, pied droit derrière, genou droit au sol. Épaules au-dessus des poignets."),
    (7, "Exhalamos, codos cerca del cuerpo, bajamos al suelo.", "On expire, coudes près du corps, on descend au sol."),
    (8, "Inhalamos, cobra suave. Exhalamos, bajamos.", "On inspire, cobra douce. On expire, on descend."),
    (9, "Inhalamos, cuatro apoyos.", "On inspire, quatre pattes."),
    (10, "Puntas de los pies. Exhalamos, perro boca abajo. ((3 resp.))", "Pointe des pieds. On expire, chien tête en bas. 3 respirations."),
    (11, "Caminamos hacia las manos. Inhalamos, espalda larga.", "On marche vers les mains. On inspire, dos long."),
    (12, "Exhalamos, flexión.", "On expire, flexion."),
    (13, "Inhalamos, subimos, brazos arriba.", "On inspire, on remonte, bras en haut."),
    (14, "Exhalamos, manos al corazón.", "On expire, mains au cœur."),
]
R3 = [
    (1, "Exhalamos… manos al corazón.", "On expire… mains au cœur."),
    (2, "Inhalamos… brazos arriba.", "On inspire… bras en haut."),
    (3, "Exhalamos… flexión.", "On expire… flexion."),
    (4, "Inhalamos… espalda larga.", "On inspire… dos long."),
    (5, "Exhalamos… pie derecho atrás, rodilla al suelo.", "On expire… pied droit derrière, genou au sol."),
    (6, "Inhalamos… pie izquierdo atrás, dos rodillas al suelo.", "On inspire… pied gauche derrière, deux genoux au sol."),
    (7, "Exhalamos… bajamos al suelo.", "On expire… on descend au sol."),
    (8, "Inhalamos… cobra suave.", "On inspire… cobra douce."),
    (9, "Exhalamos… bajamos. Inhalamos… cuatro apoyos.", "On expire… on descend. On inspire… quatre pattes."),
    (10, "Exhalamos… perro boca abajo. Nos quedamos aquí: tres respiraciones. ((→ flow de pie))",
     "On expire… chien tête en bas. On reste ici : 3 respirations. (→ flow debout)"),
]
P += [band(6, "Saludo al sol · Ronda 1: muy despacio · pie derecho", "0:24 – 0:29"), LQD,
      '<div class="cue0">' + segs([("X", "El saludo al sol une todo lo que hemos hecho. La primera vez vamos muy despacio y "
                                         "os explico cada paso.",
                                    "La salutation au soleil relie tout ce qu’on a fait. La première fois on va très "
                                    "lentement et je vous explique chaque étape.")]) + "</div>",
      strip(SUN1[:7], 0.155), strip(SUN1[7:], 0.155), steps(R1),
      band("6b", "Ronda 2: menos palabras · pie izquierdo", "0:29 – 0:31"),
      note("si tu sautes la ronde 3 : à l’étape 10 de la ronde 2, reste en chien tête en bas et enchaîne directement le flow (section 7)."),
      steps(R2, short=True),
      band("6c", "Ronda 3: un movimiento = una respiración · pie derecho", "0:31 – 0:34", opt=True),
      '<div class="cue0">' + segs([("X", "Ahora, un movimiento con cada respiración. Seguid mi voz. Esta vez terminamos en "
                                         "perro boca abajo.",
                                    "Maintenant, un mouvement par respiration. Suivez ma voix. Cette fois on termine en "
                                    "chien tête en bas.")]) + "</div>",
      steps(R3, short=True),
      ]

# =============================================================== 7/8 FLOW
def flow(right):
    k = "R" if right else "L"
    D, O = ("derecho", "izquierdo") if right else ("izquierdo", "derecho")
    Da, Oa = ("derecha", "izquierda") if right else ("izquierda", "derecha")
    fD, fO = ("droit", "gauche") if right else ("gauche", "droit")
    fDa, fOa = ("droite", "gauche") if right else ("gauche", "droite")
    dog = "downdog" if right else "downdog_L"
    L1 = "D" if right else "I"
    L2 = "I" if right else "D"
    frames = [(dog, "Perro boca abajo", None), (f"lunge_{k}", f"Pie {L1} delante", "exh"),
              (f"lunge_rise_{k}", f"Pie {L2} gira · subimos", "inh"), (f"w2_{k}", "Guerrero II", "3 resp."),
              (f"rev_{k}", "Guerrero inverso", "3 resp."), (f"sa_{k}", "Ángulo lateral", "3 resp."),
              (f"w2_{k}", "Guerrero II", "inh"), (f"lunge_{k}", "Manos al suelo", "exh"),
              (dog, f"Pie {L1} atrás · perro", "3 resp.")]
    st = [
        (1, f"**Perro boca abajo.** {'Empezamos desde aquí.' if right else 'Mismo camino con la pierna izquierda.'} "
            "Inhalamos y miramos entre las manos.",
         f"Chien tête en bas. {'On part d’ici.' if right else 'Même chemin avec la jambe gauche.'} On inspire, regard "
         "entre les mains."),
        (2, f"**Pie {D} delante.** Exhalamos: llevamos el pie {D} entre las manos. Rodilla {Da} encima del tobillo. "
            f"Si el pie no llega, apoyamos la rodilla {Oa} en el suelo y ayudamos al pie con la mano {Da}.",
         f"Pied {fD} devant. On expire : le pied {fD} entre les mains. Genou {fD} au-dessus de la cheville. Si le pied "
         f"n’arrive pas, on pose le genou {fO} au sol et on aide le pied avec la main {fDa}."),
        (3, f"**Pie de atrás y subimos.** Giramos el pie {O} hacia fuera y apoyamos todo el pie; los dedos miran hacia "
            "el lado largo de la esterilla. Inhalamos: subimos el torso, manos en las caderas. Si perdemos el "
            "equilibrio, separamos un poco más los pies hacia los lados.",
         f"Pied arrière, on se redresse. On tourne le pied {fO} vers l’extérieur et on pose tout le pied ; les orteils "
         "regardent le grand côté du tapis. On inspire : le buste se redresse, mains sur les hanches. Si on perd "
         "l’équilibre, on écarte un peu plus les pieds sur les côtés."),
        (4, f"**Guerrero II.** Exhalamos: brazos en cruz, a la altura de los hombros; brazo {D} delante, brazo {O} "
            "atrás. Pecho y caderas miran hacia el lado largo de la esterilla. "
            f"Rodilla {Da} encima del tobillo y en la dirección del segundo dedo del pie: que no caiga hacia dentro. "
            f"Pierna {Oa} estirada y fuerte. Miramos por encima de la mano {Da}. ((3 resp.)) "
            "Si hace falta, acortamos la distancia entre los pies o doblamos menos la rodilla. "
            "Si se cansan los brazos, manos en las caderas.",
         f"Guerrier II. On expire : bras en croix à hauteur d’épaules ; bras {fD} devant, bras {fO} derrière. "
         f"Poitrine et hanches vers le grand côté du tapis. Genou {fD} au-dessus de la cheville, dans la direction du "
         f"deuxième orteil : il ne tombe pas vers l’intérieur. Jambe {fO} tendue et forte. Regard au-dessus de la main "
         f"{fDa}. 3 respirations. Si besoin, on rapproche les pieds ou on plie moins le genou. Bras fatigués : mains "
         "sur les hanches."),
        (5, f"**Guerrero inverso.** Mantenemos la rodilla {Da} doblada. Bajamos la mano {Oa} y la apoyamos muy ligera "
            f"sobre la pierna {Oa}: sin peso. Inhalamos: brazo {D} arriba y un poco atrás. Alargamos el costado {D}. "
            "((3 resp.)) Si hace falta, nos inclinamos menos y miramos al frente.",
         f"Guerrier inversé. Le genou {fD} reste plié. La main {fOa} descend et se pose très légèrement sur la jambe "
         f"{fOa} : sans poids. On inspire : bras {fD} en haut et un peu en arrière. On allonge le flanc {fD}. "
         "3 respirations. Si besoin, on se penche moins et on regarde devant."),
        (6, f"**Ángulo lateral.** Inhalamos, volvemos al centro. Exhalamos: nos inclinamos hacia delante y apoyamos el "
            f"antebrazo {D} sobre el muslo {D}. Brazo {O} hacia arriba o por encima de la oreja. Pecho abierto. "
            f"((3 resp.)) Si hace falta, mano {Oa} en la cadera.",
         f"Angle latéral. On inspire, retour au centre. On expire : on se penche vers l’avant et on pose l’avant-bras "
         f"{fD} sur la cuisse {fDa}. Bras {fO} vers le haut ou au-dessus de l’oreille. Poitrine ouverte. "
         f"3 respirations. Si besoin, main {fOa} sur la hanche."),
        (7, f"**Guerrero II.** Inhalamos: empujamos con el pie {O}, subimos al centro, brazos en cruz. ((1 resp.))",
         f"Guerrier II. On inspire : on pousse sur le pied {fO}, on remonte au centre, bras en croix."),
        (8, f"**Manos al suelo.** Exhalamos: giramos el torso hacia la pierna {Da} y apoyamos las manos en el suelo, a "
            f"cada lado del pie {D}. Levantamos el talón {O}. Si hace falta, rodilla {Oa} al suelo.",
         f"Mains au sol. On expire : le buste tourne vers la jambe {fDa}, mains au sol de chaque côté du pied {fD}. "
         f"Talon {fO} levé. Si besoin, genou {fO} au sol."),
        (9, f"**Pie {D} atrás · perro boca abajo.** Exhalamos: llevamos el pie {D} atrás, al lado del {O}, y subimos "
            "las caderas. ((3 resp.)) Si hace falta, rodillas al suelo: postura del niño. " +
            ("Ahora, el mismo camino con la pierna izquierda." if right else
             "Doblamos las rodillas y caminamos hacia las manos. Soltamos los brazos. Inhalamos y subimos despacio; "
             "la cabeza sube la última. Estamos de pie, en montaña."),
         f"Pied {fD} derrière, chien tête en bas. On expire : le pied {fD} recule à côté du {fO}, hanches en haut. "
         "3 respirations. Si besoin, genoux au sol : enfant. " +
         ("Maintenant, même chemin avec la jambe gauche." if right else
          "On plie les genoux et on marche vers les mains. On lâche les bras. On inspire et on remonte doucement, la "
          "tête en dernier. Debout, en montagne.")),
    ]
    return strip(frames[:5], 0.17) + strip(frames[4:], 0.17) + (steps(st) if right else steps(FLOW_L, short=True))



FLOW_L = [
    (1, "**Perro boca abajo.** Mismo camino con la pierna izquierda. Inhalamos, miramos entre las manos.",
     "Chien tête en bas. Même chemin jambe gauche. On inspire, regard entre les mains."),
    (2, "Exhalamos: **pie izquierdo** entre las manos, rodilla izquierda encima del tobillo. Si no llega: rodilla derecha al suelo y ayudamos con la mano izquierda.",
     "On expire : pied gauche entre les mains, genou au-dessus de la cheville. Sinon : genou droit au sol, on aide avec la main gauche."),
    (3, "Giramos el pie derecho hacia fuera y apoyamos todo el pie. Inhalamos: subimos, manos en las caderas.",
     "On tourne le pied droit vers l’extérieur, tout le pied au sol. On inspire : on se redresse, mains sur les hanches."),
    (4, "Exhalamos: **Guerrero II**, brazo izquierdo delante. Rodilla izquierda encima del tobillo, hacia el segundo dedo. Miramos la mano izquierda. ((3 resp.)) Si hace falta, pies más cerca.",
     "On expire : Guerrier II, bras gauche devant. Genou gauche au-dessus de la cheville, vers le 2e orteil. Regard main gauche. 3 resp. Si besoin, pieds plus proches."),
    (5, "**Guerrero inverso:** mano derecha muy ligera sobre la pierna derecha. Inhalamos: brazo izquierdo arriba y un poco atrás. ((3 resp.))",
     "Guerrier inversé : main droite très légère sur la jambe droite. On inspire : bras gauche en haut et un peu en arrière. 3 resp."),
    (6, "Inhalamos, al centro. Exhalamos: **ángulo lateral**, antebrazo izquierdo sobre el muslo izquierdo, brazo derecho arriba. ((3 resp.)) Si hace falta, mano derecha en la cadera.",
     "On inspire, au centre. On expire : angle latéral, avant-bras gauche sur la cuisse gauche, bras droit en haut. 3 resp. Sinon main droite sur la hanche."),
    (7, "Inhalamos: empujamos con el pie derecho y subimos: **Guerrero II**.", "On inspire : on pousse sur le pied droit, on remonte : Guerrier II."),
    (8, "Exhalamos: manos al suelo a cada lado del pie izquierdo. Talón derecho arriba.", "On expire : mains au sol de chaque côté du pied gauche. Talon droit levé."),
    (9, "Exhalamos: pie izquierdo atrás, **perro boca abajo**. ((3 resp.)) Doblamos las rodillas y caminamos hacia las manos. Soltamos los brazos. Inhalamos y subimos despacio; la cabeza sube la última. Estamos en montaña.",
     "On expire : pied gauche derrière, chien tête en bas. 3 resp. Genoux pliés, on marche vers les mains. On lâche les bras. On inspire, on remonte doucement, la tête en dernier. Montagne."),
]
P += [band(7, "Flow de pie · lado derecho", "0:34 – 0:39"), LQD,
      note("face aux élèves, montre avec ta jambe <b>gauche</b> quand tu dis <b class='sr'>derecha</b> (miroir)."),
      flow(True),
      band(8, "Flow de pie · lado izquierdo", "0:39 – 0:44"), flow(False)]

# =============================================================== 9 TREE
P += [band(9, "Árbol", "0:44 – 0:47", opt=True),
      card([("tree_R_easy", "dedos en el suelo"), ("tree_R", "pie en la pantorrilla")], "Árbol", ["3 resp. por lado"], [
          ("D", "De pie, en montaña.", "Debout, en montagne."),
          ("E", "Miramos un punto fijo delante. Llevamos el peso al pie izquierdo.",
           "On regarde un point fixe devant. Le poids va sur le pied gauche."),
          ("P", "Podemos dejar los dedos del pie derecho en el suelo y apoyar el talón en el tobillo. O subimos el pie "
                "a la pantorrilla: **nunca directamente sobre la rodilla.** Rodilla derecha hacia fuera, manos delante "
                "del pecho.",
           "On peut laisser les orteils du pied droit au sol et poser le talon sur la cheville. Ou on monte le pied "
           "sur le mollet : jamais directement sur le genou. Genou droit vers l’extérieur, mains devant la poitrine."),
          ("R", "Respiramos tres veces. ((3 resp.)) Bajamos el pie y cambiamos de lado: peso al pie derecho. ((3 resp.))",
           "3 respirations. On repose le pied et on change de côté : poids sur le pied droit."),
          ("F", "Si hace falta, apoyamos una mano en la pared. Si perdemos el equilibrio, no pasa nada.",
           "Si besoin, une main contre le mur. Si on perd l’équilibre, ce n’est pas grave."),
          ("T", "Bajamos el pie. Doblamos las rodillas, apoyamos las manos en el suelo y nos sentamos despacio.",
           "On repose le pied. On plie les genoux, mains au sol, et on s’assoit doucement."),
      ], mh=30)]

# =============================================================== 10 SEATED
P += [band(10, "Sentados · mariposa y flexión suave", "0:47 – 0:53"),
      card([("butterfly", None)], "Mariposa", ["3 – 4 respiraciones"], [
          ("D", "Sentados en el centro de la esterilla.", "Assis au centre du tapis."),
          ("E", "Juntamos las plantas de los pies y dejamos caer las rodillas hacia los lados. Alejamos un poco los "
                "pies si necesitamos más espacio.",
           "On joint les plantes des pieds et on laisse tomber les genoux sur les côtés. On éloigne un peu les pieds "
           "si on a besoin de place."),
          ("P", "Inhalamos, alargamos la espalda. Exhalamos y nos inclinamos un poco hacia delante, sin forzar.",
           "On inspire, on allonge le dos. On expire, on se penche un peu vers l’avant, sans forcer."),
          ("R", "Respiramos aquí tres o cuatro veces.", "3 ou 4 respirations."),
          ("F", "No empujamos las rodillas hacia el suelo.", "On ne pousse pas les genoux vers le sol."),
          ("T", "Inhalamos y subimos. Estiramos las piernas delante.", "On inspire, on se redresse. On allonge les jambes devant."),
      ], mh=24),
      card([("seated_fold", None)], "Flexión sentada suave", ["4 – 5 respiraciones"], [
          ("D", "Sentados, piernas delante.", "Assis, jambes devant."),
          ("E", "Estiramos las piernas delante, pero mantenemos las rodillas dobladas.",
           "On allonge les jambes devant, mais on garde les genoux pliés."),
          ("P", "Inhalamos y alargamos la espalda. Exhalamos y llevamos el pecho un poco hacia delante. Las manos pueden "
                "quedarse sobre los muslos o las piernas. No necesitamos tocar los pies. Relajamos el cuello.",
           "On inspire, on allonge le dos. On expire, la poitrine va un peu vers l’avant. Les mains restent sur les "
           "cuisses ou les jambes. Pas besoin de toucher les pieds. Cou détendu."),
          ("R", "Respiramos aquí cuatro o cinco veces.", "4 ou 5 respirations."),
          ("F", "Si tira demasiado detrás de las piernas, doblamos más las rodillas.",
           "Si ça tire trop derrière les jambes, on plie plus les genoux."),
          ("T", "Inhalamos y volvemos despacio hacia arriba. Apoyamos las manos detrás de nosotros y bajamos "
                "lentamente hasta tumbarnos boca arriba.",
           "On inspire et on revient doucement. Mains derrière nous, on descend lentement jusqu’à être allongé sur "
           "le dos."),
      ], mh=24),
      ]

# =============================================================== 11 LYING
P += [band(11, "Tumbados · rodillas al pecho · limpiaparabrisas · torsión", "0:53 – 0:56"),
      card([("knees_chest", None)], "Rodillas al pecho", ["3 respiraciones"], [
          ("D", "Tumbados boca arriba.", "Allongés sur le dos."),
          ("E", "Llevamos una rodilla hacia el pecho y después la otra.", "Un genou vers la poitrine, puis l’autre."),
          ("P", "Abrazamos suavemente las piernas. Relajamos los hombros.", "On serre doucement les jambes. Épaules détendues."),
          ("R", "Respiramos aquí tres veces.", "3 respirations."),
          ("F", "Si cuesta llegar, cogemos detrás de los muslos.", "Si c’est difficile, on attrape l’arrière des cuisses."),
          ("T", "Volvemos a apoyar los pies en el suelo, un poco separados.", "On repose les pieds au sol, un peu écartés."),
      ], mh=20),
      card([("wipers", "rodillas: derecha ↔ izquierda")], "Limpiaparabrisas", ["4 – 6 veces"], [
          ("D", "Boca arriba, pies en el suelo un poco separados.", "Sur le dos, pieds au sol un peu écartés."),
          ("P", "Dejamos caer lentamente las rodillas hacia la derecha y después hacia la izquierda, como un "
                "limpiaparabrisas.",
           "On laisse tomber lentement les genoux à droite puis à gauche, comme un essuie-glace."),
          ("R", "Exhalamos al bajar las rodillas, inhalamos al volver al centro.",
           "On expire quand les genoux descendent, on inspire en revenant au centre."),
          ("F", "Movemos suavemente, sin forzar. Movimiento pequeño si molesta la espalda.",
           "Doucement, sans forcer. Petit mouvement si le dos gêne."),
          ("T", "Juntamos las rodillas y abrimos los brazos en cruz.", "On rapproche les genoux et on ouvre les bras en croix."),
      ], mh=20),
      card([("twist_R", "visto desde arriba · rodillas a la derecha")], "Torsión tumbados", ["3 resp. por lado"], [
          ("D", "Boca arriba, rodillas juntas, brazos en cruz.", "Sur le dos, genoux serrés, bras en croix."),
          ("P", "Exhalamos y dejamos caer las rodillas hacia la derecha. Miramos hacia la izquierda si es cómodo. "
                "Los hombros se quedan en el suelo.",
           "On expire, les genoux tombent à droite. Regard vers la gauche si c’est confortable. Les épaules restent au sol."),
          ("R", "Respiramos tres veces. ((3 resp.)) Inhalamos y volvemos al centro. Cambiamos de lado: exhalamos, "
                "rodillas hacia la izquierda, miramos hacia la derecha. ((3 resp.))",
           "3 respirations. On inspire, retour au centre. On change : on expire, genoux à gauche, regard à droite."),
          ("F", "Bajamos las rodillas solo un poco.", "On descend les genoux juste un peu."),
          ("T", "Inhalamos, volvemos al centro. Estiramos las piernas.", "On inspire, retour au centre. On allonge les jambes."),
      ], mh=26),
      ]

# =============================================================== 12 SAVASANA
P += [band(12, "Savasana y cierre · 4–5 minutos mínimo", "0:56 – 1:01"),
      note("<b>ne jamais raccourcir Savasana</b> : si tu es en retard, c’est la ronde 3 ou l’arbre qu’on saute."),
      card([("savasana", "visto desde arriba")], "Savasana", ["4 – 5 min de silencio"], [
          ("E", "Nos tumbamos boca arriba.", "On s’allonge sur le dos."),
          ("P", "Dejamos las piernas relajadas y los pies sueltos. Brazos un poco separados, palmas hacia arriba. "
                "Cerramos los ojos si queremos.",
           "Jambes détendues, pieds relâchés. Bras un peu écartés, paumes vers le haut. On ferme les yeux si on veut."),
          ("F", "Si es más cómodo, podemos mantener las rodillas dobladas y los pies en el suelo.",
           "Si c’est plus confortable, on peut garder les genoux pliés et les pieds au sol."),
          ("Z", "Relajamos los pies… las piernas… el abdomen… el pecho… los hombros… los brazos… las manos… "
                "la mandíbula, los ojos, toda la cara. Dejamos que la respiración sea natural. No hay nada que hacer. "
                "Solo descansar. ((4–5 minutos de silencio))",
           "On relâche les pieds… les jambes… le ventre… la poitrine… les épaules… les bras… les mains… la mâchoire, "
           "les yeux, tout le visage. La respiration devient naturelle. Rien à faire. Juste se reposer."),
          ("T", "Respiramos un poco más profundo. Movemos los dedos de las manos y de los pies. Doblamos las rodillas y "
                "giramos hacia el lado derecho. Nos quedamos ahí un momento. Cuando queráis, empujamos el suelo con la "
                "mano y nos sentamos despacio; la cabeza sube la última.",
           "On respire un peu plus profondément. On bouge les doigts et les orteils. On plie les genoux et on roule "
           "sur le côté droit. On reste un moment. Quand vous voulez, on pousse le sol avec la main et on s’assoit "
           "doucement ; la tête monte en dernier."),
      ], mh=22),
      card([("seated_cross", None)], "Cierre", [], [
          ("X", "Juntamos las manos delante del pecho. Observamos cómo nos sentimos ahora, sin juzgar. "
                "Gracias por practicar conmigo. Namasté.",
           "Mains jointes devant la poitrine. On observe comment on se sent maintenant, sans juger. Merci d’avoir "
           "pratiqué avec moi. Namasté."),
      ], mh=22),
      ]

# =============================================================== CSS / OUTPUT
CSS = B.CSS + """
@page { margin: 9mm 10mm 10mm 10mm; @top-right { content: "Yoga principiantes · guion"; font-size: 8pt; }
  @bottom-center { content: "Página " counter(page) " / " counter(pages); font-size: 8.5pt; } }
body { font-size: 10.3pt; line-height: 1.24; }
.top { display:flex; justify-content:space-between; align-items:flex-end; gap:4mm; border-bottom:2px solid var(--band); padding-bottom:1.2mm; }
.top h1 { margin:0; font-size:20pt; color:var(--band); line-height:1.05; }
.kick { font-size:8.5pt; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }
.leg { font-size:9pt; text-align:right; line-height:1.55; }
.note { font-size:8.8pt; color:#6b5a2a; background:#f6f3ea; border-left:3px solid #c9b88a; padding:1mm 2.5mm; margin:1.5mm 0; }
.band { display:flex; align-items:center; gap:2.5mm; background:var(--band); color:#fff; border-radius:2mm;
        padding:1mm 3mm; margin:3mm 0 1.2mm; font-size:12.5pt; break-after:avoid; }
.band .secn { background:#fff; color:var(--band); border-radius:3mm; min-width:6.5mm; padding:0 1.2mm; text-align:center; font-weight:700; font-size:10pt; }
.band b { flex:1; } .band .time { font-weight:700; }
.band .sr, .band .sl { color:#fff; text-decoration: underline; text-decoration-thickness: 2px; }
.band .opt { background:#fff3; border:1px solid #fff9; border-radius:2mm; padding:0 2mm; font-size:9pt; }
.lqd { font-size:9pt; font-weight:700; letter-spacing:.12em; color:var(--band); margin:0 0 1mm; }
.lqd span { font-weight:400; letter-spacing:0; color:var(--muted); }
.card { display:grid; grid-template-columns: 40mm 1fr; gap:2.5mm; border-bottom:1px solid var(--line);
        padding:1.2mm 0; break-inside:avoid; }
.cfig { background:#f5f7f9; border-radius:2mm; padding:1.2mm; text-align:center; }
.cname { font-weight:700; font-size:11.5pt; line-height:1.15; margin-bottom:1mm; text-align:left; }
.cf { margin:.6mm 0; } .cf svg { display:block; margin:0 auto; }
.fcap { font-size:8.5pt; color:var(--muted); line-height:1.15; }
.badges { display:flex; flex-wrap:wrap; gap:1mm; justify-content:center; margin-top:.8mm; }
.badge { font-size:9pt; }
.es { font-size:10.3pt; line-height:1.26; }
.seg { }
.tg { display:inline-block; font-size:7pt; font-weight:700; letter-spacing:.04em; border-radius:1.2mm;
      padding:0 1.2mm; margin-right:1.2mm; vertical-align:1.5px; line-height:1.45; }
.t-d { background:#ece7f7; color:#4a3a86; } .t-e { background:#e3ecf8; color:#234b86; }
.t-p { background:#e3ecf8; color:#234b86; } .t-r { background:#fff0b3; color:#6b5500; }
.t-f { background:#dff3e6; color:#1f6b3d; } .t-t { background:var(--band); color:#fff; }
.t-x { background:#eceff3; color:#3a4552; }
.fr { font-size:8.2pt; line-height:1.2; color:#7a8290; font-style:italic; margin-top:1mm;
      border-left:2px dotted #b8bec8; padding-left:2mm; }
.frl { font-style:normal; font-weight:700; font-size:6.8pt; color:#fff; background:#a3aab5; border-radius:1mm;
       padding:0 1mm; margin-right:1.5mm; vertical-align:1px; }
.ftg { font-style:normal; font-size:6.8pt; font-weight:700; color:#9aa2ad; text-transform:uppercase; margin:0 1mm 0 1.5mm; }
.fr .inh, .fr .exh { background:none; font-weight:400; } .fr .sr, .fr .sl { font-weight:400; color:inherit; }
.cue0 { margin:0 0 1mm; }
.fri { display:inline; border:0; padding:0; margin:0; }
.fri::before { content:'— '; font-style:normal; }
.strip { display:flex; align-items:flex-end; justify-content:space-between; gap:.8mm; background:#f5f7f9;
         border-radius:2mm; padding:1.5mm 2mm; margin:1.2mm 0; break-inside:avoid; }
.sf { display:flex; flex-direction:column; align-items:center; text-align:center; min-width:0; }
.sfig { display:flex; align-items:flex-end; gap:1mm; } .sfig svg { display:block; }
.sor { font-size:9pt; font-weight:700; color:var(--muted); align-self:center; }
.scap { font-size:8.4pt; font-weight:700; line-height:1.15; margin-top:.8mm; max-width:30mm; }
.sb { font-size:8pt; font-weight:700; border-radius:1.2mm; padding:0 1.2mm; margin-top:.5mm; white-space:nowrap; }
.sb.inh { background:var(--inh-bg); } .sb.exh { background:var(--exh-bg); } .sb.n { background:#e6eaef; }
.sb i { font-style:normal; font-size:.75em; }
.sarrow { font-size:13pt; color:var(--band); font-weight:700; align-self:center; padding-bottom:5mm; }
.keep { break-inside: avoid; }
ol.steps { list-style:none; margin:1mm 0; padding:0; }
ol.steps li { display:flex; gap:2mm; padding:1mm 0; border-bottom:1px solid #eef0f3; break-inside:avoid; }
ol.steps.short { columns:2; column-gap:5mm; }
ol.steps.short li { border-bottom:0; padding:.6mm 0; }
.nn { flex:0 0 6mm; height:6mm; border-radius:3mm; background:var(--ink); color:#fff; font-weight:700; font-size:9pt;
      display:inline-flex; align-items:center; justify-content:center; margin-top:.3mm; }
"""
def glue(parts):
    out, i = [], 0
    while i < len(parts):
        x = parts[i]
        if x.startswith('<div class="band"'):
            grp = [x]
            i += 1
            while i < len(parts) and (parts[i].startswith('<div class="lqd"') or parts[i].startswith('<div class="note"')
                                      or parts[i].startswith('<div class="cue0"')):
                grp.append(parts[i]); i += 1
            if i < len(parts):
                grp.append(parts[i]); i += 1
            out.append('<div class="keep">' + "".join(grp) + "</div>")
        else:
            out.append(x); i += 1
    return out


P = glue(P)
doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Yoga · guion v2</title>'
       f'<style>{CSS}</style></head><body>{"".join(P)}</body></html>')
out = B.ROOT / "build" / "yoga_guion_v2.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
