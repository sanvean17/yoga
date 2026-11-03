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
    "[cS]": ("SILLA", "CHAISE", "it-cs"), "[cF]": ("SUELO", "SOL", "it-cf"),
    "[cP]": ("DE PIE", "DEBOUT", "it-cp"), "[cX]": ("MÁS COMPLETO", "PLUS COMPLET", "it-cx"),
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
          "[OP]": ("vop", "", ""), "[L]": ("vline", "", ""),
          "[SE]": ("vse", "LO QUE SENTIMOS", "CE QU’ON RESSENT"),
          "[JU]": ("vj", "JUNTOS · LO QUE DIGO", "ENSEMBLE · CE QUE JE DIS")}
    for k, (c, les, lfr) in VB.items():
        h = h.replace(k, f'<span class="vb {c}"><span class="vl">{les if L == "es" else lfr}</span>')
    for k in ("[/C]", "[/CP]", "[/S]", "[/DP]", "[/SU]", "[/MC]", "[/NO]", "[/JU]", "[/TO]", "[/SE]", "[/OP]", "[/L]"):
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


# ---- spoken format: BENEFIT (start) + what we do + FEEL (end), then one small OPTIONS box ----
BEN = {
    "Cuello": ("Esto sirve para soltar el cuello.", "Ça sert à relâcher le cou."),
    "Hombros": ("Esto suelta los hombros.", "Ça relâche les épaules."),
    "Nuevo · Abrazo y apertura": ("Esto abre el pecho y estira la espalda alta.", "Ça ouvre la poitrine et étire le haut du dos."),
    "Nuevo · La cabeza atrás": ("Esto alarga la nuca y nos ayuda a estar más rectos.", "Ça allonge la nuque et ça aide à se tenir plus droit."),
    "Muñecas y tobillos": ("Esto mueve las articulaciones; unos tobillos ágiles ayudan al equilibrio.",
                           "Ça bouge les articulations ; des chevilles souples aident l’équilibre."),
    "Inclinación lateral": ("Esto estira los costados y nos ayuda a respirar mejor.", "Ça étire les côtés et ça aide à mieux respirer."),
    "Círculos del torso": ("Esto mueve la columna en todas las direcciones.", "Ça bouge la colonne dans toutes les directions."),
    "Gato-vaca": ("Esto da flexibilidad a la columna.", "Ça assouplit la colonne."),
    "Guerrero II · recordatorio": ("Esto fortalece las piernas y abre el pecho.", "Ça muscle les jambes et ouvre la poitrine."),
    "Nuevo · Ángulo lateral": ("Esto estira todo el costado y fortalece las piernas.", "Ça étire tout le côté et muscle les jambes."),
    "Triángulo adaptado · recordatorio": ("Esto estira el costado y la parte interior de las piernas.",
                                          "Ça étire le côté et l’intérieur des jambes."),
    "Nuevo · El avión": ("Esto entrena el equilibrio y fortalece los tobillos: nos ayuda a no caernos.",
                         "Ça entraîne l’équilibre et muscle les chevilles : ça aide à ne pas tomber."),
    "Nuevo · Estirarse como al despertar": ("Esto despierta todo el cuerpo y alarga la espalda.",
                                            "Ça réveille tout le corps et allonge le dos."),
    "Balanceo de la pelvis": ("Esto mueve la espalda baja con suavidad.", "Ça bouge le bas du dos en douceur."),
    "Rodilla al pecho": ("Esto relaja la espalda baja.", "Ça relâche le bas du dos."),
    "Nuevo · Talones que se deslizan": ("Esto mueve la cadera y la rodilla sin forzar.", "Ça bouge la hanche et le genou sans forcer."),
    "Nuevo · Ángel en el suelo": ("Esto abre el pecho y los hombros.", "Ça ouvre la poitrine et les épaules."),
    "La banana": ("Esto estira todo el costado.", "Ça étire tout le côté."),
    "Torsión tumbada": ("Esto relaja la espalda.", "Ça détend le dos."),
    "Nuevo · La almeja": ("Esto fortalece el lado de la cadera: nos ayuda a caminar más estables.",
                          "Ça muscle le côté de la hanche : ça aide à marcher plus stable."),
    "Nuevo · Apretar los glúteos": ("Esto fortalece los glúteos sin mover la cadera: nos ayuda a levantarnos y a caminar.",
                                    "Ça muscle les fesses sans bouger la hanche : ça aide à se lever et à marcher."),
    "Descanso: el niño": ("Esto descansa la espalda.", "Ça repose le dos."),
}
FEEL = {
    "Cuello": ("Notamos que tira suavemente en el lado del cuello. Si duele o marea, más pequeño.",
               "On sent que ça tire doucement sur le côté du cou. Si ça fait mal ou que ça tourne, plus petit."),
    "Hombros": ("Notamos calor en los hombros; el cuello no se tensa.", "On sent de la chaleur dans les épaules ; le cou ne se crispe pas."),
    "Nuevo · Abrazo y apertura": ("Al abrir, notamos el pecho que se estira; al abrazarnos, entre los omóplatos. Si pincha el "
                                  "hombro, más pequeño.",
                                  "En ouvrant, on sent la poitrine qui s’étire ; en se faisant un câlin, entre les omoplates. "
                                  "Si l’épaule pique, plus petit."),
    "Nuevo · La cabeza atrás": ("Notamos que se alarga la parte de atrás del cuello. No debe doler la garganta ni marear.",
                                "On sent l’arrière du cou qui s’allonge. La gorge ne doit pas faire mal, et ça ne doit pas "
                                "tourner."),
    "Muñecas y tobillos": ("Es un movimiento suave; si duele una articulación, más pequeño.",
                           "C’est un mouvement doux ; si une articulation fait mal, plus petit."),
    "Inclinación lateral": ("Notamos que tira en el costado de arriba, no en el cuello ni en la espalda baja.",
                            "On sent que ça tire sur le côté du haut, pas dans le cou ni dans le bas du dos."),
    "Círculos del torso": ("Notamos la espalda que se mueve suave. Si marea, círculos más pequeños.",
                           "On sent le dos qui bouge en douceur. Si ça tourne, des cercles plus petits."),
    "Gato-vaca": ("Notamos toda la espalda que se mueve, sin pellizcos en la espalda baja ni en el cuello.",
                  "On sent tout le dos qui bouge, sans pincement dans le bas du dos ni dans le cou."),
    "Guerrero II · recordatorio": ("Notamos calor y trabajo en los muslos. Si duele la rodilla o pellizca la ingle, más pequeño.",
                                   "On sent de la chaleur et du travail dans les cuisses. Si le genou fait mal ou que l’aine "
                                   "pince, plus petit."),
    "Nuevo · Ángulo lateral": ("Notamos que tira en el costado de arriba. Si pellizca la ingle, la rodilla o la espalda baja, "
                               "menos.",
                               "On sent que ça tire sur le côté du haut. Si l’aine, le genou ou le bas du dos pincent, moins."),
    "Triángulo adaptado · recordatorio": ("Notamos que tira suave en el costado y en la parte interior del muslo; nada en la "
                                          "rodilla ni en el cuello.",
                                          "On sent que ça tire doucement sur le côté et à l’intérieur de la cuisse ; rien "
                                          "dans le genou ni dans le cou."),
    "Nuevo · El avión": ("Notamos trabajo en el tobillo y en la pierna de apoyo; nada en la espalda baja.",
                         "On sent le travail dans la cheville et la jambe d’appui ; rien dans le bas du dos."),
    "Nuevo · Estirarse como al despertar": ("Notamos que todo el cuerpo se alarga, de las manos a los pies. Si molestan los "
                                            "hombros, los brazos se quedan a lo largo del cuerpo.",
                                            "On sent tout le corps qui s’allonge, des mains aux pieds. Si les épaules "
                                            "gênent, les bras restent le long du corps."),
    "Balanceo de la pelvis": ("Notamos un movimiento pequeño en la espalda baja; no debe doler.",
                              "On sent un petit mouvement dans le bas du dos ; ça ne doit pas faire mal."),
    "Rodilla al pecho": ("Notamos que tira suave en el glúteo y la espalda baja. Si pellizca delante de la cadera, la rodilla "
                         "más lejos.",
                         "On sent que ça tire doucement dans la fesse et le bas du dos. Si ça pince devant la hanche, le "
                         "genou plus loin."),
    "Nuevo · Talones que se deslizan": ("No debe tirar: es un movimiento libre. Si pellizca la ingle, más pequeño.",
                                        "Ça ne doit pas tirer : c’est un mouvement libre. Si l’aine pince, plus petit."),
    "Nuevo · Ángel en el suelo": ("Notamos que tira suave en el pecho y los hombros. Si pincha un hombro, más pequeño.",
                                  "On sent que ça tire doucement dans la poitrine et les épaules. Si une épaule pique, plus "
                                  "petit."),
    "La banana": ("Notamos todo el costado que se alarga, de los pies a las manos; nada en la espalda baja.",
                  "On sent tout le côté qui s’allonge, des pieds aux mains ; rien dans le bas du dos."),
    "Torsión tumbada": ("Notamos la espalda que se suelta. Si pellizca la espalda baja o un hombro, las rodillas menos lejos.",
                        "On sent le dos qui se relâche. Si le bas du dos ou une épaule pincent, les genoux moins loin."),
    "Nuevo · La almeja": ("Notamos calor en el lado del glúteo. Si duele la cadera o la espalda, más pequeño.",
                          "On sent de la chaleur sur le côté de la fesse. Si la hanche ou le dos font mal, plus petit."),
    "Nuevo · Apretar los glúteos": ("Notamos los glúteos que trabajan; la respiración sigue tranquila.",
                                    "On sent les fesses qui travaillent ; la respiration reste tranquille."),
    "Descanso: el niño": ("Notamos la espalda que se suelta; nada en las rodillas ni en las caderas.",
                          "On sent le dos qui se relâche ; rien dans les genoux ni dans les hanches."),
}


def _build(d, i, name=None):
    parts = []
    if d["intro"]:
        parts.append(d["intro"][i])
    say_ = []
    if name in BEN:
        say_.append(BEN[name][i])
    say_.append(d["common"][i])
    if name in FEEL:
        say_.append(FEEL[name][i])
    parts.append(" ".join(say_))
    lines = []
    if d["chair"]:
        lines.append("[L][cS] " + d["chair"][i] + "[/L]")
    if d["alt"]:
        chip = "[cF]" if d["alt"][0] == "SU" else "[cP]"
        lines.append("[L]" + chip + " " + d["alt"][1 + i] + "[/L]")
    if d["mc"]:
        lines.append("[L][cX] " + d["mc"][i] + "[/L]")
    if lines:
        parts.append("[OP]" + "".join(lines) + "[/OP]")
    if d["ju"]:
        parts.append("[JU]" + d["ju"][i] + "[/JU]")
    return " ".join(parts)


TEXTS["Nuevo · Estirarse como al despertar"] = _t((
    "Inhalamos: los brazos suben por encima de la cabeza y las piernas se alargan, como cuando nos despertamos por la "
    "mañana. Exhalamos: soltamos. ((3 veces)) Despacio, sin forzar.",
    "On inspire : les bras montent au-dessus de la tête et les jambes s’allongent, comme quand on se réveille le matin. On "
    "expire : on relâche. ((3 fois)) Lentement, sans forcer."),
    intro=("**Bajamos al suelo como hemos aprendido: de lado, a cuatro apoyos, una rodilla, las manos en la silla. Quien "
           "prefiere, se queda en la silla.**",
           "**On descend au sol comme on l’a appris : de côté, à quatre pattes, un genou, les mains sur la chaise. Ceux qui "
           "préfèrent restent sur la chaise.**"),
    chair=("Sentados, la espalda larga; los brazos suben y las piernas se estiran un poco delante.",
           "Assis, le dos long ; les bras montent et les jambes s’allongent un peu devant."),
    alt=("SU", "Tumbados boca arriba, piernas largas o rodillas dobladas.",
         "Allongés sur le dos, jambes longues ou genoux pliés."))
TEXTS["Nuevo · Apretar los glúteos"] = _t((
    "Apretamos los glúteos, como si quisiéramos sujetar una moneda. ((5 segundos)) Soltamos del todo. ((5 segundos)) "
    "((8 veces)) No aguantamos el aire: respiramos mientras apretamos.",
    "On serre les fesses, comme pour tenir une pièce de monnaie. ((5 secondes)) On relâche complètement. ((5 secondes)) "
    "((8 fois)) On ne retient pas l’air : on respire pendant qu’on serre."),
    chair=("Sentados, los pies bien apoyados.", "Assis, les pieds bien posés."),
    alt=("SU", "Tumbados boca arriba, piernas largas o rodillas dobladas.",
         "Allongés sur le dos, jambes longues ou genoux pliés."))
TEXTS["Balanceo de la pelvis"]["intro"] = None
TEXTS["Nuevo · La almeja"]["alt"] = ("SU", TEXTS["Nuevo · La almeja"]["alt"][1].replace(" Luego nos tumbamos boca arriba.", " Luego nos tumbamos boca arriba."),
                                     TEXTS["Nuevo · La almeja"]["alt"][2])



def _rename(old, new):
    TEXTS[new] = TEXTS[old]
    for dct in (BEN, FEEL):
        if old in dct:
            dct[new] = dct[old]


_rename("Nuevo · Estirarse como al despertar", "Nuevo · Montaña tumbada (Supta Tadasana)")
_rename("Rodilla al pecho", "Rodilla al pecho (Apanasana)")
_rename("La banana", "La banana (Bananasana)")
_rename("Torsión tumbada", "Torsión tumbada (Supta Matsyendrasana)")
_rename("Descanso: el niño", "Descanso: el niño (Balasana)")
TEXTS["Torsión tumbada (Supta Matsyendrasana)"]["alt"] = ("SU",
    "Tumbados, brazos en cruz: rodillas juntas a la derecha, la cabeza puede mirar a la izquierda. Los hombros se quedan "
    "apoyados; si las rodillas no llegan al suelo, se quedan a medio camino.",
    "Allongés, bras en croix : genoux serrés à droite, la tête peut regarder à gauche. Les épaules restent posées ; si les "
    "genoux n’arrivent pas au sol, ils restent à mi-chemin.")
TEXTS["Rodilla al pecho (Apanasana)"]["alt"] = ("SU",
    "Tumbados, la rodilla derecha hacia el pecho, el pie izquierdo en el suelo. Una pierna cada vez.",
    "Allongés, le genou droit vers la poitrine, le pied gauche au sol. Une jambe à la fois.")
TEXTS["Nuevo · Pierna estirada (Supta Padangusthasana adaptada)"] = _t((
    "Exhalamos: la pierna derecha se alarga hacia el techo, sin bloquear la rodilla; la rodilla puede quedarse doblada. "
    "Respiramos tranquilos. ((4 resp.)) Bajamos despacio y cambiamos de pierna. Cuidado: no tiramos de la pierna; las manos "
    "solo la sostienen.",
    "On expire : la jambe droite s’allonge vers le plafond, sans bloquer le genou ; le genou peut rester plié. On respire "
    "tranquillement. ((4 resp.)) On redescend doucement et on change de jambe. Attention : on ne tire pas sur la jambe ; les "
    "mains la soutiennent seulement."),
    chair=("Pierna derecha estirada delante, talón en el suelo; el pecho un poco hacia delante, la espalda larga.",
           "Jambe droite allongée devant, talon au sol ; la poitrine un peu vers l’avant, le dos long."),
    alt=("SU", "Tumbados, el pie izquierdo en el suelo; las manos detrás del muslo derecho, nunca detrás de la rodilla.",
         "Allongés, le pied gauche au sol ; les mains derrière la cuisse droite, jamais derrière le genou."))
BEN["Nuevo · Pierna estirada (Supta Padangusthasana adaptada)"] = (
    "Esta postura estira la parte de atrás de la pierna, tumbados, sin cargar la espalda.",
    "Cette posture étire l’arrière de la jambe, allongé, sans charger le dos.")
FEEL["Nuevo · Pierna estirada (Supta Padangusthasana adaptada)"] = (
    "Notamos que tira suave detrás del muslo; nada detrás de la rodilla ni en la espalda baja.",
    "On sent que ça tire doucement derrière la cuisse ; rien derrière le genou ni dans le bas du dos.")
TEXTS["Pecho abierto, brazos en cactus"] = _t((
    "Inhalamos: el pecho se abre y los hombros se sueltan hacia el suelo. Exhalamos: todo se relaja. ((4 resp.)) Los "
    "brazos se quedan quietos; solo respiramos.",
    "On inspire : la poitrine s’ouvre et les épaules se relâchent vers le sol. On expire : tout se détend. ((4 resp.)) Les "
    "bras restent immobiles ; on respire seulement."),
    chair=("Sentados, la espalda en el respaldo, brazos en cactus: codos a la altura de los hombros, manos arriba.",
           "Assis, le dos contre le dossier, bras en cactus : coudes à hauteur d’épaules, mains en haut."),
    alt=("SU", "Tumbados, rodillas dobladas: brazos en cactus en el suelo, el dorso de las manos apoyado. Si molesta el "
         "hombro, las manos sobre el vientre.",
         "Allongés, genoux pliés : bras en cactus au sol, le dos des mains posé. Si l’épaule gêne, les mains sur le "
         "ventre."))
BEN["Pecho abierto, brazos en cactus"] = ("Esta postura abre el pecho y los hombros, y da espacio a la respiración.",
                                         "Cette posture ouvre la poitrine et les épaules, et donne de l’espace à la respiration.")
FEEL["Pecho abierto, brazos en cactus"] = ("Notamos el pecho que se abre; si pincha un hombro, los brazos más bajos.",
                                          "On sent la poitrine qui s’ouvre ; si une épaule pique, les bras plus bas.")
BEN["Nuevo · Montaña tumbada (Supta Tadasana)"] = ("Esta postura despierta todo el cuerpo y alarga la espalda.",
                                                   "Cette posture réveille tout le corps et allonge le dos.")



TEXTS["Nuevo · Brazos de águila (Garudasana)"] = _t((
    "Brazos delante: cruzamos el brazo derecho por debajo del izquierdo y doblamos los codos; las palmas se acercan. Si no "
    "llegamos, nos abrazamos: las manos en los hombros. Inhalamos: los codos suben un poco. Exhalamos: los hombros bajan. "
    "((3 resp.)) Cambiamos de brazo. Igual en la silla o sentados en el suelo.",
    "Bras devant : on croise le bras droit sous le gauche et on plie les coudes ; les paumes se rapprochent. Si on n’y "
    "arrive pas, on se fait un câlin : les mains sur les épaules. On inspire : les coudes montent un peu. On expire : les "
    "épaules descendent. ((3 resp.)) On change de bras. Pareil sur la chaise ou assis au sol."))
BEN["Nuevo · Brazos de águila (Garudasana)"] = ("Esta postura estira la espalda alta, entre los omóplatos, y suelta los hombros.",
                                                "Cette posture étire le haut du dos, entre les omoplates, et relâche les épaules.")
FEEL["Nuevo · Brazos de águila (Garudasana)"] = ("Notamos que tira entre los omóplatos; si pincha el hombro, mejor el abrazo.",
                                                 "On sent que ça tire entre les omoplates ; si l’épaule pique, plutôt le câlin.")
TEXTS["Torsión sentada (Bharadvajasana adaptada)"] = _t((
    "Inhalamos: crecemos, la espalda larga. Exhalamos: giramos suavemente hacia la derecha, primero el abdomen, después "
    "el pecho, la cabeza al final. ((3 resp.)) Volvemos al centro y cambiamos de lado. Cuidado: giramos poco, sin forzar "
    "con las manos.",
    "On inspire : on grandit, le dos long. On expire : on tourne doucement vers la droite, d’abord le ventre, puis la "
    "poitrine, la tête en dernier. ((3 resp.)) On revient au centre et on change de côté. Attention : on tourne peu, sans "
    "forcer avec les mains."),
    chair=("Mano izquierda en la rodilla derecha, mano derecha en el reposabrazos.",
           "Main gauche sur le genou droit, main droite sur l’accoudoir."),
    alt=("SU", "Sentados con las piernas cruzadas; mano izquierda en la rodilla derecha, mano derecha en el suelo, detrás.",
         "Assis en tailleur ; main gauche sur le genou droit, main droite au sol, derrière."))
BEN["Torsión sentada (Bharadvajasana adaptada)"] = ("Esta postura mueve la columna y suelta la espalda.",
                                                    "Cette posture bouge la colonne et détend le dos.")
FEEL["Torsión sentada (Bharadvajasana adaptada)"] = ("Notamos un giro suave en la espalda; nada en la espalda baja.",
                                                     "On sent une rotation douce dans le dos ; rien dans le bas du dos.")
TEXTS["Nuevo · El bastón (Dandasana)"] = _t((
    "Las piernas largas delante, los dedos de los pies miran al techo. Las manos empujan suavemente a los lados de las "
    "caderas. Inhalamos: crecemos, la coronilla sube hacia el techo. Exhalamos: los hombros bajan, lejos de las orejas. "
    "((4 resp.)) Cuidado: no nos echamos atrás; si la espalda se redondea, doblamos las rodillas.",
    "Les jambes longues devant, les orteils regardent le plafond. Les mains poussent doucement de chaque côté des "
    "hanches. On inspire : on grandit, le sommet de la tête monte vers le plafond. On expire : les épaules descendent, "
    "loin des oreilles. ((4 resp.)) Attention : on ne part pas en arrière ; si le dos s’arrondit, on plie les genoux."),
    intro=("**Quien quiera, se sienta en el suelo despacio, con la ayuda de la silla; quien prefiera, se queda en la silla.**",
           "**Ceux qui veulent s’assoient au sol doucement, avec l’aide de la chaise ; ceux qui préfèrent restent sur la "
           "chaise.**"),
    chair=("Al borde de la silla, las dos piernas largas delante, talones en el suelo; las manos empujan el asiento.",
           "Au bord de la chaise, les deux jambes longues devant, talons au sol ; les mains poussent sur l’assise."),
    alt=("SU", "Sentados, piernas largas delante; si cuesta, las rodillas dobladas, o la espalda contra la pared.",
         "Assis, jambes longues devant ; si c’est difficile, genoux pliés, ou le dos contre le mur."),
    mc=("Inhalamos: los brazos suben por encima de la cabeza; nos quedamos 3 respiraciones con la espalda larga.",
        "On inspire : les bras montent au-dessus de la tête ; on reste 3 respirations, le dos long."))
BEN["Nuevo · El bastón (Dandasana)"] = ("Esta postura despierta la espalda y nos enseña a sentarnos rectos.",
             "Cette posture réveille le dos et nous apprend à bien nous tenir assis.")
FEEL["Nuevo · El bastón (Dandasana)"] = ("Notamos que la espalda trabaja y se alarga, y un estiramiento suave detrás de las piernas; nada en la espalda baja.",
              "On sent le dos qui travaille et s’allonge, et un étirement doux derrière les jambes ; rien dans le bas du dos.")
TEXTS["Nuevo · Una pierna larga · estiramiento sentado"] = _t((
    "La pierna derecha larga delante, los dedos del pie miran al techo; la rodilla izquierda doblada, el pie izquierdo en "
    "el suelo, un poco lejos de la cadera. Las dos rodillas miran al techo. Inhalamos: la espalda larga. Exhalamos: nos "
    "inclinamos un poco hacia la pierna derecha, desde las caderas; las manos en la pierna, donde llegan. ((4 resp.)) "
    "Subimos despacio y cambiamos de pierna. Cuidado: la cabeza no tiene que bajar; la espalda se queda larga.",
    "La jambe droite longue devant, les orteils regardent le plafond ; le genou gauche plié, le pied gauche au sol, un "
    "peu loin de la hanche. Les deux genoux regardent le plafond. On inspire : le dos long. On expire : on se penche un "
    "peu vers la jambe droite, depuis les hanches ; les mains sur la jambe, là où elles arrivent. ((4 resp.)) On remonte "
    "doucement et on change de jambe. Attention : la tête n’a pas besoin de descendre ; le dos reste long."),
    chair=("Pierna derecha estirada delante, talón en el suelo; la otra pierna doblada, el pie en el suelo.",
           "Jambe droite allongée devant, talon au sol ; l’autre jambe pliée, le pied au sol."),
    alt=("SU", "Sentados, pierna derecha larga, pie izquierdo en el suelo; si cuesta, la espalda contra la pared y solo "
         "crecemos, sin inclinarnos. Luego nos tumbamos boca arriba, despacio, apoyándonos en los codos.",
         "Assis, jambe droite longue, pied gauche au sol ; si c’est difficile, le dos contre le mur et on grandit "
         "seulement, sans se pencher. Puis on s’allonge sur le dos, doucement, en s’appuyant sur les coudes."))
BEN["Nuevo · Una pierna larga · estiramiento sentado"] = ("Esta postura estira la parte de atrás de una pierna, sin abrir la cadera.",
               "Cette posture étire l’arrière d’une jambe, sans ouvrir la hanche.")
FEEL["Nuevo · Una pierna larga · estiramiento sentado"] = ("Notamos que tira detrás del muslo de la pierna larga; si pellizca delante de la cadera, alejamos el pie "
                "o nos inclinamos menos.",
                "On sent que ça tire derrière la cuisse de la jambe longue ; si ça pince devant la hanche, on éloigne le "
                "pied ou on se penche moins.")
TEXTS["El puente pequeño (Setu Bandhasana)"] = _t((
    "Los pies empujan el suelo. Inhalamos: empujamos los pies y subimos solo un poco la pelvis. Exhalamos: bajamos "
    "despacio. ((4 veces)) Cuidado: no subimos mucho, no arqueamos la espalda y no aguantamos el aire.",
    "Les pieds poussent dans le sol. On inspire : on pousse dans les pieds et on décolle juste un peu le bassin. On "
    "expire : on redescend doucement. ((4 fois)) Attention : on ne monte pas haut, on ne creuse pas le dos et on ne "
    "retient pas l’air."),
    chair=("Sin levantarnos: los pies empujan el suelo, apretamos un poco las piernas y los glúteos, respiramos "
           "((3 resp.)) y soltamos.",
           "Sans se lever : les pieds poussent dans le sol, on contracte un peu les jambes et les fessiers, on respire "
           "((3 resp.)) et on relâche."),
    alt=("SU", "Tumbados, rodillas dobladas, pies separados como las caderas, brazos al lado del cuerpo; la pelvis "
         "sube solo un poco.",
         "Allongés, genoux pliés, pieds largeur du bassin, bras le long du corps ; le bassin décolle juste un peu."))
BEN["El puente pequeño (Setu Bandhasana)"] = ("Esto fortalece las piernas y los glúteos: nos ayuda a levantarnos y a caminar.",
               "Ça muscle les jambes et les fessiers : ça aide à se lever et à marcher.")
FEEL["El puente pequeño (Setu Bandhasana)"] = ("Notamos que trabajan los glúteos y los muslos; si pellizca la cadera, la rodilla o la espalda, la pelvis "
                "se queda en el suelo y solo empujamos los pies.",
                "On sent les fessiers et les cuisses qui travaillent ; si ça pince à la hanche, au genou ou au dos, le "
                "bassin reste au sol et on pousse juste dans les pieds.")
TEXTS["Nuevo · Montaña tumbada (Supta Tadasana)"]["intro"] = None
TEXTS["Torsión tumbada (Supta Matsyendrasana)"]["alt"] = ("SU",
    "Tumbados, brazos en cruz: rodillas juntas a la derecha, la cabeza puede mirar a la izquierda. Los hombros se quedan "
    "apoyados; si las rodillas no llegan al suelo, se quedan a medio camino. Después nos quedamos tumbados para la "
    "relajación.",
    "Allongés, bras en croix : genoux serrés à droite, la tête peut regarder à gauche. Les épaules restent posées ; si les "
    "genoux n’arrivent pas au sol, ils restent à mi-chemin. Puis on reste allongés pour la relaxation.")
TEXTS["La banana (Bananasana)"]["alt"] = ("SU",
    "Tumbados, brazos por encima de la cabeza. Llevamos los pies y las manos un poco hacia la izquierda: el cuerpo hace una "
    "banana. Si los hombros no suben, los brazos doblados o las manos en la cabeza.",
    "Allongés, bras au-dessus de la tête. On emmène les pieds et les mains un peu vers la gauche : le corps fait une banane. "
    "Si les épaules ne montent pas, les bras pliés ou les mains sur la tête.")


# ======================= COURSE 5 =======================
_rename("Nuevo · Abrazo y apertura", "Abrazo y apertura")
_rename("Nuevo · Pierna estirada (Supta Padangusthasana adaptada)", "Pierna estirada (Supta Padangusthasana adaptada)")
_rename("Nuevo · Una pierna larga · estiramiento sentado", "Una pierna larga · estiramiento sentado")
_rename("Nuevo · Ángulo lateral", "Ángulo lateral · recordatorio")
TEXTS["Una pierna larga · estiramiento sentado"] = dict(TEXTS["Una pierna larga · estiramiento sentado"])
TEXTS["Una pierna larga · estiramiento sentado"]["intro"] = (
    "**Quien quiera, se sienta en el suelo despacio, con la ayuda de la silla; quien prefiera, se queda en la silla.**",
    "**Ceux qui veulent s’assoient au sol doucement, avec l’aide de la chaise ; ceux qui préfèrent restent sur la "
    "chaise.**")
TEXTS["Una pierna larga · estiramiento sentado"]["alt"] = (
    "SU", "Sentados, pierna derecha larga, pie izquierdo en el suelo; si cuesta, la espalda contra la pared y solo "
    "crecemos, sin inclinarnos.",
    "Assis, jambe droite longue, pied gauche au sol ; si c’est difficile, le dos contre le mur et on grandit seulement, "
    "sans se pencher.")

TEXTS["Nuevo · Los pies despiertos (Pada bandha)"] = _t((
    "Los pies planos en el suelo. Inhalamos: levantamos todos los dedos de los pies y los separamos. Exhalamos: los "
    "bajamos despacio, uno a uno si podemos, empezando por el pequeño. ((5 veces)) Después sentimos los tres puntos de "
    "cada pie: el talón, la base del dedo gordo y la base del dedo pequeño. Empujamos suavemente en los tres: el arco "
    "del pie sube un poco. ((3 resp.)) Cuidado: si da un calambre, soltamos y movemos el pie.",
    "Les pieds à plat au sol. On inspire : on soulève tous les orteils et on les écarte. On expire : on les repose "
    "doucement, un par un si on peut, en commençant par le petit. ((5 fois)) Puis on sent les trois points de chaque "
    "pied : le talon, la base du gros orteil et la base du petit orteil. On pousse doucement sur les trois : la voûte du "
    "pied remonte un peu. ((3 resp.)) Attention : si une crampe arrive, on relâche et on bouge le pied."),
    chair=("Sentados al borde, los pies planos, debajo de las rodillas.",
           "Assis au bord, les pieds à plat, sous les genoux."),
    alt=("DP", "De pie detrás de la silla, las manos en el respaldo: los tres puntos de cada pie en el suelo.",
         "Debout derrière la chaise, les mains sur le dossier : les trois points de chaque pied au sol."))
BEN["Nuevo · Los pies despiertos (Pada bandha)"] = (
    "Esto despierta los pies: unos pies despiertos nos dan equilibrio.",
    "Ça réveille les pieds : des pieds réveillés nous donnent de l’équilibre.")
FEEL["Nuevo · Los pies despiertos (Pada bandha)"] = (
    "Notamos los pies más vivos y bien apoyados en el suelo.",
    "On sent les pieds plus vivants et bien posés au sol.")

# ---------------- standing: the warrior dance ----------------
TEXTS["Guerrero II · recordatorio"] = dict(TEXTS["Guerrero II · recordatorio"])
TEXTS["Guerrero II · recordatorio"]["intro"] = (
    "**Estas tres posturas ya las conocemos. Hoy lo nuevo es unirlas con la respiración, sin mover los pies: es la danza "
    "del guerrero.**",
    "**Ces trois postures, on les connaît déjà. Aujourd’hui, la nouveauté, c’est de les relier avec la respiration, sans "
    "bouger les pieds : c’est la danse du guerrier.**")
TEXTS["Guerrero II · recordatorio"]["ju"] = None
TEXTS["Ángulo lateral · recordatorio"] = dict(TEXTS["Ángulo lateral · recordatorio"])
TEXTS["Ángulo lateral · recordatorio"]["ju"] = None
TEXTS["Guerrero inverso · recordatorio"] = _t((
    "Desde el guerrero II. Inhalamos: la palma derecha mira al techo y el brazo derecho sube; la mano izquierda baja por "
    "la pierna izquierda, sin apoyar peso. ((2 resp.)) Cuidado: la rodilla de delante sigue doblada, encima del tobillo; "
    "no echamos el cuerpo atrás, el pecho se abre hacia arriba. " + HIP[0],
    "Depuis le guerrier II. On inspire : la paume droite regarde le plafond et le bras droit monte ; la main gauche "
    "descend le long de la jambe gauche, sans appuyer. ((2 resp.)) Attention : le genou avant reste plié, au-dessus de la "
    "cheville ; on ne part pas en arrière, la poitrine s’ouvre vers le haut. " + HIP[1]),
    chair=("Seguimos al borde de la silla, en el guerrero II.", "On reste au bord de la chaise, en guerrier II."),
    alt=("DP", "Igual; la mano izquierda puede quedarse en la silla.",
         "Pareil ; la main gauche peut rester sur la chaise."))
BEN["Guerrero inverso · recordatorio"] = ("Esta postura estira todo el costado y abre el pecho.",
                                         "Cette posture étire tout le côté et ouvre la poitrine.")
FEEL["Guerrero inverso · recordatorio"] = ("Notamos que tira en el costado derecho; nada en la espalda baja.",
                                          "On sent que ça tire sur le côté droit ; rien dans le bas du dos.")
FLOW = (
    "**Derecha:** pierna derecha abierta, la izquierda atrás… inhalamos, guerrero II, brazos en cruz. ((1 resp.)) "
    "Inhalamos: guerrero inverso, el brazo derecho sube… exhalamos: ángulo lateral, el antebrazo derecho en el muslo, el "
    "brazo izquierdo sube… inhalamos: guerrero inverso… exhalamos: ángulo lateral. ((3 veces)) → Los pies no se mueven; "
    "la rodilla de delante sigue encima del tobillo. Inhalamos, subimos; exhalamos, volvemos al centro. "
    "**Izquierda:** igual. → Despacio: un movimiento con cada respiración. Si cansa, nos quedamos en guerrero II o nos "
    "sentamos.",
    "**Droite :** jambe droite ouverte, la gauche en arrière… on inspire, guerrier II, bras en croix. ((1 resp.)) On "
    "inspire : guerrier inversé, le bras droit monte… on expire : angle latéral, l’avant-bras droit sur la cuisse, le "
    "bras gauche monte… on inspire : guerrier inversé… on expire : angle latéral. ((3 fois)) → Les pieds ne bougent pas ; "
    "le genou avant reste au-dessus de la cheville. On inspire, on remonte ; on expire, on revient au centre. "
    "**Gauche :** pareil. → Lentement : un mouvement par respiration. Si c’est fatigant, on reste en guerrier II ou on "
    "s’assoit.")

# ---------------- balance: the dancer ----------------
TEXTS["Nuevo · El bailarín (Natarajasana adaptado)"] = _t((
    "Primero, los tres secretos: **los pies** (tres puntos en el pie de apoyo), **el abdomen** (el bajo vientre entra un "
    "poco), **la mirada** (un punto fijo en el suelo). Inhalamos: la pierna derecha va hacia atrás, la rodilla mira al "
    "suelo; un brazo sube. ((3 resp.)) Exhalamos: volvemos despacio. Cambiamos de lado. Cuidado: la rodilla de apoyo un "
    "poco blanda; no arqueamos la espalda baja; no aguantamos el aire.",
    "D’abord, les trois secrets : **les pieds** (trois points sur le pied d’appui), **le ventre** (le bas du ventre rentre "
    "un peu), **le regard** (un point fixe au sol). On inspire : la jambe droite part en arrière, le genou regarde le "
    "sol ; un bras monte. ((3 resp.)) On expire : on revient doucement. On change de côté. Attention : le genou d’appui "
    "un peu souple ; on ne creuse pas le bas du dos ; on ne retient pas l’air."),
    chair=("Sentados de lado, en la esquina de la silla, el muslo izquierdo apoyado. La pierna derecha se desliza hacia "
           "atrás, la rodilla hacia el suelo, la punta del pie apoyada; el brazo izquierdo sube.",
           "Assis de côté, sur le coin de la chaise, la cuisse gauche posée. La jambe droite glisse vers l’arrière, le "
           "genou vers le sol, la pointe du pied posée ; le bras gauche monte."),
    alt=("DP", "La silla a la izquierda, la mano izquierda en el respaldo. El talón derecho sube hacia la nalga, sin "
         "cogerlo; las dos rodillas cerca. El brazo derecho sube.",
         "La chaise à gauche, la main gauche sur le dossier. Le talon droit monte vers la fesse, sans l’attraper ; les "
         "deux genoux proches. Le bras droit monte."),
    mc=("La mano derecha coge el tobillo o el pantalón; el brazo izquierdo va delante, o la mano se queda en la silla. "
        "El torso se inclina solo un poco hacia delante.",
        "La main droite attrape la cheville ou le pantalon ; le bras gauche part devant, ou la main reste sur la chaise. "
        "Le buste se penche juste un peu vers l’avant."),
    ju=("**Derecha:** los pies, el abdomen, la mirada… inhalamos, la pierna derecha atrás, un brazo sube. → La rodilla "
        "mira al suelo. ((3 resp.)) **Izquierda:** igual… → Si tiembla, está bien: es el equilibrio que trabaja; la mano "
        "vuelve a la silla cuando queremos.",
        "**Droite :** les pieds, le ventre, le regard… on inspire, la jambe droite en arrière, un bras monte. → Le genou "
        "regarde le sol. ((3 resp.)) **Gauche :** pareil… → Si ça tremble, c’est bien : c’est l’équilibre qui travaille ; "
        "la main revient sur la chaise quand on veut."))
BEN["Nuevo · El bailarín (Natarajasana adaptado)"] = (
    "Esta postura entrena el equilibrio y estira la parte delantera del muslo y de la cadera.",
    "Cette posture entraîne l’équilibre et étire l’avant de la cuisse et de la hanche.")
FEEL["Nuevo · El bailarín (Natarajasana adaptado)"] = (
    "Notamos que tira delante del muslo y de la cadera de la pierna de atrás; nada en la rodilla ni en la espalda baja.",
    "On sent que ça tire devant la cuisse et la hanche de la jambe arrière ; rien dans le genou ni dans le bas du dos.")

# ---------------- floor ----------------
TEXTS["Nuevo · Torsión con una rodilla arriba"] = _t((
    "La pierna izquierda larga; la rodilla derecha doblada, el pie derecho en el suelo. Inhalamos: crecemos. Exhalamos: "
    "giramos suavemente hacia la derecha, primero el abdomen, después el pecho, la cabeza al final. ((3 resp.)) "
    "Volvemos al centro y cambiamos de lado. Cuidado: las dos nalgas se quedan apoyadas; no tiramos con los brazos.",
    "La jambe gauche longue ; le genou droit plié, le pied droit au sol. On inspire : on grandit. On expire : on tourne "
    "doucement vers la droite, d’abord le ventre, puis la poitrine, la tête en dernier. ((3 resp.)) On revient au centre "
    "et on change de côté. Attention : les deux fesses restent posées ; on ne tire pas avec les bras."),
    chair=("Mano izquierda en la rodilla derecha, mano derecha en el respaldo o en el reposabrazos.",
           "Main gauche sur le genou droit, main droite sur le dossier ou sur l’accoudoir."),
    alt=("SU", "El brazo izquierdo abraza la rodilla derecha; la mano derecha en el suelo, detrás. Luego nos tumbamos "
         "boca arriba, despacio, apoyándonos en los codos.",
         "Le bras gauche entoure le genou droit ; la main droite au sol, derrière. Puis on s’allonge sur le dos, "
         "doucement, en s’appuyant sur les coudes."))
BEN["Nuevo · Torsión con una rodilla arriba"] = ("Esta postura mueve la columna y suelta la espalda.",
                                                 "Cette posture bouge la colonne et détend le dos.")
FEEL["Nuevo · Torsión con una rodilla arriba"] = (
    "Notamos un giro suave en la espalda; nada en la espalda baja ni en la cadera.",
    "On sent une rotation douce dans le dos ; rien dans le bas du dos ni dans la hanche.")

TEXTS["Nuevo · El pez suave (Matsyasana adaptada)"] = _t((
    "Inhalamos: empujamos suavemente con los antebrazos y el pecho sube un poco, hacia el techo. Exhalamos: bajamos "
    "despacio. ((3 veces)) Cuidado: la cabeza se queda apoyada, no la echamos atrás; si molesta el cuello o la espalda, "
    "más pequeño o solo respiramos con el pecho abierto.",
    "On inspire : on pousse doucement dans les avant-bras et la poitrine monte un peu, vers le plafond. On expire : on "
    "redescend doucement. ((3 fois)) Attention : la tête reste posée, on ne la renverse pas ; si le cou ou le dos gêne, "
    "plus petit ou on respire simplement la poitrine ouverte."),
    chair=("Las manos en el asiento, detrás de las caderas; el pecho sube y se abre, la mirada al frente.",
           "Les mains sur l’assise, derrière les hanches ; la poitrine monte et s’ouvre, le regard devant."),
    alt=("SU", "Tumbados, piernas largas o rodillas dobladas; los codos debajo de los hombros, los antebrazos en el suelo.",
         "Allongés, jambes longues ou genoux pliés ; les coudes sous les épaules, les avant-bras au sol."))
BEN["Nuevo · El pez suave (Matsyasana adaptada)"] = (
    "Esta postura abre el pecho y endereza la espalda, lo contrario de cuando nos encorvamos.",
    "Cette posture ouvre la poitrine et redresse le dos, l’inverse de quand on se voûte.")
FEEL["Nuevo · El pez suave (Matsyasana adaptada)"] = (
    "Notamos el pecho que se abre; nada en el cuello ni en la espalda baja.",
    "On sent la poitrine qui s’ouvre ; rien dans le cou ni dans le bas du dos.")

TEXTS["Limpiaparabrisas (Jathara Parivartanasana suave)"] = _t((
    "Las rodillas juntas. Exhalamos: las rodillas caen despacio hacia la derecha. Inhalamos: vuelven al centro. "
    "Exhalamos: hacia la izquierda. ((6 veces)) Después nos quedamos un poco a cada lado. ((3 resp.)) Cuidado: los "
    "hombros se quedan apoyados; las rodillas bajan solo hasta donde es cómodo.",
    "Les genoux serrés. On expire : les genoux tombent doucement vers la droite. On inspire : ils reviennent au centre. "
    "On expire : vers la gauche. ((6 fois)) Puis on reste un peu de chaque côté. ((3 resp.)) Attention : les épaules "
    "restent posées ; les genoux descendent seulement jusqu’où c’est confortable."),
    chair=("Sentados, rodillas juntas: las llevamos un poco a la derecha y a la izquierda, despacio; los hombros miran "
           "al frente.",
           "Assis, genoux serrés : on les emmène un peu à droite et à gauche, lentement ; les épaules regardent devant."),
    alt=("SU", "Tumbados, los pies en el suelo un poco más separados que las caderas, brazos en cruz. Después nos "
         "quedamos tumbados para la relajación.",
         "Allongés, les pieds au sol un peu plus écartés que les hanches, bras en croix. Puis on reste allongés pour la "
         "relaxation."))
BEN["Limpiaparabrisas (Jathara Parivartanasana suave)"] = (
    "Esto suelta la espalda baja y las caderas, como un masaje.",
    "Ça détend le bas du dos et les hanches, comme un massage.")
FEEL["Limpiaparabrisas (Jathara Parivartanasana suave)"] = (
    "Notamos la espalda baja que se suelta; si pellizca la cadera, el movimiento más pequeño o los pies más separados.",
    "On sent le bas du dos qui se relâche ; si la hanche pince, un mouvement plus petit ou les pieds plus écartés.")
TEXTS["La banana (Bananasana)"] = dict(TEXTS["La banana (Bananasana)"])
TEXTS["Balanceo de la pelvis"] = dict(TEXTS["Balanceo de la pelvis"])
TEXTS["Balanceo de la pelvis"]["intro"] = None



# ---------------- course 5, round 2 ----------------
TEXTS["Nuevo · La respiración del león (Simhasana)"] = _t((
    "Las manos en las rodillas, los dedos abiertos. Inhalamos por la nariz. Exhalamos por la boca bien abierta, sacando "
    "la lengua hacia la barbilla, con un sonido suave: «haaa»; los ojos bien abiertos. ((3 veces)) Cuidado: el sonido "
    "es suave, sin forzar la garganta.",
    "Les mains sur les genoux, les doigts écartés. On inspire par le nez. On expire par la bouche grande ouverte, en "
    "sortant la langue vers le menton, avec un son doux : « haaa » ; les yeux grands ouverts. ((3 fois)) Attention : le "
    "son est doux, sans forcer la gorge."),
    chair=("Sentados al borde, las manos en las rodillas.", "Assis au bord, les mains sur les genoux."),
    alt=("SU", "Sentados con las piernas cruzadas.", "Assis en tailleur."))
BEN["Nuevo · La respiración del león (Simhasana)"] = (
    "Esto suelta la cara, la mandíbula y la garganta… y nos hace sonreír.",
    "Ça détend le visage, la mâchoire et la gorge… et ça fait sourire.")


TEXTS["Nuevo · Brazos de vaca (Gomukhasana, solo los brazos)"] = _t((
    "Inhalamos: el brazo derecho sube; doblamos el codo y la mano derecha baja por detrás del cuello. Exhalamos: la mano "
    "izquierda sube por la espalda, desde abajo. Las manos no tienen que tocarse. ((3 resp.)) Cambiamos de lado. Cuidado: "
    "la cabeza no se va hacia delante; si duele el hombro, la mano de arriba se queda en el hombro o en la cabeza.",
    "On inspire : le bras droit monte ; on plie le coude et la main droite descend derrière la nuque. On expire : la main "
    "gauche remonte dans le dos, par le bas. Les mains n’ont pas besoin de se toucher. ((3 resp.)) On change de côté. "
    "Attention : la tête ne part pas vers l’avant ; si l’épaule fait mal, la main du haut reste sur l’épaule ou sur la "
    "tête."),
    chair=("Sentados al borde, lejos del respaldo.", "Assis au bord, loin du dossier."),
    alt=("SU", "Sentados con las piernas cruzadas.", "Assis en tailleur."),
    mc=("Si las manos se tocan, nos cogemos los dedos.", "Si les mains se touchent, on s’attrape les doigts."))
BEN["Nuevo · Brazos de vaca (Gomukhasana, solo los brazos)"] = (
    "Esto abre los hombros y el pecho: lo contrario del águila.",
    "Ça ouvre les épaules et la poitrine : l’inverse de l’aigle.")
FEEL["Nuevo · Brazos de vaca (Gomukhasana, solo los brazos)"] = (
    "Notamos que tira detrás del brazo de arriba y delante del hombro de abajo; nada que pinche.",
    "On sent que ça tire derrière le bras du haut et devant l’épaule du bas ; rien qui pique.")

TEXTS["Nuevo · Doblar y estirar la rodilla (Janu Naman)"] = _t((
    "Las manos debajo del muslo derecho. Inhalamos: estiramos la pierna, los dedos del pie hacia nosotros. Exhalamos: "
    "doblamos la rodilla. ((5 veces)) Cambiamos de pierna. Cuidado: no bloqueamos la rodilla al estirar; despacio, sin "
    "dolor.",
    "Les mains sous la cuisse droite. On inspire : on allonge la jambe, les orteils vers soi. On expire : on plie le "
    "genou. ((5 fois)) On change de jambe. Attention : on ne bloque pas le genou en l’allongeant ; lentement, sans "
    "douleur."),
    chair=("Sentados al borde: levantamos un poco el pie derecho y sostenemos el muslo con las manos.",
           "Assis au bord : on soulève un peu le pied droit et on tient la cuisse avec les mains."),
    alt=("SU", "Sentados, piernas largas: el talón derecho se desliza hacia nosotros y se aleja.",
         "Assis, jambes longues : le talon droit glisse vers soi et s’éloigne."))
BEN["Nuevo · Doblar y estirar la rodilla (Janu Naman)"] = (
    "Esto mueve la rodilla y despierta el muslo: unas rodillas que se mueven nos ayudan a caminar.",
    "Ça bouge le genou et réveille la cuisse : des genoux qui bougent nous aident à marcher.")
FEEL["Nuevo · Doblar y estirar la rodilla (Janu Naman)"] = (
    "Notamos el muslo que trabaja y la rodilla que se mueve; nada que pinche.",
    "On sent la cuisse qui travaille et le genou qui bouge ; rien qui pique.")

TEXTS["Nuevo · Estiramiento intenso del costado (Parsvottanasana)"] = _t((
    "La silla delante. El pie derecho delante, el izquierdo un paso atrás, los pies como sobre dos raíles; las caderas "
    "miran hacia delante. Las manos en el respaldo. Inhalamos: la espalda larga. Exhalamos: nos inclinamos desde las "
    "caderas, la espalda plana como una mesa; la rodilla de delante un poco doblada. ((3 resp.)) Inhalamos, subimos "
    "despacio. Cambiamos de pierna. Cuidado: no redondeamos la espalda; la cabeza no baja más que el corazón; si pellizca "
    "la cadera, los pies menos separados.",
    "La chaise devant. Le pied droit devant, le gauche un pas en arrière, les pieds comme sur deux rails ; les hanches "
    "regardent devant. Les mains sur le dossier. On inspire : le dos long. On expire : on se penche depuis les hanches, "
    "le dos plat comme une table ; le genou avant un peu plié. ((3 resp.)) On inspire, on remonte doucement. On change de "
    "jambe. Attention : on n’arrondit pas le dos ; la tête ne descend pas plus bas que le cœur ; si la hanche pince, les "
    "pieds moins écartés."),
    chair=("Al borde de la silla, la pierna derecha estirada delante, el talón en el suelo; las manos en el muslo; nos "
           "inclinamos con la espalda larga.",
           "Au bord de la chaise, la jambe droite allongée devant, talon au sol ; les mains sur la cuisse ; on se penche le "
           "dos long."),
    alt=("DP", "Si cuesta el equilibrio, el pie de atrás un poco hacia el lado.",
         "Si l’équilibre est difficile, le pied arrière un peu sur le côté."),
    mc=("Las manos en el asiento de la silla, en lugar del respaldo, si la espalda sigue plana.",
        "Les mains sur l’assise de la chaise, au lieu du dossier, si le dos reste plat."),
    ju=("**Derecha:** pie derecho delante, el izquierdo atrás… manos en el respaldo… inhalamos, espalda larga… exhalamos, "
        "nos inclinamos. → La rodilla de delante un poco blanda. ((3 resp.)) **Izquierda:** igual… → La espalda plana, el "
        "cuello largo.",
        "**Droite :** pied droit devant, le gauche en arrière… mains sur le dossier… on inspire, dos long… on expire, on se "
        "penche. → Le genou avant un peu souple. ((3 resp.)) **Gauche :** pareil… → Le dos plat, le cou long."))
BEN["Nuevo · Estiramiento intenso del costado (Parsvottanasana)"] = (
    "Esta postura estira la parte de atrás de la pierna de delante y alarga la espalda.",
    "Cette posture étire l’arrière de la jambe avant et allonge le dos.")
FEEL["Nuevo · Estiramiento intenso del costado (Parsvottanasana)"] = (
    "Notamos que tira detrás del muslo de la pierna de delante; nada en la espalda baja ni en la rodilla.",
    "On sent que ça tire derrière la cuisse de la jambe avant ; rien dans le bas du dos ni dans le genou.")

TEXTS["La cobra baja (Bhujangasana)"] = _t((
    "Tumbados boca abajo, la frente en el suelo. Las manos debajo de los hombros, los codos cerca del cuerpo. Inhalamos: "
    "la cabeza y el pecho suben un poco; los brazos ayudan, pero no empujan; el abdomen y la pelvis se quedan en el "
    "suelo. Exhalamos: bajamos despacio. ((4 veces)) Cuidado: subimos poco; el cuello largo, miramos al suelo delante; si "
    "molesta la espalda baja, más bajo o en esfinge.",
    "Allongés sur le ventre, le front au sol. Les mains sous les épaules, les coudes près du corps. On inspire : la tête "
    "et la poitrine montent un peu ; les bras aident, mais ne poussent pas ; le ventre et le bassin restent au sol. On "
    "expire : on redescend doucement. ((4 fois)) Attention : on monte peu ; le cou long, on regarde le sol devant ; si le "
    "bas du dos gêne, plus bas ou en sphinx."),
    chair=("Sentados al borde, las manos en los muslos: inhalamos, el pecho avanza y se abre, los hombros atrás; "
           "exhalamos, volvemos.",
           "Assis au bord, les mains sur les cuisses : on inspire, la poitrine avance et s’ouvre, les épaules en arrière ; "
           "on expire, on revient."),
    alt=("SU", "Si es más cómodo: la esfinge, los antebrazos en el suelo, los codos debajo de los hombros.",
         "Si c’est plus confortable : le sphinx, les avant-bras au sol, les coudes sous les épaules."))
BEN["La cobra baja (Bhujangasana)"] = (
    "Esta postura fortalece la espalda y abre el pecho: nos ayuda a no encorvarnos.",
    "Cette posture muscle le dos et ouvre la poitrine : elle aide à ne pas se voûter.")
FEEL["La cobra baja (Bhujangasana)"] = (
    "Notamos que trabaja la espalda, entre los omóplatos; nada que pinche en la espalda baja.",
    "On sent le dos qui travaille, entre les omoplates ; rien qui pique dans le bas du dos.")

TEXTS["La postura del niño (Balasana)"] = _t((
    "Desde boca abajo, empujamos con las manos y llevamos las caderas hacia los talones; la frente en el suelo o sobre "
    "las manos. Respiramos hacia la espalda. ((5 resp.)) Cuidado: no forzamos; si molestan las rodillas o las caderas, "
    "nos quedamos tumbados boca abajo, la cabeza sobre las manos.",
    "Depuis le ventre, on pousse avec les mains et on emmène les hanches vers les talons ; le front au sol ou sur les "
    "mains. On respire vers le dos. ((5 resp.)) Attention : on ne force pas ; si les genoux ou les hanches gênent, on "
    "reste allongé sur le ventre, la tête sur les mains."),
    chair=("Pies separados, manos en los muslos: nos inclinamos un poco, la espalda larga, y descansamos.",
           "Pieds écartés, mains sur les cuisses : on se penche un peu, le dos long, et on se repose."),
    alt=("SU", "Rodillas separadas, las caderas hacia los talones. Después nos tumbamos boca arriba, despacio, por el "
         "lado.",
         "Genoux écartés, les hanches vers les talons. Puis on s’allonge sur le dos, doucement, par le côté."))
BEN["La postura del niño (Balasana)"] = ("Esta postura descansa la espalda después de la cobra.",
                                         "Cette posture repose le dos après le cobra.")
FEEL["La postura del niño (Balasana)"] = ("Notamos la espalda que se suelta; nada en las rodillas ni en las caderas.",
                                          "On sent le dos qui se relâche ; rien dans les genoux ni dans les hanches.")
TEXTS["Nuevo · Torsión con una rodilla arriba"]["alt"] = (
    "SU", "El brazo izquierdo abraza la rodilla derecha; la mano derecha en el suelo, detrás. Luego nos tumbamos boca "
    "abajo, despacio: primero de lado, después sobre el abdomen.",
    "Le bras gauche entoure le genou droit ; la main droite au sol, derrière. Puis on s’allonge sur le ventre, "
    "doucement : d’abord sur le côté, puis sur le ventre.")


def _with_text(args, kw):
    a = list(args)
    name = a[3][0] if len(a) > 3 else None
    if name in TEXTS:
        t = (_build(TEXTS[name], 0, name), _build(TEXTS[name], 1, name))
        if len(a) > 5:
            a[5] = t
        else:
            kw["text"] = t
    return a, kw


SUN_A_SEAT = [
    ("chair_sit", ("1 Corazón", "1 Cœur"), "exh"), ("c_arms_up", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("c_hinge", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("w1_chair_prep", ("5 Pierna I atrás", "5 Jambe G arrière"), "exh"),
    ("c_arms_up", ("6 Brazos arriba", "6 Bras en haut"), "inh"), ("chair_sit", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_A_STAND = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("arms_up_chair", ("2 Brazos arriba", "2 Bras en haut"), "inh"),
    ("hinge", ("3 Flexión", "3 Flexion"), "exh"), (("dog_chair", "half_lift_thighs"), ("4 Espalda larga", "4 Dos long"), "inh"),
    ("lunge_chair_L", ("5 Pie I atrás", "5 Pied G arrière"), "exh"),
    ("arms_up_chair", ("6 Brazos arriba", "6 Bras en haut"), "inh"), ("heart_chair", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_B_SEAT = [
    ("chair_sit", ("1 Corazón", "1 Cœur"), "exh"), ("silla_c", ("2 Silla invisible", "2 Chaise invisible"), "inh"),
    ("c_hinge", ("3 Flexión", "3 Flexion"), "exh"), ("c_lean", ("4 Espalda larga", "4 Dos long"), "inh"),
    ("w1_chair_prep", ("5 Pierna I atrás", "5 Jambe G arrière"), "exh"),
    ("w1_chair", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("chair_sit", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_B_STAND = [
    ("heart_chair", ("1 Corazón", "1 Cœur"), "exh"), ("silla_p", ("2 Silla invisible", "2 Chaise invisible"), "inh"),
    ("hinge", ("3 Flexión", "3 Flexion"), "exh"), (("dog_chair", "half_lift_thighs"), ("4 Espalda larga", "4 Dos long"), "inh"),
    ("lunge_chair_L", ("5 Pie I atrás", "5 Pied G arrière"), "exh"),
    ("w1_stand", ("6 Guerrero I", "6 Guerrier I"), "inh"), ("heart_chair", ("7 Corazón", "7 Cœur"), "exh"),
]
SUN_A_STEPS = [
    (1, ("**Corazón.** Espalda larga, palmas juntas delante del pecho. Exhalamos.",
         "**Cœur.** Dos long, paumes jointes devant la poitrine. On expire.")),
    (2, ("**Brazos arriba.** Inhalamos: abrimos los brazos por los lados y los subimos, hasta donde es cómodo. Si cuesta: "
         "brazos delante o manos en los muslos.",
         "**Bras en haut.** On inspire : on ouvre les bras sur les côtés et on les monte, jusqu’où c’est confortable. Si "
         "c’est difficile : bras devant ou mains sur les cuisses.")),
    (3, ("**Flexión.** Esto estira la espalda y la parte de atrás de las piernas. Exhalamos: rodillas un poco dobladas, nos "
         "inclinamos **desde las caderas**; las manos resbalan por los muslos, la espalda larga. Notamos que tira detrás de "
         "los muslos; si pincha la espalda baja o hay vértigo, subimos un poco. "
         "[OP][L][cX] Si estamos cómodos, la cabeza y los brazos cuelgan.[/L][/OP]",
         "**Flexion.** Ça étire le dos et l’arrière des jambes. On expire : genoux légèrement pliés, on se penche **depuis "
         "les hanches** ; les mains glissent sur les cuisses, le dos long. On sent que ça tire derrière les cuisses ; si le "
         "bas du dos pique ou que ça tourne, on remonte un peu. "
         "[OP][L][cX] Si on est à l’aise, la tête et les bras pendent.[/L][/OP]")),
    (4, ("**Espalda larga.** Inhalamos: subimos un poco, la espalda plana como una mesa, el cuello largo. "
         "[OP][L][cP] Manos en el respaldo, o en los muslos.[/L][/OP]",
         "**Dos long.** On inspire : on remonte un peu, le dos plat comme une table, le cou long. "
         "[OP][L][cP] Mains sur le dossier, ou sur les cuisses.[/L][/OP]")),
    (5, ("**Pierna izquierda atrás.** Esto estira la parte delantera de la cadera. Exhalamos: la pierna izquierda va atrás "
         "y nos quedamos. ((2 resp.)) Las caderas miran hacia delante. Notamos que tira delante de la cadera de la pierna "
         "de atrás; nada en la rodilla de delante. "
         "[OP][L][cS] Giramos un poco en la silla; la pierna izquierda va atrás, al lado de la silla, la punta del pie "
         "apoyada.[/L][L][cP] El pie izquierdo da un paso atrás, pies como sobre dos raíles; las manos en la silla.[/L][/OP]",
         "**Jambe gauche en arrière.** Ça étire l’avant de la hanche. On expire : la jambe gauche part en arrière et on "
         "reste. ((2 resp.)) Les hanches regardent devant. On sent que ça tire devant la hanche de la jambe arrière ; rien "
         "dans le genou avant. "
         "[OP][L][cS] On tourne un peu sur la chaise ; la jambe gauche va en arrière, à côté de la chaise, la pointe du pied "
         "posée.[/L][L][cP] Le pied gauche recule d’un pas, pieds comme sur deux rails ; les mains sur la chaise.[/L][/OP]")),
    (6, ("**Brazos arriba.** Inhalamos: la pierna vuelve y subimos los brazos.",
         "**Bras en haut.** On inspire : la jambe revient et on monte les bras.")),
    (7, ("**Corazón.** Exhalamos: manos delante del pecho. ((1 resp.))",
         "**Cœur.** On expire : mains devant la poitrine. ((1 resp.))")),
]
SUN_B_STEPS = [
    ("B1", ("**En lugar de los brazos arriba · la silla invisible.** Inhalamos: subimos los brazos y doblamos un poco las "
            "rodillas, como para sentarnos. Fortalece los muslos: es lo que usamos para levantarnos de una silla. "
            "[OP][L][cS] Al borde de la silla, nos inclinamos un poco hacia delante con la espalda larga, como para "
            "levantarnos.[/L][L][cP] Las caderas hacia atrás, poco; el peso en todo el pie, un poco hacia los talones; "
            "las rodillas en la dirección de los pies.[/L][/OP]",
            "**À la place des bras en haut · la chaise invisible.** On inspire : on monte les bras et on plie un peu les "
            "genoux, comme pour s’asseoir. Ça muscle les cuisses : c’est ce qu’on utilise pour se lever d’une chaise. "
            "[OP][L][cS] Au bord de la chaise, on se penche un peu vers l’avant le dos long, comme pour se lever.[/L][L][cP] "
            "Les hanches en arrière, peu ; le poids sur tout le pied, un peu vers les talons ; les genoux dans la direction "
            "des pieds.[/L][/OP]")),
    ("B2", ("**Después de la pierna atrás · el guerrero I.** Inhalamos: subimos los brazos, o uno solo si la otra mano está "
            "en la silla. ((2 resp.)) Notamos que tira delante de la cadera de la pierna de atrás; nada en la rodilla de "
            "delante ni en la espalda baja.",
            "**Après la jambe en arrière · le guerrier I.** On inspire : on monte les bras, ou un seul si l’autre main est "
            "sur la chaise. ((2 resp.)) On sent que ça tire devant la hanche de la jambe arrière ; rien dans le genou avant "
            "ni dans le bas du dos.")),
]

INTRO_ES = (
    "Hola a todos, bienvenidos. Nos sentamos bien: los dos huesos de las nalgas en la silla, los pies planos, la espalda "
    "larga. Notamos la respiración. ((3 resp.)) "
    "La semana pasada me preguntasteis: ¿cómo mantener el equilibrio? En yoga hay una respuesta: los **bandhas**. Bandha "
    "quiere decir «cierre» o «llave»: un pequeño apretón, muy suave, que nos da estabilidad. Hoy, tres secretos. "
    "**Uno · los pies (Pada bandha):** tres puntos en el suelo: el talón, la base del dedo gordo y la base del dedo "
    "pequeño. Empujamos suavemente en los tres. ((2 resp.)) "
    "**Dos · el abdomen (Uddiyana bandha, versión suave):** exhalamos y el bajo vientre entra un poco hacia la espalda, "
    "como cuando nos abrochamos un pantalón. Seguimos respirando normalmente: no aguantamos el aire. ((3 resp.)) "
    "Hay también un bandha en el suelo de la pelvis (Mula bandha); hoy solo lo nombramos. "
    "**Tres · la mirada (Drishti):** miramos un punto fijo en el suelo, un poco lejos; los ojos quietos, el cuerpo "
    "quieto. Hoy, en el equilibrio, lo recordaremos: **los pies, el abdomen, la mirada.** Empezamos.")
INTRO_FR = (
    "Bonjour à tous, bienvenue. On s’assoit bien : les deux os des fesses sur la chaise, les pieds à plat, le dos long. On "
    "sent la respiration. ((3 resp.)) "
    "La semaine dernière, vous m’avez demandé : comment tenir l’équilibre ? En yoga, il y a une réponse : les "
    "**bandhas**. Bandha veut dire « verrou » ou « clé » : un petit serrage, très doux, qui nous donne de la stabilité. "
    "Aujourd’hui, trois secrets. "
    "**Un · les pieds (Pada bandha) :** trois points au sol : le talon, la base du gros orteil et la base du petit orteil. "
    "On pousse doucement sur les trois. ((2 resp.)) "
    "**Deux · le ventre (Uddiyana bandha, version douce) :** on expire et le bas du ventre rentre un peu vers le dos, "
    "comme quand on ferme un pantalon. On continue à respirer normalement : on ne retient pas l’air. ((3 resp.)) "
    "Il existe aussi un bandha du périnée (Mula bandha) ; aujourd’hui, on le nomme seulement. "
    "**Trois · le regard (Drishti) :** on regarde un point fixe au sol, un peu loin ; les yeux immobiles, le corps "
    "immobile. Aujourd’hui, dans l’équilibre, on s’en souviendra : **les pieds, le ventre, le regard.** On commence.")

P_ALL = [
    '<div class="top"><div><div class="kick">' +
    ("Clase 5 · guion de la profesora · 1 hora · de pie, en la silla o en el suelo" if L == "es"
     else "Cours 5 · version française · même ordre que la version espagnole") +
    '</div><h1>' + ("Yoga suave · cada uno a su manera" if L == "es" else "Yoga doux · chacun à sa façon") + '</h1></div>'
    '<div class="leg"><b class="sr">' + ("naranja = DERECHA" if L == "es" else "orange = DROITE") +
    '</b> · <b class="sl">' + ("azul = IZQUIERDA" if L == "es" else "bleu = GAUCHE") + "</b><br>" +
    ('<span class="fl lc">SILLA</span> <span class="fl lp">DE PIE CON APOYO</span> <span class="fl lf">SUELO</span> <span class="fl lx">MÁS COMPLETO</span>'
     if L == "es" else
     '<span class="fl lc">CHAISE</span> <span class="fl lp">DEBOUT AVEC APPUI</span> <span class="fl lf">SOL</span> <span class="fl lx">PLUS COMPLET</span>') +
    '</div></div>',
    band(1, ("Bienvenida · los secretos del equilibrio: los bandhas", "Accueil · les secrets de l’équilibre : les bandhas"), "0:00 – 0:05"),
    grid([card2("chair_sit", "heart_chair", "P", ("Los pies, el abdomen, la mirada", "Les pieds, le ventre, le regard"), None,
                (INTRO_ES, INTRO_FR), mh=11)], cols=1),
    band(2, ("Respiración", "Respiration"), "0:05 – 0:11"),
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
        card2("chair_sit", "seated_cross", "F", ("Nuevo · La respiración del león (Simhasana)", "Nouveau · La respiration du lion (Simhasana)"), ("3 veces", "3 fois"), ("", "")),
    ], cols=3),
    band(3, ("Calentamiento · en la silla o en el suelo", "Échauffement · sur la chaise ou au sol"), "0:11 – 0:22"),
    grid([
        card2("c_neck", "seated_neck", "F", ("Cuello", "Cou"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("c_shoulders", "seated_shoulders", "F", ("Hombros", "Épaules"), ("5 + 5", "5 + 5"), ("", "")),
        card2("c_wrists", "wrists", "F", ("Muñecas y tobillos", "Poignets et chevilles"), ("5 + 5", "5 + 5"), ("", "")),
        card2("cowarms_c", "cowarms_f", "F", ("Nuevo · Brazos de vaca (Gomukhasana, solo los brazos)", "Nouveau · Bras de vache (Gomukhasana, bras seulement)"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("c_side_R", "sidebend_R", "F", ("Inclinación lateral", "Inclinaison latérale"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("kneeext_c", "kneeext_f", "F", ("Nuevo · Doblar y estirar la rodilla (Janu Naman)", "Nouveau · Plier et allonger le genou (Janu Naman)"), ("5 veces/lado", "5 fois/côté"), ("", "")),
        card2("chair_cat", "cat", "F", ("Gato-vaca", "Chat-vache"), ("5 veces", "5 fois"), ("", "")),
        card2("g_chair", "seated_cross", "F", ("Nuevo · Brazos de águila (Garudasana)", "Nouveau · Bras d’aigle (Garudasana)"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("chair_sit", "heart_chair", "P", ("Nuevo · Los pies despiertos (Pada bandha)", "Nouveau · Les pieds réveillés (Pada bandha)"), ("5 veces + 3 resp.", "5 fois + 3 resp."), ("", "")),
    ], cols=3),
    part(1, "De pie o en la silla · 0:22 – 0:44", "Debout ou sur la chaise · 0:22 – 0:44"),
    say("**Para levantarnos de la silla:** los pies un poco atrás, la nariz por encima de los pies, empujamos con los pies y "
        "las manos, y nos levantamos despacio; esperamos una respiración antes de empezar. Recordad: **primero os enseño la "
        "postura paso a paso y vosotros miráis; después la hacemos juntos**, despacio, con la respiración.",
        "**Pour se lever de la chaise :** les pieds un peu en arrière, le nez au-dessus des pieds, on pousse avec les pieds "
        "et les mains, et on se lève doucement ; on attend une respiration avant de commencer. Rappel : **d’abord je vous "
        "montre la posture étape par étape et vous regardez ; ensuite on la fait ensemble**, doucement, avec la "
        "respiration."),
    '<div class="keep2">',
    band(5, ("Saludo al sol · 2 rondas A + 1 ronda B (la 4.ª opcional)",
             "Salutation au soleil · 2 rondes A + 1 ronde B (la 4e facultative)"), "0:22 – 0:31"),
    say("**Antes de empezar:** hay dos saludos. **El A** es el más sencillo. **El B** añade dos cosas: la silla invisible y el "
        "guerrero I; es un poco más fuerte. El saludo al sol completo también baja al suelo: en las próximas semanas "
        "añadiremos esas partes poco a poco, con la ayuda de la silla. **Saludo A:** primero mirad, os lo enseño entero, "
        "paso a paso. Después lo hacemos juntos.",
        "**Avant de commencer :** il y a deux salutations. **La A** est la plus simple. **La B** ajoute deux choses : la "
        "chaise invisible et le guerrier I ; elle est un peu plus forte. La vraie salutation au soleil descend aussi au "
        "sol : dans les prochaines semaines, on ajoutera ces parties petit à petit, avec l’aide de la chaise. "
        "**Salutation A :** d’abord regardez, je vous la montre entière, étape par étape. Ensuite on la fait ensemble."),
    '<div class="sl2">' + ("SENTADOS" if L == "es" else "ASSIS") + '</div>' + strip(SUN_A_SEAT, 0.13) +
    '<div class="sl2">' + ("DE PIE" if L == "es" else "DEBOUT") + '</div>' + strip(SUN_A_STAND, 0.13),
    '</div>',
    steps(SUN_A_STEPS),
    '<div class="keep2">',
    say("**Saludo B · lo conocemos de la semana pasada: es el saludo A con dos cosas más.**",
        "**Salutation B · on la connaît depuis la semaine dernière : c’est la salutation A avec deux choses en plus.**"),
    '<div class="sl2">' + ("SENTADOS" if L == "es" else "ASSIS") + '</div>' + strip(SUN_B_SEAT, 0.13) +
    '<div class="sl2">' + ("DE PIE" if L == "es" else "DEBOUT") + '</div>' + strip(SUN_B_STAND, 0.13),
    '</div>',
    steps(SUN_B_STEPS),
    '<div class="keep2">',
    say("**Ahora juntos** · menos palabras, un consejo por ronda:",
        "**Maintenant ensemble** · moins de mots, un conseil par ronde :"),
    steps([
        ("R1", ("**A · pierna izquierda atrás.** Corazón… inhalamos, brazos arriba… exhalamos, flexión… inhalamos, espalda "
                "larga… exhalamos, la pierna izquierda atrás. ((2 resp.)) Inhalamos, la pierna vuelve, brazos arriba… "
                "exhalamos, corazón. → Las caderas miran hacia delante.",
                "**A · jambe gauche en arrière.** Cœur… on inspire, bras en haut… on expire, flexion… on inspire, dos long… "
                "on expire, la jambe gauche en arrière. ((2 resp.)) On inspire, la jambe revient, bras en haut… on expire, "
                "cœur. → Les hanches regardent devant.")),
        ("R2", ("**A · pierna derecha atrás.** Corazón… brazos arriba… flexión… espalda larga… la pierna derecha atrás… "
                "brazos arriba… corazón. → En la flexión, las rodillas un poco dobladas.",
                "**A · jambe droite en arrière.** Cœur… bras en haut… flexion… dos long… la jambe droite en arrière… bras en "
                "haut… cœur. → Dans la flexion, les genoux un peu pliés.")),
        ("R3", ("**B · pierna izquierda atrás.** Corazón… silla invisible… flexión… espalda larga… la pierna izquierda "
                "atrás… guerrero I. ((2 resp.)) Corazón. → En la silla invisible, el peso en todo el pie, un poco hacia los "
                "talones.",
                "**B · jambe gauche en arrière.** Cœur… chaise invisible… flexion… dos long… la jambe gauche en arrière… "
                "guerrier I. ((2 resp.)) Cœur. → Dans la chaise invisible, le poids sur tout le pied, un peu vers les "
                "talons.")),
        ("R4", ("**Opcional · B · pierna derecha atrás.** A vuestro ritmo, un movimiento con cada respiración. → Hombros "
                "lejos de las orejas. Corazón.",
                "**Facultative · B · jambe droite en arrière.** À votre rythme, un mouvement par respiration. → Les épaules "
                "loin des oreilles. Cœur.")),
    ]),
    '</div>',
    band(6, ("La danza del guerrero · y una postura nueva: Parsvottanasana",
             "La danse du guerrier · et une posture nouvelle : Parsvottanasana"), "0:31 – 0:40"),
    say("Primero os recuerdo las tres posturas, de un lado. Después las unimos juntos con la respiración: derecha, y luego "
        "izquierda.",
        "D’abord je vous rappelle les trois postures, d’un côté. Ensuite on les relie ensemble avec la respiration : à "
        "droite, puis à gauche."),
    grid([
        card2("c_w2_R", "w2c_R", "P", ("Guerrero II · recordatorio", "Guerrier II · rappel"), ("2 resp./lado", "2 resp./côté"), ("", "")),
        card2("c_rev_R", "revc_R", "P", ("Guerrero inverso · recordatorio", "Guerrier inversé · rappel"), ("2 resp./lado", "2 resp./côté"), ("", "")),
        card2("c_sa_R", "sac_R", "P", ("Ángulo lateral · recordatorio", "Angle latéral · rappel"), ("2 resp./lado", "2 resp./côté"), ("", "")),
    ], cols=3),
    grid([card2("revc_R", "sac_R", "P", ("Nuevo · Juntos: la danza del guerrero", "Nouveau · Ensemble : la danse du guerrier"),
                ("3 veces/lado", "3 fois/côté"), ("[JU]" + FLOW[0] + "[/JU]", "[JU]" + FLOW[1] + "[/JU]"), mh=14, a_kind="P")], cols=1),
    '<div class="keep2">',
    say("Ahora, una postura nueva. Juntamos los pies, ponemos la silla delante. Primero os la enseño; después la hacemos "
        "juntos.",
        "Maintenant, une posture nouvelle. On rapproche les pieds, on met la chaise devant. D’abord je vous la montre ; "
        "ensuite on la fait ensemble."),
    grid([card2("chair_hamstring", "pyr_p", "P", ("Nuevo · Estiramiento intenso del costado (Parsvottanasana)",
                                                  "Nouveau · Étirement intense du côté (Parsvottanasana)"),
                ("3 resp./lado", "3 resp./côté"), ("", ""), mh=15)], cols=1),
    '</div>',
    '<div class="keep2">',
    band(7, ("Equilibrio · el bailarín (nuevo)", "Équilibre · le danseur (nouveau)"), "0:40 – 0:44"),
    say("Primero os enseño los tres niveles; cada uno elige el suyo. Después lo hacemos juntos.",
        "D’abord je vous montre les trois niveaux ; chacun choisit le sien. Ensuite on le fait ensemble."),
    grid([card3("dancer_c", "dancer_p", "dancer_f", ("Nuevo · El bailarín (Natarajasana adaptado)", "Nouveau · Le danseur (Natarajasana adapté)"),
                ("3 resp./lado", "3 resp./côté"), ("", ""))], cols=1),
    '</div>',
    part(2, "En la silla o en el suelo · 0:44 – 1:00", "Sur la chaise ou au sol · 0:44 – 1:00"),
    band(8, ("Sentados, boca abajo, boca arriba · caderas y espalda", "Assis, sur le ventre, sur le dos · hanches et dos"), "0:44 – 0:51"),
    grid([
        card2("chair_hamstring", "mari_f", "F", ("Una pierna larga · estiramiento sentado", "Une jambe longue · étirement assis"), ("4 resp./lado", "4 resp./côté"), ("", "")),
        card2("c_twist", "mtwist_f", "F", ("Nuevo · Torsión con una rodilla arriba", "Nouveau · Torsion avec un genou levé"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("chair_cow", "cobra", "F", ("La cobra baja (Bhujangasana)", "Le cobra bas (Bhujangasana)"), ("4 veces", "4 fois"), ("", "")),
        card2("child_chair", "child", "F", ("La postura del niño (Balasana)", "La posture de l’enfant (Balasana)"), ("5 resp.", "5 resp."), ("", "")),
        card2("chair_cat", "pelvis_f", "F", ("Balanceo de la pelvis", "Bascule du bassin"), ("6 veces", "6 fois"), ("", "")),
        card2("chair_sit", "bridge", "F", ("El puente pequeño (Setu Bandhasana)", "Le petit pont (Setu Bandhasana)"), ("4 veces", "4 fois"), ("", "")),
        card2("chair_knee", "knee1_f", "F", ("Rodilla al pecho (Apanasana)", "Genou poitrine (Apanasana)"), ("3 resp./lado", "3 resp./côté"), ("", "")),
        card2("c_side_R", "banana_f", "F", ("La banana (Bananasana)", "La banane (Bananasana)"), ("4 resp./lado", "4 resp./côté"), ("", "")),
        card2("chair_sit", "wipers", "F", ("Limpiaparabrisas (Jathara Parivartanasana suave)", "Essuie-glaces (Jathara Parivartanasana douce)"), ("6 veces + 3 resp./lado", "6 fois + 3 resp./côté"), ("", "")),
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
.vop { background:#f2f3f5; border-left:3px solid #9aa3ad; color:#2b3540; padding:.6mm 1.6mm; }
.vop .vl, .vline .vl { display:none; }
.vline { display:block; margin:.3mm 0; padding:0; background:none; border:0; }
.it-cs { background:#c0651a; color:#fff; } .it-cf { background:#3f8a5a; color:#fff; } .it-cp { background:#4a6fa5; color:#fff; }
.it-cx { background:#7a4fa0; color:#fff; }
.optc { border:2px dashed #e0701e; background:#fff8f1; }
.obadge { font-size:6.6pt; font-weight:700; color:#fff; background:#e0701e; border-radius:1mm; padding:0 1.2mm; letter-spacing:.04em; vertical-align:1px; }
"""

body = "".join(P_ALL)
title = "Yoga · clase 5 (ES)" if L == "es" else "Yoga · cours 5 (FR)"
doc = (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{title}</title>'
       f'<style>{CSS}</style></head><body>{body}</body></html>')
out = B.ROOT / "build" / f"yoga_clase5_{L.upper()}.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
