import random
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class HotelManagement:
    def __init__(self):
        self.file = "hotel_data.csv"
        self.df = self.load_data()
        self.rooms = {
            1: {"type": "Standard Non-AC", "price": 3500, "total": 50, "range": (101, 150)},
            2: {"type": "Standard AC", "price": 4000, "total": 50, "range": (201, 250)},
            3: {"type": "3-Bed Non-AC", "price": 4500, "total": 50, "range": (301, 350)},
            4: {"type": "3-Bed AC", "price": 5000, "total": 50, "range": (401, 450)}}
        self.food = {
            1: {"name": "Masala Dosa", "price": 130, "cat": "South Indian"},
            2: {"name": "Butter Naan", "price": 20, "cat": "Breads"},
            3: {"name": "Paneer Dosa", "price": 130, "cat": "South Indian"},
            4: {"name": "Biryani", "price": 250, "cat": "Rice"},
            5: {"name": "Dal Makhani", "price": 180, "cat": "Curry"},
            6: {"name": "Butter Chicken", "price": 320, "cat": "Non-Veg"}}
        self.needs = {
            1: {"name": "Extra Towels", "price": 50}, 2: {"name": "Extra Pillows", "price": 100},
            3: {"name": "Blanket", "price": 150}, 4: {"name": "Laundry Service", "price": 200},
            5: {"name": "Iron Box", "price": 80}, 6: {"name": "Toiletries Kit", "price": 120}}
        self.clr = {'pri': '#2C3E50', 'sec': '#34495E', 'acc': '#3498DB',
                   'ok': '#27AE60', 'err': '#E74C3C', 'warn': '#F39C12',
                   'lt': '#ECF0F1', 'wh': '#FFFFFF'}
        self.win = tk.Tk()
        self.win.title("Hotel Management System")
        self.win.geometry("1200x700")
        self.win.configure(bg=self.clr['lt'])
        self.cart = []
        self.total = 0
        self.setup()
        
    def load_data(self):
        try:
            d = pd.read_csv(self.file)
            for c in ['payment_done', 'cancelled']:
                d[c] = d[c].astype(bool) if c in d.columns else False
            if 'necessities_charges' not in d.columns:
                d['necessities_charges'] = 0
            return d
        except FileNotFoundError:
            return pd.DataFrame(columns=['name', 'phone', 'address', 'checkin', 'checkout', 
                'room_type', 'room_price', 'room_no', 'customer_id', 'stay_duration', 
                'restaurant_charges', 'necessities_charges', 'payment_done', 'cancelled'])

    def save(self):
        self.df.to_csv(self.file, index=False)

    def get_avail(self, rt):
        start, end = self.rooms[rt]["range"]
        used = set(self.df[(self.df['room_type'] == self.rooms[rt]['type']) & 
            (self.df['payment_done'] == False) & (self.df['cancelled'] == False)]['room_no'].tolist())
        return list(set(range(start, end + 1)) - used)

    def setup(self):
        # Header
        hdr = tk.Frame(self.win, bg=self.clr['pri'], height=80)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🏨 HOTEL ANCASA", font=("Arial", 24, "bold"), 
                bg=self.clr['pri'], fg=self.clr['wh']).pack(pady=20)
        
        self.main = tk.Frame(self.win, bg=self.clr['lt'])
        self.main.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        side = tk.Frame(self.main, bg=self.clr['sec'], width=250)
        side.pack(side=tk.LEFT, fill=tk.Y)
        side.pack_propagate(False)
        tk.Label(side, text="MAIN MENU", font=("Arial", 12, "bold"), 
                bg=self.clr['sec'], fg=self.clr['wh']).pack(pady=20)
        
        menus = [("Dashboard", self.dash), ("Single Booking", self.single),
            ("Group Booking", self.group), ("Room Availability", self.avail),
            ("Restaurant", self.restaurant), ("Necessities", self.necessity),
            ("Extend Booking", self.extend), ("Cancel Booking", self.cancel),
            ("Payment", self.pay), ("All Records", lambda: self.records('all')),
            ("Active", lambda: self.records('active')), ("Completed", lambda: self.records('done')),
            ("Exit", self.exit)]
        
        for txt, cmd in menus:
            tk.Button(side, text=txt, command=cmd, width=22, bg=self.clr['acc'], 
                     fg=self.clr['wh'], font=("Arial", 10), relief=tk.FLAT, 
                     cursor="hand2", activebackground=self.clr['pri']).pack(pady=5, padx=10)
        
        self.cont = tk.Frame(self.main, bg=self.clr['wh'])
        self.cont.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.dash()

    def clear(self):
        for w in self.cont.winfo_children():
            w.destroy()

    def msg(self, txt):
        self.stat.config(text=f"Status: {txt}")
        self.win.after(3000, lambda: self.stat.config(text="Ready"))

    def lframes(self, par, txt):
        return tk.LabelFrame(par, text=txt, font=("Arial", 12, "bold"),
                            bg=self.clr['wh'], fg=self.clr['pri'])

    def dash(self):
        self.clear()
        tk.Label(self.cont, text="Dashboard Overview", font=("Arial", 20, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        sf = tk.Frame(self.cont, bg=self.clr['wh'])
        sf.pack(fill=tk.X, pady=20)
        
        act = len(self.df[(self.df['payment_done'] == False) & (self.df['cancelled'] == False)])
        done = len(self.df[self.df['payment_done'] == True])
        canc = len(self.df[self.df['cancelled'] == True])
        rev = sum(self.df[self.df['payment_done'] == True].apply(
             lambda x: x['room_price'] * x['stay_duration'] + x['restaurant_charges'] + x['necessities_charges'], axis=1))
        
        for i, (t, v, c) in enumerate([("Active Bookings", act, self.clr['ok']),
            ("Completed", done, self.clr['acc']), ("Cancelled", canc, self.clr['err']),
            ("Revenue (Rs.)", rev, self.clr['warn'])]):
            cd = tk.Frame(sf, bg=c, relief=tk.RAISED, bd=2)
            cd.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            tk.Label(cd, text=t, font=("Arial", 12), bg=c, fg=self.clr['wh']).pack(pady=10)
            tk.Label(cd, text=str(v), font=("Arial", 24, "bold"), bg=c, fg=self.clr['wh']).pack(pady=10)
        
        of = self.lframes(self.cont, "Room Occupancy")
        of.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        for rt, info in self.rooms.items():
            av = len(self.get_avail(rt))
            occ = info['total'] - av
            pct = (occ / info['total']) * 100
            
            r = tk.Frame(of, bg=self.clr['wh'])
            r.pack(fill=tk.X, pady=5, padx=10)
            tk.Label(r, text=info['type'], font=("Arial", 10), bg=self.clr['wh'], 
                    width=20, anchor='w').pack(side=tk.LEFT)
            
            pb = tk.Frame(r, bg=self.clr['lt'], height=25, width=300)
            pb.pack(side=tk.LEFT, padx=10)
            pb.pack_propagate(False)
            fc = self.clr['ok'] if pct < 70 else self.clr['warn'] if pct < 90 else self.clr['err']
            tk.Frame(pb, bg=fc, width=int(300 * (occ / info['total']))).pack(side=tk.LEFT, fill=tk.Y)
            tk.Label(r, text=f"{occ}/{info['total']} ({pct:.1f}%)", 
                    font=("Arial", 10), bg=self.clr['wh']).pack(side=tk.LEFT)

    def booking(self, title, grp=False):
        self.clear()
        tk.Label(self.cont, text=title, font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        canv = tk.Canvas(self.cont, bg=self.clr['wh'])
        sb = ttk.Scrollbar(self.cont, orient="vertical", command=canv.yview)
        frm = tk.Frame(canv, bg=self.clr['wh'])
        frm.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv.create_window((0, 0), window=frm, anchor="nw")
        canv.configure(yscrollcommand=sb.set)
        
        fm = self.lframes(frm, "Booking Details")
        fm.pack(pady=20, padx=40, fill=tk.BOTH)
        
        inp = tk.Frame(fm, bg=self.clr['wh'])
        inp.pack(pady=10, padx=20, fill=tk.X)
        
        ent = {}
        fld = [("Name", "nm"), ("Phone", "ph"), ("Address", "addr")]
        if grp:
            fld = [("Group Name", "grp"), ("Contact Person", "cnt")] + fld[1:]
        
        for i, (lbl, key) in enumerate(fld):
            tk.Label(inp, text=f"{lbl}:", font=("Arial", 10, "bold"), bg=self.clr['wh']).grid(row=i, column=0, sticky=tk.W, pady=5)
            ent[key] = tk.Entry(inp, width=40, font=("Arial", 10))
            ent[key].grid(row=i, column=1, pady=5, padx=10)
        
        off = len(fld)
        tk.Label(inp, text="Check-In (dd/mm/yyyy):", font=("Arial", 10, "bold"), bg=self.clr['wh']).grid(row=off, column=0, sticky=tk.W, pady=5)
        cin = tk.Entry(inp, width=40, font=("Arial", 10))
        cin.grid(row=off, column=1, pady=5, padx=10)
        cin.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        tk.Label(inp, text="Check-Out (dd/mm/yyyy):", font=("Arial", 10, "bold"), bg=self.clr['wh']).grid(row=off+1, column=0, sticky=tk.W, pady=5)
        cout = tk.Entry(inp, width=40, font=("Arial", 10))
        cout.grid(row=off+1, column=1, pady=5, padx=10)
        
        dur = tk.Label(inp, text="Duration: 0 days", font=("Arial", 10), bg=self.clr['wh'], fg=self.clr['acc'])
        dur.grid(row=off+2, column=1, pady=5)
        
        if grp:
            tk.Label(inp, text="Rooms:", font=("Arial", 10, "bold"), bg=self.clr['wh']).grid(row=off+3, column=0, sticky=tk.W, pady=5)
            rms = tk.Spinbox(inp, from_=1, to=20, width=38, font=("Arial", 10))
            rms.grid(row=off+3, column=1, pady=5, padx=10)
        
        rf = tk.Frame(fm, bg=self.clr['wh'])
        rf.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(rf, text="Room Type:", font=("Arial", 12, "bold"), bg=self.clr['wh']).pack(pady=10)
        
        rv = tk.IntVar(value=1)
        for rt, info in self.rooms.items():
            av = len(self.get_avail(rt))
            cd = tk.Frame(rf, bg=self.clr['lt'], relief=tk.RAISED, bd=1)
            cd.pack(fill=tk.X, pady=5, padx=10)
            tk.Radiobutton(cd, text=f"{info['type']} - Rs.{info['price']}/day", variable=rv, 
                          value=rt, font=("Arial", 10), bg=self.clr['lt']).pack(side=tk.LEFT, padx=10)
            tk.Label(cd, text=f"Available: {av}", font=("Arial", 10), bg=self.clr['lt'], 
                    fg=self.clr['ok'] if av > 10 else self.clr['warn']).pack(side=tk.RIGHT, padx=10)
        
        pr = tk.Label(fm, text="Estimated Total: Rs. 0", font=("Arial", 14, "bold"), 
                     bg=self.clr['acc'], fg=self.clr['wh'])
        pr.pack(pady=15)
        
        def upd(*a):
            try:
                d1 = datetime.strptime(cin.get(), '%d/%m/%Y')
                d2 = datetime.strptime(cout.get(), '%d/%m/%Y')
                days = (d2 - d1).days
                if days > 0:
                    dur.config(text=f"Duration: {days} days")
                    p = self.rooms[rv.get()]['price'] * days
                    if grp:
                        p *= int(rms.get())
                    pr.config(text=f"Estimated Total: Rs. {p}")
                else:
                    dur.config(text="Duration: Invalid")
            except:
                dur.config(text="Duration: Invalid date")
        
        rv.trace('w', upd)
        cin.bind('<KeyRelease>', upd)
        cout.bind('<KeyRelease>', upd)
        
        def sub():
            try:
            # Validate required fields
                if grp:
                    # Group booking validation
                    group_name = ent['grp'].get().strip()
                    contact_person = ent['cnt'].get().strip()
                    address = ent['addr'].get().strip()

                    if not group_name:
                        messagebox.showerror("Error", "Group Name cannot be empty!")
                        ent['grp'].focus_set()
                        return
                    if not contact_person:
                        messagebox.showerror("Error", "Contact Person cannot be empty!")
                        ent['cnt'].focus_set()
                        return
                    if not address:
                        messagebox.showerror("Error", "Address cannot be empty!")
                        ent['addr'].focus_set()
                        return

                    nm = f"{group_name}-{contact_person}"
                else:
                    # Single booking validation
                    name = ent['nm'].get().strip()
                    address = ent['addr'].get().strip()

                    if not name:
                        messagebox.showerror("Error", "Name cannot be empty!")
                        ent['nm'].focus_set()
                        return
                    if not address:
                        messagebox.showerror("Error", "Address cannot be empty!")
                        ent['addr'].focus_set()
                        return

                    nm = name

                phone = ent['ph'].get().strip()

                if not (phone.isdigit() and len(phone) == 10):
                    messagebox.showerror("Error", "Phone number must be 10 digits!")
                    ent['ph'].focus_set()
                    return

                d1 = datetime.strptime(cin.get(), '%d/%m/%Y')
                d2 = datetime.strptime(cout.get(), '%d/%m/%Y')
                if d2 <= d1:
                    messagebox.showerror("Error", "Check-out date must be after check-in date!")
                    cout.focus_set()
                    return
            # Rest of the existing booking code remains the same...
                if grp:
                    nr = int(rms.get())
                    bkd = []
                    for _ in range(nr):
                        av = self.get_avail(rv.get())
                        if not av: break
                        ri = self.rooms[rv.get()]
                        bk = {
                            'name': nm, 'phone': ent['ph'].get(), 'address': ent['addr'].get(),
                            'checkin': d1.strftime('%d/%m/%Y'), 'checkout': d2.strftime('%d/%m/%Y'),
                            'room_type': ri['type'], 'room_price': ri['price'],
                            'room_no': random.choice(av),
                            'customer_id': random.randint(1000, 9999) if self.df.empty else int(max(self.df['customer_id'])) + 1,
                            'stay_duration': (d2 - d1).days, 'restaurant_charges': 0,
                            'necessities_charges': 0, 'payment_done': False, 'cancelled': False
                        }
                        self.df = pd.concat([self.df, pd.DataFrame([bk])], ignore_index=True)
                        bkd.append(f"Room {bk['room_no']} (ID: {bk['customer_id']})")
                    self.save()
                    messagebox.showinfo("Success", f"{len(bkd)} rooms booked!\n" + "\n".join(bkd))
                else:
                    av = self.get_avail(rv.get())
                    if not av:
                        messagebox.showerror("Error", "No rooms available!")
                        return
                    ri = self.rooms[rv.get()]
                    bk = {
                        'name': nm, 'phone': ent['ph'].get(), 'address': ent['addr'].get(),
                        'checkin': d1.strftime('%d/%m/%Y'), 'checkout': d2.strftime('%d/%m/%Y'),
                        'room_type': ri['type'], 'room_price': ri['price'],
                        'room_no': random.choice(av),
                        'customer_id': random.randint(1000, 9999) if self.df.empty else int(max(self.df['customer_id'])) + 1,
                        'stay_duration': (d2 - d1).days, 'restaurant_charges': 0,
                        'necessities_charges': 0, 'payment_done': False, 'cancelled': False
                    }
                    self.df = pd.concat([self.df, pd.DataFrame([bk])], ignore_index=True)
                    self.save()
                    messagebox.showinfo("Success", f"Booking successful!\nID: {bk['customer_id']}\nRoom: {bk['room_no']}")

                self.msg("Booking completed!")
                self.dash()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        bf = tk.Frame(fm, bg=self.clr['wh'])
        bf.pack(pady=20)
        tk.Button(bf, text="✓ Confirm", command=sub, bg=self.clr['ok'], 
                 fg=self.clr['wh'], font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(bf, text="✗ Cancel", command=self.dash, bg=self.clr['err'], 
                 fg=self.clr['wh'], font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
        
        canv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def single(self):
        self.booking("Single Room Booking", False)

    def group(self):
        self.booking("Group Booking", True)

    def avail(self):
        self.clear()
        tk.Label(self.cont, text="Room Availability", font=("Arial", 20, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        # Scrollable container
        canvas = tk.Canvas(self.cont, bg=self.clr['wh'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.cont, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=self.clr['wh'])

        frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Room cards
        for rt, info in self.rooms.items():
            av = len(self.get_avail(rt))
            occ = info['total'] - av
            pct = int((occ / info['total']) * 100)

            card = tk.Frame(frame, bg=self.clr['lt'], bd=2, relief=tk.GROOVE)
            card.pack(fill=tk.X, padx=20, pady=12)

        # Header
            tk.Label(card, text=info['type'], font=("Arial", 15, "bold"),
                bg=self.clr['acc'], fg=self.clr['wh']).pack(fill=tk.X)

            body = tk.Frame(card, bg=self.clr['lt'])
            body.pack(padx=10, pady=10, fill=tk.X)

        # Left information
            left = tk.Frame(body, bg=self.clr['lt'])
            left.pack(side=tk.LEFT, anchor='w')

            for lbl, val, col in [
                ("Total Rooms", info['total'], "black"),
                ("Available", av, self.clr['ok']),
                ("Occupied", occ, self.clr['err'])]:
                tk.Label(left, text=f"{lbl}: {val}", font=("Arial", 11),
                        bg=self.clr['lt'], fg=col).pack(anchor="w")

        # Right — percentage donut
            cv = tk.Canvas(body, width=110, height=110, bg=self.clr['lt'], highlightthickness=0)
            cv.pack(side=tk.RIGHT, padx=10)

        # Outer circle background
            cv.create_oval(10, 10, 100, 100, fill=self.clr['wh'], outline="")

        # Occupied portion
            cv.create_arc(10, 10, 100, 100, start=90,extent=360 * (occ / info['total']),fill=self.clr['err'], outline="")

        # Percentage text
            cv.create_text(55, 55, text=f"{pct}%", font=("Arial", 16, "bold"))

        tk.Label(card, text=f"Price: Rs.{info['price']}/day",
                 font=("Arial", 11, "bold"), bg=self.clr['lt'],
                 fg=self.clr['pri']).pack(pady=5)

    def restaurant(self):
        self.clear()
        self.cart = []
        self.total = 0
        tk.Label(self.cont, text="Restaurant Service", font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        mn = tk.Frame(self.cont, bg=self.clr['wh'])
        mn.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tp = tk.Frame(mn, bg=self.clr['wh'])
        tp.pack(fill=tk.X, pady=10)
        tk.Label(tp, text="Customer ID:", font=("Arial", 11, "bold"), bg=self.clr['wh']).pack(side=tk.LEFT, padx=5)
        ce = tk.Entry(tp, width=15, font=("Arial", 11))
        ce.pack(side=tk.LEFT, padx=5)
        il = tk.Label(tp, text="", font=("Arial", 10), bg=self.clr['wh'], fg=self.clr['acc'])
        il.pack(side=tk.LEFT, padx=20)
        
        def chk():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if ix and not self.df.iloc[ix[0]]['payment_done'] and not self.df.iloc[ix[0]]['cancelled']:
                    il.config(text=f"✓ {self.df.iloc[ix[0]]['name']} - Room {self.df.iloc[ix[0]]['room_no']}")
                    return True
                il.config(text="✗ Invalid/Completed")
                return False
            except:
                il.config(text="✗ Not found")
                return False
        
        tk.Button(tp, text="Verify", command=chk, bg=self.clr['acc'], 
                 fg=self.clr['wh'], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        ct = tk.Frame(mn, bg=self.clr['wh'])
        ct.pack(fill=tk.BOTH, expand=True, pady=10)
        
        mf = self.lframes(ct, "Menu")
        mf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        cats = {}
        for cod, itm in self.food.items():
            c = itm['cat']
            if c not in cats:
                cats[c] = []
            cats[c].append((cod, itm))
        
        for ca, its in cats.items():
            tk.Label(mf, text=ca, font=("Arial", 11, "bold"), bg=self.clr['wh']).pack(anchor='w', pady=5, padx=10)
            for cod, itm in its:
                fr = tk.Frame(mf, bg=self.clr['lt'], relief=tk.RAISED, bd=1)
                fr.pack(fill=tk.X, pady=2, padx=10)
                tk.Label(fr, text=itm['name'], font=("Arial", 10), bg=self.clr['lt']).pack(side=tk.LEFT, padx=10, pady=5)
                tk.Label(fr, text=f"Rs.{itm['price']}", font=("Arial", 10, "bold"), 
                        bg=self.clr['lt'], fg=self.clr['acc']).pack(side=tk.RIGHT, padx=10)
                tk.Button(fr, text="+ Add", command=lambda c=cod, i=itm: (self.cart.append((c, i)), 
                         setattr(self, 'total', self.total + i['price']), upd_cart()),
                         bg=self.clr['ok'], fg=self.clr['wh'], font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)
        
        cf = self.lframes(ct, "Cart")
        cf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        cl = tk.Listbox(cf, font=("Arial", 10), height=15)
        cl.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tl = tk.Label(cf, text="Total: Rs. 0", font=("Arial", 14, "bold"),
                     bg=self.clr['wh'], fg=self.clr['acc'])
        tl.pack(pady=10)
        
        def upd_cart():
            cl.delete(0, tk.END)
            for _, itm in self.cart:
                cl.insert(tk.END, f"{itm['name']} - Rs.{itm['price']}")
            tl.config(text=f"Total: Rs. {self.total}")
        
        def ord():
            if not chk() or not self.cart:
                messagebox.showerror("Error", "Verify customer and add items!")
                return
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()[0]
                self.df.at[ix, 'restaurant_charges'] += self.total
                self.save()
                messagebox.showinfo("Success", f"Order placed! Total: Rs.{self.total}")
                self.cart, self.total = [], 0
                upd_cart()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        bf = tk.Frame(cf, bg=self.clr['wh'])
        bf.pack(pady=10)
        tk.Button(bf, text="Place Order", command=ord, bg=self.clr['ok'], 
                 fg=self.clr['wh'], font=("Arial", 11, "bold"), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Clear", command=lambda: (setattr(self, 'cart', []), 
                 setattr(self, 'total', 0), upd_cart()), bg=self.clr['err'], 
                 fg=self.clr['wh'], font=("Arial", 11, "bold"), width=12).pack(side=tk.LEFT, padx=5)

    def necessity(self):
        self.clear()
        tk.Label(self.cont, text="Necessities Service", font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        fm = self.lframes(self.cont, "Request Items")
        fm.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        tp = tk.Frame(fm, bg=self.clr['wh'])
        tp.pack(pady=10, padx=20)
        tk.Label(tp, text="Customer ID:", font=("Arial", 11, "bold"), bg=self.clr['wh']).pack(side=tk.LEFT, padx=5)
        ce = tk.Entry(tp, width=15, font=("Arial", 11))
        ce.pack(side=tk.LEFT, padx=5)
        
        itf = tk.Frame(fm, bg=self.clr['wh'])
        itf.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        sel = {}
        for i, (cod, itm) in enumerate(self.needs.items()):
            cd = tk.Frame(itf, bg=self.clr['lt'], relief=tk.RAISED, bd=2)
            cd.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            vr = tk.BooleanVar()
            sel[cod] = (vr, itm)
            tk.Checkbutton(cd, text=itm['name'], variable=vr, font=("Arial", 11, "bold"), 
                          bg=self.clr['lt']).pack(pady=10, padx=10)
            tk.Label(cd, text=f"Rs.{itm['price']}", font=("Arial", 10), bg=self.clr['lt'], 
                    fg=self.clr['acc']).pack(pady=5)
        
        for i in range(3):
            itf.columnconfigure(i, weight=1)
        
        def sub():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if not ix or self.df.iloc[ix[0]]['payment_done'] or self.df.iloc[ix[0]]['cancelled']:
                    messagebox.showerror("Error", "Invalid customer!")
                    return
                tot = sum(itm['price'] for vr, itm in sel.values() if vr.get())
                if tot > 0:
                    self.df.at[ix[0], 'necessities_charges'] += tot
                    self.save()
                    messagebox.showinfo("Success", f"Request placed! Total: Rs.{tot}")
                    self.dash()
                else:
                    messagebox.showwarning("Warning", "No items selected!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(fm, text="Submit", command=sub, bg=self.clr['ok'], 
                 fg=self.clr['wh'], font=("Arial", 12, "bold"), width=20).pack(pady=20)

    def extend(self):
        self.clear()
        tk.Label(self.cont, text="Extend Booking", font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        fm = self.lframes(self.cont, "Extension")
        fm.pack(pady=20, padx=40, fill=tk.BOTH)
        
        inp = tk.Frame(fm, bg=self.clr['wh'])
        inp.pack(pady=20, padx=20)
        
        tk.Label(inp, text="Customer ID:", font=("Arial", 11, "bold"), bg=self.clr['wh']).grid(row=0, column=0, sticky=tk.W, pady=10)
        ce = tk.Entry(inp, width=20, font=("Arial", 11))
        ce.grid(row=0, column=1, pady=10, padx=10)
        
        it = scrolledtext.ScrolledText(fm, height=8, width=60, font=("Arial", 10))
        it.pack(pady=10, padx=20)
        it.config(state=tk.DISABLED)
        
        tk.Label(inp, text="New Check-Out (dd/mm/yyyy):", font=("Arial", 11, "bold"), bg=self.clr['wh']).grid(row=1, column=0, sticky=tk.W, pady=10)
        nde = tk.Entry(inp, width=20, font=("Arial", 11))
        nde.grid(row=1, column=1, pady=10, padx=10)
        
        def ld():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if ix:
                    c = self.df.iloc[ix[0]]
                    it.config(state=tk.NORMAL)
                    it.delete(1.0, tk.END)
                    if c['payment_done'] or c['cancelled']:
                        it.insert(tk.END, "Cannot extend - completed/cancelled!\n")
                    it.insert(tk.END, f"Customer: {c['name']}\nRoom: {c['room_no']}\nCurrent: {c['checkin']} to {c['checkout']}\nDuration: {c['stay_duration']} days\n")
                    it.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(inp, text="Load", command=ld, bg=self.clr['acc'], 
                 fg=self.clr['wh'], font=("Arial", 10)).grid(row=0, column=2, padx=10)
        
        def sub():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if not ix:
                    messagebox.showerror("Error", "Customer not found!")
                    return
                c = self.df.iloc[ix[0]]
                if c['payment_done'] or c['cancelled']:
                    messagebox.showerror("Error", "Cannot extend!")
                    return
                nd = datetime.strptime(nde.get(), '%d/%m/%Y')
                cur = datetime.strptime(c['checkout'], '%d/%m/%Y')
                if nd <= cur:
                    messagebox.showerror("Error", "New date must be after current!")
                    return
                ndr = (nd - datetime.strptime(c['checkin'], '%d/%m/%Y')).days
                if messagebox.askyesno("Confirm", f"Extend by {ndr - c['stay_duration']} days?"):
                    self.df.at[ix[0], 'checkout'] = nd.strftime('%d/%m/%Y')
                    self.df.at[ix[0], 'stay_duration'] = ndr
                    self.save()
                    messagebox.showinfo("Success", "Extended!")
                    self.dash()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(fm, text="Extend", command=sub, bg=self.clr['ok'], 
                 fg=self.clr['wh'], font=("Arial", 12, "bold"), width=20).pack(pady=20)

    def cancel(self):
        self.clear()
        tk.Label(self.cont, text="Cancel Booking", font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        fm = self.lframes(self.cont, "Cancellation")
        fm.pack(pady=20, padx=40, fill=tk.BOTH)
        
        inp = tk.Frame(fm, bg=self.clr['wh'])
        inp.pack(pady=20, padx=20)
        tk.Label(inp, text="Customer ID:", font=("Arial", 11, "bold"), bg=self.clr['wh']).grid(row=0, column=0, sticky=tk.W, pady=10)
        ce = tk.Entry(inp, width=20, font=("Arial", 11))
        ce.grid(row=0, column=1, pady=10, padx=10)
        
        it = scrolledtext.ScrolledText(fm, height=10, width=60, font=("Arial", 10))
        it.pack(pady=10, padx=20)
        it.config(state=tk.DISABLED)
        
        def ld():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if ix:
                    c = self.df.iloc[ix[0]]
                    it.config(state=tk.NORMAL)
                    it.delete(1.0, tk.END)
                    if c['payment_done']:
                        it.insert(tk.END, "⚠️ Cannot cancel - payment completed!\n\n")
                    elif c['cancelled']:
                        it.insert(tk.END, "⚠️ Already cancelled!\n\n")
                    it.insert(tk.END, f"Customer: {c['name']}\nPhone: {c['phone']}\nRoom: {c['room_no']}\n{c['checkin']} to {c['checkout']}\n")
                    it.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(inp, text="Load", command=ld, bg=self.clr['acc'], 
                 fg=self.clr['wh'], font=("Arial", 10)).grid(row=0, column=2, padx=10)
        
        def sub():
            try:
                ix = self.df.index[self.df['customer_id'] == int(ce.get())].tolist()
                if not ix or self.df.iloc[ix[0]]['payment_done'] or self.df.iloc[ix[0]]['cancelled']:
                    messagebox.showerror("Error", "Cannot cancel!")
                    return
                if messagebox.askyesno("Confirm", "Cancel this booking?"):
                    self.df.at[ix[0], 'cancelled'] = True
                    self.save()
                    messagebox.showinfo("Success", "Cancelled!")
                    self.dash()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(fm, text="Cancel Booking", command=sub, bg=self.clr['err'], 
                 fg=self.clr['wh'], font=("Arial", 12, "bold"), width=20).pack(pady=20)

    def pay(self):
        self.clear()
        tk.Label(self.cont, text="Payment & Checkout", font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
    
        # Search options frame
        search_frame = tk.Frame(self.cont, bg=self.clr['wh'])
        search_frame.pack(pady=20)


        tk.Label(search_frame, text="Customer ID:", font=("Arial", 12, "bold"), 
                bg=self.clr['wh']).grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        cust_id_entry = tk.Entry(search_frame, width=20, font=("Arial", 12))
        cust_id_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(search_frame, text="OR", font=("Arial", 10),bg=self.clr['wh']).grid(row=1, column=0, columnspan=2, pady=5)
    
        tk.Label(search_frame, text="Phone Number:", font=("Arial", 12, "bold"), 
            bg=self.clr['wh']).grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        phone_entry = tk.Entry(search_frame, width=20, font=("Arial", 12))
        phone_entry.grid(row=2, column=1, pady=10, padx=10)
    
        pay_frame = tk.Frame(self.cont, bg=self.clr['wh'])
        pay_frame.pack(pady=20)
    
        tk.Label(pay_frame, text="Payment Method:", font=("Arial", 12, "bold"), 
                bg=self.clr['wh']).pack(pady=10)
    
        pay_var = tk.StringVar(value="card")
    
        methods_frame = tk.Frame(pay_frame, bg=self.clr['wh'])
        methods_frame.pack(pady=10)
    
        for text, value in [("💳 Card", "card"), ("📱 UPI", "upi"), ("💵 Cash", "cash")]:
            tk.Radiobutton(methods_frame, text=text, variable=pay_var, value=value,font=("Arial", 11), bg=self.clr['wh']).pack(side=tk.LEFT, padx=20)

        def process_payment():
            try:
                customer_id = cust_id_entry.get().strip()
                phone = phone_entry.get().strip()

                if not customer_id and not phone:
                    messagebox.showerror("Error", "Please enter either Customer ID or Phone Number!")
                    return

                
                if customer_id:
                    customer_id = int(customer_id)
                    customer_data = self.df[self.df['customer_id'] == customer_id]
                else:
                    customer_data = self.df[self.df['phone'] == phone]

                if customer_data.empty:
                    messagebox.showerror("Error", "Customer not found!")
                    return

                customer = customer_data.iloc[0]

                
                if customer['payment_done']:
                    messagebox.showerror("Error", "Payment already completed!")
                    return

                if customer['cancelled']:
                    messagebox.showerror("Error", "Booking is cancelled!")
                    return

                # Calculate total
                room_total = customer['room_price'] * customer['stay_duration']
                total_amount = room_total + customer['restaurant_charges'] + customer['necessities_charges']

                # Confirm payment
                payment_method = pay_var.get()
                method_names = {'card': 'Card', 'upi': 'UPI', 'cash': 'Cash'}

                if messagebox.askyesno("Confirm Payment", 
                                    f"Customer: {customer['name']}\n"
                                    f"Room: {customer['room_no']}\n"
                                    f"Total Amount: Rs. {total_amount}\n"
                                    f"Payment Method: {method_names[payment_method]}\n\n"
                                    f"Process payment?"):

                    # Update payment status
                    index = customer_data.index[0]
                    self.df.at[index, 'payment_done'] = True
                    self.save()

                    messagebox.showinfo("Success", "Payment completed successfully!")
                    self.dash()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Customer ID!")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        pay_btn = tk.Button(self.cont, text="💳 Complete Payment", command=process_payment,
                           bg=self.clr['ok'], fg=self.clr['wh'], font=("Arial", 14, "bold"),
                           width=20, height=2)
        pay_btn.pack(pady=30)

    def calculate_total(self, index):
        c = self.df.iloc[index]
        rc = c['room_price'] * c['stay_duration']
        return rc + c['restaurant_charges'] + c['necessities_charges']
    
    def records(self, flt):
        self.clear()
        ttl = {'all': 'All Bookings', 'active': 'Active Bookings', 'done': 'Completed Bookings'}
        tk.Label(self.cont, text=ttl[flt], font=("Arial", 18, "bold"),
                bg=self.clr['wh'], fg=self.clr['pri']).pack(pady=10)
        
        d = self.df
        if flt == 'active':
            d = self.df[(self.df['payment_done'] == False) & (self.df['cancelled'] == False)]
        elif flt == 'done':
            d = self.df[self.df['payment_done'] == True]
        
        if d.empty:
            tk.Label(self.cont, text="No records!", font=("Arial", 14), bg=self.clr['wh']).pack(pady=50)
            return
        
        st = tk.Frame(self.cont, bg=self.clr['lt'])
        st.pack(fill=tk.X, pady=10, padx=20)
        tk.Label(st, text=f"Total: {len(d)}", font=("Arial", 11, "bold"), bg=self.clr['lt']).pack(side=tk.LEFT, padx=20, pady=5)
        
        sf = tk.Frame(self.cont, bg=self.clr['wh'])
        sf.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(sf, text="Search:", font=("Arial", 10), bg=self.clr['wh']).pack(side=tk.LEFT, padx=5)
        se = tk.Entry(sf, width=30, font=("Arial", 10))
        se.pack(side=tk.LEFT, padx=5)
        
        tf = tk.Frame(self.cont)
        tf.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ts = ttk.Scrollbar(tf, orient=tk.VERTICAL)
        cols = ('ID', 'Name', 'Phone', 'Room', 'Type', 'Check-In', 'Check-Out', 'Days', 'Total', 'Status')
        tr = ttk.Treeview(tf, columns=cols, show='headings', yscrollcommand=ts.set)
        ts.config(command=tr.yview)
        
        for col in cols:
            tr.heading(col, text=col)
            tr.column(col, width=80 if col in ['ID', 'Room', 'Days'] else 100)
        
        tr.tag_configure('odd', background=self.clr['wh'])
        tr.tag_configure('even', background=self.clr['lt'])
        
        def pop(s=""):
            tr.delete(*tr.get_children())
            for i, (_, b) in enumerate(d.iterrows()):
                if s and s.lower() not in str(b['customer_id']).lower() and s.lower() not in b['name'].lower() and s.lower() not in b['phone'].lower():
                    continue
                sts = "CANCELLED" if b['cancelled'] else ("COMPLETED" if b['payment_done'] else "ACTIVE")
                tot = b['room_price'] * b['stay_duration'] + b['restaurant_charges'] + b['necessities_charges']
                tr.insert('', tk.END, values=(b['customer_id'], b['name'][:20], b['phone'], b['room_no'],
                    b['room_type'][:18], b['checkin'], b['checkout'], b['stay_duration'], tot, sts),
                    tags=('even' if i % 2 == 0 else 'odd',))
        
        se.bind('<KeyRelease>', lambda e: pop(se.get()))
        pop()
        
        ts.pack(side=tk.RIGHT, fill=tk.Y)
        tr.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(self.cont, text="📥 Export CSV", 
                 command=lambda: d.to_csv(f"records_{flt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False) or messagebox.showinfo("Success", "Exported!"),
                 bg=self.clr['acc'], fg=self.clr['wh'], font=("Arial", 10)).pack(pady=10)

    def exit(self):
        if messagebox.askyesno("Exit", "Exit application?"):
            self.win.quit()

    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
    HotelManagement().run()