import customtkinter as ctk
import subprocess
import os
import threading
import sys
import datetime
import webbrowser
from tkinter import messagebox, filedialog

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProjectK(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Project K - Ultimate Scrcpy Tool")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Paths
        if getattr(sys, 'frozen', False):
            self.cwd = os.path.dirname(sys.executable)
        else:
            self.cwd = os.path.dirname(os.path.abspath(__file__))
            
        self.adb = os.path.join(self.cwd, "adb.exe")
        self.scrcpy = os.path.join(self.cwd, "scrcpy.exe")
        self.rec_dir = os.path.join(self.cwd, "Recordings")
        self.config_file = os.path.join(self.cwd, "config.txt")
        self.check_dependencies()

        # --- UI Layout ---
        self.create_sidebar()
        self.create_pages()
        
        # Show default
        self.show_page("Dashboard")

        # Initial Load
        self.refresh_devices()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1) # Spacer push launch button down

        # Title
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="PROJECT K", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Nav Buttons
        self.btn_dash = self.create_nav_btn("Dashboard", 1, lambda: self.show_page("Dashboard"))
        self.btn_qual = self.create_nav_btn("Quality", 2, lambda: self.show_page("Quality"))
        self.btn_audio = self.create_nav_btn("Audio", 3, lambda: self.show_page("Audio"))
        self.btn_tools = self.create_nav_btn("Tools", 4, lambda: self.show_page("Tools"))

        # Launch Button (Bottom)
        self.btn_launch = ctk.CTkButton(self.sidebar, text="🔥 LAUNCH", height=40, 
                                        fg_color="#007ACC", hover_color="#005FA3", 
                                        font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.start_mirroring)
        self.btn_launch.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        # Github Link
        self.btn_git = ctk.CTkButton(self.sidebar, text="@piyushkadam96k", height=20, fg_color="transparent", text_color="gray",
                                     hover_color="#333", command=lambda: webbrowser.open("https://github.com/piyushkadam96k"))
        self.btn_git.grid(row=7, column=0, padx=20, pady=10)

    def create_nav_btn(self, text, row, cmd):
        btn = ctk.CTkButton(self.sidebar, text=text, height=40, corner_radius=10, 
                            fg_color="transparent", text_color=("gray10", "#DCE4EE"), 
                            hover_color=("gray70", "gray30"), anchor="w", command=cmd)
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        return btn

    def create_pages(self):
        self.pages = {}
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # -- Dashboard --
        p_dash = ctk.CTkFrame(container, fg_color="transparent")
        self.pages["Dashboard"] = p_dash
        
        ctk.CTkLabel(p_dash, text="Device Dashboard", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        f_dev = ctk.CTkFrame(p_dash, corner_radius=10)
        f_dev.pack(fill="x", pady=10)
        ctk.CTkLabel(f_dev, text="Connected Devices", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=10)
        self.cb_devices = ctk.CTkComboBox(f_dev, width=250)
        self.cb_devices.pack(padx=15, pady=(0, 10), fill="x")
        
        ctk.CTkButton(p_dash, text="Refresh Devices", command=self.refresh_devices, width=150, fg_color="#333", hover_color="#444").pack(pady=5, anchor="w")
        ctk.CTkButton(p_dash, text="Kill ADB Server", command=self.kill_adb, width=150, fg_color="#C0392B", hover_color="#A93226").pack(pady=5, anchor="w")

        # -- Quality --
        p_qual = ctk.CTkFrame(container, fg_color="transparent")
        self.pages["Quality"] = p_qual
        
        ctk.CTkLabel(p_qual, text="Stream Quality", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        # Presets
        f_presets = ctk.CTkFrame(p_qual, corner_radius=10)
        f_presets.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(f_presets, text="Quick Presets", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=10)
        
        grid_presets = ctk.CTkFrame(f_presets, fg_color="transparent")
        grid_presets.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(grid_presets, text="YouTube/Stream (Stable)", fg_color="#E74C3C", hover_color="#C0392B", 
                      command=self.preset_stream).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(grid_presets, text="Gaming (Low Latency)", fg_color="#2ECC71", hover_color="#27AE60", 
                      command=self.preset_gaming).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(grid_presets, text="Low End PC", fg_color="#F39C12", hover_color="#D35400", 
                      command=self.preset_low).pack(side="left", expand=True, padx=5)

        f_perf = ctk.CTkFrame(p_qual, corner_radius=10)
        f_perf.pack(fill="x", pady=10)
        
        self.add_setting(f_perf, "Video Codec", ["H.264 (Default)", "H.265 (High Perf/Quality)", "AV1 (Newer)"], "self.cb_codec")
        
        # Advanced Encoder Selection
        f_enc = ctk.CTkFrame(f_perf, fg_color="transparent")
        f_enc.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(f_enc, text="Specific Encoder", width=100, anchor="w").pack(side="left")
        self.entry_encoder = ctk.CTkEntry(f_enc, width=200, placeholder_text="(Optional) e.g. omx.google...")
        self.entry_encoder.pack(side="right")
        
        ctk.CTkButton(f_perf, text="View Device Encoders", command=self.list_encoders, 
                      fg_color="#555", height=20, width=150).pack(pady=(0, 10))

        # Render Calibration
        f_calib = ctk.CTkFrame(f_perf, fg_color="transparent")
        f_calib.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(f_calib, text="Calibration", width=100, anchor="w").pack(side="left")
        self.chk_fps = ctk.CTkCheckBox(f_calib, text="Show FPS Log")
        self.chk_fps.pack(side="left", padx=10)
        self.chk_pacing = ctk.CTkCheckBox(f_calib, text="Disable Pacing")
        self.chk_pacing.pack(side="left", padx=10)

        self.add_setting(f_perf, "Resolution", ["Original (Max)", "1600p (High)", "1440p (2K/QHD)", "1080p (Safe/FHD)", "720p (Fast/HD)", "480p (Fastest)"], "self.cb_res", default="1080p (Safe/FHD)")
        self.add_setting(f_perf, "Bitrate", ["2 Mbps (Very Low)", "4 Mbps (Low)", "8 Mbps (Standard)", "16 Mbps (High)", "20 Mbps (Ultra)", "50 Mbps (Max)"], "self.cb_bit", default="8 Mbps (Standard)")
        self.add_setting(f_perf, "Max FPS", ["60 (Default)", "30 (Low CPU)", "90 (Smooth)", "120 (Ultra Smooth)", "Uncapped"], "self.cb_fps")
        self.add_setting(f_perf, "Render Driver", ["Default", "OpenGL (Compatibility)", "Direct3D (Windows)", "Software (Slow)"], "self.cb_driver")

        # -- Audio --
        p_audio = ctk.CTkFrame(container, fg_color="transparent")
        self.pages["Audio"] = p_audio
        
        ctk.CTkLabel(p_audio, text="Audio Settings", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        f_audio = ctk.CTkFrame(p_audio, corner_radius=10)
        f_audio.pack(fill="x", pady=10)
        
        self.add_setting(f_audio, "Audio Output", ["PC (Default, Mutes Phone)", "PC + Phone (Hear on Both)", "Phone Only (Mute PC)"], "self.cb_audio")
        self.add_setting(f_audio, "Buffering", ["No Buffer (Real-time)", "50ms (Low Latency)", "200ms (Wireless/Smooth)", "400ms (Very Smooth)"], "self.cb_buf", default="50ms (Low Latency)")

        # -- Tools --
        p_tools = ctk.CTkFrame(container, fg_color="transparent")
        self.pages["Tools"] = p_tools
        
        ctk.CTkLabel(p_tools, text="Tools & Extras", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        f_tools = ctk.CTkFrame(p_tools, corner_radius=10)
        f_tools.pack(fill="x", pady=10)
        
        self.chk_off = ctk.CTkCheckBox(f_tools, text="Turn Screen Off (On Launch)")
        self.chk_off.pack(anchor="w", padx=15, pady=10)
        self.chk_awake = ctk.CTkCheckBox(f_tools, text="Stay Awake")
        self.chk_awake.pack(anchor="w", padx=15, pady=10)
        self.chk_touch = ctk.CTkCheckBox(f_tools, text="Show Touches")
        self.chk_touch.pack(anchor="w", padx=15, pady=10)
        self.chk_top = ctk.CTkCheckBox(f_tools, text="Always On Top")
        self.chk_top.pack(anchor="w", padx=15, pady=10)
        
        f_rec = ctk.CTkFrame(p_tools, corner_radius=10)
        f_rec.pack(fill="x", pady=10)
        ctk.CTkLabel(f_rec, text="Recording", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=10)
        
        self.chk_rec = ctk.CTkCheckBox(f_rec, text="Record Screen to File")
        self.chk_rec.pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkButton(f_rec, text="Open Recordings Folder", command=self.open_recordings, fg_color="#555").pack(padx=15, pady=10, anchor="w")

        # Layout all pages
        for p in self.pages.values():
            p.grid(row=0, column=0, sticky="nsew")

    def add_setting(self, parent, label, values, attr_name, default=None):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=8)
        ctk.CTkLabel(f, text=label, width=100, anchor="w").pack(side="left")
        cb = ctk.CTkComboBox(f, values=values, width=200)
        cb.pack(side="right")
        if default: cb.set(default)
        exec(f"{attr_name} = cb") # Bind to self

    def show_page(self, name):
        # Reset buttons
        for btn in [self.btn_dash, self.btn_qual, self.btn_audio, self.btn_tools]:
            btn.configure(fg_color="transparent")
        
        # Highlight logic
        if name == "Dashboard": self.btn_dash.configure(fg_color=("#3B8ED0", "#1f538d"))
        elif name == "Quality": self.btn_qual.configure(fg_color=("#3B8ED0", "#1f538d"))
        elif name == "Audio": self.btn_audio.configure(fg_color=("#3B8ED0", "#1f538d"))
        elif name == "Tools": self.btn_tools.configure(fg_color=("#3B8ED0", "#1f538d"))
        
        self.pages[name].tkraise()

    # --- Logic Methods (Same as before) ---
    def check_dependencies(self):
        if not os.path.exists(self.adb): 
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, "r") as f:
                        saved_path = f.read().strip()
                        if os.path.exists(os.path.join(saved_path, "adb.exe")):
                            self.cwd = saved_path
                            self.adb = os.path.join(self.cwd, "adb.exe")
                            self.scrcpy = os.path.join(self.cwd, "scrcpy.exe")
                            self.rec_dir = os.path.join(self.cwd, "Recordings")
                            return
                except:
                    pass
            messagebox.showinfo("Setup", "ADB/Scrcpy not found. Please select the folder.")
            folder = filedialog.askdirectory(title="Select folder with adb.exe")
            if folder and os.path.exists(os.path.join(folder, "adb.exe")):
                self.cwd = folder
                self.adb = os.path.join(self.cwd, "adb.exe")
                self.scrcpy = os.path.join(self.cwd, "scrcpy.exe")
                self.rec_dir = os.path.join(self.cwd, "Recordings")
                with open(self.config_file, "w") as f:
                    f.write(self.cwd)
            else:
                sys.exit()

    def run_adb(self, args):
        try:
            subprocess.run([self.adb] + args.split(), creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

    def refresh_devices(self):
        try:
            result = subprocess.run([self.adb, "devices"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            devices = []
            for line in result.stdout.splitlines():
                if line.endswith("device") and not line.startswith("List"):
                    devices.append(line.split()[0])
            if devices:
                self.cb_devices.configure(values=devices)
                self.cb_devices.set(devices[0])
            else:
                self.cb_devices.configure(values=["No Devices Found"])
                self.cb_devices.set("No Devices Found")
        except:
            pass

    def kill_adb(self):
        self.run_adb("kill-server")
        self.refresh_devices()

    # --- Preset Handlers ---
    def preset_stream(self):
        # Stable 8Mbps 1080p, H.264 (best for OBS), 50ms buffer (smoothness)
        self.cb_codec.set("H.264 (Default)")
        self.cb_res.set("1080p (Safe/FHD)")
        self.cb_bit.set("8 Mbps (Standard)")
        self.cb_fps.set("60 (Default)")
        self.cb_driver.set("Direct3D (Windows)")
        self.cb_buf.set("50ms (Low Latency)")
        messagebox.showinfo("Preset Applied", "Settings optimized for YouTube Streaming (Stable 1080p).")

    def preset_gaming(self):
        # Ultra Low Latency, No Buffer, 720p 90fps (smooth feel but less detail)
        # Switched to H.264 + Direct3D for better compatibility
        self.cb_codec.set("H.264 (Default)")
        self.cb_res.set("720p (Fast/HD)")
        self.cb_bit.set("12 Mbps (High)") 
        self.cb_fps.set("90 (Smooth)")
        self.cb_driver.set("Direct3D (Windows)")
        self.cb_buf.set("No Buffer (Real-time)")
        messagebox.showinfo("Preset Applied", "Settings optimized for Gaming (Low Latency).")

    def preset_low(self):
        # Potato PC: 480p, 2Mbps, 30fps
        self.cb_codec.set("H.264 (Default)")
        self.cb_res.set("480p (Fastest)")
        self.cb_bit.set("2 Mbps (Very Low)")
        self.cb_fps.set("30 (Low CPU)")
        self.cb_driver.set("Software (Slow)")
        self.cb_buf.set("No Buffer (Real-time)")
        messagebox.showinfo("Preset Applied", "Settings optimized for Low End PC.")

    def list_encoders(self):
        try:
            cmd = [self.scrcpy, "--list-encoders"]
            device = self.cb_devices.get()
            if device and device != "No Devices Found":
                cmd.extend(["-s", device])
                
            result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Show result in a window
            top = ctk.CTkToplevel(self)
            top.title("Device Encoders")
            top.geometry("600x400")
            
            txt = ctk.CTkTextbox(top, width=580, height=380)
            txt.pack(padx=10, pady=10)
            txt.insert("1.0", result.stdout)
            txt.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_recordings(self):
        if os.path.exists(self.rec_dir):
            os.startfile(self.rec_dir)
        else:
            messagebox.showinfo("Info", "No recordings folder yet.")

    def start_mirroring(self):
        if not os.path.exists(self.scrcpy):
            messagebox.showerror("Error", "Scrcpy not found!")
            return

        cmd = [self.scrcpy]
        device = self.cb_devices.get()
        if device and device != "No Devices Found":
            cmd.extend(["-s", device])

        # Quality
        codec = self.cb_codec.get()
        if "H.265" in codec: cmd.extend(["--video-codec=h265"])
        elif "AV1" in codec: cmd.extend(["--video-codec=av1"])
        
        # Specific Encoder (Overrides Codec usually, or works with it)
        enc = self.entry_encoder.get()
        if enc.strip():
            cmd.extend(["--video-encoder", enc.strip()])

        res = self.cb_res.get()
        if "1600p" in res: cmd.append("--max-size=1600")
        elif "1440p" in res: cmd.append("--max-size=1440")
        elif "1080p" in res: cmd.append("--max-size=1080")
        elif "720p" in res: cmd.append("--max-size=720")
        elif "480p" in res: cmd.append("--max-size=480")

        bit = self.cb_bit.get()
        if "2 Mbps" in bit: cmd.append("--video-bit-rate=2M")
        elif "4 Mbps" in bit: cmd.append("--video-bit-rate=4M")
        elif "8 Mbps" in bit: cmd.append("--video-bit-rate=8M")
        elif "16 Mbps" in bit: cmd.append("--video-bit-rate=16M")
        elif "20 Mbps" in bit: cmd.append("--video-bit-rate=20M")
        elif "50 Mbps" in bit: cmd.append("--video-bit-rate=50M")

        fps = self.cb_fps.get()
        if "60" in fps: cmd.append("--max-fps=60")
        elif "30" in fps: cmd.append("--max-fps=30")
        elif "90" in fps: cmd.append("--max-fps=90")
        elif "120" in fps: cmd.append("--max-fps=120")
        
        driver = self.cb_driver.get()
        if "OpenGL" in driver: cmd.append("--render-driver=opengl")
        elif "Direct3D" in driver: cmd.append("--render-driver=direct3d")
        elif "Software" in driver: cmd.append("--render-driver=software")

        # Audio
        audio = self.cb_audio.get()
        if "Phone Only" in audio: 
            cmd.append("--no-audio")
        elif "PC + Phone" in audio: 
            cmd.append("--audio-dup")

        buf = self.cb_buf.get()
        if "No Buffer" in buf: cmd.append("--video-buffer=0")
        elif "50ms" in buf: cmd.append("--video-buffer=50")
        elif "200ms" in buf: cmd.append("--video-buffer=200")
        elif "400ms" in buf: cmd.append("--video-buffer=400")

        # Extras
        if self.chk_off.get(): cmd.append("--turn-screen-off")
        if self.chk_awake.get(): cmd.append("--stay-awake")
        if self.chk_touch.get(): cmd.append("--show-touches")
        if self.chk_top.get(): cmd.append("--always-on-top")

        # Calibration
        show_console = False
        if self.chk_fps.get(): 
            cmd.append("--print-fps")
            show_console = True
        if self.chk_pacing.get(): cmd.append("--no-video-pacing")

        # Record
        if self.chk_rec.get():
            if not os.path.exists(self.rec_dir): os.makedirs(self.rec_dir)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"scrcpy_rec_{ts}.mp4"
            file_path = filedialog.asksaveasfilename(
                title="Save Recording As...",
                initialdir=self.rec_dir,
                initialfile=default_name,
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
            )
            if not file_path: return 
            cmd.extend(["--record", file_path])

        try:
            # If measuring FPS, we need to see the console
            flags = 0 if show_console else subprocess.CREATE_NO_WINDOW
            subprocess.Popen(cmd, creationflags=flags)
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))

if __name__ == "__main__":
    app = ProjectK()
    app.mainloop()
