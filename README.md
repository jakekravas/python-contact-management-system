# Contact Management System

###### Configuration instructions
To run this program with pre-loaded contacts, include them in a "contacts.csv" file in the format of:
"firstname","lastname","phonenumber" with no extra spaces or empty lines

Otherwise, no specific configuration is needed.

###### Installation instructions
The libraries used in this program are built into Python, so having Python installed is all you'll need. Information on how to download Python can be accessed at https://www.python.org/downloads/

###### Operating instructions
To start the program, run python3 index.py in the terminal

To add a contact, make sure the "Add" radiobutton is selected in the bottom left corner of the program. You will not be allowed to add a contact if either the first name or last name field is left empty.

To view a contact, select it from the list in the middle of the program.

To edit a contact, select it from the list in the middle of the program, then click the "Edit" button below the contact details on the bottom left side of the program. When you've finished editing the contact, click "Save" to save the contact. If you decide you no longer wish to save your changes, click "Cancel" and they won't be saved.

To delete a contact, select it from the list in the middle of the program and click the "Delete" button.

To sort contacts based on first name or last name, select the "First Name" or "Last Name" column headers above the contact list. If the header is clicked once, contacts will sort in ascending order. If the header is clicked a second time (before clicking another header) then contacts will sort in descending order.

To search for contacts, use the text field to the right of the contacts list and click the "Search" button. To change the attribute you'd like to search by, select it from the dropdown menu in the top right of the program. To clear your search, click the "Clear" which is located to the right of the "Search" button.

###### Files
index.py
contacts.csv (optional)
