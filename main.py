import json
import tkinter as tk
from tkinter import messagebox,simpledialog
import os
import sys
if getattr(sys,"frozen",False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_NAME=os.path.join(BASE_DIR,"Student Management System")
student_list=[]
root=tk.Tk()
root.geometry("600x600")
root.title("Advanced Student Management System")
is_dark_mode=False
is_search_active=False
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        root.config(bg="white")
        entry_name.config(bg="white",fg="black",insertbackground="black")
        entry_roll.config(bg="white",fg="black",insertbackground="black")
        entry_course.config(bg="white",fg="black",insertbackground="black")
        entry_mark.config(bg="white",fg="black",insertbackground="black")
        box.config(bg="white",fg="black")
        theme_btn.config(text="Dark Mode",bg="white",fg="black")
    else:
        root.config(bg="#1e1e1e")
        entry_name.config(bg="#a0a0a0",fg="white",insertbackground="white")
        entry_roll.config(bg="#a0a0a0",fg="white",insertbackground="white")
        entry_course.config(bg="#a0a0a0",fg="white",insertbackground="white")
        entry_mark.config(bg="#a0a0a0",fg="white",insertbackground="white")
        box.config(bg="#1e1e1e",fg="white")
        theme_btn.config(text="Light Mode",bg="#1e1e1e",fg="white")
    is_dark_mode=not is_dark_mode
    
def save_date():
    try:
        with open(FILE_NAME,"w") as file:
            json.dump(student_list,file,indent=4)
    except Exception as e:
        messagebox.showerror("Error",f"Failed to save file:{e}")
        
def load_date():
    global student_list
    try:
        with open(FILE_NAME,"r") as file:
            student_list=json.load(file)
        update_box()
        update_counter()
    except FileNotFoundError:
        student_list=[]
        
def update_counter():
    total_student=len(student_list)
    counter_label.config(text=f"Total Students : {total_student}")
    
def calculate_performance(marks_str):
    try:
        mark=float(marks_str)
        if mark<0 or mark>100:
            return None
    except ValueError:
        return None
    percentage=mark
    if percentage>=95:
        grade="A+"
    elif percentage>=85:
        grade="A"
    elif percentage>=70:
        grade="B"
    elif percentage>=60:
        grade="C"
    elif percentage>=50:
        grade="D"
    else:
        grade="F"
    status="Pass" if percentage>=50 else "Fail"
    return {"mark":mark,"percentage":percentage,"grade":grade,"status":status}
    
def add_student():
    name=entry_name.get().strip()
    roll_no=entry_roll.get().strip()
    course=entry_course.get().strip()
    mark=entry_mark.get().strip()
    if not name or not roll_no or not course or not mark:
        messagebox.showerror("Error","All fields required!")
        return
    for student in student_list:
        if str(student["roll_no"]).lower()==str(roll_no).lower():
            messagebox.showerror("Error",f"The Student with this roll number '{roll_no}' already exists!")
            return
    perf=calculate_performance(mark)
    if not perf:
        messagebox.showerror("Error","Marks must be valid number between 0 and 100!")
        return None
    student={"name":name,"roll_no":roll_no,"course":course,"mark":perf["mark"],"percentage":perf["percentage"],
    "grade":perf["grade"],"status":perf["status"]}
    student_list.append(student)
    clear_fields()
    update_box()
    save_date()
    messagebox.showinfo("Success",f"Student '{name}' added Successfully")
    
def clear_fields():
    entry_name.delete(0,tk.END)
    entry_roll.delete(0,tk.END)
    entry_course.delete(0,tk.END)
    entry_mark.delete(0,tk.END)
    
def clear_box():
    confirm=messagebox.askyesno("Confirm Deletion","Are you sure you want to delete all students from the list?")
    if confirm:
        box.delete(0,tk.END)
        student_list.clear()
        save_date()
        update_counter()
        
def update_box():
    box.delete(0,tk.END)
    for student in student_list:
        display=(f"ID: {student['roll_no']} | Name: {student['name']} | Course: {student['course']} |"
        f"Grade: {student['grade']} | Status: {student['status']}")
        box.insert(tk.END,display)
        update_counter()
        
def delete_student():
    try:
        selected_box=box.curselection()[0]
        display_text=box.get(selected_box)
        extracted_roll=display_text.split(" | ")[0].replace("ID: ","").strip()
        for index,student in enumerate(student_list):
            if str(student["roll_no"])==extracted_roll:
                student_list.pop(index)
                break
        update_box()
        update_counter()
        save_date()
        messagebox.showinfo("Success","Student record deleted successfully")
    except IndexError:
        messagebox.showerror("Error","Please select a student from a list to delete it!")
        
def search_student():
    global is_search_active
    query=simpledialog.askstring("Search Student","Enter a roll number or name to search student.")
    if not query:
        return 
    query=query.strip().lower()
    found_list=[]
    for student in student_list:
        if (query in str(student["roll_no"]).lower() or query in student["name"].lower()):
            found_list.append(student)
    if found_list:
        box.delete(0,tk.END)
        for student in found_list:
            display=(f"ID: {student['roll_no']} | Name: {student['name']} | Course: {student['course']} |"
            f"Grade: {student['grade']} | Status: {student['status']}")
            box.insert(tk.END,display)
            messagebox.showinfo("Search Success",f"Found {len(found_list)} matching student(s).")
        is_search_active=True
    else:
        messagebox.showerror("Not found","No student found matching that search query!")
        
def edit_student():
    try:
        selected_box=box.curselection()[0]
        display_text=box.get(selected_box)
        extracted_roll=display_text.split(" | ")[0].replace("ID: ","").strip()
        target_idx=-1
        for index,student in enumerate(student_list):
            if str(student["roll_no"])==extracted_roll:
                target_idx=index
                break
        if target_idx !=-1:
            target_student=student_list[target_idx]
            clear_fields()
            entry_name.insert(0,target_student["name"])
            entry_roll.insert(0,target_student["roll_no"])
            entry_course.insert(0,target_student["course"])
            entry_mark.insert(0,str(target_student.get("mark","")).strip())
            student_list.pop(target_idx)
            box.delete(0,tk.END)
            update_box()
            update_counter()
            save_date()
            messagebox.showinfo("Edit Mode","Modify the Fields and click 'Add student' to save changes.")
    except IndexError:
        messagebox.showerror("Error","Please select a student from a list to edit it!")
        
def back_list():
    global is_search_active
    if not is_search_active:
       messagebox.showerror("Error","All students are already showing in the list!")
       return
    try:
        update_box()
        update_counter()
        messagebox.showinfo("Students","All students are now being shown in the list.")
        is_search_active=False
    except Exception:
        messagebox.showerror("Error","Failed to refresh the student list!")
        
def sort_by_name():
    global student_list
    student_list.sort(key=lambda x: x["name"].lower())
    update_box()
    save_date()
    messagebox.showinfo("Sorted student","Students sorted alphabetically by name")
    
def sort_by_roll():
    global student_list
    try:
        student_list.sort(key=lambda x: int(x["roll_no"]))
        update_box()
        save_date()
        messagebox.showinfo("Sorted student","Students sorted by roll number")
    except ValueError:
        messagebox.showerror("Error","Roll number must be digits that should be sorted!")
        
label=tk.Label(root,text="Student Management System",font=("Arial",16,"bold"))
label.pack(pady=10)
frame=tk.Frame(root)
frame.pack(pady=10)
entry_label=tk.Label(frame,text="Name:",font=("Arial",10,"bold"))
entry_label.grid(row=0,column=0,sticky="e",pady=2)
entry_name=tk.Entry(frame,width=30)
entry_name.grid(row=0,column=1,pady=2)
roll_label=tk.Label(frame,text="Roll Number:",font=("Arial",10,"bold"))
roll_label.grid(row=1,column=0,sticky="e",pady=2)
entry_roll=tk.Entry(frame,width=30)
entry_roll.grid(row=1,column=1,pady=2)
course_label=tk.Label(frame,text="Course:",font=("Arial",10,"bold"))
course_label.grid(row=2,column=0,sticky="e",pady=2)
entry_course=tk.Entry(frame,width=30)
entry_course.grid(row=2,column=1,pady=2)
mark_label=tk.Label(frame,text="Marks:",font=("Arial",10,"bold"))
mark_label.grid(row=3,column=0,sticky="e",pady=2)
entry_mark=tk.Entry(frame,width=30)
entry_mark.grid(row=3,column=1,pady=2)
add_btn=tk.Button(frame,text="Add Student",font=("Arial",10,"bold"),bg="royalblue",fg="yellow",command=add_student)
add_btn.grid(row=5,column=0,padx=5,pady=5)
del_btn=tk.Button(frame,text="Delete Student",font=("Arial",10,"bold"),bg="lightblue",fg="black",command=delete_student)
del_btn.grid(row=5,column=2,padx=5,pady=5)
edit_btn=tk.Button(frame,text="Edit Student",font=("Arial",10,"bold"),bg="#2c3e50",fg="white",command=edit_student)
edit_btn.grid(row=5,column=1,padx=5,pady=5)
search_btn=tk.Button(frame,text="Search Student",font=("Arial",10,"bold"),bg="darkgreen",fg="palegreen",command=search_student)
search_btn.grid(row=7,column=0,padx=5,pady=5)
name=tk.Button(frame,text="Sort Student By Name",font=("Arial",10,"bold"),bg="lavender",fg="indigo",command=sort_by_name)
name.grid(row=7,column=1,padx=5,pady=5)
roll=tk.Button(frame,text="Sort Student By Roll Number",font=("Arial",10,"bold"),bg="red",fg="white",command=sort_by_roll)
roll.grid(row=7,column=2,padx=5,pady=5)
clear=tk.Button(frame,text="Clear All List",font=("Arial",10,"bold"),bg="yellow",fg="red",command=clear_box)
clear.grid(row=9,column=0,padx=5,pady=5)
theme_btn=tk.Button(frame,text="Dark Mode",command=toggle_theme,font=("Arial",10,"bold"),bg="white",fg="black")
theme_btn.grid(row=9,column=1,padx=5,pady=5)
back_btn=tk.Button(frame,text="Show All Students",command=back_list,font=("Arial",10,"bold"),bg="purple",fg="yellow")
back_btn.grid(row=9,column=2,padx=5,pady=5)
box=tk.Listbox(root,width=80,height=15,bd=2,font=("Consolas",10))
box.pack(pady=10)
counter_label=tk.Label(root,text="Total Students: 0")
counter_label.pack(pady=10)
load_date()
root.mainloop()
