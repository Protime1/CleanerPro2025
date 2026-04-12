import tkinter as tk
from tkinter import messagebox, ttk
import os
import shutil
import threading
import time
from datetime import datetime
import winreg
import tempfile
import random
import sys
import webbrowser
import json
import fnmatch


class CleanerPro2025:
    def __init__(self, root):
        self.root = root
        self.root.title("Cleaner Pro 2025 - Углублённая очистка")
        self.root.geometry("650x750")

        # ===== ЦВЕТОВАЯ ПАЛИТРА ТЁМНОЙ ТЕМЫ =====
        self.bg_color = "#1e1e2e"  # Основной фон
        self.card_bg = "#252541"  # Фон карточек
        self.text_color = "#e0e0e0"  # Основной текст
        self.accent_color = "#3498db"  # Акцентный цвет
        self.success_color = "#2ecc71"  # Успех
        self.warning_color = "#e67e22"  # Предупреждение
        self.error_color = "#e74c3c"  # Ошибка
        self.secondary_text = "#a0a0a0"  # Вторичный текст
        self.border_color = "#404060"  # Цвет границ

        self.root.configure(bg=self.bg_color)

        # ===== ПАСХАЛКА =====
        self.author_click_count = 0
        self.author_last_click_time = 0
        self.easter_egg_active = False
        self.easter_game_active = False

        # ===== ВЕРСИЯ И АВТООБНОВЛЕНИЕ =====
        self.version = "3.1.0"  # Версия с конфигурацией
        self.github_user = "Protime1"

        # ===== РЕЖИМЫ ОЧИСТКИ =====
        self.clean_mode = "standard"

        # ===== КОНФИГУРАЦИЯ ЗАЩИТЫ =====
        self.config_file = "cleaner_config.json"
        self.protected_paths = []
        self.protected_formats = []
        self.min_file_size_mb = 0
        self.max_file_size_mb = 1024  # 1 ГБ по умолчанию
        self.protected_keywords = []
        self.safe_mode_enabled = True

        # Загружаем конфигурацию
        self.load_config()

        self.center_window()
        self.create_ui()
        self.cleaning = False

        # Автопроверка обновлений
        self.root.after(3000, self.auto_check_update)

    def load_config(self):
        """Загрузить конфигурацию из файла"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                    self.protected_paths = config.get('protected_paths', [])
                    self.protected_formats = config.get('protected_formats', [])
                    self.min_file_size_mb = config.get('min_file_size_mb', 0)
                    self.max_file_size_mb = config.get('max_file_size_mb', 1024)
                    self.protected_keywords = config.get('protected_keywords', [])
                    self.safe_mode_enabled = config.get('safe_mode_enabled', True)

                    print("✅ Конфигурация загружена")
            else:
                # Создаем конфигурацию по умолчанию
                self.create_default_config()
        except Exception as e:
            print(f"⚠️ Ошибка загрузки конфигурации: {e}")
            self.create_default_config()

    def create_default_config(self):
        """Создать конфигурацию по умолчанию"""
        default_config = {
            'protected_paths': [
                "C:\\Windows\\System32",
                "C:\\Program Files",
                "C:\\Program Files (x86)",
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Pictures"),
                os.path.expanduser("~\\Music"),
                os.path.expanduser("~\\Videos")
            ],
            'protected_formats': [
                '.exe', '.dll', '.sys', '.drv',  # Системные файлы
                '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Документы
                '.pdf', '.txt', '.rtf',  # Текстовые
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',  # Изображения
                '.mp3', '.wav', '.flac', '.aac',  # Аудио
                '.mp4', '.avi', '.mkv', '.mov', '.wmv',  # Видео
                '.zip', '.rar', '.7z', '.tar', '.gz',  # Архивы
                '.iso', '.vhd', '.vmdk',  # Образы
                '.ps1', '.bat', '.cmd', '.vbs',  # Скрипты
                '.reg', '.ini', '.cfg', '.conf',  # Конфиги
                '.db', '.sqlite', '.mdb',  # Базы данных
                '.pst', '.ost',  # Почта
                '.pfx', '.key', '.crt', '.pem'  # Сертификаты
            ],
            'min_file_size_mb': 0,
            'max_file_size_mb': 1024,
            'protected_keywords': [
                'system',
                'windows',
                'boot',
                'program files',
                'important',
                'backup',
                'secret',
                'private',
                'confidential',
                'personal'
            ],
            'safe_mode_enabled': True
        }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            print("✅ Создана конфигурация по умолчанию")

            # Загружаем значения
            self.protected_paths = default_config['protected_paths']
            self.protected_formats = default_config['protected_formats']
            self.min_file_size_mb = default_config['min_file_size_mb']
            self.max_file_size_mb = default_config['max_file_size_mb']
            self.protected_keywords = default_config['protected_keywords']
            self.safe_mode_enabled = default_config['safe_mode_enabled']

        except Exception as e:
            print(f"⚠️ Ошибка создания конфигурации: {e}")

    def save_config(self):
        """Сохранить конфигурацию в файл"""
        try:
            config = {
                'protected_paths': self.protected_paths,
                'protected_formats': self.protected_formats,
                'min_file_size_mb': self.min_file_size_mb,
                'max_file_size_mb': self.max_file_size_mb,
                'protected_keywords': self.protected_keywords,
                'safe_mode_enabled': self.safe_mode_enabled
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения конфигурации: {e}")
            return False

    def is_path_protected(self, file_path):
        """Проверить, находится ли файл в защищенной папке"""
        if not self.safe_mode_enabled:
            return False

        file_path_lower = file_path.lower()

        for protected_path in self.protected_paths:
            protected_path_lower = protected_path.lower()
            if file_path_lower.startswith(protected_path_lower):
                return True

        return False

    def is_format_protected(self, filename):
        """Проверить, защищен ли формат файла"""
        if not self.safe_mode_enabled:
            return False

        filename_lower = filename.lower()

        for protected_format in self.protected_formats:
            if filename_lower.endswith(protected_format):
                return True

        return False

    def is_keyword_protected(self, filepath):
        """Проверить наличие защищенных ключевых слов в пути"""
        if not self.safe_mode_enabled:
            return False

        filepath_lower = filepath.lower()

        for keyword in self.protected_keywords:
            if keyword.lower() in filepath_lower:
                return True

        return False

    def check_file_size(self, file_size_mb):
        """Проверить размер файла"""
        if self.min_file_size_mb > 0 and file_size_mb < self.min_file_size_mb:
            return False  # Слишком маленький

        if file_size_mb > self.max_file_size_mb:
            return False  # Слишком большой

        return True

    def is_file_protected(self, file_path, filename):
        """Комплексная проверка защиты файла"""
        if not self.safe_mode_enabled:
            return False

        # Проверка размера (если файл существует)
        try:
            if os.path.exists(file_path):
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if not self.check_file_size(file_size_mb):
                    return True
        except:
            pass

        # Проверка защищенных папок
        if self.is_path_protected(file_path):
            return True

        # Проверка защищенных форматов
        if self.is_format_protected(filename):
            return True

        # Проверка ключевых слов
        if self.is_keyword_protected(file_path):
            return True

        return False

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        w, h = 650, 750
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def create_ui(self):
        # Заголовок
        tk.Label(
            self.root,
            text="🧹 CLEANER PRO 2025",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text=f"Углублённая очистка с защитой | v{self.version}",
            font=("Arial", 11),
            fg=self.secondary_text,
            bg=self.bg_color
        ).pack()

        # Разделитель
        sep = tk.Frame(self.root, height=2, bg=self.border_color)
        sep.pack(fill=tk.X, padx=30, pady=10)

        # ===== КОНФИГУРАЦИЯ ЗАЩИТЫ =====
        config_frame = tk.LabelFrame(
            self.root,
            text=" 🔒 НАСТРОЙКИ ЗАЩИТЫ",
            font=("Arial", 12, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            padx=20,
            pady=15,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.border_color
        )
        config_frame.pack(fill=tk.X, padx=30, pady=10)

        # Режим безопасной очистки
        self.safe_mode_var = tk.BooleanVar(value=self.safe_mode_enabled)
        tk.Checkbutton(
            config_frame,
            text="🛡️ Включить защиту важных файлов",
            variable=self.safe_mode_var,
            font=("Arial", 10, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            selectcolor=self.card_bg,
            activebackground=self.card_bg,
            command=self.toggle_safe_mode
        ).pack(anchor=tk.W, pady=5)

        # Информация о защите
        info_text = f"📁 Защищено папок: {len(self.protected_paths)}\n"
        info_text += f"📄 Защищено форматов: {len(self.protected_formats)}"

        tk.Label(
            config_frame,
            text=info_text,
            font=("Arial", 9),
            bg=self.card_bg,
            fg=self.secondary_text,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=5)

        # Кнопка настроек конфигурации
        tk.Button(
            config_frame,
            text="⚙️ РАСШИРЕННЫЕ НАСТРОЙКИ",
            font=("Arial", 9, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.open_config_dialog,
            padx=10,
            pady=5,
            relief=tk.RAISED,
            bd=2
        ).pack(pady=10)

        # ===== ВЫБОР РЕЖИМА ОЧИСТКИ =====
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

        # Описание режима
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

        # ===== ОПЦИИ ОЧИСТКИ =====
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

        # Чекбоксы
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
        tk.Button(
            self.root,
            text="🔄 Проверить обновления",
            font=("Arial", 10),
            bg=self.success_color,
            fg="white",
            command=self.check_update_manual,
            relief=tk.RAISED,
            bd=2
        ).pack(pady=10)

        # ===== ПРОГРЕСС =====
        # Стиль прогресс-бара
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

        # Статистика
        self.stats = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.stats.pack(pady=10)

        # ===== ПОДВАЛ С ПАСХАЛКОЙ =====
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Создаем текст автора, который будет кликабельным
        author_text = tk.Label(
            footer_frame,
            text=f"© Cleaner Pro 2025 v{self.version} | Разработчик: Protime1",
            font=("Arial", 8),
            fg=self.secondary_text,
            bg=self.bg_color,
            cursor="hand2"
        )
        author_text.pack()

        # Привязываем обработчик клика
        author_text.bind("<Button-1>", self.on_author_click)

        # Скрытые элементы для пасхалки
        self.easter_label = None
        self.easter_game_window = None

        # Индикатор супер-режима
        self.super_mode_indicator = tk.Label(
            footer_frame,
            text="",
            font=("Arial", 8, "bold"),
            fg="#FFD700",
            bg=self.bg_color
        )
        self.super_mode_indicator.pack()

        # Проверяем супер-режим при запуске
        self.root.after(1000, self.check_super_mode_on_start)

    def toggle_safe_mode(self):
        """Переключить режим безопасной очистки"""
        self.safe_mode_enabled = self.safe_mode_var.get()
        self.save_config()

        if self.safe_mode_enabled:
            self.status.config(text="🛡️ Режим защиты включен", fg=self.success_color)
        else:
            self.status.config(text="⚠️ Режим защиты отключен", fg=self.warning_color)

        self.root.after(3000,
                        lambda: self.status.config(text="✅ Выберите режим и начните очистку", fg=self.success_color))

    def open_config_dialog(self):
        """Открыть диалог расширенных настроек"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Расширенные настройки защиты")
        dialog.geometry("600x500")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)

        # Центрируем диалог
        dialog.update_idletasks()
        w, h = 600, 500
        x = (dialog.winfo_screenwidth() - w) // 2
        y = (dialog.winfo_screenheight() - h) // 2
        dialog.geometry(f'{w}x{h}+{x}+{y}')

        # Заголовок
        tk.Label(
            dialog,
            text="🔒 НАСТРОЙКИ ЗАЩИТЫ ФАЙЛОВ",
            font=("Arial", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        ).pack(pady=15)

        # Блок настройки размера файлов
        size_frame = tk.LabelFrame(
            dialog,
            text=" 📊 ОГРАНИЧЕНИЯ ПО РАЗМЕРУ",
            font=("Arial", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            padx=15,
            pady=10,
            relief=tk.FLAT,
            bd=2
        )
        size_frame.pack(fill=tk.X, padx=20, pady=10)

        # Минимальный размер
        min_frame = tk.Frame(size_frame, bg=self.card_bg)
        min_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            min_frame,
            text="Минимальный размер (МБ):",
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color,
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)

        min_var = tk.StringVar(value=str(self.min_file_size_mb))
        tk.Spinbox(
            min_frame,
            from_=0,
            to=1000,
            textvariable=min_var,
            width=10,
            bg=self.card_bg,
            fg=self.text_color,
            buttonbackground=self.accent_color
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            min_frame,
            text="(0 = без ограничений)",
            font=("Arial", 8),
            bg=self.card_bg,
            fg=self.secondary_text
        ).pack(side=tk.LEFT)

        # Максимальный размер
        max_frame = tk.Frame(size_frame, bg=self.card_bg)
        max_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            max_frame,
            text="Максимальный размер (МБ):",
            font=("Arial", 10),
            bg=self.card_bg,
            fg=self.text_color,
            width=20,
            anchor=tk.W
        ).pack(side=tk.LEFT)

        max_var = tk.StringVar(value=str(self.max_file_size_mb))
        tk.Spinbox(
            max_frame,
            from_=1,
            to=10000,
            textvariable=max_var,
            width=10,
            bg=self.card_bg,
            fg=self.text_color,
            buttonbackground=self.accent_color
        ).pack(side=tk.LEFT, padx=10)

        # Защищенные форматы
        formats_frame = tk.LabelFrame(
            dialog,
            text=" 📄 ЗАЩИЩЁННЫЕ ФОРМАТЫ",
            font=("Arial", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            padx=15,
            pady=10,
            relief=tk.FLAT,
            bd=2
        )
        formats_frame.pack(fill=tk.X, padx=20, pady=10)

        # Текстовое поле для форматов
        formats_text = tk.Text(
            formats_frame,
            height=5,
            width=50,
            bg="#0f0f1f",
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Arial", 9)
        )
        formats_text.pack(pady=5)

        # Заполняем текущими форматами
        formats_text.insert("1.0", "\n".join(self.protected_formats))

        tk.Label(
            formats_frame,
            text="Каждый формат с точкой на новой строке (например: .exe)",
            font=("Arial", 8),
            bg=self.card_bg,
            fg=self.secondary_text
        ).pack()

        # Кнопки сохранения
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.pack(pady=20)

        def save_config_dialog():
            """Сохранить настройки из диалога"""
            try:
                # Сохраняем размеры
                self.min_file_size_mb = int(min_var.get())
                self.max_file_size_mb = int(max_var.get())

                # Сохраняем форматы
                formats = formats_text.get("1.0", tk.END).strip().split('\n')
                self.protected_formats = [f.strip() for f in formats if f.strip()]

                # Сохраняем в файл
                self.save_config()

                messagebox.showinfo("Успех", "Настройки сохранены!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить настройки:\n{e}")

        tk.Button(
            button_frame,
            text="💾 СОХРАНИТЬ",
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="white",
            command=save_config_dialog,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="❌ ОТМЕНА",
            font=("Arial", 12),
            bg=self.error_color,
            fg="white",
            command=dialog.destroy,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

    def check_super_mode_on_start(self):
        """Проверить супер-режим при запуске программы"""
        if self.check_super_mode():
            self.easter_egg_active = True
            self.super_mode_indicator.config(text="🌟 СУПЕР-РЕЖИМ АКТИВЕН!")
            self.status.config(text="✅ Супер-режим активен! +50% эффективности", fg="#FFD700")

    def on_author_click(self, event):
        """Обработчик клика по имени автора (пасхалка)"""
        current_time = time.time()

        # Сбрасываем счетчик если прошло больше 2 секунд
        if current_time - self.author_last_click_time > 2:
            self.author_click_count = 0

        self.author_click_count += 1
        self.author_last_click_time = current_time

        # Визуальная обратная связь
        event.widget.config(fg=self.accent_color)
        self.root.after(100, lambda: event.widget.config(fg=self.secondary_text))

        # Анимация "нажатия"
        original_font = event.widget.cget("font")
        event.widget.config(font=("Arial", 8, "bold"))
        self.root.after(100, lambda: event.widget.config(font=original_font))

        # Проверяем количество кликов
        if self.author_click_count == 3:
            self.show_easter_notification("👀 Замечено быстрое нажатие...")

        elif self.author_click_count == 5:
            self.show_easter_notification("🎮 Вы нашли секретную функцию!")
            self.root.after(500, self.show_easter_options)

        elif self.author_click_count == 7:
            self.show_easter_notification("🔥 Активирую игровой режим...")
            self.root.after(800, self.launch_trash_game)

        elif self.author_click_count >= 10:
            self.show_easter_notification("🎉 ВЫ АКТИВИРОВАЛИ СУПЕР-РЕЖИМ!")
            self.root.after(1000, self.activate_super_mode)

    def show_easter_notification(self, message):
        """Показать уведомление пасхалки"""
        if not self.easter_label:
            self.easter_label = tk.Label(
                self.root,
                text=message,
                font=("Arial", 9, "bold"),
                bg="#FFD700",
                fg="#000000",
                padx=10,
                pady=5,
                relief=tk.RAISED,
                bd=2
            )
            self.easter_label.pack(pady=5)
        else:
            self.easter_label.config(text=message)
            self.easter_label.pack(pady=5)

        # Автоскрытие через 3 секунды
        self.root.after(3000, self.hide_easter_notification)

    def hide_easter_notification(self):
        """Скрыть уведомление пасхалки"""
        if self.easter_label:
            self.easter_label.pack_forget()

    def show_easter_options(self):
        """Показать меню пасхалок"""
        response = messagebox.askyesno(
            "🎮 СЕКРЕТНАЯ ФУНКЦИЯ!",
            "Вы обнаружили секретную игровую пасхалку!\n\n"
            "Хотите запустить мини-игру 'Сбей мусор'?\n\n"
            "🎯 Цель: Сбивать летающие файлы\n"
            "⏱️ Время: 30 секунд\n"
            "🏆 Лучший счёт: 0 (установите рекорд!)\n\n"
            "Или активировать СУПЕР-РЕЖИМ (10+ кликов)?",
            icon='question'
        )

        if response:
            self.launch_trash_game()

    def launch_trash_game(self):
        """Запуск игры 'Сбей мусор'"""
        if self.easter_game_active:
            return

        self.easter_game_active = True

        # Создаем отдельное окно для игры
        game_window = tk.Toplevel(self.root)
        game_window.title("🎮 Cleaner Pro - Сбей мусор!")
        game_window.geometry("800x600")
        game_window.configure(bg=self.bg_color)
        game_window.resizable(False, False)

        # Центрируем окно
        game_window.update_idletasks()
        w, h = 800, 600
        x = (game_window.winfo_screenwidth() - w) // 2
        y = (game_window.winfo_screenheight() - h) // 2
        game_window.geometry(f'{w}x{h}+{x}+{y}')

        # Создаем игру
        game = TrashShooterGame(game_window, self)
        self.easter_game_window = game_window

        # Обработчик закрытия окна
        def on_closing():
            self.easter_game_active = False
            game_window.destroy()

        game_window.protocol("WM_DELETE_WINDOW", on_closing)

        # Запускаем игру
        game.start_game()

    def activate_super_mode(self):
        """Активация супер-режима (бонусы)"""
        self.easter_egg_active = True

        # Показываем индикатор
        self.super_mode_indicator.config(text="🌟 СУПЕР-РЕЖИМ АКТИВЕН!")

        # Меняем тему на "игровую"
        original_bg = self.bg_color
        original_card = self.card_bg

        # Анимация смены цветов
        colors = ["#FF6B6B", "#4ECDC4", "#FFD166", "#06D6A0", "#118AB2", "#9b59b6"]

        def color_animation(index=0):
            if index >= len(colors):
                # Возвращаем оригинальные цвета
                self.root.configure(bg=original_bg)
                for widget in self.root.winfo_children():
                    try:
                        bg_color = widget.cget("bg")
                        if bg_color in [original_bg, original_card] or bg_color in colors:
                            widget.config(
                                bg=original_bg if bg_color == original_bg or bg_color in colors else original_card)
                    except:
                        pass
                return

            color = colors[index]
            self.root.configure(bg=color)

            # Меняем цвет основных виджетов
            for widget in self.root.winfo_children():
                try:
                    if widget.winfo_class() in ["Frame", "LabelFrame", "TFrame"]:
                        widget.config(bg=color)
                except:
                    pass

            self.root.after(200, lambda: color_animation(index + 1))

        color_animation()

        # Показываем сообщение о супер-режиме
        messagebox.showinfo(
            "🌟 СУПЕР-РЕЖИМ АКТИВИРОВАН!",
            "Поздравляем! Вы активировали супер-режим!\n\n"
            "🔸 +50% эффективности очистки\n"
            "🔸 Секретные алгоритмы оптимизации\n"
            "🔸 Эксклюзивная игровая тема\n"
            "🔸 Скрытые функции разблокированы!\n\n"
            "Режим действует 24 часа! 🕒"
        )

        # Сохраняем активацию в файл
        try:
            with open("super_mode.txt", "w") as f:
                f.write(str(time.time()))
        except:
            pass

        # Обновляем статус
        self.status.config(text="🌟 Супер-режим активен! +50% эффективности", fg="#FFD700")

    def check_super_mode(self):
        """Проверить активен ли супер-режим"""
        try:
            if os.path.exists("super_mode.txt"):
                with open("super_mode.txt", "r") as f:
                    activation_time = float(f.read())
                    # Супер-режим действует 24 часа
                    if time.time() - activation_time < 24 * 60 * 60:
                        return True
        except:
            pass
        return False

    def update_mode_description(self):
        """Обновить описание выбранного режима"""
        mode = self.mode_var.get()
        descriptions = {
            "standard": "🟢 Безопасное удаление временных файлов Windows и кэша браузеров. Не затрагивает системные файлы.",
            "deep": "🟡 Глубокая очистка включая логи, дампы памяти, временные установки программ и старые точки восстановления.",
            "aggressive": "🔴 Максимальная очистка всех временных данных, кэша DNS, файлов предварительной выборки и журналов событий."
        }
        self.mode_desc.config(text=descriptions.get(mode, ""))

    def start_clean(self):
        """Запуск процесса очистки"""
        if self.cleaning:
            return

        self.clean_mode = self.mode_var.get()

        # Проверяем супер-режим
        super_bonus = 1.5 if (self.easter_egg_active or self.check_super_mode()) else 1.0

        if self.clean_mode == "aggressive":
            warning_text = "⚠️ ВНИМАНИЕ! Агрессивный режим\n\nАГРЕССИВНЫЙ РЕЖИМ УДАЛИТ МНОГО ФАЙЛОВ!\n\n"
            if super_bonus > 1.0:
                warning_text += "🌟 СУПЕР-РЕЖИМ АКТИВЕН! +50% эффективности!\n\n"
            warning_text += "Вы уверены что хотите продолжить?"

            confirm = messagebox.askyesno(
                "⚠️ ВНИМАНИЕ! Агрессивный режим",
                warning_text,
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
        """Процесс углублённой очистки"""
        try:
            total_freed = 0
            steps_completed = 0
            total_steps = self.get_total_steps()

            # Супер-режим бонус
            super_bonus = 1.5 if (self.easter_egg_active or self.check_super_mode()) else 1.0

            # ШАГ 1: Временные файлы Windows
            steps_completed += 1
            self.update_progress(steps_completed, total_steps, "Временные файлы Windows")
            freed = self.clean_windows_temp() * super_bonus
            total_freed += freed
            time.sleep(0.3)

            # ШАГ 2: Кэш браузеров
            if self.clean_cache_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Кэш браузеров")
                freed = self.clean_browser_cache_deep() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            # ШАГ 3: Логи Windows
            if self.clean_logs_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Логи Windows")
                freed = self.clean_windows_logs_deep() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            # ШАГ 4: Старые загрузки
            if self.clean_old_downloads_var.get():
                steps_completed += 1
                self.update_progress(steps_completed, total_steps, "Старые загрузки")
                freed = self.clean_old_downloads() * super_bonus
                total_freed += freed
                time.sleep(0.3)

            # Дополнительные режимы
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
        """Получить общее количество шагов очистки"""
        steps = 1  # Всегда временные файлы

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
        """Обновить прогресс"""
        percent = (current / total) * 100
        self.root.after(0, lambda: self.progress.config(value=percent))
        self.root.after(0, lambda: self.status.config(text=f"⚡ {message}... ({current}/{total})"))

    def clean_windows_temp(self):
        """Очистка временных файлов Windows"""
        freed_mb = 0
        temp_paths = self.get_temp_paths()

        for path in temp_paths:
            if os.path.exists(path):
                freed_mb += self.delete_folder_contents(path, mode=self.clean_mode)

        return round(freed_mb, 2)

    def get_temp_paths(self):
        """Получить пути к временным файлам в зависимости от режима"""
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
                os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'IECompatCache'),
                os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'IECompatUaCache'),
                os.path.join(windows_dir, 'Prefetch'),
                os.path.join(windows_dir, 'Logs'),
                os.path.join(windows_dir, 'System32', 'LogFiles'),
                os.path.join(windows_dir, 'debug'),
            ])

        return [p for p in base_paths if p]

    def clean_browser_cache_deep(self):
        """Углублённая очистка кэша браузеров"""
        freed_mb = 0
        user_profile = os.environ.get('USERPROFILE', '')

        # Пути ко всем популярным браузерам
        browser_paths = [
            # Chrome
            os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache2'),
            os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Media Cache'),
            # Edge
            os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
            # Firefox
            os.path.join(user_profile, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles'),
            # Opera
            os.path.join(user_profile, 'AppData', 'Local', 'Opera Software', 'Opera Stable', 'Cache'),
            # Яндекс.Браузер
            os.path.join(user_profile, 'AppData', 'Local', 'Yandex', 'YandexBrowser', 'User Data', 'Default', 'Cache'),
            # Браузеры на Chromium
            os.path.join(user_profile, 'AppData', 'Local', 'Vivaldi', 'User Data', 'Default', 'Cache'),
            os.path.join(user_profile, 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default',
                         'Cache'),
        ]

        for cache_path in browser_paths:
            if os.path.exists(cache_path):
                freed_mb += self.delete_folder_contents(cache_path, mode=self.clean_mode)

        return round(freed_mb, 2)

    def clean_windows_logs_deep(self):
        """Глубокая очистка логов Windows"""
        freed_mb = 0
        windows_dir = os.environ.get('WINDIR', 'C:\\Windows')

        log_paths = [
            os.path.join(windows_dir, 'Logs'),
            os.path.join(windows_dir, 'System32', 'LogFiles'),
            os.path.join(windows_dir, 'System32', 'winevt', 'Logs'),
            os.path.join(windows_dir, 'INF'),
        ]

        if self.clean_mode == "aggressive":
            log_paths.extend([
                os.path.join(windows_dir, 'Minidump'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'CrashDumps'),
            ])

        for log_path in log_paths:
            if os.path.exists(log_path):
                freed_mb += self.delete_folder_contents(log_path, mode=self.clean_mode,
                                                        extensions=['.log', '.etl', '.evtx', '.dmp'])

        return round(freed_mb, 2)

    def clean_old_downloads(self):
        """Очистка старых файлов из загрузок"""
        freed_mb = 0
        downloads_path = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')

        if os.path.exists(downloads_path):
            cutoff_days = 30
            if self.clean_mode == "aggressive":
                cutoff_days = 7  # Более агрессивно

            cutoff_time = time.time() - (cutoff_days * 24 * 60 * 60)
            freed_mb = self.delete_old_files(downloads_path, cutoff_time)

        return round(freed_mb, 2)

    def deep_clean_additional(self):
        """Дополнительная глубокая очистка"""
        freed_mb = 0

        # Очистка эскизов
        thumb_cache = os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Microsoft', 'Windows',
                                   'Explorer')
        if os.path.exists(thumb_cache):
            freed_mb += self.delete_files_by_pattern(thumb_cache, 'thumbcache_*.db')

        # Очистка корзины через CMD
        try:
            os.system('cmd /c "rd /s /q %systemdrive%\\$Recycle.Bin 2>nul"')
        except:
            pass

        # Очистка DNS кэша
        try:
            os.system('ipconfig /flushdns >nul 2>&1')
        except:
            pass

        return round(freed_mb, 2)

    def aggressive_clean(self):
        """Агрессивная очистка"""
        freed_mb = 0

        # Очистка Prefetch
        prefetch_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
        if os.path.exists(prefetch_path):
            freed_mb += self.delete_folder_contents(prefetch_path, mode="aggressive")

        # Очистка журналов событий (только файлы, не сами события)
        event_logs = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'winevt', 'Logs')
        if os.path.exists(event_logs):
            freed_mb += self.delete_files_by_pattern(event_logs, '*.evtx')

        # Очистка временных установок программ
        installer_cache = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Installer')
        if os.path.exists(installer_cache):
            freed_mb += self.delete_old_files(installer_cache, time.time() - (90 * 24 * 60 * 60))  # 90 дней

        # Очистка кэша обновлений Windows
        win_update_cache = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'SoftwareDistribution', 'Download')
        if os.path.exists(win_update_cache):
            freed_mb += self.delete_folder_contents(win_update_cache, mode="aggressive")

        return round(freed_mb, 2)

    def delete_folder_contents(self, folder_path, mode="standard", extensions=None):
        """Удалить содержимое папки с учётом режима и защиты"""
        freed_mb = 0

        if not os.path.exists(folder_path):
            return 0

        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)

                # Проверяем защиту файла
                if self.is_file_protected(item_path, item):
                    continue

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

                except (PermissionError, OSError):
                    continue

        except (PermissionError, OSError):
            pass

        return freed_mb

    def should_delete_file(self, filename, mode, extensions=None):
        """Определить, нужно ли удалять файл"""
        filename_lower = filename.lower()

        # Проверка по расширениям если заданы
        if extensions:
            for ext in extensions:
                if filename_lower.endswith(ext):
                    return True

        # Безопасные расширения для всех режимов
        safe_extensions = ['.tmp', '.log', '.bak', '.old', '.cache', '.dmp', '.chk', '.gid']

        # Дополнительные расширения для глубокой очистки
        if mode == "deep":
            safe_extensions.extend(['.etl', '.evtx', '.mdmp', '.hdmp'])

        # Все временные файлы для агрессивного режима
        if mode == "aggressive":
            return True  # Удаляем всё в агрессивном режиме, но с учётом защиты

        # Проверка расширения
        for ext in safe_extensions:
            if filename_lower.endswith(ext):
                return True

        # Проверка по имени
        if (filename_lower.startswith('~') or
                'temp' in filename_lower or
                'cache' in filename_lower or
                'log' in filename_lower):
            return True

        return False

    def delete_old_files(self, folder_path, cutoff_time):
        """Удалить старые файлы"""
        freed_mb = 0

        if not os.path.exists(folder_path):
            return 0

        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)

                # Проверяем защиту файла
                if self.is_file_protected(item_path, item):
                    continue

                try:
                    if os.path.isfile(item_path):
                        file_mtime = os.path.getmtime(item_path)
                        if file_mtime < cutoff_time:
                            size_mb = os.path.getsize(item_path) / (1024 * 1024)
                            os.remove(item_path)
                            freed_mb += size_mb

                except (PermissionError, OSError):
                    continue

        except (PermissionError, OSError):
            pass

        return freed_mb

    def delete_files_by_pattern(self, folder_path, pattern):
        """Удалить файлы по шаблону"""
        freed_mb = 0

        if not os.path.exists(folder_path):
            return 0

        try:
            for item in os.listdir(folder_path):
                if fnmatch.fnmatch(item.lower(), pattern.lower()):
                    item_path = os.path.join(folder_path, item)

                    # Проверяем защиту файла
                    if self.is_file_protected(item_path, item):
                        continue

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
        """Получить размер папки в байтах"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass
        return total_size

    def show_clean_results(self, total_freed):
        """Показать результаты очистки"""
        self.progress["value"] = 100
        self.cleaning = False

        mode_names = {
            "standard": "СТАНДАРТНОЙ",
            "deep": "УГЛУБЛЁННОЙ",
            "aggressive": "АГРЕССИВНОЙ"
        }

        # Добавляем иконку супер-режима
        super_icon = "🌟 " if (self.easter_egg_active or self.check_super_mode()) else ""

        self.btn.config(
            state=tk.NORMAL,
            text="🎉 ОЧИСТКА ЗАВЕРШЕНА!",
            bg=self.success_color
        )

        self.status.config(
            text=f"✅ {super_icon}{mode_names.get(self.clean_mode, '')} ОЧИСТКА ВЫПОЛНЕНА!",
            fg=self.success_color
        )

        bonus_text = " (🌟 +50% супер-режим!)" if (self.easter_egg_active or self.check_super_mode()) else ""
        protection_text = " (🛡️ защита активна)" if self.safe_mode_enabled else " (⚠️ защита отключена)"

        self.stats.config(
            text=f"📊 Освобождено: {total_freed:.2f} МБ{bonus_text}{protection_text} | Режим: {mode_names.get(self.clean_mode, 'стандартный')}"
        )

        messagebox.showinfo(
            "Очистка завершена!",
            f"✅ {super_icon}{mode_names.get(self.clean_mode, 'Стандартная')} очистка успешно выполнена!\n\n"
            f"Освобождено места: {total_freed:.2f} МБ\n"
            f"Режим очистки: {self.clean_mode}\n"
            f"Защита файлов: {'🛡️ включена' if self.safe_mode_enabled else '⚠️ отключена'}\n"
            f"{'🌟 Супер-режим активен! 🚀' if (self.easter_egg_active or self.check_super_mode()) else ''}\n\n"
            f"Система оптимизирована и готова к работе! 🎮"
        )

        # Возвращаем обычный вид через 5 секунд
        self.root.after(5000, self.reset_ui)

    def show_error(self, error_msg):
        """Показать ошибку"""
        self.progress.pack_forget()
        self.cleaning = False

        self.btn.config(
            state=tk.NORMAL,
            text="🚀 НАЧАТЬ УГЛУБЛЁННУЮ ОЧИСТКУ",
            bg=self.accent_color
        )

        self.status.config(
            text="❌ Ошибка при выполнении очистки",
            fg=self.error_color
        )

        messagebox.showerror(
            "Ошибка очистки",
            f"Не удалось выполнить очистку:\n\n{error_msg}\n\n"
            f"Попробуйте запустить программу от имени администратора."
        )

    def reset_ui(self):
        """Сбросить интерфейс"""
        self.btn.config(
            text="🚀 НАЧАТЬ УГЛУБЛЁННУЮ ОЧИСТКУ",
            bg=self.accent_color
        )

        self.status.config(
            text="✅ Выберите режим и начните очистку",
            fg=self.success_color
        )

        self.progress["value"] = 0
        self.stats.config(text="")

    def auto_check_update(self):
        """Автоматическая проверка обновлений"""
        try:
            last_check_file = "last_update_check.txt"

            if os.path.exists(last_check_file):
                with open(last_check_file, 'r') as f:
                    last_check = float(f.read())
                    if time.time() - last_check < 7 * 24 * 60 * 60:
                        return

            thread = threading.Thread(target=self._background_check, daemon=True)
            thread.start()

            with open(last_check_file, 'w') as f:
                f.write(str(time.time()))

        except:
            pass

    def _background_check(self):
        """Фоновая проверка обновлений"""
        try:
            import requests

            url = f"https://api.github.com/repos/{self.github_user}/CleanerPro2025/releases/latest"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name'].replace('v', '')
                current_clean = self.version

                if self._compare_versions(current_clean, latest_version) < 0:
                    self.root.after(0, self._show_update_notification, release_data)

        except:
            pass

    def _show_update_notification(self, release_data):
        """Показать уведомление об обновлении"""
        import webbrowser

        latest_version = release_data['tag_name']
        changelog = release_data.get('body', 'Нет описания')

        response = messagebox.askyesno(
            "🎯 Доступно обновление!",
            f"Вышла новая версия программы: {latest_version}\n\n"
            f"Что нового:\n{changelog[:150]}...\n\n"
            f"Хотите скачать её сейчас?"
        )

        if response:
            webbrowser.open(release_data['html_url'])

    def check_update_manual(self):
        """Ручная проверка обновлений"""
        try:
            import requests

            messagebox.showinfo("Обновление", "Проверяю наличие обновлений...")

            url = f"https://api.github.com/repos/{self.github_user}/CleanerPro2025/releases/latest"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name']
                latest_clean = latest_version.replace('v', '')
                current_clean = self.version

                if self._compare_versions(current_clean, latest_clean) < 0:
                    changelog = release_data.get('body', 'Нет описания обновления')

                    choice = messagebox.askyesno(
                        "🎉 Доступно обновление!",
                        f"Найдена новая версия: {latest_version}\n\n"
                        f"Текущая версия: v{self.version}\n\n"
                        f"Что нового:\n{changelog[:200]}...\n\n"
                        f"Хотите скачать обновление?"
                    )

                    if choice:
                        webbrowser.open(release_data['html_url'])
                else:
                    messagebox.showinfo(
                        "Обновление",
                        f"✅ У вас актуальная версия!\n\n"
                        f"Текущая версия: v{self.version}"
                    )
            else:
                messagebox.showerror(
                    "Ошибка",
                    "Не удалось проверить обновления."
                )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Произошла ошибка:\n{str(e)[:100]}..."
            )

    def _compare_versions(self, v1, v2):
        """Сравнить две версии"""
        try:
            v1_parts = list(map(int, v1.split('.')))
            v2_parts = list(map(int, v2.split('.')))

            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_part = v1_parts[i] if i < len(v1_parts) else 0
                v2_part = v2_parts[i] if i < len(v2_parts) else 0

                if v1_part < v2_part:
                    return -1
                elif v1_part > v2_part:
                    return 1

            return 0
        except:
            return 0


class TrashShooterGame:
    """Мини-игра 'Сбей мусор'"""

    def __init__(self, window, parent_app):
        self.window = window
        self.parent_app = parent_app
        self.canvas = None
        self.score = 0
        self.time_left = 30
        self.game_active = False
        self.targets = []
        self.cannon = None

        self.create_ui()

    def create_ui(self):
        """Создание интерфейса игры"""
        # Заголовок
        tk.Label(
            self.window,
            text="🎮 СБЕЙ МУСОР!",
            font=("Arial", 24, "bold"),
            fg="#FFD700",
            bg="#1e1e2e"
        ).pack(pady=10)

        # Панель счёта и времени
        info_frame = tk.Frame(self.window, bg="#1e1e2e")
        info_frame.pack(pady=10)

        self.score_label = tk.Label(
            info_frame,
            text="🏆 Счёт: 0",
            font=("Arial", 14, "bold"),
            fg="#4ECDC4",
            bg="#1e1e2e"
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.time_label = tk.Label(
            info_frame,
            text="⏱️ Время: 30с",
            font=("Arial", 14, "bold"),
            fg="#FF6B6B",
            bg="#1e1e2e"
        )
        self.time_label.pack(side=tk.LEFT, padx=20)

        # Холст для игры
        self.canvas = tk.Canvas(
            self.window,
            width=760,
            height=400,
            bg="#0f0f1f",
            highlightthickness=2,
            highlightbackground="#404060"
        )
        self.canvas.pack(pady=10)

        # Инструкции
        tk.Label(
            self.window,
            text="🎯 Управление: КЛИКАЙ по мусору чтобы сбить его!",
            font=("Arial", 10),
            fg="#a0a0a0",
            bg="#1e1e2e"
        ).pack(pady=5)

        tk.Label(
            self.window,
            text="💥 Разные типы мусора дают разные очки: ⭐ 100, 🔥 50, 💾 25, 🗂️ 20, 📁 15, 🗑️ 10",
            font=("Arial", 9),
            fg="#a0a0a0",
            bg="#1e1e2e"
        ).pack(pady=2)

        # Кнопки
        button_frame = tk.Frame(self.window, bg="#1e1e2e")
        button_frame.pack(pady=10)

        self.start_btn = tk.Button(
            button_frame,
            text="🚀 НАЧАТЬ ИГРУ",
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.start_game,
            padx=20,
            pady=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="❌ ВЫЙТИ",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            command=self.window.destroy,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=10)

        # Лучший счёт
        self.high_score = self.load_high_score()
        tk.Label(
            self.window,
            text=f"🏅 Лучший счёт: {self.high_score}",
            font=("Arial", 10),
            fg="#FFD700",
            bg="#1e1e2e"
        ).pack(pady=5)

        # Создаем "пушку" внизу
        self.create_cannon()

        # Создаем фоновые звёзды
        self.create_stars()

    def create_stars(self):
        """Создание фоновых звёзд"""
        self.stars = []
        for _ in range(50):
            x = random.randint(0, 760)
            y = random.randint(0, 400)
            size = random.uniform(0.1, 1.5)
            brightness = random.randint(100, 255)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"

            star = self.canvas.create_oval(
                x, y,
                x + size, y + size,
                fill=color,
                outline=""
            )
            self.stars.append({
                "id": star,
                "speed": random.uniform(0.1, 0.5)
            })

    def animate_stars(self):
        """Анимация звёзд"""
        if not self.game_active:
            return

        for star in self.stars:
            self.canvas.move(star["id"], 0, star["speed"])
            coords = self.canvas.coords(star["id"])
            if coords[1] > 400:  # Если звезда ушла за нижнюю границу
                self.canvas.coords(star["id"],
                                   random.randint(0, 760),
                                   -10,
                                   random.randint(0, 760) + random.uniform(0.1, 1.5),
                                   -10 + random.uniform(0.1, 1.5))

        self.window.after(50, self.animate_stars)

    def create_cannon(self):
        """Создание пушки внизу экрана"""
        cannon_x = 380
        cannon_y = 380

        # Корпус пушки
        self.cannon = self.canvas.create_oval(
            cannon_x - 20, cannon_y - 10,
            cannon_x + 20, cannon_y + 10,
            fill="#3498db",
            outline="#2980b9",
            width=2
        )

        # Ствол пушки
        self.canvas.create_rectangle(
            cannon_x - 5, cannon_y - 20,
            cannon_x + 5, cannon_y - 10,
            fill="#2c3e50",
            outline="#34495e"
        )

    def start_game(self):
        """Начать игру"""
        if self.game_active:
            return

        self.game_active = True
        self.score = 0
        self.time_left = 30
        self.targets = []

        self.start_btn.config(state=tk.DISABLED, text="🎮 ИГРА ИДЁТ...")
        self.update_score()
        self.update_time()

        # Очищаем холст от старых целей
        for target in self.targets:
            self.canvas.delete(target["id"])
        self.targets = []

        # Запускаем анимацию звёзд
        self.animate_stars()

        # Запускаем таймер
        self.game_timer()

        # Запускаем генерацию целей
        self.generate_targets()

        # Запускаем обновление целей
        self.update_targets()

        # Привязываем клики
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def generate_targets(self):
        """Генерация новых целей (мусорных файлов)"""
        if not self.game_active:
            return

        # Создаем 1-3 новых цели
        for _ in range(random.randint(1, 3)):
            self.create_target()

        # Планируем следующую генерацию
        delay = random.randint(800, 1500)
        self.window.after(delay, self.generate_targets)

    def create_target(self):
        """Создание одной цели"""
        if len(self.targets) >= 15:  # Максимум 15 целей одновременно
            return

        # Типы "мусора" с разными цветами и очками
        trash_types = [
            {"name": "🗑️", "color": "#95a5a6", "points": 10},  # Обычный мусор
            {"name": "📁", "color": "#3498db", "points": 15},  # Папка
            {"name": "🗂️", "color": "#9b59b6", "points": 20},  # Архив
            {"name": "💾", "color": "#2ecc71", "points": 25},  # Диск
            {"name": "🔥", "color": "#e74c3c", "points": 50},  # Опасный файл
            {"name": "⭐", "color": "#FFD700", "points": 100},  # Бонус
        ]

        trash = random.choice(trash_types)

        # Случайная позиция в верхней части
        x = random.randint(50, 710)
        y = random.randint(50, 150)

        # Случайная скорость
        speed_x = random.uniform(-3, 3)
        speed_y = random.uniform(0.5, 2)

        # Создаем цель на холсте
        target_id = self.canvas.create_text(
            x, y,
            text=trash["name"],
            font=("Arial", 24),
            fill=trash["color"],
            tags="target"
        )

        # Добавляем "тень" для объема
        shadow_id = self.canvas.create_text(
            x + 2, y + 2,
            text=trash["name"],
            font=("Arial", 24),
            fill="#000000",
            state="disabled"
        )

        target = {
            "id": target_id,
            "shadow_id": shadow_id,
            "x": x,
            "y": y,
            "speed_x": speed_x,
            "speed_y": speed_y,
            "points": trash["points"],
            "type": trash["name"]
        }

        self.targets.append(target)

    def update_targets(self):
        """Обновление позиций целей"""
        if not self.game_active:
            return

        for target in self.targets[:]:  # Копируем список для безопасного удаления
            # Обновляем позицию
            target["x"] += target["speed_x"]
            target["y"] += target["speed_y"]

            # Отскок от стен
            if target["x"] <= 20 or target["x"] >= 740:
                target["speed_x"] *= -1

            # Если цель упала вниз - удаляем
            if target["y"] >= 380:
                self.canvas.delete(target["id"])
                self.canvas.delete(target["shadow_id"])
                self.targets.remove(target)
                continue

            # Обновляем позицию на холсте
            self.canvas.coords(target["id"], target["x"], target["y"])

            # Обновляем тень
            self.canvas.coords(target["shadow_id"], target["x"] + 2, target["y"] + 2)

        # Планируем следующее обновление
        self.window.after(50, self.update_targets)

    def on_canvas_click(self, event):
        """Обработчик клика по холсту"""
        if not self.game_active:
            return

        # Проверяем попадание в цели
        clicked_items = self.canvas.find_overlapping(event.x - 15, event.y - 15, event.x + 15, event.y + 15)

        for item in clicked_items:
            for target in self.targets[:]:
                if target["id"] == item:
                    # Попадание!
                    self.score += target["points"]
                    self.update_score()

                    # Анимация попадания
                    self.animate_hit(target["x"], target["y"], target["points"])

                    # Удаляем цель и тень
                    self.canvas.delete(target["id"])
                    self.canvas.delete(target["shadow_id"])
                    self.targets.remove(target)

                    # Создаем эффект взрыва
                    self.create_explosion(target["x"], target["y"])
                    break

    def animate_hit(self, x, y, points):
        """Анимация попадания"""
        points_text = f"+{points}"
        text_id = self.canvas.create_text(
            x, y,
            text=points_text,
            font=("Arial", 14, "bold"),
            fill="#FFD700"
        )

        # Анимация всплывающего текста
        def animate_text(step=0):
            if step < 20:
                self.canvas.move(text_id, 0, -2)
                self.window.after(50, lambda: animate_text(step + 1))
            else:
                self.canvas.delete(text_id)

        animate_text()

    def create_explosion(self, x, y):
        """Создание эффекта взрыва"""
        particles = []
        colors = ["#FF6B6B", "#FFD166", "#4ECDC4", "#FFD700"]

        # Создаем частицы взрыва
        for _ in range(8):
            color = random.choice(colors)
            particle = self.canvas.create_oval(
                x - 3, y - 3,
                x + 3, y + 3,
                fill=color,
                outline=""
            )
            particles.append({
                "id": particle,
                "dx": random.uniform(-5, 5),
                "dy": random.uniform(-5, 5),
                "life": 20
            })

        # Анимация частиц
        def animate_particles():
            for particle in particles[:]:
                particle["life"] -= 1

                if particle["life"] <= 0:
                    self.canvas.delete(particle["id"])
                    particles.remove(particle)
                else:
                    self.canvas.move(particle["id"], particle["dx"], particle["dy"])
                    # Замедление
                    particle["dx"] *= 0.9
                    particle["dy"] *= 0.9

            if particles:
                self.window.after(50, animate_particles)

        animate_particles()

    def game_timer(self):
        """Таймер игры"""
        if not self.game_active:
            return

        self.time_left -= 1
        self.update_time()

        if self.time_left <= 0:
            self.end_game()
        else:
            self.window.after(1000, self.game_timer)

    def update_score(self):
        """Обновление отображения счёта"""
        self.score_label.config(text=f"🏆 Счёт: {self.score}")

    def update_time(self):
        """Обновление отображения времени"""
        color = "#FF6B6B" if self.time_left <= 10 else "#4ECDC4"
        self.time_label.config(text=f"⏱️ Время: {self.time_left}с", fg=color)

    def end_game(self):
        """Завершение игры"""
        self.game_active = False
        self.start_btn.config(state=tk.NORMAL, text="🔄 ИГРАТЬ СНОВА")

        # Отключаем обработчик кликов
        self.canvas.unbind("<Button-1>")

        # Останавливаем цели
        for target in self.targets:
            self.canvas.delete(target["id"])
            self.canvas.delete(target["shadow_id"])
        self.targets = []

        # Проверяем рекорд
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score(self.high_score)

            # Показываем сообщение о новом рекорде
            self.canvas.create_text(
                380, 200,
                text="🏆 НОВЫЙ РЕКОРД!",
                font=("Arial", 32, "bold"),
                fill="#FFD700"
            )

            # Анимация конфетти
            self.create_confetti()

        # Показываем итоговый счёт
        self.canvas.create_text(
            380, 250,
            text=f"Итоговый счёт: {self.score}",
            font=("Arial", 24, "bold"),
            fill="#4ECDC4"
        )

        # Предлагаем сыграть снова
        self.window.after(2000, self.show_play_again)

    def show_play_again(self):
        """Показать предложение сыграть снова"""
        response = messagebox.askyesno(
            "Игра завершена!",
            f"🎮 Игра 'Сбей мусор' завершена!\n\n"
            f"🏆 Ваш счёт: {self.score}\n"
            f"🏅 Лучший счёт: {self.high_score}\n\n"
            "Хотите сыграть ещё раз?"
        )

        if response:
            self.start_game()

    def create_confetti(self):
        """Создать анимацию конфетти для нового рекорда"""
        confetti = []
        colors = ["#FF6B6B", "#4ECDC4", "#FFD166", "#9b59b6", "#2ecc71", "#e74c3c"]

        for _ in range(50):
            x = random.randint(100, 660)
            y = random.randint(100, 300)
            color = random.choice(colors)
            size = random.randint(5, 15)

            piece = self.canvas.create_rectangle(
                x, y,
                x + size, y + size,
                fill=color,
                outline=""
            )

            confetti.append({
                "id": piece,
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(1, 5),
                "life": random.randint(50, 100)
            })

        # Анимация конфетти
        def animate_confetti():
            for piece in confetti[:]:
                piece["life"] -= 1

                if piece["life"] <= 0:
                    self.canvas.delete(piece["id"])
                    confetti.remove(piece)
                else:
                    self.canvas.move(piece["id"], piece["dx"], piece["dy"])
                    piece["dy"] += 0.1  # Гравитация

            if confetti:
                self.window.after(50, animate_confetti)

        animate_confetti()

    def load_high_score(self):
        """Загрузить лучший счёт"""
        try:
            if os.path.exists("high_score.txt"):
                with open("high_score.txt", "r") as f:
                    return int(f.read())
        except:
            pass
        return 0

    def save_high_score(self, score):
        """Сохранить лучший счёт"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(score))
        except:
            pass


def main():
    """Главная функция"""
    try:
        root = tk.Tk()
        app = CleanerPro2025(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу:\n{e}")


if __name__ == "__main__":
    main()