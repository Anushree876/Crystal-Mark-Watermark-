import PIL.Image as pil_image
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog,messagebox

background='#F2F2F2'
font=("Georgia",10,"normal")

actual_img_pil=None
watermark_img_pil=None
final_img=None


def open_image_file():
    global actual_img_pil
    file_path=filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files","*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    # path = r"C:\Users\abhig\OneDrive\Desktop\Photos\contact_bg.jpg"
    if file_path:
        actual_img_pil = pil_image.open(file_path)
        max_size=(400,400)
        actual_img_pil.thumbnail(max_size)
        # actual_img=ImageTk.PhotoImage(actual_img_pil)
        # img_label.config(image=actual_img)
        update_preview()

def open_watermark_image():
    global watermark_img_pil
    file_path=filedialog.askopenfilename(
        title="Select the image.",
        filetypes=[("Image files","*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        watermark_img_pil=pil_image.open(file_path)
        max_size=(100,100)
        watermark_img_pil.thumbnail(max_size)
        # watermark_img=ImageTk.PhotoImage(watermark_img_pil)
        #
        # watermark_label.config(image=watermark_img)
        # watermark_label.image=watermark_img
        update_preview()

def calculate_position(base_size,wm_size,position,margin=10):
    base_w,base_h=base_size
    wm_w,wm_h=wm_size

    if position=="top-left":
        return(margin,margin)
    elif position=="top-right":
        return(base_w-wm_w-margin,margin)
    elif position=="bottom-left":
        return(margin,base_h-wm_h-margin)
    elif position=="bottom-right":
        return(base_w-wm_w-margin, base_h-wm_h-margin)
    elif position=="center":
        return((base_w - wm_w) // 2 , ((base_h-wm_h))//2)
    elif position=="center-left":
        return (margin, (base_h - wm_h) // 2)
    elif position == "center-right":
        return (base_w - wm_w - margin, (base_h - wm_h) // 2)
    elif position == "center-top":
        return ((base_w - wm_w) // 2, margin)
    elif position == "center-bottom":
        return ((base_w - wm_w) // 2, base_h - wm_h - margin)
    else:
        # Default to bottom-right
        return (base_w - wm_w - margin, base_h - wm_h - margin)

def update_preview():
    global final_img

    if actual_img_pil is None:
        return
    base=actual_img_pil.copy()
    if watermark_img_pil :
        position_text=position_var.get()
        position=calculate_position(base.size,watermark_img_pil.size,position_text)
        base.paste(watermark_img_pil,position,watermark_img_pil)
    final_img=base

    preview_img=ImageTk.PhotoImage(base)
    img_label.config(image=preview_img)
    img_label.image=preview_img

def position_change():
    update_preview()
def save_image():
    if final_img is None:
        return
    save_path=filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image","*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
    )
    if save_path:
        final_img.convert("RGB").save(save_path)
        messagebox.showinfo("Saved",f"Saved to : \n{save_path}")



window=Tk()
window.title("watermark")

window.config(padx=50,pady=10,bg=background)


title_label=Label(window,text="CrystalMark",bg=background,font=("Georgia",25,"normal"))
title_label.grid(column=1,row=0,columnspan=3,pady=20)

image_button=Button(text="Select base Image",width=25,height=1,command=open_image_file,font=font)
image_button.grid(column=0,row=1,padx=10)

water_image_button=Button(text="Select watermark image ",width=25,height=1,command=open_watermark_image,font=font)
water_image_button.grid(column=2,row=1,padx=10)


save_button=Button(text="Save",command=save_image,width=25,height=1,font=font)
save_button.grid (column=4,row=1,padx=10)

position_label=Label(text="Position : ",bg=background,font=font)
position_label.grid(column=0,row=2)

img_label=Label(window,bg=background)
img_label.grid(column=2,row=5)


position_var=StringVar(value="bottom-right")
positions=[
    "top-left","top-right","bottom-left","bottom-right","center","center-left","center-right",
    "center-top","center-bottom"
]
for idx,pos in enumerate(positions):
    rb=Radiobutton(window,text=pos,variable=position_var,value=pos,command=position_change,bg=background,font=font)
    rb.grid(column=1+idx % 3, row=2+idx//3,sticky="w", padx=5,pady=5)

window.mainloop()

