import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Proyecto")
st.write('Repositorio de Github: https://github.com/EduardoCalderon9/ProyectoPerinola')
resultados_perinola = ["Pon 1", "Pon 2", "Toma 1", "Toma 2", "Todos Ponen", "Toma Todo"]

jugadores_cant = st.text_input("Cantidad de Jugadores")
juegos_cant = st.text_input("Cantidad de juegos")
rondas_cant = st.text_input("Cantidad de rondas por juego")
st.write(
    "Define un numero alto de rondas si deseas que el juego continue hasta que se vacie el pozo o quede solo un jugador que no haya perdido todo su dinero. "
)
apuesta_inicial = st.text_input("Apuesta inicial por jugador")
pozo_inicial = st.text_input("Apuesta inicial en el pozo")

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
    st.markdown('Un jugador pierde si llega a tener una billetera vacia (0), despues de esto ya no tirara la perinola en las rondas restantes.')
    st.markdown('Gana el jugador que al finalizar las rondas tiene la mayor cantidad de dinero o cuando todos los jugadores menos uno se quedan sin dinero.')

def simulacion_perinola(cantidad_jugadores, cantidad_juegos, cantidad_rondas, apuesta_inicial_jugador, apuesta_inicial_pozo):
    pozo = apuesta_inicial_pozo

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

    jugadores_perdedores = [] # Jugadores que ya perdieron, se reinicia al inicio de cada juego
    rondas_para_jugador_sin_dinero = [] # Cantidad de rondas para que uno de los jugadores se quede sin dinero
    juegos_para_ganador = [] # Cantidad de rondas necesarias para qwue un jugador se considere ganador
    ganancias_perdidas_por_jugador = [] # lista de ganancias y perdidas de cada jugador en cada juego

    for i in range(len(jugadores)):
        ganancias_perdidas_por_jugador.append({'ganancias': [], 'perdidas': []})

    for i in range(cantidad_juegos):
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
            if len(jugadores_perdedores) == len(jugadores) - 1:
                juegos_para_ganador.append(k)
                break
            for j in range(cantidad_jugadores):
                if j not in jugadores_perdedores and pozo > 0:
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
                            if not jugador_sin_dinero:
                                rondas_para_jugador_sin_dinero.append(k)
                                jugador_sin_dinero = True
                            jugadores_perdedores.append(j)
                        pozo += 1
                        jugadores[j]["billetera"] -= 1
                        jugadores[j]["perdido"] += 1
                    elif resultado_actual == "Pon 2":
                        if jugadores[j]["billetera"] == 2 or jugadores[j]["billetera"] == 1:
                            if not jugador_sin_dinero:
                                rondas_para_jugador_sin_dinero.append(k)
                                jugador_sin_dinero = True
                            jugadores_perdedores.append(j)
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
                        for jugador in jugadores:
                            if list(jugadores).index(jugador) not in jugadores_perdedores:
                                if jugador["billetera"] == 1:
                                    if not jugador_sin_dinero:
                                        rondas_para_jugador_sin_dinero.append(k)
                                        jugador_sin_dinero = True
                                    jugadores_perdedores.append(
                                        list(jugadores).index(jugador)
                                    )
                                jugador["billetera"] -= 1
                                jugador["perdido"] += 1

                        pozo += len(jugadores) - len(jugadores_perdedores)
                    elif resultado_actual == "Todos Ponen":
                        for jugador in jugadores:
                            if list(jugadores).index(jugador) not in jugadores_perdedores:
                                if jugador["billetera"] == 1:
                                    if not jugador_sin_dinero:
                                        rondas_para_jugador_sin_dinero.append(k)
                                        jugador_sin_dinero = True
                                    jugadores_perdedores.append(
                                        list(jugadores).index(jugador)
                                    )
                                jugador["billetera"] -= 1
                                jugador["perdido"] += 1

                        pozo += len(jugadores) - len(jugadores_perdedores)
        if len(juegos_para_ganador) == i:
            juegos_para_ganador.append(cantidad_rondas)
            
        for jugador in range(len(jugadores)):
            ganancias_perdidas_por_jugador[jugador]['perdidas'].append(jugadores[jugador]['perdido'])
            ganancias_perdidas_por_jugador[jugador]['ganancias'].append(jugadores[jugador]['ganado'])
        ganador = max(
                [jugador for jugador in jugadores if jugador not in jugadores_perdedores],
                key=lambda x: x["billetera"],
            )
        
    return rondas_para_jugador_sin_dinero, juegos_para_ganador, ganancias_perdidas_por_jugador
if (jugadores_cant.isdigit() and juegos_cant.isdigit() and rondas_cant.isdigit() and apuesta_inicial.isdigit() and pozo_inicial.isdigit()):  
    rondas_perdedor, rondas_ganador, billeteras = simulacion_perinola(int(jugadores_cant), int(juegos_cant), int(rondas_cant), int(apuesta_inicial), int(pozo_inicial))
    st.subheader('¿Cuantas rondas son necesarios para que un jugador se quede sin dinero?', divider='gray')
    st.text(f'juegos en los que al menos un jugador se quedo sin dinero: {len(rondas_perdedor)}')
    st.text(f'Cantidad de rondas promedio para que un jugador se quede sin dinero: {np.mean(rondas_perdedor)}')
    st.text(f'Cantidad de rondas para jugador sin dinero por juego: {rondas_perdedor}')

    st.subheader('¿En cuantas rondas en promedio hay un ganador?', divider='gray')
    st.text(f'Cantidad de rondas promedio para que un jugador sea el ganador: {np.mean(rondas_ganador)}')
    st.text(f'Cantidad de rondas para jugador ganador por juego: {rondas_ganador}')


    st.subheader('¿Cómo afecta el número de jugadores al número de rondas para que un jugador se gane todo el dinero?', divider='gray')

    st.write('Se corren las simulaciones con el rango de jugadores ingresado.')
    st.write('Para obtener mejores resultados se debe ingresar una cantidad alta de juegos y rondas y una cantidad baja de dinero por jugador y dinero en el pozo.')
    jugadores_min = st.text_input('Cantidad minima de jugadores')
    jugadores_max = st.text_input('Cantidad maxima de jugadores')
    indices_jugadores = []
    sim_rondas = []
    if (jugadores_min.isdigit() and jugadores_max.isdigit()):  
        for i in range(int(jugadores_min), int(jugadores_max) + 1):
            rondas_perdedor_i, rondas_ganador_i, billeteras_i = simulacion_perinola(int(i), int(juegos_cant), int(rondas_cant), int(apuesta_inicial), int(pozo_inicial))
            indices_jugadores.append(i)
            sim_rondas.append(np.mean(rondas_ganador_i))
        sim_df = pd.DataFrame({'Jugadores': indices_jugadores, 'Cantidad de rondas para ganador': sim_rondas })
        sim_df.set_index('Jugadores', inplace=True)
        st.table(sim_df)
        st.line_chart(sim_df)
        st.write('Una mayor cantidad de jugadores resulta en una mayor cantidad de rondas para que uno se considere ganador.')

    st.subheader('Gráfica por jugador de ganancia y pérdida al termino de las simulación', divider='gray')

    for i in range(int(jugadores_cant)):
        df = pd.DataFrame({'Ganancias':billeteras[i]['ganancias'], 'Perdidas': billeteras[i]['perdidas'] })
        st.subheader(f'Ganancias y perdidas de jugador {i+1}', divider='gray')
        st.line_chart(df)
