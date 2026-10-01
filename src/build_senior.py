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
          "[S]": ("vs", "SIN APOYO", "SANS APPUI")}
    for k, (c, les, lfr) in VB.items():
        h = h.replace(k, f'<span class="vb {c}"><span class="vl">{les if L == "es" else lfr}</span>')
    for k in ("[/C]", "[/CP]", "[/S]"):
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
# CONTENT · class for older beginners: 3 parts
#   1 seated (floor or chair) · 2 standing with chair or wall · 3 floor or chair
# ===================================================================


def part(n, es_t, fr_t):
    return (f'<div class="part"><span>{"PARTE" if L == "es" else "PARTIE"} {n}</span>'
            f'{es_t if L == "es" else fr_t}</div>')


# =================================================================== PAGE 1
p1 = [
    '<div class="top"><div><div class="kick">' +
    ("Guion de la profesora · 1 hora · principiantes mayores · se lee en voz alta" if L == "es"
     else "Version française du guion · même ordre et mêmes numéros que la version espagnole") +
    '</div><h1>' + ("Yoga suave para principiantes" if L == "es" else "Yoga doux pour débutants") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="inh"><i>▲</i>Inhalamos</span> <span class="exh"><i>▼</i>Exhalamos</span>'
     if L == "es" else '<span class="inh"><i>▲</i>On inspire</span> <span class="exh"><i>▼</i>On expire</span>') +
    ' · <span class="pause">' + ("gris = pausa" if L == "es" else "gris = pause") + '</span></div></div>',
    note("avant le cours, place les 4–5 chaises <b>contre le mur</b>, dossier vers la salle : ceux qui n’ont pas de "
         "chaise utiliseront le mur. ≈ 60 min. En retard : saute la ronde 3 ou l’arbre, <b>jamais la relaxation</b>. "
         "En avance : section 12."),
    part(1, "Sentados · en el suelo o en una silla · 0:00 – 0:18", "Assis · au sol ou sur une chaise · 0:00 – 0:18"),
    band(1, ("Bienvenida · cómo sentarnos", "Accueil · comment s’asseoir"), "0:00 – 0:05"),
    grid([
        card(["seated_cross", "chair_sit"], ("En el suelo o en la silla", "Au sol ou sur une chaise"), None, (
            "Hola a todos, bienvenidos. Me llamo ___. Es una clase suave para principiantes: vamos despacio. **Es mi primera clase en español:** si algo no está claro o no lo pronuncio bien, no dudéis en preguntarme. Para empezar, cada uno elige. En el suelo: piernas cruzadas, o piernas estiradas con las rodillas un poco dobladas. [C]Pies bien apoyados en el suelo, espalda separada del respaldo.[/C] Manos sobre los muslos, espalda larga, hombros relajados. Podéis cambiar de posición cuando queráis.",
            'Bonjour à tous, bienvenue. Je m’appelle ___. C’est un cours doux pour débutants : on va doucement. **C’est mon premier cours en espagnol :** si quelque chose n’est pas clair ou si je prononce mal, n’hésitez pas à me demander. Pour commencer, chacun choisit. Au sol : jambes croisées, ou jambes allongées, genoux un peu pliés. [C]Pieds bien posés au sol, dos décollé du dossier.[/C] Mains sur les cuisses, dos long, épaules détendues. Vous pouvez changer de position quand vous voulez.'), mh=13, row=True),
        card(["chair_sit"], ("Qué vamos a hacer", "Ce qu’on va faire"), None, (
            "Hoy vamos a intentar coordinar el movimiento con la respiración. Muchas veces inhalaremos para crecer o "
            "abrir el cuerpo, y exhalaremos para bajar o entrar suavemente en una postura. Primero sentados, después "
            "de pie con la ayuda de una silla o de la pared, y al final otra vez sentados o tumbados. No buscamos una "
            "postura perfecta. **Nada debe doler.** Si algo no se siente bien, paramos y descansamos sentados.",
            "Aujourd’hui on va essayer de coordonner le mouvement et la respiration. Souvent on inspirera pour grandir "
            "ou ouvrir le corps, et on expirera pour descendre ou entrer doucement dans une posture. D’abord assis, "
            "puis debout avec l’aide d’une chaise ou du mur, et à la fin de nouveau assis ou allongés. On ne cherche "
            "pas la posture parfaite. **Rien ne doit faire mal.** Si quelque chose ne va pas, on s’arrête et on se "
            "repose assis."), mh=13),
    ]),
    band(2, ("Respiración", "Respiration"), "0:05 – 0:08"),
    grid([card(["seated_cross"], ("Respiración tranquila", "Respiration tranquille"), RESP(5), (
        "Cerramos los ojos si queréis. Una mano en el abdomen y otra en el pecho. Inhalamos lentamente por la nariz y "
        "dejamos que el abdomen y las costillas se expandan suavemente. Exhalamos y dejamos que vuelvan. Sin forzar. "
        "Inhalamos… dos, tres, cuatro. Exhalamos… dos, tres, cuatro. ((5 respiraciones)) [T] Manos a los muslos, abrimos los ojos despacio.",
        "On ferme les yeux si vous voulez. Une main sur le ventre, l’autre sur la poitrine. On inspire lentement par le "
        "nez et on laisse le ventre et les côtes s’ouvrir doucement. On expire et on les laisse revenir. Sans forcer. "
        "On inspire… deux, trois, quatre. On expire… deux, trois, quatre. ((5 respirations)) [T] Mains sur les cuisses, on ouvre les yeux doucement."))], cols=1),
    band(3, ("Calentamiento sentados", "Échauffement assis"), "0:08 – 0:18"),
    grid([
        card(["seated_neck"], ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), (
            "Espalda larga. Exhalamos: oreja derecha hacia el hombro derecho. ((3 resp.)) Inhalamos, al centro. "
            "Exhalamos: oreja izquierda al hombro izquierdo. ((3 resp.)) Inhalamos, al centro. "
            "[F] Movimiento pequeño, sin tirar con la mano.",
            "Dos long. On expire : oreille droite vers l’épaule droite. ((3 resp.)) On inspire, au centre. On expire : "
            "oreille gauche vers l’épaule gauche. ((3 resp.)) On inspire, au centre. [F] Petit mouvement, sans tirer.")),
        card(["seated_shoulders"], ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), (
            "Inhalamos, subimos los hombros hacia las orejas. Exhalamos, atrás y abajo. Cinco círculos hacia atrás… "
            "cinco hacia delante. [F] Círculos pequeños.",
            "On inspire, épaules vers les oreilles. On expire, en arrière et en bas. Cinq cercles vers l’arrière… cinq "
            "vers l’avant. [F] Petits cercles.")),
        card(["wrists"], ("Muñecas y tobillos", "Poignets et chevilles"), ("5 + 5", "5 + 5"), (
            "Brazos delante: círculos suaves con las muñecas, cinco hacia cada lado. Después levantamos un poco un pie "
            "y hacemos círculos con el tobillo; cambiamos de pie. [F] Codos doblados; el talón puede quedarse en el suelo.",
            "Bras devant : cercles doux avec les poignets, cinq de chaque côté. Puis on soulève un peu un pied et on fait "
            "des cercles avec la cheville ; on change de pied. [F] Coudes pliés ; le talon peut rester au sol.")),
        card(["sidebend_R"], ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), (
            "Mano izquierda en el suelo, a un palmo de la cadera izquierda. [C]Mano izquierda en el borde del asiento, junto a la cadera, o el brazo cuelga al lado de la silla.[/C] Inhalamos, brazo derecho arriba. Exhalamos, nos inclinamos a la izquierda. ((3 resp.)) Al centro y cambiamos de lado: mano derecha abajo, brazo izquierdo arriba. Si hace falta, la mano de arriba en la cintura.",
            'Main gauche au sol, à une main de la hanche gauche. [C]Main gauche sur le bord du siège, près de la hanche, ou le bras pend à côté de la chaise.[/C] On inspire, bras droit en haut. On expire, on se penche à gauche. ((3 resp.)) Au centre et on change de côté : main droite en bas, bras gauche en haut. Si besoin, la main du haut sur la taille.')),
        card(["seated_twist"], ("Torsión sentados", "Torsion assise"), ("2 resp./lado", "2 resp./côté"), (
            "Mano izquierda sobre la rodilla derecha. Mano derecha en el suelo, detrás de nosotros, cerca de la cadera. [C]Mano izquierda por fuera de la rodilla derecha; mano derecha en el respaldo.[/C] Inhalamos, espalda larga. Exhalamos y giramos suavemente hacia la derecha. No forzamos. ((2 resp.)) Al centro y cambiamos: mano derecha sobre la rodilla izquierda, mano izquierda detrás.",
            'Main gauche sur le genou droit. Main droite au sol, derrière nous, près de la hanche. [C]Main gauche à l’extérieur du genou droit ; main droite sur le dossier.[/C] On inspire, dos long. On expire, on tourne doucement vers la droite. On ne force pas. ((2 resp.)) Au centre et on change : main droite sur le genou gauche, main gauche derrière.')),
        card(["chair_cat", "cat"], ("Vaca-gato", "Vache-chat"), ("5 veces", "5 fois"), (
            "Sentados, manos en las rodillas. Inhalamos: abrimos el pecho y miramos un poco arriba. Exhalamos: redondeamos la espalda y miramos al ombligo. ((5 veces)) Si os sentís cómodos de rodillas, podéis hacerlo a cuatro apoyos: manos debajo de los hombros, rodillas debajo de las caderas, el mismo movimiento con la espalda. Movimiento pequeño. [T] Vamos a ponernos de pie.",
            'Assis, mains sur les genoux. On inspire : on ouvre la poitrine, regard un peu en haut. On expire : dos rond, regard vers le nombril. ((5 fois)) Si vous êtes à l’aise à genoux, vous pouvez le faire à quatre pattes : mains sous les épaules, genoux sous les hanches, le même mouvement du dos. Petit mouvement. [T] On va se mettre debout.'), row=True, mh=13),
    ]),
]

# =================================================================== PAGE 2
SAL = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("arms_up_chair", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    (("dog_chair", "half_lift_thighs"), ("3 Espalda larga: con apoyo / sin apoyo", "3 Dos long : avec / sans appui"),
     ("3 resp.", "3 resp.")),
    ("stand_hold", ("4 Volvemos y subimos", "4 On revient, on se redresse"), "inh"),
    ("lunge_chair_R", ("5 Pie D atrás", "5 Pied D arrière"), "exh"),
    ("stand_hold", ("6 Pie D vuelve", "6 Pied D revient"), "inh"),
    ("arms_up_chair", ("7 Brazos arriba", "7 Bras en haut"), "inh"), ("heart_chair", ("8 Corazón", "8 Cœur"), "exh"),
]
R1 = [
    (1, ('**Corazón.** De pie, pies a la anchura de las caderas. [CP]Frente a la silla o a la pared, a un paso largo.[/CP] Palmas juntas delante del pecho. Exhalamos.',
         '**Cœur.** Debout, pieds largeur de hanches. [CP]Face à la chaise ou au mur, à un grand pas.[/CP] Paumes jointes devant la poitrine. On expire.')),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos. Hombros lejos de las orejas. "
         "Solo hasta donde es cómodo.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte. Épaules loin des oreilles. "
         "Seulement jusqu’où c’est confortable.")),
    (3, ('**Espalda larga.** Exhalamos: bajamos los brazos. [CP]Manos en el respaldo o en la pared; caminamos un poco hacia atrás hasta que la espalda queda larga, como una mesa. Brazos largos, rodillas suaves.[/CP][S]Rodillas dobladas, manos en los muslos, espalda larga, miramos al suelo.[/S] ((3 resp.))',
         '**Dos long.** On expire : on baisse les bras. [CP]Mains sur le dossier ou au mur ; on recule un peu jusqu’à avoir le dos long, comme une table. Bras longs, genoux souples.[/CP][S]Genoux pliés, mains sur les cuisses, dos long, regard au sol.[/S] ((3 resp.))')),
    (4, ('**Volvemos y subimos.** Inhalamos y subimos el torso: estamos de pie. [CP]Caminamos hacia el apoyo; las manos siguen en el apoyo.[/CP][S]Manos en las caderas.[/S]',
         '**On revient, on se redresse.** On inspire, le buste remonte : on est debout. [CP]On avance vers l’appui ; les mains restent sur l’appui.[/CP][S]Mains sur les hanches.[/S]')),
    (5, ('**Pie derecho atrás.** Exhalamos: el pie derecho da un paso atrás, talón levantado. Doblamos un poco la rodilla izquierda, encima del tobillo. Espalda recta, manos en las caderas; si hace falta, una mano en el apoyo. ((2 resp.)) Paso pequeño si hace falta.',
         '**Pied droit derrière.** On expire : le pied droit recule d’un pas, talon levé. On plie un peu le genou gauche, au-dessus de la cheville. Dos vertical, mains sur les hanches ; si besoin, une main sur l’appui. ((2 resp.)) Petit pas si besoin.')),
    (6, ("**Volvemos.** Inhalamos: el pie derecho vuelve al lado del izquierdo.",
         "**On revient.** On inspire : le pied droit revient à côté du gauche.")),
    (7, ("**Brazos arriba.** Exhalamos, soltamos las manos. Inhalamos, brazos arriba.",
         "**Bras en haut.** On expire, on lâche les mains. On inspire, bras en haut.")),
    (8, ("**Corazón.** Exhalamos, manos delante del pecho. ((1 resp.))",
         "**Cœur.** On expire, mains devant la poitrine. ((1 resp.))")),
]
R2 = [
    (1, ("Corazón. Esta vez con el pie izquierdo.", "Cœur. Cette fois avec le pied gauche.")),
    (2, ("Inhalamos, brazos arriba.", "On inspire, bras en haut.")),
    (3, ("Exhalamos, manos al apoyo, atrás: espalda larga. ((3 resp.))", "On expire, mains sur l’appui, on recule : dos long. ((3 resp.))")),
    (4, ("Volvemos. Inhalamos, subimos.", "On revient. On inspire, on se redresse.")),
    (5, ("Exhalamos, pie izquierdo atrás. ((2 resp.))", "On expire, pied gauche derrière. ((2 resp.))")),
    (6, ("Inhalamos, el pie vuelve.", "On inspire, le pied revient.")),
    (7, ("Inhalamos, brazos arriba.", "On inspire, bras en haut.")),
    (8, ("Exhalamos, corazón.", "On expire, cœur.")),
]
R3 = [
    (1, ("Exhalamos… corazón.", "On expire… cœur.")), (2, ("Inhalamos… brazos arriba.", "On inspire… bras en haut.")),
    (3, ("Exhalamos… manos al apoyo, espalda larga.", "On expire… mains sur l’appui, dos long.")),
    (4, ("Inhalamos… volvemos y subimos.", "On inspire… on revient, on se redresse.")),
    (5, ("Exhalamos… pie derecho atrás. Inhalamos… vuelve.", "On expire… pied droit derrière. On inspire… il revient.")),
    (6, ("Exhalamos… pie izquierdo atrás. Inhalamos… vuelve.", "On expire… pied gauche derrière. On inspire… il revient.")),
    (7, ("Inhalamos… brazos arriba.", "On inspire… bras en haut.")), (8, ("Exhalamos… corazón.", "On expire… cœur.")),
]
p2 = [
    part(2, "De pie · con una silla o la pared · 0:18 – 0:41", "Debout · avec une chaise ou le mur · 0:18 – 0:41"),
    band(4, ("Levantarnos · montaña", "Se lever · montagne"), "0:18 – 0:20"),
    grid([
        card(["stand_hold"], ("Levantarnos", "Se lever"), None, (
            "Nos levantamos despacio. Desde el suelo: nos giramos de lado y nos levantamos despacio. Cada uno elige: con silla, con la pared o sin apoyo. **La silla está aquí para ayudaros. Podéis apoyar una mano cuando queráis.**",
            'On se lève doucement. Depuis le sol : on se tourne sur le côté et on se lève doucement. Chacun choisit : avec chaise, avec le mur ou sans appui. **La chaise est là pour vous aider. Vous pouvez poser une main quand vous voulez.**')),
        card(["tadasana"], ("Montaña", "Montagne"), RESP(3), (
            "Pies a la anchura de las caderas, peso repartido. Rodillas sueltas, hombros relajados, brazos a los lados. "
            "Miramos al frente. ((3 resp.)) Si hace falta, una mano en el apoyo. [T] Manos al pecho.",
            "Pieds largeur de hanches, poids réparti. Genoux souples, épaules détendues, bras le long du corps. Regard "
            "devant. ((3 resp.)) Si besoin, une main sur l’appui. [T] Mains à la poitrine.")),
    ]),
    band(5, ("Saludo con apoyo · Ronda 1: muy despacio · pie derecho",
             "Salutation avec appui · Ronde 1 : très lent · pied droit"), "0:20 – 0:24"),
    note("chaise, mur ou sans appui : chacun choisit, les gestes sont les mêmes. Sans appui : mains sur les cuisses "
         "(étape 3) et sur les hanches (étapes 4–5). Personne ne descend au sol ici."),
    strip(SAL, 0.15), steps(R1),
    '<div class="two">'
    '<div class="rnd">' + band("5b", ("Ronda 2 · pie izquierdo", "Ronde 2 · pied gauche"), "0:24 – 0:26") + steps(R2) +
    "</div>"
    '<div class="rnd">' + band("5c", ("Ronda 3 · 1 movimiento = 1 respiración", "Ronde 3 · 1 mouvement = 1 respiration"),
                               "0:26 – 0:28", opt=True) + steps(R3) + "</div></div>",
]

# =================================================================== PAGE 3


def warriors(right):
    k = "R" if right else "L"
    frames = [(f"widec_{k}", ("Pies separados", "Pieds écartés"), "exh"),
              (f"w2c_{k}", ("Guerrero II", "Guerrier II"), RESP(3)), (f"revc_{k}", ("Inverso", "Inversé"), RESP(2)),
              (f"sac_{k}", ("Ángulo lateral", "Angle latéral"), RESP(2)), (f"w2c_{k}", ("Guerrero II", "Guerrier II"), "inh"),
              (f"widec_{k}", ("Pies al centro", "Pieds au centre"), "exh")]
    return strip(frames, 0.135)


WAR_R = [
    (1, ("**Pies separados.** Nos colocamos con la silla o la pared a nuestra derecha, lo bastante cerca "
         "para tocarla sin inclinarnos, mirando al lado largo de la esterilla. La silla está aquí para ayudaros: "
         "podéis apoyar una mano cuando queráis. Exhalamos y separamos bien los pies. Manos en las caderas.",
         "**Pieds écartés.** On se place avec la chaise ou le mur à notre droite, assez près pour le toucher "
         "sans se pencher, face au grand côté du tapis. La chaise est là pour vous aider : vous pouvez poser une main "
         "quand vous voulez. On expire et on écarte bien les pieds. Mains sur les hanches.")),
    (2, ("**Giramos.** El pie derecho gira hacia fuera, hacia la silla; el pie izquierdo, un poco hacia dentro.",
         "**On tourne.** Le pied droit tourne vers l’extérieur, vers la chaise ; le pied gauche un peu vers l’intérieur.")),
    (3, ("**Guerrero II.** Inhalamos: brazos en cruz, o la mano derecha ligera en el respaldo y la mano izquierda en la "
         "cadera. Exhalamos: doblamos la rodilla derecha, encima del tobillo y hacia el segundo dedo del pie: que no "
         "caiga hacia dentro. Pierna izquierda estirada. Miramos al frente o hacia la mano derecha. ((3 resp.)) "
         "[F] Doblamos poco la rodilla; pies más cerca.",
         "**Guerrier II.** On inspire : bras en croix, ou la main droite légère sur le dossier et la main gauche sur la "
         "hanche. On expire : on plie le genou droit, au-dessus de la cheville et vers le 2e orteil : il ne tombe pas "
         "vers l’intérieur. Jambe gauche tendue. Regard devant ou vers la main droite. ((3 resp.)) [F] Genou peu plié ; "
         "pieds plus proches.")),
    (4, ("**Guerrero inverso.** Mano izquierda muy ligera sobre la pierna izquierda, sin peso. Inhalamos: el brazo "
         "derecho sube, solo un poco. ((2 resp.)) Si no nos sentimos estables, nos quedamos en Guerrero II con la mano "
         "en la silla.",
         "**Guerrier inversé.** Main gauche très légère sur la jambe gauche, sans poids. On inspire : le bras droit "
         "monte, juste un peu. ((2 resp.)) Si on ne se sent pas stable, on reste en Guerrier II, main sur la chaise.")),
    (5, ("**Ángulo lateral.** Exhalamos: antebrazo derecho sobre el muslo derecho. Mano izquierda en la cadera, o brazo "
         "arriba. Pecho abierto. La silla sigue al lado si queremos volver a apoyar la mano. ((2 resp.))",
         "**Angle latéral.** On expire : avant-bras droit sur la cuisse droite. Main gauche sur la hanche, ou bras en "
         "haut. Poitrine ouverte. La chaise reste à côté si on veut reposer la main. ((2 resp.))")),
    (6, ("**Guerrero II.** Inhalamos: subimos al centro.", "**Guerrier II.** On inspire : on remonte au centre.")),
    (7, ("**Volvemos.** Exhalamos: estiramos la rodilla, pies al centro, manos en las caderas. Juntamos los pies "
         "caminando: montaña. ((1 resp.)) [T] Nos giramos para tener la silla a la izquierda.",
         "**On revient.** On expire : on tend le genou, pieds au centre, mains sur les hanches. On rapproche les pieds "
         "en marchant : montagne. ((1 resp.)) [T] On se tourne pour avoir la chaise à gauche.")),
]
WAR_L = [
    (1, ("Silla a la izquierda. Exhalamos, separamos los pies.", "Chaise à gauche. On expire, on écarte les pieds.")),
    (2, ("Pie izquierdo hacia fuera, hacia la silla.", "Pied gauche vers l’extérieur, vers la chaise.")),
    (3, ("Inhalamos: brazos en cruz o mano izquierda en el respaldo. Exhalamos, rodilla izquierda doblada. ((3 resp.))",
         "On inspire : bras en croix ou main gauche sur le dossier. On expire, genou gauche plié. ((3 resp.))")),
    (4, ("Mano derecha ligera en la pierna. Inhalamos, el brazo izquierdo sube un poco. ((2 resp.))",
         "Main droite légère sur la jambe. On inspire, le bras gauche monte un peu. ((2 resp.))")),
    (5, ("Exhalamos, antebrazo izquierdo sobre el muslo; mano derecha en la cadera. ((2 resp.))",
         "On expire, avant-bras gauche sur la cuisse ; main droite sur la hanche. ((2 resp.))")),
    (6, ("Inhalamos, al centro.", "On inspire, au centre.")),
    (7, ("Exhalamos, pies juntos: montaña.", "On expire, pieds joints : montagne.")),
]
p3 = [
    band(6, ("Guerreros · lado derecho", "Guerriers · côté droit"), "0:28 – 0:33"),
    note("installation : <b>chaise — jambe droite pliée — bassin — jambe gauche tendue</b>. La chaise ne bouge pas "
         "pendant tout le côté droit ; pour la gauche, ils se retournent. Face à eux, montre en miroir."),
    warriors(True), steps(WAR_R),
    band("6b", ("Guerreros · lado izquierdo", "Guerriers · côté gauche"), "0:33 – 0:38"),
    warriors(False), steps(WAR_L, cols=2),
    band(7, ("Árbol con apoyo", "Arbre avec appui"), "0:38 – 0:41", opt=True),
    grid([card(["tree_wall", "tree_R"], ("Árbol", "Arbre"), ("3 resp./lado", "3 resp./côté"), (
        "De lado junto a la silla o la pared, una mano apoyada. Miramos un punto fijo. Peso al pie izquierdo. Dejamos "
        "los dedos del pie derecho en el suelo y apoyamos el talón en el tobillo. O el pie en la pantorrilla: **nunca "
        "sobre la rodilla.** ((3 resp.)) Bajamos el pie y cambiamos de lado. Si hace falta, las dos manos en el apoyo.",
        "De côté près de la chaise ou du mur, une main en appui. Regard sur un point fixe. Poids sur le pied gauche. "
        "On laisse les orteils du pied droit au sol et on pose le talon sur la cheville. Ou le pied sur le mollet : "
        "**jamais sur le genou.** ((3 resp.)) On repose le pied et on change de côté. Si besoin, les deux mains sur l’appui."),
        mh=17, row=True)], cols=1),
    band(8, ("Volver a sentarnos", "Se rasseoir"), "0:41 – 0:43"),
    grid([card(["chair_sit", "seated_cross"], ("Silla o suelo", "Chaise ou sol"), None, (
            "Cada uno elige otra vez. Al suelo: bajamos despacio, con una mano en la silla o en la pared si hace falta, y nos sentamos de lado. [C]Nos sentamos despacio, pies apoyados.[/C]",
            'Chacun choisit de nouveau. Au sol : on descend doucement, une main sur la chaise ou au mur si besoin, et on s’assoit sur le côté. [C]On s’assoit doucement, pieds posés.[/C]'),
        mh=12, row=True)], cols=1),
]

# =================================================================== PAGE 4
p4 = [
    part(3, "Sentados o tumbados · en el suelo o en la silla · 0:43 – 1:00",
         "Assis ou allongés · au sol ou sur la chaise · 0:43 – 1:00"),
    band(9, ("Caderas y piernas", "Hanches et jambes"), "0:43 – 0:48"),
    grid([
        card(["butterfly"], ("Mariposa", "Papillon"), ("3–4 resp.", "3–4 resp."), (
            "Plantas de los pies juntas, rodillas hacia los lados. [C]Rodillas separadas, pies en el suelo, manos en los muslos.[/C] Inhalamos, espalda larga. Exhalamos, nos inclinamos un poco, sin forzar. No empujamos las rodillas.",
            'Plantes des pieds jointes, genoux sur les côtés. [C]Genoux écartés, pieds au sol, mains sur les cuisses.[/C] On inspire, dos long. On expire, on se penche un peu, sans forcer. On ne pousse pas les genoux.')),
        card(["seated_fold", "chair_hamstring"], ("Estiramiento de piernas", "Étirement des jambes"), ("4–5 resp.", "4–5 resp."), (
            "Piernas delante, rodillas dobladas. [C]Estiramos la pierna derecha, talón en el suelo; después la izquierda.[/C] Inhalamos, espalda larga. Exhalamos, el pecho un poco hacia delante; manos en los muslos. Si tira, doblamos más las rodillas.",
            'Jambes devant, genoux pliés. [C]On allonge la jambe droite, talon au sol ; puis la gauche.[/C] On inspire, dos long. On expire, la poitrine un peu vers l’avant ; mains sur les cuisses. Si ça tire, on plie plus les genoux.'), row=True, mh=12),
    ]),
    band(10, ("Espalda suave", "Dos en douceur"), "0:48 – 0:52"),
    note("au sol : on s’allonge (mains derrière, sur les coudes, puis sur le dos). Version chaise : bloc marron « SILLA »."),
    grid([
        card(["knees_chest", "chair_knee"], ("Rodillas al pecho", "Genoux poitrine"), RESP(3), (
            "Tumbados: una rodilla hacia el pecho y después la otra; abrazamos las piernas. Si hace falta, cogemos detrás del muslo. [C]Abrazamos una rodilla, luego la otra.[/C]",
            'Allongés : un genou vers la poitrine, puis l’autre ; on serre les jambes. Si besoin, on tient l’arrière de la cuisse. [C]On serre un genou, puis l’autre.[/C]'), mh=11),
        card(["wipers"], ("Limpiaparabrisas", "Essuie-glaces"), ("4–6 veces", "4–6 fois"), (
            "Tumbados, pies en el suelo separados: rodillas lentamente a la derecha y a la izquierda. Sin forzar. [C]Torsión sentados, dos respiraciones por lado.[/C]",
            'Allongés, pieds au sol écartés : genoux lentement à droite puis à gauche. Sans forcer. [C]Torsion assise, deux respirations par côté.[/C]')),
        card(["twist_R"], ("Torsión tumbados", "Torsion allongée"), ("3 resp./lado", "3 resp./côté"), (
            "Brazos en cruz. Exhalamos, rodillas a la derecha; miramos a la izquierda si es cómodo. ((3 resp.)) "
            "Inhalamos, al centro, y cambiamos. [F] Rodillas solo un poco.",
            "Bras en croix. On expire, genoux à droite ; regard à gauche si c’est confortable. ((3 resp.)) On inspire, au "
            "centre, et on change. [F] Genoux juste un peu.")),
    ], cols=3),
    band(11, ("Relajación · 4–5 min mínimo · respiración final · cierre", "Relaxation · 4–5 min minimum · respiration finale · clôture"),
         "0:52 – 1:00"),
    grid([
        card(["savasana", "chair_sit"], ("Relajación", "Relaxation"), ("4–5 min", "4–5 min"), (
            "Tumbados boca arriba, piernas relajadas, brazos un poco separados, palmas hacia arriba; si es más cómodo, rodillas dobladas. [C]Espalda apoyada en el respaldo, pies en el suelo, manos en los muslos.[/C] Cerramos los ojos. Relajamos los pies… las piernas… el abdomen… los hombros… la cara. ((4–5 min de silencio)) [T] Movemos los dedos. Desde el suelo: giramos a la derecha y nos sentamos despacio; la cabeza sube la última.",
            'Allongés sur le dos, jambes détendues, bras un peu écartés, paumes vers le haut ; si c’est plus confortable, genoux pliés. [C]Dos appuyé contre le dossier, pieds au sol, mains sur les cuisses.[/C] On ferme les yeux. On relâche les pieds… les jambes… le ventre… les épaules… le visage. ((4–5 min de silence)) [T] On bouge les doigts. Au sol : on roule à droite et on s’assoit doucement ; la tête en dernier.'), mh=10),
        card(["seated_cross"], ("Respiración final y cierre", "Respiration finale et clôture"), ("4 resp.", "4 resp."), (
            "Sentados. Inhalamos por la nariz… dos, tres, cuatro. Exhalamos despacio… dos, tres, cuatro, cinco, seis. "
            "((4 veces)) [F] Exhalamos hasta cuatro. Manos delante del pecho. Observamos cómo nos sentimos, sin juzgar. "
            "Gracias por practicar conmigo. Namasté.",
            "Assis. On inspire par le nez… deux, trois, quatre. On expire lentement… deux, trois, quatre, cinq, six. "
            "((4 fois)) [F] On expire sur quatre. Mains devant la poitrine. On observe comment on se sent, sans juger. "
            "Merci d’avoir pratiqué avec moi. Namasté.")),
    ]),
    band(12, ("Si sobra tiempo · opciones suaves", "S’il reste du temps · options douces"), "+2 – 6 min", opt=True),
    note("A pendant la partie 2 (debout) ; B et C avant la relaxation. Choisis-en une, deux ou trois."),
    grid([
        card(["heel_raise"], ("A · Talones arriba", "A · Talons levés"), ("8 veces", "8 fois"), (
            "De pie, manos en el apoyo. Inhalamos, subimos los talones. Exhalamos, bajamos despacio. "
            "[F] Subimos solo un poco.",
            "Debout, mains sur l’appui. On inspire, on monte sur la pointe des pieds. On expire, on redescend doucement. "
            "[F] On monte juste un peu.")),
        card(["leg_stretch"], ("B · Estiramiento de pierna", "B · Étirement de jambe"), ("5 resp./lado", "5 resp./côté"), (
            "Tumbados, pie izquierdo en el suelo. Subimos la pierna derecha y la cogemos detrás del muslo, rodilla doblada. ((5 resp.)) Cambiamos. [C]Pierna estirada delante, talón en el suelo.[/C]",
            'Allongés, pied gauche au sol. On monte la jambe droite et on la tient derrière la cuisse, genou plié. ((5 resp.)) On change. [C]Jambe allongée devant, talon au sol.[/C]')),
        card(["chair_sit"], ("C · Brazos y respiración", "C · Bras et respiration"), ("5 veces", "5 fois"), (
            "Sentados. Inhalamos, subimos los brazos por los lados. Exhalamos, los bajamos despacio. "
            "[F] Brazos solo hasta los hombros.",
            "Assis. On inspire, on monte les bras sur les côtés. On expire, on les baisse doucement. "
            "[F] Bras seulement jusqu’aux épaules.")),
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
pages = [p1, p2, p3, p4]
body = "".join(f'<div class="pg">{"".join(p)}</div>' for p in pages)
title = "Yoga · guion (ES)" if L == "es" else "Yoga · guion (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_guion_suave_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
