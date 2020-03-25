import sqlite3
import hashlib
db_file_path='./hospital.db'
conn=sqlite3.connect(db_file_path)
c=conn.cursor()
conn.text_factory=str
conn.row_factory=sqlite3.Row
c=conn.cursor()




class Doctor:
    def __init__(self):
        return None

    def getPatient(self,hcno):

        #printing out the list of all the charts
        #gets all the chart_ids
        c.execute('SELECT chart_id FROM charts ORDER BY adate')
        chart_ids = [row[0] for row in c.fetchall()] #this seems to get rid of the commas at the end

        #gets all the charts ordered by adate
        c.execute('SELECT * FROM charts ORDER BY adate')
        chart_list = c.fetchall()

        #go through all the charts
        for row in chart_list:
            if row['hcno']==hcno and row['edate']=='NULL':
                print row
                print 'status: OPEN'
            elif row['hcno']==hcno and row['edate'] != 'NULL':
                print row
                print 'status: Closed'

                
        #gets user's chart choice
        #input_chart_id = str(raw_input("\nEnter a chart_id that you would like to view\n"))
         #gets the chart to find the hcno numbe
         #gets user's chart choice
        input_chart_id = str(raw_input("\nEnter a chart_id that you would like to view\n"))
        c.execute("SELECT * FROM  charts Where chart_id == '%s'" %input_chart_id)
        c.execute('select * from charts NOCASE;')
        x=c.fetchall()
        for the in x:
            if the[0] == input_chart_id:

                print "\n\nSYMPTOMS"
                print "--------"
                for row in c.execute("SELECT symptom FROM symptoms Where chart_id LIKE '%s' ORDER BY obs_date" %input_chart_id):
                    print row[0]
                print "\nDIAGNOSES"
                print "---------"
                for row in c.execute("SELECT diagnosis FROM diagnoses Where chart_id LIKE '%s' ORDER BY ddate" %input_chart_id):
                    print row[0]
                print "\nMEDICATIONS"
                print "-----------"
                for row in c.execute("SELECT drug_name  FROM medications Where chart_id LIKE '%s' ORDER BY mdate" %input_chart_id):
                    print row[0]
                print "\n"
                
                return 
        
        print "Invalid Chart ID"
        return 
    def addSymptom(self,hcno,staff_id):
        c.execute("select * from charts NOCASE; ")
        things=c.fetchall()
        for r in things:
            if r['hcno']== hcno and r['edate']=='NULL':
                chart_id= r['chart_id']
                symptom=str(raw_input('Please eneter symptom: '))
                date= "DATETIME('now','localtime')"
                values=[(hcno,chart_id,staff_id, symptom)]
                c.executemany("Insert into symptoms values (?,?,?,DATETIME('now','localtime'),?)",values)
                conn.commit()
                
                return
    
            
        print('Chart or patient does not exist')
            
        return hcno, staff_id
    def addDiagnosis(self, hcno,staff_id):
        c.execute("select * from charts NOCASE; ")
        things=c.fetchall()
        for r in things:
            if r['hcno']== hcno and r['edate']=='NULL':
                chart_id= r['chart_id']
                symptom=str(raw_input('Please eneter diagnosis: '))
                date= "DATETIME('now','localtime')"
                values=[(hcno,chart_id,staff_id, symptom)]
                c.executemany("Insert into diagnoses values (?,?,?,DATETIME('now','localtime'),?)",values)
                conn.commit()
                
                return
    
            
        print('Chart or patient does not exist')        
        #adds entry to patient diagnosis
        
        return hcno,staff_id 
    def addMedications(self, hcno,staff_id):
        c.execute('select * from charts NOCASE; ')
        some=c.fetchall()
        for h in some:
            if h['hcno'] == hcno and h['edate'] =='NULL':
                print 'chart exists'
                chart_id=h['chart_id']
                medication= str(raw_input('Please enter medication name: '))
                amount= int(raw_input('Please enter amount of medication: '))
                c.execute('select * from patients where hcno=?',(hcno,))
                p=c.fetchall()
                for age in p:
                    age_group=age['age_group']
                c.execute('select * from dosage;')
                l=c.fetchall()
                for comp in l:
                    if comp['drug_name'] == medication and comp['age_group'] == age_group and comp[2] < amount:
                        print 'Warning Exceeding Suggested Amount. The suggested amount for the patients age is', comp[2]
                        cont=str(raw_input('Would you like to prescribe anyway? Y/N: '))
                        if cont=='y' or cont == 'Y':
                            break
                        elif cont=='n' or cont=='N':
                            return
                
                c.execute('Select * from reportedallergies where hcno=?',(hcno,))
                drug=c.fetchall()
                for it in drug:
                    drugal=it['drug_name']
                    if drugal == medication:
                        print 'Warning patient has reported allergy'
                        return
            
                c.execute('select * from inferredallergies where alg=?',(drugal,))
                inferredal = c.fetchall()
                for possible in inferredal:
                    if possible['canbe_alg'] == medication:
                        print 'Warning ', possible['canbe_alg'], 'is an inffered allergy from the reported allergy', drugal
                        return
                start=str(raw_input('Please enter start date in format YYYY-MM-DD HH:MM:SS '))
                end=str(raw_input('Please enter end date in the format YYYY-MM-DD HH:MM:SS '))
                values=[(hcno,chart_id, staff_id,start,end,amount,medication)]
                c.executemany("Insert into medications values(?,?,?,DATETIME('now','localtime'),?,?,?,?)",values)
                #print hcno, chart_id, staff_id, amount, medication
                conn.commit()
                return
        print 'Patient or chart does not exist'
        return hcno, staff_id
    


class Nurse:
    def __init__(self):
        return None
#Creates Chart
    def create_chart(self,hcno):
        c.execute("Select * From charts NOCASE; ")
        run= c.fetchall()
        #Checks if chart exists
        for row in run:
            
            if row['hcno']== hcno and row['edate'] == 'NULL':
                print  "Chart already exists"
                option=str(raw_input('Would you like to close this chart? Y/N '))
                if option == "Y" or option=='y':
    
                    c.execute("UPDATE charts SET edate = DATETIME('now','localtime') Where hcno = ?",(hcno,))
                    return
                elif option=='N' or option=='n':
                    return
    
        #Creates new chart    
        chart_id=str(raw_input('Enter chart_id: '))
        patient_info=hcno
        edate='NULL'
        info= [(chart_id,hcno,edate)]
        try:
            c.executemany("Insert into charts Values(?,?,DATETIME('now','localtime'),?)", info)
            conn.commit()
        except:
            print "This chart may already exist/Invalid Chart ID, Please try again\n"
            return
        #check if patients exist
        c.execute('Select * from patients; ')
        red= c.fetchall()
        for stuff in red:
            if stuff['hcno'] == hcno:
                return
        name=str(raw_input('Enter patients name: '))
        age_group= str(raw_input('Enter patients age group: '))
        add=str(raw_input('Enter patients address: '))
        phone=str(raw_input('Enter patients phone: '))
        emg_phone= str(raw_input('Enter patints emergency number: '))
        patient_stuff= [(hcno,name,age_group,add,phone,emg_phone)]
        try:
            c.executemany("Insert into patients values(?,?,?,?,?,?)", patient_stuff)
            conn.commit()
        except:
            print "This chart may already exist/Invalid Chart ID, Please try again\n"
            return

        return hcno
#closes chart
    def close_chart(self,hcno):
        c.execute('Select * from charts NOCASE')
        ok=c.fetchall()
        for things in ok:
            if things['hcno']== hcno and things['edate'] == 'NULL':
                c.execute("UPDATE charts SET edate = DATETIME('now','localtime') Where hcno = ?",(hcno,))
                print 'Chart closed'
                return
        print 'No chart to close'

                            
        return hcno
    def addSymptom(self,hcno,staff_id):
        c.execute("select * from charts NOCASE; ")
        things=c.fetchall()
        for r in things:
            if r['hcno']== hcno and r['edate']=='NULL':
                chart_id= r['chart_id']
                symptom=str(raw_input('Please eneter symptom: '))
                date= "DATETIME('now','localtime')"
                values=[(hcno,chart_id,staff_id, symptom)]
                c.executemany("Insert into symptoms values (?,?,?,DATETIME('now','localtime'),?)",values)
                conn.commit()
                
                return
    
            
        print('Chart or patient does not exist')
        return hcno,staff_id
    def getPatient(self):
        #returns patient info sorted by a date
        con = sqlite3.connect('hospital.db') #opens the database file
        con.execute('PRAGMA forteign_keys=ON; ')
        con.text_factory = str #this gets rid of the u in front.
        c = con.cursor()  
        
        #printing out the list of all the charts
        #gets all the chart_ids
        c.execute('SELECT chart_id FROM charts ORDER BY adate')
        chart_ids = [row[0] for row in c.fetchall()] #this seems to get rid of the commas at the end

        #gets all the charts ordered by adate
        c.execute('SELECT * FROM charts ORDER BY adate')
        chart_list = c.fetchall()

        
        print "available charts:"
        print (" chart_id   hcno     adate         edate")
        #go through all the charts
        for num in range(0,len(chart_list)):
            if chart_list[num][3]=='NULL':
                print "%s %s chart is open" % (chart_list[num], chart_list[num][0])
            else:
                print "%s %s chart is closed" % (chart_list[num], chart_list[num][0])

                
        #gets user's chart choice
        input_chart_id = str(raw_input("\nEnter a chart_id that you would like to view\n"))
        c.execute("SELECT * FROM  charts Where chart_id == '%s'" %input_chart_id)
        c.execute('select * from charts NOCASE;')
        x=c.fetchall()
        for the in x:
            if the[0] == input_chart_id:

                print "\n\nSYMPTOMS"
                print "--------"
                for row in c.execute("SELECT symptom FROM symptoms Where chart_id LIKE '%s' ORDER BY obs_date" %input_chart_id):
                    print row[0]
                print "\nDIAGNOSES"
                print "---------"
                for row in c.execute("SELECT diagnosis FROM diagnoses Where chart_id LIKE '%s' ORDER BY ddate" %input_chart_id):
                    print row[0]
                print "\nMEDICATIONS"
                print "-----------"
                for row in c.execute("SELECT drug_name  FROM medications Where chart_id LIKE '%s' ORDER BY mdate" %input_chart_id):
                    print row[0]
                print "\n"
                
                return 
        
        print "Invalid Chart ID"
        return
'''class AdminStaff:
    def __init__(self):
        return None
    def get_presc_amt(self,period):
        con = sqlite3.connect('hospital.db') #opens the database file
        con.execute('PRAGMA forteign_keys=ON; ')
        con.text_factory = str #this gets rid of the u in front.
        c = con.cursor()
       
        #creates a list with only doctor info from staff table
        c.execute("SELECT * FROM staff WHERE role = 'D'")
        staff_list = c.fetchall()
      
        #reports for each doctor, all drugnames along with amounts prescribed over a specified period
       
       
        try:
            c.execute("SELECT * FROM medications WHERE mdate >= Datetime('2014-05-16-07:02:14') AND mdate <= Datetime('2014-05-26-09:04:13')",(period[0],period[1]))
            medic_list = c.fetchall()
            doc_list = []
            dict_list = []
            #organizes the two queries
            for doc in staff_list:
                for medic in medic_list:
                    if doc[0]==medic[2]:
                        if doc[2] not in doc_list:
                            #creates a new dictionary to store drugname and amount
                            doclist.append(doc[2])
                            doc[2] = {}
                            doc[2][medic[7]] = medic[6]
                        else:
                            doc[2].update({medic[7]: medic[6]})
                        dict_list.append(doc[2])
                #printing the results or you could return the two lists       
                i = 0
                for doc in doc_list:
                    print(doc_list[i])
                    print(dict_list+[i])
                    i=i+1                       
                           
           
                       
        except:
            print('Please enter a tuple in the format (yyyy-mm-dd-HH:MM:SS,yyyy-mm-dd-HH:MM:SS)')
           
        #date = period.replace('-', '').replace(' ', '')
      
        #return None
    def get_cat_amt(self, period):
        #returns a total amount for each drug in said category and total amount of all drugs in the same category within the period
        c.execute("SELECT * FROM drugs ORDER BY category")
        drugdata1 = c.fetchall()
        
       
        try:
            c.execute("SELECT amount,drug_name FROM medications WHERE mdate >= Datetime(?) AND mydate <= Datetime(?)",(period[0],period[1]))
            drugdata2 = c.fetchall()
            dict_list = []
            for data1 in drugdata1:
                for data2 in drugdata2:
                    if data1[0] == data2[1]:
                        if data1[1] not in categorylist:
                            categorylist.append(data1[1])
                            data1[1] = {}
                            data1[1][data1[0]]= data2[0]
                        else:
                            data1[1].update({data1[0]: data2[0]})
                        dict_list.append(data1[1])
        except:
            print('Please enter a tuple in the format (yyyy-mm-dd-HH:MM:SS,yyyy-mm-dd-HH:MM:SS)')                       
            #printing the results or you could return the two lists
            i = 0
            for cat in categorylist:
                print(categorylist[i])
                print(dict_list[i])
                i=i+1
               

'''
        

loggedIn = False
while loggedIn == False:
    loginInfo = str(raw_input("Welcome please enter your login name: "))
    password = str(raw_input("Please enter your password: "))
    hash_object =hashlib.sha224(password)
    test= hash_object.hexdigest()
    
    #todo fill in the login stuff
    c.execute("Select * From staff;")
    result =c.fetchall()
    for row in result:
        if row['role']==  "D" and row["login"]==loginInfo and row['password']==test:
            #print "Doctor Stuff", row['staff_id']
            loggedIn = True
            doc = Doctor()
            while loggedIn == True:
                print("Actions:")
                print("1) Search for a patient")
                print("2) Add a symptom entry for a patient's chart")
                print("3) Add a diagnosis entry for a patient's chart")
                print("4) Add a medication entry for a patient's chart")
                print("5) Logout")
                choice = int(raw_input("Please select press the number associated with the action you wish to preform: "))
                
                if choice ==  1:
                    hcno=str(raw_input('Enter patients hcno: '))

                    doc.getPatient(hcno)
                    pass
                elif choice == 2: 
                    hcno = str(raw_input('Enter the patients hcno: ')).lower()
                    staff_id = row['staff_id']
                    doc.addSymptom(hcno,staff_id)
                    pass
                elif choice == 3:
                    hcno = str(raw_input('Enter the patients hcno: ')).lower()
                    staff_id = row['staff_id']
                    doc.addDiagnosis(hcno,staff_id)                    
                    
                    pass
                elif choice == 4: 
                    hcno= str(raw_input('Enter patients hcno: ')).lower()
                    staff_id= row['staff_id']
                    doc.addMedications(hcno, staff_id)
                    pass
                elif choice == 5: 
                    print('Goodbye')
                    break

        elif row['role']  == "A" and row["login"]==loginInfo and row['password']==test:
            print "admin Stuff"
            print("Actions:")
            print("1) Create report")
            print("2) List prescriptions")
            print("3) List medications")
            print("4) List diagnoses")
            adminstaff=AdminStaff()
            print("5) Logout")
            choice = int(raw_input("Please select press the number associated with the action you wish to preform: "))
            if choice ==  1:
                period_start=str(raw_input("Please enter starting period: "))
                period_end=str(raw_input("please enter end period: "))
                period=(period_start,period_end)
                adminstaff.get_presc_amt(period)
                
                pass
            elif choice == 2: 
                pass
            elif choice == 3: 
                pass
            elif choice == 4: 
                pass
            elif choice == 5: 
                print('Goodbye')
                break            
        



       



        elif row['role'] == "N" and row["login"]==loginInfo and row['password']==test:
            print "nurse Stuff"
            loggedIn = True
            nurse= Nurse()
            while loggedIn == True:
                print("Actions:")
                print("1) Open new chart")
                print("2) Add a symptom entry for a patient's chart")
                print("3) Search for patient")
                print("4) Close chart")
                print("5) Logout")
                choice = int(raw_input("Please select press the number associated with the action you wish to preform: "))
                if choice ==  1:
                    patients_id=str(raw_input("Please enter the patients hcno: ")).lower()
                    nurse.create_chart(patients_id)
                    
                    pass
                elif choice == 2:
                    patient_id=str(raw_input('Please enter patients hcno: ')).lower()
                    staff_id=row['staff_id']
                    nurse.addSymptom(patient_id,staff_id)
                    pass
                elif choice == 3: 
                    nurse.getPatient()
                elif choice == 4: 
                    patients_id=str(raw_input('Please enter patients hcno: ')).lower()
                    nurse.close_chart(patients_id)                    
                    pass
                elif choice == 5: 
                    print('Goodbye')
                    break


                

conn.commit()
conn.close()
