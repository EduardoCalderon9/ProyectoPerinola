import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Proyecto")

resultados_perinola = ["Pon 1", "Pon 2", "Toma 1", "Toma 2", "Todos Ponen", "Toma Todo"]

cantidad_jugadores = st.text_input("Cantidad de Jugadores")
cantidad_juegos = st.text_input("Cantidad de juegos")
cantidad_rondas = st.text_input("Cantidad de rondas por juego")
st.write(
    "Define un numero alto de rondas si deseas que el juego continue hasta que se vacie el pozo o quede solo un jugador que no haya perdido todo su dinero. "
)
apuesta_inicial_jugador = st.text_input("Apuesta inicial por jugador")
apuesta_inicial_pozo = st.text_input("Apuesta inicial en el pozo")

with st.expander("Especificaciones del juego"):
    st.markdown(
        """Cada jugador tira la perinola en su turno y obtiene uno de seis resultados:"""
    )
    st.markdown(
        """
    - Pon 1
    - Pon 2
    - Toma 1
    - Toma 2
    - Todos Ponen
    - Toma Todo: El jugador toma todo el dinero del pozo y después cada jugador que todavía tiene dinero pone 1 en el pozo para evitar que el juego termine demasiado rápido.
    """
    )

cantidad_jugadores = int(cantidad_jugadores)
cantidad_juegos = int(cantidad_juegos)
cantidad_rondas = int(cantidad_rondas)

apuesta_inicial_jugador = int(apuesta_inicial_jugador)
pozo = int(apuesta_inicial_pozo)

cantidad_ganadores = 0

rondas_para_perdedor = (
    []
)  # Cantidad de rondas que toma para que un jugador se quede sin dinero
rondas_para_ganador = (
    []
)  # Cantidad de rondas que toma para que un jugador sea el ganador del juego

jugadores = np.array(
    [
        {"billetera": apuesta_inicial_jugador, "ganado": 0, "perdido": 0}
        for x in range(int(cantidad_jugadores))
    ]
)

jugadores_perdedores = []
rondas_para_jugador_sin_dinero = []
juegos_para_ganador = []
ganancias_perdidas_por_jugador = []

for i in range(len(jugadores)):
    ganancias_perdidas_por_jugador.append({'ganancias': [], 'perdidas': []})

for i in range(cantidad_juegos):
    st.write(f"Juego {i}")
    jugador_sin_dinero = False
    pozo = int(apuesta_inicial_pozo)
    jugadores_perdedores = []
    jugadores = np.array(
        [
            {"billetera": apuesta_inicial_jugador, "ganado": 0, "perdido": 0}
            for x in range(int(cantidad_jugadores))
        ]
    )
    for k in range(cantidad_rondas):
        #st.write(f'ronda {k}')
        if len(jugadores_perdedores) == len(jugadores) - 1:
            juegos_para_ganador.append(k)
            break
        for j in range(cantidad_jugadores):
            if j not in jugadores_perdedores and pozo > 0:
                #st.write(f"TURNO {j}")
                resultado_actual = np.random.choice(resultados_perinola)
                if resultado_actual == "Toma 1":
                    jugadores[j]["billetera"] += 1
                    jugadores[j]["ganado"] += 1
                    pozo -= 1
                elif resultado_actual == "Toma 2":
                    if pozo == 1:
                        jugadores[j]["billetera"] += 1
                        jugadores[j]["ganado"] += 1
                        pozo -= 1
                    else:
                        jugadores[j]["billetera"] += 2
                        jugadores[j]["ganado"] += 2
                        pozo -= 2
                elif resultado_actual == "Pon 1":
                    if jugadores[j]["billetera"] == 1:
                        print(jugador_sin_dinero)
                        if not jugador_sin_dinero:
                            rondas_para_jugador_sin_dinero.append(k)
                            jugador_sin_dinero = True
                        jugadores_perdedores.append(j)
                        #st.write(f"PERDIO {j}")

                    pozo += 1
                    jugadores[j]["billetera"] -= 1
                    jugadores[j]["perdido"] += 1
                elif resultado_actual == "Pon 2":
                    if jugadores[j]["billetera"] == 2 or jugadores[j]["billetera"] == 1:
                        print(jugador_sin_dinero)
                        if not jugador_sin_dinero:
                            rondas_para_jugador_sin_dinero.append(k)
                            jugador_sin_dinero = True
                        jugadores_perdedores.append(j)
                        #st.write(f"PERDIO {j}")

                        pozo += jugadores[j]["billetera"]
                        jugadores[j]["perdido"] += jugadores[j]["billetera"]
                        jugadores[j]["billetera"] -= jugadores[j]["billetera"]
                    else:
                        pozo += 2
                        jugadores[j]["billetera"] -= 2
                        jugadores[j]["perdido"] += 2
                elif resultado_actual == "Toma Todo":
                    jugadores[j]["billetera"] += pozo
                    jugadores[j]["ganado"] += pozo
                    pozo = 0
                    #st.write(jugadores_perdedores)
                    for jugador in jugadores:
                        if list(jugadores).index(jugador) not in jugadores_perdedores:
                            if jugador["billetera"] == 1:
                                print(jugador_sin_dinero)
                                if not jugador_sin_dinero:
                                    rondas_para_jugador_sin_dinero.append(k)
                                    jugador_sin_dinero = True
                                jugadores_perdedores.append(
                                    list(jugadores).index(jugador)
                                )
                                #st.write(f"PERDIO {list(jugadores).index(jugador)}")
                            #st.write(list(jugadores).index(jugador))
                            jugador["billetera"] -= 1
                            jugador["perdido"] += 1

                    pozo += len(jugadores) - len(jugadores_perdedores)
                elif resultado_actual == "Todos Ponen":
                    for jugador in jugadores:
                        #st.write(list(jugadores).index(jugador))
                        #st.write(jugadores_perdedores)
                        if list(jugadores).index(jugador) not in jugadores_perdedores:
                            if jugador["billetera"] == 1:
                                print(jugador_sin_dinero)
                                if not jugador_sin_dinero:
                                    rondas_para_jugador_sin_dinero.append(k)
                                    jugador_sin_dinero = True
                                jugadores_perdedores.append(
                                    list(jugadores).index(jugador)
                                )
                                #st.write(f"PERDIO {list(jugadores).index(jugador)}")
                            jugador["billetera"] -= 1
                            jugador["perdido"] += 1

                    pozo += len(jugadores) - len(jugadores_perdedores)
    #st.write(jugadores)
    if len(juegos_para_ganador) == i:
        juegos_para_ganador.append(cantidad_rondas)
        
    for jugador in range(len(jugadores)):
        ganancias_perdidas_por_jugador[jugador]['perdidas'].append(jugadores[jugador]['perdido'])
        ganancias_perdidas_por_jugador[jugador]['ganancias'].append(jugadores[jugador]['ganado'])
    #st.write(ganancias_perdidas_por_jugador)
    ganador = max(
            [jugador for jugador in jugadores if jugador not in jugadores_perdedores],
            key=lambda x: x["billetera"],
        )
    #st.write('ganador')
    #st.write(ganador)
st.write(juegos_para_ganador)
st.subheader('¿Cuantos juegos son necesarios para que un jugador se quede sin dinero?', divider='gray')
st.text(f'juegos en los que al menos un jugador se quedo sin dinero: {len(rondas_para_jugador_sin_dinero)}')
st.text(f'Cantidad de rondas promedio para que un jugador se quede sin dinero: {np.mean(rondas_para_jugador_sin_dinero)}')
st.text('rondas para jugador sin dinero')
st.text(rondas_para_jugador_sin_dinero)

st.subheader('¿En cuantos juegos en promedio hay un ganador?', divider='gray')
st.subheader('¿Cómo afecta el número de jugadores al número de juegos para que un jugador se gane todo el dinero?', divider='gray')
st.subheader('Gráfica por jugador de ganancia y pérdida al termino de las simulación', divider='gray')


for i in range(len(jugadores)):
    df = pd.DataFrame({'Ganancias':ganancias_perdidas_por_jugador[i]['ganancias'], 'Perdidas': ganancias_perdidas_por_jugador[i]['perdidas'] })
    st.subheader(f'Ganancias y perdidas de jugador {i+1}', divider='gray')
    st.line_chart(df)
