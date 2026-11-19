
import tkinter as tk
import random
import time


class TypingTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Trainer")
        self.root.geometry("850x830")
        self.root.configure(bg="#171923")

        self.texts = [
            "Python is a powerful programming language that is easy to learn.",
            "Programming helps people solve problems and create useful applications.",
            "Practice makes perfect. The more you type, the faster you become.",
            "Technology is changing the world and creating new opportunities.",
            "Learning programming develops logical thinking and creativity."
        ]

        self.mode = tk.StringVar(value="random")

        self.current_text = ""
        self.start_time = None
        self.timer_id = None
        self.finished = False

        self.create_interface()

    def create_interface(self):
        title = tk.Label(
            self.root,
            text="Typing Speed Trainer",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#171923"
        )
        title.pack(pady=(20,0))

        subtitle = tk.Label(
            self.root,
            text="Перевір свою швидкість друку!",
            font=("Arial", 16),
            fg="#a0aec0",
            bg="#171923"
        )
        subtitle.pack(pady=(15,0))

        mode_label = tk.Label(
            self.root,
            text="Вибери режим тренування:",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#171923"
        )
        mode_label.pack(pady=(15, 0))

        radio_buttons_frame = tk.Frame(self.root, bg="#171923")
        radio_buttons_frame.pack(pady=(5, 0))

        tk.Radiobutton(
            radio_buttons_frame,
            text="Випадковий текст",
            variable=self.mode,
            value="random",
            command=self.update_mode,
            bg="#171923",
            fg="white",
            selectcolor="#252a3a",
            activebackground="#171923",
            activeforeground="white",
            font=("Arial", 12),
            bd=0,
            highlightthickness=0,
            relief="flat",
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            radio_buttons_frame,
            text="Власний текст",
            variable=self.mode,
            value="custom",
            command=self.update_mode,
            bg="#171923",
            fg="white",
            selectcolor="#252a3a",
            activebackground="#171923",
            activeforeground="white",
            font=("Arial", 12),
            bd=0,
            highlightthickness=0,
            relief="flat",
        ).pack(side="left", padx=10)

        input_label = tk.Label(
            self.root,
            text="Введи власний текст нижче:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#171923",

        )
        input_label.pack(pady=(20, 0))

        self.custom_text = tk.Text(
            self.root,
            height=3,
            width=80,
            font=("Arial", 12),
            bg="#252a3a",
            fg="white",
            insertbackground="white",
            wrap="word",
            padx=10,
            pady=10
        )
        self.custom_text.pack(pady=(10, 0))

        self.text_label = tk.Label(
            self.root,
            text="Тут з'явиться текст для друку",
            font=("Arial", 12),
            fg="white",
            bg="#252a3a",
            height=3,
            width=80,
            padx=10,
            pady=10,
        )
        self.text_label.pack(pady=(40, 0))

        input_label = tk.Label(
            self.root,
            text="Введи текст нижче:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#171923",

        )
        input_label.pack(pady=(40, 0))

        self.input_field = tk.Text(
            self.root,
            font=("Arial", 12),
            bg="#252a3a",
            fg="white",
            insertbackground="white",
            wrap="word",
            height=3,
            width=80,
            padx=10,
            pady=10
        )
        self.input_field.pack(pady=(10))

        self.input_field.bind(
            "<KeyRelease>",
            self.check_input
        )

        self.stats_frame = tk.Frame(
            self.root,
            bg="#171923"
        )
        self.stats_frame.pack(pady=12)

        self.timer_label = tk.Label(
            self.stats_frame,
            text="Час: 0 сек",
            font=("Arial", 16, "bold"),
            fg="#68d391",
            bg="#171923",
        )
        self.timer_label.pack(side="left", padx=10)

        self.stats_label = tk.Label(
            self.stats_frame,
            text="Швидкість: 0 WPM    Точність: 0%",
            font=("Arial", 16, "bold"),
            fg="#68d391",
            bg="#171923"
        )
        self.stats_label.pack(side="left", padx=10)

        self.result_label = tk.Label(
            self.root,
            text="Вибери текст і почни тренування",
            font=("Arial", 14),
            fg="#a0aec0",
            bg="#171923"
        )
        self.result_label.pack(pady=5)
 
        buttons_frame = tk.Frame(self.root, bg="#171923")
        buttons_frame.pack(pady=(20, 0))

        self.start_button = tk.Button(
            buttons_frame,
            text="Почати тренування",
            font=("Arial", 12, "bold"),
            bg="#7057A3",
            activebackground="#8269B8",
            fg="white",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.start_test
        )

        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(
            buttons_frame,
            text="Зупинити тренування",
            font=("Arial", 12, "bold"),
            bg="#A05C78",
            activebackground="#B66D8D",
            fg="white",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.stop_test,
            state="disabled"
        )

        self.stop_button.pack(side="left", padx=10)

        self.update_mode()

    def update_mode(self):
        if self.mode.get() == "custom":
            self.custom_text.config(state="normal")
        else:
            self.custom_text.config(state="disabled")

    def start_test(self):
        # Зупиняємо попередній таймер, якщо він існує
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Вибираємо текст
        if self.mode.get() == "random":
            self.current_text = random.choice(self.texts)
        else:
            self.current_text = self.custom_text.get(
                "1.0", "end-1c"
            ).strip()

            if not self.current_text:
                self.result_label.config(
                    text="Спочатку введи власний текст!"
                )
                return

        # Скидаємо попередні результати
        self.start_time = None
        self.finished = False

        self.text_label.config(text=self.current_text)

        self.input_field.config(state="normal")
        self.input_field.delete("1.0", tk.END)
        self.input_field.focus_set()

        self.timer_label.config(text="Час: 0 сек")

        self.stats_label.config(
            text="Швидкість: 0 WPM    Точність: 0%"
        )

        self.result_label.config(text="Почни друкувати!")

        # Оновлюємо доступність кнопок
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def check_input(self, event=None):
        if self.finished or not self.current_text:
            return

        typed_text = self.input_field.get(
            "1.0", "end-1c"
        )

        if not typed_text:
            return

        # Запускаємо таймер після першого символу
        if self.start_time is None:
            self.start_time = time.time()
            self.update_timer()

        elapsed = time.time() - self.start_time

        # Рахуємо правильно введені символи
        correct = 0

        for a, b in zip(typed_text, self.current_text):
            if a == b:
                correct += 1

        # Розрахунок статистики
        accuracy = correct / len(typed_text) * 100

        minutes = elapsed / 60
        speed = correct / 5 / minutes if minutes > 0 else 0

        errors = len(typed_text) - correct

        self.stats_label.config(
            text=f"Швидкість: {speed:.0f} WPM    "
                 f"Точність: {accuracy:.1f}%"
        )

        self.result_label.config(
            text=f"Помилки: {errors}"
        )

        # Автоматично завершуємо тренування
        if len(typed_text) >= len(self.current_text):
            self.finish_test()

    def update_timer(self):
        if self.finished or self.start_time is None:
            return

        elapsed = int(time.time() - self.start_time)

        self.timer_label.config(
            text=f"Час: {elapsed} сек"
        )

        self.timer_id = self.root.after(
            500, self.update_timer
        )

    def stop_test(self):
        if self.finished:
            return

        if self.start_time is None:
            self.finish_test()
            return

        self.finish_test()

    def finish_test(self):
        if self.finished:
            return

        # Позначаємо тренування як завершене
        self.finished = True

        # Зупиняємо таймер
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Одразу повертаємо доступність кнопок
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")

        # Блокуємо поле введення
        self.input_field.config(state="disabled")

        typed_text = self.input_field.get(
            "1.0", "end-1c"
        )

        # Якщо користувач нічого не ввів
        if not typed_text or self.start_time is None:
            self.timer_label.config(text="Час: 0 сек")

            self.stats_label.config(
                text="Швидкість: 0 WPM    Точність: 0%"
            )

            self.result_label.config(
                text="Тренування зупинено. Текст не введено."
            )
            return

        # Розрахунок результатів
        elapsed = max(time.time() - self.start_time, 0.001)

        correct = sum(
            1 for a, b in zip(
                typed_text,
                self.current_text
            ) if a == b
        )

        accuracy = correct / len(typed_text) * 100

        speed = correct / 5 / (elapsed / 60)

        errors = len(typed_text) - correct

        self.timer_label.config(
            text=f"Час: {elapsed:.1f} сек"
        )

        self.stats_label.config(
            text=f"Швидкість: {speed:.0f} WPM    "
                 f"Точність: {accuracy:.1f}%"
        )

        self.result_label.config(
            text=f"Тренування завершено! Помилок: {errors}"
        )
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTrainer(root)
    root.mainloop()

