#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  example.py
#  
#  Copyright 2019 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from arpylogingtk import LoginWindow, UsersConfigWindow 


class MainWindow(Gtk.Window):
    def __init__(self,username,isadmin,user_db):
        Gtk.Window.__init__(self)
        
        self.__isadmin  = isadmin
        self.__username = username
        self.__user_db  = user_db
        
        mainvbox = Gtk.VBox()
        
        edit_users_button = Gtk.Button()
        edit_users_button.props.label = "Edit Users"
        edit_users_button.connect("clicked",self.__when_edit_users_button_clicked)
        
        stat_label             = Gtk.Label()
        
        if self.__isadmin:
            stat_label.props.label = "{} Is Admin You Can Add/Edit/Remove Users".format(self.__username)
        else:
            stat_label.props.label = "{} Is not Admin You can't Add/Edit/Remove Users".format(self.__username)
            edit_users_button.set_sensitive(False)
            
            
        mainvbox.pack_start(stat_label,True,True,0)
        mainvbox.pack_start(edit_users_button,True,True,0)
        self.add(mainvbox)

    def __when_edit_users_button_clicked(self,button):
        usersconfigcindow = UsersConfigWindow(user_db=self.__user_db,                           
                                              icon_show_location="./icons/132906.svg", 
                                              icon_hide_location="./icons/130516.svg")
        usersconfigcindow.connect("delete-event",usersconfigcindow._quit)
        usersconfigcindow.show_all()



def on__success(login_window,username,isadmin,user_db):
    
    login_window.destroy()
    
    mainwindow = MainWindow(username,isadmin,user_db)
    mainwindow.connect("delete-event",Gtk.main_quit)                       
    mainwindow.show_all()
    

loginwindow =  LoginWindow(main_label="Welcome", # Default
                           user_label="User",    # Default
                           password_label="Password",# Default
                           title="Login", # Default
                           user_entry_placeholder="Enter User", # Default
                           password_entry_placeholder="Enter Password", # Default
                           login_button_label="Login",
                           user_entry_default_text="", # Default
                           login_faild="Login Faild",  # Default
                           remmber_user_name="db/remmber_user_name.db",
                           user_db="db/test.db",
                           apply_msg="Connecting", # Default
                           active_remember=True,   # Default
                           show_password_tooltip="<b>Show Password</b>", # Default
                           hide_password_tooltip="<b>Hide Password</b>", # Default
                           stat_msg_timeout=3, # Default
                           icon_show_location="./icons/132906.svg", 
                           icon_hide_location="./icons/130516.svg",
                           remember_label="Remember", # Default
                           apply_button_css_class="destructive-action" ) # Default
                         

loginwindow.connect("delete-event",Gtk.main_quit)                       
loginwindow.connect("onsuccess",on__success)
loginwindow.show_all()
Gtk.main()

    
    
    
