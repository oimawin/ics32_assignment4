from tkinter import *
from tkinter import filedialog, messagebox, simpledialog, ttk
from Profile import Profile, DsuFileError
from ds_messenger import DirectMessenger
import a4

class LoginWindow(Tk):
    def __init__(self):
        super().__init__()
        self.user = Profile()
        self._draw()
        
    def _draw(self) -> None:
        # Create widgets
        welcome_msg = Label(master=self,
                            text='Welcome to the ICS 32 Server!\nTo get started, enter a username and password\nor enter a dsu file path.')
        
        def _manual_entry() -> None:
            self.user.username = username_entry.get()
            self.user.password = password_entry.get()
            self.quit()
        
        def _file_entry() -> None:
            self._open_file()
            self.destroy()
            print(self.user.__dict__)
        
        # Widgets for user/password entry
        username_label = Label(master=self, text='Username')
        username_entry = Entry(master=self)
        password_label = Label(master=self, text='Password')
        password_entry = Entry(master=self)
        login_button = Button(master=self, text='Login', command=_manual_entry)
        
        or_label = Label(master=self, text='\nor\n')
        
        # Button widget for loading Profile from dsu file
        file_label = Button(master=self, text='Load a dsu file', command=_file_entry)
        
        # Pack widgets
        welcome_msg.grid(row=0, columnspan=2, padx=20, pady=20)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1)
        login_button.grid(row=4, columnspan=2, pady=10)
        or_label.grid(row=5, columnspan=2)
        file_label.grid(row=6, columnspan=2)
    
    def _open_file(self) -> None:
        try:
            filepath = filedialog.askopenfilename()
            self.user.load_profile(filepath)
        except DsuFileError:
            messagebox.showinfo("File error", "Not a valid dsu file! Try again or enter a username and password.")


class Body(Frame):
    def __init__(self, root, recipient_selected_callback=None):
        Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        print(self._contacts)
        print(entry)
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

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

        self.message_editor = Text(message_frame, width=0, height=5) #yscrollcommand
        self.message_editor.pack(fill=BOTH, side=LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = Text(editor_frame, width=0, height=5, state='disabled')
        #state=disabled
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


class ServerDialog(simpledialog.Dialog):
    def __init__(self, root, title=None, server=None):
        self.root = root
        self.server = server
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = Entry(frame, width=30)
        self.server_entry.pack()

    def apply(self):
        self.server = self.server_entry.get()


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


class MainApp(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = DirectMessenger()
        self.profile = Profile()
        self._draw()
        self._login_page()
        self.body.insert_contact("studentexw23") # adding one example student.

    def send_message(self):
        # You must implement this!
        body = self.body
        message = body.get_text_entry()
        body.node_select()
        self.direct_messenger.send(message, self.recipient)
        body.insert_user_message(message)

    def add_contact(self):
        rd = NewContactDialog(self.root, "Add Contact")
        self.body.insert_contact(rd.recipient)
        # Profile class add to recipient list
        # You must implement this!
        # Hint: check how to use simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        sd = ServerDialog(self.root, "Configure Server")
        self.server = sd.server
        self.direct_messenger.dsuserver = sd.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

    def publish(self, message:str):
        self.send(message, self.recipient)
        # You must implement this!

    def check_new(self):
        
        # You must implement this!
        pass
    
    def open_file(self) -> None:
        try:
            filepath = filedialog.askopenfilename()
            dsuprofile = Profile()
            dsuprofile.load_profile(filepath)
            self.profile = dsuprofile
            self.username = dsuprofile.username
            self.password = dsuprofile.password
            self.direct_messenger.username = dsuprofile.username
            self.direct_messenger.password = dsuprofile.password
        except DsuFileError:
            messagebox.showinfo("File error", "Not a valid dsu file! Try again or enter a username and password.")

    def _login_page(self) -> None:
        start = LoginWindow()
        start.title("ICS 32 DS Login")

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...',
                              command=self.open_file)
        menu_file.add_command(label='Close')

        settings_file = Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=BOTH, side=TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=BOTH, side=BOTTOM)


def main_page():
    main_window = Tk()
    
    recipients_scroll = Scrollbar(main_window)
    recipients_lb = Listbox(main_window, yscrollcommand = recipients_scroll.set)
    recipients_lb.insert(1, 'recipient1')
    
    recipient_label = Label(main_window, text='recipient1')
    
    conversation = Label(main_window)
    message_entry_label = Label(main_window, text='Type a message and press send')
    message_entry = Entry(main_window)
    send_button = Button(main_window, text='Send')
    
    logout_button = Button(main_window, text='Logout')
    
    adduser_button = Button(main_window, text='Add User')
    
    
    recipients_lb.grid(row=0, column=0, rowspan=10, columnspan=3)
    recipients_scroll.grid()
    recipient_label.grid(row=0, column=3, columnspan=5)
    conversation.grid(row=1, column=3, rowspan=8, columnspan=5)
    message_entry_label.grid(row=9, column=3, columnspan=5)
    message_entry.grid(row=10, column=3, columnspan=5)
    send_button.grid(row=10, column=10)
    adduser_button.grid(row=10, column=0, columnspan=3)
    logout_button.grid(row=11, column=3, pady=10)
    
    main_window.mainloop()

if __name__ == "__main__":
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
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
    
    # start = LoginWindow()
    # start.title("ICS 32 Distributed Social Login")
    # start.mainloop()