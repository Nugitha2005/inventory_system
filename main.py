
import tkinter as tk
from tkinter import messagebox, ttk
import db_helper  # Ensure this file is in the same folder

# --- COLOR PALETTE (Futuristic Theme) ---
COLOR_BG = "#0B1120"  # Deepest Navy (Background)
COLOR_CARD = "#1F2937"  # Dark Blue-Grey (Panels/Cards)
COLOR_ACCENT = "#00D4FF"  # Neon Cyan (Buttons/Highlights)
COLOR_TEXT = "#FFFFFF"  # White
COLOR_TEXT_DIM = "#9CA3AF"  # Light Grey for labels
COLOR_DANGER = "#FF007F"  # Neon Pink (Logout/Delete)
FONT_HEADER = ("Segoe UI", 32, "bold")
FONT_BODY = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory System 2077")
        self.geometry("1440x1024")
        self.configure(bg=COLOR_BG)

        # Initialize the global style for the app
        self.setup_styles()

        # Start at Login
        self.show_login()

    def setup_styles(self):
        # Configure the Treeview (Table) to look dark and modern
        style = ttk.Style()
        style.theme_use("clam")

        # Table Header
        style.configure("Treeview.Heading",
                        background=COLOR_CARD,
                        foreground=COLOR_ACCENT,
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)

        # Table Body
        style.configure("Treeview",
                        background=COLOR_BG,
                        foreground=COLOR_TEXT,
                        fieldbackground=COLOR_BG,
                        font=("Segoe UI", 12),
                        rowheight=40,
                        borderwidth=0)

        # Table Selection (When you click a row)
        style.map("Treeview", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "black")])

    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        login_frame = LoginFrame(self, self)
        login_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()
        dashboard_frame = DashboardFrame(self, self)
        dashboard_frame.pack(fill="both", expand=True)


# --- LOGIN PAGE ---
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLOR_BG)

        # 1. Background Card (Floating Dark Panel)
        # Using a border highlight to give it a "tech" feel
        card = tk.Frame(self, bg=COLOR_CARD, width=500, height=600, highlightbackground=COLOR_ACCENT,
                        highlightthickness=2)
        card.place(relx=0.5, rely=0.5, anchor="center")  # Perfectly center the card

        # 2. Login Title (Neon Effect)
        tk.Label(card, text="SYSTEM ACCESS", bg=COLOR_CARD, fg=COLOR_ACCENT, font=FONT_HEADER).place(x=0, y=50,
                                                                                                     width=500)
        tk.Label(card, text="Please authenticate", bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Segoe UI", 10)).place(x=0,
                                                                                                                  y=100,
                                                                                                                  width=500)

        # 3. Inputs
        # Username
        tk.Label(card, text="USERNAME", bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Segoe UI", 10, "bold")).place(x=50,
                                                                                                               y=180)
        self.user_entry = tk.Entry(card, font=FONT_BODY, bg="#374151", fg="white", insertbackground="white",
                                   relief="flat")
        self.user_entry.place(x=50, y=210, width=400, height=45)

        # Password
        tk.Label(card, text="PASSWORD", bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Segoe UI", 10, "bold")).place(x=50,
                                                                                                               y=280)
        self.pass_entry = tk.Entry(card, show="•", font=FONT_BODY, bg="#374151", fg="white", insertbackground="white",
                                   relief="flat")
        self.pass_entry.place(x=50, y=310, width=400, height=45)

        # 4. Login Button (Neon Cyan)
        login_btn = tk.Button(card, text="INITIALIZE SESSION", bg=COLOR_ACCENT, fg="#000000",
                              font=("Segoe UI", 14, "bold"),
                              activebackground="#FFFFFF", activeforeground=COLOR_ACCENT, relief="flat", cursor="hand2",
                              command=self.do_login)
        login_btn.place(x=50, y=450, width=400, height=55)

    def do_login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if db_helper.check_login(u, p):
            self.controller.show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials")


# --- DASHBOARD PAGE ---
class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLOR_BG)

        # --- 1. SIDEBAR (Darker Zone) ---
        sidebar = tk.Frame(self, bg=COLOR_CARD, width=280, height=1024)
        sidebar.place(x=0, y=0)

        # Logo/Brand area
        tk.Label(sidebar, text="NEXUS\nINVENTORY", bg=COLOR_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 24, "bold"),
                 justify="left").place(x=30, y=40)

        # Sidebar Buttons (Flat, Minimalist)
        self.create_sidebar_btn(sidebar, "Dashboard", 150)
        self.create_sidebar_btn(sidebar, "Inventory Stats", 220)

        # Logout Button (Red/Pink for danger)
        btn_logout = tk.Button(sidebar, text="TERMINATE SESSION", bg=COLOR_DANGER, fg="white",
                               font=("Segoe UI", 12, "bold"),
                               relief="flat", cursor="hand2", command=self.controller.show_login)
        btn_logout.place(x=30, y=900, width=220, height=50)

        # --- 2. TOP BAR ---
        # Search Bar
        search_bg = tk.Frame(self, bg=COLOR_CARD, height=60, width=400)
        search_bg.place(x=320, y=40)

        tk.Label(search_bg, text="🔍", bg=COLOR_CARD, fg=COLOR_TEXT).place(x=15, y=15)
        self.search_entry = tk.Entry(search_bg, font=FONT_BODY, bg=COLOR_CARD, fg="white", insertbackground="white",
                                     relief="flat")
        self.search_entry.place(x=50, y=10, width=330, height=40)
        # Placeholder text hack
        self.search_entry.insert(0, "Search database...")

        # Add Item Button (Futuristic Pill Shape)
        btn_add = tk.Button(self, text="+ NEW ENTRY", bg=COLOR_ACCENT, fg="black", font=("Segoe UI", 12, "bold"),
                            relief="flat", cursor="hand2", command=self.open_add_popup)
        btn_add.place(x=1200, y=40, width=180, height=60)

        # --- 3. TABLE AREA ---
        # We use a frame to hold the treeview to give it a border
        table_frame = tk.Frame(self, bg=COLOR_CARD, highlightbackground=COLOR_ACCENT, highlightthickness=1)
        table_frame.place(x=320, y=150, width=1060, height=750)

        columns = ("name", "price", "qty", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Headings
        self.tree.heading("name", text="ITEM DESIGNATION")
        self.tree.heading("price", text="UNIT COST ($)")
        self.tree.heading("qty", text="QUANTITY")
        self.tree.heading("status", text="SYSTEM STATUS")

        # Column Widths & Alignment
        self.tree.column("name", width=350, anchor="w")
        self.tree.column("price", width=150, anchor="center")
        self.tree.column("qty", width=150, anchor="center")
        self.tree.column("status", width=200, anchor="center")

        # Place Table inside the frame
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # Load Data
        self.load_data()

    def create_sidebar_btn(self, parent, text, y_pos):
        """Helper to create consistent sidebar buttons"""
        btn = tk.Button(parent, text=text, bg=COLOR_CARD, fg=COLOR_TEXT, font=("Segoe UI", 14),
                        activebackground=COLOR_BG, activeforeground=COLOR_ACCENT,
                        relief="flat", anchor="w", padx=20, cursor="hand2")
        btn.place(x=0, y=y_pos, width=280, height=60)

    def load_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            items = db_helper.fetch_all_items()
            for item in items:
                # Logic: item = (id, name, price, qty)
                qty = item[3]
                status = "ACTIVE" if qty >= 5 else "CRITICAL LOW"

                self.tree.insert("", "end", values=(item[1], item[2], item[3], status))
        except Exception as e:
            print("DB Error:", e)

    def open_add_popup(self):
        # Popup Window Logic - Themed Dark
        popup = tk.Toplevel(self)
        popup.title("New Entry")
        popup.geometry("400x500")
        popup.configure(bg=COLOR_CARD)

        tk.Label(popup, text="NEW DATABASE ENTRY", bg=COLOR_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 16, "bold")).pack(
            pady=30)

        frame = tk.Frame(popup, bg=COLOR_CARD)
        frame.pack()

        # Helper for Popup Inputs
        def create_input(label_text, r):
            tk.Label(frame, text=label_text, bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=FONT_BOLD).grid(row=r, column=0,
                                                                                                    sticky="w",
                                                                                                    pady=(10, 0))
            entry = tk.Entry(frame, font=FONT_BODY, bg="#374151", fg="white", relief="flat")
            entry.grid(row=r + 1, column=0, pady=(5, 15), ipady=5, ipadx=5)
            return entry

        entry_name = create_input("ITEM NAME", 0)
        entry_price = create_input("UNIT PRICE", 2)
        entry_qty = create_input("QUANTITY", 4)

        def save():
            if entry_name.get() and entry_price.get() and entry_qty.get():
                db_helper.insert_item(entry_name.get(), entry_price.get(), entry_qty.get())
                self.load_data()
                popup.destroy()
            else:
                messagebox.showwarning("Error", "Fill all fields")

        tk.Button(popup, text="COMMIT TO DATABASE", bg=COLOR_ACCENT, fg="black", font=("Segoe UI", 12, "bold"),
                  relief="flat", command=save).pack(pady=30, ipadx=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()