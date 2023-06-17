from __future__ import annotations
import os
import json
import socket
import tkinter
import webbrowser
import customtkinter
import db_functions_2 as db

from pathlib import Path
from tkinter import messagebox
from typing import Union, Any, Dict, List, Callable

associar = False


with open( db.resource_path("file\\weapon_list.json") ) as file:
    weapon_list_json = json.load( file )


def open_discord() -> None:
    webbrowser.open_new( "https://discord.gg/ZSXEVB9h8C" )


def EnterPress( event: tkinter.Event ) -> Union[ str, None ] :
    
    widget = event.widget  # type: customtkinter.CTkEntry

    if event.keysym.isdigit() or event.keysym in [ "Tab", "Shift_L",  "Shift_R", "BackSpace", "Delete", "Up", "Down", "Left", "Right" ]:
        for x in ["n","u","l"]:
            if x in widget.get() and event.keysym != "BackSpace":
                widget.bell()
                return "break"

        if widget.select_present() and event.keysym == "0":
            if widget.index("sel.first") == widget.index(0):
                widget.bell()
                return "break"
        
        if widget.index("insert") < 1 and event.keysym == "0":
            widget.bell()
            return "break"

        if event.keysym == "Up":
            widget.icursor(0)

        elif event.keysym == "Down":
            widget.icursor("end")

        return
    else:
        widget.bell()
        return "break"


def StringVar( string: str ) -> Any:
    return customtkinter.StringVar( value=string )
        

def has_upgraded_support( weapon: str ) -> bool:
    return weapon in weapon_list_json["support an upgrade"]


def can_upgraded_weapon( weapon: str ) -> bool:
    return has_upgraded_support( weapon ) and weapon in weapon_list_json["support an attachment"]


def common_data( self: Union[ App, ButtonsAcess ] ) -> Dict[ str, Union[ App, ButtonsAcess ] ]:
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


def add( self: Union[ App, ButtonsAcess ] ) -> None:
    weapon = common_data( self )
    db.add_weapon_database( weapon["class"], weapon["name_id"], weapon["name_string"], weapon["alias"], weapon["cost"], weapon["cost_up"],
                            weapon["cost_re_up"], weapon["limit"], weapon["round"], weapon["kills"], weapon["hs"] )


def upgraded( self: Union[ App, ButtonsAcess ] ) -> None:
    weapon = common_data( self )
    db.update_data_from_database( weapon["name_id"], weapon["alias"], weapon["cost"], weapon["cost_up"], weapon["cost_re_up"],
                                    weapon["limit"], weapon["round"], weapon["kills"], weapon["hs"] )


class Rcon:
    def send_command( ip: str, port: int, password: str, command: str, serve_name ) -> str:
        try:
            connect = socket.socket (socket.AF_INET, socket.SOCK_DGRAM )
            message = b"\xFF\xFF\xFF\xFFrcon %s %s" % ( password.encode(), command.encode() )
            connect.sendto( message, ( ip, port ) )

            data, address = connect.recvfrom( 4096 )

            respond = data[10:].decode()

            messagebox.showerror( title="rcon", message=f"Atualizador com sucesso")

            return respond

        except socket.error as e:
            messagebox.showerror( title="rcon", message=f"Error ao tenta se conectar ao serve: {serve_name}")
    
class App( customtkinter.CTk ):
    def __init__( self ):
        super().__init__()
        self.toplevel = None
        self.main_window()


    def main_window( self ) -> None:
        self.title("T6WeaponEdit")
        self.iconbitmap(db.resource_path("file\\T6WeapEd.ico"))
        x_screen = self.winfo_screenmmheight()
        y_screen = self.winfo_screenmmwidth()

        self.minsize(width=800, height=500)
        self.geometry( f"800x500+{ int( x_screen/0.3 - 800/2 ) }+{ int( y_screen/1 - 500/2 ) }" )

        self.frames()


    def frames( self ) -> None:
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.pack(padx=10, pady=10, ipadx=20, side="left", fill="both")

        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.pack(padx=10, pady=10, side="right", fill="both", expand=True)

        self.frame2.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=True)
        self.frame2.grid_columnconfigure(1 , weight=True)
        # self.bind
        self = Buttons.buttons_F1( self )

    def CallBacks( self , valid_button: str ) -> None:
        if valid_button == "ButtonCreateWeapon":
            self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal", "normal" )

        elif valid_button == "ButtonEditWeapon":
            if db.has_weapon_in_database("Editar"):
                self.create_or_edit_weapon( ButtonsAcess.EditWeaponEntry, "ButtonEditWeapon", "disabled", "normal", "normal", "normal" )
            else:
                self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal", "normal" )

        elif valid_button == "ButtonDeletWeapon":
            if db.has_weapon_in_database("deleta"):
                self.create_or_edit_weapon( ButtonsAcess.DeleteWeaponEntry, "ButtonDeletWeapon", "normal", "normal", "disabled", "normal" )
            else:
                self.create_or_edit_weapon( ButtonsAcess.CreateWeaponEntry, "ButtonCreateWeapon", "normal", "disabled", "normal", "normal" )

        elif valid_button == "ButtonUpdateWeaponInGame":
            self.create_or_edit_weapon( ButtonsAcess.UpdateWeaponInGame, "ButtonUpdateWeaponInGame", "normal", "normal", "normal", "disabled" )


    def create_or_edit_weapon( self: Union[ App, Buttons, ButtonsAcess ], callback_func: Callable, button: str, ButtonEdit: str, ButtonCreate: str, ButtonDelet: str, ButtonUpdate: str ) -> None:
        self = callback_func( self )
        self = Buttons.buttons_F2( self, button )
        self.ButtonEditWeapon.configure( state=ButtonEdit )
        self.ButtonCreateWeapon.configure( state=ButtonCreate )
        self.ButtonDeletWeapon.configure( state=ButtonDelet )
        self.ButttonUpdateWeaponInGame.configure( state=ButtonUpdate )


    def create_entry_and_label( self, use_placeholders: bool=True ):
        self.Weapon = {} # type: Dict[ str, Union[ customtkinter.CTkLabel, customtkinter.CTkEntry ] ]
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
    def ClearFrameData( self: Union[ App, ButtonsAcess ] ) -> None:
        for widget in self.frame2.winfo_children():
            widget.destroy()


    def has_text_in_entrys( self: Union[ App, Buttons, ButtonsAcess ], event: tkinter.Event ) -> bool:
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
        

    def update_button_clearEntrys( self: Union[ App, Buttons, ButtonsAcess ], event: tkinter.Event ) -> None:
        if Updates.has_text_in_entrys( self, event ):
            self.ButtonClearWeapon.configure( state="normal" )
        else:
            self.ButtonClearWeapon.configure( state="disabled" )  
        

    def ClearEntrys( self: Union[ App, Buttons, ButtonsAcess ] ) -> None:
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


    def update_weapon_names_dropdown( self: ButtonsAcess, WeaponClass: str ) -> None:
        global level_Class
        if WeaponClass != level_Class:
            list_weapons = [ weapons for weapons in weapon_list_json["all"][WeaponClass] ]
            self.WeaponName.configure( values=list_weapons , variable=StringVar( list_weapons[0] ) )
            Updates.ClearEntrys( self )
            Updates.update_weapon_cost_fields_from_name( self, self.WeaponName.get() )
            level_Class = WeaponClass


    def update_weapon_cost_fields_from_name( self: Union[ App, Buttons ], Weapon: str )  -> None:
        global level_weapon
        if Weapon != level_weapon:
            level_weapon = Weapon
            
            if has_upgraded_support( Weapon ):
                self.Weapon["cost_up"].configure(state="normal")

            else:
                self.Weapon["cost_up"].delete(0, "end")
                self.Weapon["cost_up"].insert(0, "null")
                self.Weapon["cost_up"].configure(state="disabled")

            if can_upgraded_weapon( Weapon ):
                self.Weapon["cost_re_up"].configure(state="normal")

            else:
                self.Weapon["cost_re_up"].delete(0, "end")
                self.Weapon["cost_re_up"].insert(0, "null")
                self.Weapon["cost_re_up"].configure(state="disabled")

            Updates.ClearEntrys( self )
            self.ButtonClearWeapon.focus()

        
    def entry_weapon_delete( self: Union[ Buttons, ButtonsAcess ], event ):
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
    def update_weapon_names_dropdown( self: ButtonsAcess, WeaponClass: str ) -> None:
        global level_Class
        if WeaponClass != level_Class:
            WeaponsName = db.get_weapons_by_class_from_database( WeaponClass )
            self.WeaponName.configure( values=WeaponsName, variable=StringVar( WeaponsName[0] ) )
            UpdatesEdit.update_current_weapon_entry( self, WeaponsName[0] )
            level_Class = WeaponClass
        

    def update_weapon_names_dropdown_delete( self: ButtonsAcess, WeaponClass ) -> None:
        global level_Class
        if WeaponClass != level_Class:
            WeaponsName = db.get_weapons_by_class_from_database( WeaponClass )
            self.WeaponName.configure( values=WeaponsName, variable=StringVar( WeaponsName[0] ) )
            level_Class = WeaponClass


    def update_current_weapon_entry( self: Union[ App, Buttons, ButtonsAcess ], WeaponName ):
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
    def buttons_F1( self: Union[ App, Buttons, ButtonsAcess ] ) -> Union[ App, Buttons, ButtonsAcess ]:
        self.ButtonCreateWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Create Weapon", command=lambda : self.CallBacks( "ButtonCreateWeapon" ) )
        self.ButtonCreateWeapon.pack( pady=10, padx=5 )

        self.ButtonEditWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Edit Weapon", command=lambda : self.CallBacks( "ButtonEditWeapon" ) )
        self.ButtonEditWeapon.pack( pady=10, padx=5 )

        self.ButtonDeletWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Delete Weapon", command=lambda : self.CallBacks( "ButtonDeletWeapon" ) )
        self.ButtonDeletWeapon.pack( pady=10, padx=5 )

        self.ButtonExportInJson = customtkinter.CTkButton( self.frame1, height=35, text="Export Json", command=db.export_database_to_json )
        self.ButtonExportInJson.pack( pady=10, padx=5 )
      
        self.ButtonClearWeapon = customtkinter.CTkButton( self.frame1, height=35, text="Clear Text", state="disabled", command=lambda : Updates.ClearEntrys( self ) )
        self.ButtonClearWeapon.pack( pady=10, padx=5 )
        
        self.ButtonOptionMenu = customtkinter.CTkOptionMenu( self.frame1, height=35, values=["dark","light"], command=customtkinter.set_appearance_mode )
        self.ButtonOptionMenu.pack( pady=10, padx=5, side="bottom" )

        self.ButttonUpdateWeaponInGame = customtkinter.CTkButton( self.frame1, height=35, text="Update In Game", command=lambda : self.CallBacks( "ButtonUpdateWeaponInGame" ) )
        self.ButttonUpdateWeaponInGame.pack( pady=10, padx=5 )

        self.ButtonRestart = customtkinter.CTkButton( self.frame1, height=35, text="Restart", command=lambda : UpdatesEdit.update_current_weapon_entry( self, self.WeaponName.get() )  )

        self.Creditos = customtkinter.CTkButton( self.frame1, text="Made by: BOY7", height=35, font=customtkinter.CTkFont("Courier New"), command=open_discord )
        self.Creditos.pack( side="bottom" )

        return self


    def buttons_F2( self: Union[ App, Buttons, ButtonsAcess ], valid_button: str ) -> Union[ App, Buttons, ButtonsAcess ]:
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
        
        elif valid_button == "ButtonUpdateWeaponInGame":
            return self


class ButtonsAcess:
    def CreateWeaponEntry( self: Union[ Buttons, ButtonsAcess, App ] ) -> Union[ App, Buttons, ButtonsAcess ]:
        self.ButtonClearWeapon.configure( state="disabled" )

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
    

    def EditWeaponEntry( self: Union[ App, Buttons, ButtonsAcess ] ) -> Union[ App, Buttons, ButtonsAcess ]:
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
    

    def DeleteWeaponEntry( self: Union[ App, Buttons, ButtonsAcess ] ) -> Union[ App, Buttons, ButtonsAcess ]:
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
    
    def UpdateWeaponInGame( self: Union[ App, Buttons, ButtonsAcess ] ) -> Union[ App, Buttons, ButtonsAcess ]:
        self.ButtonClearWeapon.configure(state="disabled")

        self.iconify() # minimiza a tela principal.

        if self.toplevel is not None and self.toplevel.winfo_exists(): # verfica ser já existe o toplevel.
            self.toplevel.deiconify() # tras a janela minimizada para frente.

        else: # se o toplevel não existe criar.
            self.toplevel = customtkinter.CTkToplevel()
            self.toplevel.title("Update Weapons inGame")

            x_screen = self.toplevel.winfo_screenmmheight()
            y_screen = self.toplevel.winfo_screenmmwidth()

            self.toplevel.resizable( False, False )
            self.toplevel.geometry(f"800x500+{int(x_screen/0.3 - 800/2)}+{int(y_screen/1 - 500/2)}")

            self.toplevel.protocol( "WM_DELETE_WINDOW", lambda: ButtonsAcess.reative( self ) )

            # Criando as frames botões etc...

            self.top_level_frame1 = customtkinter.CTkFrame( self.toplevel )
            self.top_level_frame1.pack( padx=10, pady=2, side="left", fill="both", expand=False )

            self.top_level_frame2 = customtkinter.CTkScrollableFrame( self.toplevel )
            self.top_level_frame2.pack( padx=10, pady=2, side="right", fill="both", expand=True )

            self.top_level_frame2.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=True)
            self.top_level_frame2.grid_columnconfigure(1 , weight=True)

            self.top_level_frame1.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=True)
            self.top_level_frame1.grid_columnconfigure(1 , weight=True)

            self.top_level_label_name = customtkinter.CTkLabel( self.top_level_frame1, text="Name:" )
            self.top_level_label_name.grid( row=0, column=0, padx=10, sticky="e" )
            self.top_level_entry_name = customtkinter.CTkEntry( self.top_level_frame1 )
            self.top_level_entry_name.grid( row=0, column=1, padx=10 )

            self.top_level_label_password = customtkinter.CTkLabel( self.top_level_frame1, text="Password:" )
            self.top_level_label_password.grid( row=1, column=0, padx=10, sticky="e" )
            self.top_level_entry_password = customtkinter.CTkEntry( self.top_level_frame1, show="*" )
            self.top_level_entry_password.grid( row=1, column=1, padx=10 )

            self.top_level_label_ip = customtkinter.CTkLabel( self.top_level_frame1, text="Ip:" )
            self.top_level_label_ip.grid( row=2, column=0, padx=10, sticky="e" )
            self.top_level_entry_ip = customtkinter.CTkEntry( self.top_level_frame1 )
            self.top_level_entry_ip.grid( row=2, column=1, padx=10 )

            self.top_level_label_port = customtkinter.CTkLabel( self.top_level_frame1, text="Port:" )
            self.top_level_label_port.grid( row=3, column=0, padx=10, sticky="e" )
            self.top_level_entry_port = customtkinter.CTkEntry( self.top_level_frame1 )
            self.top_level_entry_port.grid( row=3, column=1, padx=10 )

            self.top_level_button_create = customtkinter.CTkButton( self.top_level_frame1, height=35, text="Add Serve", command=lambda: ButtonsAcess.add_serve( self ) )
            self.top_level_button_create.grid( row=4, column=0, columnspan=2, padx=10 ) 

            self.top_level_button_up_all = customtkinter.CTkButton( self.top_level_frame1, height=35, text="Update All", command=lambda: ButtonsAcess.update_all_serves( self ) )
            self.top_level_button_up_all.grid( row=5, column=0, columnspan=2, pady=5,  padx=10, sticky="s", rowspan=5 )

            self = ButtonsAcess.load_widgets_to_serves( self )

        return self
    
    def update_all_serves( self ) -> None:
        serves = db.get_servers()
        
        if serves.__len__() < 1:
            print( "nem um serve encontrado!" )
            return

        for serve in serves:
            ButtonsAcess.send_command( serves[serve] )


    def ClearFrameData( self: Union[ App, ButtonsAcess ] ) -> None:
        for widget in self.top_level_frame2.winfo_children():
            widget.destroy()


    def load_widgets_to_serves( self ) -> ButtonsAcess:
        serves = db.get_servers()
        
        self.top_level_serve = {} # type: Dict[ str, Union[ customtkinter.CTkLabel, customtkinter.CTkButton ] ]

        for num , serve in enumerate( serves ):
            texto = serve
            if serve.__len__() > 20:
                texto = texto[:10] + "..."

            self.top_level_serve[serve + "_lb"] = customtkinter.CTkLabel( self.top_level_frame2, text=texto )
            self.top_level_serve[serve + "_lb"].grid( row=num, column=0, padx=10, pady=5, sticky="s" )

            self.top_level_serve[serve + "_btn"] = customtkinter.CTkButton( self.top_level_frame2, text="Update Serve", command=lambda _serve_=serve: ButtonsAcess.send_command( serves[_serve_] ) )
            self.top_level_serve[serve + "_btn"].grid( row=num, column=1, padx=5, pady=5 )

            self.top_level_serve[serve + "del_btn"] = customtkinter.CTkButton( self.top_level_frame2, text="Delet Serve", command=lambda _self_=self, _serve_=serve: ButtonsAcess.delet( _self_, _serve_ ) )
            self.top_level_serve[serve + "del_btn"].grid( row=num, column=2, padx=5, pady=5 )

        return self
    

    def delet( self, serve_name: str ) -> None:
        self.top_level_serve[serve_name + "_lb"].destroy()
        self.top_level_serve[serve_name + "_btn"].destroy()
        self.top_level_serve[serve_name + "del_btn"].destroy()
        
        db.delete_serve( serve_name )


    def send_command( serve: Dict[ str, str ] ) -> None:
        Rcon.send_command( serve["ip"], int( serve["port"] ), serve["password"], "wp_list up", serve["name"] )


    def add_serve( self ) -> None:
        if not ButtonsAcess.is_error_in_entry( self ):
            ButtonsAcess.create_serve( self, self.top_level_entry_name.get(), self.top_level_entry_password.get(), self.top_level_entry_ip.get(), self.top_level_entry_port.get() )


    def is_error_in_entry( self ) -> bool:
        if self.top_level_entry_name.get().strip() == "":
            messagebox.showinfo( title="Name", message="Preenchar o campo Name.")
            return True
        
        if self.top_level_entry_password.get().strip() == "":
            messagebox.showinfo( title="Password", message="Preenchar o campo Password.")
            return True
        
        if self.top_level_entry_ip.get().strip() == "":
            messagebox.showinfo( title="Ip", message="Preenchar o campo Ip.")
            return True
        
        if self.top_level_entry_port.get().strip() == "":
            messagebox.showinfo( title="Port", message="Preenchar o campo Port.")
            return True

        if not self.top_level_entry_port.get().strip().isdigit():
            messagebox.showinfo( title="Port", message="Preenchar o campo com numero int.")
            return True

        serves = db.get_servers() # dict com os servidores.

        if self.top_level_entry_name.get().strip() in serves:
            messagebox.showinfo( title="Name", message="Esse name de serve já existe tente outro nome por favor")
            return True
                
        return False


    def create_serve( self, name: str, password: str, ip: str, port: str ) -> None:
        __file__name__ = Path( db.resource_path( "file\\serve.json") )
        db.add_server( name, password, ip, port )

        ButtonsAcess.ClearFrameData( self )
        ButtonsAcess.load_widgets_to_serves( self )


    def reative( self: Union[ App, Buttons, ButtonsAcess ] ):
        self.ButttonUpdateWeaponInGame.configure( state="normal" )
        self.toplevel.destroy()
        self.toplevel = None


App().mainloop()