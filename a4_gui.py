
import time
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog, ttk
from Profile import Profile, DsuFileError, DsuProfileError
from ds_messenger import DirectMessenger, DirectMessage


# Server = 168.235.86.101

class Body(Frame):
    def __init__(self, root, recipient_selected_callback=None, new_msgs_callback=None, prev_msgs_callback=None):
        Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._new_msgs_callback = new_msgs_callback
        self._prev_msgs_callback = prev_msgs_callback
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        self.entry_editor.configure(state='normal')
        self.entry_editor.delete(1.0, END)
        self.entry_editor.configure(state='disabled')
        #load previous messages in session
        if self._select_callback is not None:
            self._select_callback(entry)
        if self._prev_msgs_callback is not None:
            self._prev_msgs_callback()
        if self._new_msgs_callback is not None:
            self._new_msgs_callback()

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def insert_contact_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(END, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = Frame(master=self, width=250)
        posts_frame.pack(fill=BOTH, side=LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=BOTH, side=TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = Frame(master=self, bg="")
        entry_frame.pack(fill=BOTH, side=TOP, expand=True)

        editor_frame = Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=BOTH, side=LEFT, expand=True)

        scroll_frame = Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=BOTH, side=LEFT, expand=False)

        message_frame = Frame(master=self, bg="yellow")
        message_frame.pack(fill=BOTH, side=TOP, expand=False)

        self.message_editor = Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=BOTH, side=LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = Text(editor_frame, width=0, height=5, state='disabled')
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=BOTH, side=LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=Y, side=LEFT,
                                    expand=False, padx=0, pady=0)

class Footer(Frame):
    def __init__(self, root, send_callback=None):
        Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=BOTH, side=RIGHT, padx=5, pady=5)

        self.footer_label = Label(master=self, text="Ready.")
        self.footer_label.pack(fill=BOTH, side=LEFT, padx=5)


class LoginDialog(simpledialog.Dialog):
    def __init__(self, root, title=None):
        self.root = root
        self.dsuserver = None
        self.username = None
        self.password = None
        super().__init__(root, title)

    def body(self, frame):
        self.username_label = Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = Entry(frame, width=30)
        self.username_entry.pack()
        
        self.password_label = Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = Entry(frame, width=30, show='*')
        self.password_entry.pack()
        
        self.dsuserver_label = Label(frame, width=30, text="DS Server Address")
        self.dsuserver_label.pack()
        self.dsuserver_entry = Entry(frame, width=30)
        self.dsuserver_entry.pack()

    def apply(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.dsuserver = self.dsuserver_entry.get()

class ServerDialog(simpledialog.Dialog):
    def __init__(self, root, title=None, server=None):
        self.root = root
        self.dsuserver = server
        super().__init__(root, title)

    def body(self, frame):
        self.dsuserver_label = Label(frame, width=30, text="DS Server Address")
        self.dsuserver_label.pack()
        self.dsuserver_entry = Entry(frame, width=30)
        self.dsuserver_entry.pack()

    def apply(self):
        self.dsuserver = self.dsuserver_entry.get()

class NewContactDialog(simpledialog.Dialog):
    def __init__(self, root, title=None, recipient=None):
        self.root = root
        self.recipient = recipient
        super().__init__(root, title)

    def body(self, frame):
        self.username_label = Label(frame, width=30, text="New Recipient Username")
        self.username_label.pack()
        self.username_entry = Entry(frame, width=30)
        self.username_entry.pack()
    
    def apply(self):
        self.recipient = self.username_entry.get()

class UserInfoDialog(simpledialog.Dialog):
    def __init__(self, root, username, dsuserver, title=None):
        self.root = root
        self.username = username
        self.dsuserver = dsuserver
        super().__init__(root, title)

    def body(self, frame):
        Label(frame, width=30, text="User Information").pack()
        Label(frame, width=30, text=f"Username: {self.username}").pack()
        Label(frame, width=30, text=f"DSU Server: {self.dsuserver}").pack()


class MainApp(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.dsuserver = None
        self.recipient = None
        self.dsufilepath = None
        self.direct_messenger = None
        self.profile = None
        self._draw()
        self.after(500, self.display_new_msgs)
        #self.after(5000, self.check_connected)

    def load_prev_messages(self):
        all_msgs = self.profile.directmsgs
        if self.recipient in all_msgs:
            for dm_obj in all_msgs[self.recipient]:
                if dm_obj.recipient == self.username:
                    self.body.insert_contact_message(dm_obj.message)
                elif dm_obj.recipient == self.recipient:
                    self.body.insert_user_message(dm_obj.message)

    def send_message(self):
        # You must implement this!
        if self.dsuserver is None:
            messagebox.showinfo("Offline", "You are not connected to a server!")
        else:
            message = self.body.get_text_entry()
            if self.direct_messenger.send(message, self.recipient):
                dm = DirectMessage()
                dm.create_dm(self.recipient, message, time.time())
                self.profile.store_dm(dm, self.recipient)
                self.body.insert_user_message(message)
                self.body.set_text_entry('')
            else:
                messagebox.showinfo("Send error", "Message could not be sent!")

    def add_contact(self):
        rd = NewContactDialog(self.root, "Add Contact")
        self.body.insert_contact(rd.recipient)
        self.profile.recipients.append(rd.recipient)
        # Profile class add to recipient list
        # You must implement this!
        # Hint: check how to use simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        sd = ServerDialog(self.root, "Configure Server")
        self.dsuserver = sd.dsuserver
        self.direct_messenger.dsuserver = sd.dsuserver
        self.profile.dsuserver = sd.dsuserver
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

    def publish(self, message:str):
        self.send(message, self.recipient)
        # You must implement this!

    def check_new(self):
        return self.direct_messenger.retrieve_new()
    
    def display_new_msgs(self):
        if self.recipient is not None and self.recipient is not None:
            new_msgs = self.check_new()
            for each in new_msgs:
                dm = DirectMessage()
                dm.create_dm(self.username, each.message, each.timestamp)
                self.profile.store_dm(dm, self.recipient)
                if each.recipient == self.recipient:
                    self.body.insert_contact_message(each.message)
            self.after(500, self.display_new_msgs)
    
    def open_file(self) -> None:
        try:
            filepath = filedialog.askopenfilename(filetypes=[("dsu file", "*.dsu")])
            dsuprofile = Profile()
            dsuprofile.load_profile(filepath)
            self.profile = dsuprofile
            self.username = dsuprofile.username
            self.password = dsuprofile.password
            self.dsuserver = dsuprofile.dsuserver
            self.direct_messenger = DirectMessenger(self.dsuserver, self.username, self.password)
            for i in dsuprofile.recipients:
                self.body.insert_contact(i)
            self.dsufilepath = filepath
        except DsuFileError:
            messagebox.showinfo("File error", "Not a valid dsu file! Try again or enter a username and password.")

    def _login_page(self) -> None:
        login = LoginDialog(self.root)
        self.username = login.username
        self.password = login.password
        self.dsuserver = login.dsuserver
        self.profile = Profile(self.dsuserver, self.username, self.password)
        self.direct_messenger = DirectMessenger(self.dsuserver, self.username, self.password)
        
    def show_user_info(self) -> None:
        UserInfoDialog(self.root, self.username, self.dsuserver)
    
    def check_connected(self) -> None:
        # TODO
        if self.dsuserver is None:
            self.footer.footer_label.config(text="Offline")
        else:
            self.footer.footer_label.config(text = "Online")
    
    def disconnect_server(self) -> None:
        self.dsuserver = None
        messagebox.showinfo("Disconnected", "You have been disconnected from the server.\nPlease reconnect to a server to send messages.")

    def save_and_close(self) -> None:
        try:
            if self.profile is None:
                raise DsuProfileError
            if self.dsufilepath is None:
                self.dsufilepath = filedialog.asksaveasfilename(filetypes=[("dsu file", "*.dsu")])
            self.profile.save_profile(self.dsufilepath)
            self.root.destroy()
        except DsuProfileError:
            messagebox.showinfo("Profile error", "You do not have a profile loaded! Please create a username and password before saving.")
        
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New',
                              command=self._login_page)
        menu_file.add_command(label='Open...',
                              command=self.open_file)
        menu_file.add_command(label='Close',
                              command=self.save_and_close)

        settings_file = Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Login',
                                  command=self._login_page)
        settings_file.add_command(label='User Information',
                                  command=self.show_user_info)
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        settings_file.add_command(label='Disconnect from DSU Server',
                                  command=self.disconnect_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected,
                         new_msgs_callback=self.display_new_msgs,
                         prev_msgs_callback=self.load_prev_messages)
        self.body.pack(fill=BOTH, side=TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=BOTH, side=BOTTOM)

def start_gui():
    main = Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()