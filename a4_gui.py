from tkinter import *
from tkinter import filedialog, messagebox
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
        
        def get_info():
            self.user.username = username_entry.get()
            self.user.password = password_entry.get()
            # filepath = filedialog.asksaveasfilename()
            # self.user.save_profile(filepath)
        
        # Widgets for user/password entry
        username_label = Label(master=self, text='Username')
        username_entry = Entry(master=self)
        password_label = Label(master=self, text='Password')
        password_entry = Entry(master=self)
        login_button = Button(master=self, text='Login', command=get_info)
        
        or_label = Label(master=self, text='\nor\n')
        
        # Button widget for loading Profile from dsu file
        file_label = Button(master=self, text='Load a dsu file', command=self._open_file)
        
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
    
    def _load_user(self) -> None:
        dmuser = DirectMessenger()
        pass


def create_empty_window():
    window = Tk(className="Window name")
    
    window.geometry = ('400x400')
    # frame = tk.Fram e(window, height=400, width=400)
    # #frame.bind('<Enter>', _on_enter)
    # #frame.bind('<Leave>', _on_exit)
    # frame.pack()
    
    
    # message1 = Label(text="ICS32 Example GUI")
    # message2 = Label(window, text="This is label 2")
    
    # message1.grid(row=2, column=1)
    # message2.grid(row=2, column=1)
    # message.pack()
    
    # master: the widget objext that contains the widget
    # command: pass a function to run when the button is clicked through the command argument
        # Bind a function to an event
    button = Button(master=window, text="Press me")
    button.pack()
    
    window.mainloop()

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
    start = LoginWindow()
    start.title("ICS 32 Distributed Social Login")
    start.mainloop()