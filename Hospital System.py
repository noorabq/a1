from tkinter import *
from tkinter import ttk  # Import ttk for themed widgets
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import StringVar
import sqlite3
import tkinter.messagebox

from tkinter import Label, Entry, Button, Toplevel, messagebox

class System:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Hospital Management System")
        self.root.geometry("400x400")
        self.root.configure(background='grey')

        self.conn = sqlite3.connect('Hospital.system.db')
        self.cursor = self.conn.cursor()

        # Create the employees table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.conn.commit()

        # Login Frame
        self.login_frame = Frame(self.root, bd=10, width=400, height=200, padx=20, relief=RIDGE)
        self.login_frame.grid(row=0, column=0, padx=50, pady=50)

        # Add Username and Password Entry
        self.lblUsername = Label(self.login_frame, text="Username:", font=('arial', 12, 'bold'))
        self.lblUsername.grid(row=0, column=0, padx=10, pady=10)
        self.entryUsername = Entry(self.login_frame, font=('arial', 12))
        self.entryUsername.grid(row=0, column=1, padx=10, pady=10)

        self.lblPassword = Label(self.login_frame, text="Password:", font=('arial', 12, 'bold'))
        self.lblPassword.grid(row=1, column=0, padx=10, pady=10)
        self.entryPassword = Entry(self.login_frame, font=('arial', 12), show='*')
        self.entryPassword.grid(row=1, column=1, padx=10, pady=10)

        self.btnLogin = Button(self.login_frame, text="Login", font=('arial', 12, 'bold'), command=self.login)
        self.btnLogin.grid(row=2, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.entryUsername.get()
        password = self.entryPassword.get()

        # Check if the username and password match in the database
        self.cursor.execute('SELECT * FROM employees WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome to the Hospital Management System!")
            # Open the Hospital Management System window after successful login
            self.open_hospital_system()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_hospital_system(self):
        # Open the hospital management system GUI here
        self.root.destroy()  # Close the login window
        root = Tk()
        application = Hospital(root)
        root.mainloop()

class Patient:
    def __init__(self, patient_id, patient_name, appointment_time, is_emergency=False):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.appointment_time = appointment_time
        self.is_emergency = is_emergency
        self.doctor = None
        self.medications = []

class Doctor:
    def __init__(self, doctor_id, doctor_name):
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1350x750")
        self.root.configure(background='powder blue')

        self.conn = sqlite3.connect('Hospital.system.db')
        self.cursor = self.conn.cursor()

        self.emergency_checkbox_var = BooleanVar()
        self.emergency_checkbox_var.set(False)

        self.waiting_list = []
        cmbNameTablets = StringVar()
        Ref = StringVar()
        Dose = StringVar()
        NumberTables = StringVar()
        AppointmentDate = StringVar()
        IssuedDate = StringVar()
        HowtoUseMedication = StringVar()  # Added HowtoUseMedication variable
        Medication = StringVar()
        PatientID = StringVar()
        PatientNHSNo = StringVar()
        PatientName = StringVar()
        DateOfBirth = StringVar()
        PatientAddress = StringVar()
        Prescription = StringVar()
        DoctorName = StringVar()
        self.search_var = StringVar()

        # Create the patients table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference_no TEXT,
                issued_date TEXT,
                appointment_date TEXT,
                patient_id TEXT,
                patient_name TEXT,
                date_of_birth TEXT,
                patient_address TEXT,
                nhs_number TEXT,
                name_of_tablets TEXT,
                no_of_tablets TEXT,
                dose TEXT,
                use_medication_main TEXT,  -- Added use_medication_main field
                use_medication_details TEXT,  -- Added use_medication_details field
                doctor_name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_appointment_date
            ON patients (appointment_date)
        ''')
        
        self.conn.commit()



        #======================================openMedicationWindow=============================================

        def openMedicationWindow():
            # Create a new window for medication details
            medication_window = Toplevel()
            medication_window.title("Medication Details")
            medication_window.geometry("400x300")
            
            # Medication labels and entry widgets in the new window
            lblNameTablet = Label(medication_window, font=('arial', 12, 'bold'), text="Name of Tablets:", padx=2, pady=2)
            lblNameTablet.grid(row=0, column=0, sticky=W)
            cboNameTablet = ttk.Combobox(medication_window, textvariable=cmbNameTablets, state='readonly', font=('arial', 12, 'bold'), width=23)
            cboNameTablet['values'] = ('', 'Ibuprofen', 'Co-codamol', 'Paracetamol', 'Amlodipine','Acetaminophen','Adderall','Amitriptyline','Amlodipine','Amoxicillin','Ativan')
            cboNameTablet.current(0)
            cboNameTablet.grid(row=0, column=1, sticky=W)

            lblNoOfTablets = Label(medication_window, font=('arial', 12, 'bold'), text="No. of Tablets:", padx=2 ,pady=2)
            lblNoOfTablets.grid(row=1, column=0, sticky=W)
            txtNoOfTablets = Entry(medication_window, font=('arial', 12, 'bold'), textvariable=NumberTables, width=25)
            txtNoOfTablets.grid(row=1, column=1)
            
            lblDose = Label(medication_window, font=('arial', 12, 'bold'), text="Dose:", padx=2 , pady=4)
            lblDose.grid(row=2, column=0, sticky=W)
            txtDose = Entry(medication_window, font=('arial', 12, 'bold'), textvariable=Dose, width=25)
            txtDose.grid(row=2, column=1)
            
            lblUseMedication = Label(medication_window, font=('arial', 12, 'bold'), text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=3, column=0, sticky=W)
            txtUseMedication = Entry(medication_window, font=('arial', 12, 'bold'), textvariable=HowtoUseMedication, width=25)
            txtUseMedication.grid(row=3, column=1)

            btnSaveMedication = Button(medication_window, text='Save Medication', font=('arial', 12, 'bold'), width=24, bd=4, command=saveMedication)
            btnSaveMedication.grid(row=4, column=1)

        def saveMedication():
            name_tablets = cmbNameTablets.get()
            no_of_tablets = NumberTables.get()
            dose = Dose.get()
            use_medication_details = HowtoUseMedication.get()  # Changed variable name

            self.cursor.execute('''
                INSERT INTO patients (name_of_tablets, no_of_tablets, dose, use_medication_details)
                VALUES (?, ?, ?, ?)
            ''', (name_tablets, no_of_tablets, dose, use_medication_details))


            self.conn.commit()
            tkinter.messagebox.showinfo("Success", "Medication details saved successfully!")


        #=============================================iExit==============================================

        
        def iExit():
            iExit=tkinter.messagebox.askyesno("Hospital Managment System","Confirm if you want to exit")
            if iExit>0:
                root.destroy()
                return
            
        #=============================================iPrescription==============================================


        def iPrescription():

            # Get data from entry widgets
            reference_no = Ref.get()
            issued_date = IssuedDate.get()
            appointment_date = AppointmentDate.get()
            patient_id = PatientID.get()
            patient_name = PatientName.get()
            date_of_birth = DateOfBirth.get()
            patient_address = PatientAddress.get()
            nhs_number = PatientNHSNo.get()
            name_of_tablets = cmbNameTablets.get()
            no_of_tablets = NumberTables.get()
            dose = Dose.get()
            Howtossemedication = HowtoUseMedication.get()  # Changed variable name or name it usemedication details
            doctor_name = DoctorName.get()
            use_medication_main=Medication.get()
            


            self.cursor.execute('''
            INSERT INTO patients (
            reference_no, issued_date, appointment_date, patient_id, patient_name, date_of_birth,
            patient_address, nhs_number, name_of_tablets, no_of_tablets, dose,use_medication_main, use_medication_details, doctor_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reference_no, issued_date, appointment_date, patient_id, patient_name, date_of_birth,
                patient_address, nhs_number, name_of_tablets, no_of_tablets, dose,use_medication_main, Howtossemedication,doctor_name
            ))
            self.conn.commit()

            prescription_data = (
            f"Reference No: {reference_no}\n"
            f"Issued Date: {issued_date}\n"
            f"Appointment Date: {appointment_date}\n"
            f"Patient ID: {patient_id}\n"
            f"Patient Name: {patient_name}\n"
            f"Date of Birth: {date_of_birth}\n"
            f"Patient Address: {patient_address}\n"
            f"NHS Number: {nhs_number}\n"
            f"Name of Tablets: {name_of_tablets}\n"
            f"No. of Tablets: {no_of_tablets}\n"
            f"Dose: {dose}\n"
            f"Medication: {Howtossemedication}\n"
            f"Doctor Name: {doctor_name}\n\n"
            )
            self.textPrescription.insert(END, prescription_data)

            self.textFrameDetail.insert(END, f"\t{Medication.get()}\t\t\n")
        
        #=============================================iDelete==============================================
        
        def iDelete():

            Ref.set("")
            DoctorName.set("")
            NumberTables.set("")
            Dose.set("")
            AppointmentDate.set("")
            IssuedDate.set("")
            PatientID.set("")
            PatientNHSNo.set("")
            PatientName.set("")
            DateOfBirth.set("")
            PatientAddress.set("")
            Prescription.set("")
            Medication.set("")
            HowtoUseMedication.set("")
            self.textPrescription.delete("1.0",END)
            self.textFrameDetail.delete("1.0",END)

            return

        #=============================================iReset==============================================
        def iReset():

            Ref.set("")
            DoctorName.set("")
            Dose.set("")
            NumberTables.set("")
            AppointmentDate.set("")
            IssuedDate.set("")
            PatientID.set("")
            PatientNHSNo.set("")
            PatientName.set("")
            DateOfBirth.set("")
            PatientAddress.set("")
            Prescription.set("")
            Medication.set("")
            HowtoUseMedication.set("")
            self.textPrescription.delete("1.0",END)
            self.textFrameDetail.delete("1.0",END)

            return
        
        #=============================================OpenAddPatientWindow==============================================
        
        def add_patient():
            patient_id = self.entryPatientID.get()
            patient_name = self.entryPatientName.get()
            appointment_time = self.entryAppointmentTime.get()
            is_emergency = self.emergency_checkbox_var.get()

            if patient_id and patient_name and appointment_time:
                new_patient = Patient(patient_id, patient_name, appointment_time, is_emergency=is_emergency)
                self.waiting_list.append(new_patient)
                messagebox.showinfo("Success", "Patient added to waiting list!")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
            
            return
       
        def remove_patient():
            if self.waiting_list:
                removed_patient = self.waiting_list.pop(0)
                messagebox.showinfo("Success", f"Patient {removed_patient.patient_name} removed from waiting list.")
            else:
                messagebox.showinfo("Info", "No patients in the waiting list.")

            return
                        
        def OpenAddPatientWindow():

            add_patient_window = Toplevel()
            add_patient_window.title("Add Patient")
            add_patient_window.geometry("400x200")

            lblTitle = Label(add_patient_window, text="Add New Patient", font=('arial', 14, 'bold'))
            lblTitle.pack()

            lblPatientID = Label(add_patient_window, text="Patient ID:")
            lblPatientID.pack()
            self.entryPatientID = Entry(add_patient_window)
            self.entryPatientID.pack()

            lblPatientName = Label(add_patient_window, text="Patient Name:")
            lblPatientName.pack()
            self.entryPatientName = Entry(add_patient_window)
            self.entryPatientName.pack()

            lblAppointmentTime = Label(add_patient_window, text="Arrivel Time:")
            lblAppointmentTime.pack()
            self.entryAppointmentTime = Entry(add_patient_window)
            self.entryAppointmentTime.pack()

            emergency_checkbox = Checkbutton(add_patient_window, text="Emergency Patient",
                                            variable=self.emergency_checkbox_var, onvalue=True, offvalue=False)
            emergency_checkbox.pack()

            btnAdd = Button(add_patient_window, text="Add Patient", command=add_patient)
            btnAdd.pack()

            return
        
        #=============================================OpenWaitingRoom==============================================

        def OpenWaitingRoom():
            waiting_window = Toplevel()
            waiting_window.title("Waiting Room List")
            waiting_window.geometry("600x400")

            lblTitle = Label(waiting_window, text="Patients Waiting for Consultation", font=('arial', 14, 'bold'))
            lblTitle.pack()

            lbl_header = Label(waiting_window, text="Patient ID | Name | Appointment Time | Emergency |  Doctor | ")
            lbl_header.pack()

            for idx, patient in enumerate(self.waiting_list, start=1):
                patient_info = f"{patient.patient_id} | {patient.patient_name} | {patient.appointment_time} | " \
                           f"{patient.is_emergency} | {patient.doctor.doctor_name if patient.doctor else 'Not assigned'} | " 
                lbl_patient_info = Label(waiting_window, text=patient_info)
                lbl_patient_info.pack()

            btn_remove_patient = Button(waiting_window, text="Remove Patient", command=remove_patient)
            btn_remove_patient.pack()

        
        #=============================================OpenUpdateWindow==============================================


        def OpenUpdateWindow():
            Update_window = Toplevel()
            Update_window.title("Update Details")
            Update_window.geometry("800x250")

            lblRef = Label(Update_window, font=('arial', 12, 'bold'), text="Reference No:", padx=2 , pady=2)
            lblRef.grid(row=0, column=0)
            txtRef = Entry(Update_window, font=('arial', 12, 'bold'),textvariable=Ref, width=25)
            txtRef.grid(row=0, column=1)

            lblPatientID = Label(Update_window, font=('arial', 12, 'bold'), text="Patient ID:", padx=2, pady=2)
            lblPatientID.grid(row=0, column=2)
            txtPatientID = Entry(Update_window, font=('arial', 12, 'bold'), textvariable=PatientID, width=25)
            txtPatientID.grid(row=0, column=3)

            lblNHSNumber = Label(Update_window, font=('arial', 12, 'bold'), text="NHS Number:", padx=2, pady=2)
            lblNHSNumber.grid(row=1, column=0)
            txtNHSNumber = Entry(Update_window, font=('arial', 12, 'bold'),textvariable=PatientNHSNo , width=25)
            txtNHSNumber.grid(row=1, column=1)

            lblPatientName = Label(Update_window, font=('arial', 12, 'bold'), text="Patient Name:", padx=2, pady=2)
            lblPatientName.grid(row=1, column=2)
            txtPatientName = Entry(Update_window, font=('arial', 12, 'bold'),textvariable=PatientName , width=25)
            txtPatientName.grid(row=1, column=3)

            lblDateOfBirth = Label(Update_window, font=('arial', 12, 'bold'), text="Date Of Birth:", padx=2, pady=2)
            lblDateOfBirth.grid(row=2, column=0)
            txtDateOfBirth = DateEntry(Update_window, font=('arial', 12, 'bold'), textvariable=DateOfBirth, width=23)
            txtDateOfBirth.grid(row=2, column=1)

            lblPatientAddress = Label(Update_window, font=('arial', 12, 'bold'), text="Patient Address:", padx=2, pady=2)
            lblPatientAddress.grid(row=2, column=2)
            txtPatientAddress= Entry(Update_window, font=('arial', 12, 'bold'),textvariable=PatientAddress , width=25)
            txtPatientAddress.grid(row=2, column=3)

            lblIssuedDate = Label(Update_window, font=('arial', 12, 'bold'), text="Issued Date:", padx=2, pady=2)
            lblIssuedDate.grid(row=3, column=0)
            txtIssuedDate = DateEntry(Update_window, font=('arial', 12, 'bold'), textvariable=IssuedDate, width=23)
            txtIssuedDate.grid(row=3, column=1)

            lblAppointmentDate = Label(Update_window, font=('arial', 12, 'bold'), text="AppointmentDate", padx=2, pady=2)
            lblAppointmentDate.grid(row=3, column=2)
            txtAppointmentDate = DateEntry(Update_window, font=('arial', 12, 'bold'), textvariable=AppointmentDate, width=23)
            txtAppointmentDate.grid(row=3, column=3)

            lblDoctorName= Label(Update_window, font=('arial', 12, 'bold'), text="  Doctor Name:", padx=2 ,pady=2)
            lblDoctorName.grid(row=4, column=0)
            txtDoctorName = Entry(Update_window, font=('arial', 12, 'bold'),textvariable=DoctorName , width=25)
            txtDoctorName.grid(row=4, column=1)

            lblNameTablet = Label(Update_window, font=('arial', 12, 'bold'), text="Name of Tablets:", padx=2, pady=2)
            lblNameTablet.grid(row=4, column=2, sticky=W)
            cboNameTablet = ttk.Combobox(Update_window, textvariable=cmbNameTablets, state='readonly', font=('arial', 12, 'bold'), width=23)
            cboNameTablet['values'] = ('', 'Ibuprofen', 'Co-codamol', 'Paracetamol', 'Amlodipine','Acetaminophen','Adderall','Amitriptyline','Amlodipine','Amoxicillin','Ativan')
            cboNameTablet.current(0)
            cboNameTablet.grid(row=4, column=3, sticky=W)

            lblNoOfTablets = Label(Update_window, font=('arial', 12, 'bold'), text="No. of Tablets:", padx=2 ,pady=2)
            lblNoOfTablets.grid(row=5, column=0, sticky=W)
            txtNoOfTablets = Entry(Update_window, font=('arial', 12, 'bold'), textvariable=NumberTables, width=25)
            txtNoOfTablets.grid(row=5, column=1)
            
            lblDose = Label(Update_window, font=('arial', 12, 'bold'), text="Dose:", padx=2 , pady=4)
            lblDose.grid(row=5, column=2, sticky=W)
            txtDose = Entry(Update_window, font=('arial', 12, 'bold'), textvariable=Dose, width=25)
            txtDose.grid(row=5, column=3)
            
            lblUseMedication = Label(Update_window, font=('arial', 12, 'bold'), text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=6, column=0, sticky=W)
            txtUseMedication = Entry(Update_window, font=('arial', 12, 'bold'), textvariable=HowtoUseMedication, width=25)
            txtUseMedication.grid(row=6, column=1)
            

            lblUseMedication = Label(Update_window, font=('arial', 12, 'bold'), text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=6, column=2)
            txtUseMedication = Entry(Update_window, font=('arial', 12, 'bold'),textvariable=Medication , width=25)
            txtUseMedication.grid(row=6, column=3)
            # Set initial text for the text box

            btnUpdate = Button(Update_window, text='Update', font=('arial', 12, 'bold'), width=24, bd=4, command=iUpdate)
            btnUpdate.grid(row=10, column=1)
            return
        
        def iUpdate():
            patient_id =PatientID.get()
            patient_name =PatientName.get()
            date_of_birth =DateOfBirth.get()
            patient_address = PatientAddress.get()
            nhs_number =PatientNHSNo.get()
            name_of_tablets =cmbNameTablets.get()
            no_of_tablets = NumberTables.get()
            dose = Dose.get()
            use_medication_main = HowtoUseMedication.get()
            doctor_name = DoctorName.get()
            appointment_date = AppointmentDate.get()

            # Check if patient_id exists
            self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Update the record
                self.cursor.execute('''
                    UPDATE patients SET
                    patient_name = ?,
                    date_of_birth = ?,
                    patient_address = ?,
                    nhs_number = ?,
                    name_of_tablets = ?,
                    no_of_tablets = ?,
                    dose = ?,
                    use_medication_main = ?,
                    doctor_name = ?,
                    appointment_date = ?
                    WHERE patient_id = ?
                ''', (patient_name, date_of_birth, patient_address, nhs_number, name_of_tablets,
                    no_of_tablets, dose, use_medication_main, doctor_name, appointment_date, patient_id))
                self.conn.commit()
                tkinter.messagebox.showinfo("Success", "Patient record updated successfully!")
            else:
                tkinter.messagebox.showerror("Error", "Patient ID not found!")

            return   
        #=============================================search==============================================
        def search():
            search_window = Toplevel()
            search_window.title("search Details")
            search_window.geometry("800x250")
            self.lblSearch = Label(search_window, text="Enter Patient ID:")
            self.lblSearch.pack()

            self.entrySearch = Entry(search_window, textvariable=self.search_var)
            self.entrySearch.pack()

            self.btnSearch = Button(search_window, text="Search", command=search_patient)
            self.btnSearch.pack()
            return
        
        def search_patient():
            patient_id = self.search_var.get()

            # Check if patient ID is provided
            if not patient_id:
                messagebox.showerror("Error", "Please enter a patient ID.")
                return

            # Search for patient in the database
            self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            patient_record = self.cursor.fetchone()

            if not patient_record:
                messagebox.showinfo("Info", "Patient not found.")
                return
            # Display patient details in a new window
            display_patient_summary(patient_record)
            return
    
        def display_patient_summary(patient_record):
            # Create a new window for displaying patient summary
            summary_window = Toplevel(self.root)
            summary_window.title("Patient Summary")
            summary_window.geometry("600x400")

            # Display patient details using labels and text boxes
            lblPatientID = Label(summary_window, text="Patient ID:")
            lblPatientID.grid(row=0, column=0)
            txtPatientID = Entry(summary_window)
            txtPatientID.insert(0, patient_record[4])
            txtPatientID.grid(row=0, column=1)

            lblPatientName = Label(summary_window, text="Patient Name:")
            lblPatientName.grid(row=1, column=0)
            txtPatientName = Entry(summary_window)
            txtPatientName.insert(0, patient_record[5])
            txtPatientName.grid(row=1, column=1)

            lblAppointmentTime = Label(summary_window, text="Appointment Time:")
            lblAppointmentTime.grid(row=2, column=0)
            txtAppointmentTime = Entry(summary_window)
            txtAppointmentTime.insert(0, patient_record[3])
            txtAppointmentTime.grid(row=2, column=1)

            lblDoctorName = Label(summary_window, text="Doctor Name:")
            lblDoctorName.grid(row=3, column=0)
            txtDoctorName = Entry(summary_window)
            txtDoctorName.insert(0, patient_record[14])
            txtDoctorName.grid(row=3, column=1)

            lblMedications = Label(summary_window, text="Medications:")
            lblMedications.grid(row=4, column=0)
            txtMedications = Text(summary_window, height=5, width=50)
            txtMedications.insert(END, patient_record[12])
            txtMedications.grid(row=4, column=1)
        
        #===========================================frame=========================================================
        MainFrame = Frame(self.root)
        MainFrame.grid()

        TitleFrame = Frame(MainFrame, bd=20, width=1350, padx=20, relief=RIDGE)
        TitleFrame.pack(side=TOP)

        self.lblTitle = Label(TitleFrame, font=('arial', 40, 'bold'), text="Hospital Management System", padx=2)
        self.lblTitle.grid()

        FrameDetail = Frame(MainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE)
        FrameDetail.pack(side=BOTTOM)

        ButtonFrame = Frame(MainFrame, bd=20, width=1350, height=50, padx=20, relief=RIDGE)
        ButtonFrame.pack(side=BOTTOM)

        DataFrame = Frame(MainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE)
        DataFrame.pack(side=BOTTOM)

        DataFrameLEFT = LabelFrame(DataFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE
                              , font=('arial', 12, 'bold'), text="Patient Information:",)
        DataFrameLEFT.pack(side=LEFT)

        DataFrameRIGHT = LabelFrame(DataFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE
                                    , font=('arial', 12, 'bold'), text="Prescription:",)
        DataFrameRIGHT.pack(side=RIGHT)

        #=============================================DataFrameLEFT==============================================


        self.lblRef = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Reference No:", padx=2 , pady=2)
        self.lblRef.grid(row=0, column=0)
        self.txtRef = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=Ref, width=25)
        self.txtRef.grid(row=0, column=1)


        self.lblIssuedDate = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Issued Date:", padx=2, pady=2)
        self.lblIssuedDate.grid(row=0, column=2)
        self.txtIssuedDate = DateEntry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable=IssuedDate, width=23)
        self.txtIssuedDate.grid(row=0, column=3)


        self.lblAppointmentDate = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="AppointmentDate", padx=2, pady=2)
        self.lblAppointmentDate.grid(row=1, column=0)
        self.txtAppointmentDate = DateEntry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable=AppointmentDate, width=23)
        self.txtAppointmentDate.grid(row=1, column=1)


        self.lblPatientID = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Patient ID:", padx=2, pady=2)
        self.lblPatientID.grid(row=1, column=2)
        self.txtPatientID = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=PatientID , width=25)
        self.txtPatientID.grid(row=1, column=3)

        
        self.lblPatientName = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Patient Name:", padx=2, pady=2)
        self.lblPatientName.grid(row=2, column=0)
        self.txtPatientName = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=PatientName , width=25)
        self.txtPatientName.grid(row=2, column=1)


        self.lblDateOfBirth = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Date Of Birth:", padx=2, pady=2)
        self.lblDateOfBirth.grid(row=2, column=2)
        self.txtDateOfBirth = DateEntry(DataFrameLEFT, font=('arial', 12, 'bold'), textvariable=DateOfBirth, width=23)
        self.txtDateOfBirth.grid(row=2, column=3)


        self.lblPatientAddress = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Patient Address:", padx=2, pady=2)
        self.lblPatientAddress.grid(row=3, column=0)
        self.txtPatientAddress= Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=PatientAddress , width=25)
        self.txtPatientAddress.grid(row=3, column=1)

        
        self.lblNHSNumber = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="NHS Number:", padx=2, pady=2)
        self.lblNHSNumber.grid(row=3, column=2)
        self.txtNHSNumber = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=PatientNHSNo , width=25)
        self.txtNHSNumber.grid(row=3, column=3)
        

        self.lblUseMedication = Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="Use Medication:", padx=2, pady=2)
        self.lblUseMedication.grid(row=4, column=0)
        self.txtUseMedication = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=Medication , width=25)
        self.txtUseMedication.grid(row=4, column=1)
        # Set initial text for the text box
        


        self.lblDoctorName= Label(DataFrameLEFT, font=('arial', 12, 'bold'), text="  Doctor Name:", padx=2 ,pady=2)
        self.lblDoctorName.grid(row=4, column=2)
        self.txtDoctorName = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),textvariable=DoctorName , width=25)
        self.txtDoctorName.grid(row=4, column=3)



        
        #====================================DataFrameRIGHT=====================================================================
        
        self.textPrescription=Text(DataFrameRIGHT, font=('arial', 12, 'bold'),width=43, height=14, padx=2, pady=2)
        self.textPrescription.grid(row=0, column=0)



        #=====================================ButtonFrame==================================================================

        self.btnPrescription=Button(ButtonFrame,text='Prescription', font=('arial', 12, 'bold'),width=24 ,bd=4
                                    ,command=iPrescription)
        self.btnPrescription.grid(row=0, column=0)

        self.btnPrescription=Button(ButtonFrame,text='Medication Details', font=('arial', 12, 'bold'),width=24 ,bd=4,
                                     command=openMedicationWindow)
        self.btnPrescription.grid(row=0, column=1)


        self.btnDelete=Button(ButtonFrame,text='Delete', font=('arial', 12, 'bold'),width=24 ,bd=4
                              ,command=iDelete)
        self.btnDelete.grid(row=0, column=2)

        self.btnReset=Button(ButtonFrame,text='Reset', font=('arial', 12, 'bold'),width=24 ,bd=4
                             ,command=iReset)
        self.btnReset.grid(row=0, column=3)
        
        self.btnExit=Button(ButtonFrame,text='Exit', font=('arial', 12, 'bold'),width=24 ,bd=4
                            ,command=iExit)
        self.btnExit.grid(row=0, column=4)

        self.btnUpdate=Button(ButtonFrame,text='Update', font=('arial', 12, 'bold'),width=24 ,bd=4
                            ,command=OpenUpdateWindow)
        self.btnUpdate.grid(row=1, column=0)

        self.btnAddPatient=Button(ButtonFrame,text='Add Patient', font=('arial', 12, 'bold'),width=24 ,bd=4
                            ,command=OpenAddPatientWindow)
        self.btnAddPatient.grid(row=1, column=1)

        self.btnWaitingRoom=Button(ButtonFrame,text='WaitingRoom', font=('arial', 12, 'bold'),width=24 ,bd=4
                            ,command=OpenWaitingRoom)
        self.btnWaitingRoom.grid(row=1, column=2)

        self.btnSearch = Button(ButtonFrame, text='Search for patient', font=('arial', 12, 'bold'), width=24, bd=4,
                                command=search)
        self.btnSearch.grid(row=1, column=3)

        
        #=====================================FrameDetail=======================================================================

        self.lblLabel = Label(FrameDetail, font=('arial', 10, 'bold'), pady=4, padx=2,
                              text="Type of medical condition/Does the patient use medications?")
        self.lblLabel.grid(row=0, column=0)

        self.textFrameDetail=Text(FrameDetail,font=('arial', 12, 'bold'),width=141, height=4, padx=2, pady=4)
        self.textFrameDetail.insert(END, f"\t{Medication.get()}\t\t\n")   
        self.textFrameDetail.grid(row=1, column=0)


if __name__ == '__main__':

    root = Tk()
    application = System(root)
    root.mainloop()
