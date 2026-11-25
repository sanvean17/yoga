from pathlib import Path
import contextlib
import io
import sys

with contextlib.redirect_stdout(io.StringIO()):
    from build import fig
    from poses import ALL, chair, side, wall


def pyramid_wall():
    figure = side(
        (0, 81), 60, head=60, face=0,
        armN=((62, 101), -1), armF=((63, 100), -1),
        legN=((18, 4), 1), legF=((-34, 4), 1),
        footN=0, footF=-8,
    )
    wall(figure, 63, h=145)
    return figure


def pyramid_classic():
    return side(
        (0, 81), 52, head=52, face=0,
        armN=((5, 83), 1), armF=((3, 83), 1),
        legN=((22, 4), 1), legF=((-34, 4), 1),
        footN=0, footF=-8,
    )


def dog_wall():
    figure = side(
        (0, 81), 9, head=9, face=-55,
        armN=((93, 102), -1), armF=((92, 102), -1),
        legN=((4, 4), 1), legF=((0, 4), 1),
        footN=0, footF=0,
    )
    wall(figure, 93, h=142)
    return figure


def clock_stand(one_hand=False):
    figure = side(
        (0, 81.5), 90, head=90,
        armN=((10, 44), -1) if one_hand else ((37, 88), -1),
        armF=((37, 88), -1),
        legN=((23, 7), 1), legF=((0, 4), 1),
        footN=-36, footF=0,
    )
    chair(figure, 41, back_left=True)
    figure.arrow([(5, 8), (24, 12)], bulge=5)
    return figure


def clock_seated():
    figure = side(
        (0, 48), 90, head=90,
        armN=((8, 48), -1), armF=((4, 48), -1),
        legN=((49, 7), 1), legF=((39, 4), 1),
        footN=-36, footF=0,
    )
    chair(figure, -10, back_left=True)
    figure.arrow([(40, 11), (54, 13)], bulge=4)
    return figure


def calf_floor():
    return side(
        (0, 9.5), 180, head=180, face=90,
        armN=((-4, 5), 1), armF=((-6, 5), 1),
        legN=((74, 5), 1), legF=((34, 5), 1),
        footN=83, footF=-2,
    )


ALL["calf_floor"] = calf_floor
ALL["dog_wall"] = dog_wall
ALL["c_clock"] = clock_seated
ALL["clock_supported"] = clock_stand
ALL["clock_one_hand"] = lambda: clock_stand(one_hand=True)
ALL["pyramid_wall"] = pyramid_wall
ALL["pyramid_classic"] = pyramid_classic

fr = sys.argv[1] == "fr"
def t(es, french):
    return french if fr else es

import runpy
import re

with contextlib.redirect_stdout(io.StringIO()):
    legacy = runpy.run_path(str(Path(__file__).with_name("build_c5.py")))

def render_text(pair):
    html = legacy["T"](pair)
    html = html.replace("CHAISE OU MUR</span>", "AVEC APPUI</span>").replace(
        "SILLA O PARED</span>", "CON APOYO</span>"
    )
    return html
chair_poses = {"danda_c", "heel_c", "silla_c", "calf_chair", "child_chair", "hug_chair", "chest_chair"}
floor_poses = {"cat", "cow", "openbook_f", "knee1_f", "calf_floor", "seated_cross", "sidebend_R", "hug_floor", "prone", "cobra", "tabletop", "downdog", "plank_knees",
               "step_back_R_knee", "step_back_L_knee", "seated_fold",
               "child", "bridge", "wipers", "savasana"}

def illustration(pose):
    if pose in chair_poses or pose.startswith(("chair_", "c_")):
        label, style = t("SILLA", "CHAISE"), "lc"
    elif pose in floor_poses or pose in {"seated_neck", "seated_shoulders"}:
        label, style = t("SUELO", "SOL"), "lf"
    elif pose == "clock_one_hand":
        label, style = t("MÁS COMPLETO", "PLUS COMPLET"), "lx"
    elif pose in {"pyramid_wall", "dog_wall", "clock_supported"}:
        label, style = t("DE PIE CON APOYO", "DEBOUT AVEC APPUI"), "lp"
    else:
        label, style = t("DE PIE", "DEBOUT"), "lp"
    return (f'<div class="f2">{fig(pose, max_w=27, max_h=19, cap=.14)}'
            f'<span class="fl {style}">{label}</span></div>')

def render_card(poses, title, cue):
    pictures = "".join(illustration(pose) for pose in poses.split())
    figures = f'<div class="qf row2">{pictures}</div>' if pictures else ""
    return (f'<div class="qc c2">{figures}<div class="qt">'
            f'<div class="qn">{render_text(title)}</div>'
            f'<div class="qcue">{render_text(cue)}</div></div></div>')

def block(time, name, exercises):
    number, _, _ = name[0].partition(" · ")
    plain_name = tuple(n.split(" · ", 1)[1] for n in name)
    cols = 3 if number in {"3", "8"} else (2 if number in {"2", "4", "5"} else 1)
    cards = [render_card(*entry) for entry in exercises]
    if number == "8":
        layout = legacy["grid"](cards[:6], cols=3)
        layout += legacy["grid"](cards[6:], cols=1)
    elif number == "4":
        layout = legacy["grid"](cards[:1], cols=1)
        layout += legacy["grid"](cards[1:3], cols=2)
        layout += legacy["grid"](cards[3:], cols=1)
    else:
        layout = legacy["grid"](cards, cols=cols)
    return legacy["band"](number, plain_name, time) + layout

def card(poses, fr_title, es_title, fr_text, es_text):
    return poses, (es_title, fr_title), (es_text, fr_text)

def part(time, fr_title, es_title, *cards):
    return time, (es_title, fr_title), cards

pages = [
  (part("0:00–0:05", "1 · Accueil · salutation au soleil A", "1 · Bienvenida · saludo al sol A",
    card("chair_sit", "À dire au groupe", "Para decir al grupo",
      "Bonjour ! Aujourd’hui, on va se concentrer sur la salutation au soleil qu’on a commencée ensemble. Jusqu’ici, on a vu les mouvements debout. Aujourd’hui, on y ajoute le passage au sol pour faire la salutation au soleil A complète.",
      "¡Hola! Hoy nos centramos en el saludo al sol que empezamos juntas. Ya conocemos la parte de pie. Hoy añadimos el paso por el suelo para hacer el saludo al sol A completo."),
    card("", "Pourquoi saluer le soleil ?", "¿Por qué saludamos al sol?",
      "Surya veut dire « soleil » et namaskar « salutation ». Traditionnellement, on salue le soleil le matin pour accueillir le jour et honorer ce qui nous donne lumière et chaleur. En pratique, les mouvements réchauffent le corps peu à peu. On mobilise les épaules, les hanches et le dos. Les bras et les jambes travaillent, et on apprend à coordonner le geste avec le souffle. Le soir, certaines traditions proposent la salutation à la lune. Le rythme est plus calme pour ralentir avant le repos.",
      "Surya significa «sol» y namaskar significa «saludo». Tradicionalmente, saludamos al sol por la mañana para recibir el día y agradecer su luz y su calor. Con el movimiento, el cuerpo entra en calor poco a poco. Movemos los hombros, las caderas y la espalda. Trabajan los brazos y las piernas, y coordinamos el movimiento con la respiración. Por la noche, algunas tradiciones proponen el saludo a la luna. Es más tranquilo y ayuda a bajar el ritmo antes de descansar."),
  ),),
  (part("0:05–0:10", "2 · Respirer à son rythme", "2 · Respirar a nuestro ritmo",
    card("chair_sit seated_cross", "1 · Un souffle continu · environ 5 fois", "1 · Respiración continua · unas 5 veces",
      "[C] On s’assoit avec les pieds à plat. [/C] [SU] On s’assoit jambes croisées ou pliées, le dos long. [/SU] On pose les mains sur les côtes basses et on relâche les épaules. **On inspire** doucement et on sent les côtes s’ouvrir sous les mains. **On expire** et elles reviennent. Ce souffle régulier nous aide à trouver un rythme avant de bouger. Si ça vous aide, comptez « un, deux » à l’inspiration et « un, deux » à l’expiration. **Chacune compte dans sa tête, à son rythme**, en laissant l’air circuler sans pause. Si le compte gêne, on le laisse de côté.",
      "[C] Nos sentamos con los pies en el suelo. [/C] [SU] Nos sentamos con las piernas cruzadas o dobladas y la espalda larga. [/SU] Ponemos las manos sobre las costillas bajas y soltamos los hombros. **Inhalamos** suave y sentimos cómo se abren las costillas. **Exhalamos** y vuelven a su sitio. Así encontramos un ritmo tranquilo antes de movernos. Si nos ayuda contar, decimos «uno, dos» al entrar y «uno, dos» al salir. **Cada una cuenta por dentro, a su ritmo.** Dejamos que el aire siga, sin aguantarlo. Si el conteo molesta, respiramos sin contar."),
    card("c_breath seated_cross", "2 · Souffle et bras · 5 fois", "2 · Brazos y respiración · 5 veces",
      "On pose les mains sur les cuisses et on relâche les coudes. **On inspire** en ouvrant les bras, paumes vers le haut et mains sous les épaules. On sent la poitrine s’ouvrir doucement et les épaules se mobiliser. **On expire** en ramenant les mains sur les cuisses. Chacune laisse son souffle donner le rythme aux bras.",
      "Apoyamos las manos en los muslos y soltamos los codos. **Inhalamos** y abrimos los brazos con las palmas hacia arriba y las manos por debajo de los hombros. Notamos cómo se abre el pecho al mover los hombros. **Exhalamos** y volvemos a apoyar las manos. Cada una mueve los brazos al ritmo de su respiración."),
  ),),
  (part("0:10–0:21", "3 · Échauffement · sol ou chaise", "3 · Calentamiento · suelo o silla",
    card("c_shoulders seated_neck", "Épaules et nuque · 2 souffles par côté", "Hombros y cuello · 2 respiraciones por lado",
      "[C] On pose les pieds à plat et les mains sur les cuisses. [/C] [SU] On plie ou croise les jambes et on pose les mains sur les cuisses. [/SU] Pour délier les épaules, on les monte et on les relâche trois fois. On fait quatre cercles en arrière et quatre en avant. On regarde devant, on garde les épaules basses et on rapproche une oreille de l’épaule. On sent un léger étirement de l’autre côté du cou. On prend deux souffles, puis on change de côté.",
      "[C] Apoyamos los pies y dejamos las manos sobre los muslos. [/C] [SU] Doblamos o cruzamos las piernas y apoyamos las manos en los muslos. [/SU] Para soltar los hombros, los subimos y dejamos que bajen tres veces. Hacemos cuatro círculos hacia atrás y cuatro hacia delante. Miramos al frente, dejamos los hombros bajos y acercamos una oreja al hombro. Sentimos cómo se estira suavemente el otro lado del cuello. Respiramos dos veces y cambiamos de lado."),
    card("hug_chair hug_floor", "Haut du dos et poitrine · 3 fois", "Espalda alta y pecho · 3 veces",
      "[C] On s’assoit avec les pieds à plat. [/C] [SU] On s’assoit jambes croisées ou pliées. [/SU] **On expire** et on enlace un arbre. Les omoplates s’écartent et on sent le haut du dos s’étirer. **On inspire**, on ouvre les bras, paumes vers le haut, et l’étirement passe devant la poitrine. On garde les épaules basses et le bas du dos tranquille.",
      "[C] Nos sentamos con los pies en el suelo. [/C] [SU] Nos sentamos con las piernas cruzadas o dobladas. [/SU] **Exhalamos** y abrazamos un árbol. Se separan los omóplatos y sentimos cómo se estira la espalda alta. **Inhalamos** y abrimos los brazos con las palmas hacia arriba. Ahora sentimos la apertura en el pecho. Dejamos los hombros bajos y la zona lumbar tranquila."),
    card("c_side_R sidebend_R", "Flancs · 2 souffles par côté", "Costados · 2 respiraciones por lado",
      "[C] Les pieds à plat, on pose une main sur l’assise. [/C] [SU] Les jambes pliées ou croisées, on pose une main au sol près de la hanche. [/SU] On garde l’autre main à la taille ou on la lève. On se grandit puis on se penche vers l’appui, les deux fesses posées. On assouplit le buste en sentant le flanc du haut s’allonger. On respire deux fois et on change de côté.",
      "[C] Con los pies apoyados, ponemos una mano en el asiento. [/C] [SU] Con las piernas dobladas o cruzadas, ponemos una mano en el suelo junto a la cadera. [/SU] La otra mano se queda en la cintura o sube. Nos alargamos y nos inclinamos hacia la mano de apoyo, con los dos glúteos apoyados. Así movemos el tronco y sentimos cómo se estira el costado de arriba. Respiramos dos veces y cambiamos."),
    card("c_hinge seated_fold", "Pli des hanches · 3 fois", "Flexión de caderas · 3 veces",
      "[C] On s’assoit vers le bord, les pieds à plat. [/C] [SU] On allonge les jambes devant avec les genoux pliés. [/SU] Mains sur les cuisses, **on inspire** pour se grandir. **On expire** et on incline un peu le buste depuis les hanches, puis on remonte. On prépare la flexion de la salutation en sentant le pli des hanches, parfois un léger étirement derrière les cuisses. Si le dos s’arrondit, on se penche moins.",
      "[C] Nos sentamos cerca del borde, con los pies apoyados. [/C] [SU] Colocamos las piernas delante, con las rodillas dobladas. [/SU] Apoyamos las manos en los muslos. **Inhalamos** y alargamos la espalda. **Exhalamos**, nos inclinamos un poco desde las caderas y volvemos. Al preparar la flexión del saludo, notamos el pliegue de las caderas y quizá un estiramiento detrás de los muslos. Si la espalda se redondea, bajamos menos."),
    card("cat cow chair_cat", "Chat-vache · 5 fois", "Gato-vaca · 5 veces",
      "[SU] On se met à quatre pattes, poignets sous les épaules et genoux sous les hanches. [/SU] [C] On pose les pieds à plat et les mains sur les cuisses. [/C] **On inspire** en avançant la poitrine et **on expire** en arrondissant le dos. La tête accompagne le mouvement. On mobilise la colonne dans les deux sens : la poitrine s’ouvre, puis le haut du dos s’élargit.",
      "[SU] Nos ponemos a cuatro patas, con las manos bajo los hombros y las rodillas bajo las caderas. [/SU] [C] Apoyamos los pies y ponemos las manos en los muslos. [/C] **Inhalamos** y llevamos el pecho hacia delante. **Exhalamos** y redondeamos la espalda. La cabeza acompaña. Movemos la columna en los dos sentidos y notamos cómo se abre el pecho y luego se ensancha la espalda alta."),
    card("tabletop c_wrists", "Poignets après le chat-vache · 3 fois", "Muñecas después del gato-vaca · 3 veces",
      "[SU] À quatre pattes, on pose les paumes, doigts devant. On avance et on recule un tout petit peu les épaules pour préparer les appuis. On sent une pression légère dans les paumes. Si ça gêne, on fait les cercles assis. [/SU] [C] On pose les avant-bras sur les cuisses et on laisse les mains libres. On fait trois petits cercles dans chaque sens pour mobiliser les poignets. [/C]",
      "[SU] A cuatro patas, apoyamos las palmas con los dedos hacia delante. Desplazamos un poco los hombros hacia delante y volvemos. Así preparamos los apoyos y sentimos una presión suave en las palmas. Si molesta, hacemos los círculos sentadas. [/SU] [C] Apoyamos los antebrazos en los muslos y dejamos las manos libres. Hacemos tres círculos pequeños en cada sentido para mover las muñecas. [/C]"),
  ),),
  (part("0:21–0:29", "4 · Préparer le passage au tapis", "4 · Preparar el paso por el suelo",
    card("", "Je montre une fois, vous essayez deux fois", "Lo muestro una vez y lo hacemos dos veces",
      "[JU] Je montre la descente, le cobra et le chien tête en bas, un par un. Vous essayez chaque mouvement deux fois. Ensuite, on enchaîne deux rondes complètes. Vous pouvez suivre au tapis, au mur ou sur une chaise stable, et changer d’appui entre les rondes. [/JU] Choisissez le tapis si vous descendez et remontez facilement. Si ça pince, changez de variante. Si une douleur ou un vertige apparaît, arrêtez-vous.",
      "[JU] Muestro la bajada, la cobra y el perro, uno por uno. Probamos cada uno dos veces. Luego hacemos dos vueltas completas. Podéis seguir en la esterilla, en la pared o en una silla firme, y cambiar de apoyo entre vueltas. [/JU] Elegid la esterilla si bajáis y subís con facilidad. Si algo pinza, probamos otra opción. Con dolor o mareo, paramos."),
    card("tabletop plank_knees prone", "1 · Descendre depuis quatre pattes", "1 · Bajar desde cuatro patas",
      "[SU] À quatre pattes, on pose les paumes sous les épaules et on recule un peu les genoux en les gardant au sol. **On expire**, on avance un peu la poitrine et on plie les coudes près des côtes. On sent les bras travailler en freinant la descente de la poitrine et du bassin. On revient à quatre pattes pour répéter. [/SU] [CP] On pose les mains au mur et on recule un peu les pieds. On plie doucement les coudes et on sent les bras travailler en repoussant le mur. [/CP] [C] Mains sur les cuisses, on arrondit un peu le dos pour sentir le haut du dos s’élargir, puis on revient. [/C]",
      "[SU] A cuatro patas, apoyamos las manos bajo los hombros y llevamos las rodillas un poco atrás, sin levantarlas. **Exhalamos**, llevamos el pecho un poco hacia delante y doblamos los codos cerca de las costillas. Notamos cómo trabajan los brazos mientras bajamos el pecho y la pelvis despacio. Volvemos a cuatro patas para repetir. [/SU] [CP] Ponemos las manos en la pared y llevamos los pies un poco atrás. Doblamos los codos despacio y sentimos el trabajo de los brazos al empujar la pared. [/CP] [C] Con las manos en los muslos, redondeamos un poco la espalda para sentir cómo se ensancha por arriba. Luego volvemos. [/C]"),
    card("prone cobra chair_cow", "2 · Petit cobra · ouvrir la poitrine", "2 · Cobra baja · abrir el pecho",
      "[SU] Sur le ventre, on laisse le bassin et le dessus des pieds au tapis. On pose les paumes sous les épaules, coudes près des côtes. **On inspire** et on avance le sternum pour soulever un peu la poitrine, les coudes pliés, les épaules basses et le regard vers le tapis. On sent la poitrine s’ouvrir et le haut du dos travailler. Si les lombaires pincent, on monte moins. **On expire** pour redescendre. [/SU] [CP] Les mains au mur et les coudes un peu pliés, **on inspire** en repoussant doucement le mur pour ouvrir la poitrine. [/CP] [C] On pose les mains sur les cuisses et **on inspire** en avançant juste un peu la poitrine. [/C]",
      "[SU] Boca abajo, dejamos la pelvis y los empeines en el suelo. Ponemos las manos bajo los hombros y los codos cerca de las costillas. **Inhalamos** y llevamos el pecho un poco hacia delante y arriba, con los codos doblados, los hombros bajos y la mirada al suelo. Sentimos cómo se abre el pecho y trabaja la espalda alta. Si pinza la zona lumbar, subimos menos. **Exhalamos** y bajamos. [/SU] [CP] Con las manos en la pared y los codos un poco doblados, **inhalamos** y empujamos suavemente la pared para abrir el pecho. [/CP] [C] Apoyamos las manos en los muslos e **inhalamos** llevando el pecho un poco hacia delante. [/C]"),
    card("downdog tabletop dog_wall c_hinge", "3 · Chien tête en bas · monter puis revenir", "3 · Perro boca abajo · subir y volver",
      "[SU] On revient à quatre pattes, les mains à la largeur des épaules et les pieds à la largeur du bassin. On écarte les doigts et on rentre les orteils. **On expire**, on presse les paumes et on monte les hanches vers le haut et l’arrière pour faire un V inversé. On garde les bras longs, la tête entre les bras, le regard vers les jambes et les genoux pliés pour sentir le dos s’allonger. Les bras travaillent et ça peut tirer doucement derrière les cuisses ou dans les mollets. On peut allonger un peu les jambes en laissant les talons libres. Après un souffle, on repose les genoux. Pour une version plus douce, on garde les genoux au sol et on recule seulement les hanches. [/SU] [CP] On pose les paumes au mur à hauteur des épaules. On recule les pieds et les hanches, genoux souples, jusqu’à sentir le dos s’allonger. [/CP] [C] Les pieds à plat et les mains sur les cuisses, on se penche un peu depuis les hanches en gardant le dos long. [/C]",
      "[SU] Volvemos a cuatro patas, con las manos al ancho de los hombros y los pies al ancho de las caderas. Abrimos los dedos de las manos y apoyamos los dedos de los pies. **Exhalamos**, empujamos el suelo y llevamos las caderas arriba y atrás para formar una V invertida. Dejamos los brazos largos, la cabeza entre los brazos y las rodillas dobladas. Miramos hacia las piernas y sentimos cómo se alarga la espalda. Trabajan los brazos y puede tirar suavemente detrás de los muslos o en las pantorrillas. Podemos estirar un poco las piernas con los talones libres. Tras una respiración, apoyamos las rodillas. Para hacerlo más suave, dejamos las rodillas en el suelo y solo llevamos las caderas atrás. [/SU] [CP] Ponemos las manos en la pared a la altura de los hombros. Llevamos los pies y las caderas hacia atrás con las rodillas suaves, hasta notar que se alarga la espalda. [/CP] [C] Con los pies apoyados y las manos en los muslos, nos inclinamos un poco desde las caderas con la espalda larga. [/C]"),
  ),),
  (part("0:29–0:39", "5 · Salutation au soleil A · deux rondes complètes", "5 · Saludo al sol A · dos vueltas completas",
    card("tadasana_heart arms_up fold", "1–3 · Cœur → bras levés → flexion", "1–3 · Pecho → brazos arriba → flexión",
      "1. On place les pieds sous les hanches et les mains au cœur. On sent les deux pieds au sol pour trouver l’équilibre. 2. **On inspire** et on lève les bras à une hauteur confortable. Les flancs s’allongent et les épaules restent basses. 3. **On expire**, on plie un peu les genoux et on penche le buste depuis les hanches. On sent un étirement doux derrière les cuisses. [C] On fait les mêmes gestes assis, les pieds à plat. [/C]",
      "1. Ponemos los pies bajo las caderas y las manos al pecho. Sentimos los dos pies en el suelo para encontrar el equilibrio. 2. **Inhalamos** y subimos los brazos hasta una altura cómoda. Se alargan los costados y los hombros se quedan bajos. 3. **Exhalamos**, doblamos un poco las rodillas y nos inclinamos desde las caderas. Sentimos un estiramiento suave detrás de los muslos. [C] Hacemos los mismos gestos en la silla, con los pies apoyados. [/C]"),
    card("step_back_R_knee plank_knees prone", "4–6 · Fente → genoux au sol → descente", "4–6 · Zancada → rodillas al suelo → bajada",
      "4. On pose les mains au tapis. **On inspire**, on recule le pied droit et on pose le genou droit, pied gauche à plat. Le genou avant suit la direction du pied. On sent une ouverture devant la hanche arrière. 5. **On expire**, on recule le pied gauche et on pose les deux genoux. 6. On plie les coudes près des côtes et on laisse les bras freiner la descente. [CP] Mains au mur, on recule le pied droit puis le gauche et on plie un peu les coudes. [/CP] [C] On glisse le pied droit en arrière et on le ramène. On arrondit un peu le dos pour sentir le haut du dos s’élargir. [/C]",
      "4. Ponemos las manos en la esterilla. **Inhalamos**, llevamos el pie derecho atrás y apoyamos esa rodilla. El pie izquierdo queda plano y la rodilla de delante sigue su dirección. Sentimos cómo se abre la parte de delante de la cadera de atrás. 5. **Exhalamos**, llevamos el pie izquierdo atrás y apoyamos las dos rodillas. 6. Doblamos los codos cerca de las costillas y dejamos que los brazos frenen la bajada. [CP] Con las manos en la pared, llevamos atrás el pie derecho y luego el izquierdo. Doblamos un poco los codos. [/CP] [C] Deslizamos el pie derecho atrás y lo traemos al centro. Redondeamos un poco la espalda para sentir cómo se ensancha por arriba. [/C]"),
    card("cobra downdog step_back_L_knee", "7–9 · Cobra → chien → fente de retour", "7–9 · Cobra → perro → zancada de vuelta",
      "7. **On inspire** et on fait un petit cobra pour ouvrir la poitrine. 8. **On expire**, on repasse à quatre pattes et on monte en chien, ou on recule les hanches avec les genoux posés, pour allonger le dos. 9. **On inspire** et on ramène le pied droit devant pour retrouver un appui stable. On peut reposer les genoux et prendre un souffle de plus pour avancer le pied. [CP] On repousse le mur, on recule les hanches et on avance le pied droit. [/CP] [C] On ouvre la poitrine, on incline le buste et on avance le talon droit. [/C]",
      "7. **Inhalamos** y hacemos una cobra baja para abrir el pecho. 8. **Exhalamos**, volvemos a cuatro patas y hacemos el perro para alargar la espalda. También podemos llevar las caderas atrás con las rodillas apoyadas. 9. **Inhalamos** y llevamos el pie derecho delante para recuperar un apoyo firme. Si hace falta, bajamos las rodillas y respiramos otra vez antes de mover el pie. [CP] Empujamos la pared, llevamos las caderas atrás y adelantamos el pie derecho. [/CP] [C] Abrimos el pecho, inclinamos el torso y adelantamos el talón derecho. [/C]"),
    card("fold arms_up tadasana_heart", "10–12 · Rapprocher les pieds → remonter → cœur", "10–12 · Juntar los pies → subir → pecho",
      "10. **On expire** et on ramène le pied gauche. On reprend ses appuis avant de remonter, avec une aide si besoin. 11. **On inspire** en redressant le buste et en levant les bras. On sent les jambes nous porter. 12. **On expire**, on ramène les mains au cœur et on relâche les épaules. [C] On ramène les pieds sous les genoux, on redresse le buste et on revient les mains au cœur. [/C] [JU] On fait la première ronde à droite puis à gauche, et la deuxième pareil. Le pied qui recule le premier revient le premier. On respire entre les passages. [/JU]",
      "10. **Exhalamos** y traemos el pie izquierdo al centro. Recuperamos los apoyos antes de subir. Usamos un apoyo si hace falta. 11. **Inhalamos** y subimos el torso y los brazos. Sentimos que las piernas nos sostienen. 12. **Exhalamos**, volvemos con las manos al pecho y soltamos los hombros. [C] Ponemos los pies bajo las rodillas, enderezamos el torso y llevamos las manos al pecho. [/C] [JU] Hacemos la primera vuelta a la derecha y luego a la izquierda. Repetimos en la segunda. El pie que va primero atrás vuelve primero delante. Respiramos entre pasadas. [/JU]"),
  ),),
  (part("0:39–0:42", "6 · Debout · la pyramide", "6 · De pie · la pirámide",
    card("pyramid_classic pyramid_wall chair_hamstring", "Parsvottanasana · 3 souffles par côté", "Parsvottanasana · 3 respiraciones por lado",
      "[MC] On place le pied droit devant et le gauche un peu en arrière et sur le côté. Le talon arrière reste au sol. On oriente le bassin vers l’avant, mains aux hanches et genoux souples. **On inspire** en se grandissant et **on expire** en se penchant depuis les hanches, le regard vers le sol. [/MC] [CP] On pose les mains au mur, avec le pied droit devant. On raccourcit le pas et on incline un peu le buste. [/CP] [C] Au bord de la chaise, on avance le talon droit en gardant le pied gauche à plat. On pose les mains sur les cuisses et on incline un peu le buste. [/C] En se penchant depuis les hanches, on cherche un étirement doux derrière la cuisse avant. On garde le dos long et on se redresse avant de changer de côté.",
      "[MC] Ponemos el pie derecho delante y el izquierdo un poco atrás y al lado. El talón de atrás queda apoyado. Giramos la pelvis hacia delante, con las manos en las caderas y las rodillas suaves. **Inhalamos** y nos alargamos. **Exhalamos** y nos inclinamos desde las caderas con la mirada al suelo. [/MC] [CP] Ponemos las manos en la pared con el pie derecho delante. Acortamos el paso y nos inclinamos un poco. [/CP] [C] Nos sentamos cerca del borde y adelantamos el talón derecho, con el pie izquierdo apoyado. Ponemos las manos en los muslos y nos inclinamos un poco. [/C] Al inclinarnos desde las caderas, buscamos un estiramiento suave detrás del muslo de delante. Mantenemos la espalda larga y subimos antes de cambiar de lado."),
  ),
   part("0:42–0:44", "7 · Équilibre · l’horloge du pied", "7 · Equilibrio · el reloj del pie",
    card("c_clock clock_supported clock_one_hand", "Devant → côté → derrière · 1 série par jambe", "Delante → al lado → detrás · 1 serie por pierna",
      "[CP] On pose les deux mains sur le dossier d’une chaise calée contre le mur et on fixe un point devant. On met le poids sur le pied gauche, genou souple. Pour travailler l’équilibre, on garde ce pied bien ancré pendant que la pointe droite touche devant, sur le côté, puis derrière. On touche près de soi et on revient au centre à chaque fois. Puis on change de pied. [/CP] [C] On garde le pied gauche au sol pendant que le droit fait les mêmes touches. Puis on change de pied. [/C] [MC] Si on se sent stable, on garde une main sur le dossier. [/MC]",
      "[CP] Apoyamos las dos manos en el respaldo, con la silla contra la pared, y miramos un punto fijo delante. Pasamos el peso al pie izquierdo y dejamos la rodilla suave. Para trabajar el equilibrio, sentimos ese pie firme mientras la punta derecha toca delante, al lado y detrás. Tocamos cerca del cuerpo y volvemos al centro cada vez. Después cambiamos de pie. [/CP] [C] Dejamos el pie izquierdo apoyado y hacemos los mismos toques con el derecho. Luego cambiamos. [/C] [MC] Si nos sentimos estables, dejamos una mano en el respaldo. [/MC]"),
  )),
  (part("0:44–0:53", "8 · Sept étirements et mobilisations · sol ou chaise", "8 · Siete estiramientos y movilizaciones · suelo o silla",
    card("c_hinge seated_fold", "1 · Pince douce · 3 souffles", "1 · Pinza suave · 3 respiraciones",
      "[SU] On s’assoit, jambes devant et genoux pliés. [/SU] [C] On s’assoit près du bord, pieds à plat. [/C] On pose les mains sur les cuisses et on se grandit. On se penche depuis les hanches jusqu’à sentir un étirement doux derrière les cuisses. Si ça tire trop, on plie davantage les genoux ou on se redresse un peu.",
      "[SU] Nos sentamos con las piernas delante y las rodillas dobladas. [/SU] [C] Nos sentamos cerca del borde, con los pies apoyados. [/C] Colocamos las manos en los muslos y alargamos la espalda. Nos inclinamos desde las caderas hasta sentir un estiramiento suave detrás de los muslos. Si tira mucho, doblamos más las rodillas o subimos un poco."),
    card("child_chair child", "2 · Enfant adapté · 3 souffles", "2 · Postura del niño adaptada · 3 respiraciones",
      "[SU] À quatre pattes, on recule un peu les hanches vers les talons en laissant les mains au sol. Si les genoux gênent, on prend la chaise. [/SU] [C] On pose les pieds à plat et on laisse les avant-bras reposer sur les cuisses. [/C] On relâche les épaules et on sent le dos et les flancs s’élargir avec le souffle.",
      "[SU] A cuatro patas, llevamos un poco las caderas hacia los talones y dejamos las manos en el suelo. Si molestan las rodillas, usamos la silla. [/SU] [C] Apoyamos los pies y dejamos los antebrazos sobre los muslos. [/C] Soltamos los hombros y sentimos cómo se ensanchan la espalda y los costados al respirar."),
    card("c_twist openbook_f", "3 · Livre ouvert · 2 fois par côté", "3 · Libro abierto · 2 veces por lado",
      "[SU] On s’allonge sur le côté, genoux pliés et joints, les bras devant. On ouvre le bras du dessus et on tourne la poitrine en gardant les genoux ensemble. [/SU] [C] Pieds à plat, on ouvre un bras et on tourne un peu la poitrine, le bassin stable. [/C] On mobilise le haut du dos et on sent la poitrine s’ouvrir. Si l’épaule tire, on plie un peu le coude. On referme, puis on change de côté.",
      "[SU] Nos tumbamos de lado, con las rodillas dobladas y juntas y los brazos delante. Abrimos el brazo de arriba y giramos el pecho, con las rodillas juntas. [/SU] [C] Con los pies apoyados, abrimos un brazo y giramos un poco el pecho, con la pelvis quieta. [/C] Movemos la espalda alta y sentimos cómo se abre el pecho. Si tira el hombro, doblamos un poco el codo. Cerramos y cambiamos de lado."),
    card("chair_sit bridge", "4 · Petit pont · 3 fois", "4 · Puente pequeño · 3 veces",
      "[SU] Sur le dos, on plie les genoux et on pose les pieds à plat sous les genoux. On appuie dans les pieds et on soulève un peu le bassin pour sentir les fessiers et l’arrière des cuisses travailler. On regarde le plafond et on repose le bassin doucement. [/SU] [C] On presse les pieds au sol, fesses sur la chaise. On sent l’appui sous les pieds, puis on relâche. [/C]",
      "[SU] Boca arriba, doblamos las rodillas y ponemos los pies planos debajo de ellas. Empujamos con los pies y levantamos un poco la pelvis para sentir el trabajo de los glúteos y la parte de atrás de los muslos. Miramos al techo y bajamos despacio. [/SU] [C] Presionamos los pies contra el suelo con los glúteos en el asiento. Sentimos el apoyo bajo los pies y soltamos. [/C]"),
    card("chair_sit wipers", "5 · Essuie-glaces · 4 allers-retours", "5 · Limpiaparabrisas · 4 idas y vueltas",
      "[SU] Sur le dos, on plie les genoux et on écarte un peu les pieds. Les épaules restent au sol pendant qu’on laisse les genoux aller un peu à droite, au centre, puis à gauche. Ce petit mouvement mobilise les hanches et se sent autour du bassin et dans le bas du dos. [/SU] [C] Pieds à plat, on ouvre un peu un genou pour sentir la hanche bouger. On garde le buste devant, on revient et on change de côté. [/C]",
      "[SU] Boca arriba, doblamos las rodillas y separamos un poco los pies. Con los hombros apoyados, llevamos las rodillas un poco a la derecha, al centro y a la izquierda. Este movimiento suave se siente alrededor de las caderas y en la zona lumbar. [/SU] [C] Con los pies apoyados, abrimos un poco una rodilla y sentimos cómo se mueve la cadera. Dejamos el pecho al frente, volvemos y cambiamos de lado. [/C]"),
    card("calf_chair calf_floor", "6 · Mollets · 2 souffles par côté", "6 · Pantorrillas · 2 respiraciones por lado",
      "[SU] Sur le dos, on allonge une jambe en gardant l’autre pied à plat. [/SU] [C] On avance un talon et on garde le genou souple. [/C] On garde le talon posé et on ramène doucement les orteils vers le tibia. On fait bouger la cheville et on sent le mollet s’étirer. On relâche, puis on change de côté.",
      "[SU] Boca arriba, estiramos una pierna y dejamos el otro pie apoyado. [/SU] [C] Adelantamos un talón con la rodilla suave. [/C] Dejamos el talón apoyado y acercamos los dedos del pie hacia la espinilla. Así movemos el tobillo y sentimos cómo se estira suavemente la pantorrilla. Soltamos y cambiamos de lado."),
    card("chair_knee knee1_f", "7 · Genou vers la poitrine · 2 souffles par côté", "7 · Rodilla hacia el pecho · 2 respiraciones por lado",
      "[SU] Sur le dos, genoux pliés, on pose les mains derrière une cuisse et on rapproche le genou. L’autre pied reste posé et la tête se repose. On sent un étirement doux dans la fesse ou le bas du dos. [/SU] [C] Le dos long et un pied au sol, on prend l’autre cuisse par-derrière et on la soulève un peu pour sentir la hanche se plier. [/C] Si ça pince dans l’aine, on éloigne le genou. On relâche et on change de côté.",
      "[SU] Boca arriba, con las rodillas dobladas, ponemos las manos detrás de un muslo y acercamos esa rodilla. Dejamos el otro pie en el suelo y la cabeza apoyada. Sentimos un estiramiento suave en el glúteo o en la parte baja de la espalda. [/SU] [C] Con la espalda larga y un pie en el suelo, cogemos el otro muslo por detrás y lo elevamos un poco para sentir cómo se dobla la cadera. [/C] Si pinza la ingle, alejamos la rodilla. Soltamos y cambiamos de lado."),
  ),),
  (part("0:53–0:58", "9 · Relaxation au chaud", "9 · Relajación al abrigo",
    card("c_relax savasana", "Repos · 5 minutes", "Descanso · 5 minutos",
      "[C] On pose le dos contre le dossier et les pieds au sol. [/C] [SU] On s’allonge sur le dos et on plie les genoux, pieds au sol, si c’est plus confortable. [/SU] Si on a froid, on garde une couche. Pour revenir au calme, on relâche la mâchoire, les épaules et les mains. On sent le poids du corps se déposer sur le tapis ou sur la chaise, et on laisse l’air aller et venir. [Silence.]",
      "[C] Apoyamos la espalda en el respaldo y los pies en el suelo. [/C] [SU] Nos tumbamos boca arriba. Si la espalda queda más cómoda, doblamos las rodillas y apoyamos los pies. [/SU] Si hace frío, nos abrigamos. Para volver a la calma, soltamos la mandíbula, los hombros y las manos. Sentimos el peso del cuerpo en la esterilla o la silla y dejamos que el aire entre y salga. [Silencio.]"),
  ),
   part("0:58–1:00", "10 · Clôture", "10 · Cierre",
    card("", "Retour progressif", "Vuelta progresiva",
      "On bouge les doigts et les pieds. Au tapis, on se tourne sur le côté avant de s’asseoir. On sent ses appuis en position assise et on prend trois souffles à son rythme avant de se lever. Merci à toutes. Namasté.",
      "Movemos las manos y los pies. En la esterilla, giramos de lado antes de sentarnos. Sentimos el apoyo al sentarnos y respiramos tres veces, cada una a su ritmo, antes de levantarnos. Gracias a todas. Namasté."),
  )),
]

title = t("Yoga suave · Saludo al sol A", "Yoga doux · Salutation au soleil A")
language = "fr" if fr else "es"
css = legacy["CSS"] + """
.qgrid { align-items: start; }
.qcue { font-size: 11pt; line-height: 1.26; }
.qn { font-size: 11.5pt; }
.qc { padding: 1.4mm 2mm; }
.qf.row2 { flex-wrap: wrap; }
.floor-page .qcue { font-size: 10.5pt; line-height: 1.2; }
.floor-page .vb { margin-block: .45mm; padding-block: .3mm; }
.floor-page .qf svg { max-height: 16mm; }
.floor-page .qgrid.c1 .qc.c2 { flex-direction: row; align-items: center; }
.floor-page .qgrid.c1 .qf.row2 { width: 46mm; gap: 1.5mm; }
"""
top = legacy["P_ALL"][0].replace("Clase 5", "Clase 6").replace("Cours 5", "Cours 6")
top = re.sub(r"<h1>.*?</h1>", f"<h1>{title}</h1>", top)
document = (f'<!doctype html><html lang="{language}"><meta charset="utf-8">'
            f'<title>{title}</title><style>{css}</style><body>')
for index, page in enumerate(pages):
    if index != 1:
        page_class = "pg floor-page" if index == 6 else "pg"
        document += f'<section class="{page_class}">' + (top if index == 0 else "")
    if index == 3:
        document += legacy["part"](1, "De pie, en la silla o en la esterilla", "Debout, sur chaise ou au tapis")
    if index == 6:
        document += legacy["part"](2, "En la silla o en el suelo", "Sur la chaise ou au sol")
    document += "".join(block(*entry) for entry in page)
    if index != 0:
        document += "</section>"
destination = Path(__file__).resolve().parent.parent / "build" / f"yoga_clase6_{language.upper()}.html"
sources = [
    ("Central University of Tamil Nadu · Surya Namaskar and Pranayama", "https://cutn.ac.in/wp-content/uploads/2025/08/MSC_YOGA_SYLLABUS-DPES_CUTN_15082025.pdf"),
    ("Kripalu · Chandra Namaskar", "https://kripalu.org/living-kripalu/chandra-namaskar-honoring-moon-salute"),
    ("American Heart Association · Flexibility Exercise", "https://www.heart.org/en/healthy-living/exercise-and-physical-activity/fitness-basics/flexibility-exercise-stretching/"),
    ("American Heart Association · How to Stay Active in Cold Weather", "https://www.heart.org/en/healthy-living/exercise-and-physical-activity/getting-active/how-to-stay-active-in-cold-weather"),
    ("NHS · Breathing exercises", "https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/"),
    ("CUH · Breathing pattern and physiotherapy", "https://www.cuh.nhs.uk/patient-information/breathing-pattern-disorders-and-physiotherapy/"),
    ("NHS · Sitting exercises", "https://www.nhs.uk/live-well/exercise/sitting-exercises/"),
    ("The Art of Living · Classic Sun Salutation", "https://www.artofliving.org/us-en/yoga/poses/sun-salutation"),
    ("The Art of Living · Cobra", "https://www.artofliving.org/us-en/yoga/poses/cobra-pose"),
    ("Yoga International · Downward-Facing Dog", "https://yogainternational.com/article/view/three-ways-to-practice-downward-facing-dog/"),
    ("Yoga Vastu · Parsvottanasana", "https://yogavastu.com/p/parsvottanasana/"),
    ("Kingston and Richmond NHS · Clock point touches", "https://www.kingstonandrichmond.nhs.uk/patients-and-families/patient-leaflets/home-exercise-programme-falls-prevention"),
    ("CUH · Back mobility exercises", "https://www.cuh.nhs.uk/patient-information/back-mobility-exercises/"),
    ("NHS Dynamic Health · Cat-camel et open book", "https://dynamichealth.nhs.uk/help-and-advice/mid-back-pain/"),
    ("The Art of Living · Child’s pose", "https://www.artofliving.org/us-en/yoga/yoga-poses/child-pose-shishuasana"),
    ("NHS · Flexibility exercises", "https://www.nhs.uk/live-well/exercise/flexibility-exercises/"),
]
links = " · ".join(f'<a href="{url}">{label}</a>' for label, url in sources)
document = document.removesuffix("</section>") + f'<p style="font-size:9pt">{t("Fuentes", "Sources")} — {links}</p></section>'
destination.write_text(document + "</body></html>", encoding="utf-8")
