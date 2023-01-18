"""
Brenden Nelson
CPTS 451 Project Milestone 2

Code will connect to application and database and allow user to make all 4 use cases as required by project description
"""

from os import close
import sys
from unittest import result
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2
import math

qtCreatorFile = "MainWindowMilestone1.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.ZipCodeList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.CategoryList.itemSelectionChanged.connect(self.CategoryChanged)

    def executeQuery(self,sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='bbj172824'")
        except:
            print("Unable to connect to the DataBase!!")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        results = cur.fetchall()
        conn.close()
        return results

    def loadStateList(self):
        self.ui.stateList.clear()
        self.ui.num_businesses_obj.clear()
        self.ui.pop_obj.clear()
        self.ui.avg_obj.clear()
        self.ui.CategoryList.clear()
        sql_str = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
    
    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.CategoryList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT DISTINCT city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query has failed!")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business where state ='" + state + "'ORDER BY name ;"
            try:
                results = self.executeQuery(sql_str)                
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num CheckIns'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,200)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query has failed!")

    def cityChanged(self):
        self.ui.ZipCodeList.clear()
        self.ui.CategoryList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()

            sql_str = "SELECT DISTINCT postal_code FROM business WHERE state ='" + state + "' AND city='" + city + "' ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.ZipCodeList.addItem(row[0])
            except:
                print("Query has failed!")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business where state ='" + state + "' AND city='" + city + "'ORDER BY name ;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num CheckIns'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,200)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query has failed!")
    
    def zipChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.ZipCodeList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipCode = self.ui.ZipCodeList.selectedItems()[0].text()

            # Below is to parse through categories to fill in categoryList
            sql_str = "SELECT DISTINCT categories FROM business WHERE state ='" + state + "' AND city='" + city + "'"
            try:
                results = self.executeQuery(sql_str)
                added = []
                for row in results:
                    for r in row:
                        r = r.replace('`','')
                        r = r.replace(' ','')
                        r = r[1:len(r)-1]
                        rr = r.split(',')
                        for item in rr:
                            if item not in added:
                                added.append(item)
                                self.ui.CategoryList.addItem(item)
            except:
                print("Query has failed")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business where state ='" + state + "' AND city='" + city + "' AND postal_code='" + zipCode + "'ORDER BY name ;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num CheckIns'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,200)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query has failed!")


            # Queries for information about zipcodes

            sql_str2 = "SELECT population FROM zipcodedata WHERE zipcode ='" + zipCode + "'"
            try:
                results2 = self.executeQuery(sql_str2)
                self.ui.pop_obj.setText(str(results2[0][0]))
            except:
                print("Query has failed!")


            sql_str3 = "SELECT meanincome FROM zipcodedata WHERE zipcode ='" + zipCode + "'"
            try:
                results3 = self.executeQuery(sql_str3)
                self.ui.avg_obj.setText(str(results3[0][0]))
            except:
                print("Query has failed!")


            sql_str4 = "SELECT num_businesses FROM zipcodedata WHERE zipcode ='" + zipCode + "'"
            try:
                results4 = self.executeQuery(sql_str4)
                self.ui.num_businesses_obj.setText(str(results4[0][0]))
            except:
                print("Query has failed!")

            
            # Query for Popular businesses within a zipcode 
            # found by taking total interactions for a business and displaying top 25% within specific zipcode
            sql_str5 = "SELECT name, review_count + numcheckins FROM business WHERE postal_code ='" + zipCode + "'ORDER BY review_count+numcheckins DESC;"
            try:
                results5 = self.executeQuery(sql_str5)
                results5 = results5[:math.ceil(len(results5)/4)]
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularTable.setColumnCount(len(results5[0]))
                self.ui.popularTable.setRowCount(len(results5))
                self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'Interaction Count'])
                self.ui.popularTable.resizeColumnsToContents()
                self.ui.popularTable.setColumnWidth(0,300)
                self.ui.popularTable.setColumnWidth(1,100)
                currentRowCount = 0
                for row in results5:
                    for colCount in range(0, len(results5[0])):
                        self.ui.popularTable.setItem(currentRowCount,colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query has failed!")



            # Query for Successful businsesses within a zipcode
            # found by filtering businesses by stars >= 4.0, rating >= 4.0 and review_count >= 10
            # further only looked at businesses currently open and display the top results within specific zipcode
            sql_str6 = "SELECT name, stars, reviewrating, review_count FROM business WHERE postal_code ='" + zipCode + "'AND is_open='True' AND stars>=4.0 AND reviewrating>=4.0 AND review_count>10 ORDER BY review_count+numcheckins DESC;"
            try:
                results6 = self.executeQuery(sql_str6)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulTable.horizontalHeader().setStyleSheet(style)
                self.ui.successfulTable.setColumnCount(len(results6[0]))
                self.ui.successfulTable.setRowCount(len(results6))
                self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Rating', 'Review Count'])
                self.ui.successfulTable.resizeColumnsToContents()
                self.ui.successfulTable.setColumnWidth(0,200)
                self.ui.successfulTable.setColumnWidth(1,75)
                self.ui.successfulTable.setColumnWidth(2,100)
                self.ui.successfulTable.setColumnWidth(3,75)
                currentRowCount = 0
                for row in results6:
                    for colCount in range(0, len(results6[0])):
                        self.ui.successfulTable.setItem(currentRowCount,colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query has failed!")

    def CategoryChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.ZipCodeList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipCode = self.ui.ZipCodeList.selectedItems()[0].text()
            category = self.ui.CategoryList.selectedItems()[0].text()
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins, categories FROM business where state ='" + state + "' AND city='" + city + "' AND postal_code='" + zipCode + "'ORDER BY name ;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num CheckIns'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,200)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                self.ui.businessTable.setColumnWidth(6,50)
                currentRowCount = 0
                for row in results:
                    # businesses only in specified category
                    r = row[-1]
                    r = r.replace('`','')
                    r = r.replace(' ','')
                    r = r[1:len(r)-1]
                    rr = r.split(',')
                    if str(category) in rr:
                        for colCount in range(0, len(results[0])-1):
                            self.ui.businessTable.setItem(currentRowCount,colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
            except:
                print("Query has failed!")

            




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())