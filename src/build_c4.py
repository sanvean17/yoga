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
          "[MC]": ("vx", "MÁS COMPLETO", "PLUS COMPLET"),
          "[NO]": ("vn", "LO QUE NO HACEMOS", "CE QU’ON NE FAIT PAS"),
          "[TO]": ("vt", "PARA TODOS", "POUR TOUS"),
          "[SE]": ("vse", "LO QUE SENTIMOS", "CE QU’ON RESSENT"),
          "[JU]": ("vj", "JUNTOS · LO QUE DIGO", "ENSEMBLE · CE QUE JE DIS")}
    for k, (c, les, lfr) in VB.items():
        h = h.replace(k, f'<span class="vb {c}"><span class="vl">{les if L == "es" else lfr}</span>')
    for k in ("[/C]", "[/CP]", "[/S]", "[/DP]", "[/SU]", "[/MC]", "[/NO]", "[/JU]", "[/TO]", "[/SE]"):
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
# COURSE 4 · tips at the start (sit / stand up safely, stretch or pain, benefits)
# salutation "type B" (invisible chair + warrior I) · W2 → NEW side angle → triangle
# balance: NEW airplane · floor: knee to chest, NEW heel slides, twist, banana, NEW legs on the chair
# ===================================================================
_card2 = card2


def card2(*a, **k):
    k.setdefault('mh', 17)
    a, k = _with_text(a, k)
    return _card2(*a, **k)


_card3 = card3


def card3(*a, **k):
    a, k = _with_text(a, k)
    return _card3(*a, **k)


def opt(html):
    lab = "FACULTATIVO" if L == "es" else "FACULTATIF"
    html = html.replace('class="qc c2"', 'class="qc c2 optc"', 1)
    return html.replace('<div class="qn">', f'<div class="qn"><span class="obadge">{lab}</span> ', 1)


def say(es_t, fr_t):
    return para(es_t, fr_t)


def _t(common, chair=None, alt=None, mc=None, ju=None, intro=None):
    return dict(common=common, chair=chair, alt=alt, mc=mc, ju=ju, intro=intro)


def _build(d, i):
    parts = []
    if d["intro"]:
        parts.append(d["intro"][i])
    if d["chair"]:
        parts.append("[C]" + d["chair"][i] + "[/C]")
    if d["alt"]:
        tag = d["alt"][0]
        parts.append(f"[{tag}]" + d["alt"][1 + i] + f"[/{tag}]")
    if d["chair"] or d["alt"]:
        parts.append("[TO]" + d["common"][i] + "[/TO]")
    else:
        parts.append(d["common"][i])
    if d.get("se"):
        parts.append("[SE]" + d["se"][i] + "[/SE]")
    if d["mc"]:
        parts.append("[MC]" + d["mc"][i] + "[/MC]")
    if d["ju"]:
        parts.append("[JU]" + d["ju"][i] + "[/JU]")
    return " ".join(parts)


HIP = ("Si pellizca en la cadera: los pies menos separados, el pie de delante menos girado, la rodilla menos doblada, o "
       "en la silla.",
       "Si ça pince dans la hanche : les pieds moins écartés, le pied avant moins tourné, le genou moins plié, ou sur la "
       "chaise.")

TEXTS = {
    # ---------------- warm-up ----------------
    "Cuello": _t((
        "Exhalamos: oreja derecha hacia el hombro derecho. ((3 resp.)) Al centro, y al otro lado. Después giramos la cabeza "
        "despacio: miramos a la derecha… a la izquierda. Movimiento pequeño. Los hombros bajan, la mandíbula se suelta. "
        "Cuidado: no hacemos círculos completos con la cabeza y no tiramos con la mano.",
        "On expire : oreille droite vers l’épaule droite. ((3 resp.)) Au centre, puis de l’autre côté. Puis on tourne la tête "
        "lentement : on regarde à droite… à gauche. Petit mouvement. Les épaules descendent, la mâchoire se desserre. "
        "Attention : on ne fait pas de cercles complets avec la tête et on ne tire pas avec la main.")),
    "Hombros": _t((
        "Inhalamos, subimos los hombros. Exhalamos, atrás y abajo. Cinco círculos hacia atrás… cinco hacia delante. Los "
        "brazos sueltos; círculos lentos, al ritmo de la respiración. Sin fuerza: el cuello no se tensa.",
        "On inspire, on monte les épaules. On expire, en arrière et en bas. Cinq cercles vers l’arrière… cinq vers l’avant. "
        "Les bras relâchés ; des cercles lents, au rythme de la respiration. Sans force : le cou ne se crispe pas.")),
    "Nuevo · La cabeza atrás": _t((
        "Espalda larga, mirada al frente. Llevamos la cabeza un poco hacia atrás, sin subir ni bajar la barbilla, como si "
        "hiciéramos una papada. ((2 o 3 segundos)) Soltamos. ((5 veces)) La nuca se alarga. Cuidado: movimiento pequeño; "
        "no miramos hacia arriba y no forzamos.",
        "Dos long, regard devant. On recule un peu la tête, sans lever ni baisser le menton, comme si on faisait un double "
        "menton. ((2 ou 3 secondes)) On relâche. ((5 fois)) La nuque s’allonge. Attention : petit mouvement ; on ne regarde "
        "pas vers le haut et on ne force pas."),
        chair=("Sentados con la espalda larga, la cabeza cerca del respaldo si queremos.",
               "Assis le dos long, la tête près du dossier si on veut."),
        alt=("SU", "Sentados con las piernas cruzadas o estiradas.", "Assis jambes croisées ou allongées.")),
    "Muñecas y tobillos": _t((
        "Círculos con las muñecas, cinco hacia cada lado. Abrimos y cerramos las manos. Después levantamos un poco un pie: "
        "círculos con el tobillo. Cambiamos de pie. Si duelen las articulaciones, el movimiento es más pequeño. Si el pie no "
        "sube, el talón se queda en el suelo y hacemos círculos con la punta.",
        "Cercles avec les poignets, cinq de chaque côté. On ouvre et on ferme les mains. Puis on soulève un peu un pied : "
        "cercles avec la cheville. On change de pied. Si les articulations font mal, le mouvement est plus petit. Si le pied "
        "ne monte pas, le talon reste au sol et on fait des cercles avec la pointe.")),
    "Inclinación lateral": _t((
        "Inhalamos, brazo derecho arriba. Exhalamos, nos inclinamos a la izquierda. ((3 resp.)) Cambiamos. Imaginamos que "
        "estamos entre dos cristales. Si cuesta subir el brazo, la mano en la cabeza o en la cintura. Cuidado: no nos "
        "inclinamos hacia delante; las dos nalgas se quedan apoyadas.",
        "On inspire, bras droit en haut. On expire, on se penche à gauche. ((3 resp.)) On change. On imagine qu’on est entre "
        "deux vitres. Si le bras monte difficilement, la main sur la tête ou à la taille. Attention : on ne se penche pas "
        "vers l’avant ; les deux fesses restent posées."),
        chair=("Antebrazo izquierdo en el reposabrazos.", "Avant-bras gauche sur l’accoudoir."),
        alt=("SU", "Mano izquierda en el suelo, junto a la cadera.", "Main gauche au sol, près de la hanche.")),
    "Círculos del torso": _t((
        "Círculos suaves con el torso: hacia delante, hacia un lado, hacia atrás y al otro lado. ((4 círculos)) Cambiamos de "
        "dirección. ((4 círculos)) Cuidado: no vamos lejos hacia delante ni hacia atrás; la cabeza sigue al torso.",
        "Des cercles doux avec le buste : vers l’avant, sur un côté, vers l’arrière et de l’autre côté. ((4 cercles)) On "
        "change de sens. ((4 cercles)) Attention : on ne va pas loin vers l’avant ni vers l’arrière ; la tête suit le "
        "buste."),
        chair=("Sentados al borde, pies bien apoyados, manos sobre las rodillas.",
               "Assis au bord, pieds bien posés, mains sur les genoux."),
        alt=("SU", "Sentados con las piernas cruzadas, manos sobre las rodillas.",
             "Assis en tailleur, mains sur les genoux.")),
    "Gato-vaca": _t((
        "Inhalamos, abrimos el pecho. Exhalamos, redondeamos **un poco** la espalda. ((5 veces)) Movimiento pequeño, empieza "
        "en la pelvis. Cuidado: no echamos la cabeza atrás y no forzamos la espalda.",
        "On inspire, on ouvre la poitrine. On expire, on arrondit **un peu** le dos. ((5 fois)) Petit mouvement, il commence "
        "dans le bassin. Attention : on ne lance pas la tête en arrière et on ne force pas le dos."),
        chair=("Manos en las rodillas, pies bien apoyados.", "Mains sur les genoux, pieds bien posés."),
        alt=("SU", "A cuatro apoyos, si las rodillas y las muñecas están cómodas: manos debajo de los hombros, rodillas "
             "debajo de las caderas.",
             "À quatre pattes, si les genoux et les poignets sont à l’aise : mains sous les épaules, genoux sous les "
             "hanches.")),
    # ---------------- standing ----------------
    "Guerrero II · recordatorio": _t((
        "La rodilla derecha doblada, encima del tobillo. Inhalamos, brazos en cruz; miramos la mano derecha. ((2 resp.)) "
        "Cuidado: la rodilla no se cae hacia dentro; el torso no se inclina hacia delante; los hombros no suben. " + HIP[0],
        "Le genou droit plié, au-dessus de la cheville. On inspire, bras en croix ; regard sur la main droite. ((2 resp.)) "
        "Attention : le genou ne tombe pas vers l’intérieur ; le buste ne penche pas vers l’avant ; les épaules ne montent "
        "pas. " + HIP[1]),
        intro=("**Estas dos posturas ya las conocemos: el Guerrero II y el Triángulo. Hoy añadimos una nueva entre las dos: "
               "el ángulo lateral. Hacemos las tres seguidas de un lado, y después del otro.**",
               "**Ces deux postures, on les connaît déjà : le Guerrier II et le Triangle. Aujourd’hui on en ajoute une "
               "nouvelle entre les deux : l’angle latéral. On fait les trois à la suite d’un côté, puis de l’autre.**"),
        chair=("Al borde de la silla. La pierna derecha se abre hacia la derecha, delante del reposabrazos; la pierna "
               "izquierda se estira atrás y a la izquierda, el pie apoyado.",
               "Au bord de la chaise. La jambe droite s’ouvre vers la droite, devant l’accoudoir ; la jambe gauche s’allonge "
               "en arrière et à gauche, pied posé."),
        alt=("DP", "Pies separados, pie derecho hacia fuera; una mano en la silla si hace falta.",
             "Pieds écartés, pied droit vers l’extérieur ; une main sur la chaise si besoin."),
        ju=("**Derecha:** pierna derecha abierta, la izquierda atrás… inhalamos, brazos en cruz. → La rodilla mira en la "
            "misma dirección que el pie. ((2 resp.))",
            "**Droite :** jambe droite ouverte, la gauche en arrière… on inspire, bras en croix. → Le genou regarde dans la "
            "même direction que le pied. ((2 resp.))")),
    "Nuevo · Ángulo lateral": _t((
        "Desde el guerrero II. Exhalamos: el antebrazo derecho baja y se apoya en el muslo derecho, sin empujar. Inhalamos: "
        "el brazo izquierdo sube, o la mano se queda en la cintura. Todo el costado izquierdo se alarga. ((2 resp.)) "
        "Inhalamos, subimos con la ayuda de las piernas. Cuidado: el pecho no cae hacia el suelo; el cuello sigue largo; "
        "miramos al frente o al suelo, no hacia arriba si molesta el cuello. " + HIP[0],
        "Depuis le guerrier II. On expire : l’avant-bras droit descend et se pose sur la cuisse droite, sans appuyer. On "
        "inspire : le bras gauche monte, ou la main reste sur la taille. Tout le côté gauche s’allonge. ((2 resp.)) On "
        "inspire, on remonte avec l’aide des jambes. Attention : la poitrine ne tombe pas vers le sol ; le cou reste long ; "
        "on regarde devant ou vers le sol, pas vers le haut si le cou gêne. " + HIP[1]),
        chair=("Seguimos al borde de la silla, en el guerrero II. El antebrazo puede apoyarse en el muslo o en el "
               "reposabrazos.",
               "On reste au bord de la chaise, en guerrier II. L’avant-bras peut se poser sur la cuisse ou sur "
               "l’accoudoir."),
        alt=("DP", "Seguimos en el guerrero II, con la silla cerca de la pierna de delante.",
             "On reste en guerrier II, la chaise près de la jambe avant."),
        ju=("Exhalamos, el antebrazo en el muslo… inhalamos, el brazo sube. → El costado se alarga, como una línea "
            "desde el pie hasta la mano. ((2 resp.))",
            "On expire, l’avant-bras sur la cuisse… on inspire, le bras monte. → Le côté s’allonge, comme une ligne du pied "
            "jusqu’à la main. ((2 resp.))")),
    "Triángulo adaptado · recordatorio": _t((
        "Estiramos un poco la rodilla derecha, sin bloquearla. Exhalamos: nos inclinamos hacia la derecha; la mano derecha "
        "baja entre la cintura y la rodilla, y nunca empuja; el brazo izquierdo sube o se queda en la cintura. ((2 resp.)) "
        "Inhalamos, subimos. Cambiamos de lado: guerrero II, ángulo lateral y triángulo a la izquierda. Cuidado: no "
        "bajamos la mano más de lo cómodo; el cuello sigue largo. " + HIP[0],
        "On allonge un peu le genou droit, sans le bloquer. On expire : on se penche vers la droite ; la main droite descend "
        "entre la taille et le genou, et ne pousse jamais ; le bras gauche monte ou reste sur la taille. ((2 resp.)) On "
        "inspire, on remonte. On change de côté : guerrier II, angle latéral et triangle à gauche. Attention : on ne "
        "descend pas la main plus bas que confortable ; le cou reste long. " + HIP[1]),
        chair=("Al borde de la silla, en la misma posición de piernas. El antebrazo derecho en el muslo o en el "
               "reposabrazos.",
               "Au bord de la chaise, même position des jambes. L’avant-bras droit sur la cuisse ou sur l’accoudoir."),
        alt=("DP", "Las piernas más largas, sin bloquear las rodillas; la silla cerca de la pierna de delante.",
             "Les jambes plus longues, sans bloquer les genoux ; la chaise près de la jambe avant."),
        ju=("Estiramos un poco la rodilla… exhalamos, nos inclinamos. → La mano de abajo descansa, no empuja. ((2 resp.)) "
            "**Izquierda:** guerrero II… ángulo lateral… triángulo. → Hombros lejos de las orejas.",
            "On allonge un peu le genou… on expire, on se penche. → La main du bas se pose, elle ne pousse pas. ((2 resp.)) "
            "**Gauche :** guerrier II… angle latéral… triangle. → Les épaules loin des oreilles.")),
    "Nuevo · El avión": _t((
        "Inhalamos: espalda larga. Exhalamos: el torso se inclina un poco hacia delante, como un avión. ((3 resp.)) "
        "Inhalamos: volvemos despacio. Cambiamos de lado. Cuidado: no arqueamos la espalda baja, no bloqueamos la rodilla de "
        "apoyo y no aguantamos el aire.",
        "On inspire : dos long. On expire : le buste se penche un peu vers l’avant, comme un avion. ((3 resp.)) On inspire : "
        "on revient doucement. On change de côté. Attention : on ne creuse pas le bas du dos, on ne bloque pas le genou "
        "d’appui et on ne retient pas l’air."),
        intro=("**Miramos un punto fijo en el suelo, un poco lejos.**", "**On regarde un point fixe au sol, un peu loin.**"),
        chair=("Al borde, nos inclinamos con la espalda larga, brazos delante. El pie derecho se separa un poco del suelo.",
               "Au bord, on se penche le dos long, bras devant. Le pied droit décolle un peu du sol."),
        alt=("DP", "Las dos manos en el respaldo. El pie izquierdo se desliza hacia atrás; el talón se separa del suelo y "
             "la pierna sube un poco, baja. Los dedos del pie pueden quedarse en el suelo.",
             "Les deux mains sur le dossier. Le pied gauche glisse vers l’arrière ; le talon décolle et la jambe monte un "
             "peu, basse. Les orteils peuvent rester au sol."),
        mc=("Una mano en la silla, o ninguna; brazos delante o en cruz. La pierna de atrás sigue baja.",
            "Une main sur la chaise, ou aucune ; bras devant ou en croix. La jambe arrière reste basse."),
        ju=("**Derecha:** miramos el punto fijo… exhalamos, el torso se inclina. → La rodilla de apoyo un poco blanda. "
            "((3 resp.)) **Izquierda:** igual… → La pierna de atrás larga y baja, el cuello largo.",
            "**Droite :** on regarde le point fixe… on expire, le buste se penche. → Le genou d’appui un peu souple. "
            "((3 resp.)) **Gauche :** pareil… → La jambe arrière longue et basse, le cou long.")),
    # ---------------- floor / chair ----------------
    "Rodilla al pecho": _t((
        "((3 resp.)) Cambiamos de pierna. Cogemos **detrás del muslo**, no la rodilla. Los hombros sueltos. Cuidado: no "
        "tiramos fuerte; si pellizca delante de la cadera, la rodilla se queda más lejos.",
        "((3 resp.)) On change de jambe. On tient **derrière la cuisse**, pas le genou. Les épaules relâchées. Attention : on "
        "ne tire pas fort ; si ça pince devant la hanche, le genou reste plus loin."),
        intro=("**Bajamos al suelo como hemos aprendido: de lado, a cuatro apoyos, una rodilla, las manos en la silla. Quien "
               "prefiere, se queda en la silla.**",
               "**On descend au sol comme on l’a appris : de côté, à quatre pattes, un genou, les mains sur la chaise. Ceux "
               "qui préfèrent restent sur la chaise.**"),
        chair=("Abrazamos la rodilla derecha, espalda larga.", "On serre le genou droit, dos long."),
        alt=("SU", "Tumbados, la rodilla derecha hacia el pecho, el pie izquierdo en el suelo. Una pierna cada vez.",
             "Allongés, le genou droit vers la poitrine, le pied gauche au sol. Une jambe à la fois.")),
    "Nuevo · Talones que se deslizan": _t((
        "Exhalamos: el talón se acerca. Inhalamos: se aleja. ((5 veces)) Cambiamos de pierna. Despacio, sin dolor, solo "
        "hasta donde es cómodo. Cuidado: nada debe tirar fuerte; si pellizca en la ingle, el movimiento es más pequeño.",
        "On expire : le talon se rapproche. On inspire : il s’éloigne. ((5 fois)) On change de jambe. Lentement, sans "
        "douleur, seulement jusqu’où c’est confortable. Attention : rien ne doit tirer fort ; si ça pince dans l’aine, le "
        "mouvement est plus petit."),
        chair=("El pie derecho se desliza por el suelo hacia delante y hacia atrás, el talón en el suelo.",
               "Le pied droit glisse sur le sol vers l’avant et vers l’arrière, le talon au sol."),
        alt=("SU", "Tumbados, una rodilla doblada. El talón de la otra pierna se desliza por el suelo hacia las nalgas y "
             "vuelve.",
             "Allongés, un genou plié. Le talon de l’autre jambe glisse sur le sol vers les fesses et revient.")),
    "Torsión tumbada": _t((
        "((4 resp.)) Cambiamos de lado. Con cada exhalación, soltamos un poco más. Cuidado: no forzamos.",
        "((4 resp.)) On change de côté. À chaque expiration, on relâche un peu plus. Attention : on ne force pas."),
        chair=("Mano izquierda en el reposabrazos derecho. Inhalamos: espalda larga. Exhalamos: giramos suavemente a la "
               "derecha.",
               "Main gauche sur l’accoudoir droit. On inspire : dos long. On expire : on tourne doucement vers la droite."),
        alt=("SU", "Tumbados, brazos en cruz: rodillas juntas a la derecha, la cabeza puede mirar a la izquierda. Los "
             "hombros se quedan apoyados; si las rodillas no llegan al suelo, se quedan a medio camino.",
             "Allongés, bras en croix : genoux serrés à droite, la tête peut regarder à gauche. Les épaules restent "
             "posées ; si les genoux n’arrivent pas au sol, ils restent à mi-chemin.")),
    "La banana": _t((
        "Se estira el lado derecho. ((4 resp.)) Cambiamos. Cuidado: no giramos la pelvis y no arqueamos la espalda.",
        "Le côté droit s’étire. ((4 resp.)) On change. Attention : on ne tourne pas le bassin et on ne creuse pas le dos."),
        chair=("Mano izquierda en el reposabrazos, brazo derecho arriba. Exhalamos: nos inclinamos hacia la izquierda.",
               "Main gauche sur l’accoudoir, bras droit en haut. On expire : on s’incline vers la gauche."),
        alt=("SU", "Tumbados, brazos por encima de la cabeza. Llevamos los pies y las manos un poco hacia la izquierda: el "
             "cuerpo hace una banana. Si los hombros no suben, los brazos doblados o las manos en la cabeza.",
             "Allongés, bras au-dessus de la tête. On emmène les pieds et les mains un peu vers la gauche : le corps fait "
             "une banane. Si les épaules ne montent pas, les bras pliés ou les mains sur la tête.")),
    "Nuevo · Piernas en la silla": _t((
        "Brazos sueltos, palmas hacia arriba. Respiramos tranquilos. ((5 resp.)) Nada debe tirar: es descanso. Podemos "
        "quedarnos así para la relajación.",
        "Bras relâchés, paumes vers le haut. On respire tranquillement. ((5 resp.)) Rien ne doit tirer : c’est du repos. "
        "On peut rester comme ça pour la relaxation."),
        chair=("Nos sentamos atrás, la espalda en el respaldo, los pies en el suelo.",
               "On s’assoit au fond, le dos contre le dossier, les pieds au sol."),
        alt=("SU", "Tumbados, las pantorrillas sobre el asiento de la silla. Si no es cómodo, rodillas dobladas y pies en "
             "el suelo.",
             "Allongés, les mollets sur l’assise de la chaise. Si ce n’est pas confortable, genoux pliés et pieds au "
             "sol.")),
    "Descanso: el niño": _t((
        "((5 resp.)) Respiramos hacia la espalda. Cuidado: no forzamos.",
        "((5 resp.)) On respire vers le dos. Attention : on ne force pas."),
        chair=("Pies separados, manos en los muslos. Nos inclinamos un poco, espalda larga, y descansamos. Subimos "
               "despacio.",
               "Pieds écartés, mains sur les cuisses. On se penche un peu, dos long, et on se repose. On remonte "
               "doucement."),
        alt=("SU", "Rodillas en el suelo, separadas; caderas hacia los talones. Si molestan las rodillas o las caderas, "
             "mejor en la silla.",
             "Genoux au sol, écartés ; hanches vers les talons. Si les genoux ou les hanches gênent, plutôt sur la "
             "chaise.")),
    "Relajación": _t((
        "Cerramos los ojos. Con cada exhalación, el cuerpo pesa un poco más: los pies… las piernas… los brazos… los "
        "hombros… la cara. ((5 minutos de silencio)) [T] Movemos los dedos, abrimos los ojos. Para levantarnos, despacio: "
        "de lado, esperamos una respiración, y después nos sentamos.",
        "On ferme les yeux. À chaque expiration, le corps devient un peu plus lourd : les pieds… les jambes… les bras… les "
        "épaules… le visage. ((5 minutes de silence)) [T] On bouge les doigts, on ouvre les yeux. Pour se relever, "
        "doucement : sur le côté, on attend une respiration, puis on s’assoit."),
        chair=("Nos sentamos atrás, espalda en el respaldo, antebrazos en los reposabrazos o manos en los muslos, palmas "
               "hacia arriba. Pies en el suelo.",
               "On s’assoit au fond, dos contre le dossier, avant-bras sur les accoudoirs ou mains sur les cuisses, paumes "
               "vers le haut. Pieds au sol."),
        alt=("SU", "Tumbados boca arriba, las piernas en la silla o las rodillas dobladas.",
             "Allongés sur le dos, les jambes sur la chaise ou les genoux pliés.")),
}


TEXTS["Nuevo · Abrazo y apertura"] = _t((
    "Inhalamos: abrimos los brazos a los lados, el pecho se abre, los omóplatos se acercan. Exhalamos: nos abrazamos, las "
    "manos en los hombros; la espalda alta se ensancha. ((5 veces)) Despacio, con la respiración. Igual en la silla o "
    "sentados en el suelo. Cuidado: no echamos la cabeza atrás; los brazos se abren solo hasta donde es cómodo.",
    "On inspire : on ouvre les bras sur les côtés, la poitrine s’ouvre, les omoplates se rapprochent. On expire : on se "
    "fait un câlin, les mains sur les épaules ; le haut du dos s’élargit. ((5 fois)) Lentement, avec la respiration. Pareil "
    "sur la chaise ou assis au sol. Attention : on ne lance pas la tête en arrière ; les bras s’ouvrent seulement jusqu’où "
    "c’est confortable."))
TEXTS["Balanceo de la pelvis"] = _t((
    "Exhalamos: la espalda baja se redondea un poco. Inhalamos: se arquea un poco. ((6 veces)) Movimiento pequeño y lento. "
    "Cuidado: no empujamos con fuerza.",
    "On expire : le bas du dos s’arrondit un peu. On inspire : il se creuse un peu. ((6 fois)) Petit mouvement, lent. "
    "Attention : on ne pousse pas avec force."),
    intro=("**Bajamos al suelo como hemos aprendido: de lado, a cuatro apoyos, una rodilla, las manos en la silla. Quien "
           "prefiere, se queda en la silla.**",
           "**On descend au sol comme on l’a appris : de côté, à quatre pattes, un genou, les mains sur la chaise. Ceux qui "
           "préfèrent restent sur la chaise.**"),
    chair=("Sentados, manos en las rodillas.", "Assis, mains sur les genoux."),
    alt=("SU", "Tumbados, rodillas dobladas, pies separados como las caderas. Al exhalar, la espalda baja se apoya en el "
         "suelo.",
         "Allongés, genoux pliés, pieds écartés largeur de hanches. À l’expiration, le bas du dos se pose au sol."))
TEXTS["Nuevo · Ángel en el suelo"] = _t((
    "Inhalamos: los brazos se deslizan hacia arriba, despacio, solo hasta donde es cómodo. Exhalamos: bajan. ((5 veces)) "
    "Si molesta un hombro, el movimiento es más pequeño, o las manos descansan sobre el vientre. Cuidado: la espalda baja "
    "no se arquea.",
    "On inspire : les bras glissent vers le haut, lentement, seulement jusqu’où c’est confortable. On expire : ils "
    "redescendent. ((5 fois)) Si une épaule gêne, le mouvement est plus petit, ou les mains se posent sur le ventre. "
    "Attention : le bas du dos ne se creuse pas."),
    chair=("Sentados, la espalda en el respaldo, brazos en cactus: codos a la altura de los hombros.",
           "Assis, le dos contre le dossier, bras en cactus : coudes à hauteur d’épaules."),
    alt=("SU", "Tumbados, rodillas dobladas, brazos en cactus en el suelo, el dorso de las manos apoyado; los brazos se "
         "deslizan por el suelo, como un ángel en la nieve.",
         "Allongés, genoux pliés, bras en cactus au sol, le dos des mains posé ; les bras glissent sur le sol, comme un ange "
         "dans la neige."))
TEXTS["Nuevo · La almeja"] = _t((
    "Exhalamos al abrir, inhalamos al cerrar. ((8 veces)) Despacio. Cuidado: la pelvis no gira hacia atrás; el movimiento "
    "es pequeño.",
    "On expire en ouvrant, on inspire en fermant. ((8 fois)) Lentement. Attention : le bassin ne tourne pas vers l’arrière ; "
    "le mouvement est petit."),
    chair=("Sentados al borde, rodillas juntas, manos por fuera de las rodillas. Abrimos un poco las rodillas; las manos "
           "frenan suavemente.",
           "Assis au bord, genoux serrés, mains à l’extérieur des genoux. On ouvre un peu les genoux ; les mains freinent "
           "doucement."),
    alt=("SU", "Tumbados sobre el lado izquierdo, rodillas dobladas, la cabeza sobre el brazo. Los pies juntos; la rodilla "
         "de arriba sube un poco, como una almeja que se abre, y baja. Después, el otro lado. Luego nos tumbamos boca "
         "arriba.",
         "Allongés sur le côté gauche, genoux pliés, la tête sur le bras. Les pieds joints ; le genou du dessus monte un "
         "peu, comme un coquillage qui s’ouvre, et redescend. Puis l’autre côté. Ensuite on s’allonge sur le dos."))
TEXTS["Torsión tumbada"]["alt"] = ("SU", TEXTS["Torsión tumbada"]["alt"][1] + " Luego nos ponemos sobre el lado izquierdo.",
                                   TEXTS["Torsión tumbada"]["alt"][2] + " Puis on se met sur le côté gauche.")
TEXTS["Rodilla al pecho"]["intro"] = None
TEXTS["Relajación"]["alt"] = ("SU", "Tumbados boca arriba; si es más cómodo, rodillas dobladas.",
                              "Allongés sur le dos ; si c’est plus confortable, genoux pliés.")

SE = {
    "Cuello": ("Sirve para soltar la tensión del cuello. ✓ Tira suavemente en el lado del cuello. ✗ No debe doler ni marear.",
               "Sert à relâcher la tension du cou. ✓ Ça tire doucement sur le côté du cou. ✗ Ça ne doit pas faire mal ni donner "
               "le vertige."),
    "Hombros": ("Sirve para soltar los hombros. ✓ Calor y movimiento en los hombros. ✗ Dolor en el cuello.",
                "Sert à relâcher les épaules. ✓ Chaleur et mouvement dans les épaules. ✗ Douleur dans le cou."),
    "Nuevo · Abrazo y apertura": ("Sirve para abrir el pecho y estirar la espalda alta. ✓ Al abrir, se estira el pecho; al "
                                  "abrazar, entre los omóplatos. ✗ Pinchazo en los hombros.",
                                  "Sert à ouvrir la poitrine et étirer le haut du dos. ✓ En ouvrant, la poitrine s’étire ; "
                                  "en se faisant un câlin, entre les omoplates. ✗ Piqûre dans les épaules."),
    "Nuevo · La cabeza atrás": ("Sirve para alargar la nuca y ayudar a la espalda a estar más recta. ✓ Se alarga la parte "
                                "de atrás del cuello. ✗ Dolor en la garganta o mareo.",
                                "Sert à allonger la nuque et aider le dos à se redresser. ✓ L’arrière du cou s’allonge. "
                                "✗ Douleur dans la gorge ou vertige."),
    "Muñecas y tobillos": ("Sirve para mover las articulaciones; los tobillos ágiles ayudan al equilibrio. ✓ Movimiento "
                           "suave. ✗ Dolor en la articulación: más pequeño.",
                           "Sert à bouger les articulations ; des chevilles souples aident l’équilibre. ✓ Mouvement doux. "
                           "✗ Douleur dans l’articulation : plus petit."),
    "Inclinación lateral": ("Sirve para estirar los costados y respirar mejor. ✓ Tira en el costado. ✗ Cuello, espalda baja.",
                            "Sert à étirer les côtés et mieux respirer. ✓ Ça tire sur le côté. ✗ Cou, bas du dos."),
    "Círculos del torso": ("Sirve para mover la columna en todas las direcciones. ✓ Movimiento suave en la espalda. "
                           "✗ Mareo o dolor en la espalda baja.",
                           "Sert à bouger la colonne dans toutes les directions. ✓ Mouvement doux dans le dos. ✗ Vertige "
                           "ou douleur dans le bas du dos."),
    "Gato-vaca": ("Sirve para dar flexibilidad a la columna. ✓ Movimiento en toda la espalda. ✗ Pellizco en la espalda baja "
                  "o en el cuello.",
                  "Sert à assouplir la colonne. ✓ Mouvement dans tout le dos. ✗ Pincement dans le bas du dos ou dans le cou."),
    "Guerrero II · recordatorio": ("Sirve para fortalecer las piernas y abrir el pecho. ✓ Trabajo, calor en los muslos. "
                                   "✗ Rodilla, ingle que pellizca.",
                                   "Sert à muscler les jambes et ouvrir la poitrine. ✓ Travail, chaleur dans les cuisses. "
                                   "✗ Genou, aine qui pince."),
    "Nuevo · Ángulo lateral": ("Sirve para estirar todo el costado y fortalecer las piernas. ✓ Tira en el costado de "
                               "arriba. ✗ Ingle, rodilla, espalda baja, cuello.",
                               "Sert à étirer tout le côté et muscler les jambes. ✓ Ça tire sur le côté du haut. ✗ Aine, "
                               "genou, bas du dos, cou."),
    "Triángulo adaptado · recordatorio": ("Sirve para estirar el costado y la parte interior de las piernas. ✓ Costado e "
                                          "interior del muslo, suave. ✗ Rodilla, ingle, cuello.",
                                          "Sert à étirer le côté et l’intérieur des jambes. ✓ Côté et intérieur de la "
                                          "cuisse, doucement. ✗ Genou, aine, cou."),
    "Nuevo · El avión": ("Sirve para entrenar el equilibrio y fortalecer los tobillos y las piernas: ayuda a evitar caídas. "
                         "✓ Trabajo en el tobillo y la pierna de apoyo. ✗ Espalda baja.",
                         "Sert à entraîner l’équilibre et muscler les chevilles et les jambes : ça aide à éviter les "
                         "chutes. ✓ Travail dans la cheville et la jambe d’appui. ✗ Bas du dos."),
    "Balanceo de la pelvis": ("Sirve para mover la espalda baja con suavidad. ✓ Movimiento pequeño en la espalda baja. "
                              "✗ Dolor en la espalda.",
                              "Sert à bouger le bas du dos en douceur. ✓ Petit mouvement dans le bas du dos. ✗ Douleur "
                              "dans le dos."),
    "Rodilla al pecho": ("Sirve para relajar la espalda baja. ✓ Glúteo y espalda baja, suave. ✗ Pellizco delante de la "
                         "cadera, rodilla.",
                         "Sert à relâcher le bas du dos. ✓ Fesse et bas du dos, doucement. ✗ Pincement devant la hanche, "
                         "genou."),
    "Nuevo · Talones que se deslizan": ("Sirve para mover la cadera y la rodilla sin forzar. ✓ Movimiento libre, sin tirar. "
                                        "✗ Pellizco en la ingle.",
                                        "Sert à bouger la hanche et le genou sans forcer. ✓ Mouvement libre, sans tirer. "
                                        "✗ Pincement dans l’aine."),
    "Nuevo · Ángel en el suelo": ("Sirve para abrir el pecho y los hombros, y enderezar la espalda. ✓ Tira suavemente en "
                                  "el pecho y los hombros. ✗ Pinchazo en el hombro: más pequeño.",
                                  "Sert à ouvrir la poitrine et les épaules, et redresser le dos. ✓ Ça tire doucement dans "
                                  "la poitrine et les épaules. ✗ Piqûre dans l’épaule : plus petit."),
    "La banana": ("Sirve para estirar todo el costado. ✓ El costado, de los pies a las manos. ✗ Espalda baja.",
                  "Sert à étirer tout le côté. ✓ Le côté, des pieds aux mains. ✗ Bas du dos."),
    "Torsión tumbada": ("Sirve para relajar la espalda. ✓ Espalda, glúteo, pecho. ✗ Espalda baja u hombro que pellizca.",
                        "Sert à détendre le dos. ✓ Dos, fesse, poitrine. ✗ Bas du dos ou épaule qui pince."),
    "Nuevo · La almeja": ("Sirve para fortalecer el lado de la cadera: ayuda a caminar con más estabilidad. ✓ Trabajo, "
                          "calor en el lado del glúteo. ✗ Dolor en la cadera o en la espalda baja: más pequeño.",
                          "Sert à muscler le côté de la hanche : ça aide à marcher avec plus de stabilité. ✓ Travail, "
                          "chaleur sur le côté de la fesse. ✗ Douleur dans la hanche ou le bas du dos : plus petit."),
    "Descanso: el niño": ("Sirve para descansar la espalda. ✓ La espalda se suelta. ✗ Rodillas o caderas.",
                          "Sert à reposer le dos. ✓ Le dos se relâche. ✗ Genoux ou hanches."),
}
for _k, _v in SE.items():
    TEXTS[_k]["se"] = _v


def _with_text(args, kw):
    a = list(args)
    name = a[3][0] if len(a) > 3 else None
    if name in TEXTS:
        t = (_build(TEXTS[name], 0), _build(TEXTS[name], 1))
        if len(a) > 5:
            a[5] = t
        else:
            kw["text"] = t
    return a, kw


SUN_SEAT = [
    ("chair_sit", ("1 Corazón", "1 Cœur"), "exh"), ("silla_c", ("2 Silla invisible", "2 Chaise invisible"), "inh"),
    ("c_hinge", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("w1_chair_prep", ("5 Pierna I atrás", "5 Jambe G arrière"), "exh"),
    ("w1_chair", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("chair_sit", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STAND = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("silla_p", ("2 Silla invisible", "2 Chaise invisible"), "inh"),
    ("hinge", ("3 Flexión", "3 Flexion"), "exh"), (("dog_chair", "half_lift_thighs"), ("4 Espalda larga", "4 Dos long"), "inh"),
    ("lunge_chair_L", ("5 Pie I atrás", "5 Pied G arrière"), "exh"),
    ("w1_stand", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("heart_chair", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_STEPS = [
    (1, ("**Corazón.** Espalda larga, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Dos long, paumes jointes devant la poitrine. On expire.")),
    (2, ("**NUEVO EN EL SALUDO · La silla invisible.** Inhalamos: subimos los brazos. "
         "[C]Al borde de la silla, nos inclinamos un poco hacia delante con la espalda larga, como para levantarnos.[/C] "
         "[DP]Doblamos las rodillas y llevamos las caderas hacia atrás, como para sentarnos en una silla que no está. Poco. "
         "El peso en los talones, las rodillas en la dirección de los pies. La silla de verdad detrás, por seguridad.[/DP] "
         "[TO]Si cuesta subir los brazos: brazos delante o manos en los muslos. Cuidado: no bajamos mucho; si molestan las "
         "rodillas, menos.[/TO] [SE]Sirve para fortalecer los muslos y los glúteos: levantarnos de una silla, subir "
         "escaleras. ✓ Calor en los muslos. ✗ Dolor en las rodillas.[/SE]",
         "**NOUVEAU DANS LA SALUTATION · La chaise invisible.** On inspire : on monte les bras. "
         "[C]Au bord de la chaise, on se penche un peu vers l’avant le dos long, comme pour se lever.[/C] "
         "[DP]On plie les genoux et on recule les hanches, comme pour s’asseoir sur une chaise qui n’est pas là. Peu. Le "
         "poids sur les talons, les genoux dans la direction des pieds. La vraie chaise derrière, par sécurité.[/DP] "
         "[TO]Si les bras montent difficilement : bras devant ou mains sur les cuisses. Attention : on ne descend pas "
         "beaucoup ; si les genoux gênent, moins.[/TO] [SE]Sert à muscler les cuisses et les fesses : se lever d’une chaise, "
         "monter les escaliers. ✓ Chaleur dans les cuisses. ✗ Douleur dans les genoux.[/SE]")),
    (3, ("**Flexión.** Exhalamos: rodillas un poco dobladas, nos inclinamos **desde las caderas**; las manos resbalan por "
         "los muslos. La espalda larga. Cuidado: si hay vértigo, la cabeza no baja más que el corazón. "
         "[SE]Sirve para estirar la espalda y la parte de atrás de las piernas. ✓ Tira detrás de los muslos. ✗ Pinchazo en la "
         "espalda baja o en las rodillas.[/SE] [MC]Si estamos cómodos, soltamos más: la cabeza y los brazos cuelgan.[/MC]",
         "**Flexion.** On expire : genoux légèrement pliés, on se penche **depuis les hanches** ; les mains glissent sur "
         "les cuisses. Le dos long. Attention : en cas de vertige, la tête ne descend pas plus bas que le cœur. "
         "[SE]Sert à étirer le dos et l’arrière des jambes. ✓ Ça tire derrière les cuisses. ✗ Piqûre dans le bas du dos ou les "
         "genoux.[/SE] [MC]Si on est à l’aise, on relâche davantage : la tête et les bras pendent.[/MC]")),
    (4, ("**Espalda larga.** Inhalamos: subimos un poco, la espalda plana como una mesa, el cuello largo. "
         "[DP]Manos en el respaldo, o en los muslos.[/DP]",
         "**Dos long.** On inspire : on remonte un peu, le dos plat comme une table, le cou long. "
         "[DP]Mains sur le dossier, ou sur les cuisses.[/DP]")),
    (5, ("**Pierna izquierda atrás.** Exhalamos. [C]Giramos un poco en la silla; la pierna izquierda va atrás, al lado de "
         "la silla, la punta del pie apoyada.[/C] [DP]El pie izquierdo da un paso atrás, pies como sobre dos raíles; una "
         "mano en la silla.[/DP] [TO]Las caderas miran hacia delante.[/TO]",
         "**Jambe gauche en arrière.** On expire. [C]On tourne un peu sur la chaise ; la jambe gauche va en arrière, à côté "
         "de la chaise, la pointe du pied posée.[/C] [DP]Le pied gauche recule d’un pas, pieds comme sur deux rails ; une "
         "main sur la chaise.[/DP] [TO]Les hanches regardent devant.[/TO]")),
    (6, ("**Guerrero I.** Inhalamos: subimos los brazos, o uno solo si la otra mano está en la silla. ((2 resp.)) "
         "[SE]Sirve para fortalecer las piernas y estirar la parte delantera de la cadera. ✓ Tira delante de la cadera de la "
         "pierna de atrás. ✗ Rodilla de delante, espalda baja.[/SE]",
         "**Guerrier I.** On inspire : on monte les bras, ou un seul si l’autre main est sur la chaise. ((2 resp.)) "
         "[SE]Sert à muscler les jambes et étirer l’avant de la hanche. ✓ Ça tire devant la hanche de la jambe arrière. "
         "✗ Genou avant, bas du dos.[/SE]")),
    (7, ("**Corazón.** Exhalamos: bajamos los brazos, la pierna vuelve, manos delante del pecho. ((1 resp.))",
         "**Cœur.** On expire : on descend les bras, la jambe revient, mains devant la poitrine. ((1 resp.))")),
]

BENEFITS = [
    ("☀", ("**Saludo al sol:** calienta todo el cuerpo, mueve la columna y une el movimiento con la respiración.",
           "**Salutation au soleil :** réchauffe tout le corps, bouge la colonne et relie le mouvement à la respiration.")),
    ("1", ("**La silla invisible (nueva):** fortalece los muslos y los glúteos; es lo que usamos para levantarnos de una "
           "silla o subir escaleras. ✓ Trabajo en los muslos. ✗ Dolor en las rodillas.",
           "**La chaise invisible (nouvelle) :** muscle les cuisses et les fesses ; c’est ce qu’on utilise pour se lever "
           "d’une chaise ou monter les escaliers. ✓ Travail dans les cuisses. ✗ Douleur dans les genoux.")),
    ("2", ("**La flexión:** estira la espalda y la parte de atrás de las piernas; nos enseña a agacharnos sin hacernos "
           "daño. ✓ Tira detrás de los muslos. ✗ Pinchazo en la espalda baja o en las rodillas.",
           "**La flexion :** étire le dos et l’arrière des jambes ; elle apprend à se pencher sans se faire mal. ✓ Ça tire "
           "derrière les cuisses. ✗ Piqûre dans le bas du dos ou dans les genoux.")),
    ("3", ("**Guerrero I:** fortalece las piernas y estira la parte delantera de la cadera, que se acorta al estar mucho "
           "sentados. ✓ Tira delante de la cadera de la pierna de atrás. ✗ Rodilla de delante, espalda baja.",
           "**Guerrier I :** muscle les jambes et étire l’avant de la hanche, qui se raccourcit quand on est beaucoup "
           "assis. ✓ Ça tire devant la hanche de la jambe arrière. ✗ Genou avant, bas du dos.")),
    ("4", ("**Guerrero II, ángulo lateral (nuevo) y triángulo:** fortalecen las piernas y estiran todo el costado. "
           "✓ Trabajo en los muslos, tira en el costado. ✗ Rodilla, ingle que pellizca, cuello.",
           "**Guerrier II, angle latéral (nouveau) et triangle :** musclent les jambes et étirent tout le côté. ✓ Travail "
           "dans les cuisses, ça tire sur le côté. ✗ Genou, aine qui pince, cou.")),
    ("5", ("**El avión (nuevo):** fortalece los tobillos y las piernas, y entrena el equilibrio para evitar caídas. "
           "✓ Trabajo en el tobillo y la pierna de apoyo. ✗ Espalda baja.",
           "**L’avion (nouveau) :** muscle les chevilles et les jambes, et entraîne l’équilibre pour éviter les chutes. "
           "✓ Travail dans la cheville et la jambe d’appui. ✗ Bas du dos.")),
    ("6", ("**Al final, en el suelo o en la silla:** la rodilla al pecho y los talones que se deslizan (nuevo) relajan la "
           "espalda baja y mueven la cadera con suavidad; la torsión y la banana sueltan la espalda y el costado; las "
           "piernas en la silla (nuevo) son descanso. ✓ Estiramiento suave. ✗ Pellizco delante de la cadera.",
           "**À la fin, au sol ou sur la chaise :** le genou poitrine et les talons qui glissent (nouveau) relâchent le bas "
           "du dos et bougent la hanche en douceur ; la torsion et la banane détendent le dos et le côté ; les jambes sur "
           "la chaise (nouveau), c’est du repos. ✓ Étirement doux. ✗ Pincement devant la hanche.")),
]

P_ALL = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 4 · guion de la profesora · 1 hora · de pie, en la silla o en el suelo" if L == "es"
     else "Cours 4 · version française · même ordre que la version espagnole") +
    '</div><h1>' + ("Yoga suave · cada uno a su manera" if L == "es" else "Yoga doux · chacun à sa façon") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="fl lc">SILLA</span> <span class="fl lp">DE PIE CON APOYO</span> <span class="fl lf">SUELO</span> <span class="fl lx">MÁS COMPLETO</span>'
     if L == "es" else
     '<span class="fl lc">CHAISE</span> <span class="fl lp">DEBOUT AVEC APPUI</span> <span class="fl lf">SOL</span> <span class="fl lx">PLUS COMPLET</span>') +
    '</div></div>',
    band(1, ("Bienvenida · un consejo", "Accueil · une astuce"), "0:00 – 0:04"),
    grid([card2("chair_sit", "c_lean", "S", ("Bienvenida · sentarse y levantarse bien", "Accueil · bien s’asseoir et se lever"), None, (
        "Hola a todos, bienvenidos de nuevo. Como siempre: cada uno elige su opción, **no forzamos nunca** y respiramos a "
        "nuestro ritmo. Si algo tira suavemente, está bien; si pincha o duele en una articulación, salimos un poco. "
        "**Hoy, un consejo:** sentados, sobre los dos huesos de las nalgas, los pies planos. Para levantarnos: los pies un "
        "poco atrás, la nariz por encima de los pies, empujamos con los pies y las manos. Y cambiamos de posición despacio: "
        "esperamos una respiración antes de levantarnos.",
        "Bonjour à tous, rebienvenue. Comme toujours : chacun choisit son option, **on ne force jamais** et on respire à son "
        "rythme. Si ça tire doucement, c’est bien ; si ça pique ou fait mal dans une articulation, on sort un peu. "
        "**Aujourd’hui, une astuce :** assis, sur les deux os des fesses, les pieds à plat. Pour se lever : les pieds un peu "
        "en arrière, le nez au-dessus des pieds, on pousse avec les pieds et les mains. Et on change de position "
        "lentement : on attend une respiration avant de se lever."))], cols=1),
    band(2, ("Respiración", "Respiration"), "0:04 – 0:11"),
    grid([
        card2("r_chair", "r_floor", "F", ("Respiración en tres partes", "Respiration en trois parties"), ("5 resp.", "5 resp."), (
            "Cerramos los ojos si queréis. Una mano en el abdomen. Inhalamos: el abdomen y las costillas se expanden "
            "suavemente… el pecho se abre un poco. Exhalamos despacio y todo vuelve. Sin forzar, a vuestro ritmo. "
            "((5 respiraciones))",
            "On ferme les yeux si vous voulez. Une main sur le ventre. On inspire : le ventre et les côtes s’ouvrent "
            "doucement… la poitrine s’ouvre un peu. On expire lentement et tout revient. Sans forcer, à votre rythme. "
            "((5 respirations))")),
        card2("c_breath", "arms_up", "P", ("Brazos y respiración", "Bras et respiration"), ("5 veces", "5 fois"), (
            "Inhalamos por la nariz y abrimos o subimos los brazos, despacio. Exhalamos y los bajamos lentamente. El "
            "movimiento dura lo mismo que la respiración. ((5 veces)) Los brazos suben solo hasta donde es cómodo.",
            "On inspire par le nez et on ouvre ou on monte les bras, lentement. On expire et on les redescend lentement. Le "
            "mouvement dure autant que la respiration. ((5 fois)) Les bras montent seulement jusqu’où c’est confortable.")),
    ]),
    band(3, ("Calentamiento · en la silla o en el suelo", "Échauffement · sur la chaise ou au sol"), "0:11 – 0:22"),
    grid([
        card2("c_neck", "seated_neck", "F", ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("c_shoulders", "seated_shoulders", "F", ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), ("", "")),
        card2("open_c", "hug_chair", "S", ("Nuevo · Abrazo y apertura", "Nouveau · S’ouvrir et se faire un câlin"), ("5 veces", "5 fois"), ("", ""), a_kind="S"),
        card2("chin_c", "chin_f", "F", ("Nuevo · La cabeza atrás", "Nouveau · La tête en arrière"), ("5 veces", "5 fois"), ("", "")),
        card2("c_wrists", "wrists", "F", ("Muñecas y tobillos", "Poignets et chevilles"), ("5 + 5", "5 + 5"), ("", "")),
        card2("c_side_R", "sidebend_R", "F", ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("tcircles_c", "tcircles_f", "F", ("Círculos del torso", "Cercles du buste"), ("4 + 4", "4 + 4"), ("", "")),
        card2("chair_cat", "cat", "F", ("Gato-vaca", "Chat-vache"), ("5 veces", "5 fois"), ("", "")),
    ], cols=3),
    part(1, "De pie o en la silla · 0:22 – 0:44", "Debout ou sur la chaise · 0:22 – 0:44"),
    say("Recordad: **primero os enseño la postura paso a paso y vosotros miráis; después la hacemos juntos**, despacio, "
        "con la respiración.",
        "Rappel : **d’abord je vous montre la posture étape par étape et vous regardez ; ensuite on la fait ensemble**, "
        "doucement, avec la respiration."),
    '<div class="keep2">',
    band(5, ("Saludo al sol · con la silla invisible y el guerrero I · 3 rondas, la tercera opcional",
             "Salutation au soleil · avec la chaise invisible et le guerrier I · 3 rondes, la troisième facultative"), "0:22 – 0:31"),
    say("Primero mirad: os enseño el saludo entero, paso a paso. Después lo hacemos juntos.",
        "D’abord regardez : je vous montre la salutation entière, étape par étape. Ensuite on la fait ensemble."),
    '<div class="sl2">' + ("SENTADOS" if L == "es" else "ASSIS") + '</div>' + strip(SUN_SEAT, 0.13) +
    '<div class="sl2">' + ("DE PIE" if L == "es" else "DEBOUT") + '</div>' + strip(SUN_STAND, 0.13),
    '</div>',
    steps(SUN_STEPS),
    '<div class="keep2">',
    say("**Ahora juntos · 3 rondas** · menos palabras, un consejo por ronda:",
        "**Maintenant ensemble · 3 rondes** · moins de mots, un conseil par ronde :"),
    steps([
        ("R1", ("**Pierna izquierda atrás.** Corazón… inhalamos, silla invisible… exhalamos, flexión… inhalamos, espalda "
                "larga… exhalamos, la pierna izquierda atrás… inhalamos, guerrero I. → En la silla invisible, el peso en "
                "los talones. ((2 resp.)) Corazón.",
                "**Jambe gauche en arrière.** Cœur… on inspire, chaise invisible… on expire, flexion… on inspire, dos long… "
                "on expire, la jambe gauche en arrière… on inspire, guerrier I. → Dans la chaise invisible, le poids sur "
                "les talons. ((2 resp.)) Cœur.")),
        ("R2", ("**Pierna derecha atrás.** Corazón… silla… flexión… espalda larga… la pierna derecha atrás… guerrero I. "
                "→ Las caderas miran hacia delante. ((2 resp.)) Corazón.",
                "**Jambe droite en arrière.** Cœur… chaise… flexion… dos long… la jambe droite en arrière… guerrier I. → Les "
                "hanches regardent devant. ((2 resp.)) Cœur.")),
        ("R3", ("**Opcional · pierna izquierda.** A vuestro ritmo, un movimiento con cada respiración. → Hombros lejos de "
                "las orejas. Corazón.",
                "**Facultative · jambe gauche.** À votre rythme, un mouvement par respiration. → Les épaules loin des "
                "oreilles. Cœur.")),
    ]),
    '</div>',
    '<div class="keep2">',
    band(6, ("Guerrero II → ángulo lateral (nuevo) → triángulo", "Guerrier II → angle latéral (nouveau) → triangle"), "0:31 – 0:40"),
    say("Primero os enseño las tres seguidas, de un lado. Después las hacemos juntos: derecha, y luego izquierda.",
        "D’abord je vous montre les trois à la suite, d’un côté. Ensuite on les fait ensemble : à droite, puis à gauche."),
    grid([
        card2("c_w2_R", "w2c_R", "P", ("Guerrero II · recordatorio", "Guerrier II · rappel"), ("2 resp./lado", "2 resp./côté"), ("", "")),
        card2("c_sa_R", "sac_R", "P", ("Nuevo · Ángulo lateral", "Nouveau · Angle latéral"), ("2 resp./lado", "2 resp./côté"), ("", "")),
        card2("t_chair", "t_stand", "P", ("Triángulo adaptado · recordatorio", "Triangle adapté · rappel"), ("2 resp./lado", "2 resp./côté"), ("", "")),
    ], cols=3),
    '</div>',
    '<div class="keep2">',
    band(7, ("Equilibrio · el avión (nuevo)", "Équilibre · l’avion (nouveau)"), "0:40 – 0:44"),
    say("Primero os enseño los tres niveles; cada uno elige el suyo. Después lo hacemos juntos.",
        "D’abord je vous montre les trois niveaux ; chacun choisit le sien. Ensuite on le fait ensemble."),
    grid([card3("avion_c", "avion_p", "avion_f", ("Nuevo · El avión", "Nouveau · L’avion"), ("3 resp./lado", "3 resp./côté"),
                ("", ""))], cols=1),
    '</div>',
    part(2, "En la silla o en el suelo · 0:44 – 1:00", "Sur la chaise ou au sol · 0:44 – 1:00"),
    band(8, ("Estiramientos suaves · caderas y espalda", "Étirements doux · hanches et dos"), "0:44 – 0:51"),
    grid([
        card2("chair_cat", "pelvis_f", "F", ("Balanceo de la pelvis", "Bascule du bassin"), ("6 veces", "6 fois"), ("", "")),
        card2("chair_knee", "knee1_f", "F", ("Rodilla al pecho", "Genou poitrine"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("heel_c", "heel_f", "F", ("Nuevo · Talones que se deslizan", "Nouveau · Talons qui glissent"), ("5 veces/lado", "5 fois/côté"), ("", "")),
        card2("cactus_c", "cactus_f", "F", ("Nuevo · Ángel en el suelo", "Nouveau · L’ange au sol"), ("5 veces", "5 fois"), ("", "")),
        card2("c_side_R", "banana_f", "F", ("La banana", "La banane"), ("4 resp./lado", "4 resp./côté"), ("", "")),
        card2("c_twist", "twist_R", "F", ("Torsión tumbada", "Torsion allongée"), ("4 resp./lado", "4 resp./côté"), ("", "")),
        card2("d_chair", "clam_f", "F", ("Nuevo · La almeja", "Nouveau · La coquille"), ("8 veces/lado", "8 fois/côté"), ("", "")),
        opt(card2("child_chair", "child", "F", ("Descanso: el niño", "Repos : l’enfant"), ("5 resp.", "5 resp."), ("", ""))),
    ], cols=3),
    band(9, ("Relajación · 5 minutos", "Relaxation · 5 minutes"), "0:51 – 0:56"),
    grid([card2("c_relax", "savasana", "F", ("Relajación", "Relaxation"), ("5 min", "5 min"), ("", ""), mh=12)], cols=1),
    band(10, ("Respiración final y cierre", "Respiration finale et clôture"), "0:56 – 1:00"),
    grid([
        card2("chair_sit", "seated_cross", "F", ("Exhalación un poco más larga", "Expiration un peu plus longue"), ("6 veces", "6 fois"), (
            "Ojos cerrados. Inhalamos despacio por la nariz… dos, tres, cuatro. Exhalamos despacio… dos, tres, cuatro, cinco, "
            "seis. Si los números son demasiado largos, contamos menos o respiramos a nuestro ritmo. Sin retener el aire. "
            "((6 veces))",
            "Yeux fermés. On inspire lentement par le nez… deux, trois, quatre. On expire lentement… deux, trois, quatre, cinq, "
            "six. Si les chiffres sont trop longs, on compte moins ou on respire à son rythme. Sans retenir l’air. "
            "((6 fois))"), mh=13),
        card2("chair_sit", "seated_cross", "F", ("Contar hacia atrás y cierre", "Compter à l’envers et clôture"), ("10 resp.", "10 resp."), (
            "Ojos cerrados. Contamos cada exhalación, en silencio, de diez a uno. Si perdemos la cuenta, volvemos a diez, "
            "sin prisa. Manos delante del pecho: gracias por practicar conmigo. Namasté.",
            "Yeux fermés. On compte chaque expiration, en silence, de dix à un. Si on perd le compte, on revient à dix, sans "
            "se presser. Mains devant la poitrine : merci d’avoir pratiqué avec moi. Namasté."), mh=13),
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

CSS += """
.vn { background:#fbeaea; border-left:3px solid #b8453f; color:#5c1f1b; } .vn .vl { background:#b8453f; }
.vj { background:#e3f3f3; border-left:3px solid #2a8a8a; color:#154545; } .vj .vl { background:#2a8a8a; }
.vt { background:#ffffff; border:1.4px solid #222; border-left:4px solid #222; color:#111; } .vt .vl { background:#222; }
.vc { background:#fbe3c9 !important; border-left:3px solid #c0651a !important; color:#5a2e08 !important; } .vc .vl { background:#c0651a !important; }
.vse { background:#fff6d6; border-left:3px solid #c9a227; color:#4d3d05; } .vse .vl { background:#b38f12; }
.optc { border:2px dashed #e0701e; background:#fff8f1; }
.obadge { font-size:6.6pt; font-weight:700; color:#fff; background:#e0701e; border-radius:1mm; padding:0 1.2mm; letter-spacing:.04em; vertical-align:1px; }
"""

body = "".join(P_ALL)
title = "Yoga · clase 4 (ES)" if L == "es" else "Yoga · cours 4 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase4_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
