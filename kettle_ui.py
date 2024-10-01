from tkinter import *
from PIL import Image, ImageTk
from kettle_logic import *
import time

root = Tk()
root.title("Electric Kettle")
root.geometry("700x700")

background_image_path = "Images/bg.jpg"
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

cool_image_path = "cool.png"
warming_image_path = "warming.png"
boiling_image_path = "boiling.png"

cool_image = ImageTk.PhotoImage(Image.open('Images/Cool.png').resize((300, 300), Image.Resampling.LANCZOS))
warming_image = ImageTk.PhotoImage(Image.open('Images/Warm.png').resize((300, 300), Image.Resampling.LANCZOS))
boiling_image = ImageTk.PhotoImage(Image.open('Images/Boil.png').resize((300, 300), Image.Resampling.LANCZOS))

kettle_label = Label(root, image=cool_image)
kettle_label.pack(side=BOTTOM, pady=20)

countdown_label = Label(root, text="Time Remaining: 0 min 0 sec", font=("Arial", 16))
countdown_label.pack(pady=10)


def update_kettle_image(phase):
    if phase == "cool":
        kettle_label.config(image=cool_image)
    elif phase == "warming":
        kettle_label.config(image=warming_image)
    elif phase == "boiling":
        kettle_label.config(image=boiling_image)


def update_countdown(time_left):
    if time_left > 0:
        minutes = int(time_left % 60)
        seconds = int((time_left % 1) * 100)
        countdown_label.config(text=f"Time Remaining: {minutes} min {seconds} sec")
        root.after(1, update_countdown, time_left - 0.0011)  
    else:
        countdown_label.config(text="Boiling complete!")
        time.sleep(2)
        countdown_label.config(text="Time Remaining: 0 min 0 sec")

def calculate_time():
    try:
        current_temp = int(current_temp_entry.get())
        amount_of_water = float(amount_of_water_entry.get())
        desired_temp = 100  # Boiling point in Celsius
        
        power_low, power_medium, power_high = fuzzy_rules_extended_five(current_temp, desired_temp, amount_of_water)
        final_power = defuzzify(power_low, power_medium, power_high)

        temp_difference = desired_temp - current_temp
        if temp_difference <= 0:
            time_to_boil = 0  
        else:
            wattz_power = 2000  
            c = 4.186  # Constant. Heat capacity of water
            time_to_boil = (c * 1000 * amount_of_water * temp_difference) / (wattz_power * final_power / 100 * 60)

        needed_time_label.config(text=f"Estimated time to boil: {time_to_boil:.2f} minutes")
    
        update_countdown(time_to_boil)
        visualize_boiling(time_to_boil)

    except ValueError:
        needed_time_label.config(text="Please enter valid numeric values!")

def visualize_boiling(boiling_time):
    boiling_time_scaled = boiling_time * 1000  
    warming_duration = int(boiling_time_scaled * 0.5)  # 40% warming
    boiling_duration = int(boiling_time_scaled * 0.5)  # 60% boiling

    print(f"Scaled Warming Duration: {warming_duration} ms")
    print(f"Scaled Boiling Duration: {boiling_duration} ms")

    print("Warming phase started")  
    update_kettle_image("warming")
    
    root.after(warming_duration, lambda: start_boiling(boiling_duration))

def start_boiling(boiling_duration):
    print("Boiling phase started")  
    update_kettle_image("boiling")
     
    root.after(boiling_duration, lambda: print("Boiling Done"))
    root.after(boiling_duration, lambda: update_kettle_image("cool"))


current_temp_label = Label(root, text="Current Water Temperature (°C):")
current_temp_label.pack(pady=5)
current_temp_entry = Entry(root)
current_temp_entry.pack(pady=5)

amount_of_water_label = Label(root, text="Amount of Water (liters):")
amount_of_water_label.pack(pady=5)
amount_of_water_entry = Entry(root)
amount_of_water_entry.pack(pady=5)

calculate_button = Button(root, text="Calculate Time to Boil", command=calculate_time)
calculate_button.pack(pady=20)

needed_time_label = Label(root, text="")
needed_time_label.pack(pady=20)

root.mainloop()
