import sys
import cx_Oracle

x = input('enter username: ')
y = input('enter password: ')
connStr = x+'/'+y+'@gwynne.cs.ualberta.ca:1521/CRS'
	
try:
	connection = cx_Oracle.connect(connStr)
	curs = connection.cursor()
	
	# ======================================================================================================	
	def doPrescription():
		print("\nYou have chosen to enter a prescription")
		doctor_list = []#contains a list of tuples with doctors name and id number
		doc_id_list =[]#contains a list of doctor medical employee numbers
		mult_doc_list=[]
		test_list=[]
		patient_name_list = []
		not_allowed_list= []
		danger = "DANGER PATIENT IS NOT ALLOWED TO TAKE THIS TEST"
		double_occurance = False
		position = 0
		more_than_1 = False
		count = 0
		highest_value =[]
		size = 0
		data = []
		end = False
		test_id_number = 0
		#Find a doctor
		while end == False:
			#Asks how the person would like to enter a prescription from doctor
			option = input("\nPrescribe via Doctor Name (1) or Prescribe via Employee number (2): ")
			if option == "1":
				#query for finding the name of the doctor and therefor his id number
				try:
					name = input("\nPlease enter the Name of the doctor prescribing the test: ")
					if ';' in name:
						int('n')
					curs.execute("select p.name, d.employee_no from patient p, doctor d where d.health_care_no=p.health_care_no and p.name like '"+name+"'")
					rows = curs.fetchall()
					#print(rows)
					#The situation if there is only one doctor with this name
					if len(rows) == 1:
						doctor_id = str(int(rows[0][1]))
						doctor_name = rows[0][0]
						print(doctor_id)
						print("\nThere is a match: ")
						print("Name:"+doctor_name)
						print("Employee No.: "+str(doctor_id))
						
					#the situation if there is more than one doctor with this name
					elif len(rows) > 1:
						count = 0
						for row in rows:
							count+=1
							print(row)
						#they HAVE to enter the correct id this time, shouldn't be a problem though since everthing is presented to them in the list
						specific=input("There are "+str(count)+" doctors with this name. please enter the medical employee number of the doctor prescribing the test from the list above: ")
						doctor_id = str(specific)
						count = 0
						
					#we will now loop around 
					elif len(rows) == 0:
						print("There is no doctor with that name in our database.")
						end = True
				except:
					print("There was an error processing your request")
					end = True
					
			elif option == "2":
				try:	
					#getting the query
					d_id = str(int(input("\nPlease enter the EMPLOYEE NUMBER of the doctor prescribing the test: ")))
					curs.execute("select d.employee_no from doctor d where d.employee_no ="+d_id)
					rows = curs.fetchall()
					if len(rows) == 1:
						#there will be a match
						doctor_id= str(int(rows[0][0]))
						print("\nThere is a match: ")
						print("Employee No.:"+str(doctor_id))
					
					if len(rows) == 0:
						#no matches starting all over again
						print("There is no doctor with that medical id number in our system please try again")
				except:
					#there was an issue in processing the request
					print("There was an error processing your request")
					end = True
				
			else:
				#they have made an error so they must choose again
				print("ERROR not valid.")
				end = True
					
			#Finding a patient
			
			if end == False:
				patient = input("\nDo you want to select the patient by name (1) or by healthcare number (2): ")
				if patient == "1":
					patient_name = input("\nPlease enter the name of the patient who is recieving the prescription: ")
					try:
						#trying the search for patient name 
						query = "select p.name, p.health_care_no from patient p where p.name like'"+patient_name+"'"
						curs.execute(query)
						patient_names = curs.fetchall()
						#the case with only one patient
						if len(patient_names) == 1:
							patient_id = str(int(patient_names[0][1]))
							patient_name =patient_names[0][0]
							print("\nThere is a match: ")
							print("Name:"+patient_name)
							print("Health Care No.:"+str(patient_id))
						#the case with multiple patients
						elif len(patient_names) > 1:
							count = 0
							for patient in patient_names:
								count += 1
								print(patient)
							narrowed =input("There are "+str(count)+" patients with this name. please enter the health care number of patient receiving the test from the list above: ")
							patient_id = narrowed
					except:
						print("There was an error processing your request, please try again")
						end = True
				elif patient == '2':
					#looking the patient up by healthcare number
					try:
						patient_num = str(int(input("Please enter the healtcare number of the patient who is recieving the prescription: ")))
						curs.execute("select p.health_care_no from patient p where p.health_care_no="+patient_num)
						all_patient_ids = curs.fetchall()

					except:
						print("There was an error processing your request")
						end = True
						
					if len(all_patient_ids) == 0:
						print("Sorry that patient does not appear to be in our database, please try again")
					if len(all_patient_ids) == 1:
						patient_id = str(int(all_patient_ids[0][0]))
						print("\nThere is a match: ")
						print("Health Care No.:"+str(patient_id))					
				else:
					#they have made an error so they must choose again
					print("ERROR not valid.")
					end = True
			
			#finding the tests
			if end == False:
				try:
					test_type= str(input("\nWhat is the name of the test that is being prescribed:"))
					curs.execute("select type_id, test_name from test_type where test_name like'"+test_type+"'")
					tests = curs.fetchall()
					#print(tests)
					if len(tests) ==1:
						#acceptable amount of tests
						test_id = str(int(tests[0][0]))
						test_name = str(tests[0][1])
						print("\nThere is a match:")
						print("\nTest_id: "+test_id)
						print("Test name: "+ test_name)
					if len(tests) == 0:
						print("Sorry that test is not in our database.")
						end = True
				except:
					print("There was an error processing your request.")
					end = True
					
			if end == False:
				print("\nChecking if you are allowed to take this test...")
				#checking if the patient is allowed to take this test
				try:
					check_query = "select health_care_no from not_allowed where type_id =" + test_id +" and health_care_no="+ patient_id
					curs.execute(check_query)
					not_allowed_list = curs.fetchall()
					if len(not_allowed_list) > 0:
						print(danger)
						print("\nFatal error sending you back to main menu, patient is NOT ALLOWED to take this test")
						end = True
					else:
						#patient is allowed to take this test
						print("\nPatient is allowed to take this test at this current time")
						#giving an update of interface progress
						print("\nGenerating Test ID...")
				except:
					print("\nError processing your request to see if patient is allowed to take this test")
					end = True
					#should boot em out of the application for trying this statement 
					
			if end == False:
				try:
					curs.execute("select MAX(test_id) As HIGHRECORD from test_record")
					test_numbers = curs.fetchall()
					test_record_id = str(test_numbers[0][0]+1)
					print("The Test ID for this prescription is: "+test_record_id)
					#finally the last few queries that they can fill if they want, not entering anything generates a null value
					date_prescribed=input("\nPlease enter the date in which this test was prescribed in the form DD/MMM/YYYY: ")
					test_date = input("\nWhat day is the test being conducted on in the form DD/MMM/YYYY? (if unknown press enter): ")
					result=input("\nPlease enter the result of the test (if unknown press enter): ")
					test_location = input("Where is this test being preformed? (press enter if unknown): ")
					try:
						#actually inputting the 
						curs.execute("insert into test_record values ("+test_record_id+", "+test_id+", "+patient_id+", "+doctor_id+", '"+test_location+"', '"+result+"', '" +date_prescribed+"', '"+test_date+"') ")
						connection.commit()
					except:
						print("Error inputing your prescrition into the database.")
						#go again
				except:
					print("Error generating new test id")
			end = False
			continueing = input("\nWould you like to insert another prescription into the test record? (y/n): ")
			if continueing != 'y':
				end = True
			
		
	# ======================================================================================================	
	def doMedTest():
		#loops through while user is still enetering test results
		addAnotherResult = True
		while addAnotherResult == True:
			# takes in the patient health-care-number and doctors employee number and checks if there is a test that contains the two as doctor and patient (noth must be integers)
			legal = True
			try:
				patientTested = str(int(input('\nWhat is the Health-Care-Number of the patient who recieved the test?: ')))
				doctorOfTest = str(int(input('What is the Employee Number of the doctor who performed the test?: ')))
			except:
				print('Not an integer')
				legal = False
			
			if legal == True:
				prescriptionComand = "select * from test_record where employee_no = "+doctorOfTest+" and patient_no = "+patientTested
				curs.execute(prescriptionComand)
				prescription = curs.fetchall()
				# if there are no such test then it will prompt this message
				if len(prescription) == 0:
					print('No such test exists.')
				else:
					# else it will print out all of the test conducted between the two
					presIDs = []
					for pres in prescription:
						presIDs.append(str(pres[0]))
						print(pres)
					# asks the user to choose from the displayed tests and select the test by the test_id (first column)
					goodEntry = False
					while goodEntry == False:
						testID = input('\nFrom the Test_ID\'s above (first column), which test would you like to edit?: ') 
						if testID in presIDs and ';' not in testID:
							goodEntry = True
					# asks the user to enter the lab, test date, and the result of the test and puts in sql statment that will be executed
					labName = input('What was the name of the lab where this test was performed?: ')
					testDate = input('What was the date when this test was performed?(DD/mon/YYYY): ')
					result = input('What was the result of this experiment?: ')
					updateTest = "update test_record set medical_lab ='"+labName+"', result = '"+result+"', test_date ='"+testDate+"' where test_id ="+testID+" and employee_no = "+doctorOfTest+" and patient_no = "+patientTested
				
					# attempts to execute the statment if it works it will update the data base	
					try:
						curs.execute(updateTest)
						connection.commit()
					# if it doesnt work will prompt error that one of the above attributes was not acceptible
					except:
						print('Error in one of the entered attributes.')
			
			# asks user to enter more results otherwise exits to 'main menu'
			if input("\nWould you like to add another test result?(y/n): ") != 'y':
				addAnotherResult = False
			
	# ======================================================================================================
	# completed will give options of edit of add patient and giev errors if invalid input is entered and oracle recieves error.
	def doPatientUpdate():
		# loops thorugh the updating un till the users selects done and then will leave.
		doneUpdating = False
		while doneUpdating == False:
			# take in the inputed choice and stores
			option = input('\nAdd new Patient (add), Edit existing patient (edit), or finish update (done)?: ')
			
			# adds new patient to patient table
			if option == 'add':
				# loops through addMore as long as user decides to add more patients to data base
				addMore = True
				
				# these are user for executing multiple commands and must be reset in loop so no duplicates occur
				size = 0
				data = []
				while addMore == True:
					
					# take in all the information need for patient
					try:
						#patientDataHealthCareNum = int(input('Enter patient HealthCareNumber: '))

						curs.execute("select MAX(health_care_no) As HIGHNO from patient")
						health_nos = curs.fetchall()
						patientDataHealthCareNum = str(health_nos[0][0]+1)
						print("The health care number for this patient is: "+patientDataHealthCareNum)						
						
						patientDataName = input('Enter patient name: ')
						patientDataAddress = input('Enter patient address: ')
						patientDataBday = input('Enter patient birthdate(DD/mon/YYYY): ')
						patientDataphone = input('Enter patient phone: ')
						# appends the patient to the list of patients created
						data += [(patientDataHealthCareNum, patientDataName, patientDataAddress, patientDataBday, patientDataphone)]
						size += 1
						# user can add multiple at once
						if input('\nadd another?(y/n): ') == 'n':
							addMore = False
					except:
						print('Did not enter Correctly.')
	
				# after all are in data list will attemept to add all to data base
				# if one is incorect then that and all after will not be entered and an error will be prompted
				try:
					cursInsert = connection.cursor()
					cursInsert.bindarraysize = len(data)
					cursInsert.setinputsizes(int, 100, 200, 11, 10)
					cursInsert.executemany("insert into patient (health_care_no, name, address,  birth_day, phone) VALUES (:1, :2, :3, :4, :5)", data)
					connection.commit()
					cursInsert.close()
				except:
					print('\nError: one entry was entered incorrectly or patient may already exist with the health-care-number, name, or phone. therefore, could not complete all comands.')
				
			
			# edits patient in table
			elif option == 'edit':
				
				# loops through while the user wishes to stay on edit option
				editMore = True
				while editMore == True:
					
					# finds patient user wishes to edit by patient key Health-Care-Number
					hcn = input('\nWhat is the Health-Care-Number of the patient you wish to edit?: ')

					executable = 'select * from patient where health_care_no = '+hcn
					curs.execute(executable)
					patient = curs.fetchall()
					# checks if the patient exists otherwise tells the user
					if len(patient) != 0:
						
						# displays attributes of the patient the user wishes to edit
						print(patient)
						
						keepEditing = True
						while keepEditing == True:
							# askes the user what they would like to have edited on the patient
							editOption = input('\nWhat would you like to edit?(name (1), address (2), birthday (3), phone (4)): ')
							# cahnges the command based on if the user edits:
						
							# name
							if editOption == '1':
								name = input('new name: ')
								comand = "update patient set name ='"+name+"' where health_care_no ="+hcn
								# address
							elif editOption == '2':
								address = input('new address: ')
								comand = "update patient set address ='"+address+"' where health_care_no ="+hcn
								# birthday
							elif editOption == '3':
								bday = input('new birthday:(DD/mon/YYYY) ')
								comand = "update patient set birth_day ='"+bday+"' where health_care_no ="+hcn
								# phone number
							elif editOption == '4':
								phone = input('new phone: ')
								comand = "update patient set phone ='"+phone+"' where health_care_no ="+hcn
								# none of the provided options where selected
							else:
								print('Error: invalid input.')
						
								# attempts the comand will prompt error if the new edit is not permited due to
								# uniqueness or an invalid entered data type
							try:
								if ';' in comand:
									int('n')
								curs.execute(comand)
							
							except:
								print('Error: illegal entry, edit not completed')
							
							if input('\nKeep editing this patient?(y/n): ') != 'y':
								keepEditing = False
						
						# prints out edited/unedited patient
						curs.execute(executable)
						patient = curs.fetchall()
						print(patient)						
						
					else:
						print('Patient does not exist.')
						
					#asks user if they wish to edit another patient
					editAnother = input('would you like to edit another?(y/n): ')
					if editAnother == 'n':
						editMore = False
			
			# if done is selected then the system displays the list of all patients in the data base currently
			elif option == 'done':
				doneUpdating = True			
			# promts error if no option was slected
			else:
				print('Error: Invalid input.')    
				                
	# ======================================================================================================	
	def doSearch():
		doneSearching = False
		#Loop until user specifies to exit
		while doneSearching == False:
			input_string = '\nSearch test records (1), Search prescriptons (2), Display patients that have reached the alarming age for a test (3), or finish search (finish)?: '
			option = input(input_string)
			#Search test records
			if option == '1':
				#Loop until user specifies to exit
				searchRecord = True
				while searchRecord == True:
					record_query = 'SELECT patient.health_care_no, patient.name, test_type.test_name, test_record.test_date, test_record.result '
					record_query += 'FROM patient, test_type, test_record '
					record_query += 'WHERE patient.health_care_no = test_record.patient_no AND test_record.type_id = test_type.type_id '     	  
					mode = input('\nSearch by patient health care number (1) or by patient name (2)?: ')
					#Search by health care_no
					if mode == '1':
						health_care_no = input('\nPatient health care number: ')
						record_query += "AND patient.health_care_no = '" + health_care_no + "'"
						record_query += 'ORDER BY patient.health_care_no, patient.name, '
						record_query += 'test_type.test_name, test_record.test_date, test_record.result '
						try:	    
							curs.execute(record_query)
						except:
							print('Error retreiving patient list.') 
						results = curs.fetchall()
						#If there are results, print them.
						if len(results) == 0:
							print('No test records for that patient.')
						else:
							for row in results:
								print('Health Care No:', row[0], ', Name:', row[1], ', Test:', row[2], ', Date:',
							              str(row[3]), ', Result:', row[4] )					    
					#Search by name
					elif mode == '2':		
						patient_name = input('\nPatient name: ')
					
						#TODO: check if name must be exact or if we should use patient.name LIKE *name*?
					    
						name_query = "SELECT name, health_care_no FROM patient WHERE name = '" + patient_name + "' "
						#Search database for patients of that name
						try:
							#print(patient_name.split(''))
							rows = curs.execute(name_query)
						except:
							print('Error retreiving patient list')
						patients = []
						#Add results to a list
						for row in rows:
							patients.append(row)
						#check if there were results
						if len(patients) == 0:
							print('Sorry, that patient is not in our records.')
						else:
							#If there are multiple results, ask the user to specify one based on health care number
							if len(patients) != 1:
								print('Multiple results: ')
								for i in range(len(patients)):
									print(i + 1, ': Patient:',patients[i][0],', Health Care No.:', patients[i][1])
								while True:
									try:
										result_no = int(input('\nSelect result #: ')) - 1
										#loop until result selected is in range
										while True:
											if result_no not in range(0, len(patients)):
												print('Result out of range.')
												result_no = int(input('Select result #: ')) - 1
											else:
												break
										break
									except:
										print('Not an Integer')	
							#If there is only one patient with that name, execute query with that patient
							else:
								result_no = 0
							#Execute query with that health_care_no
							health_care_no = str(patients[result_no][1])
							record_query += "AND patient.health_care_no = '" + health_care_no + "'"
							record_query += 'ORDER BY patient.health_care_no, patient.name, '
							record_query += 'test_type.test_name, test_record.test_date, test_record.result '							
							try:	    
								curs.execute(record_query)
							except:
								print('\nError retreiving patient list.') 
							results = curs.fetchall()
							#If there are results, print them.
							if len(results) == 0:
								print('No test records for that patient.')
							else:
								for row in results:
									print('Health Care No:', row[0], ', Name:', row[1], ', Test:', row[2], ', Date:',
									      str(row[3]), ', Result:', row[4] )
					else:
						print('Error: Invalid input.')
					if input('\nSearch for another record? (y/n): ').lower() != 'y':
						searchRecord = False
			#Search for prescription
			elif option == '2':
		
			#TODO: This may need to be edited due to date/string types and format.
			#I will test it and correct it to the right format.
		    
				#loop until user specifies
				searchPresc = True
				while searchPresc == True:
					invalid = False
					presc_query = 'SELECT patient.health_care_no, patient.name, test_type.test_name, test_record.prescribe_date '
					presc_query += 'FROM patient, doctor, test_type, test_record '
					presc_query += 'WHERE patient.health_care_no = test_record.patient_no AND test_record.type_id = test_type.type_id AND test_record.employee_no = doctor.employee_no '
					mode = input('\nSearch by doctor employee number (1) or name (2)?: ')
					#Search by doctor employee number
					if mode == '1':
						employee_no = input('Doctor employee number: ')
						presc_query += 'AND doctor.employee_no = ' + employee_no + ' '
					#Search by doctor name
					elif mode == '2':
						doctor_name = input('Doctor name: ') 
						name_query = 'SELECT patient.name, doctor.employee_no FROM patient, doctor '
						name_query += "WHERE patient.health_care_no = doctor.health_care_no AND patient.name = '" + doctor_name + "'"
						#Search database for doctors of that name
						try:
							curs.execute(name_query)
						except:
							print('Error retreiving patient list')
						results = curs.fetchall()
						doctors = []
						#Add results to a list
						for row in results:
							doctors.append(row)
						#Check if the doctor exists in the database
						if len(doctors) == 0:
							print('Sorry, that doctor is not in our records.')
							invalid = True
						else:
							#If there are multiple results, ask the user to specify one based on employee number
							if len(doctors) != 1:
								print('Multiple results: ')
								for i in range(len(doctors)):
									print(i + 1, ': Doctor:',doctors[i][0],', Employee No.:', doctors[i][1])
								while True:
									try:
										result_no = int(input('Select result #: ')) - 1
										#loop until result selected is in range
										while True:
											if result_no not in range(0, len(doctors)):
												print('Result out of range.')
												result_no = int(input('Select result #: ')) - 1
											else:
												break
										break
									except:
										print('Not an Integer.')
							#if there is only one doctor by that name, use that one
							else:
								result_no = 0
							employee_no = str(doctors[result_no][1])
							presc_query += "AND doctor.employee_no = '" + employee_no + "' "
					else:
						print('Error: Invalid input.')
						invalid = True
					if invalid == False:
						#Ask user to specify which dates to search between
						start_date = input('Search from date (DD/MON/YYYY): ').upper()
						end_date = input('Search to date (DD/MON/YYYY): ').upper()
						presc_query += "AND test_record.prescribe_date BETWEEN to_date('" + start_date + "', 'DD/MON/YYYY') "
						presc_query += "AND to_date('" + end_date + "', 'DD/MON/YYYY') "
						presc_query += 'ORDER BY patient.health_care_no, patient.name, test_type.test_name, test_record.prescribe_date '

						try:
							curs.execute(presc_query)
							results = curs.fetchall()
							#print if there are results
							if len(results) == 0:
								print('No results for prescription between the specified dates.')
							else:
								for row in results:
									print('Health Care No:', row[0], ', Name:', row[1], ', Test:', row[2], ', Date:', str(row[3]) )							
						except:
							print('Error retreiving results')
					if input('\nSearch for another prescription? (y/n): ') != 'y':
						searchPresc = False
			#Search alarming age
			elif option == '3':
				drop_query = 'DROP VIEW medical_risk'
				#loop until user specifies
				searchAlarming = True
				while searchAlarming == True:
					cursRisk = connection.cursor()
					cursAlarming = connection.cursor()					
				
					try:
						cursRisk.execute(drop_query)
					except:
						print('\nError dropping medical risk')
	
					risk_query = 'CREATE VIEW medical_risk(medical_type,alarming_age,abnormal_rate) '
					risk_query += 'AS SELECT c1.type_id,min(c1.age),ab_rate FROM '
					risk_query += '(SELECT   t1.type_id, count(distinct t1.patient_no)/count(distinct t2.patient_no) ab_rate ' 
					risk_query += 'FROM     test_record t1, test_record t2 '
					risk_query += 'WHERE    t1.result <> \'normal\' AND t1.type_id = t2.type_id GROUP BY t1.type_id ) r, '
					risk_query += '(SELECT   t1.type_id,age,COUNT(distinct p1.health_care_no) AS ab_cnt '
					risk_query += 'FROM     patient p1,test_record t1, '
					risk_query += '(SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age '
					risk_query += 'FROM patient p1) WHERE    trunc(months_between(sysdate,p1.birth_day)/12)>=age '
					risk_query += 'AND p1.health_care_no=t1.patient_no AND t1.result<>\'normal\' '
					risk_query += 'AND t1.result IS NOT NULL '
					risk_query += 'GROUP BY age,t1.type_id  ) c1, '
					risk_query += '(SELECT  t1.type_id,age,COUNT(distinct p1.health_care_no) AS cnt '
					risk_query += 'FROM    patient p1, test_record t1, '
					risk_query += '(SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age '
					risk_query += 'FROM patient p1) WHERE trunc(months_between(sysdate,p1.birth_day)/12)>=age '
					risk_query += 'AND p1.health_care_no=t1.patient_no GROUP BY age,t1.type_id ) c2 '
					risk_query += 'WHERE  c1.age = c2.age AND c1.type_id = c2.type_id '
					risk_query += 'AND c1.type_id = r.type_id AND c1.ab_cnt/c2.cnt>=2*r.ab_rate '
					risk_query += 'GROUP BY c1.type_id,ab_rate'
			    
					try:
						cursRisk.execute(risk_query)
					except:
						print('\nError creating view medical_risk')
				
					test_name = input('\nName of test type to display patients who have reached alarming age: ')
			    
					alarming_query = 'SELECT DISTINCT patient.health_care_no, patient.name, patient.address, patient.phone '
					alarming_query += 'FROM   patient, medical_risk, test_type '
					alarming_query += 'WHERE  trunc(months_between(sysdate, patient.birth_day)/12) >= medical_risk.alarming_age '
					alarming_query += 'AND    medical_risk.medical_type = test_type.type_id '
					alarming_query += "AND    test_type.test_name = '" + test_name + "' "
					alarming_query += 'AND    patient.health_care_no NOT IN (SELECT patient_no '
					alarming_query += 'FROM   test_record, medical_risk, test_type '
					alarming_query += 'WHERE  medical_risk.medical_type = test_record.type_id '
					alarming_query += 'AND test_record.result IS NOT NULL) '
					alarming_query += 'ORDER BY patient.health_care_no, patient.name, patient.address, patient.phone '
					
					try:
						cursAlarming.execute(alarming_query)
					except:
						print('\nError retreiving results')
					results = cursAlarming.fetchall()
					if len(results) == 0:
						print('\nAll patients at the alarming age for that test have been tested.')
					else:
						for row in results:
							print('Health Care No:', row[0], ', Name:', row[1], ', Address:', row[2], ', Phone:',
					                      str(row[3]) )
					cursRisk.close()
					cursAlarming.close()		
					if input('\nSearch another test for patients at the alarming age? (y/n): ') != 'y':
						searchAlarming = False						
		
			elif option == 'finish':
				doneSearching = True
		
			else:
				print('Error: Invalid input.')	
	
	
	# ======================================================================================================
	# something of a main menu for deciding which component the user whishes to select or exit function
	exit = False
	while exit == False:
		componentSelect = input('\nWhich component would you like to select?(Options: Prescription (1), Medical Test (2), Patient Information Update (3), Search Engine (4), Exit (exit): ')
		if componentSelect == '1':
			doPrescription()
		elif componentSelect == '2':
			doMedTest()
		elif componentSelect == '3':
			doPatientUpdate()
		elif componentSelect == '4':
			doSearch()
		elif componentSelect == 'exit':
			exit = True			
		else:
			print('Error: Invalid entry try again.')	
		
		
		
		
	# closes all running connections
	curs.close()
	connection.close()
except cx_Oracle.DatabaseError as exc:
	error, = exc.args
	print( sys.stderr, "Oracle code:", error.code)
	print( sys.stderr, "Oracle message:", error.message)