# ==========================================================
# ZOO AKINATOR RNA
# Juego interactivo tipo Akinator con una RNA profunda y coincidencias exactas
# Sin instalaciones externas: usa solo tkinter, json, math y random.
# Proyecto Cálculo Multivariable
# ==========================================================

import json
import math
import os
import random
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================================
# 1. DATASET INICIAL
# ==========================================================

DATASET_FILE = "dataset_animales_akinator.json"

FEATURES = [
    {
        "key": "pelo",
        "question": "¿Tiene pelo?",
        "type": "binary",
    },
    {
        "key": "plumas",
        "question": "¿Tiene plumas?",
        "type": "binary",
    },
    {
        "key": "vuela",
        "question": "¿Puede volar?",
        "type": "binary",
    },
    {
        "key": "acuatico",
        "question": "¿Vive principalmente en el agua?",
        "type": "binary",
    },
    {
        "key": "carnivoro",
        "question": "¿Es carnívoro?",
        "type": "binary",
    },
    {
        "key": "domestico",
        "question": "¿Es doméstico?",
        "type": "binary",
    },
    {
        "key": "grande",
        "question": "¿Es grande?",
        "type": "binary",
    },
    {
        "key": "nocturno",
        "question": "¿Es nocturno?",
        "type": "binary",
    },
    {
        "key": "rayas",
        "question": "¿Tiene rayas visibles?",
        "type": "binary",
    },
    {
        "key": "cuello_largo",
        "question": "¿Tiene cuello largo?",
        "type": "binary",
    },
    {
        "key": "caparazon",
        "question": "¿Tiene caparazón o concha?",
        "type": "binary",
    },
    {
        "key": "escamas",
        "question": "¿Tiene escamas?",
        "type": "binary",
    },
    {
        "key": "huevos",
        "question": "¿Pone huevos?",
        "type": "binary",
    },
    {
        "key": "patas_norm",
        "question": "¿Cuántas patas tiene aproximadamente?",
        "type": "choice",
        "choices": [
            ("0 patas", 0.0),
            ("2 patas", 0.5),
            ("4 o más patas", 1.0),
        ],
    },
]

INITIAL_ANIMALS = [
    {"name": "perro", "features": [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1.0]},
    {"name": "foca", "features": [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0.0]},
    {"name": "pulpo", "features": [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0.0]},
    {"name": "ballena", "features": [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0.0]},
    {"name": "araña", "features": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1.0]},
    {"name": "ornitorrinco", "features": [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1.0]},
    {"name": "jirafa", "features": [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1.0]},
    {"name": "pez", "features": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0.0]},
    {"name": "hormiga", "features": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1.0]},
    {"name": "búho", "features": [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0.5]},
    {"name": "elefante", "features": [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1.0]},
    {"name": "vaca", "features": [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1.0]},
    {"name": "humano", "features": [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0.5]},
    {"name": "gato", "features": [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1.0]},
    {"name": "tigre", "features": [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1.0]},
    {"name": "pato", "features": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0.5]},
    {"name": "koala", "features": [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1.0]},
    {"name": "pingüino", "features": [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0.5]},
    {"name": "caracol", "features": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0.0]},
    {"name": "murciélago", "features": [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0.5]},
]



def get_initial_animals():
    # Copia profunda del dataset base.
    # Evita que los cambios del juego modifiquen INITIAL_ANIMALS accidentalmente.
    return json.loads(json.dumps(INITIAL_ANIMALS, ensure_ascii=False))


def reset_dataset_file():
    # Sobrescribe el archivo guardado y vuelve exactamente a los 20 animales iniciales.
    animals = get_initial_animals()
    save_animals(animals)
    return animals

# ==========================================================
# 2. UTILIDADES MATEMÁTICAS SIN NUMPY
# ==========================================================


def relu(vec):
    return [max(0.0, x) for x in vec]


def relu_derivative(vec):
    return [1.0 if x > 0 else 0.0 for x in vec]


def sigmoid(vec):
    # Función sigmoide aplicada componente a componente.
    # Se incluye porque la pauta pide comparar funciones de activación.
    return [1.0 / (1.0 + math.exp(-max(min(x, 60.0), -60.0))) for x in vec]


def sigmoid_derivative_from_activation(activated_vec):
    # Si a = sigmoid(z), entonces sigma'(z) = a(1-a).
    return [a * (1.0 - a) for a in activated_vec]


def softmax(vec):
    m = max(vec)
    exps = [math.exp(x - m) for x in vec]
    total = sum(exps)
    return [x / total for x in exps]


def cross_entropy(y_index, prediction):
    eps = 1e-9
    return -math.log(prediction[y_index] + eps)


def zeros(rows, cols):
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def random_matrix(rows, cols, scale=0.2):
    return [[random.uniform(-scale, scale) for _ in range(cols)] for _ in range(rows)]


def matvec(vec, matrix):
    # vec: n, matrix: n x m -> result: m
    return [sum(vec[i] * matrix[i][j] for i in range(len(vec))) for j in range(len(matrix[0]))]


def add_vec(a, b):
    return [a[i] + b[i] for i in range(len(a))]

# ==========================================================
# 3. RED NEURONAL PROFUNDA SIMPLE
# ==========================================================


class DeepAnimalNetwork:
    def __init__(self, input_size, output_size, hidden_layers=(32, 24, 16), learning_rate=0.08, activation="relu"):
        random.seed(42)
        self.layer_sizes = [input_size] + list(hidden_layers) + [output_size]
        self.learning_rate = learning_rate
        self.activation = activation
        self.weights = []
        self.biases = []
        self.weight_path = []

        for i in range(len(self.layer_sizes) - 1):
            self.weights.append(random_matrix(self.layer_sizes[i], self.layer_sizes[i + 1], scale=0.25))
            self.biases.append([0.0 for _ in range(self.layer_sizes[i + 1])])

    def forward(self, x):
        activations = [x]
        z_values = []
        a = x

        for layer in range(len(self.weights) - 1):
            z = add_vec(matvec(a, self.weights[layer]), self.biases[layer])
            if self.activation == "sigmoid":
                a = sigmoid(z)
            else:
                a = relu(z)
            z_values.append(z)
            activations.append(a)

        z_out = add_vec(matvec(a, self.weights[-1]), self.biases[-1])
        a_out = softmax(z_out)
        z_values.append(z_out)
        activations.append(a_out)
        return activations, z_values

    def predict_proba(self, x):
        activations, _ = self.forward(x)
        return activations[-1]

    def average_loss(self, X, y_indices):
        if not X:
            return 0.0
        total = 0.0
        for x, y_index in zip(X, y_indices):
            total += cross_entropy(y_index, self.predict_proba(x))
        return total / len(X)

    def train(self, X, y_indices, epochs=800):
        errors = []
        self.weight_path = []
        n = len(X)

        for epoch in range(epochs):
            total_error = 0.0
            order = list(range(n))
            random.shuffle(order)

            for idx in order:
                x = X[idx]
                y_index = y_indices[idx]
                activations, z_values = self.forward(x)
                pred = activations[-1]
                total_error += cross_entropy(y_index, pred)

                # dZ salida = pred - y
                deltas = [None for _ in self.weights]
                delta_out = pred[:]
                delta_out[y_index] -= 1.0
                deltas[-1] = delta_out

                # Backpropagation capas ocultas
                for layer in range(len(self.weights) - 2, -1, -1):
                    next_delta = deltas[layer + 1]
                    next_weights = self.weights[layer + 1]
                    if self.activation == "sigmoid":
                        deriv = sigmoid_derivative_from_activation(activations[layer + 1])
                    else:
                        deriv = relu_derivative(z_values[layer])
                    delta = []
                    for i in range(self.layer_sizes[layer + 1]):
                        influence = sum(next_delta[j] * next_weights[i][j] for j in range(len(next_delta)))
                        delta.append(influence * deriv[i])
                    deltas[layer] = delta

                # Actualización pesos y sesgos
                for layer in range(len(self.weights)):
                    a_prev = activations[layer]
                    delta = deltas[layer]
                    for i in range(len(self.weights[layer])):
                        for j in range(len(self.weights[layer][0])):
                            self.weights[layer][i][j] -= self.learning_rate * a_prev[i] * delta[j]
                    for j in range(len(self.biases[layer])):
                        self.biases[layer][j] -= self.learning_rate * delta[j]

            avg_error = total_error / n
            errors.append(avg_error)
            if len(self.weights) > 0 and len(self.weights[0]) > 1 and len(self.weights[0][0]) > 0:
                # Guardamos dos pesos como trayectoria 2D para visualizar el descenso del error.
                self.weight_path.append((self.weights[0][0][0], self.weights[0][1][0]))

        return errors

# ==========================================================
# 4. DATASET
# ==========================================================


def normalize_name(name):
    return name.strip().lower()


def load_animals():
    if os.path.exists(DATASET_FILE):
        try:
            with open(DATASET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            pass
    return get_initial_animals()


def save_animals(animals):
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        json.dump(animals, f, ensure_ascii=False, indent=2)


def dataset_to_xy(animals):
    X = [a["features"][:] for a in animals]
    y = list(range(len(animals)))
    names = [a["name"] for a in animals]
    return X, y, names

# ==========================================================
# 5. LÓGICA TIPO AKINATOR
# ==========================================================


def value_matches(feature_value, answer_value, tolerance=0.05):
    return abs(feature_value - answer_value) <= tolerance


def candidate_score(animal_features, answers):
    # Puntaje simple para candidatos: mientras más coincide, mejor.
    if not answers:
        return 1.0

    score = 0.0
    total = 0.0
    for feature_index, answer_value in answers.items():
        feature_type = FEATURES[feature_index]["type"]
        if feature_type == "binary":
            total += 1.0
            if value_matches(animal_features[feature_index], answer_value):
                score += 1.0
        else:
            total += 1.0
            if value_matches(animal_features[feature_index], answer_value, tolerance=0.2):
                score += 1.0
    return score / max(total, 1.0)


def exact_candidate_animals(animals, answers):
    # Devuelve animales que coinciden exactamente con todas las respuestas conocidas.
    # Las respuestas "No sé" no se guardan, por lo tanto no eliminan candidatos.
    matches = []
    for animal in animals:
        ok = True
        for feature_index, answer_value in answers.items():
            feature_type = FEATURES[feature_index]["type"]
            tolerance = 0.05 if feature_type == "binary" else 0.2
            if not value_matches(animal["features"][feature_index], answer_value, tolerance=tolerance):
                ok = False
                break
        if ok:
            matches.append(animal)
    return matches


def same_full_features_group(animals, reference_features):
    # Devuelve animales con el mismo vector completo de características.
    group = []
    for animal in animals:
        if all(value_matches(a, b, tolerance=0.05) for a, b in zip(animal["features"], reference_features)):
            group.append(animal["name"])
    return group


def choose_next_question(animals, answers, asked):
    # Elige la pregunta que mejor divide a los candidatos actuales.
    remaining_indices = [i for i in range(len(FEATURES)) if i not in asked]
    if not remaining_indices:
        return None

    # Candidatos más compatibles con lo respondido hasta ahora.
    # Primero usamos coincidencia exacta con las respuestas conocidas.
    # Si quedan muy pocos, usamos una coincidencia flexible para no bloquear el juego.
    filtered = exact_candidate_animals(animals, answers)
    if len(filtered) < 2:
        filtered = []
        for animal in animals:
            if candidate_score(animal["features"], answers) >= 0.65:
                filtered.append(animal)
    if len(filtered) < 2:
        filtered = animals

    best_idx = remaining_indices[0]
    best_balance = -1.0

    for feature_index in remaining_indices:
        values = [animal["features"][feature_index] for animal in filtered]
        feature_type = FEATURES[feature_index]["type"]

        if feature_type == "binary":
            ones = sum(1 for v in values if v >= 0.5)
            zeros = len(values) - ones
            balance = min(ones, zeros) / max(len(values), 1)
        else:
            counts = {0.0: 0, 0.5: 0, 1.0: 0}
            for v in values:
                closest = min(counts.keys(), key=lambda c: abs(c - v))
                counts[closest] += 1
            balance = 1.0 - (max(counts.values()) / max(len(values), 1))

        if balance > best_balance:
            best_balance = balance
            best_idx = feature_index

    return best_idx

# ==========================================================
# 6. INTERFAZ GRÁFICA
# ==========================================================


class ZooAkinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoo RNA")
        self.root.geometry("880x620")
        self.root.minsize(820, 560)

        self.animals = load_animals()
        self.network = None
        self.errors = []
        self.answers = {}
        self.asked = []
        self.current_question_index = None
        self.last_ranking = []
        self.training_runs = 0
        self.last_error_summary = ""
        self._graph_redraw_after_id = None
        self._surface_redraw_after_id = None
        self.zoo_image = None
        self.activation_name = tk.StringVar(value="relu")
        self.learning_rate_var = tk.StringVar(value="0.06")

        self.setup_style()
        self.build_ui()

        # Importante: mostramos primero la ventana y entrenamos después.
        # Así, en computadores más lentos, no parece que el programa "no abre".
        if hasattr(self, "dataset_label"):
            self.dataset_label.config(text=f"Animales cargados: {len(self.animals)} | Preparando red...")
        self.root.after(150, self.start_app)

    def setup_style(self):
        # Paleta inspirada en la presentación verde/blanca de zoológico:
        # fondo verde suave, tarjetas crema, acentos hoja y detalles cálidos.
        self.bg = "#AFC79A"          # verde safari suave
        self.card = "#FFF8E8"        # crema cálido
        self.text = "#31412E"        # verde bosque oscuro
        self.accent = "#4F8A4B"      # verde hoja principal
        self.accent_dark = "#2F6130" # verde profundo
        self.soft = "#DDE8C8"        # verde muy claro
        self.warm = "#F2B84B"        # amarillo cálido tipo ilustración
        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")

        # Pestañas
        style.configure("TNotebook", background=self.bg, borderwidth=0, tabmargins=(6, 4, 6, 0))
        style.configure(
            "TNotebook.Tab",
            background="#DCE9C8",
            foreground=self.text,
            padding=(20, 10),
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.card), ("active", "#EEF5DD")],
            foreground=[("selected", self.accent_dark), ("active", self.accent_dark)],
        )

        # Fondos y textos
        style.configure("TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.card)
        style.configure("Title.TLabel", background=self.bg, foreground="white", font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=self.bg, foreground="#F8FFE9", font=("Segoe UI", 11))
        style.configure("CardTitle.TLabel", background=self.card, foreground=self.accent_dark, font=("Segoe UI", 19, "bold"))
        style.configure("CardText.TLabel", background=self.card, foreground=self.text, font=("Segoe UI", 12))
        style.configure("BigQuestion.TLabel", background=self.card, foreground=self.accent_dark, font=("Segoe UI", 23, "bold"))

        # Botones: mismos botones y funciones, solo estilo visual.
        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=9,
            background=self.accent,
            foreground="white",
            borderwidth=0,
            focusthickness=0,
        )
        style.map(
            "TButton",
            background=[("active", self.accent_dark), ("pressed", "#234D25"), ("disabled", "#B7C4AA")],
            foreground=[("disabled", "#EEF2E7")],
        )
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=9, background=self.warm, foreground=self.text)

    def start_app(self):
        try:
            self.train_network()
            self.new_game()
        except Exception as e:
            messagebox.showerror("Error al iniciar", f"Ocurrió un error al entrenar o abrir el juego:\n\n{e}")

    def build_ui(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=22, pady=(18, 8))

        ttk.Label(header, text="Zoo RNA", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Piensa en un animal, responde las preguntas y la red intentará adivinarlo.  🌿 🐘 🐒 🦜",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=22, pady=12)

        self.tab_inicio = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_juego = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_resultado = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_aprender = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_error = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_superficie = ttk.Frame(self.notebook, style="Card.TFrame")

        self.notebook.add(self.tab_inicio, text="Inicio")
        self.notebook.add(self.tab_juego, text="Preguntas")
        self.notebook.add(self.tab_resultado, text="Resultado")
        self.notebook.add(self.tab_aprender, text="Aprender")
        self.notebook.add(self.tab_error, text="Error")
        self.notebook.add(self.tab_superficie, text="Superficie")

        self.build_inicio_tab()
        self.build_juego_tab()
        self.build_resultado_tab()
        self.build_aprender_tab()
        self.build_error_tab()
        self.build_superficie_tab()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def find_zoo_image_path(self):
        # Busca una versión PNG de la imagen del zoológico.
        # Tkinter carga PNG sin instalar librerías externas; JPG no siempre funciona en todos los computadores.
        script_dir = Path(__file__).resolve().parent
        home = Path.home()
        candidates = [
            script_dir / "zoo_header.png",
            script_dir / "zoo.png",
            script_dir / "zoo.jpg",
            script_dir / "zoo.jpeg",
            script_dir / "zoo" / "zoo_header.png",
            script_dir / "zoo" / "zoo.png",
            script_dir / "zoo" / "zoo.jpg",
            script_dir / "zoo" / "zoo.jpeg",
            home / "Desktop" / "zoo" / "zoo_header.png",
            home / "Desktop" / "zoo" / "zoo.png",
            home / "Desktop" / "zoo" / "zoo.jpg",
            home / "Desktop" / "zoo" / "zoo.jpeg",
            home / "Escritorio" / "zoo" / "zoo_header.png",
            home / "Escritorio" / "zoo" / "zoo.png",
            home / "Escritorio" / "zoo" / "zoo.jpg",
            home / "Escritorio" / "zoo" / "zoo.jpeg",
            Path("/mnt/data/zoo_header.png"),
            Path("/mnt/data/zoo.png"),
            Path("/mnt/data/zoo.jpg"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def load_zoo_photo(self):
        image_path = self.find_zoo_image_path()
        if image_path is None:
            return None

        # Tkinter suele leer PNG, pero JPG depende de la versión de Tcl/Tk.
        # Si la imagen está en JPG e instala Pillow, la convertimos automáticamente a PNG.
        # Si Pillow no está disponible, el programa sigue funcionando sin la imagen.
        if image_path.suffix.lower() in (".jpg", ".jpeg"):
            converted_path = image_path.with_name("zoo_header.png")
            if not converted_path.exists():
                try:
                    from PIL import Image
                    pil_img = Image.open(image_path)
                    pil_img = pil_img.resize((360, 203))
                    pil_img.save(converted_path)
                    image_path = converted_path
                except Exception:
                    pass
            elif converted_path.exists():
                image_path = converted_path

        try:
            img = tk.PhotoImage(file=str(image_path))
            # Si se usa la imagen grande, la reducimos para que sea decorativa y no distraiga.
            if img.width() > 420:
                factor = max(1, img.width() // 360)
                img = img.subsample(factor, factor)
            return img
        except Exception:
            return None

    def build_inicio_tab(self):
        frame = self.tab_inicio

        # La pestaña Inicio ahora es desplazable.
        # Así, si la ventana queda más baja o Windows cambia el escalado,
        # ningún botón queda perdido fuera de la pantalla.
        outer = ttk.Frame(frame, style="Card.TFrame")
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=self.card,
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        box = ttk.Frame(canvas, style="Card.TFrame")
        window_id = canvas.create_window((0, 0), window=box, anchor="nw")

        def _update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _resize_inner(event):
            canvas.itemconfigure(window_id, width=event.width)

        def _mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        box.bind("<Configure>", _update_scrollregion)
        canvas.bind("<Configure>", _resize_inner)
        canvas.bind_all("<MouseWheel>", _mousewheel)

        content = ttk.Frame(box, style="Card.TFrame")
        content.pack(fill="both", expand=True, padx=22, pady=18)

        ttk.Label(content, text="Modo juego", style="CardTitle.TLabel").pack(anchor="w", pady=(2, 8))
        ttk.Label(
            content,
            text=(
                "1. Piensa en un animal.\n"
                "2. Responde una pregunta por pantalla.\n"
                "3. La red neuronal mostrará los 4 animales más probables.\n"
                "4. Si falla, puedes enseñarle el animal correcto."
            ),
            style="CardText.TLabel",
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        self.dataset_label = ttk.Label(content, text="", style="CardText.TLabel")
        self.dataset_label.pack(anchor="w", pady=(0, 10))

        settings = ttk.Frame(content, style="Card.TFrame")
        settings.pack(anchor="w", pady=(0, 10))
        ttk.Label(settings, text="Activación:", style="CardText.TLabel").pack(side="left", padx=(0, 8))
        ttk.Combobox(
            settings,
            textvariable=self.activation_name,
            values=("relu", "sigmoid"),
            state="readonly",
            width=10,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(0, 18))
        ttk.Label(settings, text="η:", style="CardText.TLabel").pack(side="left", padx=(0, 8))
        ttk.Entry(settings, textvariable=self.learning_rate_var, width=8, font=("Segoe UI", 11)).pack(side="left")

        self.build_config_table(content)

        # Botones en grilla compacta para que no se salgan de la ventana.
        buttons = ttk.Frame(content, style="Card.TFrame")
        buttons.pack(fill="x", pady=(6, 0))

        button_specs = [
            ("Nueva partida", self.new_game),
            ("Reentrenar con estos parámetros", self.retrain_from_button),
            ("Ver gráfico de error", lambda: self.notebook.select(self.tab_error)),
            ("Ver superficie de error", lambda: self.notebook.select(self.tab_superficie)),
            ("Reiniciar a los 20 animales iniciales", self.reset_to_initial_animals),
            ("Refrescar todo desde cero", self.refresh_everything),
        ]

        for index, (text, command) in enumerate(button_specs):
            row = index // 3
            col = index % 3
            ttk.Button(buttons, text=text, command=command).grid(
                row=row,
                column=col,
                sticky="ew",
                padx=5,
                pady=5,
            )

        for col in range(3):
            buttons.columnconfigure(col, weight=1, uniform="inicio_buttons")

        ttk.Label(
            content,
            text="Tip: para jugar y presentar, usa ReLU con η = 0.06. Cambia a Sigmoid solo para comparar activaciones.",
            style="CardText.TLabel",
            wraplength=1000,
        ).pack(anchor="w", pady=(10, 0))

    def build_config_table(self, parent):
        table_box = tk.Frame(parent, bg="#FFFDF2", padx=10, pady=10, highlightthickness=1, highlightbackground=self.soft)
        table_box.pack(anchor="w", fill="x", pady=(2, 14))

        title = tk.Label(
            table_box,
            text="Configuración recomendada",
            bg="#FFFDF2",
            fg=self.accent_dark,
            font=("Segoe UI", 12, "bold"),
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        headers = ["Caso", "Activación", "η recomendado"]
        rows = [
            ("Jugar normal / demostrar que funciona", "ReLU", "0.06"),
            ("Mostrar comparación para el informe", "Sigmoid", "0.03 o 0.04"),
            ("Si el error baja muy lento", "ReLU", "0.08"),
            ("Si el gráfico se vuelve inestable o raro", "ReLU", "0.03"),
        ]

        for col, header in enumerate(headers):
            tk.Label(
                table_box,
                text=header,
                bg=self.soft,
                fg=self.text,
                font=("Segoe UI", 10, "bold"),
                padx=8,
                pady=5,
                anchor="w",
            ).grid(row=1, column=col, sticky="ew", padx=1, pady=1)

        for row_idx, row_values in enumerate(rows, start=2):
            for col, value in enumerate(row_values):
                tk.Label(
                    table_box,
                    text=value,
                    bg="#FFFDF2",
                    fg=self.text,
                    font=("Segoe UI", 10),
                    padx=8,
                    pady=5,
                    anchor="w",
                ).grid(row=row_idx, column=col, sticky="ew", padx=1, pady=1)

        table_box.columnconfigure(0, weight=3)
        table_box.columnconfigure(1, weight=1)
        table_box.columnconfigure(2, weight=1)

    def build_juego_tab(self):
        frame = self.tab_juego
        box = ttk.Frame(frame, style="Card.TFrame")
        box.pack(fill="both", expand=True, padx=35, pady=30)

        self.progress_label = ttk.Label(box, text="Pregunta 1", style="CardText.TLabel")
        self.progress_label.pack(anchor="w", pady=(5, 15))

        self.question_label = ttk.Label(box, text="", style="BigQuestion.TLabel", wraplength=720, justify="center")
        self.question_label.pack(fill="x", pady=(25, 35))

        self.answer_area = ttk.Frame(box, style="Card.TFrame")
        self.answer_area.pack(fill="x", pady=10)

        nav = ttk.Frame(box, style="Card.TFrame")
        nav.pack(fill="x", pady=(30, 5))

        ttk.Button(nav, text="Volver al inicio", command=lambda: self.notebook.select(self.tab_inicio)).pack(side="left")
        ttk.Button(nav, text="Intentar adivinar ahora", command=self.show_result).pack(side="right")

    def build_resultado_tab(self):
        frame = self.tab_resultado
        box = ttk.Frame(frame, style="Card.TFrame")
        box.pack(fill="both", expand=True, padx=35, pady=30)

        ttk.Label(box, text="Mi intento", style="CardTitle.TLabel").pack(anchor="w", pady=(5, 10))

        self.result_text = tk.Text(
            box,
            height=11,
            wrap="word",
            font=("Segoe UI", 13),
            bg="#FFFDF2",
            fg=self.text,
            relief="flat",
            padx=16,
            pady=14,
            highlightthickness=1,
            highlightbackground=self.soft,
            insertbackground=self.text,
        )
        self.result_text.pack(fill="x", pady=(8, 18))
        self.result_text.config(state="disabled")

        buttons = ttk.Frame(box, style="Card.TFrame")
        buttons.pack(fill="x", pady=8)

        ttk.Button(buttons, text="Sí, acertó", command=self.correct_guess).pack(side="left", padx=(0, 10))
        ttk.Button(buttons, text="No, aprender animal", command=lambda: self.notebook.select(self.tab_aprender)).pack(side="left", padx=10)
        ttk.Button(buttons, text="Nueva partida", command=self.new_game).pack(side="right")

    def build_aprender_tab(self):
        frame = self.tab_aprender
        box = ttk.Frame(frame, style="Card.TFrame")
        box.pack(fill="both", expand=True, padx=35, pady=30)

        ttk.Label(box, text="Enséñame el animal correcto", style="CardTitle.TLabel").pack(anchor="w", pady=(5, 15))
        ttk.Label(
            box,
            text="Escribe el nombre del animal que estabas pensando. Usaré tus respuestas de esta partida como sus características.",
            style="CardText.TLabel",
            wraplength=720,
        ).pack(anchor="w", pady=(0, 16))

        row = ttk.Frame(box, style="Card.TFrame")
        row.pack(fill="x", pady=8)
        ttk.Label(row, text="Animal correcto:", style="CardText.TLabel").pack(side="left")
        self.learn_entry = ttk.Entry(row, font=("Segoe UI", 12), width=30)
        self.learn_entry.pack(side="left", padx=12)

        ttk.Button(box, text="Guardar y reentrenar", command=self.learn_current_animal).pack(anchor="w", pady=18)

        self.learn_status = ttk.Label(box, text="", style="CardText.TLabel")
        self.learn_status.pack(anchor="w", pady=8)

    def build_error_tab(self):
        frame = self.tab_error
        box = ttk.Frame(frame, style="Card.TFrame")
        box.pack(fill="both", expand=True, padx=35, pady=30)

        ttk.Label(box, text="Error relativo durante el entrenamiento", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            box,
            text="La curva muestra la entropía cruzada relativa: 100% corresponde al error inicial del entrenamiento actual.",
            style="CardText.TLabel",
        ).pack(anchor="w", pady=(4, 12))

        self.error_status_label = ttk.Label(box, text="", style="CardText.TLabel")
        self.error_status_label.pack(anchor="w", pady=(0, 8))

        self.error_canvas = tk.Canvas(box, bg="#FFFDF2", height=330, highlightthickness=1, highlightbackground=self.soft)
        self.error_canvas.pack(fill="both", expand=True, pady=10)
        self.error_canvas.bind("<Configure>", self.schedule_error_graph_redraw)

        error_buttons = ttk.Frame(box, style="Card.TFrame")
        error_buttons.pack(anchor="w", pady=8)

        ttk.Button(error_buttons, text="Reentrenar y actualizar gráfico", command=self.retrain_from_button).pack(side="left", padx=(0, 10))
        ttk.Button(error_buttons, text="Reiniciar gráfico", command=self.reset_error_graph).pack(side="left", padx=(0, 10))
        ttk.Button(error_buttons, text="Refrescar todo", command=self.refresh_everything).pack(side="left")

    def build_superficie_tab(self):
        frame = self.tab_superficie
        box = ttk.Frame(frame, style="Card.TFrame")
        box.pack(fill="both", expand=True, padx=35, pady=30)

        ttk.Label(box, text="Superficie de error y trayectoria de pesos", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            box,
            text=(
                "Esta visualización toma dos pesos de la primera capa y calcula cómo cambia la función de costo J. "
                "La línea muestra cómo esos pesos se desplazaron durante el entrenamiento."
            ),
            style="CardText.TLabel",
            wraplength=760,
        ).pack(anchor="w", pady=(4, 12))

        self.surface_status_label = ttk.Label(box, text="", style="CardText.TLabel")
        self.surface_status_label.pack(anchor="w", pady=(0, 8))

        self.surface_canvas = tk.Canvas(box, bg="#FFFDF2", height=360, highlightthickness=1, highlightbackground=self.soft)
        self.surface_canvas.pack(fill="both", expand=True, pady=10)
        self.surface_canvas.bind("<Configure>", self.schedule_surface_redraw)

        surface_buttons = ttk.Frame(box, style="Card.TFrame")
        surface_buttons.pack(anchor="w", pady=8)
        ttk.Button(surface_buttons, text="Actualizar superficie", command=self.draw_surface_graph).pack(side="left", padx=(0, 10))
        ttk.Button(surface_buttons, text="Reentrenar y actualizar", command=self.retrain_from_button).pack(side="left")

    def schedule_surface_redraw(self, event=None):
        if not hasattr(self, "root"):
            return
        if self._surface_redraw_after_id is not None:
            try:
                self.root.after_cancel(self._surface_redraw_after_id)
            except Exception:
                pass
        self._surface_redraw_after_id = self.root.after(180, self.draw_surface_graph)

    def surface_color(self, value, min_value, max_value):
        # Escala suave crema -> verde oscuro. Valor bajo = más claro; valor alto = más oscuro.
        ratio = 0.0 if max_value == min_value else (value - min_value) / (max_value - min_value)
        ratio = max(0.0, min(1.0, ratio))
        start = (255, 248, 232)
        end = (79, 138, 75)
        r = int(start[0] + ratio * (end[0] - start[0]))
        g = int(start[1] + ratio * (end[1] - start[1]))
        b = int(start[2] + ratio * (end[2] - start[2]))
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_surface_graph(self):
        self._surface_redraw_after_id = None
        if not hasattr(self, "surface_canvas"):
            return

        canvas = self.surface_canvas
        canvas.delete("all")
        canvas.update_idletasks()
        width = canvas.winfo_width() or 760
        height = canvas.winfo_height() or 340

        if self.network is None or not self.errors:
            canvas.create_text(width / 2, height / 2, text="Entrena la red para ver la superficie.", font=("Segoe UI", 12, "bold"), fill=self.text)
            return

        X, y, _ = dataset_to_xy(self.animals)
        if not X:
            return

        path = self.network.weight_path or []
        if path:
            xs = [p[0] for p in path]
            ys = [p[1] for p in path]
            cx = xs[-1]
            cy = ys[-1]
            span = max(max(xs) - min(xs), max(ys) - min(ys), 0.8) * 1.25
        else:
            cx = self.network.weights[0][0][0]
            cy = self.network.weights[0][1][0]
            span = 1.0

        steps = 26
        half = span / 2
        x_values = [cx - half + span * i / (steps - 1) for i in range(steps)]
        y_values = [cy - half + span * j / (steps - 1) for j in range(steps)]

        original_w1 = self.network.weights[0][0][0]
        original_w2 = self.network.weights[0][1][0]
        losses = []
        for wy in y_values:
            row = []
            for wx in x_values:
                self.network.weights[0][0][0] = wx
                self.network.weights[0][1][0] = wy
                row.append(self.network.average_loss(X, y))
            losses.append(row)
        self.network.weights[0][0][0] = original_w1
        self.network.weights[0][1][0] = original_w2

        flat = [v for row in losses for v in row]
        min_loss = min(flat)
        max_loss = max(flat)

        margin_left = 72
        margin_top = 42
        margin_right = 34
        margin_bottom = 58
        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom
        cell_w = plot_w / steps
        cell_h = plot_h / steps

        canvas.create_rectangle(margin_left, margin_top, width - margin_right, height - margin_bottom, fill="#FFFDF2", outline=self.soft)
        for j, row in enumerate(losses):
            for i, loss in enumerate(row):
                x0 = margin_left + i * cell_w
                y0 = margin_top + (steps - 1 - j) * cell_h
                canvas.create_rectangle(
                    x0, y0, x0 + cell_w + 1, y0 + cell_h + 1,
                    fill=self.surface_color(loss, min_loss, max_loss),
                    outline="",
                )

        def map_x(weight):
            return margin_left + ((weight - x_values[0]) / max(x_values[-1] - x_values[0], 1e-9)) * plot_w

        def map_y(weight):
            return height - margin_bottom - ((weight - y_values[0]) / max(y_values[-1] - y_values[0], 1e-9)) * plot_h

        # Trajectory of two selected weights. Sampled so it remains readable.
        if len(path) >= 2:
            step = max(1, len(path) // 180)
            sampled = path[::step]
            if sampled[-1] != path[-1]:
                sampled.append(path[-1])
            points = [(map_x(a), map_y(b)) for a, b in sampled]
            for i in range(len(points) - 1):
                canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=self.accent_dark, width=2)
            canvas.create_oval(points[0][0] - 4, points[0][1] - 4, points[0][0] + 4, points[0][1] + 4, fill=self.warm, outline=self.accent_dark)
            canvas.create_oval(points[-1][0] - 5, points[-1][1] - 5, points[-1][0] + 5, points[-1][1] + 5, fill=self.accent_dark, outline=self.accent_dark)

        canvas.create_line(margin_left, height - margin_bottom, width - margin_right, height - margin_bottom, fill=self.accent_dark, width=2)
        canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom, fill=self.accent_dark, width=2)
        canvas.create_text(width / 2, 20, text="J(W,b) variando dos pesos", font=("Segoe UI", 12, "bold"), fill=self.text)
        canvas.create_text(width / 2, height - 22, text="Peso W[0][0]", font=("Segoe UI", 10, "bold"), fill=self.text)
        canvas.create_text(28, height / 2, text="W[1][0]", font=("Segoe UI", 10, "bold"), fill=self.text)
        canvas.create_text(margin_left, height - margin_bottom + 18, text=f"{x_values[0]:.2f}", font=("Segoe UI", 9), fill=self.text)
        canvas.create_text(width - margin_right, height - margin_bottom + 18, text=f"{x_values[-1]:.2f}", font=("Segoe UI", 9), fill=self.text)
        canvas.create_text(margin_left - 8, height - margin_bottom, text=f"{y_values[0]:.2f}", anchor="e", font=("Segoe UI", 9), fill=self.text)
        canvas.create_text(margin_left - 8, margin_top, text=f"{y_values[-1]:.2f}", anchor="e", font=("Segoe UI", 9), fill=self.text)

        if hasattr(self, "surface_status_label"):
            self.surface_status_label.config(
                text=f"Activación: {self.network.activation} | η={self.network.learning_rate} | J mín. visualizada: {min_loss:.4f} | J máx.: {max_loss:.4f}"
            )

    def train_network(self):
        X, y, names = dataset_to_xy(self.animals)
        try:
            learning_rate = float(self.learning_rate_var.get())
        except Exception:
            learning_rate = 0.06
            self.learning_rate_var.set("0.06")
        learning_rate = max(0.001, min(learning_rate, 1.0))

        activation = self.activation_name.get() if hasattr(self, "activation_name") else "relu"
        if activation not in ("relu", "sigmoid"):
            activation = "relu"
            self.activation_name.set("relu")

        self.network = DeepAnimalNetwork(
            input_size=len(FEATURES),
            output_size=len(names),
            hidden_layers=(32, 24, 16),
            learning_rate=learning_rate,
            activation=activation,
        )
        self.errors = self.network.train(X, y, epochs=650)
        self.training_runs += 1
        self.update_error_summary()
        self.schedule_error_graph_redraw()
        self.schedule_surface_redraw()
        if hasattr(self, "dataset_label"):
            self.dataset_label.config(text=f"Animales aprendidos: {len(self.animals)}")

    def retrain_from_button(self):
        self.train_network()
        # Forzamos el redibujado después de que tkinter haya recalculado tamaños.
        self.root.after(80, self.draw_error_graph)
        messagebox.showinfo("Listo", "La red fue reentrenada y el gráfico se actualizó.")

    def on_tab_changed(self, event=None):
        if hasattr(self, "notebook") and hasattr(self, "tab_error"):
            if self.notebook.select() == str(self.tab_error):
                self.schedule_error_graph_redraw()
            if hasattr(self, "tab_superficie") and self.notebook.select() == str(self.tab_superficie):
                self.schedule_surface_redraw()

    def schedule_error_graph_redraw(self, event=None):
        if not hasattr(self, "root"):
            return
        if self._graph_redraw_after_id is not None:
            try:
                self.root.after_cancel(self._graph_redraw_after_id)
            except Exception:
                pass
        self._graph_redraw_after_id = self.root.after(120, self.draw_error_graph)

    def update_error_summary(self):
        if not self.errors:
            self.last_error_summary = "Todavía no hay datos de entrenamiento."
            return
        initial = max(self.errors[0], 1e-9)
        final = self.errors[-1]
        reduction = max(0.0, (1.0 - final / initial) * 100)
        self.last_error_summary = (
            f"Entrenamiento #{self.training_runs} | "
            f"Animales: {len(self.animals)} | "
            f"Error inicial: {initial:.4f} | "
            f"Error final: {final:.4f} | "
            f"Reducción: {reduction:.1f}%"
        )
        if hasattr(self, "error_status_label"):
            self.error_status_label.config(text=self.last_error_summary)

    def draw_error_graph(self):
        self._graph_redraw_after_id = None
        if not hasattr(self, "error_canvas"):
            return

        canvas = self.error_canvas
        canvas.delete("all")
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 100 or height < 100:
            width = 760
            height = 300
        margin_left = 58
        margin_right = 28
        margin_top = 42
        margin_bottom = 58

        if hasattr(self, "error_status_label"):
            self.error_status_label.config(text=self.last_error_summary)

        if not self.errors:
            canvas.create_text(width / 2, height / 2, text="Sin datos para graficar todavía", font=("Segoe UI", 12, "bold"), fill=self.text)
            return

        # Convertimos la entropía cruzada a porcentaje relativo para que el gráfico sea fácil de leer.
        initial = max(self.errors[0], 1e-9)
        percent_errors = [(e / initial) * 100 for e in self.errors]
        max_y = max(percent_errors)
        min_y = min(percent_errors)
        # Damos un pequeño colchón visual para que la curva no quede pegada al borde.
        padding = max((max_y - min_y) * 0.08, 1.0)
        y_top = max_y + padding
        y_bottom = max(0.0, min_y - padding)
        y_range = max(y_top - y_bottom, 1e-9)

        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom

        # Fondo suave del área del gráfico
        canvas.create_rectangle(margin_left, margin_top, width - margin_right, height - margin_bottom, fill="#FFFDF2", outline=self.soft)

        # Líneas de grilla y etiquetas Y
        for k in range(5):
            y_val = y_bottom + (y_range * k / 4)
            y = height - margin_bottom - ((y_val - y_bottom) / y_range) * plot_h
            canvas.create_line(margin_left, y, width - margin_right, y, fill="#E9E4C8")
            canvas.create_text(margin_left - 8, y, text=f"{y_val:.0f}%", anchor="e", font=("Segoe UI", 9), fill=self.text)

        # Ejes
        canvas.create_line(margin_left, height - margin_bottom, width - margin_right, height - margin_bottom, fill=self.accent_dark, width=2)
        canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom, fill=self.accent_dark, width=2)

        canvas.create_text(width / 2, 20, text="Error relativo durante el entrenamiento", font=("Segoe UI", 12, "bold"), fill=self.text)
        canvas.create_text(width / 2, height - 22, text="Épocas", font=("Segoe UI", 10, "bold"), fill=self.text)
        canvas.create_text(18, height / 2, text="%", font=("Segoe UI", 10, "bold"), fill=self.text)

        # Etiquetas X
        canvas.create_text(margin_left, height - margin_bottom + 18, text="0", font=("Segoe UI", 9), fill=self.text)
        canvas.create_text(width - margin_right, height - margin_bottom + 18, text=str(len(percent_errors) - 1), font=("Segoe UI", 9), fill=self.text)

        # Muestreamos para no dibujar 900 puntos si no es necesario.
        points = []
        step = max(1, len(percent_errors) // 300)
        sampled = percent_errors[::step]
        if percent_errors[-1] != sampled[-1]:
            sampled.append(percent_errors[-1])

        for i, val in enumerate(sampled):
            x = margin_left + (i / max(len(sampled) - 1, 1)) * plot_w
            y = height - margin_bottom - ((val - y_bottom) / y_range) * plot_h
            points.append((x, y))

        # Curva principal
        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=self.accent, width=3, smooth=True)

        # Puntos inicial y final
        if points:
            canvas.create_oval(points[0][0] - 4, points[0][1] - 4, points[0][0] + 4, points[0][1] + 4, fill=self.warm, outline=self.accent_dark)
            canvas.create_oval(points[-1][0] - 4, points[-1][1] - 4, points[-1][0] + 4, points[-1][1] + 4, fill=self.accent_dark, outline=self.accent_dark)

        canvas.create_text(
            width / 2,
            height - 6,
            text=f"Inicial: {percent_errors[0]:.1f}%    Final: {percent_errors[-1]:.1f}%    Entrenamiento #{self.training_runs}",
            font=("Segoe UI", 10, "bold"),
            fill=self.text,
        )


    def reset_error_graph(self):
        confirm = messagebox.askyesno(
            "Reiniciar gráfico",
            "Esto limpiará el gráfico actual y volverá a entrenar la red para generar una curva nueva desde cero.\n\n"
            "No borrará animales aprendidos.\n\n"
            "¿Quieres continuar?"
        )
        if not confirm:
            return

        if self._graph_redraw_after_id is not None:
            try:
                self.root.after_cancel(self._graph_redraw_after_id)
            except Exception:
                pass
            self._graph_redraw_after_id = None

        self.errors = []
        self.training_runs = 0
        self.last_error_summary = "Gráfico reiniciado. Reentrenando la red..."
        if hasattr(self, "error_status_label"):
            self.error_status_label.config(text=self.last_error_summary)
        if hasattr(self, "error_canvas"):
            self.error_canvas.delete("all")
            self.error_canvas.create_text(
                self.error_canvas.winfo_width() / 2 or 380,
                self.error_canvas.winfo_height() / 2 or 160,
                text="Reentrenando...",
                font=("Segoe UI", 12, "bold"),
                fill=self.text,
            )

        self.train_network()
        self.root.after(100, self.draw_error_graph)
        messagebox.showinfo("Gráfico reiniciado", "Listo: el gráfico se generó nuevamente desde el entrenamiento #1.")

    def clear_current_game_state(self):
        self.answers = {}
        self.asked = []
        self.last_ranking = []
        self.current_question_index = None

        if hasattr(self, "learn_entry"):
            self.learn_entry.delete(0, "end")
        if hasattr(self, "learn_status"):
            self.learn_status.config(text="")
        if hasattr(self, "result_text"):
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.config(state="disabled")

    def refresh_everything(self):
        confirm = messagebox.askyesno(
            "Refrescar todo",
            "Esto hará un reinicio total del juego:\n\n"
            "• volverá a los 20 animales iniciales;\n"
            "• borrará animales aprendidos;\n"
            "• limpiará respuestas, ranking y resultado;\n"
            "• reiniciará el contador de entrenamientos;\n"
            "• generará un gráfico de error nuevo desde cero.\n\n"
            "¿Quieres continuar?"
        )
        if not confirm:
            return

        if self._graph_redraw_after_id is not None:
            try:
                self.root.after_cancel(self._graph_redraw_after_id)
            except Exception:
                pass
            self._graph_redraw_after_id = None

        self.animals = reset_dataset_file()
        self.network = None
        self.errors = []
        self.training_runs = 0
        self.last_error_summary = "Todo fue refrescado. Reentrenando desde cero..."

        self.clear_current_game_state()

        if hasattr(self, "error_status_label"):
            self.error_status_label.config(text=self.last_error_summary)
        if hasattr(self, "error_canvas"):
            self.error_canvas.delete("all")
        if hasattr(self, "dataset_label"):
            self.dataset_label.config(text=f"Animales aprendidos: {len(self.animals)}")

        self.train_network()
        self.root.after(100, self.draw_error_graph)
        messagebox.showinfo(
            "Refresco completo",
            "Listo: el juego volvió a los 20 animales iniciales, la red fue reentrenada y el gráfico se reinició."
        )
        self.new_game()

    def reset_to_initial_animals(self):
        confirm = messagebox.askyesno(
            "Reiniciar dataset",
            "Esto borrará los animales aprendidos y volverá al dataset base de 20 animales.\n\n"
            "También limpiará el gráfico anterior y generará uno nuevo desde cero.\n\n"
            "El archivo dataset_animales_akinator.json se sobrescribirá.\n\n"
            "¿Quieres continuar?"
        )
        if not confirm:
            return

        self.animals = reset_dataset_file()
        self.errors = []
        self.training_runs = 0
        self.clear_current_game_state()

        if hasattr(self, "learn_status"):
            self.learn_status.config(text="Dataset reiniciado: se volvió a los 20 animales iniciales.")
        if hasattr(self, "error_canvas"):
            self.error_canvas.delete("all")
        if hasattr(self, "dataset_label"):
            self.dataset_label.config(text=f"Animales aprendidos: {len(self.animals)}")

        self.train_network()
        self.root.after(100, self.draw_error_graph)

        messagebox.showinfo(
            "Dataset reiniciado",
            "Listo: el juego volvió a los 20 animales iniciales, la red fue reentrenada y el gráfico se reinició."
        )
        self.new_game()

    def new_game(self):
        self.answers = {}
        self.asked = []
        self.last_ranking = []
        if hasattr(self, "learn_entry"):
            self.learn_entry.delete(0, "end")
        if hasattr(self, "learn_status"):
            self.learn_status.config(text="")
        if hasattr(self, "dataset_label"):
            self.dataset_label.config(text=f"Animales aprendidos: {len(self.animals)}")
        self.notebook.select(self.tab_juego)
        self.next_question()

    def next_question(self):
        # Pregunta todas las características antes de mostrar el resultado.
        # Antes se detenía en 8 preguntas, lo que hacía que los animales nuevos
        # se guardaran incompletos con valores 0.5.
        if len(self.asked) >= len(FEATURES):
            self.show_result()
            return

        q_idx = choose_next_question(self.animals, self.answers, self.asked)
        if q_idx is None:
            self.show_result()
            return

        self.current_question_index = q_idx
        self.asked.append(q_idx)
        feature = FEATURES[q_idx]

        self.progress_label.config(text=f"Pregunta {len(self.asked)} de {len(FEATURES)}")
        self.question_label.config(text=feature["question"])

        for widget in self.answer_area.winfo_children():
            widget.destroy()

        if feature["type"] == "binary":
            ttk.Button(self.answer_area, text="Sí", command=lambda: self.record_answer(1.0)).pack(side="left", expand=True, fill="x", padx=8)
            ttk.Button(self.answer_area, text="No", command=lambda: self.record_answer(0.0)).pack(side="left", expand=True, fill="x", padx=8)
            ttk.Button(self.answer_area, text="No sé", command=lambda: self.record_unknown()).pack(side="left", expand=True, fill="x", padx=8)
        else:
            for label, value in feature["choices"]:
                ttk.Button(self.answer_area, text=label, command=lambda v=value: self.record_answer(v)).pack(side="left", expand=True, fill="x", padx=8)
            ttk.Button(self.answer_area, text="No sé", command=lambda: self.record_unknown()).pack(side="left", expand=True, fill="x", padx=8)

    def record_answer(self, value):
        self.answers[self.current_question_index] = value
        self.next_question()

    def record_unknown(self):
        # No guarda respuesta, pero sí avanza.
        self.next_question()

    def build_vector_from_answers(self):
        # Si algo no fue preguntado, se usa 0.5 como incertidumbre neutral.
        vector = []
        for i, feature in enumerate(FEATURES):
            if i in self.answers:
                vector.append(self.answers[i])
            else:
                vector.append(0.5)
        return vector

    def get_exact_matches(self):
        # Animales que coinciden exactamente con las respuestas dadas hasta ahora.
        return exact_candidate_animals(self.animals, self.answers)

    def get_identical_group_for_name(self, animal_name):
        # Animales que tienen el mismo vector completo de características que animal_name.
        normalized = normalize_name(animal_name)
        reference = None
        for animal in self.animals:
            if normalize_name(animal["name"]) == normalized:
                reference = animal["features"]
                break
        if reference is None:
            return []
        return same_full_features_group(self.animals, reference)

    def explain_candidate(self, animal_name, max_items=5):
        # Explica en palabras simples por qué un animal quedó como candidato.
        normalized = normalize_name(animal_name)
        animal = None
        for item in self.animals:
            if normalize_name(item["name"]) == normalized:
                animal = item
                break
        if animal is None or not self.answers:
            return []

        reasons = []
        for feature_index, answer_value in self.answers.items():
            feature = FEATURES[feature_index]
            animal_value = animal["features"][feature_index]
            tolerance = 0.05 if feature["type"] == "binary" else 0.2
            if value_matches(animal_value, answer_value, tolerance=tolerance):
                if feature["type"] == "binary":
                    if answer_value >= 0.5:
                        reasons.append(feature["question"].replace("¿", "").replace("?", "").lower())
                    else:
                        reasons.append("no: " + feature["question"].replace("¿", "").replace("?", "").lower())
                else:
                    label = None
                    for choice_label, choice_value in feature["choices"]:
                        if value_matches(choice_value, answer_value, tolerance=0.2):
                            label = choice_label
                            break
                    if label:
                        reasons.append(f"patas: {label}")
        return reasons[:max_items]

    def get_ranking(self, top_n=4):
        vector = self.build_vector_from_answers()
        probs = self.network.predict_proba(vector)

        # Mezcla probabilidad de la RNA con coincidencia tipo Akinator.
        # Si un animal coincide exactamente con las respuestas dadas, se prioriza
        # por sobre la RNA. Esto evita que un animal recién aprendido quede abajo
        # solo porque la red aún reparte probabilidades entre animales parecidos.
        exact_names = {animal["name"] for animal in self.get_exact_matches()}
        combined = []

        for i, animal in enumerate(self.animals):
            match = candidate_score(animal["features"], self.answers)

            if animal["name"] in exact_names:
                score = 10.0 + probs[i]
            else:
                score = 0.50 * probs[i] + 0.35 * match

            combined.append((animal["name"], score, probs[i], match))

        combined.sort(key=lambda x: x[1], reverse=True)
        top = combined[:top_n]

        total = sum(item[1] for item in top) or 1.0
        normalized = []
        for name, score, prob, match in top:
            normalized.append((name, (score / total) * 100, prob * 100, match * 100))
        return normalized

    def show_result(self):
        self.last_ranking = self.get_ranking(top_n=4)
        exact_matches = self.get_exact_matches()
        exact_names = [animal["name"] for animal in exact_matches]

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")

        if exact_names:
            self.result_text.insert("end", "Coincidencias exactas con tus respuestas:\n\n")
            for i, name in enumerate(exact_names, start=1):
                self.result_text.insert("end", f"{i}. {name.capitalize()}\n")
            if len(exact_names) > 1:
                self.result_text.insert(
                    "end",
                    "\nEstos animales todavía no se pueden distinguir con la información respondida. "
                    "Por eso los muestro juntos antes del ranking de la RNA.\n"
                )
            else:
                self.result_text.insert("end", "\nHay una coincidencia exacta con las respuestas dadas.\n")
        else:
            self.result_text.insert(
                "end",
                "No hay coincidencias exactas con todas tus respuestas. Usaré el ranking probabilístico de la RNA.\n"
            )

        self.result_text.insert("end", "\nRanking probabilístico de la red neuronal:\n\n")
        for i, (name, percent, neural_percent, match_percent) in enumerate(self.last_ranking, start=1):
            self.result_text.insert(
                "end",
                f"{i}. {name.capitalize()} — {percent:.1f}% "
                f"(RNA: {neural_percent:.1f}%, coincidencia: {match_percent:.1f}%)\n"
            )

        best_name = None
        if exact_names:
            best_name = exact_names[0]
        elif self.last_ranking:
            best_name = self.last_ranking[0][0]

        if best_name:
            identical_group = self.get_identical_group_for_name(best_name)
            if len(identical_group) > 1:
                self.result_text.insert(
                    "end",
                    "\nAnimales indistinguibles en el dataset completo:\n"
                )
                self.result_text.insert(
                    "end",
                    ", ".join(name.capitalize() for name in identical_group) + "\n"
                )
                self.result_text.insert(
                    "end",
                    "Comparten exactamente el mismo vector de características guardado.\n"
                )

            reasons = self.explain_candidate(best_name)
            if reasons:
                self.result_text.insert("end", f"\nCreo que podría ser {best_name.capitalize()} porque:\n")
                for reason in reasons:
                    self.result_text.insert("end", f"• {reason}.\n")

        self.result_text.insert("end", "\n¿Era ese o alguno de la lista?")
        self.result_text.config(state="disabled")
        self.notebook.select(self.tab_resultado)

    def correct_guess(self):
        messagebox.showinfo("¡Bien!", "¡Yay! La red acertó o estuvo cerca. Puedes iniciar otra partida.")
        self.new_game()

    def learn_current_animal(self):
        name = normalize_name(self.learn_entry.get())
        if not name:
            messagebox.showwarning("Falta el nombre", "Escribe el nombre del animal correcto.")
            return

        unanswered = [FEATURES[i]["question"] for i in range(len(FEATURES)) if i not in self.answers]
        if unanswered:
            messagebox.showwarning(
                "Faltan características",
                "Para aprender bien un animal nuevo, necesito que respondas todas las preguntas de la partida.\n\n"
                "Vuelve a jugar, evita usar 'No sé' si quieres enseñarme ese animal, y luego guárdalo otra vez."
            )
            return

        features = self.build_vector_from_answers()

        same_group = same_full_features_group(self.animals, features)
        if same_group:
            messagebox.showinfo(
                "Características compartidas",
                "Este animal tendrá las mismas características que: " + ", ".join(same_group) +
                "\n\nCuando ocurra, el juego mostrará esos animales juntos como posibilidades equivalentes."
            )

        existing = None
        for animal in self.animals:
            if normalize_name(animal["name"]) == name:
                existing = animal
                break

        if existing:
            existing["features"] = features
            action = "actualizado"
        else:
            self.animals.append({"name": name, "features": features})
            action = "agregado"

        save_animals(self.animals)
        self.train_network()
        self.learn_status.config(text=f"'{name}' fue {action}. La red fue reentrenada.")
        messagebox.showinfo("Aprendido", f"'{name}' fue {action}. Ahora la red sabe un poco más.")
        self.new_game()


# ==========================================================
# 7. EJECUCIÓN
# ==========================================================


if __name__ == "__main__":
    root = tk.Tk()
    app = ZooAkinatorApp(root)
    root.mainloop()
