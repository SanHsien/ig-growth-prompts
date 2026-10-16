"""Phase 6: Desktop GUI Workbench for igprompts.

Features:
- UI Themes: Dark (深色), Light (淺色), System (跟隨 Windows 11 系統設定).
- Execution Modes: Series 1 (Faceless), Series 2 (Reels), or Both simultaneously.
- Provider Options: Manual Handoff, Local CLI Pipe, Dry Run.
- Live Logging and direct multi-channel calendar export (Notion, Airtable, Buffer, Markdown).
- Local Task Scheduler generation for Windows.
"""

from __future__ import annotations

import os
import sys
import threading
from datetime import date
from pathlib import Path
from typing import Any

from .batch import TopicItem, run_batch_queue
from .calendar import (
    export_airtable_csv,
    export_buffer_csv,
    export_markdown_calendar,
    export_notion_csv,
    generate_calendar_from_workflow_state,
)
from .core import SERIES_FACELESS, SERIES_REELS
from .providers import CommandProvider, DryRunProvider, ManualProvider
from .workflow import WorkflowRunner, WorkflowState

# Lazy-import tkinter & winreg
try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False


def detect_system_theme() -> str:
    """Detect Windows 11 / 10 Light or Dark mode via registry without external deps."""
    if sys.platform != "win32":
        return "dark"
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if value == 1 else "dark"
    except Exception:
        return "dark"


THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "bg": "#18181b",
        "panel": "#27272a",
        "panel_border": "#3f3f46",
        "fg": "#f4f4f5",
        "fg_muted": "#a1a1aa",
        "accent": "#6366f1",
        "accent_hover": "#4f46e5",
        "console_bg": "#09090b",
        "console_fg": "#e4e4e7",
        "entry_bg": "#18181b",
        "entry_fg": "#f4f4f5",
    },
    "light": {
        "bg": "#f8fafc",
        "panel": "#ffffff",
        "panel_border": "#e2e8f0",
        "fg": "#0f172a",
        "fg_muted": "#64748b",
        "accent": "#4f46e5",
        "accent_hover": "#4338ca",
        "console_bg": "#f1f5f9",
        "console_fg": "#1e293b",
        "entry_bg": "#ffffff",
        "entry_fg": "#0f172a",
    },
}


class IGPromptsGUI:
    def __init__(self, root: tk.Tk | None = None) -> None:
        if not TK_AVAILABLE:
            raise RuntimeError("tkinter is not available in this Python environment.")

        self.root = root or tk.Tk()
        self.root.title("IG Growth Prompts Workbench - 爆款內容工作台")
        self.root.geometry("900x780")
        self.root.minsize(800, 640)

        self.current_theme_mode = tk.StringVar(value="system")
        self._create_widgets()
        self.apply_theme()

    def _get_active_theme_colors(self) -> dict[str, str]:
        mode = self.current_theme_mode.get()
        if mode == "system":
            actual_mode = detect_system_theme()
        else:
            actual_mode = mode
        return THEMES.get(actual_mode, THEMES["dark"])

    def apply_theme(self) -> None:
        c = self._get_active_theme_colors()
        self.root.configure(bg=c["bg"])

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=c["bg"], foreground=c["fg"], font=("Segoe UI", 10))
        style.configure("TLabel", background=c["panel"], foreground=c["fg"])
        style.configure("Header.TLabel", background=c["panel"], font=("Segoe UI", 12, "bold"), foreground=c["accent"])
        style.configure("TCheckbutton", background=c["panel"], foreground=c["fg"])
        style.configure("TRadiobutton", background=c["panel"], foreground=c["fg"])
        style.configure("TFrame", background=c["panel"])
        style.configure("Card.TFrame", background=c["panel"], relief="flat")
        style.configure("TNotebook", background=c["bg"])
        style.configure("TNotebook.Tab", background=c["panel"], foreground=c["fg"], padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", c["accent"])], foreground=[("selected", "#ffffff")])

        # Update native components
        if hasattr(self, "txt_log"):
            self.txt_log.configure(bg=c["console_bg"], fg=c["console_fg"], insertbackground=c["fg"])
        if hasattr(self, "btn_run"):
            self.btn_run.configure(bg=c["accent"], activebackground=c["accent_hover"])
        if hasattr(self, "header_frame"):
            self.header_frame.configure(bg=c["panel"])
        if hasattr(self, "theme_box"):
            self.theme_box.configure(bg=c["panel"])

    def _create_widgets(self) -> None:
        # Top Header Bar: Title + Theme Switcher
        self.header_frame = tk.Frame(self.root, bg="#27272a", height=50)
        self.header_frame.pack(fill="x", side="top", padx=12, pady=(10, 4))

        title_lbl = tk.Label(
            self.header_frame,
            text="🚀 IG Growth Prompts Workbench",
            font=("Segoe UI", 13, "bold"),
            bg="#27272a",
            fg="#818cf8",
        )
        title_lbl.pack(side="left", padx=10, pady=8)

        # Theme Switcher Box
        self.theme_box = tk.Frame(self.header_frame, bg="#27272a")
        self.theme_box.pack(side="right", padx=10, pady=8)

        tk.Label(self.theme_box, text="風格主題: ", font=("Segoe UI", 9), bg="#27272a", fg="#a1a1aa").pack(side="left")
        for mode_val, text_lbl in [("dark", "🌙 深色"), ("light", "☀️ 淺色"), ("system", "💻 跟隨系統")]:
            rb = tk.Radiobutton(
                self.theme_box,
                text=text_lbl,
                value=mode_val,
                variable=self.current_theme_mode,
                command=self.apply_theme,
                font=("Segoe UI", 9),
                bg="#27272a",
                fg="#f4f4f5",
                selectcolor="#3f3f46",
                activebackground="#27272a",
                activeforeground="#f4f4f5",
            )
            rb.pack(side="left", padx=4)

        # Tabs Container
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tab_run = ttk.Frame(notebook)
        notebook.add(self.tab_run, text=" ⚡ 執行工作流 ")

        self.tab_cal = ttk.Frame(notebook)
        notebook.add(self.tab_cal, text=" 📅 內容發布日曆 ")

        self.tab_sched = ttk.Frame(notebook)
        notebook.add(self.tab_sched, text=" ⏰ 本地排程器 ")

        self._build_run_tab()
        self._build_calendar_tab()
        self._build_scheduler_tab()

    def _build_run_tab(self) -> None:
        p = ttk.Frame(self.tab_run, style="Card.TFrame", padding=14)
        p.pack(fill="both", expand=True)

        # 1. Series Selection
        ttk.Label(p, text="1. 選擇執行系列（可單選或同時推進兩套）", style="Header.TLabel").pack(anchor="w", pady=(0, 6))

        series_f = ttk.Frame(p)
        series_f.pack(fill="x", pady=(0, 8))

        self.var_faceless = tk.BooleanVar(value=True)
        self.var_reels = tk.BooleanVar(value=True)

        ttk.Checkbutton(series_f, text="系列 1：圖文與不露臉精準留存 (Prompts 01 ~ 05)", variable=self.var_faceless).pack(anchor="w", pady=2)
        ttk.Checkbutton(series_f, text="系列 2：短影音爆款與假設驗證 (Prompts 06 ~ 12)", variable=self.var_reels).pack(anchor="w", pady=2)

        # 2. Parameters
        ttk.Label(p, text="2. 設定內容參數", style="Header.TLabel").pack(anchor="w", pady=(8, 6))

        grid = ttk.Frame(p)
        grid.pack(fill="x", pady=(0, 8))

        ttk.Label(grid, text="🎯 利基領域:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_niche = ttk.Entry(grid, width=38)
        self.ent_niche.insert(0, "個人成長與遠端工作")
        self.ent_niche.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(grid, text="👥 目標受眾:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_audience = ttk.Entry(grid, width=38)
        self.ent_audience.insert(0, "想轉職遠端的上班族")
        self.ent_audience.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(grid, text="💡 主題/構想:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_topic = ttk.Entry(grid, width=50)
        self.ent_topic.insert(0, "新手遠端工作的3個常見誤區與破局解法")
        self.ent_topic.grid(row=2, column=1, sticky="w", padx=8, pady=4)

        # 3. Provider Mode
        ttk.Label(p, text="3. 選擇 AI 工具模式", style="Header.TLabel").pack(anchor="w", pady=(8, 6))
        prov_f = ttk.Frame(p)
        prov_f.pack(fill="x", pady=(0, 8))

        self.var_provider = tk.StringVar(value="dry-run")
        ttk.Radiobutton(prov_f, text="離線驗證 (Dry Run - 本機測試工作流完整性)", variable=self.var_provider, value="dry-run").pack(anchor="w", pady=2)
        ttk.Radiobutton(prov_f, text="手動交接 (Manual - 產生提示詞檔案，手動貼入 ChatGPT/Claude)", variable=self.var_provider, value="manual").pack(anchor="w", pady=2)
        ttk.Radiobutton(prov_f, text="本機 CLI 管道 (Command - 串接 Ollama / LLM 指令)", variable=self.var_provider, value="command").pack(anchor="w", pady=2)

        # 4. Output Dir
        dir_f = ttk.Frame(p)
        dir_f.pack(fill="x", pady=(0, 8))
        ttk.Label(dir_f, text="📁 輸出目錄:").pack(side="left")
        self.ent_out = ttk.Entry(dir_f, width=35)
        self.ent_out.insert(0, "gui_output")
        self.ent_out.pack(side="left", padx=8)

        # Action Buttons
        act_f = ttk.Frame(p)
        act_f.pack(fill="x", pady=8)

        self.btn_run = tk.Button(
            act_f,
            text=" ▶ 開始執行工作流 ",
            bg="#6366f1",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._start_run_thread,
        )
        self.btn_run.pack(side="left", padx=(0, 10))

        # Log Window
        self.txt_log = tk.Text(p, height=9, bg="#09090b", fg="#e4e4e7", font=("Consolas", 9), relief="solid", bd=1)
        self.txt_log.pack(fill="both", expand=True, pady=(6, 0))

    def _build_calendar_tab(self) -> None:
        p = ttk.Frame(self.tab_cal, style="Card.TFrame", padding=14)
        p.pack(fill="both", expand=True)

        ttk.Label(p, text="📅 多渠道內容發布日曆匯出", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(p, text="讀取工作流產出的檢查點，自動將圖文或短影音腳本轉換為各平台排程檔案。").pack(anchor="w", pady=(0, 12))

        date_f = ttk.Frame(p)
        date_f.pack(fill="x", pady=6)
        ttk.Label(date_f, text="發布起始日期 (YYYY-MM-DD):").pack(side="left")
        self.ent_cal_date = ttk.Entry(date_f, width=15)
        self.ent_cal_date.insert(0, date.today().isoformat())
        self.ent_cal_date.pack(side="left", padx=8)

        btn_grid = ttk.Frame(p)
        btn_grid.pack(fill="x", pady=10)

        formats = [
            ("匯出 Notion Database (CSV)", "notion", "#2563eb"),
            ("匯出 Airtable Content Calendar (CSV)", "airtable", "#0284c7"),
            ("匯出 Buffer 社群排程 (CSV)", "buffer", "#059669"),
            ("匯出 Markdown 視覺發布表格", "markdown", "#7c3aed"),
        ]

        for title, fmt, col in formats:
            b = tk.Button(
                btn_grid,
                text=f" {title} ",
                bg=col,
                fg="#ffffff",
                relief="flat",
                font=("Segoe UI", 10),
                pady=6,
                cursor="hand2",
                command=lambda f=fmt: self._export_calendar(f),
            )
            b.pack(anchor="w", pady=4, fill="x")

    def _build_scheduler_tab(self) -> None:
        p = ttk.Frame(self.tab_sched, style="Card.TFrame", padding=14)
        p.pack(fill="both", expand=True)

        ttk.Label(p, text="⏰ 本機自動定時排程 (Windows Task Scheduler)", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(p, text="產生 Windows 批次排程檔（.bat），可直接設定至 Windows 工作排程器，定時自動推進隊列。").pack(anchor="w", pady=(0, 12))

        tk.Button(
            p,
            text=" ⚙ 產生本機排程執行批次檔 (.bat) ",
            bg="#6366f1",
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self._generate_scheduler_script,
        ).pack(anchor="w", pady=6)

        self.txt_sched_preview = tk.Text(p, height=12, bg="#09090b", fg="#93c5fd", font=("Consolas", 9), relief="solid", bd=1)
        self.txt_sched_preview.pack(fill="both", expand=True, pady=6)

    def _log(self, msg: str) -> None:
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)

    def _start_run_thread(self) -> None:
        if not self.var_faceless.get() and not self.var_reels.get():
            messagebox.showwarning("提示", "請至少勾選一個執行系列！")
            return

        self.btn_run.config(state="disabled")
        threading.Thread(target=self._run_workflows, daemon=True).start()

    def _run_workflows(self) -> None:
        try:
            niche = self.ent_niche.get().strip()
            audience = self.ent_audience.get().strip()
            topic = self.ent_topic.get().strip()
            out_base = Path(self.ent_out.get().strip() or "gui_output")
            prov_type = self.var_provider.get()

            self._log("=== 開始執行工作流 ===")
            self._log(f"主題: {topic} | 領域: {niche}")
            self._log(f"輸出目標: {out_base.resolve()}")

            series_to_run = []
            if self.var_faceless.get():
                series_to_run.append(SERIES_FACELESS)
            if self.var_reels.get():
                series_to_run.append(SERIES_REELS)

            for s in series_to_run:
                self._log(f"\n▶ 正在推進系列: {s} ...")
                s_out = out_base / s
                s_out.mkdir(parents=True, exist_ok=True)

                if prov_type == "dry-run":
                    provider = DryRunProvider()
                elif prov_type == "manual":
                    provider = ManualProvider(s_out / "handoff")
                else:
                    provider = CommandProvider(command=os.environ.get("IGPROMPTS_LLM_CMD", "echo [Mock LLM]"))

                config = {
                    "niche": niche,
                    "audience": audience,
                    "topic": topic,
                    "idea": topic,
                    "goal": "精準留存與破圈",
                    "content": f"關於 {topic} 的深度拆解內容",
                    "tone": "專業且富有啟發",
                    "voice": "親和且直指痛點",
                    "brand_voice": "成長教練",
                }

                runner = WorkflowRunner(config=config, series=s, provider=provider)
                state_path = s_out / "workflow_state.json"
                runner.run_all(checkpoint_path=state_path)
                artifacts = runner.export_manifest(s_out)

                self._log(f"✓ 完成！Manifest: {artifacts['manifest']}")

            self._log("\n🎉 所有勾選系列已全數執行完畢！可切換至「內容發布日曆」分頁匯出排程。")
        except Exception as exc:
            self._log(f"❌ 錯誤: {exc}")
        finally:
            self.btn_run.config(state="normal")

    def _export_calendar(self, fmt: str) -> None:
        try:
            out_base = Path(self.ent_out.get().strip() or "gui_output")
            state_files = list(out_base.glob("*/workflow_state.json"))
            if not state_files:
                messagebox.showwarning("提示", f"在 {out_base} 找不到任何工作流狀態！請先執行工作流。")
                return

            entries = []
            start_date = self.ent_cal_date.get().strip()
            for sf in state_files:
                st = WorkflowState.load_checkpoint(sf)
                entries.extend(generate_calendar_from_workflow_state(st, start_date=start_date))

            exp_dir = out_base / "calendar_export"
            exp_dir.mkdir(parents=True, exist_ok=True)

            if fmt == "notion":
                target = exp_dir / "notion_database.csv"
                export_notion_csv(entries, target)
            elif fmt == "airtable":
                target = exp_dir / "airtable_calendar.csv"
                export_airtable_csv(entries, target)
            elif fmt == "buffer":
                target = exp_dir / "buffer_schedule.csv"
                export_buffer_csv(entries, target)
            else:
                target = exp_dir / "content_calendar.md"
                export_markdown_calendar(entries, target)

            messagebox.showinfo("匯出成功", f"成功匯出 {fmt.upper()} 檔案：\n{target.resolve()}")
        except Exception as exc:
            messagebox.showerror("匯出失敗", f"匯出錯誤: {exc}")

    def _generate_scheduler_script(self) -> None:
        out_base = Path(self.ent_out.get().strip() or "gui_output")
        script_path = Path("run_scheduled_pipeline.bat")
        script_content = f"""@echo off
REM ========================================================
REM IG Growth Prompts - 本機定時排程執行批次腳本
REM ========================================================
set PYTHONIOENCODING=utf-8
cd /d "{Path.cwd()}"

echo [IG Prompts] 正在執行主題隊列...
python -m igprompts batch run -f examples/sample_topics_queue.json -o {out_base} --provider dry-run

echo [IG Prompts] 正在彙整全渠道發布日曆...
python -m igprompts calendar generate --from-batch {out_base} --format all -o {out_base}/calendar_export

echo [IG Prompts] 排程推進完成！
"""
        script_path.write_text(script_content, encoding="utf-8")
        self.txt_sched_preview.delete("1.0", tk.END)
        self.txt_sched_preview.insert(tk.END, script_content)
        messagebox.showinfo("成功", f"排程腳本已生成：{script_path.resolve()}\n可直接加入 Windows 工作排程器每日定時執行！")

    def run(self) -> None:
        self.root.mainloop()


def launch_gui() -> None:
    """Launch the GUI application."""
    if not TK_AVAILABLE:
        sys.stderr.write("Error: tkinter is required to run the desktop GUI.\n")
        sys.exit(1)
    app = IGPromptsGUI()
    app.run()
