#Required software to run: Clarifai, Pillow

#app = ClarifaiApp()
#model1.train()
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from os import listdir
from os.path import isfile, join
#from twilio.rest import Client
#import os
#import twilio_code
from tkinter import *
from tkinter import filedialog
#INSTALL PILLOW
from PIL import Image, ImageTk
import tkinter.messagebox
import pprint

from watson_developer_cloud import VisualRecognitionV3
visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    api_key='e6048342d85488f0d7d95e65ecf13c0671a97c1c'
    )

root = Tk()

root.title("Trash-Detect")


app = ClarifaiApp(api_key='e30c5080088c4c998632632e5aa7b267')
model = app.models.get('general-v1.3')



#TESTING FOR A SINGLE IMAGE
def singlescan():
    trashfound = False
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file")
    print (root.filename)
    load = Image.open(root.filename)
    newload = load.resize((500, 300))
    render = ImageTk.PhotoImage(newload)
    #photo = PhotoImage(file="/Users/enkel/Pictures/443309.jpg")
    img = Label(root, image=render)
    img.image = render
    img.place(x=100,y=100)
    #label.pack()
    #Scanning = Label(root, text="Scanning Picture...")
    #Scanning.pack()
    
    trash_concepts = ['trash', 'garbage', 'litter', 'pollution', 'waste']
    #image = ClImage(url='https://www.outdoorlife.com/sites/outdoorlife.com/files/styles/2000_1x_/public/images/2017/10/kimber-super-jagare-hand-gun-hero.jpg?itok=4ld0IgLW&fc=50,50')

    image = ClImage(file_obj=open(root.filename, 'rb'))
    results = model.predict([image])
    for concept in results['outputs'][0]['data']['concepts']:
        value = concept['value']
        name = concept['name']
        if value > 0.8:
            if name in trash_concepts:
                print(concept['name'], value )
                trashfound = True
    
    if trashfound == True:
        print("Trash present")
        #w = Label(root, text="Trash present!")
        #w.pack()
        tkinter.messagebox.showinfo("Result", "Trash present!")

    #    import twilio_code
    else:
        print("Trash not present")
        #w = Label(root, text="Trash not present!")
        #w.pack()
        tkinter.messagebox.showinfo("Result", "Trash not present!")
    #oh so this is how u comment
    #Scanning.destroy()
    img.destroy()

# Some code to grab all files in folder (returns list)


def multiplescan():
    
    trashfound = False
    root.directory = filedialog.askdirectory(initialdir = "/",title = "Select directory")
    print (root.directory)
    mypath = root.directory + '/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.remove('.DS_Store')
    trash_concepts = ['trash', 'garbage', 'litter', 'pollution', 'waste']
    for photo_name in onlyfiles:
        full_path = mypath + photo_name
        print(full_path)
        load = Image.open(full_path)
        newload = load.resize((500, 300))
        render = ImageTk.PhotoImage(newload)
        #photo = PhotoImage(file="/Users/enkel/Pictures/443309.jpg")
        img = Label(root, image=render)
        img.image = render
        img.place(x=100,y=100)
        #label.pack()
        #Scanning = Label(root, text="Scanning Picture...")
        #Scanning.pack()
        image = ClImage(file_obj=open(full_path, 'rb'))
        results = model.predict([image])
        for concept in results['outputs'][0]['data']['concepts']:
            value = concept['value']
            name = concept['name']
            if value > 0.8:
                if name in trash_concepts:
                    print(concept['name'], value )
                    trashfound = True
        #Scanning.destroy()
        img.destroy()
    if trashfound == True:
        print("Trash Present")
        #w = Label(root, text="Trash present!")
        #w.pack()
        tkinter.messagebox.showinfo("Result", "Trash present!")
    
    #    import twilio_code
    else:
        print("Trash not present")
        #w = Label(root, text="Trash not present!")
        #w.pack()
        tkinter.messagebox.showinfo("Result", "Trash not present!")


def watsonscan():
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file")
    print (root.filename)
    load = Image.open(root.filename)
    newload = load.resize((500, 300))
    render = ImageTk.PhotoImage(newload)
    #photo = PhotoImage(file="/Users/enkel/Pictures/443309.jpg")
    photo = Label(root, image=render)
    photo.image = render
    photo.place(x=100,y=100)
    with open(root.filename, 'rb') as images_file:
        img = visual_recognition.classify(images_file, threshold='0.6')
    pprint.pprint(img)
    pprint.pprint(img['images'][0]['classifiers'][0]['classes'])
    datas = img['images'][0]['classifiers'][0]['classes'];
    xpos = 0
    info = ""
    for data in datas:
        info = info + "     " + data['class']
        #findings = Label(root, text=info)
        
        #findings.pack(side = "left")
        #findings.place(x=xpos,y=415)
        #print(data['class'])
        print(data['class'])
        print(data['score'])
        print()
        #xpos = xpos+150
    tkinter.messagebox.showinfo("Result", info)
    photo.destroy()


title = Label(root, text="Welcome to Trash Detect!")

#title.pack(side = "left")
title.place(x=250,y=100)
button_1 = Button(root, text="Scan an image for trash", command=singlescan)
button_1.pack()
button_1.place(x = 250, y=150)
button_2 = Button(root, text="Scan a directory for trash", command=multiplescan)
button_2.pack()
button_2.place(x=250, y=180)
button_3 = Button(root, text="Scan an image with IBM Watson", command=watsonscan)
button_3.pack()
button_3.place(x=250, y=210)

def center_window(width=700, height=450):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y-50))

center_window(700, 450)
#root.minsize(700,450)

root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

root.mainloop()

