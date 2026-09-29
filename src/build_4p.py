"""4-page complete teaching script (A4 portrait) - the main deliverable.

python3 build_4p.py -> ../build/yoga_guion_4p.html  (then print.js -> PDF)
Markup inside the spoken text:
  Inhala / Exhala, derecha / izquierda -> auto highlight (see build.rich)
  [F] easier option   [S] stronger option   [T] transition to next pose
  ((...)) grey stage direction (not read aloud)   **x** bold
"""
import contextlib
import io
import re

with contextlib.redirect_stdout(io.StringIO()):
    import build as B
from build import fig, rich, strip

TOK = {
    "[F]": '<span class="it it-f">MÁS FÁCIL</span>',
    "[S]": '<span class="it it-s">MÁS FUERTE</span>',
    "[T]": '<span class="it it-t">→ SIGUIENTE</span>',
}


def say(t):
    h = rich(t)
    for k, v in TOK.items():
        h = h.replace(k, v)
    return h


def card(pose, name, badge, text, mh=17, mw=26, extra_pose=None, row=False):
    b = f' <span class="badge b-n">{badge}</span>' if badge else ""
    rc = " row" if row else ""
    f2 = fig(extra_pose, max_w=mw, max_h=mh, cap=0.12) if extra_pose else ""
    return (f'<div class="qc"><div class="qf{rc}">{fig(pose, max_w=mw, max_h=mh, cap=0.12)}{f2}</div>'
            f'<div class="qt"><div class="qn">{rich(name)}{b}</div><div class="qcue">{say(text)}</div></div></div>')


def band(num, title, time):
    return (f'<div class="qband"><span class="secn">{num}</span><b>{rich(title)}</b>'
            f'<span class="time">{time}</span></div>')


def grid(cards, cols=2):
    return f'<div class="qgrid c{cols}">' + "".join(cards) + "</div>"


def steps(items, cols=2):
    return (f'<ol class="st c{cols}">' + "".join(
        f'<li><span class="nn">{n}</span><span>{say(t)}</span></li>' for n, t in items) + "</ol>")


def lo_que_digo():
    return '<div class="lqd">LO QUE DIGO</div>'


# ================================================================ PAGE 1
p1 = [
    '<div class="top"><div><div class="kick">Guion completo · se lee en voz alta</div>'
    '<h1>Yoga para principiantes</h1></div>'
    '<div class="leg"><b class="sr">naranja = DERECHA</b> · <b class="sl">azul = IZQUIERDA</b> del alumno'
    ' · figuras de pie vistas de espaldas<br><span class="inh"><i>▲</i>Inhala</span> <span class="exh"><i>▼</i>Exhala</span>'
    ' · <span class="pause">gris = no se lee</span> · <span class="it it-f">MÁS FÁCIL</span> '
    '<span class="it it-t">→ SIGUIENTE</span></div></div>',
    '<div class="pm"><b>Pour moi :</b> lis lentement, 1 respiration de silence entre les phrases. Face à eux, démontre en '
    'miroir mais <b>dis</b> le côté écrit. En retard ? raccourcis l’arbre ou supprime la ronde 2 — <b>jamais Savasana : 4 min pleines minimum</b>.</div>',
    band(1, "Bienvenida · cómo sentarse · reglas", "0:00 – 0:05"), lo_que_digo(),
    grid([
        card("seated_cross", "Sentarse cómodamente", "",
             "Hola a todos, bienvenidos. Me llamo ___. Es una clase para principiantes: vamos despacio. "
             "Siéntate de la forma más cómoda para ti: piernas cruzadas —si las rodillas quedan altas, siéntate sobre una manta—, "
             "piernas estiradas con las rodillas un poco dobladas, o de rodillas sobre los talones, si es cómodo. "
             "Manos sobre los muslos, espalda larga, hombros relajados. [F] Si te molesta, cambia de posición.",
             extra_pose="kneeling", mh=14),
        card("child", "Qué es el yoga · reglas", "",
             "Hoy vamos a intentar coordinar el movimiento con la respiración. Muchas veces inhalaremos para crecer o abrir el cuerpo, y exhalaremos para bajar o entrar suavemente en una postura. "
             "Respiramos por la nariz. No hace falta una postura perfecta: cada cuerpo es diferente. "
             "**Nada debe doler.** Estirar, sí; dolor, no: si algo duele, sal despacio. "
             "Puedes descansar siempre en la **postura del niño**. Si tienes una lesión o estás embarazada, avísame."),
    ]),
    band(2, "Respiración", "0:05 – 0:08"),
    grid([card("seated_cross", "Respiración abdominal", "5 resp.",
               "Cierra los ojos si quieres. Una mano en el abdomen, otra en el pecho. "
               "Inhala por la nariz: el abdomen se hincha como un globo. Exhala: el abdomen baja. "
               "Inhala… dos, tres, cuatro. Exhala… dos, tres, cuatro. ((5 respiraciones)) "
               "[F] Si contar te agobia, solo observa el aire. "
               "[T] Manos a los muslos, respiración natural, abre los ojos.")], cols=1),
    band(3, "Calentamiento sentado", "0:08 – 0:12"),
    grid([
        card("seated_neck", "Cuello", "3 resp./lado",
             "Espalda larga. Exhala: oreja derecha hacia el hombro derecho; el hombro izquierdo baja. ((3 resp.)) "
             "Inhala, al centro. Exhala: oreja izquierda al hombro izquierdo. ((3 resp.)) Inhala, al centro. "
             "[F] Movimiento pequeño, sin tirar con la mano."),
        card("seated_shoulders", "Hombros", "5 + 5",
             "Inhala, sube los hombros hacia las orejas. Exhala, llévalos atrás y abajo. "
             "Cinco círculos hacia atrás… cinco hacia delante. [F] Círculos más pequeños. "
             "[T] Hombros quietos y relajados."),
        card("sidebend_R", "Inclinación lateral", "3 resp./lado",
             "Mano izquierda en el suelo, junto a la cadera. Inhala, brazo derecho arriba. "
             "Exhala, inclínate a la izquierda; los dos glúteos en el suelo. ((3 resp.)) "
             "Inhala al centro, exhala baja el brazo. Otro lado: mano derecha al suelo, brazo izquierdo arriba, inclínate a la derecha. "
             "[F] Inclínate poco, mano en la cintura.", extra_pose="sidebend_L", mh=14),
        card("tabletop", "Cuatro apoyos", "2 resp.",
             "[T] Descruza las piernas, gira y ponte de rodillas mirando al frente de la esterilla. "
             "Manos justo debajo de los hombros, dedos abiertos. Rodillas debajo de las caderas. Empeines en el suelo. "
             "Espalda plana como una mesa, mira entre las manos. [F] Manta debajo de las rodillas."),
    ]),
    band(4, "Vaca-gato · niño · perro boca abajo", "0:12 – 0:18"),
    grid([
        card("cow", "Vaca / gato", "5 veces",
             "Manos y rodillas quietas: solo se mueve la espalda. **Vaca:** inhala, baja el abdomen, pecho adelante, mira un poco arriba. "
             "**Gato:** exhala, empuja el suelo, redondea la espalda, mira al ombligo. Cinco veces, a tu ritmo. "
             "[F] Movimiento pequeño, cuello tranquilo. [T] Espalda plana.", extra_pose="cat", mh=13),
        card("child", "Postura del niño", "3 resp.",
             "Junta los dedos gordos, separa un poco las rodillas. Exhala, caderas a los talones. "
             "Brazos largos delante, frente al suelo, hombros relajados. ((3 resp.)) "
             "[F] Puños o bloque bajo la frente; manta entre caderas y talones. Aquí puedes descansar siempre. "
             "[T] Inhala, vuelve a cuatro apoyos."),
    ]),
    strip([("tabletop", "1 · Cuatro apoyos", None), ("tabletop_toes", "2 · Dedos de los pies dentro", None),
           ("downdog_lift", "3 · Caderas arriba y atrás", "exh"), ("downdog", "4 · Perro boca abajo", "3–5 resp.")],
          scale=0.13),
    grid([card("downdog", "Perro boca abajo", "3–5 resp.",
               "Desde cuatro apoyos, manos un poco más adelante. Mete los dedos de los pies. Presiona toda la palma. "
               "Exhala: caderas arriba y atrás. Dobla las rodillas todo lo que necesites: lo importante es la espalda larga. "
               "Pies al ancho de las caderas; los talones no tienen que tocar el suelo. Orejas entre los brazos, cabeza relajada, mira a las rodillas. "
               "((3–5 resp.)) Si quieres, pedalea. [F] Rodillas al suelo: postura del niño.")], cols=1),
]

# ================================================================ PAGE 2
r1 = [
    (1, "**Montaña, manos al corazón.** Pies al ancho de las caderas, palmas juntas delante del pecho. Exhala."),
    (2, "**Brazos arriba.** Inhala: abre los brazos por los lados y súbelos. Hombros lejos de las orejas, no arquees la espalda."),
    (3, "**Flexión.** Exhala: dobla las rodillas y baja el pecho a los muslos. Manos al suelo o a las espinillas, cabeza relajada."),
    (4, "**Media elevación.** Inhala: manos en las espinillas, espalda plana hacia delante, mira al suelo."),
    (5, "**Pie derecho atrás.** Exhala: manos al suelo y un paso grande atrás con el pie derecho. Rodilla izquierda sobre el tobillo. [F] Rodilla derecha al suelo."),
    (6, "**Plancha.** Inhala: pie izquierdo atrás. Manos bajo los hombros, rodillas al suelo, cuerpo en línea. [S] Piernas estiradas."),
    (7, "**Bajar.** Exhala: codos hacia atrás, baja despacio todo el cuerpo al suelo. Manos al lado del pecho."),
    (8, "**Cobra.** Inhala: sube un poco el pecho. Pelvis, muslos y empeines en el suelo; codos doblados y pegados. Nuca larga. [F] Antebrazos al suelo."),
    (9, "**Perro boca abajo.** Exhala: dedos de los pies dentro, cuatro apoyos, caderas arriba y atrás. ((3 resp.)) [F] Niño o cuatro apoyos."),
    (10, "**Caminar a las manos.** Rodillas dobladas, camina los pies a las manos. Inhala: media elevación."),
    (11, "**Flexión.** Exhala: rodillas dobladas, cabeza relajada."),
    (12, "**Subir.** Inhala: abre los brazos y sube con la espalda larga, brazos arriba. [F] Manos en las caderas si te mareas."),
    (13, "**Manos al corazón.** Exhala. Observa cómo te sientes. ((1 resp.))"),
]
sun = B.sun_frames
p2 = [
    band(5, "Del perro a la montaña", "0:18 – 0:20"), lo_que_digo(),
    grid([
        card("fold", "Caminar a las manos", "3 resp.",
             "Dobla las rodillas, mira entre las manos y camina con pasos pequeños hacia ellas. "
             "Pies al ancho de las caderas. Deja colgar cabeza y brazos. ((3 resp.)) [F] Manos en las espinillas."),
        card("roll_up", "Subir enrollando", "1–2 resp.",
             "Rodillas dobladas, barbilla al pecho. Inhala y sube despacio, vértebra a vértebra; la cabeza sube la última. "
             "[F] Si te mareas, más despacio."),
        card("tadasana", "Montaña", "3 resp.",
             "Pies paralelos al ancho de las caderas, peso repartido. Rodillas sueltas, pelvis neutra. "
             "Hombros relajados, la coronilla sube. Mira al frente. [F] Separa más los pies. "
             "[T] Manos al pecho: saludo al sol."),
        card("tadasana_heart", "Saludo al sol", "3 rondas",
             "El saludo al sol une todo lo que hemos hecho. La primera vez vamos muy despacio y te explico cada paso. "
             "((Ronda 1 aquí abajo, rondas 2 y 3 en la página siguiente))"),
    ]),
    band(6, "Saludo al sol · Ronda 1: muy despacio, todo explicado", "0:20 – 0:26"),
    strip(sun[:7], scale=0.14) + strip(sun[7:], scale=0.14),
    steps(r1, cols=1),
    '<div class="pm2">[T]</div>'.replace("[T]", say("[T] Muy bien. Repetimos con menos palabras.")),
]

# ================================================================ PAGE 3
r2 = [
    (1, "Manos al corazón. Esta vez empezamos con el pie izquierdo."), (2, "Inhala, brazos arriba."),
    (3, "Exhala, flexión. Rodillas dobladas."), (4, "Inhala, espalda larga."),
    (5, "Exhala, manos al suelo, pie izquierdo atrás."), (6, "Inhala, pie derecho atrás. Rodillas al suelo."),
    (7, "Exhala, baja al suelo despacio."), (8, "Inhala, cobra."),
    (9, "Exhala, perro boca abajo. ((3 respiraciones))"), (10, "Camina a las manos. Inhala, espalda larga."),
    (11, "Exhala, flexión."), (12, "Inhala, sube, brazos arriba."), (13, "Exhala, manos al corazón."),
]
r3 = [
    (1, "Exhala, manos al corazón."), (2, "Inhala… brazos arriba."), (3, "Exhala… flexión."),
    (4, "Inhala… espalda larga."), (5, "Exhala… pie derecho atrás."),
    (6, "Inhala… pie izquierdo atrás, plancha."), (7, "Exhala… rodillas al suelo, baja."),
    (8, "Inhala… **cobra** para la mayoría: pelvis y muslos en el suelo, codos doblados. "
        "Si quieres una opción más intensa, **perro boca arriba**: brazos estirados, solo las manos y los empeines en el suelo, rodillas elevadas. "
        "[F] Si notas las muñecas o la zona lumbar, cobra."),
    (9, "Exhala… perro boca abajo. Nos quedamos aquí. ((3 resp. → flow))"),
]
cmp = f'''<div class="cmp">
 <div class="cmpf"><div><b>Cobra</b> <span class="badge b-n">por defecto</span></div>{fig("cobra", max_w=40, max_h=11, cap=0.3)}
   <div class="cmpd">codos <b>doblados</b> · pelvis y muslos <b>en el suelo</b> · casi sin peso en las manos · suave</div></div>
 <div class="cmpf"><div><b>Perro boca arriba</b> <span class="badge b-s">opcional · más fuerte</span></div>{fig("updog", max_w=40, max_h=11, cap=0.3)}
   <div class="cmpd">brazos <b>estirados</b> · solo <b>manos y empeines</b> tocan el suelo · rodillas y muslos elevados · más peso en muñecas, más arco</div></div>
</div>'''

fl_r = [("downdog", "Perro abajo", None), ("lunge_R", "Pie D adelante", "exh"), ("lunge_rise_R", "Pie I gira · sube", "inh"),
        ("w2_R", "Guerrero II", "3 resp."), ("rev_R", "Inverso", "3 resp."), ("sa_R", "Ángulo lateral", "3 resp."),
        ("w2_R", "Guerrero II", "inh"), ("lunge_R", "Manos al suelo", "exh"), ("downdog", "Pie D atrás · perro", "3 resp.")]
flow_r = [
    (1, "**Perro boca abajo.** Empezamos desde aquí. Inhala, mira entre las manos."),
    (2, "**Pie derecho adelante.** Exhala: el pie derecho entre las manos, rodilla derecha sobre el tobillo. [F] Rodilla izquierda al suelo y ayuda al pie con la mano derecha."),
    (3, "**Pie de atrás.** Gira el pie izquierdo hacia fuera y apoya todo el pie; los dedos miran al lado largo de la esterilla. Inhala: sube el torso, manos a las caderas."),
    (4, "**Guerrero II.** Exhala: brazos en cruz, brazo derecho delante. Pecho y caderas al lado largo. Rodilla derecha sobre el tobillo, hacia el segundo dedo: que no caiga hacia dentro. Pierna izquierda fuerte. Mira la mano derecha. ((3 resp.)) [F] Pies más cerca, rodilla menos doblada."),
    (5, "**Guerrero inverso.** Rodilla derecha doblada. Mano izquierda muy ligera en la pierna izquierda. Inhala: brazo derecho arriba y un poco atrás. Alarga el costado derecho. ((3 resp.)) [F] Inclínate menos."),
    (6, "**Ángulo lateral.** Inhala, al centro. Exhala: antebrazo derecho sobre el muslo derecho. Brazo izquierdo arriba o sobre la oreja: una línea del pie izquierdo a la mano. Pecho abierto. ((3 resp.)) [F] Mano izquierda en la cadera. [S] Mano derecha al suelo o en un bloque."),
    (7, "**Guerrero II.** Inhala: empuja con el pie izquierdo, sube al centro, brazos en cruz. ((1 resp.))"),
    (8, "**Manos al suelo.** Exhala: gira hacia la pierna derecha, manos a cada lado del pie derecho. Talón izquierdo arriba. [F] Rodilla izquierda al suelo."),
    (9, "**Perro boca abajo.** Exhala: pie derecho atrás, caderas arriba. ((3 resp.)) [F] Niño. [T] Mismo camino con la pierna izquierda."),
]
p3 = [
    band("6b", "Saludo al sol · Rondas 2 y 3", "0:26 – 0:31"), lo_que_digo(),
    '<div class="two">'
    f'<div class="rnd"><div class="rh">Ronda 2 · menos palabras · <span class="sl">pie izquierdo</span> atrás</div>{steps(r2, cols=1)}'
    f'<div class="rt">{say("[T] Una vez más: un movimiento con cada respiración.")}</div></div>'
    f'<div class="rnd"><div class="rh">Ronda 3 · un movimiento = una respiración · <span class="sr">pie derecho</span> atrás</div>'
    f'{steps(r3, cols=1)}{cmp}</div></div>',
    band(7, "Flow de pie · lado derecho", "0:31 – 0:37"),
    '<div class="pm"><b>Pour moi :</b> face à eux, montre avec ta jambe <b>gauche</b> quand tu dis <b class="sr">derecha</b>.</div>',
    strip(fl_r, scale=0.1),
    steps(flow_r, cols=1),
]

# ================================================================ PAGE 4
fl_l = [("downdog_L", "Perro abajo", None), ("lunge_L", "Pie I adelante", "exh"), ("lunge_rise_L", "Pie D gira · sube", "inh"),
        ("w2_L", "Guerrero II", "3 resp."), ("rev_L", "Inverso", "3 resp."), ("sa_L", "Ángulo lateral", "3 resp."),
        ("w2_L", "Guerrero II", "inh"), ("lunge_L", "Manos al suelo", "exh"), ("downdog_L", "Pie I atrás · perro", "3 resp.")]
flow_l = [
    (1, "Perro boca abajo. Inhala, mira entre las manos."),
    (2, "Exhala: pie izquierdo entre las manos. [F] Rodilla derecha al suelo."),
    (3, "Gira el pie derecho, apoya todo el pie. Inhala: sube, manos a las caderas."),
    (4, "Exhala: **Guerrero II**, brazo izquierdo delante. Rodilla izquierda sobre el tobillo. Mira la mano izquierda. ((3 resp.))"),
    (5, "**Inverso:** mano derecha ligera en la pierna derecha. Inhala, brazo izquierdo arriba y atrás. ((3 resp.))"),
    (6, "Inhala al centro. Exhala: **ángulo lateral**, antebrazo izquierdo sobre el muslo izquierdo, brazo derecho arriba. ((3 resp.))"),
    (7, "Inhala: **Guerrero II**."), (8, "Exhala: manos al suelo a cada lado del pie izquierdo."),
    (9, "Exhala: pie izquierdo atrás, **perro boca abajo**. ((3 resp.)) [T] Camina a las manos. Inhala, sube enrollando: montaña."),
]
p4 = [
    band(8, "Flow de pie · lado izquierdo", "0:37 – 0:42"), lo_que_digo(),
    strip(fl_l, scale=0.1),
    steps(flow_l, cols=2),
    band(9, "Árbol", "0:42 – 0:46"),
    grid([card("tree_R_easy", "Árbol", "3–5 resp./lado",
               "Mira un punto fijo. Peso al pie izquierdo. Fácil: talón derecho en el tobillo izquierdo, dedos al suelo. "
               "Más: planta en la pantorrilla, **nunca sobre la rodilla.** Rodilla derecha hacia fuera, manos al pecho, pelvis al frente. "
               "((3–5 resp.)) Exhala, baja; otro lado: peso al pie derecho. [F] Pared o silla; si pierdes el equilibrio, no pasa nada. "
               "[T] Dobla las rodillas, manos al suelo y siéntate despacio.", extra_pose="tree_R", mh=20, row=True)], cols=1),
    band(10, "En el suelo", "0:46 – 0:52"),
    grid([
        card("butterfly", "Mariposa", "3 resp.",
             "Plantas de los pies juntas, rodillas abiertas. Manos en los pies, espalda larga. Exhala, inclínate solo un poco. "
             "[F] Pies más lejos; no empujes las rodillas. [T] Inhala, sube. Túmbate despacio boca arriba, sobre los codos."),
        card("bridge", "Puente", "3 veces",
             "Rodillas dobladas, pies al ancho de las caderas cerca de los glúteos, brazos al lado. "
             "Inhala: empuja los pies, eleva la pelvis. Exhala: baja. La última vez, 2–3 resp. arriba. Rodillas paralelas, cabeza quieta. "
             "[F] Sube menos."),
        card("knees_chest", "Rodillas al pecho", "3 resp.",
             "Abraza las rodillas. Hombros y cabeza en el suelo, zona lumbar relajada. Balancéate si quieres. "
             "[F] Agarra detrás de los muslos. [T] Brazos en cruz, palmas abajo."),
        card("twist_R", "Torsión", "3 resp./lado",
             "Exhala: rodillas juntas a la derecha; mira a la izquierda si es cómodo. Hombros pesados. ((3 resp.)) "
             "Inhala al centro. Exhala: rodillas a la izquierda, mira a la derecha. [F] Cojín bajo las rodillas. "
             "[T] Inhala al centro, estira las piernas.", mh=15),
    ]),
    band(11, "Savasana y cierre", "0:52 – 1:00"),
    grid([
        card("savasana", "Savasana", "4 min mínimo",
             "Túmbate boca arriba, piernas estiradas, pies sueltos. Brazos un poco separados, palmas arriba. "
             "[F] Rodillas dobladas o cojín bajo las rodillas; manta si tienes frío. Cierra los ojos. "
             "Relaja los pies… las piernas… el abdomen… el pecho… los hombros… los brazos… la cara. "
             "No hay nada que hacer. Solo descansar. ((4 minutos enteros de silencio: no acortar))", mh=12),
        card("seated_cross", "Volver y cerrar", "",
             "Respira un poco más profundo. Mueve los dedos de las manos y de los pies. Dobla las rodillas y gira a la derecha. "
             "Cuando quieras, siéntate despacio; la cabeza sube la última. Manos al pecho. "
             "Observa cómo te sientes, sin juzgar. Gracias por practicar conmigo. Namasté."),
    ]),
]

css = B.CSS + """
@page { margin: 7mm 8mm 8mm 8mm; @top-right { content: none; }
  @bottom-center { content: "Página " counter(page) " / " counter(pages); font-size: 7.5pt; } }
body { font-size: 9.3pt; line-height: 1.2; }
.pg { break-before: page; } .pg:first-child { break-before: auto; }
.top { display:flex; justify-content:space-between; align-items:flex-end; gap:4mm; border-bottom:2px solid var(--band); padding-bottom:1mm; }
.top h1 { margin:0; font-size:17pt; color:var(--band); line-height:1.05; }
.kick { font-size:8pt; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }
.leg { font-size:8.3pt; text-align:right; line-height:1.5; }
.pm { font-size:8.3pt; background:#fff7df; border-left:3px solid #e2b33c; padding:.7mm 2mm; margin:1mm 0; }
.pm2 { margin: .8mm 0; }
.qband { display:flex; align-items:center; gap:2mm; background:var(--band); color:#fff; border-radius:1.6mm;
         padding:.5mm 2.2mm; margin:1.4mm 0 .8mm; font-size:10.5pt; break-after: avoid; }
.qband .secn { background:#fff; color:var(--band); border-radius:2.5mm; min-width:5.5mm; padding:0 1mm; text-align:center; font-weight:700; font-size:9pt; }
.qband b { flex:1; } .qband .time { font-weight:700; }
.qband .sr, .qband .sl { color:#fff; text-decoration: underline; text-decoration-thickness: 2px; }
.qf.row { flex-direction:row; align-items:flex-end; }
.lqd { font-size:7.5pt; font-weight:700; letter-spacing:.12em; color:var(--band); margin:0 0 .6mm; }
.qgrid { display:grid; gap:1mm; } .qgrid.c2 { grid-template-columns:1fr 1fr; } .qgrid.c1 { grid-template-columns:1fr; }
.qc { display:flex; gap:1.6mm; align-items:flex-start; background:#f5f7f9; border-radius:1.6mm; padding:.9mm 1.4mm; break-inside:avoid; }
.qf { flex:0 0 auto; display:flex; flex-direction:column; align-items:center; gap:.6mm; min-width:14mm; }
.qf svg { display:block; }
.qn { font-weight:700; font-size:9.6pt; margin-bottom:.3mm; } .qn .badge { font-size:7.5pt; padding:0 1.3mm; }
.qcue { font-size:9.3pt; }
.it { font-size:6.6pt; font-weight:700; border-radius:1mm; padding:0 1mm; letter-spacing:.03em; white-space:nowrap; vertical-align:1px; }
.it-f { background:#dff3e6; color:#1f6b3d; } .it-s { background:#fde3cf; color:#8a3a06; } .it-t { background:var(--band); color:#fff; }
.strip { margin-top:.8mm; } .srow { padding:.8mm 2mm; border-radius:1.6mm; } .striptitle { display:none; }
.scap { font-size:7.6pt; } .sb { font-size:7.2pt; } .sarrow { font-size:11pt; padding-bottom:4mm; }
ol.st { list-style:none; margin:1mm 0 0; padding:0; } ol.st.c2 { columns:2; column-gap:4mm; }
ol.st li { display:flex; gap:1.5mm; margin-bottom:.7mm; break-inside:avoid; }
.nn { flex:0 0 4.6mm; height:4.6mm; font-size:7.6pt; border-radius:2.3mm; margin-top:0; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:2mm; }
.rnd { border:1px solid var(--line); border-radius:1.6mm; padding:1mm 1.8mm; }
.rh { font-weight:700; font-size:9.8pt; margin-bottom:.6mm; }
.rt { margin:.8mm 0; }
.cmp { display:grid; grid-template-columns:1fr 1fr; gap:1.5mm; margin-top:1mm; border:0; padding:0; }
.cmpf { background:#f5f7f9; border-radius:1.4mm; padding:.8mm 1.2mm; text-align:center; font-size:9pt; }
.cmpf svg { display:block; margin:.5mm auto; }
.cmpd { font-size:8.2pt; text-align:left; }
"""
pages = [p1, p2, p3, p4]
body = "".join(f'<div class="pg">{"".join(p)}</div>' for p in pages)
doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Yoga · guion 4 páginas</title>'
       f'<style>{css}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / "yoga_guion_4p.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
