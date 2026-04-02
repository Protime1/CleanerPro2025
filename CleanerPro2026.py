import tkinter as tk
from tkinter import messagebox, ttk
import os
import shutil
import threading
import time
from datetime import datetime
import tempfile
import random
import sys
import webbrowser


class CleanerPro2026:
    def __init__(self, root):
        self.root = root
        self.root.title("Cleaner Pro 2026 - Углублённая очистка")
        self.root.geometry("600x700")

        # ===== ЦВЕТОВАЯ ПАЛИТРА =====
        self.bg_color = "#1e1e2e"
        self.card_bg = "#252541"
        self.text_color = "#e0e0e0"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.warning_color = "#e67e22"
        self.error_color = "#e74c3c"
        self.secondary_text = "#a0a0a0"
        self.border_color = "#404060"

        self.root.configure(bg=self.bg_color)

        # ===== ПАСХАЛКА =====
        self.author_click_count = 0
        self.author_last_click_time = 0
        self.easter_egg_active = False
        self.easter_game_active = False

        # ===== ВЕРСИЯ =====
        self.version = "3.1.0"
        self.github_user = "Protime1"

        # ===== РЕЖИМЫ =====
        self.clean_mode = "standard"

        # ===== ПРАНК =====
        self.april_fools_active = False
        self.prank_windows = []

        self.center_window()
        self.create_ui()
        self.cleaning = False

    def center_window(self):
        """Центрирование окна"""
        self.root.update_idletasks()
        w, h = 600, 700
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def create_ui(self):
        # Заголовок
        self.title_label = tk.Label(
            self.root,
            text="🧹 CLEANER PRO 2026",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(pady=(20, 5))

        tk.Label(
            self.root,
            text=f"Углублённая очистка системы | v{self.version}",
            font=("Arial", 11),
            fg=self.secondary_text,
            bg=self.bg_color
        ).pack()

        sep = tk.Frame(self.root, height=2, bg=self.border_color)
        sep.pack(fill=tk.X, padx=30, pady=10)

        # ===== ВЫБОР РЕЖИМА =====
        mode_frame = tk.LabelFrame(
            self.root,
            text=" 🎯 ВЫБЕРИТЕ РЕЖИМ ОЧИСТКИ",
            font=("Arial", 12, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            padx=20,
            pady=15,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.border_color
        )
        mode_frame.pack(fill=tk.X, padx=30, pady=10)

        self.mode_var = tk.StringVar(value="standard")

        modes = [
            ("🟢 СТАНДАРТНЫЙ", "standard", "Безопасная очистка (5-15 ГБ)"),
            ("🟡 УГЛУБЛЁННЫЙ", "deep", "Глубокая очистка (15-30 ГБ)"),
            ("🔴 АГРЕССИВНЫЙ", "aggressive", "Максимальная очистка (30-50+ ГБ)")
        ]

        for text, value, desc in modes:
            frame = tk.Frame(mode_frame, bg=self.card_bg)
            frame.pack(fill=tk.X, pady=8)

            tk.Radiobutton(
                frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=("Arial", 11, "bold"),
                bg=self.card_bg,
                fg=self.text_color,
                selectcolor=self.card_bg,
                activebackground=self.card_bg,
                activeforeground=self.accent_color,
                command=self.update_mode_description
            ).pack(side=tk.LEFT)

            tk.Label(
                frame,
                text=desc,
                font=("Arial", 9),
                bg=self.card_bg,
                fg=self.secondary_text
            ).pack(side=tk.LEFT, padx=(10, 0))

        self.mode_desc = tk.Label(
            mode_frame,
            text="Безопасное удаление временных файлов Windows и кэша браузеров.",
            font=("Arial", 9, "italic"),
            bg=self.card_bg,
            fg=self.text_color,
            wraplength=500,
            justify=tk.LEFT
        )
        self.mode_desc.pack(anchor=tk.W, pady=(10, 0))

        # ===== ОПЦИИ =====
        options_frame = tk.LabelFrame(
            self.root,
            text=" ⚙️ ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ",
            font=("Arial", 12, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            padx=20,
            pady=15,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.border_color
        )
        options_frame.pack(fill=tk.X, padx=30, pady=10)

        self.clean_cache_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="🗑️ Очистить кэш браузеров",
            variable=self.clean_cache_var,
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color,
            selectcolor=self.card_bg,
            activebackground=self.card_bg
        ).pack(anchor=tk.W, pady=5)

        self.clean_logs_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="📝 Удалить логи Windows",
            variable=self.clean_logs_var,
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color,
            selectcolor=self.card_bg,
            activebackground=self.card_bg
        ).pack(anchor=tk.W, pady=5)

        self.clean_old_downloads_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="📥 Удалить старые загрузки (30+ дней)",
            variable=self.clean_old_downloads_var,
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color,
            selectcolor=self.card_bg,
            activebackground=self.card_bg
        ).pack(anchor=tk.W, pady=5)

        # ===== КНОПКИ =====
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)

        self.btn = tk.Button(
            button_frame,
            text="🚀 НАЧАТЬ УГЛУБЛЁННУЮ ОЧИСТКУ",
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg="white",
            width=30,
            height=2,
            cursor="hand2",
            command=self.start_clean,
            relief=tk.RAISED,
            bd=3,
            activebackground="#2980b9"
        )
        self.btn.pack()

        # Кнопка проверки обновлений
        self.update_btn = tk.Button(
            self.root,
            text="🔄 Проверить обновления",
            font=("Arial", 10),
            bg=self.success_color,
            fg="white",
            command=self.check_update_manual,
            relief=tk.RAISED,
            bd=2
        )
        self.update_btn.pack(pady=10)

        # ===== ПРОГРЕСС =====
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar",
                        thickness=20,
                        troughcolor=self.card_bg,
                        background=self.accent_color,
                        bordercolor=self.border_color,
                        lightcolor=self.accent_color,
                        darkcolor=self.accent_color
                        )

        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate',
            style="TProgressbar"
        )

        self.status = tk.Label(
            self.root,
            text="✅ Выберите режим и начните очистку",
            font=("Arial", 11, "bold"),
            fg=self.success_color,
            bg=self.bg_color
        )
        self.status.pack(pady=15)

        self.stats = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.stats.pack(pady=10)

        # ===== ПОДВАЛ =====
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        author_text = tk.Label(
            footer_frame,
            text=f"© Cleaner Pro 2026 v{self.version} | Разработчик: Protime1",
            font=("Arial", 8),
            fg=self.secondary_text,
            bg=self.bg_color,
            cursor="hand2"
        )
        author_text.pack()
        author_text.bind("<Button-1>", self.on_author_click)

        self.easter_label = None
        self.easter_game_window = None

        self.super_mode_indicator = tk.Label(
            footer_frame,
            text="",
            font=("Arial", 8, "bold"),
            fg="#FFD700",
            bg=self.bg_color
        )
        self.super_mode_indicator.pack()

        self.root.after(1000, self.check_super_mode_on_start)

    def check_april_fools(self):
        """Проверка на 1 апреля"""
        today = datetime.now()
        return today.month == 4 and today.day == 1

    def start_clean(self):
        """Запуск очистки с пранком 1 апреля"""
        if self.cleaning:
            return

        # Проверяем, сегодня ли 1 апреля
        if self.check_april_fools() and not self.april_fools_active:
            self.april_fools_active = True
            self.launch_virus_prank()
            return

        # Обычная очистка
        self.do_normal_clean()

    def launch_virus_prank(self):
        """Запуск страшного пранка с вирусами"""
        self.btn.config(state=tk.DISABLED)

        # Создаём главное окно "установки"
        virus_window = tk.Toplevel(self.root)
        virus_window.title("⚠️ КРИТИЧЕСКАЯ УГРОЗА ⚠️")
        virus_window.geometry("650x550")
        virus_window.configure(bg="#1a0000")
        virus_window.attributes("-topmost", True)

        virus_window.update_idletasks()
        x = (virus_window.winfo_screenwidth() - 650) // 2
        y = (virus_window.winfo_screenheight() - 550) // 2
        virus_window.geometry(f"650x550+{x}+{y}")

        # Череп вверху
        skull = tk.Label(
            virus_window,
            text="💀💀💀",
            font=("Arial", 48),
            bg="#1a0000",
            fg="#ff0000"
        )
        skull.pack(pady=(20, 5))

        tk.Label(
            virus_window,
            text="ОБНАРУЖЕНО ВНЕДРЕНИЕ ВРЕДОНОСНОГО ПО",
            font=("Arial", 14, "bold"),
            bg="#1a0000",
            fg="#ff4444"
        ).pack()

        tk.Label(
            virus_window,
            text="ЗАПУЩЕНА УСТАНОВКА ВИРУСНЫХ РАСАДНИКОВ",
            font=("Arial", 12, "bold"),
            bg="#1a0000",
            fg="#ff6666"
        ).pack(pady=5)

        # Прогресс-бар
        self.prank_progress = ttk.Progressbar(
            virus_window,
            length=500,
            mode='determinate'
        )
        self.prank_progress.pack(pady=20)

        # Статус
        self.prank_status = tk.Label(
            virus_window,
            text="",
            font=("Arial", 10, "bold"),
            bg="#1a0000",
            fg="#ffaa00"
        )
        self.prank_status.pack(pady=10)

        # Текстовый лог
        self.prank_log = tk.Text(
            virus_window,
            height=12,
            width=70,
            bg="#0a0000",
            fg="#ff4444",
            font=("Consolas", 9),
            relief=tk.FLAT,
            bd=2
        )
        self.prank_log.pack(pady=10, padx=20)

        # Кнопка "Отмена" (бесполезная)
        cancel_btn = tk.Button(
            virus_window,
            text="💀 ПОПЫТАТЬСЯ ОСТАНОВИТЬ 💀",
            font=("Arial", 10, "bold"),
            bg="#8b0000",
            fg="white",
            command=lambda: self.fake_cancel_prank(virus_window)
        )
        cancel_btn.pack(pady=10)

        # Список "вирусов" для установки
        self.viruses = [
            ("🦠 Trojan.Win32.Agent", 8, "Внедрение в системные процессы..."),
            ("🦠 CryptoLocker.Ransom", 15, "Шифрование пользовательских файлов..."),
            ("🦠 Spyware.Keylogger", 22, "Установка перехватчика нажатий..."),
            ("🦠 Worm.Network", 30, "Распространение по локальной сети..."),
            ("🦠 Rootkit.Hidden", 38, "Скрытие процессов от антивируса..."),
            ("🦠 Miner.Crypto", 45, "Запуск скрытого майнера..."),
            ("🦠 Backdoor.Access", 52, "Открытие бэкдора в системе..."),
            ("🦠 Botnet.Client", 60, "Подключение к C&C серверу..."),
            ("🦠 Stealer.Passwords", 68, "Сбор паролей из браузеров..."),
            ("🦠 Ransomware.Encrypt", 75, "Шифрование документов..."),
            ("🦠 Exploit.Kit", 82, "Загрузка дополнительных модулей..."),
            ("🦠 Wiper.Destroyer", 90, "Подготовка к уничтожению данных..."),
            ("💀 ФИНАЛЬНАЯ АКТИВАЦИЯ", 98, "Установка завершается..."),
        ]

        self.virus_index = 0
        self.prank_window = virus_window

        # Запускаем установку
        self.install_virus()

        # Создаём дополнительные панические окна
        self.create_panic_windows()

    def install_virus(self):
        """Установка фейковых вирусов"""
        if not hasattr(self, 'prank_window') or not self.prank_window:
            return

        if self.virus_index < len(self.viruses):
            name, progress, desc = self.viruses[self.virus_index]

            self.prank_progress["value"] = progress
            self.prank_status.config(text=f"📡 {name} - {desc}")

            # Добавляем в лог
            self.prank_log.config(state=tk.NORMAL)
            self.prank_log.insert(tk.END, f"[{progress:3}%] Установка {name}...\n")
            self.prank_log.insert(tk.END, f"     └─ {desc}\n")

            # Страшные сообщения
            scary_msgs = [
                f"     ⚠️ Заражено файлов: {random.randint(100, 500)}",
                f"     ⚠️ Скомпрометировано: {random.randint(5, 50)} процессов",
                f"     💀 Доступ к камере: ПОЛУЧЕН",
                f"     💀 Перехват буфера обмена: АКТИВЕН",
                f"     🔐 Шифрование диска C: {random.randint(10, 50)}%",
                f"     🌐 Отправка данных на сервер: {random.randint(100, 5000)} КБ",
                f"     🎮 Майнер использует {random.randint(20, 80)}% GPU",
            ]

            if random.random() < 0.6:
                self.prank_log.insert(tk.END, f"{random.choice(scary_msgs)}\n")

            self.prank_log.see(tk.END)
            self.prank_log.config(state=tk.DISABLED)

            self.virus_index += 1

            # Случайная задержка для пущего страха
            delay = random.randint(600, 1200)
            self.prank_window.after(delay, self.install_virus)
        else:
            # Установка завершена
            self.prank_progress["value"] = 100
            self.prank_status.config(text="💀 ВСЕ ВИРУСНЫЕ РАСАДНИКИ УСТАНОВЛЕНЫ 💀", fg="#ff0000")

            self.prank_log.config(state=tk.NORMAL)
            self.prank_log.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.prank_log.insert(tk.END, "💀💀💀 УСТАНОВКА ЗАВЕРШЕНА! 💀💀💀\n")
            self.prank_log.insert(tk.END, "Ваша система скомпрометирована!\n")
            self.prank_log.insert(tk.END, "Все данные будут уничтожены через 30 секунд...\n")
            self.prank_log.insert(tk.END, "=" * 60 + "\n")
            self.prank_log.config(state=tk.DISABLED)

            # Начинаем обратный отсчёт
            self.countdown = 30
            self.start_final_countdown()

    def start_final_countdown(self):
        """Обратный отсчёт перед раскрытием пранка"""

        def update_countdown():
            if not hasattr(self, 'prank_window') or not self.prank_window:
                return

            if self.countdown > 0:
                self.prank_status.config(text=f"💀 УНИЧТОЖЕНИЕ ДАННЫХ ЧЕРЕЗ {self.countdown} СЕКУНД 💀", fg="#ff0000")
                self.countdown -= 1
                self.prank_window.after(1000, update_countdown)
            else:
                self.reveal_april_fools()

        update_countdown()

    def fake_cancel_prank(self, window):
        """Фейковая кнопка отмены - создаёт панику"""
        self.prank_log.config(state=tk.NORMAL)
        self.prank_log.insert(tk.END, "\n⚠️⚠️⚠️ ПОПЫТКА ОТМЕНЫ ⚠️⚠️⚠️\n")
        self.prank_log.insert(tk.END, "❌ ОШИБКА: Процесс не может быть остановлен!\n")
        self.prank_log.insert(tk.END, "💀 Защита от удаления активирована!\n")
        self.prank_log.see(tk.END)
        self.prank_log.config(state=tk.DISABLED)

        # Создаём несколько панических окон
        for i in range(3):
            self.root.after(i * 500, self.create_panic_window)

    def create_panic_windows(self):
        """Создание панических окон"""
        for i in range(5):
            self.root.after(i * 800, self.create_panic_window)

    def create_panic_window(self):
        """Создание панического окна"""
        panic = tk.Toplevel(self.root)
        panic.title("⚠️ КРИТИЧЕСКАЯ ОШИБКА ⚠️")
        panic.geometry("400x250")
        panic.configure(bg="#2c001e")
        panic.attributes("-topmost", True)

        x = panic.winfo_screenwidth() // 2 - 200 + random.randint(-100, 100)
        y = panic.winfo_screenheight() // 2 - 125 + random.randint(-80, 80)
        panic.geometry(f"400x250+{x}+{y}")

        tk.Label(
            panic,
            text="🚨🚨🚨",
            font=("Arial", 36),
            bg="#2c001e",
            fg="#ff0000"
        ).pack(pady=10)

        error_messages = [
            "СИСТЕМА СКОМПРОМЕТИРОВАНА!",
            "ОБНАРУЖЕНА АКТИВНАЯ УГРОЗА!",
            "ВИРУСНАЯ АКТИВАЦИЯ ПОДТВЕРЖДЕНА!",
            "НЕСАНКЦИОНИРОВАННЫЙ ДОСТУП!",
            "ШИФРОВАНИЕ ДАННЫХ ЗАПУЩЕНО!"
        ]

        tk.Label(
            panic,
            text=random.choice(error_messages),
            font=("Arial", 12, "bold"),
            bg="#2c001e",
            fg="#ff6666"
        ).pack()

        tk.Label(
            panic,
            text=f"Код ошибки: 0x{random.randint(1000, 9999):04X}",
            font=("Arial", 10),
            bg="#2c001e",
            fg="#ff9999"
        ).pack(pady=5)

        # Прогресс "шифрования"
        crypto_progress = ttk.Progressbar(
            panic,
            length=300,
            mode='determinate'
        )
        crypto_progress.pack(pady=10)
        crypto_progress["value"] = random.randint(30, 85)

        # Автоуничтожение
        panic.after(4000, panic.destroy)

    def reveal_april_fools(self):
        """Раскрытие пранка"""
        # Закрываем все окна пранка
        if hasattr(self, 'prank_window') and self.prank_window:
            try:
                self.prank_window.destroy()
            except:
                pass

        # Закрываем все панические окна
        for window in self.prank_windows:
            try:
                window.destroy()
            except:
                pass

        # Показываем финальное сообщение
        msg = tk.Toplevel(self.root)
        msg.title("🎉 С 1 АПРЕЛЯ! 🎉")
        msg.geometry("500x400")
        msg.configure(bg=self.bg_color)
        msg.attributes("-topmost", True)

        msg.update_idletasks()
        x = (msg.winfo_screenwidth() - 500) // 2
        y = (msg.winfo_screenheight() - 400) // 2
        msg.geometry(f"500x400+{x}+{y}")

        # Анимация появления
        for i in range(10):
            msg.attributes("-alpha", i / 10)
            msg.update()
            time.sleep(0.02)

        tk.Label(
            msg,
            text="🎉🎊🎉",
            font=("Arial", 48),
            bg=self.bg_color,
            fg="#FFD700"
        ).pack(pady=(20, 5))

        tk.Label(
            msg,
            text="ЭТО БЫЛ ПРАНК!",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.success_color
        ).pack()

        tk.Label(
            msg,
            text="С 1 АПРЕЛЯ!",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#e67e22"
        ).pack()

        tk.Label(
            msg,
            text="\nНикаких вирусов не было установлено!\n"
                 "Ваша система в полной безопасности.\n\n"
                 "Это был шуточный розыгрыш в честь Дня смеха!\n\n"
                 "Не бойтесь чистить систему, она вас не съест! 😊\n\n"
                 "P.S. Нажмите 5 раз на имя разработчика\n"
                 "чтобы поиграть в секретную игру! 🎮",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color,
            justify=tk.CENTER
        ).pack(pady=10)

        def close_and_reset():
            for i in range(10, 0, -1):
                msg.attributes("-alpha", i / 10)
                msg.update()
                time.sleep(0.02)
            msg.destroy()
            self.april_fools_active = False
            self.btn.config(state=tk.NORMAL)

        tk.Button(
            msg,
            text="😊 ПОНЯЛ, ХОРОШО ПОШУТИЛИ!",
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            command=close_and_reset,
            padx=20,
            pady=10
        ).pack(pady=20)

    def do_normal_clean(self):
        """Обычная очистка без пранка"""
        if self.cleaning:
            return

        self.clean_mode = self.mode_var.get()

        super_bonus = 1.5 if (self.easter_egg_active or self.check_super_mode()) else 1.0

        warning_message = "АГРЕССИВНЫЙ РЕЖИМ УДАЛИТ МНОГО ФАЙЛОВ!\n\n"
        if super_bonus > 1.0:
            warning_message += "🌟 СУПЕР-РЕЖИМ АКТИВЕН! +50% эффективности!\n\n"
        warning_message += "Вы уверены что хотите продолжить?"

        if self.clean_mode == "aggressive":
            confirm = messagebox.askyesno(
                "⚠️ ВНИМАНИЕ! Агрессивный режим",
                warning_message,
                icon='warning'
            )
            if not confirm:
                return

        self.cleaning = True
        self.btn.config(
            state=tk.DISABLED,
            text="⏳ ВЫПОЛНЯЕТСЯ ОЧИСТКА...",
            bg=self.warning_color
        )
        self.status.config(text="🔍 Анализирую систему...", fg=self.warning_color)
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        thread = threading.Thread(target=self.deep_clean_process, daemon=True)
        thread.start()

    def deep_clean_process(self):
        """Процесс очистки"""
        try:
            total_freed = 0
            steps_completed = 0
            total_steps = self.get_total_steps()

            super_bonus = 1.5 if (self.easter_egg_active or self.check_super_mode()) else 1.0

            steps_completed += 1
            self.update_progress(steps_completed, total_steps, "Временные файлы Windows")
            freed = self.clean_windows_temp() * super_bonus
            total_freed += freed
            time.sleep(0.3)

            if self.clean_cache_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Кэш браузеров")
                freed = self.clean_browser_cache_deep() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            if self.clean_logs_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Логи Windows")
                freed = self.clean_windows_logs_deep() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            if self.clean_old_downloads_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Старые загрузки")
                freed = self.clean_old_downloads() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            if self.clean_mode == "deep":
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Глубокая очистка")
                freed = self.deep_clean_additional() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            elif self.clean_mode == "aggressive":
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Агрессивная очистка")
                freed = self.aggressive_clean() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            self.root.after(0, self.show_clean_results, total_freed)

        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def get_total_steps(self):
        steps = 1
        if self.clean_cache_var.get():
            steps += 1
        if self.clean_logs_var.get():
            steps += 1
        if self.clean_old_downloads_var.get():
            steps += 1
        if self.clean_mode == "deep":
            steps += 1
        elif self.clean_mode == "aggressive":
            steps += 1
        return steps

    def update_progress(self, current, total, message):
        percent = (current / total) * 100
        self.root.after(0, lambda: self.progress.config(value=percent))
        self.root.after(0, lambda: self.status.config(text=f"⚡ {message}... ({current}/{total})"))

    def clean_windows_temp(self):
        freed_mb = 0
        temp_paths = self.get_temp_paths()
        for path in temp_paths:
            if os.path.exists(path):
                freed_mb += self.delete_folder_contents(path, mode=self.clean_mode)
        return round(freed_mb, 2)

    def get_temp_paths(self):
        user_profile = os.environ.get('USERPROFILE', '')
        windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
        base_paths = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            os.path.join(user_profile, 'AppData', 'Local', 'Temp'),
            os.path.join(windows_dir, 'Temp'),
        ]
        if self.clean_mode == "deep":
            base_paths.extend([
                os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
                os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCookies'),
                os.path.join(windows_dir, 'SoftwareDistribution', 'Download'),
            ])
        elif self.clean_mode == "aggressive":
            base_paths.extend([
                os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'History'),
                os.path.join(windows_dir, 'Prefetch'),
                os.path.join(windows_dir, 'Logs'),
                os.path.join(windows_dir, 'System32', 'LogFiles'),
            ])
        return [p for p in base_paths if p]

    def clean_browser_cache_deep(self):
        freed_mb = 0
        user_profile = os.environ.get('USERPROFILE', '')
        browser_paths = [
            os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(user_profile, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles'),
        ]
        for cache_path in browser_paths:
            if os.path.exists(cache_path):
                freed_mb += self.delete_folder_contents(cache_path, mode=self.clean_mode)
        return round(freed_mb, 2)

    def clean_windows_logs_deep(self):
        freed_mb = 0
        windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
        log_paths = [
            os.path.join(windows_dir, 'Logs'),
            os.path.join(windows_dir, 'System32', 'LogFiles'),
        ]
        for log_path in log_paths:
            if os.path.exists(log_path):
                freed_mb += self.delete_folder_contents(log_path, mode=self.clean_mode,
                                                        extensions=['.log', '.etl', '.evtx'])
        return round(freed_mb, 2)

    def clean_old_downloads(self):
        freed_mb = 0
        downloads_path = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
        if os.path.exists(downloads_path):
            cutoff_days = 30
            if self.clean_mode == "aggressive":
                cutoff_days = 7
            cutoff_time = time.time() - (cutoff_days * 24 * 60 * 60)
            freed_mb = self.delete_old_files(downloads_path, cutoff_time)
        return round(freed_mb, 2)

    def deep_clean_additional(self):
        freed_mb = 0
        thumb_cache = os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Microsoft', 'Windows',
                                   'Explorer')
        if os.path.exists(thumb_cache):
            freed_mb += self.delete_files_by_pattern(thumb_cache, 'thumbcache_*.db')
        try:
            os.system('cmd /c "rd /s /q %systemdrive%\\$Recycle.Bin 2>nul"')
            os.system('ipconfig /flushdns >nul 2>&1')
        except:
            pass
        return round(freed_mb, 2)

    def aggressive_clean(self):
        freed_mb = 0
        prefetch_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
        if os.path.exists(prefetch_path):
            freed_mb += self.delete_folder_contents(prefetch_path, mode="aggressive")
        win_update_cache = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'SoftwareDistribution', 'Download')
        if os.path.exists(win_update_cache):
            freed_mb += self.delete_folder_contents(win_update_cache, mode="aggressive")
        return round(freed_mb, 2)

    def delete_folder_contents(self, folder_path, mode="standard", extensions=None):
        freed_mb = 0
        if not os.path.exists(folder_path):
            return 0
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isfile(item_path):
                        if self.should_delete_file(item, mode, extensions):
                            size_mb = os.path.getsize(item_path) / (1024 * 1024)
                            os.remove(item_path)
                            freed_mb += size_mb
                    elif os.path.isdir(item_path):
                        if mode == "aggressive" or "temp" in item.lower() or "cache" in item.lower():
                            dir_size = self.get_folder_size(item_path) / (1024 * 1024)
                            shutil.rmtree(item_path, ignore_errors=True)
                            freed_mb += dir_size
                except:
                    continue
        except:
            pass
        return freed_mb

    def should_delete_file(self, filename, mode, extensions=None):
        filename_lower = filename.lower()
        if extensions:
            for ext in extensions:
                if filename_lower.endswith(ext):
                    return True
        safe_extensions = ['.tmp', '.log', '.bak', '.old', '.cache', '.dmp']
        if mode == "deep":
            safe_extensions.extend(['.etl', '.evtx'])
        if mode == "aggressive":
            return True
        for ext in safe_extensions:
            if filename_lower.endswith(ext):
                return True
        if filename_lower.startswith('~') or 'temp' in filename_lower or 'cache' in filename_lower:
            return True
        return False

    def delete_old_files(self, folder_path, cutoff_time):
        freed_mb = 0
        if not os.path.exists(folder_path):
            return 0
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isfile(item_path):
                        if os.path.getmtime(item_path) < cutoff_time:
                            size_mb = os.path.getsize(item_path) / (1024 * 1024)
                            os.remove(item_path)
                            freed_mb += size_mb
                except:
                    continue
        except:
            pass
        return freed_mb

    def delete_files_by_pattern(self, folder_path, pattern):
        import fnmatch
        freed_mb = 0
        if not os.path.exists(folder_path):
            return 0
        try:
            for item in os.listdir(folder_path):
                if fnmatch.fnmatch(item.lower(), pattern.lower()):
                    item_path = os.path.join(folder_path, item)
                    try:
                        if os.path.isfile(item_path):
                            size_mb = os.path.getsize(item_path) / (1024 * 1024)
                            os.remove(item_path)
                            freed_mb += size_mb
                    except:
                        pass
        except:
            pass
        return freed_mb

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                try:
                    total_size += os.path.getsize(os.path.join(dirpath, filename))
                except:
                    pass
        return total_size

    def show_clean_results(self, total_freed):
        self.progress["value"] = 100
        self.cleaning = False
        mode_names = {"standard": "СТАНДАРТНОЙ", "deep": "УГЛУБЛЁННОЙ", "aggressive": "АГРЕССИВНОЙ"}
        super_icon = "🌟 " if (self.easter_egg_active or self.check_super_mode()) else ""
        self.btn.config(state=tk.NORMAL, text="🎉 ОЧИСТКА ЗАВЕРШЕНА!", bg=self.success_color)
        self.status.config(text=f"✅ {super_icon}{mode_names.get(self.clean_mode, '')} ОЧИСТКА ВЫПОЛНЕНА!",
                           fg=self.success_color)
        bonus_text = " (🌟 +50% супер-режим!)" if (self.easter_egg_active or self.check_super_mode()) else ""
        self.stats.config(text=f"📊 Освобождено: {total_freed:.2f} МБ{bonus_text}")
        messagebox.showinfo("Очистка завершена!", f"Освобождено: {total_freed:.2f} МБ\nРежим: {self.clean_mode}")
        self.root.after(5000, self.reset_ui)

    def show_error(self, error_msg):
        self.progress.pack_forget()
        self.cleaning = False
        self.btn.config(state=tk.NORMAL, text="🚀 НАЧАТЬ УГЛУБЛЁННУЮ ОЧИСТКУ", bg=self.accent_color)
        self.status.config(text="❌ Ошибка при выполнении очистки", fg=self.error_color)
        messagebox.showerror("Ошибка очистки", f"Не удалось выполнить очистку:\n\n{error_msg}")

    def reset_ui(self):
        self.btn.config(text="🚀 НАЧАТЬ УГЛУБЛЁННУЮ ОЧИСТКУ", bg=self.accent_color)
        self.status.config(text="✅ Выберите режим и начните очистку", fg=self.success_color)
        self.progress["value"] = 0
        self.stats.config(text="")

    def on_author_click(self, event):
        current_time = time.time()
        if current_time - self.author_last_click_time > 2:
            self.author_click_count = 0
        self.author_click_count += 1
        self.author_last_click_time = current_time
        if self.author_click_count == 5:
            self.show_easter_notification("🎮 Вы нашли секретную игру!")
            self.root.after(500, self.launch_trash_game)
        elif self.author_click_count >= 10:
            self.activate_super_mode()

    def show_easter_notification(self, message):
        if not self.easter_label:
            self.easter_label = tk.Label(self.root, text=message, font=("Arial", 9, "bold"), bg="#FFD700", fg="#000000",
                                         padx=10, pady=5, relief=tk.RAISED, bd=2)
            self.easter_label.pack(pady=5)
        else:
            self.easter_label.config(text=message)
            self.easter_label.pack(pady=5)
        self.root.after(3000, lambda: self.easter_label.pack_forget() if self.easter_label else None)

    def launch_trash_game(self):
        if self.easter_game_active:
            return
        self.easter_game_active = True
        game_window = tk.Toplevel(self.root)
        game_window.title("🎮 Cleaner Pro - Сбей мусор!")
        game_window.geometry("800x600")
        game_window.configure(bg=self.bg_color)
        game = TrashShooterGame(game_window, self)
        self.easter_game_window = game_window
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.close_game(game_window))
        game.start_game()

    def close_game(self, window):
        self.easter_game_active = False
        window.destroy()

    def activate_super_mode(self):
        self.easter_egg_active = True
        self.super_mode_indicator.config(text="🌟 СУПЕР-РЕЖИМ АКТИВЕН!")
        messagebox.showinfo("🌟 СУПЕР-РЕЖИМ!", "+50% эффективности очистки на 24 часа!")
        try:
            with open("super_mode.txt", "w") as f:
                f.write(str(time.time()))
        except:
            pass
        self.status.config(text="🌟 Супер-режим активен! +50% эффективности", fg="#FFD700")

    def check_super_mode(self):
        try:
            if os.path.exists("super_mode.txt"):
                with open("super_mode.txt", "r") as f:
                    if time.time() - float(f.read()) < 24 * 60 * 60:
                        return True
        except:
            pass
        return False

    def check_super_mode_on_start(self):
        if self.check_super_mode():
            self.easter_egg_active = True
            self.super_mode_indicator.config(text="🌟 СУПЕР-РЕЖИМ АКТИВЕН!")

    def update_mode_description(self):
        mode = self.mode_var.get()
        desc = {"standard": "🟢 Безопасное удаление временных файлов", "deep": "🟡 Глубокая очистка включая логи",
                "aggressive": "🔴 Максимальная очистка всех временных данных"}
        self.mode_desc.config(text=desc.get(mode, ""))

    def check_update_manual(self):
        messagebox.showinfo("Обновление", "У вас актуальная версия! ✅")


class TrashShooterGame:
    def __init__(self, window, parent_app):
        self.window = window
        self.parent_app = parent_app
        self.canvas = None
        self.score = 0
        self.time_left = 30
        self.game_active = False
        self.targets = []
        self.create_ui()

    def create_ui(self):
        tk.Label(self.window, text="🎮 СБЕЙ МУСОР!", font=("Arial", 24, "bold"), fg="#FFD700", bg="#1e1e2e").pack(
            pady=10)
        info_frame = tk.Frame(self.window, bg="#1e1e2e")
        info_frame.pack(pady=10)
        self.score_label = tk.Label(info_frame, text="🏆 Счёт: 0", font=("Arial", 14, "bold"), fg="#4ECDC4",
                                    bg="#1e1e2e")
        self.score_label.pack(side=tk.LEFT, padx=20)
        self.time_label = tk.Label(info_frame, text="⏱️ Время: 30с", font=("Arial", 14, "bold"), fg="#FF6B6B",
                                   bg="#1e1e2e")
        self.time_label.pack(side=tk.LEFT, padx=20)
        self.canvas = tk.Canvas(self.window, width=760, height=400, bg="#0f0f1f", highlightthickness=2)
        self.canvas.pack(pady=10)
        self.start_btn = tk.Button(self.window, text="🚀 НАЧАТЬ ИГРУ", font=("Arial", 12, "bold"), bg="#2ecc71",
                                   fg="white", command=self.start_game)
        self.start_btn.pack(pady=10)

    def start_game(self):
        if self.game_active:
            return
        self.game_active = True
        self.score = 0
        self.time_left = 30
        self.targets = []
        self.start_btn.config(state=tk.DISABLED, text="🎮 ИГРА ИДЁТ...")
        self.update_score()
        self.game_timer()
        self.generate_targets()
        self.update_targets()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def generate_targets(self):
        if not self.game_active:
            return
        for _ in range(random.randint(1, 2)):
            self.create_target()
        self.window.after(random.randint(800, 1200), self.generate_targets)

    def create_target(self):
        if len(self.targets) >= 12:
            return
        types = [("🗑️", "#95a5a6", 10), ("📁", "#3498db", 15), ("🔥", "#e74c3c", 30), ("⭐", "#FFD700", 50)]
        name, color, points = random.choice(types)
        x, y = random.randint(50, 710), random.randint(50, 150)
        tid = self.canvas.create_text(x, y, text=name, font=("Arial", 24), fill=color)
        self.targets.append(
            {"id": tid, "x": x, "y": y, "dx": random.uniform(-2, 2), "dy": random.uniform(0.5, 1.5), "points": points})

    def update_targets(self):
        if not self.game_active:
            return
        for t in self.targets[:]:
            t["x"] += t["dx"]
            t["y"] += t["dy"]
            if t["x"] <= 20 or t["x"] >= 740:
                t["dx"] *= -1
            if t["y"] >= 380:
                self.canvas.delete(t["id"])
                self.targets.remove(t)
                continue
            self.canvas.coords(t["id"], t["x"], t["y"])
        self.window.after(50, self.update_targets)

    def on_canvas_click(self, event):
        if not self.game_active:
            return
        for t in self.targets[:]:
            if abs(t["x"] - event.x) < 30 and abs(t["y"] - event.y) < 30:
                self.score += t["points"]
                self.update_score()
                self.canvas.delete(t["id"])
                self.targets.remove(t)
                break

    def game_timer(self):
        if not self.game_active:
            return
        self.time_left -= 1
        self.time_label.config(text=f"⏱️ Время: {self.time_left}с")
        if self.time_left <= 0:
            self.end_game()
        else:
            self.window.after(1000, self.game_timer)

    def update_score(self):
        self.score_label.config(text=f"🏆 Счёт: {self.score}")

    def end_game(self):
        self.game_active = False
        self.start_btn.config(state=tk.NORMAL, text="🔄 ИГРАТЬ СНОВА")
        self.canvas.unbind("<Button-1>")
        for t in self.targets:
            self.canvas.delete(t["id"])
        self.targets = []
        messagebox.showinfo("Игра завершена!", f"Ваш счёт: {self.score}")


def main():
    try:
        root = tk.Tk()
        app = CleanerPro2026(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу:\n{e}")


if __name__ == "__main__":
    main()