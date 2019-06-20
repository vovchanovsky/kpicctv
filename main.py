import Tkinter as tk
import Tkconstants, tkFileDialog
from PIL import Image
from PIL import ImageTk
import io, vlc, os, subprocess
from urllib2 import urlopen
from datetime import datetime

def video():
    t2 = tk.Toplevel(root)
    t2.focus_force()
    t2.title( u"Video")
    t2.geometry("250x50")
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    player.video_set_scale(0.5)
    def destroy():
        player.stop()
        t2.destroy()
    def rec():
            def stop():
                subprocess.Popen("taskkill /F /T /PID %i"%handle.pid , shell=True)
                s.destroy()
                r.pack()
            r.pack_forget()
            s=tk.Button(t2, text="Stop", bg = "red",command=stop)
            s.pack()
            handle = subprocess.Popen('vlc -I dummy --dummy-quiet -vvv http://stream.kpi.ua:'+options[variable.get()]+'/stream.flv --sout "#transcode{acodec=none}:file{dst=Data\%s.avi,no-overwrite} --dummy-quiet -I dummy' % str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')+options[variable.get()]), shell=False) 
    def play(self):
        r.pack()
        Media = Instance.media_new('http://stream.kpi.ua:'+options[variable.get()]+'/stream.flv')	
        Media.get_mrl()
        player.set_media(Media)
        player.play()
    variable = tk.StringVar(t2)
    options = {"Main Entrance": "50100",  "Knowledge Square": "8101", "Sikorsky": "8104","Monuments Alley": "8108", "Fountain": "8105",
               "Polyana": "8103", "Benchs-14k": "8107"}
    tk.Label(t2, text="Watch:").pack(side=tk.LEFT)
    tk.OptionMenu(t2, variable, *sorted(options.keys()), command=play).pack(side=tk.LEFT)
    r=tk.Button(t2, text="Record", bg = "red", command=rec)
    tk.Button(t2, text="Quit", command=destroy).pack()
    t2.mainloop()

def archive():
    filename = tkFileDialog.askopenfilename(initialdir = "Data",title = "Select file",filetypes = (("image files","*.png"),("avi files","*.avi")))
    if filename:
        os.system("start "+filename)
def conf():
    t3 = tk.Toplevel(root)
    t3.focus_force()
    t3.grab_set()
    t3.title("Settings")
    t3.geometry("250x160")
    tk.Label(t3, text="Video resolution:").pack() 
    tk.OptionMenu(t3, variable1, '720p', '480p', '240p').pack()
    tk.Label(t3, text="Frame per second:").pack()
    tk.OptionMenu(t3, variable2, '25', '50').pack()
    tk.Checkbutton(t3, text="Quality Enhancer", variable=var).pack()
    tk.Button(t3, text="Apply", command=lambda: t3.destroy()).pack()

    t3.mainloop()
def snapshot():
    t1 = tk.Toplevel(root)
    t1.title( u"Snapshot")
    t1.geometry("350x100")
    t1.focus_force()
    global label
    label = tk.Label(t1)
    def save():
            filename=tkFileDialog.asksaveasfilename(initialdir = "Data",title = "Save snapshot",initialfile=datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')+options[variable.get()]+'.png',filetypes = (("png files","*.png"),("all files","*.*")))
            if filename:
                url = "http://stream.kpi.ua/webcampics/latest-image.php?webcam="+options[variable.get()]
                fin = urlopen(url)
                t = io.BytesIO(fin.read())
                Image.open(t).save(filename,"PNG")
    def getimage(self):
        global label
        t1.geometry("640x450")
        url = "http://stream.kpi.ua/webcampics/latest-image.php?webcam="+options[variable.get()]
        fin = urlopen(url)
        # read into a memory stream
        s = io.BytesIO(fin.read())
        pil_image = Image.open(s)
        pil_image = pil_image.resize((640, 360))
        tk_image = ImageTk.PhotoImage(pil_image)
        # show the image in a label
        label.pack_forget()
        label = tk.Label(t1, image=tk_image)
        label.image = tk_image
        label.pack()
        savebtn.pack(side=tk.BOTTOM)
    savebtn=tk.Button(t1, text="Save", command=save)
    tk.Label(t1, text="Choose camera:").pack()
    variable = tk.StringVar(t1)
    options = {"Main Entrance": "b1-cam1",  "Knowledge Square": "b7-cam3", "Sikorsky": "b6-cam1","Monuments Alley": "b6-cam3", "Fountain": "b6-cam2",
               "Stone": "b4-cam1", "Polyana": "b12-cam2", "Benchs-14k": "b14-cam1", "Politechnichna-16k": "b16-cam1", "Politechnichna-RTF": "b17-cam1",
               "Politechnichna-2k1": "b2-cam1", "Politechnichna-2k2": "b2-cam2", "Sosnovyi-1": "b25-cam1", "Sosnovyi-2": "b25-cam2", "Sosnovyi-3": "b25-cam3"} 
    tk.OptionMenu(t1, variable, *sorted(options.keys()),command=getimage).pack()
    t1.mainloop()

if not os.path.exists("Data"):
    os.makedirs("Data")
root = tk.Tk()
frame = tk.Frame(root)
global variable1,variable2
variable1 = tk.StringVar(root)
variable2 = tk.StringVar(root)
var = tk.IntVar()
var.set(1)
variable1.set('720p')
variable2.set('25')
frame.pack()
tk.Label(frame, text="Welcome to Camera Control System!").pack()
tk.Label(frame, text="Choose your mode:").pack()
tk.Button(frame, text="Video", command=video).pack(side=tk.LEFT)
tk.Button(frame, text="Archive", command=archive).pack(side=tk.LEFT)
tk.Button(frame, text="Settings", command=conf).pack(side=tk.LEFT)
tk.Button(frame, text="Snapshot",command=snapshot).pack(side=tk.LEFT)
root.title("Camera Control System")
root.geometry("350x75")
root.mainloop()
