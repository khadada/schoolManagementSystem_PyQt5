import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
# from PyQt5.uic import loadUi
from fullProgram import Ui_MainWindow
import sqlite3

class Software(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Software,self).__init__()
        self.setupUi(self)
        self.db_connect()
        self.handelButtons()
        self.load_info()
        self.data_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.data_table.horizontalHeader()
        # header.setSectionResizeMode(1, QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        # header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7,QHeaderView.Stretch)
        header.setSectionResizeMode(8,QHeaderView.Stretch)
    def db_connect(self):
        try:
            self.db = sqlite3.connect("schoolData.db")
            self.agentRobot = self.db.cursor()
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS students(ID INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,first_name TEXT,last_name TEXT,national_id TEXT,categorie TEXT,workstation TEXT,address TEXT,phone TEXT,mobile TEXT)"
            ) 
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS categorie(categorie_id INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL ,categorie_name INTEGER)"
            )
            
            QMessageBox.information(self,"Connnection State","The connection to database is working with fun.")
        except sqlite3.Error as er:
            QMessageBox.warning(self,"Error Database",f"{er}")
    def handelButtons(self):
        self.add_btn.clicked.connect(self.add_student)
        self.search_btn.clicked.connect(self.lookingFor)
        self.aboutDeveloper.triggered.connect(self.about_us)
        self.delete_btn.clicked.connect(self.delete_student)
        self.update_btn.clicked.connect(self.update_student)
        self.refresh_btn.clicked.connect(self.load_info)
        self.clear_btn.clicked.connect(self.clear_all)
        self.data_table.cellDoubleClicked.connect(self.selected_Row)
    def add_student(self):
        """
        Add Student to database 
        """
        s_Fname = self.firstname_field.text()
        s_Lname = self.lastname_field.text()
        s_mobile = self.mobile_field.text()
        s_phone = self.phone_field.text()
        s_nationalid = self.nationalid_field.text()
        s_categorie = self.categorie_cb.currentIndex()
        s_status = self.status_cb.currentIndex()
        s_address = self.address_field.text()
        if s_Fname and s_Lname and s_nationalid != "":
            commandCheck = f"select first_name, last_name,national_id from students where first_name ='{s_Fname}' and last_name='{s_Lname}' and national_id= '{s_nationalid}'"
            self.agentRobot.execute(commandCheck)
            isExists = self.agentRobot.fetchone()
            if not isExists:
                commandAdd = f"insert into students (first_name,last_name,national_id,categorie,workstation,address,phone,mobile) values ('{s_Fname}','{s_Lname}','{s_nationalid}','{s_categorie}','{s_status}','{s_address}','{s_phone}','{s_mobile}')"
                self.agentRobot.execute(commandAdd)
                QMessageBox.information(self,"Congratulations ","The student added to database with sucess. (^_^)")
                self.clear_fields()
                self.db.commit()
                self.load_info()
            else:
                QMessageBox.information(self,"Alert!!! ","The student exists in the database ")        
        else:
            QMessageBox.warning(self,"Missing Information","Please Check the necessary/required field.")
    def selected_Row(self):
        self.index = self.data_table.selectedItems()
        commandSelect = f"SELECT * from students WHERE ID = '{self.index[0].text()}'"
        self.agentRobot.execute(commandSelect)
        row_selected = self.agentRobot.fetchone()
        print(row_selected)
        if row_selected:
            self.id_label.setText(str(row_selected[0]))
            self.firstname_field.setText(row_selected[1])
            self.lastname_field.setText(row_selected[2])
            self.phone_field.setText(row_selected[3])
            self.categorie_cb.setCurrentIndex(int(row_selected[4]))
            self.status_cb.setCurrentIndex(int(row_selected[5]))
            self.nationalid_field.setText(row_selected[6])
            self.mobile_field.setText(row_selected[8])
            self.address_field.setText(row_selected[7])
    def messageToUser(self,title,messageText):
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(messageText)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()
    def lookingFor(self):
        item_looking = self.search_field.text()
        if  item_looking:
            commandSearch = f"SELECT * FROM students where first_name='{item_looking}' or national_id ='{item_looking}' or ID ='{item_looking}'"
            self.agentRobot.execute(commandSearch)
            result = self.agentRobot.fetchone()
            if result:
                QMessageBox.information(self,'Student Found',"The student found in database. ")
                # print(result[1])
                self.id_label.setText(str(result[0]))
                self.firstname_field.setText(result[1])
                self.lastname_field.setText(result[2])
                self.categorie_cb.setCurrentIndex(int(result[3]))
                self.phone_field.setText(result[4])
                self.nationalid_field.setText(result[5])
                self.status_cb.setCurrentIndex(int(result[6]))
                self.mobile_field.setText(result[8])
                self.address_field.setText(result[7])
            else:
                QMessageBox.information(self,'Student Not Found',"The student doesn't exists in found in database. ")
        else:
            QMessageBox.information(self,'Error',"Cant't search for nothing. ")
    def delete_student(self):
        id_student = self.id_label.text()
        if id_student !="":
            data = self.agentRobot.fetchone()
            commandDelete = f"DELETE FROM students where ID='{id_student}'"
            self.agentRobot.execute(commandDelete)
            self.db.commit()
            QMessageBox.information(self,"Congratulations","The student deleted with success")
            self.clear_fields()
            self.load_info()
        else:
            QMessageBox.warning(self,"Error","Not student has been selected to work with.")
    def update_student(self):
        id_student = self.id_label.text()
        if id_student !="":
            s_Fname = self.firstname_field.text()
            s_Lname = self.lastname_field.text()
            s_mobile = self.mobile_field.text()
            s_phone = self.phone_field.text()
            s_nationalid = self.nationalid_field.text()
            s_categorie = self.categorie_cb.currentIndex()
            s_status = self.status_cb.currentIndex()
            s_address = self.address_field.text()
            commandUpdate = f"UPDATE students SET first_name = '{s_Fname}',last_name = '{s_Lname}',national_id = '{s_nationalid}',categorie = '{s_categorie}',workstation = '{s_status}',address = '{s_address}',phone = '{s_phone}',mobile = '{s_mobile}' WHERE ID='{id_student}'"
            self.agentRobot.execute(commandUpdate)
            self.db.commit()
            QMessageBox.information(self,'Congratulations','The information of the student was update successfuly')
            self.clear_fields() 
            self.load_info()      
        else:
            QMessageBox.warning(self,'Error','There is no student seleted to work with.')
    def clear_all(self):
        answer = QMessageBox.question(self,"Attention:","Are you sure need to clear your database?",QMessageBox.Ok,QMessageBox.Cancel)
        if answer == QMessageBox.Ok:
            commandDeleteAll = "DELETE FROM students"
            self.agentRobot.execute(commandDeleteAll)
            QMessageBox.information(self,"Congratulations","All database information is deleted successfuly.")
            self.load_info()
            self.clear_fields()
            
    def load_info(self):
        commandLoad = f"SELECT * FROM students"
        self.agentRobot.execute(commandLoad)
        result = self.agentRobot.fetchall()
        self.data_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.data_table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.data_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))  
        if not result:
            QMessageBox.information(self,"Notice","The database is compeletly empty")
    def clear_fields(self):
        self.search_field.setText("")
        self.id_label.setText("")
        self.firstname_field.setText("")
        self.lastname_field.setText("")
        self.categorie_cb.setCurrentIndex(0)
        self.phone_field.setText("")
        self.nationalid_field.setText("")
        self.status_cb.setCurrentIndex(0)
        self.mobile_field.setText("")
        self.address_field.setText("")
    def about_us(self):
        """
        Display information about the Developer who code this GUI.
        """
        QMessageBox.about(self,"About Me","Beginner's Pratical Guid to Create GUI\n\nThis program was create by:Khaled Melizi\n\nPhone: +213780360303\n\nEmail:lkhadada@gmail.com\n\nDate:11/06/2022\n\nIn: Temacine W. Touggourt.")
    
            
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    school = Software()
    school.show()
    sys.exit(app.exec_())