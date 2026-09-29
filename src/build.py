"""Builds the printable A4 teaching script (HTML) for the 60-min beginner class.

python3 build.py  ->  ../build/yoga_clase_principiantes.html
The PDF is printed from that HTML with headless Chromium (see print.js).
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from poses import ALL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "yoga_clase_principiantes.html"


# ------------------------------------------------------------------ helpers
def fig(name, max_w=33, max_h=26, cap=0.2):
    """Figure scaled to fit a box (mm). cap limits the scale so small poses
    are not blown up."""
    f = ALL[name]()
    svg = f.svg(scale=1)
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
    w, h = float(m.group(3)), float(m.group(4))
    s = min(max_w / w, max_h / h, cap)
    svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w * s:.1f}mm" height="{h * s:.1f}mm"', svg, count=1)
    return svg


def fig_fixed(name, scale):
    """Figure at a fixed scale (mm per unit) - used in strips so all
    frames share the same scale."""
    f = ALL[name]()
    svg = f.svg(scale=1)
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
    w, h = float(m.group(3)), float(m.group(4))
    return re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w * scale:.1f}mm" height="{h * scale:.1f}mm"', svg, count=1)


BREATH = re.compile(r"\b(Inhala|inhala|Exhala|exhala)\b")
SIDE = re.compile(r"\b(derech[oa]s?|izquierd[oa]s?)\b")
PAUSE = re.compile(r"\(\(([^)]*)\)\)")


def rich(t):
    """Markup for spoken text:
    Inhala / Exhala -> highlighted, derecha / izquierda -> coloured,
    ((...)) -> grey stage direction (not spoken), **x** -> bold."""
    t = html.escape(t, quote=False)
    t = PAUSE.sub(r'<span class="pause">\1</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

    def br(m):
        w = m.group(1)
        k = "inh" if w.lower().startswith("inh") else "exh"
        arrow = "▲" if k == "inh" else "▼"
        return f'<span class="{k}"><i>{arrow}</i>{w}</span>'

    t = BREATH.sub(br, t)

    def sd(m):
        w = m.group(1)
        k = "sr" if w.lower().startswith("der") else "sl"
        return f'<span class="{k}">{w}</span>'

    t = SIDE.sub(sd, t)
    return t


TAGS = {
    "E": ("ENTRADA", "t-in"),
    "P": ("POSTURA", "t-pos"),
    "M": ("MOVIMIENTO", "t-mov"),
    "R": ("RESPIRA", "t-br"),
    "F": ("MÁS FÁCIL", "t-easy"),
    "S": ("MÁS FUERTE", "t-strong"),
    "T": ("TRANSICIÓN", "t-next"),
    "X": ("EXPLICO", "t-say"),
    "Z": ("RELAJACIÓN", "t-say"),
    "C": ("CIERRE", "t-say"),
}


def cues(items):
    out = []
    for tag, lines in items:
        label, cls = TAGS[tag]
        if isinstance(lines, str):
            lines = [lines]
        body = "<p>" + " ".join(rich(x) for x in lines) + "</p>"
        out.append(f'<div class="cue"><span class="tag {cls}">{label}{" ↓" if tag == "T" else ""}</span>'
                   f'<div class="say">{body}</div></div>')
    return "".join(out)


def badge(text, kind="n"):
    return f'<span class="badge b-{kind}">{text}</span>'


def row(figs, name, badges, items, num=None, last=False):
    """figs: list of (pose, caption or None) ; badges: list of (text, kind)."""
    fhtml = []
    n = len(figs)
    for p, cap in figs:
        mh = 26 if n == 1 else (19 if n == 2 else 15)
        fhtml.append(f'<div class="fc">{fig(p, max_h=mh)}'
                     + (f'<div class="fcap">{rich(cap)}</div>' if cap else "") + "</div>")
    b = "".join(badge(t, k) for t, k in badges)
    numh = f'<span class="stepn">{num}</span>' if num is not None else ""
    down = "" if last else '<div class="down">↓</div>'
    return (f'<tr><td class="figcell"><div class="pname">{numh}{rich(name)}</div>{"".join(fhtml)}'
            f'<div class="badges">{b}</div>{down}</td>'
            f'<td class="saycell">{cues(items)}</td></tr>')


def table(rows):
    return ('<table class="script"><thead><tr><th class="h-fig">POSTURA</th>'
            '<th class="h-say">LO QUE DIGO</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")


def section(num, title, time, body, sub=None, brk=True):
    s = f'<p class="secsub">{rich(sub)}</p>' if sub else ""
    return (f'<section class="sec{" brk" if brk else ""}"><header class="sech"><span class="secn">{num}</span>'
            f'<h2>{rich(title)}</h2><span class="time">{time}</span></header>{s}{body}</section>')


def strip(frames, scale=0.17, title=None):
    """frames: list of (pose, caption, breath) breath in {'inh','exh',None, text}."""
    cells = []
    for i, (p, cap, br) in enumerate(frames):
        if i:
            cells.append('<div class="sarrow">→</div>')
        bb = ""
        if br == "inh":
            bb = '<span class="sb inh"><i>▲</i>Inhala</span>'
        elif br == "exh":
            bb = '<span class="sb exh"><i>▼</i>Exhala</span>'
        elif br:
            bb = f'<span class="sb n">{br}</span>'
        cells.append(f'<div class="sf"><div class="sfig">{fig_fixed(p, scale)}</div>'
                     f'<div class="scap">{rich(cap)}</div>{bb}</div>')
    t = f'<div class="striptitle">{title}</div>' if title else ""
    return f'<div class="strip">{t}<div class="srow">{"".join(cells)}</div></div>'


INH = ("▲ Inhala", "inh")
EXH = ("▼ Exhala", "exh")


def resp(n):
    return (f"{n} respiraciones" if n != 1 else "1 respiración", "n")


# ================================================================ CONTENT
parts = []

# ---------------------------------------------------------------- COVER
timeline = [
    ("0:00", "1", "Bienvenida y cómo sentarse", "seated_cross"),
    ("0:05", "2", "Respiración", "seated_cross"),
    ("0:08", "3", "Calentamiento sentado", "sidebend_R"),
    ("0:12", "4", "Cuatro apoyos · gato-vaca · niño · perro", "cat"),
    ("0:18", "5", "Del perro a la montaña", "roll_up"),
    ("0:20", "6", "Saludo al sol × 3 rondas", "arms_up"),
    ("0:31", "7", "Flow de pie · lado derecho", "w2_R"),
    ("0:37", "8", "Flow de pie · lado izquierdo", "w2_L"),
    ("0:42", "9", "Árbol", "tree_R"),
    ("0:46", "10", "Suelo: mariposa · puente · torsión", "bridge"),
    ("0:53", "11", "Savasana y cierre", "savasana"),
]
tl_rows = "".join(
    f'<tr><td class="tlt">{t}</td><td class="tln">{n}</td><td class="tlf">{fig(p, max_w=22, max_h=13, cap=0.12)}</td>'
    f'<td class="tls">{rich(s)}</td></tr>' for t, n, s, p in timeline)

cover = f'''
<section class="cover">
  <div class="ctitle">
    <div class="kicker">Guion para la profesora · se lee en voz alta</div>
    <h1>Yoga para principiantes</h1>
    <div class="csub">Clase de 60 minutos · en español · todo lo que digo está escrito</div>
  </div>
  <div class="cgrid">
    <div>
      <h3>La clase en 11 partes</h3>
      <table class="tl">{tl_rows}<tr><td class="tlt">1:00</td><td></td><td></td><td class="tls"><b>Fin</b></td></tr></table>
    </div>
    <div>
      <h3>Cómo leer este guion</h3>
      <div class="legend">
        <div class="lg"><span class="sw sw-r"></span><div><b class="sr">Naranja = DERECHA</b> del alumno <span class="lgs">(letra D)</span></div></div>
        <div class="lg"><span class="sw sw-l"></span><div><b class="sl">Azul = IZQUIERDA</b> del alumno <span class="lgs">(letra I)</span></div></div>
        <div class="lg"><span class="sw sw-far"></span><div>Gris claro = brazo o pierna del otro lado (más lejos)</div></div>
        <div class="lg"><span class="inh"><i>▲</i>Inhala</span> <span class="exh"><i>▼</i>Exhala</span></div>
        <div class="lg"><span class="pause">3 respiraciones</span><div>= texto gris: <b>no se lee</b>, es una pausa</div></div>
        <div class="lg"><span class="tag t-next">TRANSICIÓN ↓</span><div>= cómo paso a la postura siguiente</div></div>
        <div class="lg lgfig">{fig("w2_R", max_w=30, max_h=22, cap=0.13)}<div>Figuras de pie <b>vistas de espaldas</b>: la derecha del dibujo es la derecha del alumno.</div></div>
      </div>
      <div class="pourmoi">
        <div class="pmh">Pour moi (à ne pas lire)</div>
        <ul>
          <li>Lis lentement, phrase par phrase. Après chaque phrase : une respiration de silence.</li>
          <li>Si tu démontres face à eux, fais le côté opposé (miroir), mais <b>dis</b> le côté écrit.</li>
          <li>Si tu es en retard : raccourcis la ronde 2, l’arbre ou le pont. Garde 4 min de Savasana.</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="cgrid2">
    <div class="rescue">
      <h3>Frases útiles en cualquier momento</h3>
      <p>{rich("Descansa en la postura del niño cuando quieras.")}</p>
      <p>{rich("Si algo duele, sal de la postura despacio.")}</p>
      <p>{rich("Sin prisa. Respira.")}</p>
      <p>{rich("Dobla las rodillas todo lo que necesites.")}</p>
    </div>
    <div class="gloss">
      <h3>Vocabulario · Vocabulaire</h3>
      <table>
        <tr><td>la esterilla</td><td>le tapis</td><td>la rodilla</td><td>le genou</td></tr>
        <tr><td>inhala / exhala</td><td>inspire / expire</td><td>la cadera</td><td>la hanche</td></tr>
        <tr><td>el suelo</td><td>le sol</td><td>el muslo</td><td>la cuisse</td></tr>
        <tr><td>el techo</td><td>le plafond</td><td>la espinilla</td><td>le tibia</td></tr>
        <tr><td>la palma</td><td>la paume</td><td>la pantorrilla</td><td>le mollet</td></tr>
        <tr><td>el codo</td><td>le coude</td><td>el tobillo</td><td>la cheville</td></tr>
        <tr><td>el hombro</td><td>l’épaule</td><td>el talón</td><td>le talon</td></tr>
      </table>
    </div>
  </div>
</section>'''
parts.append(cover)

# ---------------------------------------------------------------- 1 + 2
s1 = table([
    row([("seated_cross", "Piernas cruzadas"), ("legs_long", "Piernas estiradas"), ("kneeling", "De rodillas")],
        "Sentarse cómodamente", [("todo el tiempo necesario", "n")], [
            ("E", ["Hola a todos y bienvenidos. Me llamo ______.",
                   "Hoy es una clase para principiantes: vamos a ir despacio."]),
            ("P", ["Siéntate en tu esterilla de la forma más cómoda para ti.",
                   "Puedes cruzar las piernas. Si las rodillas quedan más altas que las caderas, siéntate sobre una manta doblada.",
                   "Puedes estirar las piernas hacia delante. Si tira la espalda, dobla un poco las rodillas.",
                   "O puedes sentarte de rodillas, sobre los talones, solo si es cómodo para tus rodillas.",
                   "Apoya las manos sobre los muslos. Alarga la espalda y relaja los hombros."]),
            ("F", "Si en algún momento te molesta la posición, cámbiala. Es tu práctica."),
        ]),
    row([("child", "La postura del niño = descanso")], "Qué es el yoga · las reglas", [], [
        ("X", ["El yoga une el movimiento y la respiración. Cada movimiento va con una inhalación o con una exhalación.",
               "Normalmente, cuando subimos o abrimos el cuerpo, inhalamos. Cuando bajamos o nos doblamos, exhalamos.",
               "Respiramos por la nariz, con calma. Si te pierdes, no pasa nada: respira normal y sigue.",
               "No hace falta hacer una postura perfecta. Cada cuerpo es diferente. La mejor postura es la que puedes hacer respirando con calma.",
               "**Nada debe doler.** Sentir un estiramiento está bien. Sentir dolor, no. Si algo duele, sal de la postura despacio.",
               "En cualquier momento puedes descansar en la **postura del niño**: de rodillas, las caderas hacia los talones, la frente en el suelo. Te la enseño en unos minutos.",
               "Si tienes alguna lesión o estás embarazada, avísame, por favor. Te daré otras opciones."]),
        ("T", "Quédate en tu posición. Vamos a empezar con la respiración."),
    ], last=True),
])
parts.append(section(1, "Bienvenida y cómo sentarse", "0:00 – 0:05", s1, brk=True))

s2 = table([
    row([("seated_cross", None)], "Respiración abdominal", [resp(5)], [
        ("E", "Quédate en tu posición. Cierra los ojos si te apetece, o mira al suelo delante de ti."),
        ("P", ["Espalda larga, hombros relajados, mandíbula suelta.",
               "Pon una mano sobre el abdomen y la otra sobre el pecho."]),
        ("R", ["Inhala por la nariz: el abdomen se hincha, como un globo.",
               "Exhala por la nariz: el abdomen baja despacio.",
               "Seguimos juntos. Inhala… dos, tres, cuatro. Exhala… dos, tres, cuatro.",
               "Cinco respiraciones más, a tu ritmo. ((5 respiraciones en silencio))"]),
        ("F", "Si contar te agobia, no cuentes: solo observa cómo entra y sale el aire."),
        ("T", ["Baja las manos a los muslos. Deja la respiración natural.",
               "Abre los ojos despacio. Seguimos en el suelo para mover el cuello."]),
    ], last=True),
])
parts.append(section(2, "Respiración", "0:05 – 0:08", s2, brk=False))

# ---------------------------------------------------------------- 3 warm-up
s3 = table([
    row([("seated_neck", "Oreja derecha hacia el hombro derecho")], "Cuello", [("3 resp. por lado", "n")], [
        ("E", "Seguimos en la misma posición, con las manos sobre los muslos."),
        ("P", ["Alarga la espalda: imagina un hilo que tira de tu cabeza hacia el techo.",
               "Exhala e inclina la cabeza hacia la derecha: la oreja derecha va hacia el hombro derecho.",
               "El hombro izquierdo baja hacia el suelo. Mira al frente."]),
        ("R", ["Quédate aquí tres respiraciones. Con cada exhalación, relaja un poco más el hombro. ((3 respiraciones))",
               "Inhala, la cabeza vuelve al centro.",
               "Exhala, la oreja izquierda va hacia el hombro izquierdo. ((3 respiraciones))",
               "Inhala, vuelve al centro."]),
        ("F", "Haz el movimiento pequeño. No empujes la cabeza con la mano."),
        ("T", "Deja la cabeza en el centro. Ahora los hombros."),
    ]),
    row([("seated_shoulders", None)], "Círculos de hombros", [("5 + 5 círculos", "n")], [
        ("P", "Brazos relajados, manos sobre los muslos."),
        ("R", ["Inhala, sube los hombros hacia las orejas. Exhala, llévalos hacia atrás y hacia abajo.",
               "Cinco círculos hacia atrás, despacio, con la respiración. ((5 círculos))",
               "Ahora cinco círculos hacia delante. ((5 círculos))"]),
        ("F", "Haz círculos más pequeños."),
        ("T", "Deja los hombros quietos y relajados."),
    ]),
    row([("sidebend_R", "Brazo derecho arriba"), ("sidebend_L", "Brazo izquierdo arriba")],
        "Inclinación lateral", [("3 resp. por lado", "n")], [
            ("E", "Apoya la mano izquierda en el suelo, al lado de la cadera izquierda."),
            ("P", ["Inhala y sube el brazo derecho hacia el techo.",
                   "Exhala e inclínate hacia la izquierda: el brazo derecho pasa por encima de la cabeza.",
                   "Los dos glúteos se quedan en el suelo. El pecho mira al frente."]),
            ("R", ["Quédate tres respiraciones. Al inhalar, siente cómo se abre el costado derecho. ((3 respiraciones))",
                   "Inhala, vuelve al centro. Exhala, baja el brazo.",
                   "Cambiamos de lado: mano derecha en el suelo. Inhala, brazo izquierdo arriba. Exhala, inclínate hacia la derecha. ((3 respiraciones))",
                   "Inhala, vuelve al centro. Exhala, baja el brazo."]),
            ("F", "Inclínate solo un poco. Puedes dejar la mano de arriba en la cintura."),
            ("T", ["Ahora vamos a cuatro apoyos. Descruza las piernas, gira hacia un lado y ponte de rodillas, mirando hacia la parte delantera de la esterilla.",
                   "Apoya las manos en el suelo, delante de ti."]),
        ], last=True),
])
parts.append(section(3, "Calentamiento sentado", "0:08 – 0:12", s3, brk=False))

# ---------------------------------------------------------------- 4 all fours
s4 = table([
    row([("tabletop", None)], "Cuatro apoyos", [resp(2)], [
        ("E", "Estamos de rodillas, con las manos en el suelo."),
        ("P", ["Manos justo debajo de los hombros. Abre bien los dedos y presiona toda la palma.",
               "Rodillas debajo de las caderas, separadas al ancho de las caderas. Empeines en el suelo.",
               "Espalda larga y plana, como una mesa. Mira al suelo, entre las manos: la nuca larga."]),
        ("R", "Respira aquí dos veces. ((2 respiraciones))"),
        ("F", "Si te duelen las rodillas, dobla la esterilla o pon una manta debajo."),
        ("T", "Ahora movemos la espalda: la vaca y el gato."),
    ]),
    row([("cow", "Vaca · inhala"), ("cat", "Gato · exhala")], "Vaca y gato", [("5 veces", "n")], [
        ("P", "Las manos y las rodillas se quedan en su sitio. Solo se mueve la espalda."),
        ("R", ["**Vaca:** inhala, deja bajar el abdomen, lleva el pecho hacia delante y mira un poco hacia arriba.",
               "**Gato:** exhala, empuja el suelo con las manos, redondea la espalda hacia el techo y mira hacia el ombligo.",
               "Inhala, vaca… Exhala, gato…",
               "Seguimos cinco veces, a tu ritmo. ((5 veces))"]),
        ("F", "Haz un movimiento pequeño. No hace falta mover mucho el cuello: intenta que se mueva toda la espalda."),
        ("T", "Vuelve a la espalda plana, como una mesa."),
    ]),
    row([("child", None)], "Postura del niño", [resp(3)], [
        ("E", ["Junta los dedos gordos de los pies y separa un poco las rodillas.",
               "Exhala y lleva las caderas hacia los talones."]),
        ("P", ["Brazos estirados hacia delante, palmas en el suelo.",
               "Apoya la frente en el suelo. Relaja los hombros y la cara."]),
        ("R", "Respira aquí tres veces. Siente cómo la respiración mueve tu espalda. ((3 respiraciones))"),
        ("F", ["Si la frente no llega al suelo, pon los puños o un bloque debajo.",
               "Si te molestan las rodillas, pon una manta entre las caderas y los talones.",
               "Recuerda: puedes volver a esta postura siempre que quieras descansar."]),
        ("T", "Inhala y sube despacio a cuatro apoyos."),
    ], last=True),
])
parts.append(section(4, "Cuatro apoyos, vaca-gato y niño", "0:12 – 0:16", s4, brk=False))

dog_strip = strip([
    ("child", "Niño", None),
    ("tabletop", "1 · Cuatro apoyos", None),
    ("tabletop_toes", "2 · Mete los dedos de los pies", None),
    ("downdog_lift", "3 · Caderas arriba y atrás", "exh"),
    ("downdog", "4 · Perro boca abajo", "3–5 resp."),
], scale=0.2, title="Del niño al perro boca abajo, paso a paso")

s4b = dog_strip + table([
    row([("downdog", None)], "Perro boca abajo", [("3 – 5 respiraciones", "n")], [
        ("E", ["**1.** Desde cuatro apoyos: manos debajo de los hombros, rodillas debajo de las caderas.",
               "**2.** Lleva las manos un poco más adelante. Mete los dedos de los pies.",
               "**3.** Presiona toda la palma de las manos contra el suelo.",
               "**4.** Exhala y eleva las caderas hacia arriba y hacia atrás."]),
        ("P", ["Dobla las rodillas todo lo que necesites: lo importante es alargar la espalda, no estirar las piernas.",
               "Pies separados al ancho de las caderas. Los talones no tienen que tocar el suelo.",
               "Manos al ancho de los hombros, dedos abiertos.",
               "Brazos largos, las orejas entre los brazos. Relaja la cabeza y mira hacia las rodillas."]),
        ("R", ["Respira aquí de tres a cinco veces. ((3–5 respiraciones))",
               "Si quieres, pedalea: dobla una rodilla y luego la otra."]),
        ("F", "Si necesitas descansar, baja las rodillas al suelo y vuelve a la postura del niño."),
        ("T", "Ahora vamos a ponernos de pie."),
    ], last=True),
])
parts.append(section("4b", "Del niño al perro boca abajo", "0:16 – 0:18", s4b, brk=False))

# ---------------------------------------------------------------- 5 up to standing
s5 = table([
    row([("fold", None)], "Caminar hacia las manos", [resp(3)], [
        ("E", ["Desde el perro, dobla las rodillas y mira entre tus manos.",
               "Camina con pasos pequeños hasta que los pies lleguen cerca de las manos."]),
        ("P", ["Pies separados al ancho de las caderas. Dobla las rodillas todo lo que quieras.",
               "Deja colgar la cabeza y los brazos. Si quieres, agarra los codos con las manos."]),
        ("R", "Respira aquí tres veces. Relaja el cuello. ((3 respiraciones))"),
        ("F", "Si no llegas al suelo, apoya las manos en las espinillas."),
        ("T", "Vamos a subir muy despacio."),
    ]),
    row([("roll_up", None)], "Subir enrollando la espalda", [("1 – 2 respiraciones", "n")], [
        ("P", "Rodillas dobladas. La barbilla cerca del pecho."),
        ("R", ["Inhala y sube muy despacio, enrollando la espalda, vértebra a vértebra.",
               "La cabeza sube la última."]),
        ("F", "Si te mareas, dobla más las rodillas y sube todavía más despacio."),
        ("T", "Ya estás de pie."),
    ]),
    row([("tadasana", None)], "Montaña (Tadasana)", [resp(3)], [
        ("P", ["Estás de pie, en la postura de la montaña.",
               "Pies paralelos, separados al ancho de las caderas. Reparte el peso entre los dos pies.",
               "Rodillas sueltas, no bloqueadas. Pelvis neutra, abdomen suave.",
               "Hombros relajados, brazos a los lados. La coronilla sube hacia el techo. Mira al frente."]),
        ("R", "Respira aquí tres veces. Siente los pies en el suelo. ((3 respiraciones))"),
        ("F", "Si te cuesta el equilibrio, separa un poco más los pies."),
        ("T", "Junta las manos delante del pecho. Empezamos el saludo al sol."),
    ], last=True),
])
parts.append(section(5, "Del perro a la montaña", "0:18 – 0:20", s5, brk=False))

# ---------------------------------------------------------------- 6 sun salutation round 1
sun_r1 = [
    (1, [("tadasana_heart", None)], "Montaña, manos al corazón", [EXH], [
        ("X", "El saludo al sol une todo lo que hemos hecho. La primera vez vamos muy despacio y te explico cada paso."),
        ("P", ["De pie, pies al ancho de las caderas, el peso repartido.",
               "Junta las palmas delante del pecho. Hombros relajados."]),
        ("R", "Exhala por la nariz."),
    ]),
    (2, [("arms_up", None)], "Brazos arriba", [INH], [
        ("M", "Inhala: abre los brazos por los lados y súbelos hacia el techo."),
        ("P", "Brazos al ancho de los hombros. Hombros lejos de las orejas. Mira al frente. No arquees la espalda."),
        ("F", "Si te molestan los hombros, sube los brazos solo hasta donde es cómodo."),
    ]),
    (3, [("fold", None)], "Flexión hacia delante", [EXH], [
        ("M", "Exhala: dobla las rodillas y baja el pecho hacia los muslos, doblándote desde las caderas."),
        ("P", "Las manos van al suelo, a los lados de los pies. Relaja la cabeza."),
        ("F", "Dobla las rodillas todo lo que necesites. Las manos pueden ir a las espinillas."),
    ]),
    (4, [("half_lift", None)], "Media elevación", [INH], [
        ("M", "Inhala: manos en las espinillas y alarga la espalda hacia delante."),
        ("P", "Espalda plana, como una mesa. Mira al suelo, un poco delante de ti."),
        ("F", "Dobla más las rodillas. Las manos pueden subir a los muslos."),
    ]),
    (5, [("step_back_right", None)], "Pie derecho atrás", [EXH], [
        ("M", "Exhala: dobla las rodillas, pon las manos en el suelo a los lados de los pies y lleva el pie derecho atrás, un paso grande."),
        ("P", "Rodilla izquierda encima del tobillo izquierdo. Los dedos del pie derecho apoyados en el suelo."),
        ("F", "Puedes bajar la rodilla derecha al suelo."),
    ]),
    (6, [("plank_knees", None)], "Plancha con rodillas en el suelo", [INH], [
        ("M", "Inhala: lleva también el pie izquierdo atrás, al lado del derecho."),
        ("P", ["Manos debajo de los hombros. Baja las dos rodillas al suelo.",
               "El cuerpo en línea, desde las rodillas hasta la cabeza. Abdomen activo."]),
        ("S", "Si quieres más fuerza, estira las piernas: plancha completa."),
    ]),
    (7, [("prone", None)], "Bajar al suelo", [EXH], [
        ("M", "Exhala: dobla los codos hacia atrás y baja despacio todo el cuerpo al suelo."),
        ("P", "Estás boca abajo. Empeines en el suelo. Manos al lado del pecho, codos pegados al cuerpo."),
        ("F", "Baja como puedas, por partes: primero el pecho, luego el abdomen. Sin prisa."),
    ]),
    (8, [("cobra", None)], "Cobra", [INH], [
        ("M", "Inhala: presiona suavemente las manos y sube un poco el pecho."),
        ("P", ["La pelvis, los muslos y los empeines se quedan en el suelo.",
               "Codos doblados y pegados al cuerpo. Hombros lejos de las orejas.",
               "Mira al suelo, un poco delante de ti: la nuca larga. Casi sin peso en las manos."]),
        ("F", "Sube solo un poco, o apoya los antebrazos en el suelo."),
    ]),
    (9, [("downdog", None)], "Perro boca abajo", [EXH, resp(3)], [
        ("M", ["Exhala: baja el pecho al suelo.",
               "Mete los dedos de los pies, sube a cuatro apoyos y lleva las caderas hacia arriba y hacia atrás."]),
        ("P", "Rodillas dobladas si lo necesitas. Talones libres. Cabeza relajada."),
        ("R", "Quédate aquí tres respiraciones. ((3 respiraciones))"),
        ("F", "Puedes quedarte en cuatro apoyos o en la postura del niño."),
    ]),
    (10, [("half_lift", None)], "Caminar a las manos · media elevación", [INH], [
        ("M", ["Dobla las rodillas, mira entre las manos y camina los pies hacia las manos.",
               "Inhala: manos en las espinillas, espalda larga."]),
    ]),
    (11, [("fold", None)], "Flexión hacia delante", [EXH], [
        ("M", "Exhala: flexión hacia delante. Rodillas dobladas, cabeza relajada."),
    ]),
    (12, [("arms_up", None)], "Subir · brazos arriba", [INH], [
        ("M", "Inhala: dobla las rodillas, abre los brazos por los lados y sube con la espalda larga hasta estar de pie, brazos arriba."),
        ("F", "Si te mareas, sube despacio con las manos en las caderas."),
    ]),
    (13, [("tadasana_heart", None)], "Manos al corazón", [EXH], [
        ("M", "Exhala: baja las manos delante del pecho."),
        ("R", "Respira aquí una vez. Observa cómo te sientes. ((1 respiración))"),
        ("T", "Vamos a repetir el saludo al sol, con menos palabras."),
    ]),
]
r1rows = [row(f, n, b, it, num=k, last=(k == 13)) for k, f, n, b, it in sun_r1]
parts.append(section(6, "Saludo al sol · Ronda 1: muy despacio", "0:20 – 0:26", table(r1rows),
                     sub="Explico cada paso. Esta ronda vuelve a la montaña al final."))

# ---------------------------------------------------------------- 6b cobra vs upward dog + rounds 2, 3
cmp_html = f'''
<div class="cmp">
  <div class="cmpcol">
    <div class="cmph">Cobra <span class="badge b-n">por defecto</span></div>
    {fig("cobra", max_w=62, max_h=26, cap=0.4)}
  </div>
  <div class="cmpcol">
    <div class="cmph">Perro boca arriba <span class="badge b-s">opcional · más fuerte</span></div>
    {fig("updog", max_w=62, max_h=26, cap=0.4)}
  </div>
  <table class="cmpt">
    <tr><th></th><th>Cobra</th><th>Perro boca arriba</th></tr>
    <tr><td>Brazos</td><td>codos <b>doblados</b>, pegados al cuerpo</td><td>brazos <b>estirados</b></td></tr>
    <tr><td>Pelvis y muslos</td><td><b>en el suelo</b></td><td><b>elevados</b>: no tocan el suelo</td></tr>
    <tr><td>Toca el suelo</td><td>manos, pelvis, piernas, empeines</td><td>solo <b>manos y empeines</b></td></tr>
    <tr><td>Fuerza</td><td>la espalda trabaja, casi sin peso en las manos</td><td>mucho peso en brazos y muñecas; más arco en la espalda</td></tr>
  </table>
</div>'''

sun_frames = [
    ("tadasana_heart", "1", "exh"), ("arms_up", "2", "inh"), ("fold", "3", "exh"), ("half_lift", "4", "inh"),
    ("step_back_right", "5 · pie D atrás", "exh"), ("plank_knees", "6", "inh"), ("prone", "7", "exh"),
    ("cobra", "8", "inh"), ("downdog", "9", "3 resp."), ("half_lift", "10", "inh"), ("fold", "11", "exh"),
    ("arms_up", "12", "inh"), ("tadasana_heart", "13", "exh"),
]
sun_strip = (strip(sun_frames[:7], scale=0.155, title="El saludo al sol completo (números = pasos de la ronda 1)")
             + strip(sun_frames[7:], scale=0.155))

r2 = [
    (1, "Manos al corazón."), (2, "Inhala, brazos arriba."), (3, "Exhala, flexión. Rodillas dobladas."),
    (4, "Inhala, espalda larga."), (5, "Exhala, manos al suelo, pie derecho atrás."),
    (6, "Inhala, pie izquierdo atrás. Rodillas al suelo."), (7, "Exhala, baja al suelo despacio."),
    (8, "Inhala, cobra."), (9, "Exhala, perro boca abajo. ((3 respiraciones))"),
    (10, "Camina a las manos. Inhala, espalda larga."), (11, "Exhala, flexión."),
    (12, "Inhala, sube, brazos arriba."), (13, "Exhala, manos al corazón."),
]
r3 = [
    (1, "Exhala, manos al corazón."), (2, "Inhala… brazos arriba."), (3, "Exhala… flexión."),
    (4, "Inhala… espalda larga."), (5, "Exhala… pie derecho atrás."),
    (6, "Inhala… pie izquierdo atrás, plancha."), (7, "Exhala… rodillas al suelo, baja despacio."),
    (8, "Inhala… cobra, o perro boca arriba."),
    (9, "Exhala… perro boca abajo. Nos quedamos aquí. ((3 respiraciones, luego empieza el flow))"),
]


def numlist(items):
    return '<ol class="nl">' + "".join(f'<li><span class="nn">{n}</span><span>{rich(t)}</span></li>' for n, t in items) + "</ol>"


r2html = f'''<div class="round">
  <div class="roundh"><span class="rtag">Ronda 2</span> Misma secuencia, menos palabras <span class="time">0:26 – 0:28</span></div>
  {cues([("E", "Otra vez el saludo al sol. Ahora con menos palabras. Sigue mi voz.")])}
  {numlist(r2)}
  {cues([("T", "Muy bien. Una vez más: ahora, un movimiento con cada respiración.")])}
</div>'''

r3html = f'''<div class="round">
  <div class="roundh"><span class="rtag">Ronda 3</span> Un movimiento = una respiración <span class="time">0:28 – 0:31</span></div>
  {cues([("X", ["En esta ronda, en el paso 8, puedes elegir.",
                "La **cobra**: pelvis y muslos en el suelo, codos doblados. Es la opción básica, y es igual de buena.",
                "O el **perro boca arriba**, más fuerte: estira los brazos, empuja los empeines contra el suelo y eleva las rodillas y los muslos. Solo tocan el suelo las manos y los empeines.",
                "Si notas las muñecas o la zona lumbar, quédate en cobra."]),
         ("R", "Ahora, un movimiento con cada respiración. Sigue mi voz.")])}
  {numlist(r3)}
  {cues([("T", "Esta vez no subimos: nos quedamos en perro boca abajo y empezamos el flow de pie.")])}
</div>'''

s6b = cmp_html + sun_strip + r2html + r3html
parts.append(section("6b", "Cobra o perro boca arriba · Rondas 2 y 3", "0:26 – 0:31", s6b, brk=False))


# ---------------------------------------------------------------- 7/8 standing flow
def flow(side_r=True):
    D = "derecho" if side_r else "izquierdo"
    O = "izquierdo" if side_r else "derecho"
    Da = "derecha" if side_r else "izquierda"
    Oa = "izquierda" if side_r else "derecha"
    k = "R" if side_r else "L"
    dog = "downdog" if side_r else "downdog_L"
    frames = [
        (dog, "Perro boca abajo", None),
        (f"lunge_{k}", f"Pie {D} adelante", "exh"),
        (f"lunge_rise_{k}", f"Talón {O} abajo · sube", "inh"),
        (f"w2_{k}", "Guerrero II", "3 resp."),
        (f"rev_{k}", "Guerrero inverso", "3 resp."),
        (f"sa_{k}", "Ángulo lateral", "3 resp."),
        (f"w2_{k}", "Guerrero II", "inh"),
        (f"lunge_{k}", "Manos al suelo", "exh"),
        (dog, f"Pie {D} atrás · perro", "3 resp."),
    ]
    st = (strip(frames[:5], scale=0.14, title=f"El camino completo · lado {D}")
          + strip(frames[4:], scale=0.14))
    rows = [
        row([(dog, None)], "Perro boca abajo", [resp(1)], [
            ("E", ("Estamos en perro boca abajo. Empezamos el flow directamente desde aquí."
                   if side_r else "Estamos en perro boca abajo. Ahora, el mismo camino con la pierna izquierda.")),
            ("R", "Inhala: mira entre las manos."),
        ], num=1),
        row([(f"lunge_{k}", None)], f"Pie {D} adelante", [EXH], [
            ("M", f"Exhala: lleva el pie {D} hacia delante, entre las manos."),
            ("P", f"Rodilla {Da} encima del tobillo {D}. Pierna {Oa} larga, atrás."),
            ("F", f"Si el pie no llega, baja la rodilla {Oa} al suelo y ayuda al pie con la mano {Da}."),
        ], num=2),
        row([(f"lunge_rise_{k}", None)], f"Talón {O} abajo · subir", [INH], [
            ("M", [f"Gira el pie {O} hacia fuera y apoya todo el pie en el suelo. Los dedos del pie {O} miran hacia el lado largo de la esterilla.",
                   "Inhala: sube el torso, manos en las caderas."]),
            ("F", "Si pierdes el equilibrio, separa un poco más los pies hacia los lados."),
        ], num=3),
        row([(f"w2_{k}", None)], f"Guerrero II · {Da}", [EXH, resp(3)], [
            ("M", f"Exhala: abre los brazos en cruz, a la altura de los hombros. Brazo {D} hacia delante, brazo {O} hacia atrás."),
            ("P", ["El pecho y las caderas miran hacia el lado largo de la esterilla.",
                   f"Rodilla {Da} doblada, encima del tobillo, en la dirección del segundo dedo del pie. No dejes que la rodilla caiga hacia dentro.",
                   f"Pierna {Oa} estirada y fuerte: el borde exterior del pie {O} presiona el suelo.",
                   f"Torso recto, encima de las caderas. Hombros relajados. Mira por encima de la mano {Da}."]),
            ("R", "Respira aquí tres veces. ((3 respiraciones))"),
            ("F", [f"Acorta la distancia entre los pies o dobla menos la rodilla {Da}.",
                   "Si se cansan los brazos, manos en las caderas."]),
        ], num=4),
        row([(f"rev_{k}", None)], "Guerrero inverso", [INH, resp(3)], [
            ("M", [f"Mantén la rodilla {Da} doblada. Baja la mano {Oa} y apóyala, muy ligera, sobre la pierna {Oa}.",
                   f"Inhala: sube el brazo {D} hacia el techo y un poco hacia atrás."]),
            ("P", [f"No pongas peso en la mano de atrás. Alarga el costado {D}.",
                   f"Mira hacia la mano {Da}, o al frente si te molesta el cuello."]),
            ("R", "Respira aquí tres veces. ((3 respiraciones))"),
            ("F", "Inclínate menos: el brazo de arriba más vertical."),
        ], num=5),
        row([(f"sa_{k}", None)], "Ángulo lateral extendido", [EXH, resp(3)], [
            ("M", ["Inhala: sube el torso al centro.",
                   f"Exhala: inclínate hacia delante, por encima de la pierna {Da}, y apoya el antebrazo {D} sobre el muslo {D}."]),
            ("P", [f"La rodilla {Da} sigue encima del tobillo.",
                   f"El brazo {O} sube hacia el techo, o se estira por encima de la oreja.",
                   f"Una línea larga desde el pie {O} hasta la mano {Oa}. Abre el pecho hacia el lado largo de la esterilla.",
                   "Mira hacia arriba o al frente."]),
            ("R", "Respira aquí tres veces. ((3 respiraciones))"),
            ("F", f"Deja la mano {Oa} en la cadera."),
            ("S", f"Mano {Da} en un bloque o en el suelo, por fuera del pie {D}, solo si el pecho sigue abierto."),
        ], num=6),
        row([(f"w2_{k}", None)], "Guerrero II", [INH], [
            ("M", f"Inhala: empuja con el pie {O}, sube el torso al centro y abre los brazos en cruz. Guerrero II."),
            ("R", "Una respiración. ((1 respiración))"),
        ], num=7),
        row([(f"lunge_{k}", None)], "Manos al suelo", [EXH], [
            ("M", [f"Exhala: gira el torso hacia la pierna {Da} y baja las manos al suelo, una a cada lado del pie {D}.",
                   f"Levanta el talón {O}: los dedos del pie {O} apoyados en el suelo."]),
            ("F", f"Baja la rodilla {Oa} al suelo, o pon las manos en bloques."),
        ], num=8),
        row([(dog, None)], f"Pie {D} atrás · perro boca abajo", [EXH, resp(3)], [
            ("M", [f"Inhala… Exhala: lleva el pie {D} atrás, al lado del pie {O}, y sube las caderas: perro boca abajo."]),
            ("R", "Respira aquí tres veces. ((3 respiraciones))"),
            ("F", "Si necesitas descansar, baja las rodillas: postura del niño."),
            ("T", ("Ahora, el mismo camino con la pierna izquierda."
                   if side_r else "Dobla las rodillas, mira entre las manos y camina los pies hacia las manos.")),
        ], num=9, last=side_r),
    ]
    if not side_r:
        rows += [
            row([("roll_up", None)], "Subir a la montaña", [INH, resp(3)], [
                ("M", ["Pies al ancho de las caderas, rodillas dobladas.",
                       "Inhala y sube muy despacio, enrollando la espalda. La cabeza sube la última."]),
                ("P", "De pie, en la montaña. Brazos a los lados. Respira tres veces. ((3 respiraciones))"),
                ("T", "Ahora vamos a trabajar el equilibrio: el árbol."),
            ], num=10, last=True),
        ]
    return st + table(rows)


note_mirror = ('<div class="pmline">Pour moi : face à eux, montre avec ta jambe <b>gauche</b> quand tu dis '
               '<b class="sr">derecho</b> (miroir). Le texte parle toujours du côté de l’élève.</div>')
parts.append(section(7, "Flow de pie · lado derecho", "0:31 – 0:37", note_mirror + flow(True)))
parts.append(section(8, "Flow de pie · lado izquierdo", "0:37 – 0:42", flow(False), brk=False))

# ---------------------------------------------------------------- 9 tree
s9 = table([
    row([("tree_R_easy", "Fácil: dedos en el suelo"), ("tree_R", "Pie en la pantorrilla")],
        "Árbol · pie derecho arriba", [("3 – 5 respiraciones", "n")], [
            ("E", "De pie, en la montaña. Mira un punto fijo delante de ti, algo que no se mueve."),
            ("P", ["Lleva el peso al pie izquierdo.",
                   "Primero la opción fácil: apoya el talón derecho en el tobillo izquierdo y deja los dedos del pie derecho en el suelo.",
                   "Si quieres más, sube la planta del pie derecho a la pantorrilla izquierda. **Nunca sobre la rodilla.**",
                   "La rodilla derecha se abre hacia el lado. Manos juntas delante del pecho.",
                   "Pierna izquierda activa. La pelvis mira al frente."]),
            ("R", "Respira aquí de tres a cinco veces. ((3–5 respiraciones))"),
            ("F", ["Puedes tocar una pared o una silla con una mano.",
                   "Si pierdes el equilibrio, no pasa nada: vuelve a colocar el pie y sigue respirando."]),
            ("T", "Exhala, baja el pie. Siente los dos pies en el suelo. Cambiamos de lado."),
        ]),
    row([("tree_L", None)], "Árbol · pie izquierdo arriba", [("3 – 5 respiraciones", "n")], [
        ("E", "Mira tu punto fijo. Lleva el peso al pie derecho."),
        ("P", ["Talón izquierdo en el tobillo derecho, dedos en el suelo. O la planta del pie izquierdo en la pantorrilla derecha.",
               "La rodilla izquierda se abre hacia el lado. Manos delante del pecho. Pierna derecha activa."]),
        ("R", "Respira aquí de tres a cinco veces. ((3–5 respiraciones))"),
        ("F", "Pared, silla o dedos en el suelo: todas las opciones están bien."),
        ("T", ["Exhala, baja el pie.",
               "Ahora bajamos al suelo: dobla las rodillas, apoya las manos en el suelo y siéntate despacio en el centro de la esterilla."]),
    ], last=True),
])
parts.append(section(9, "Árbol · equilibrio", "0:42 – 0:46", s9, brk=False))

# ---------------------------------------------------------------- 10 floor
floor_strip = strip([
    ("butterfly", "Mariposa", "3 resp."),
    ("supine_knees", "Boca arriba", None),
    ("bridge", "Puente", "3 veces"),
    ("knees_chest", "Rodillas al pecho", "3 resp."),
    ("twist_R", "Torsión derecha", "3 resp."),
    ("twist_L", "Torsión izquierda", "3 resp."),
], scale=0.13, title="Bajamos la intensidad poco a poco")

s10 = floor_strip + table([
    row([("butterfly", None)], "Mariposa", [resp(3)], [
        ("E", "Siéntate en el centro de la esterilla. Junta las plantas de los pies y deja las rodillas abiertas hacia los lados."),
        ("P", ["Agarra los pies o los tobillos con las manos. Alarga la espalda.",
               "Exhala e inclínate solo un poco hacia delante, con la espalda larga."]),
        ("R", "Respira aquí tres veces. ((3 respiraciones))"),
        ("F", ["Aleja los pies del cuerpo, o quédate con la espalda recta.",
               "No empujes las rodillas hacia el suelo. Si quedan altas, pon cojines debajo."]),
        ("T", ["Inhala, sube la espalda. Estira las piernas.",
               "Apoya las manos detrás de ti, baja sobre los codos y túmbate despacio boca arriba."]),
    ]),
    row([("supine_knees", "Posición de salida"), ("bridge", "Puente")], "Puente", [("3 veces", "n"), ("+ 2–3 resp. arriba", "n")], [
        ("E", ["Boca arriba. Dobla las rodillas y apoya los pies en el suelo.",
               "Pies paralelos, al ancho de las caderas, cerca de los glúteos: los dedos de las manos casi tocan los talones.",
               "Brazos a los lados del cuerpo, palmas hacia abajo."]),
        ("M", ["Inhala: empuja los pies contra el suelo y eleva la pelvis.",
               "Exhala: baja despacio.",
               "Repetimos tres veces. En la última, quédate arriba dos o tres respiraciones. ((3 veces))"]),
        ("P", "Rodillas paralelas: no se abren. Nuca larga: no gires la cabeza."),
        ("F", "Sube menos la pelvis."),
        ("T", "Exhala, baja la espalda despacio al suelo."),
    ]),
    row([("knees_chest", None)], "Rodillas al pecho", [resp(3)], [
        ("E", "Lleva las rodillas hacia el pecho y abrázalas."),
        ("P", "Relaja los hombros y la cabeza en el suelo. Deja que la zona lumbar descanse."),
        ("R", "Respira aquí tres veces. Si quieres, balancéate un poco de un lado a otro. ((3 respiraciones))"),
        ("F", "Agarra la parte de atrás de los muslos, en lugar de las espinillas."),
        ("T", "Abre los brazos en cruz, a la altura de los hombros, palmas hacia abajo. Rodillas juntas."),
    ]),
    row([("twist_R", "Visto desde arriba")], "Torsión · derecha", [EXH, resp(3)], [
        ("M", "Exhala y deja caer las dos rodillas hacia la derecha."),
        ("P", ["Mira hacia la izquierda, solo si es cómodo para el cuello.",
               "Los dos hombros se quedan pesados en el suelo."]),
        ("R", "Respira aquí tres veces. ((3 respiraciones))"),
        ("F", "Baja las rodillas solo un poco, o pon un cojín debajo de ellas."),
        ("T", "Inhala, rodillas al centro."),
    ]),
    row([("twist_L", "Visto desde arriba")], "Torsión · izquierda", [EXH, resp(3)], [
        ("M", "Exhala y deja caer las dos rodillas hacia la izquierda."),
        ("P", "Mira hacia la derecha, si es cómodo. Los dos hombros pesados en el suelo."),
        ("R", "Respira aquí tres veces. ((3 respiraciones))"),
        ("T", ["Inhala, rodillas al centro.",
               "Apoya los pies en el suelo y estira las piernas, una y luego la otra. Nos preparamos para la relajación final."]),
    ], last=True),
])
parts.append(section(10, "En el suelo · mariposa, puente, torsión", "0:46 – 0:53", s10, brk=False))

# ---------------------------------------------------------------- 11 savasana
s11 = table([
    row([("savasana", "Visto desde arriba")], "Savasana · relajación final", [("3 – 4 min de silencio", "n")], [
        ("E", "Túmbate boca arriba. Estira las piernas y deja los pies caer suavemente hacia los lados."),
        ("P", ["Brazos a los lados del cuerpo, un poco separados, palmas hacia arriba.",
               "Si te molesta la zona lumbar, dobla las rodillas y apoya los pies en el suelo, o pon un cojín debajo de las rodillas.",
               "Si tienes frío, tápate con una manta. Cierra los ojos si te apetece."]),
        ("Z", ["Relaja los pies… las piernas… el abdomen…",
               "Relaja el pecho… los hombros… los brazos… las manos…",
               "Relaja la mandíbula, los ojos, toda la cara.",
               "Deja que la respiración sea natural.",
               "No hay nada que hacer. Solo descansar.",
               "((3–4 minutos de silencio real))"]),
    ]),
    row([("seated_cross", None)], "Volver y cerrar", [], [
        ("T", ["Poco a poco, respira un poco más profundo.",
               "Mueve los dedos de las manos y de los pies.",
               "Si te apetece, estira los brazos por encima de la cabeza.",
               "Dobla las rodillas y gira hacia el lado derecho. Quédate ahí un momento.",
               "Cuando quieras, empuja el suelo con la mano y siéntate despacio, sin prisa. La cabeza sube la última."]),
        ("C", ["Junta las manos delante del pecho.",
               "Observa cómo te sientes ahora, sin juzgar.",
               "Gracias por practicar conmigo hoy. Namasté."]),
    ], last=True),
])
parts.append(section(11, "Savasana y cierre", "0:53 – 1:00", s11, brk=False))

# ================================================================ PAGE
font_dir = "../fonts"
CSS = (Path(__file__).parent / "style.css").read_text(encoding="utf-8").replace("{FONTS}", font_dir)
doc = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yoga para principiantes · guion</title>
<style>{CSS}</style></head>
<body>{"".join(parts)}</body></html>'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(doc, encoding="utf-8")
print("wrote", OUT)
