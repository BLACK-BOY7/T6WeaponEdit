import json
import webbrowser
import customtkinter
import db_functions_2 as db


associar = False


with open( db.resource_path("file\\weapon_list.json") ) as file:
    weapon_list_json = json.load( file )


def open_discord():
    webbrowser.open_new( "https://discord.gg/ZSXEVB9h8C" )


def EnterPress(event):
    if event.keysym.isdigit() or event.keysym in [ "Tab", "Shift_L", "Shift_R", "BackSpace", "Delete", "Up", "Down", "Left", "Right", "0" ]:
        for x in ["n","u","l"]:
            if x in event.widget.get() and event.keysym != "BackSpace":
                event.widget.bell()
                return "break"

        if event.widget.index("insert") <= 0 and event.keysym == "0":
            event.widget.bell()
            return "break"

        if event.keysym == "Up":
            event.widget.icursor(0)

        elif event.keysym == "Down":
            event.widget.icursor("end")

        return
    else:
        event.widget.bell()
        return "break"


def StringVar(string):
    return customtkinter.StringVar(value=string)
        

def has_upgraded_support(weapon):
    return weapon in weapon_list_json["support an upgrade"]


def can_upgraded_weapon(weapon):
    return has_upgraded_support(weapon) and weapon in weapon_list_json["support an attachment"]


def common_data(self):
    return {
        "class": self.WeaponClass.get(),
        "name_string": self.WeaponName.get(),
        "name_id": weapon_list_json["all"][self.WeaponClass.get()][self.WeaponName.get()],
        "alias": self.Weapon["alias"].get().strip(),
        "cost": self.Weapon["cost"].get().strip(),
        "cost_up": self.Weapon["cost_up"].get().strip(),
        "cost_re_up": self.Weapon["cost_re_up"].get().strip(),
        "limit": self.Weapon["limit"].get().strip(),
        "round": self.Weapon["round"].get().strip(),
        "kills": self.Weapon["kills"].get().strip(),
        "hs": self.Weapon["hs"].get().strip()
    }


def add(self):
    weapon = common_data(self)
    db.add_weapon_database(weapon["class"], weapon["name_id"], weapon["name_string"], weapon["alias"], weapon["cost"], weapon["cost_up"],
                            weapon["cost_re_up"], weapon["limit"], weapon["round"], weapon["kills"], weapon["hs"])


def upgraded(self):
    weapon = common_data(self)
    db.update_data_from_database(weapon["name_id"], weapon["alias"], weapon["cost"],weapon["cost_up"], weapon["cost_re_up"],
                                    weapon["limit"], weapon["round"], weapon["kills"], weapon["hs"])


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.main_window()


    def main_window(self):
        self.title("T6WeaponS")
        self.iconbitmap(db.resource_path("file\\T6WeapEd.ico"))
        x_screen = self.winfo_screenmmheight()
        y_screen = self.winfo_screenmmwidth()

        self.minsize(width=800, height=500)
        self.geometry( f"800x500+{ int( x_screen/0.3 - 800/2 ) }+{ int( y_screen/1 - 500/2 ) }" )

        self.frames()


    def frames(self):
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.pack(padx=10, pady=10, ipadx=20, side="left", fill="both")

        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.pack(padx=10, pady=10, side="right", fill="both", expand=True)

        self.frame2.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=True)
        self.frame2.grid_columnconfigure(1 , weight=True)
        self = Buttons.buttons_F1( self )


    def CallBacks( self, valid_button ):
        if valid_button == "ButtonCreateWeapon":
            self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal" )

        elif valid_button == "ButtonEditWeapon":
            if db.has_weapon_in_database("Editar"):
                self.create_or_edit_weapon( ButtonsAcess.EditWeaponEntry, "ButtonEditWeapon", "disabled", "normal", "normal" )
            else:
                self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal" )
        elif valid_button == "ButtonDeletWeapon":
            if db.has_weapon_in_database("deleta"):
                self.create_or_edit_weapon( ButtonsAcess.DeleteWeaponEntry, "ButtonDeletWeapon", "normal", "normal", "disabled" )
            else:
                self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal" )


    def create_or_edit_weapon( self, callback_func, button, ButtonEdit, ButtonCreate, ButtonDelet ):
        self = callback_func( self )
        self = Buttons.buttons_F2( self, button )
        self.ButtonEditWeapon.configure( state=ButtonEdit )
        self.ButtonCreateWeapon.configure( state=ButtonCreate )
        self.ButtonDeletWeapon.configure( state=ButtonDelet )


    def create_entry_and_label(self, use_placeholders=True):
        self.Weapon = {}
        global associar
        keys = ["cost", "cost_up", "cost_re_up", "limit", "round", "kills", "hs", "alias"]
        texts = ["Cost:", "Cost Up:", "Cost Re-Up:", "Limit Round:", "Round Unlock:", "Kills Unlock:", "Hs Unlock:", "Alias:"]
        placeholders = ["Somente Numeros Inteiros.",
                        "Somente Numeros Inteiros.",
                        "Somente Numeros Inteiros.",
                        "Somente Numeros Inteiros valor padrão: [ Unlimit ].",
                        "Somente Numeros Inteiros valor padrão: [ Unlimit ].",
                        "Somente Numeros Inteiros valor padrão: [ Unlimit ].",
                        "Somente Numeros Inteiros valor padrão: [ Unlimit ].",
                        "Array de nomes separados por: \",\"."]

        for num, key_string in enumerate(keys):
            self.Weapon[key_string + "_lb"] = customtkinter.CTkLabel(self.frame2, text=texts[num])
            self.Weapon[key_string + "_lb"].grid(row=(2 + num), column=0, sticky="e", padx=10)

            placeholder_text = placeholders[num] if use_placeholders else None

            self.Weapon[key_string] = customtkinter.CTkEntry(self.frame2, placeholder_text=placeholder_text)
            self.Weapon[key_string].grid(row=(2 + num), column=1, sticky="we", padx=10)
            self.Weapon[key_string].bind("<KeyRelease>", command=lambda event: Updates.update_button_clearEntrys(self, event))

            if key_string != "alias":
                self.Weapon[key_string].bind( "<KeyPress>", EnterPress )


class Updates:
    def ClearFrameData( self ):
        for widget in self.frame2.winfo_children():
            widget.destroy()


    def has_text_in_entrys( self, event ):
        for child in self.frame2.winfo_children():
            if isinstance( child, customtkinter.CTkEntry ):
                if len( child.get() ) > 0 and child == self.Weapon["cost_up"]:
                    if has_upgraded_support( self.WeaponName.get() ):
                        return True
                    
                if len( child.get() ) > 0 and child == self.Weapon["cost_re_up"]:
                    if can_upgraded_weapon( self.WeaponName.get() ):
                        return True

                if len( child.get() ) > 0 and child not in [ self.Weapon["cost_up"], self.Weapon["cost_re_up"] ]:
                    return True
                
        return False
        

    def update_button_clearEntrys( self, event ):
        if Updates.has_text_in_entrys( self, event ):
            self.ButtonClearWeapon.configure( state="normal" )
        else:
            self.ButtonClearWeapon.configure( state="disabled" )  
        

    def ClearEntrys( self ):
        self.ButtonClearWeapon.focus()

        for widget in self.frame2.winfo_children():
            if isinstance( widget, customtkinter.CTkEntry ):
                if len( widget.get() ) > 0 and widget in [ self.Weapon["cost_up"], self.Weapon["cost_re_up"] ]:
                    if has_upgraded_support( self.WeaponName.get() ) or can_upgraded_weapon( self.WeaponName.get() ):
                        widget.delete( 0, "end" )
                        widget.focus()
                        continue

                if len( widget.get() ) > 0:
                    widget.delete( 0, "end" )
                    widget.focus()

        self.ButtonClearWeapon.configure( state="disabled" )
        self.ButtonClearWeapon.focus()


    def update_weapon_names_dropdown( self, WeaponClass ):
        global level_Class
        if WeaponClass != level_Class:
            list_weapons = [ weapons for weapons in weapon_list_json["all"][WeaponClass] ]
            self.WeaponName.configure( values=list_weapons , variable=StringVar( list_weapons[0] ) )
            Updates.ClearEntrys( self )
            Updates.update_weapon_cost_fields_from_name( self, self.WeaponName.get() )
            level_Class = WeaponClass


    def update_weapon_cost_fields_from_name( self, Weapon ):
        global level_weapon
        if Weapon != level_weapon:
            level_weapon = Weapon
            
            if has_upgraded_support(Weapon):
                self.Weapon["cost_up"].configure(state="normal")

            else:
                self.Weapon["cost_up"].delete(0, "end")
                self.Weapon["cost_up"].insert(0, "null")
                self.Weapon["cost_up"].configure(state="disabled")

            if can_upgraded_weapon(Weapon):
                self.Weapon["cost_re_up"].configure(state="normal")

            else:
                self.Weapon["cost_re_up"].delete(0, "end")
                self.Weapon["cost_re_up"].insert(0, "null")
                self.Weapon["cost_re_up"].configure(state="disabled")

            Updates.ClearEntrys( self )
            self.ButtonClearWeapon.focus()

        
    def entry_weapon_delete( self, event ):
        if not( db.has_weapon_in_database( "", False ) ):
            App.CallBacks( self, "ButtonCreateWeapon" )

        else:
            list_class = db.get_available_class_from_database()
            if self.WeaponClass.get() in list_class:
                list_weapon = db.get_weapons_by_class_from_database(self.WeaponClass.get())
            else:
                list_weapon = db.get_weapons_by_class_from_database(list_class[0])
                self.WeaponClass.configure( values=list_class, variable=StringVar(list_class[0]))

            self.WeaponName.configure( values=list_weapon, variable=StringVar(list_weapon[0]))


class UpdatesEdit:
    def update_weapon_names_dropdown( self, WeaponClass ):
        global level_Class
        if WeaponClass != level_Class:
            WeaponsName = db.get_weapons_by_class_from_database( WeaponClass )
            self.WeaponName.configure( values=WeaponsName, variable=StringVar( WeaponsName[0] ) )
            UpdatesEdit.update_current_weapon_entry( self, WeaponsName[0] )
            level_Class = WeaponClass
        

    def update_weapon_names_dropdown_delete( self, WeaponClass ):
        global level_Class
        if WeaponClass != level_Class:
            WeaponsName = db.get_weapons_by_class_from_database( WeaponClass )
            self.WeaponName.configure( values=WeaponsName, variable=StringVar( WeaponsName[0] ) )
            level_Class = WeaponClass


    def update_current_weapon_entry( self, WeaponName ):
        data_weapon = db.get_data_from_database_by_weaponName( WeaponName )

        self.Weapon["cost"].configure( textvariable=StringVar( data_weapon["cost"] ) )
        
        if has_upgraded_support( WeaponName ):
            costUp = data_weapon["costUp"]
            self.Weapon["cost_up"].configure( state="normal" )
        else:
            costUp = "null"
            self.Weapon["cost_up"].configure( state="disabled" )
        
        if can_upgraded_weapon( WeaponName ):
            costReUp = data_weapon["costReUp"]
            self.Weapon["cost_re_up"].configure( state="normal" )
        else:
            costReUp = "null"
            self.Weapon["cost_re_up"].configure( state="disabled" )
        
        self.Weapon["cost_up"].configure( textvariable=StringVar( costUp) )
        self.Weapon["cost_re_up"].configure( textvariable=StringVar( costReUp ) )
        self.Weapon["limit"].configure( textvariable=StringVar( data_weapon["limitRound"] ) )
        self.Weapon["round"].configure( textvariable=StringVar( data_weapon["roundUnlock"] ) )
        self.Weapon["kills"].configure( textvariable=StringVar( data_weapon["killsUnlock"] ) )
        self.Weapon["hs"].configure( textvariable=StringVar( data_weapon["hsUnlock"] ) )
        self.Weapon["alias"].configure( textvariable=StringVar( data_weapon["alias"] ) )

        self.ButtonClearWeapon.configure( state="normal" )


class Buttons:
    def buttons_F1( self ):
        self.ButtonCreateWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Create Weapon", command=lambda : self.CallBacks( "ButtonCreateWeapon" ) )
        self.ButtonCreateWeapon.pack( pady=15, padx=5 )

        self.ButtonEditWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Edit Weapon", command=lambda : self.CallBacks( "ButtonEditWeapon" ) )
        self.ButtonEditWeapon.pack( pady=10, padx=5 )

        self.ButtonDeletWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Delete Weapon", command=lambda : self.CallBacks( "ButtonDeletWeapon" ) )
        self.ButtonDeletWeapon.pack( pady=15, padx=5 )

        self.ButtonExportInJson = customtkinter.CTkButton( self.frame1, height=35, text="Export Json", command=db.export_database_to_json )
        self.ButtonExportInJson.pack( pady=10, padx=5 )
      
        self.ButtonClearWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Clear Text", state="disabled", command=lambda : Updates.ClearEntrys( self ) )
        self.ButtonClearWeapon.pack( pady=15, padx=5 )
        
        self.ButtonOptionMenu = customtkinter.CTkOptionMenu( self.frame1, height=35, values=["dark","light"], command=customtkinter.set_appearance_mode )
        self.ButtonOptionMenu.pack( pady=10, padx=5, side="bottom" )

        self.ButtonRestart = customtkinter.CTkButton( self.frame1, height=35, text="Restart", command=lambda : UpdatesEdit.update_current_weapon_entry( self, self.WeaponName.get() )  )

        self.Creditos = customtkinter.CTkButton( self.frame1, text="Made by: BOY7", height=35, font=customtkinter.CTkFont("Courier New"), command=open_discord )
        self.Creditos.pack( side="bottom" )

        return self


    def buttons_F2( self, valid_button ):
        if valid_button == "ButtonCreateWeapon":
            self.ButtonAddWeapon = customtkinter.CTkButton( self.frame2, height=35, text="Add Weapon Sqlite", command=lambda : add( self )  )
            self.ButtonAddWeapon.grid( row=10, column=1, columnspan=2, pady=10 )

            self.ButtonRestart.pack_forget()

            return self

        elif valid_button == "ButtonEditWeapon":
            self.ButtonEditWeaponSqlite = customtkinter.CTkButton( self.frame2, height=35, text="Edit Weapon Sqlite", command=lambda : upgraded( self ) )
            self.ButtonEditWeaponSqlite.grid( row=10, column=1, columnspan=2, pady=10 )
            
            self.ButtonRestart.pack( pady=10 )

            return self

        elif valid_button == "ButtonDeletWeapon":
            self.ButtonDeletWeaponSqlite = customtkinter.CTkButton( self.frame2, height=35, text="Delete Weapon Sqlite", command=lambda : db.delete_weapon_by_database( self.WeaponName.get() ) )
            self.ButtonDeletWeaponSqlite.grid( row=10, column=1, columnspan=2, pady=10 )
            self.ButtonDeletWeaponSqlite.bind( "<Button-1>", lambda event: Updates.entry_weapon_delete( self, event ) )

            self.ButtonRestart.pack_forget()

            return self


class ButtonsAcess:
    def CreateWeaponEntry( self ):
        self.ButtonClearWeapon.configure(state="disabled")

        Updates.ClearFrameData( self )

        self.WeaponClass_lb = customtkinter.CTkLabel( self.frame2, text="Class:" )
        self.WeaponClass_lb.grid( row=0, column=0, sticky="e", padx=10 )
        self.WeaponClass = customtkinter.CTkComboBox( self.frame2, values=[ Class for Class in weapon_list_json["all"] ], state="readonly", variable=StringVar( "Snipers" ),command=lambda WeaponClass: Updates.update_weapon_names_dropdown( self, WeaponClass ) )
        self.WeaponClass.grid( row=0, column=1, sticky="we", padx=10 )
        global level_Class
        level_Class = self.WeaponClass.get()

        self.WeaponName_lb = customtkinter.CTkLabel( self.frame2, text="Name:" )
        self.WeaponName_lb.grid( row=1, column=0, sticky="e", padx=10 )
        self.WeaponName = customtkinter.CTkComboBox( self.frame2, values=[ Weapons for Weapons in weapon_list_json["all"][self.WeaponClass.get()] ], state="readonly", variable=StringVar( "DSR50" ), command=lambda Weapon: Updates.update_weapon_cost_fields_from_name( self, Weapon ) )
        self.WeaponName.grid( row=1, column=1, sticky="we", padx=10 )
        
        global level_weapon
        level_weapon = self.WeaponName.get()
        self.create_entry_and_label( True )

        return self
    

    def EditWeaponEntry( self ):
        self.ButtonClearWeapon.configure(state="normal")

        Updates.ClearFrameData( self )
        WeaponsClass = db.get_available_class_from_database()
        WeaponsName = db.get_weapons_by_class_from_database( WeaponsClass[0] )

        self.WeaponClass_lb = customtkinter.CTkLabel( self.frame2, text="Class:" )
        self.WeaponClass_lb.grid( row=0, column=0, sticky="e", padx=10 )
        self.WeaponClass = customtkinter.CTkComboBox( self.frame2, values=WeaponsClass, variable=StringVar(WeaponsClass[0]), state="readonly", command=lambda WeaponClass: UpdatesEdit.update_weapon_names_dropdown( self, WeaponClass ) )
        self.WeaponClass.grid( row=0, column=1, sticky="we", padx=10 )

        self.WeaponName_lb = customtkinter.CTkLabel( self.frame2, text="Name:" )
        self.WeaponName_lb.grid( row=1, column=0, sticky="e", padx=10 )
        self.WeaponName = customtkinter.CTkComboBox( self.frame2, values=WeaponsName, variable=StringVar(WeaponsName[0]), state="readonly", command=lambda WeaponName: UpdatesEdit.update_current_weapon_entry( self, WeaponName ) )
        self.WeaponName.grid( row=1, column=1, sticky="we", padx=10 )
        
        global level_Class
        level_Class = WeaponsClass[0]

        self.create_entry_and_label( False )

        UpdatesEdit.update_current_weapon_entry( self, WeaponsName[0] )

        return self
    

    def DeleteWeaponEntry(self):
        self.ButtonClearWeapon.configure(state="disabled")

        Updates.ClearFrameData( self )
        WeaponsClass = db.get_available_class_from_database()
        WeaponsName = db.get_weapons_by_class_from_database( WeaponsClass[0] )

        self.WeaponClass_lb = customtkinter.CTkLabel( self.frame2, text="Class:" )
        self.WeaponClass_lb.grid( row=0, column=0, sticky="e", padx=10 )
        self.WeaponClass = customtkinter.CTkComboBox( self.frame2, values=WeaponsClass, variable=StringVar(WeaponsClass[0]), state="readonly", command=lambda WeaponClass: UpdatesEdit.update_weapon_names_dropdown_delete( self, WeaponClass ) )
        self.WeaponClass.grid( row=0, column=1, sticky="we", padx=10 )

        self.WeaponName_lb = customtkinter.CTkLabel( self.frame2, text="Name:" )
        self.WeaponName_lb.grid( row=1, column=0, sticky="e", padx=10 )
        self.WeaponName = customtkinter.CTkComboBox( self.frame2, values=WeaponsName, variable=StringVar(WeaponsName[0]), state="readonly" )
        self.WeaponName.grid( row=1, column=1, sticky="we", padx=10 )
        
        global level_Class
        level_Class = WeaponsClass[0]

        return self

App().mainloop()