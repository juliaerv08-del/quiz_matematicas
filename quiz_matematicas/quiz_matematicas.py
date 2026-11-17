import random
import tkinter as tk
from tkinter import messagebox


class QuizMatematicasApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Quiz de Matemáticas Aplicadas")
    self.root.geometry("450x350")

    # Variables de control del juego
    self.nombre_usuario = ""
    self.preguntas = []
    self.preguntas_seleccionadas = []
    self.indice_actual = 0
    self.puntaje = 0
    self.vidas = 3
    self.correctas = 0
    self.incorrectas = 0

    # Cargar las preguntas directamente al iniciar
    self.cargar_preguntas()

    # Iniciar mostrando la pantalla de inicio
    self.crear_pantalla_inicio()

  def cargar_preguntas(self):
    """Carga las preguntas directamente en una lista de diccionarios."""
    self.preguntas = [
        {
            "pregunta": "15 + 27 = ?",
            "respuesta_esperada": "42",
            "dificultad": "1",
            "unidad": "",
        },
        {
            "pregunta": "Raíz cuadrada de 144 = ?",
            "respuesta_esperada": "12",
            "dificultad": "2",
            "unidad": "",
        },
        {
            "pregunta": "(3 + 5) * 2 = ?",
            "respuesta_esperada": "16",
            "dificultad": "2",
            "unidad": "",
        },
        {
            "pregunta": "100 / 4 = ?",
            "respuesta_esperada": "25",
            "dificultad": "1",
            "unidad": "",
        },
        {
            "pregunta": "8 * 7 = ?",
            "respuesta_esperada": "56",
            "dificultad": "1",
            "unidad": "",
        },
    ]

  def limpiar_ventana(self):
    """Elimina todos los widgets actuales de la ventana para cambiar de vista."""
    for widget in self.root.winfo_children():
      widget.destroy()

  def crear_pantalla_inicio(self):
    """Vista 1: Ingreso de nombre del usuario."""
    self.limpiar_ventana()

    titulo = tk.Label(
        self.root,
        text="Quiz de Matemáticas Aplicadas",
        font=("Times New Roman", 16, "bold"),
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    lbl_nombre = tk.Label(
        self.root, text="Ingresa tu nombre:", font=("Times New Roman", 12)
    )
    lbl_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    self.entry_nombre = tk.Entry(self.root, font=("Times New Roman", 12))
    self.entry_nombre.grid(row=1, column=1, padx=10, pady=10)
    self.entry_nombre.focus()

    btn_iniciar = tk.Button(
        self.root,
        text="Comenzar Quiz",
        font=("Times New Roman", 12, "bold"),
        command=self.iniciar_juego,
    )
    btn_iniciar.grid(row=2, column=0, columnspan=2, pady=20)

  def iniciar_juego(self):
    """Valida el nombre y selecciona aleatoriamente 5 preguntas."""
    nombre = self.entry_nombre.get().strip()
    if not nombre:
      messagebox.showwarning(
          "Advertencia", "Por favor ingresa tu nombre para continuar."
      )
      return

    self.nombre_usuario = nombre
    self.preguntas_seleccionadas = random.sample(self.preguntas, 5)
    self.indice_actual = 0
    self.puntaje = 0
    self.vidas = 3
    self.correctas = 0
    self.incorrectas = 0

    self.crear_pantalla_juego()

  def crear_pantalla_juego(self):
    """Vista 2: Muestra la pregunta actual, vidas y puntaje."""
    self.limpiar_ventana()

    p_actual = self.preguntas_seleccionadas[self.indice_actual]

    # Panel superior de estado
    lbl_estado = tk.Label(
        self.root,
        text=(
            f"Jugador: {self.nombre_usuario} | Vidas: {self.vidas} | Puntaje:"
            f" {self.puntaje}"
        ),
        font=("Times New Roman", 10, "italic"),
    )
    lbl_estado.grid(row=0, column=0, columnspan=2, pady=10)

    # Enunciado de la pregunta (con fuente Times New Roman)
    lbl_num_p = tk.Label(
        self.root,
        text=(
            f"Pregunta {self.indice_actual + 1} de 5 (Dificultad:"
            f" {p_actual['dificultad']})"
        ),
        font=("Times New Roman", 12, "bold"),
    )
    lbl_num_p.grid(row=1, column=0, columnspan=2, pady=5)

    lbl_enunciado = tk.Label(
        self.root, text=p_actual["pregunta"], font=("Times New Roman", 14)
    )
    lbl_enunciado.grid(row=2, column=0, columnspan=2, pady=10)

    lbl_resp = tk.Label(
        self.root, text="Tu respuesta:", font=("Times New Roman", 12)
    )
    lbl_resp.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    # Widget Entry principal para la respuesta numérica
    self.entry_respuesta = tk.Entry(self.root, font=("Times New Roman", 12))
    self.entry_respuesta.grid(row=3, column=1, padx=10, pady=10)
    self.entry_respuesta.focus()

    btn_enviar = tk.Button(
        self.root,
        text="Responder",
        font=("Times New Roman", 12),
        command=self.verificar_respuesta,
    )
    btn_enviar.grid(row=4, column=0, columnspan=2, pady=20)

    # Permitir enviar presionando la tecla Enter
    self.root.bind("<Return>", lambda event: self.verificar_respuesta())

  def verificar_respuesta(self):
    """Valida que la entrada sea numérica y evalúa si es correcta o incorrecta."""
    texto_ingresado = self.entry_respuesta.get().strip()

    # Validación de número con try-except (ValueError)
    try:
      respuesta_usuario = float(texto_ingresado)
    except ValueError:
      messagebox.showerror(
          "Error de Validación",
          "Por favor introduce un valor numérico válido.",
      )
      return

    p_actual = self.preguntas_seleccionadas[self.indice_actual]
    respuesta_esperada = float(p_actual["respuesta_esperada"])
    dificultad = int(p_actual["dificultad"])

    # Asignación de puntaje según dificultad (1->5pts, 2->10pts, 3->15pts)
    if dificultad == 1:
      puntos_ganados = 5
    elif dificultad == 2:
      puntos_ganados = 10
    else:
      puntos_ganados = 15

    # Desvincular Enter temporalmente
    self.root.unbind("<Return>")

    # Comprobación de respuesta exacta
    if respuesta_usuario == respuesta_esperada:
      self.puntaje += puntos_ganados
      self.correctas += 1
      messagebox.showinfo(
          "¡Correcto!", f"¡Muy bien! Has ganado {puntos_ganados} puntos."
      )
    else:
      self.vidas -= 1
      self.incorrectas += 1
      messagebox.showerror(
          "Incorrecto",
          f"La respuesta correcta era: {p_actual['respuesta_esperada']}",
      )

    # Verificar si se acabaron las vidas
    if self.vidas <= 0:
      messagebox.showwarning(
          "Game Over", "Te has quedado sin vidas. Fin del juego."
      )
      self.crear_pantalla_resultados()
      return

    # Avanzar a la siguiente pregunta o mostrar resultados
    self.indice_actual += 1
    if self.indice_actual >= len(self.preguntas_seleccionadas):
      self.crear_pantalla_resultados()
    else:
      self.crear_pantalla_juego()

  def crear_pantalla_resultados(self):
    """Vista 3: Muestra el resumen final del puntaje y estadísticas."""
    self.limpiar_ventana()

    titulo = tk.Label(
        self.root, text="¡Resultados Finales!", font=("Times New Roman", 18, "bold")
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    resumen = (
        f"Participante: {self.nombre_usuario}\n\n"
        f"Puntaje Total: {self.puntaje} puntos\n"
        f"Preguntas Correctas: {self.correctas}\n"
        f"Preguntas Incorrectas: {self.incorrectas}\n"
        f"Vidas Restantes: {self.vidas}"
    )

    lbl_resumen = tk.Label(
        self.root, text=resumen, font=("Times New Roman", 12), justify="left"
    )
    lbl_resumen.grid(row=1, column=0, columnspan=2, pady=10)

    btn_reiniciar = tk.Button(
        self.root,
        text="Jugar Nuevamente",
        font=("Times New Roman", 12),
        command=self.crear_pantalla_inicio,
    )
    btn_reiniciar.grid(row=2, column=0, pady=20, padx=10)

    btn_salir = tk.Button(
        self.root,
        text="Salir",
        font=("Times New Roman", 12),
        command=self.root.destroy,
    )
    btn_salir.grid(row=2, column=1, pady=20, padx=10)


if __name__ == "__main__":
  root = tk.Tk()
  app = QuizMatematicasApp(root)
  root.mainloop()