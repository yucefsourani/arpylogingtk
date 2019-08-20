#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arpylogingtk.py
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
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib,Gdk,GdkPixbuf,Pango,GObject
import os
import threading
import time
import sqlite3
from sqlite3 import Error




sql_create_remember_user_table = """ CREATE TABLE IF NOT EXISTS remember (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL DEFAULT ''
                                    ); """

sql_update_remember_user_table = ''' UPDATE remember
              SET name = ?
              WHERE id = ? '''

sql_insert_remember_user_table = ''' INSERT INTO remember(name) 
                      SELECT  '' 
                      WHERE NOT EXISTS(SELECT 1 FROM remember WHERE id = 1 ); '''
              
sql_select_remember_user_table = "SELECT name FROM remember WHERE id=?"
              

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent=None):
        Gtk.MessageDialog.__init__(self,buttons = Gtk.ButtonsType.OK_CANCEL)
        self.props.message_type = Gtk.MessageType.QUESTION
        self.props.text         = msg
        self.p=parent
        if self.p != None:
            self.parent=self.p
            self.set_transient_for(self.p)
            self.set_modal(True)
            self.p.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            if self.p != None:
                self.p.set_sensitive(True)
            return True
        else:
            if self.p != None:
                self.p.set_sensitive(True)
            self.destroy()
            return False

class UsersConfig(object):
    def __init__(self,db_file):
        self.__db_file = db_file
        self.__create_table()

        
    def __get_conn(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.__db_file)
        except Error as e:
            print(e)

        return conn
        
    def get_all_users(self):
        sql_get_all_users = "SELECT name FROM loginremember"
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_get_all_users)
                    rows = cur.fetchall()
                    return  rows
            except Error as e:
                print(e)
                return False
        else:
            return False
            
    def get_all_users_with_admin(self):
        sql_get_all_users = "SELECT name,admin FROM loginremember"
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_get_all_users)
                    rows = cur.fetchall()
                    return  rows
            except Error as e:
                print(e)
                return False
        else:
            return False
    
    def get_all_passwords(self):
        sql_get_all_passwords = "SELECT password FROM loginremember"
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_get_all_passwords)
                    rows = cur.fetchall()
                    return  rows
            except Error as e:
                print(e)
                return False
        else:
            return Falses

    def get_user_password(self,user_):
        sql_get_user_password = "SELECT password FROM loginremember WHERE name=?"
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_get_user_password,(user_,))
                    rows = cur.fetchall()
                    return  rows
            except Error as e:
                print(e)
                return False
        else:
            return Falses
    
    def get_user_info(self,user):
        sql_get_user_info = "SELECT name,password,admin FROM loginremember"
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_get_user_info)
                    rows = cur.fetchall()
                    for row in rows:
                        if row[0]==user:
                            return  row
            except Error as e:
                print(e)
                return False
        else:
            return Falses
        
    def add_user(self,user,password,admin):
        all_users = [u for i in self.get_all_users() for u in i if u==user]
        print(all_users)
        if all_users:
            return "e"
        sql_insert_user = ''' INSERT INTO loginremember(name,password,admin)
                                                 VALUES(?,?,?) '''
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_insert_user,(user,password,admin))
                    return cur.lastrowid
            except Error as e:
                print(e)
                return False
        else:
            return False
        
    def remove_user(self,user):
        sql_delete_user = ''' DELETE FROM loginremember WHERE name=?'''
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_delete_user,(user,))
                    return cur.lastrowid
            except Error as e:
                print(e)
                return False
        else:
            return False
        
    def change_user_password(self,user,password):
        sql_change_user_password = ''' UPDATE loginremember
                                       SET password = ? 
                                       WHERE name = ?'''
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_change_user_password,(password,user))
                    return cur.lastrowid
            except Error as e:
                print(e)
                return False
        else:
            return False
    
    def change_user_admin(self,user,admin):
        sql_change_user_admin = ''' UPDATE loginremember
                                       SET admin = ? 
                                       WHERE name = ?'''
        conn = self.__get_conn()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_change_user_admin,(admin,user))
                    return cur.lastrowid
            except Error as e:
                print(e)
                return False
        else:
            return False
        
    def __create_table(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        create_table_sql = """ CREATE TABLE IF NOT EXISTS loginremember (
                                        id integer PRIMARY KEY,
                                        name  text NOT NULL,
                                        password  text NOT NULL,
                                        admin integer NOT NULL
                                    ); """
        conn = self.__get_conn()
        try:
            with conn:
                c = conn.cursor()
                c.execute(create_table_sql)
        except Error as e:
            print(e)
            return False
        return True
        


class EditUser(Gtk.Window):
    def __init__(self,user,
                 text_view=None,
                 uu=None,
                 parent=None,
                 liststore=None,
                 show_password_tooltip="<b>Show Password</b>",
                 hide_password_tooltip="<b>Hide Password</b>",
                 stat_msg_timeout=3,
                 icon_show_location="",
                 icon_hide_location=""):
                    
        Gtk.Window.__init__(self)
        self.props.default_height = 200
        self.props.default_width = 400
        self.props.resizable = False
        
        self.user                       = user
        self.parent                     = parent
        self.text_view                  = text_view
        self.uu                         = uu
        self.liststore                  = liststore
        self.show_password_tooltip      = show_password_tooltip
        self.hide_password_tooltip      = hide_password_tooltip
        self.stat_msg_timeout           = stat_msg_timeout
        self.icon_show_location         = icon_show_location
        self.icon_hide_location         = icon_hide_location
        

        
        if self.parent:
            self.set_modal(True)
            self.set_transient_for(self.parent)
            self.set_destroy_with_parent(True)

        self.vmain_box  = Gtk.VBox()
        self.vmain_box.set_margin_top(10)
        self.vmain_box.set_margin_bottom(5)
        self.vmain_box.set_margin_start(10)
        self.vmain_box.set_margin_end(10)
        self.vmain_box.props.spacing = 10
        
        user_label = Gtk.Label()
        user_label.props.label = self.user
        user_label.get_style_context().add_class("h1")
        self.vmain_box.pack_start(user_label,False,False,0)
        
        self.hmain_box  = Gtk.HBox()
        self.hmain_box.props.spacing = 10
        
        
        
        
        vbox1 = Gtk.VBox()
        vbox1.props.homogeneous = True
        vbox1.props.spacing     = 10
        
        vbox2 = Gtk.VBox()
        vbox2.props.homogeneous = True
        vbox2.props.spacing     = 10
        
        
        pass0_label = Gtk.Label()
        pass0_label.props.label = "Old Password"
        
        pass1_label = Gtk.Label()
        pass1_label.props.label = "New Password"
        
        pass2_label = Gtk.Label()
        pass2_label.props.label = "Retype Password"
        

        
        
        
        
        if self.icon_show_location:
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(self.icon_show_location)
        else:
            icon_show      = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"132906.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/132906.svg")] if os.path.isfile(i)]
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(icon_show[0])
    
        if self.icon_hide_location:
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(self.icon_hide_location)
        else:
            icon_hide       = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"130516.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/130516.svg")] if os.path.isfile(i)]
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(icon_hide[0])


        self.pass0_entry             = Gtk.Entry()
        self.pass0_entry.props.max_length   = 30
        self.pass0_entry.set_visibility(False)
        self.pass0_entry.props.placeholder_text = "Enter Password"
        self.pass0_entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.pass0_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass0_entry.connect("icon-press",self.on_icon_press)
        
        
        self.pass1_entry             = Gtk.Entry()
        self.pass1_entry.props.max_length   = 30
        self.pass1_entry.set_visibility(False)
        self.pass1_entry.props.placeholder_text = "Enter Password"
        self.pass1_entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.pass1_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass1_entry.connect("icon-press",self.on_icon_press)
        
        self.pass2_entry             = Gtk.Entry()
        self.pass2_entry.props.max_length   = 30
        self.pass2_entry.set_visibility(False)
        self.pass2_entry.props.placeholder_text = "Retype Password"
        self.pass2_entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.pass2_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass2_entry.connect("icon-press",self.on_icon_press)
        
        

        
        hboxbutton = Gtk.HBox()
        hboxbutton.props.homogeneous = True
        hboxbutton.props.spacing     = 5
        
        cancelbutton = Gtk.Button()
        cancelbutton.props.label = "Cancel"
        cancelbutton.connect("clicked",self.__on_cancelbutton_clicked)
        
        applybutton = Gtk.Button()
        applybutton.props.label = "Apply"
        applybutton.connect("clicked",self.__on_applybutton_clicked)
        
        hboxbutton.pack_start(cancelbutton,False,False,0)
        hboxbutton.pack_start(applybutton,False,False,0)
        
        self.stat_label = Gtk.Label()
        self.stat_label.get_style_context().add_class("h3")
        
        vbox1.pack_start(pass0_label,False,False,0)
        vbox1.pack_start(pass1_label,False,False,0)
        vbox1.pack_start(pass2_label,False,False,0)

        
        vbox2.pack_start(self.pass0_entry,False,False,0)
        vbox2.pack_start(self.pass1_entry,False,False,0)
        vbox2.pack_start(self.pass2_entry,False,False,0)

        
        self.hmain_box.pack_start(vbox1,False,False,0)
        self.hmain_box.pack_start(vbox2,False,False,0)

        
        self.vmain_box.pack_start(self.hmain_box,False,False,0)
        self.vmain_box.pack_start(hboxbutton,False,False,0)
        self.vmain_box.pack_start(self.stat_label,False,False,0)
        self.add(self.vmain_box)

    def __on_cancelbutton_clicked(self,button):
        self.destroy()
        
    def __on_applybutton_clicked(self,button):
        pass0   = self.pass0_entry.get_text().replace(" ","")
        pass1   = self.pass1_entry.get_text().replace(" ","")
        pass2   = self.pass2_entry.get_text().replace(" ","")

        
        check = GLib.Checksum(GLib.ChecksumType.SHA256)
        check.update(pass0.encode("utf-8"))
        __oldpass1 = check.get_string()
        __oldpass2 = self.uu.get_user_password(self.user)[0][0]

        
        if len(pass0)<6:
            print("Old Password should be at least 6 characters" )
            self.change_stat_label(self.stat_label,"Old Password should be at least 6 characters")
            return
        if len(pass1)<6:
            print("Enter New Password  at least 6 characters" )
            self.change_stat_label(self.stat_label,"Enter New Password  at least 6 characters")
            return
        if not pass2:
            print("Enter Retype Password")
            self.change_stat_label(self.stat_label,"Enter Retype Password")
            return
        if pass1!=pass2:
            print("Password not match")
            self.change_stat_label(self.stat_label,"Password not match")
            return
        if __oldpass1!=__oldpass2:
            print("Old Password not match")
            self.change_stat_label(self.stat_label,"Old Password not match")
            return
            
        
        check.reset()
        check.update(pass1.encode("utf-8"))
        __pass = check.get_string()
        self.uu.change_user_password(self.user,__pass)
        

        print("Edit User {} done".format(self.user))
        #self.change_stat_label(self.stat_label,"Edit User {} done".format(self.user))
        self._quit()
        
    def on_icon_press(self, entry,icon_position,event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button==1:
            if entry.get_visibility():
                entry.set_visibility(False)
                entry.props.secondary_icon_tooltip_markup = self.show_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_show
            else:
                entry.set_visibility(True)
                entry.props.secondary_icon_tooltip_markup = self.hide_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_hide
                
    def __thread_change_stat_label(self,stat_label,label):
        stat_label.props.label = label
        GLib.idle_add(self.stat_label.set_label,label)
        time.sleep(self.stat_msg_timeout)
        #GLib.idle_add(stat_label.show)
        if not self.stat_msg_timeout <=0:
            GLib.idle_add(stat_label.set_label,"")
        #GLib.idle_add(stat_label.hide)
        
    def change_stat_label(self,stat_label,label):
        threading.Thread(target=self.__thread_change_stat_label,args=(stat_label,label),daemon=True).start()
        
    def _quit(self,window=None,event=None):
        self.hide()
        self.destroy()
        



class AddUser(Gtk.Window):
    def __init__(self,text_view=None,
                 uu=None,parent=None,
                liststore=None,
                show_password_tooltip="<b>Show Password</b>",
                hide_password_tooltip="<b>Hide Password</b>",
                stat_msg_timeout=3,
                icon_show_location="",
                icon_hide_location=""):
                    
        Gtk.Window.__init__(self)
        self.props.default_height = 200
        self.props.default_width = 400
        self.props.resizable = False
        
        self.parent                     = parent
        self.text_view                  = text_view
        self.uu                         = uu
        self.liststore                  = liststore
        self.show_password_tooltip      = show_password_tooltip
        self.hide_password_tooltip      = hide_password_tooltip
        self.stat_msg_timeout           = stat_msg_timeout
        self.icon_show_location         = icon_show_location
        self.icon_hide_location         = icon_hide_location
        
        if self.parent:
            self.set_modal(True)
            self.set_transient_for(self.parent)
            self.set_destroy_with_parent(True)

        self.vmain_box  = Gtk.VBox()
        self.vmain_box.set_margin_top(10)
        self.vmain_box.set_margin_bottom(5)
        self.vmain_box.set_margin_start(10)
        self.vmain_box.set_margin_end(10)
        self.vmain_box.props.spacing = 10
        self.hmain_box  = Gtk.HBox()
        self.hmain_box.props.spacing = 10
        
        
        
        
        vbox1 = Gtk.VBox()
        vbox1.props.homogeneous = True
        vbox1.props.spacing     = 10
        
        vbox2 = Gtk.VBox()
        vbox2.props.homogeneous = True
        vbox2.props.spacing     = 10
        
        
        user_label = Gtk.Label()
        user_label.props.label = "New User"
        
        pass1_label = Gtk.Label()
        pass1_label.props.label = "Password"
        
        pass2_label = Gtk.Label()
        pass2_label.props.label = "Retype Password"
        
        admin_label = Gtk.Label()
        admin_label.props.label = "IsAdmin"
        
        
        
        
        if self.icon_show_location:
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(self.icon_show_location)
        else:
            icon_show      = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"132906.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/132906.svg")] if os.path.isfile(i)]
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(icon_show[0])
    
        if self.icon_hide_location:
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(self.icon_hide_location)
        else:
            icon_hide       = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"130516.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/130516.svg")] if os.path.isfile(i)]
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(icon_hide[0])


        self.user_entry             = Gtk.Entry()
        self.user_entry.props.max_length   = 30
        self.user_entry.props.placeholder_text = "Enter New User"
        
        self.pass1_entry             = Gtk.Entry()
        self.pass1_entry.props.max_length   = 30
        self.pass1_entry.set_visibility(False)
        self.pass1_entry.props.placeholder_text = "Enter Password"
        self.pass1_entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.pass1_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass1_entry.connect("icon-press",self.on_icon_press)
        
        self.pass2_entry             = Gtk.Entry()
        self.pass2_entry.props.max_length   = 30
        self.pass2_entry.set_visibility(False)
        self.pass2_entry.props.placeholder_text = "Retype Password"
        self.pass2_entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.pass2_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass2_entry.connect("icon-press",self.on_icon_press)
        
        
        self.isadmin = Gtk.CheckButton.new()
        self.isadmin.set_active(True)
        
        hboxbutton = Gtk.HBox()
        hboxbutton.props.homogeneous = True
        hboxbutton.props.spacing     = 5
        
        cancelbutton = Gtk.Button()
        cancelbutton.props.label = "Cancel"
        cancelbutton.connect("clicked",self.__on_cancelbutton_clicked)
        
        addbutton = Gtk.Button()
        addbutton.props.label = "Add"
        addbutton.connect("clicked",self.__on_addbutton_clicked)
        
        hboxbutton.pack_start(cancelbutton,False,False,0)
        hboxbutton.pack_start(addbutton,False,False,0)
        
        self.stat_label = Gtk.Label()
        self.stat_label.get_style_context().add_class("h3")
        
        vbox1.pack_start(user_label,False,False,0)
        vbox1.pack_start(pass1_label,False,False,0)
        vbox1.pack_start(pass2_label,False,False,0)
        vbox1.pack_start(admin_label,False,False,0)
        
        vbox2.pack_start(self.user_entry,False,False,0)
        vbox2.pack_start(self.pass1_entry,False,False,0)
        vbox2.pack_start(self.pass2_entry,False,False,0)
        vbox2.pack_start(self.isadmin,False,False,0)
        
        self.hmain_box.pack_start(vbox1,False,False,0)
        self.hmain_box.pack_start(vbox2,False,False,0)

        
        self.vmain_box.pack_start(self.hmain_box,False,False,0)
        self.vmain_box.pack_start(hboxbutton,False,False,0)
        self.vmain_box.pack_start(self.stat_label,False,False,0)
        self.add(self.vmain_box)

    def __on_cancelbutton_clicked(self,button):
        self.destroy()
        
    def __on_addbutton_clicked(self,button):
        user    = self.user_entry.get_text().replace(" ","")
        pass1   = self.pass1_entry.get_text().replace(" ","")
        pass2   = self.pass2_entry.get_text().replace(" ","")
        __admin =  1 if self.isadmin.get_active() else 0
        
        

        if not user:
            print("Enter New User")
            self.change_stat_label(self.stat_label,"Enter New User")
            return
        else:
            for i in self.uu.get_all_users():
                if user in i:
                    print("User already exists")
                    self.change_stat_label(self.stat_label,"User already exists")
                    return
            

        if len(pass1)<6:
            print("Enter Password  at least 6 characters" )
            self.change_stat_label(self.stat_label,"Enter Password  at least 6 characters")
            return
        if not pass2:
            print("Enter Retype Password")
            self.change_stat_label(self.stat_label,"Enter Retype Password")
            return
        if pass1!=pass2:
            print("Password not match")
            self.change_stat_label(self.stat_label,"Password not match")
            return
        
        check = GLib.Checksum(GLib.ChecksumType.SHA256)
        check.update(pass1.encode("utf-8"))
        __pass = check.get_string()
        

        self.uu.add_user(user,__pass,__admin)
        
        self.liststore.append([user,self.isadmin.get_active()])
        

        self._quit()
        print("Add User {} done".format(user))
        
    def on_icon_press(self, entry,icon_position,event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button==1:
            if entry.get_visibility():
                entry.set_visibility(False)
                entry.props.secondary_icon_tooltip_markup = self.show_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_show
            else:
                entry.set_visibility(True)
                entry.props.secondary_icon_tooltip_markup = self.hide_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_hide
                
    def __thread_change_stat_label(self,stat_label,label):
        stat_label.props.label = label
        GLib.idle_add(self.stat_label.set_label,label)
        time.sleep(self.stat_msg_timeout)
        #GLib.idle_add(stat_label.show)
        if not self.stat_msg_timeout <=0:
            GLib.idle_add(stat_label.set_label,"")
        #GLib.idle_add(stat_label.hide)
        
    def change_stat_label(self,stat_label,label):
        threading.Thread(target=self.__thread_change_stat_label,args=(stat_label,label),daemon=True).start()
        
    def _quit(self,window=None,event=None):
        self.hide()
        self.destroy()



class UsersConfigWindow(Gtk.Window):
    def __init__(self,parent=None,
                user_db="test.db",
                show_password_tooltip="<b>Show Password</b>",
                hide_password_tooltip="<b>Hide Password</b>",
                stat_msg_timeout=3,
                icon_show_location="",
                icon_hide_location=""):
                    
        Gtk.Window.__init__(self)
        self.parent                     = parent
        self.user_db                    = user_db
        self.show_password_tooltip      = show_password_tooltip
        self.hide_password_tooltip      = hide_password_tooltip
        self.stat_msg_timeout           = stat_msg_timeout
        self.icon_show_location         = icon_show_location
        self.icon_hide_location         = icon_hide_location
        
        self.props.default_height = 200
        self.props.default_width = 400
        if self.parent:
            self.set_modal(True)
            self.set_transient_for(self.parent)
            self.set_destroy_with_parent(True)
            
        self.uu = UsersConfig(self.user_db)
            
        self.main_box          = Gtk.VBox()
        #self.main_box.set_margin_top(10)
        #self.main_box.set_margin_bottom(5)
        #self.main_box.set_margin_start(10)
        #self.main_box.set_margin_end(10)
        self.main_box.props.spacing = 10

        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        toolbar = Gtk.Toolbar()
        toolbutton = Gtk.ToolButton()
        toolbutton.set_label("New User")
        toolbutton.set_is_important(True)
        toolbutton.set_icon_name("gtk-new")
        toolbar.add(toolbutton)
        
        dtoolbutton = Gtk.ToolButton()
        dtoolbutton.set_label("Delete User")
        dtoolbutton.set_is_important(True)
        dtoolbutton.set_icon_name("gtk-delete")
        dtoolbutton.set_sensitive(False)
        toolbar.add(dtoolbutton)
        
        etoolbutton = Gtk.ToolButton()
        etoolbutton.set_label("Edit")
        etoolbutton.set_is_important(True)
        etoolbutton.set_icon_name(Gtk.STOCK_EDIT)
        etoolbutton.set_sensitive(False)
        toolbar.add(etoolbutton)

        self.liststore = Gtk.ListStore(str, bool)
        for user in self.uu.get_all_users_with_admin():
            self.liststore.append([user[0],True if user[1]==1 else False])


        treeview = Gtk.TreeView()
        treeview.set_hover_expand(True)
        
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.liststore)
        treeview.set_activate_on_single_click(True)
        treeview.connect("row-activated",self.__on_row_activate,dtoolbutton,etoolbutton)
        
        cellrenderertext = Gtk.CellRendererText()
        cellrenderertext.set_property("ellipsize", Pango.EllipsizeMode.START)

        treeviewcolumn = Gtk.TreeViewColumn("Users")
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.set_fixed_width(399)
        treeviewcolumn.set_min_width(30)
        treeviewcolumn.set_max_width(100)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        treeview.append_column(treeviewcolumn)

        renderer_toggle = Gtk.CellRendererToggle()
        self.renderer_toggle_signal_handler = renderer_toggle.connect("toggled", self.on_cell_toggled)


        treeviewcolumn = Gtk.TreeViewColumn("Admin",renderer_toggle, active=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.set_fixed_width(399)
        treeviewcolumn.set_min_width(30)
        treeviewcolumn.set_max_width(100)
        treeviewcolumn.set_alignment(0.5)
        
        self.main_box.pack_start(toolbar,False,False,0)
        self.main_box.pack_start(scrolled_window,True,True,0)
        scrolled_window.add(treeview)
        
        dtoolbutton.connect("clicked",self.__on_toolbutton_delete,treeview,dtoolbutton,etoolbutton)
        toolbutton.connect("clicked",self.__on_toolbutton_new,treeview,dtoolbutton,etoolbutton)
        etoolbutton.connect("clicked",self.__on_toolbutton_edit,treeview)
        self.add(self.main_box)

    def on_cell_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]
        isadmin = 1 if self.liststore[path][1] else 0
        user    = self.liststore[path][0]
        if isadmin:
            yn = Yes_Or_No("Make {} Admin?".format(user),self)
        else:
            yn = Yes_Or_No("Remove {} From Admin?".format(user),self)
        if not yn.check():
            self.liststore[path][1] = 0 if isadmin else 1
            return
        self.uu.change_user_admin(user,isadmin)
                
    def __on_row_activate(self,tree_view, path, column,dtoolbutton,etoolbutton):
        """print(tree_view)
        print(path)
        print(self.liststore[path])
        print(self.liststore[path][0])
        print(self.liststore[path][1])
        print(column)"""
        dtoolbutton.set_sensitive(True)
        etoolbutton.set_sensitive(True)


        
    def __on_toolbutton_new(self,button,tree_view,dtoolbutton,etoolbutton):
        mainwindow = AddUser(tree_view,self.uu,self,self.liststore,\
                             self.show_password_tooltip,self.hide_password_tooltip,\
                             self.stat_msg_timeout,self.icon_show_location,self.icon_hide_location)
        mainwindow.connect("delete-event",mainwindow._quit)
        mainwindow.show_all()
        if len(self.liststore)==0:
            dtoolbutton.set_sensitive(False)
            etoolbutton.set_sensitive(False)
        else:
            dtoolbutton.set_sensitive(True)
            etoolbutton.set_sensitive(True)
        
    def __on_toolbutton_delete(self,button,tree_view,dtoolbutton,etoolbutton):
        selection = tree_view.get_selection()
        model, paths = selection.get_selected_rows()
        
        for path in paths:
            iter = model.get_iter(path)
            _user = model.get_value(iter,0)
            yn = Yes_Or_No("Delete {}".format(_user),self)
            if not yn.check():
                return
            self.uu.remove_user(_user)
            model.remove(iter)
        if len(self.liststore)==0:
            dtoolbutton.set_sensitive(False)
            etoolbutton.set_sensitive(False)
        else:
            dtoolbutton.set_sensitive(True)
            etoolbutton.set_sensitive(True)
            
        
    def __on_toolbutton_edit(self,button,tree_view):
        selection = tree_view.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            iter = model.get_iter(path)
            _user = model.get_value(iter,0)
        mainwindow = EditUser(_user,tree_view,self.uu,self,self.liststore,\
                     self.show_password_tooltip,self.hide_password_tooltip,\
                     self.stat_msg_timeout,self.icon_show_location,self.icon_hide_location)
        mainwindow.connect("delete-event",mainwindow._quit)
        mainwindow.show_all()

    #def on_cell_edited(self, cellrenderertext, treepath, text):
    #    self.liststore[treepath][1] = text
    

    
    def _quit(self,window=None,event=None):
        self.hide()
        self.destroy()
    
    
    
    
    
    
    
    
    
    
class LoginWindow(Gtk.Window):
    __gsignals__ = {
        "onsuccess"     : (GObject.SignalFlags.RUN_LAST, None, (str,bool,str)),

    }
    def __init__(self,main_label="Welcome",
                     user_label="User",\
                     password_label="Password",
                     title="Login",\
                     user_entry_placeholder="Enter User",\
                     password_entry_placeholder="Enter Password",\
                     login_button_label="Connect",\
                     user_entry_default_text="",
                     login_faild="Login Faild",
                     remmber_user_name="remmber_user_name.db",
                     user_db="test.db",
                     apply_msg="Connecting",
                     active_remember=True,
                     show_password_tooltip="<b>Show Password</b>",
                     hide_password_tooltip="<b>Hide Password</b>",
                     stat_msg_timeout=3,
                     icon_show_location="",
                     icon_hide_location="",
                     remember_label="Remember",
                     apply_button_css_class="destructive-action" ):# suggested-action
                         
        Gtk.Window.__init__(self)
        self.props.default_height = 200
        self.props.default_width = 400
        self.props.resizable = False
        self.old_user = ""
        css = b"""
        .h1 {
            font-size: 24px;
        }

        .h2 {
            font-weight: 300;
            font-size: 18px;
        }

        .h3 {
            font-size: 11px;
            color: red;
            font-weight: bold;
        }

        .h4 {
            color: alpha (@text_color, 0.7);
            font-weight: bold;
            text-shadow: 0 1px @text_shadow_color;
        }

        .h4 {
            padding-bottom: 6px;
            padding-top: 6px;
        }
        """
        self.main_label                 = main_label
        self.user_label                 = user_label
        self.password_label             = password_label
        self.login_button_label         = login_button_label
        self.user_entry_placeholder     = user_entry_placeholder
        self.password_entry_placeholder = password_entry_placeholder
        self.login_button_label         = login_button_label
        self.user_entry_default_text    = user_entry_default_text 
        self.login_faild                = login_faild
        self.remmber_user_name          = remmber_user_name
        self.user_db                    = user_db
        self.apply_msg                  = apply_msg
        self.title                      = title
        self.active_remember            = active_remember
        self.show_password_tooltip      = show_password_tooltip
        self.hide_password_tooltip      = hide_password_tooltip
        self.stat_msg_timeout           = stat_msg_timeout
        self.icon_show_location         = icon_show_location
        self.icon_hide_location         = icon_hide_location
        self.remember_label             = remember_label
        self.apply_button_css_class     = apply_button_css_class
        
        self.set_title(self.title)
        
        
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        mainlabel = Gtk.Label()
        mainlabel.props.label = self.main_label
        mainlabel.get_style_context().add_class("h1")
        mainlabel.set_margin_top(10)
        mainlabel.set_margin_bottom(10)
        mainlabel.set_margin_start(10)
        mainlabel.set_margin_end(10)
        mainlabel.props.wrap = True


        self.main_box          = Gtk.VBox()
        self.main_box.set_margin_top(10)
        self.main_box.set_margin_bottom(5)
        self.main_box.set_margin_start(10)
        self.main_box.set_margin_end(10)
        self.main_box.props.spacing = 10
        
        

        user_pass_main_hbox       = Gtk.HBox()
        user_pass_main_hbox.props.spacing = 10
        
        label_vbox                = Gtk.VBox()
        label_vbox.props.homogeneous = True
        label_vbox.props.spacing  = 10
        
        entry_vbox                = Gtk.VBox()
        entry_vbox.props.homogeneous = True
        entry_vbox.props.spacing  = 12
        
        user_entry_hbox                = Gtk.HBox()
        user_entry_hbox.props.spacing  = 5
        pass_entry_hbox                = Gtk.HBox()
        user_entry_hbox.props.spacing  = 5


        self._user_label               = Gtk.Label()
        self._user_label.props.label   = self.user_label
        self._user_label.get_style_context().add_class("h2")
        self.user_entry           = Gtk.Entry()
        self.user_entry.props.placeholder_text = self.user_entry_placeholder
        self.user_entry.set_text(self.user_entry_default_text)
        #self.user_entry.set_tooltip_markup("Thomson Router Admin User (Try Administrator)")
        self.user_entry.props.max_length       = 30 
        

        if self.active_remember:
            user_check_button = Gtk.CheckButton.new_with_label(self.remember_label)
            
        
            conn = self.create_connection(self.remmber_user_name)
            if conn:
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql_select_remember_user_table, (1,))
                    rows = cur.fetchall()
                    user_t = rows[0][0]
                    self.user_entry.set_text(user_t)
                    if user_t:
                        user_check_button.set_active(True)
            else:
                print("Connect to {} Faild.".format(self.remmber_user_name))
        else:
            user_check_button = None

        if self.icon_show_location:
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(self.icon_show_location)
        else:
            icon_show      = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"132906.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/132906.svg")] if os.path.isfile(i)]
            self.icon_show = GdkPixbuf.Pixbuf.new_from_file(icon_show[0])
    
        if self.icon_hide_location:
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(self.icon_hide_location)
        else:
            icon_hide       = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"130516.svg"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/130516.svg")] if os.path.isfile(i)]
            self.icon_hide = GdkPixbuf.Pixbuf.new_from_file(icon_hide[0])
        
        self._pass_label             = Gtk.Label()
        self._pass_label.props.label = self.password_label
        self._pass_label.get_style_context().add_class("h2")
        self.pass_entry             = Gtk.Entry()
        self.pass_entry.props.max_length   = 30
        self.pass_entry.set_visibility(False)
        self.pass_entry.props.placeholder_text = self.password_entry_placeholder
        self.pass_entry.props.secondary_icon_tooltip_markup = self.show_password_tooltip
        self.pass_entry.props.secondary_icon_pixbuf = self.icon_show
        self.pass_entry.connect("icon-press",self.on_icon_press)


        label_vbox.pack_start(self._user_label,False,True,0)
        entry_vbox.pack_start(user_entry_hbox,False,True,0)
        user_entry_hbox.pack_start(self.user_entry,False,True,0)
        if self.active_remember:
            user_entry_hbox.pack_start(user_check_button,False,True,0)
        
        
        label_vbox.pack_start(self._pass_label,False,True,0)
        entry_vbox.pack_start(pass_entry_hbox,False,True,0)
        pass_entry_hbox.pack_start(self.pass_entry,False,True,0)
        
        user_pass_main_hbox.pack_start(label_vbox,True,True,0)
        user_pass_main_hbox.pack_start(entry_vbox,True,True,0)


###################################################################################################################
        stat_label = Gtk.Label()
        stat_label.get_style_context().add_class("h3")
        
        
        self.connect_button = Gtk.Button()
        self.connect_button.props.label = self.login_button_label
        if self.apply_button_css_class:
            self.connect_button.get_style_context().add_class(self.apply_button_css_class) 
        self.connect_button.connect("clicked",self.on_connect,self,self.user_entry,self.pass_entry,main_label,self._user_label,self._pass_label,stat_label,user_check_button)


        
        self.main_box.pack_start(mainlabel,False,True,0)
        self.main_box.pack_start(user_pass_main_hbox,False,True,0)
        self.main_box.pack_start(self.connect_button,False,True,0)
        self.main_box.pack_start(stat_label,False,True,0)

        self.add(self.main_box)



            
    def on_icon_press(self, entry,icon_position,event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button==1:
            if entry.get_visibility():
                entry.set_visibility(False)
                entry.props.secondary_icon_tooltip_markup = self.show_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_show
            else:
                entry.set_visibility(True)
                entry.props.secondary_icon_tooltip_markup = self.hide_password_tooltip
                entry.props.secondary_icon_pixbuf = self.icon_hide



    def __thread_change_stat_label(self,stat_label,label):
        stat_label.props.label = label
        GLib.idle_add(stat_label.set_label,label)
        time.sleep(self.stat_msg_timeout)
        #GLib.idle_add(stat_label.show)
        if not self.stat_msg_timeout<=0:
            GLib.idle_add(stat_label.set_label,"")
        #GLib.idle_add(stat_label.hide)
        
    def change_stat_label(self,stat_label,label):
        threading.Thread(target=self.__thread_change_stat_label,args=(stat_label,label),daemon=True).start()
        
    def on_connect(self,button,parent,user_entry,password_entry,main_label,_user_label,_pass_label,stat_label,user_check_button):
        threading.Thread(target=self.thread_on_connect,args=(button,parent,user_entry,password_entry,main_label,_user_label,_pass_label,stat_label,user_check_button)).start()
        
        
    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            self.create_table(conn,sql_create_remember_user_table)
        except Error as e:
            print(e)

        return conn
        
    def create_table(self,conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            c.execute(sql_insert_remember_user_table)
        except Error as e:
            print(e)
            return False
        return True
        
    def thread_on_connect(self,button,parent,user_entry,password_entry,main_label,_user_label,_pass_label,stat_label,user_check_button):
        pass0   = password_entry.get_text().replace(" ","")
        user_found = False
            
        GLib.idle_add(stat_label.set_label,self.apply_msg)
        GLib.idle_add(parent.set_sensitive,False)
        
        uu = UsersConfig(self.user_db)
        
        _user_ = user_entry.get_text().replace(" ","")
        if not _user_:
            print("Enter '{} Entry'".format(self._user_label.get_label()))
            self.change_stat_label(stat_label,"Enter '{} Entry'".format(self._user_label.get_label()))
            GLib.idle_add(parent.set_sensitive,True)
            return
        if not pass0:
            print("Enter '{} Entry'".format(self._pass_label.get_label()))
            self.change_stat_label(stat_label,"Enter '{} Entry'".format(self._pass_label.get_label()))
            GLib.idle_add(parent.set_sensitive,True)
            return
        for i in uu.get_all_users():
            if _user_ in i:
                user_found = True
                
        if not user_found:
            print(self.login_faild)
            self.change_stat_label(stat_label,self.login_faild)
            GLib.idle_add(parent.set_sensitive,True)
            return
        

            
        check = GLib.Checksum(GLib.ChecksumType.SHA256)
        check.update(pass0.encode("utf-8"))
        __newpass = check.get_string()
        check.reset()
        
        __oldpass = uu.get_user_password(_user_)[0][0]
        
        
        if __oldpass == __newpass:
            conn = self.create_connection(self.remmber_user_name)
            if self.active_remember:
                if not user_check_button.get_active():
                    if conn:
                        with conn:
                            cur = conn.cursor()
                            cur.execute(sql_update_remember_user_table, ("",1))
                    else:
                        print("Conenct to {} Faild.".format(self.remmber_user_name))
                else:
                    if conn:
                        with conn:
                            cur = conn.cursor()
                            olduser = user_entry.get_text()
                            cur.execute(sql_update_remember_user_table, (olduser,1))
                    else:
                        print("Conenct to {} Faild.".format(self.remmber_user_name))
                    
            #print("Login Success")
            #self.change_stat_label(stat_label,"Login Success")
            #GLib.idle_add(self.destroy)
            GLib.idle_add(self.__on__success,_user_,True if uu.get_user_info(_user_)[-1]==1 else False)
        else:
            print(self.login_faild)
            self.change_stat_label(stat_label,self.login_faild) 
            GLib.idle_add(parent.set_sensitive,True)
        GLib.idle_add(parent.set_sensitive,True)
        
    def __on__success(self,username,isadmin,):
        self.emit("onsuccess",username,isadmin,self.user_db)



