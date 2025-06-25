import customtkinter

app = customtkinter.CTk()
app.geometry("1500x1000")

settings_button = customtkinter.CTkButton(
    master=app,
    text="Settings Button"
)
settings_button.pack()
app.mainloop()

I have a big problem. I wanted to create a nice looking UI. But now there is customtkinter in the way. Because of a weird bug everything in the UI would be pixalated on my linux machine, so I can't work from my laptop what means I only can work on it tomorry when I'm at my pc.