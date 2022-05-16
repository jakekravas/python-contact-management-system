from tkinter import *
from tkinter import ttk
import csv
import os.path
import uuid

root = Tk()
root.title('Contact Management System')
root.geometry('1100x500')
root.configure(bg='#252526')


# GET CONTACTS FROM contacts.csv
def get_contacts_from_csv():

  # if contacts.csv exists, get the data and return it as a list
  if os.path.isfile('contacts.csv'):
    with open('contacts.csv', newline='') as f:
      reader = csv.reader(f)
      data = list(reader)
      if data:
        for i in range(len(data)):
          id = str(uuid.uuid4())
          data[i].append(id)
      return data
  # if contacts.csv doesn't exist, return empty list
  else:
    return []

contacts = get_contacts_from_csv()
display_contacts = contacts.copy()

# MAIN FUNCTION
def main():
  global contacts
  global display_contacts

  search_by_options = [
    'First Name',
    'Last Name',
    'Phone #'
  ]

  # INITIALIZE StringVars / IntVars / BooleanVars ##
  # Variables for viewing/editing a contact
  first_name_VE = StringVar()
  last_name_VE = StringVar()
  phone_VE = StringVar()

  # Variables for adding a contact
  first_name_add = StringVar()
  last_name_add = StringVar()
  phone_add = StringVar()

  # Variable for search text
  search_text = StringVar()

  # Variable for attribute to search by
  search_by_val = StringVar()

  # Variable for add and view/edit display toggle
  add_VE_toggle = IntVar()

  # Variable for attribute to sort vy
  sort_attribute = StringVar()

  # Variable for whether sort is in ascending or descending order
  sort_ascending = BooleanVar()

  selected_id = StringVar()


  # SET VARIABLES TO INITIAL VALUE
  search_by_val.set(search_by_options[0])
  sort_attribute.set('First Name')
  sort_ascending.set(True)
  add_VE_toggle.set(2)


  # VALIDATE INPUT
  def validate_input(name, index, mode):

    #prevent first name text from exceeding 20 characters
    if name == 'PY_VAR0':
      val = first_name_VE.get()
      first_name_VE.set(val[0:20])

    #prevent last name text from exceeding 20 characters
    elif name == 'PY_VAR1':
      val = last_name_VE.get()
      last_name_VE.set(val[0:20])

    #ensure phone # is numeric and prevent it from exceeding 15 characters
    elif name == 'PY_VAR2':

      val = phone_VE.get()

      if val:
        if not val[-1].isnumeric():
          phone_VE.set(val[0:-1])
        
        if len(val) > 15:
          phone_VE.set(val[0:15])

    #prevent first name text from exceeding 20 characters
    elif name == 'PY_VAR4':
      val = first_name_add.get()
      first_name_add.set(val[0:20])

    #prevent last name text from exceeding 20 characters
    elif name == 'PY_VAR5':
      val = last_name_add.get()
      last_name_add.set(val[0:20])

    #ensure phone # is numeric and prevent it from exceeding 15 characters
    elif name == 'PY_VAR6':

      val = phone_add.get()

      if val:
        if not val[-1].isnumeric():
          phone_add.set(val[0:-1])
        
        if len(val) > 15:
          phone_add.set(val[0:15])

    #prevent search text from exceeding 20 characters
    elif name == 'PY_VAR7':
      val = search_text.get()
      search_text.set(val[0:20])
      

  # trigger validate_input every time input field changes
  first_name_VE.trace('w', validate_input)
  last_name_VE.trace('w', validate_input)
  phone_VE.trace('w', validate_input)
  first_name_add.trace('w', validate_input)
  last_name_add.trace('w', validate_input)
  phone_add.trace('w', validate_input)
  search_text.trace('w', validate_input)

  # CONTACT SELECT
  def contact_select(e):
    cancel_delete()
    for i in tree.selection():

      selected_id.set(tree.item(i,'text'))

      first = tree.item(i,'values')[0]
      last = tree.item(i,'values')[1]
      phone = tree.item(i,'values')[2]

      first_name_VE.set(first)
      last_name_VE.set(last)
      phone_VE.set(phone)

    view_mode()
    
    if add_VE_toggle.get() == 2:
      add_VE_toggle.set(1)
      toggle_modes()

  # TOGGLE ADD/VIEW MODES
  def toggle_modes():
    if add_VE_toggle.get() == 1:
      set_contact_fields_to_VE()
      cancel_delete()
      view_mode()
    else:
      add_mode()

  # SET CONTACT ENTRY FIELDS TO VIEW/EDIT VALUES
  def set_contact_fields_to_VE():
    first_name_entry['textvariable'] = first_name_VE
    last_name_entry['textvariable'] = last_name_VE
    phone_entry['textvariable'] = phone_VE

  # GET INDEX OF SELECTED TREE ITEM
  def get_tree_index():
    selected = tree.selection()[0]
    tree_contacts = tree.get_children()
    tree_index = tree_contacts.index(selected)
    return tree_index

  # SAVE CONTACTS TO contacts.csv
  def save_to_csv():

    contacts_save_list = []
    #save contacts to CSV without ID
    for i in range(len(contacts)):
      contacts_save_list.append(contacts[i][0:-1])

    with open('contacts.csv', 'w', newline='') as w:
      writer = csv.writer(w)
      writer.writerows(contacts_save_list)

  # CREATE CONTACT
  def create_contact():
    first = first_name_add.get()
    last = last_name_add.get()
    phone = phone_add.get()

    # If all fields are filled out then create contact
    if first.strip() != '' and last.strip() != '' and phone.strip() != '':
      
      id = str(uuid.uuid4())

      contacts.append([first,last,phone,id])
      display_contacts.append([first,last,phone,id])

      save_to_csv()

      attribute_index = search_by_options.index(sort_attribute.get())
      
      merge_sort(contacts, attribute_index)
      merge_sort(display_contacts, attribute_index)
      clear_add_fields()
      render_contacts(display_contacts)
      alert_label.grid_forget()
    else:
      alert_label.grid(row=10, column=0)

  # ON DELETE BUTTON CONTACT
  def delete_button_click():
    # cancel_edit()
    delete_button.grid_forget()
    delete_confirm_label.grid( row = 8, column = 4, sticky=E, padx=(0,60) )
    delete_no_button.grid( row=8, column = 4, sticky = E, padx=(0,35) )
    delete_yes_button.grid( row=8, column = 4, sticky = E )

  # DELETE CONTACT
  def delete_contact():
    tree_id = selected_id.get()

    for i in range(len(contacts)):
      if contacts[i][-1] == tree_id:
        del contacts[i]
        break
        
    for i in range(len(display_contacts)):
      if display_contacts[i][-1] == tree_id:
        del display_contacts[i]
        break

    save_to_csv()

    selected_items = tree.selection()[0]
    tree.delete(selected_items)

    clear_VE_fields()
    cancel_delete()

  # CANCEL DELETE
  def cancel_delete():
    delete_confirm_label.grid_forget()
    delete_no_button.grid_forget()
    delete_yes_button.grid_forget()
    delete_button.grid( row = 8, column = 4, sticky = E )
  
  # ON EDIT BUTTON CONTACT
  def edit_click():
    if tree.selection():
      cancel_delete()
      edit_mode()

  # UPDATE CONTACT
  def update_contact():
    cancel_delete()
    tree_index = get_tree_index()
    tree_id = selected_id.get()

    #get text values of each input
    first = first_name_VE.get()
    last = last_name_VE.get()
    phone = phone_VE.get()

    #find contact by id and update it with new info
    for i in range(len(contacts)):
      if contacts[i][-1] == tree_id:
        contacts[i][0] = first
        contacts[i][1] = last
        contacts[i][2] = phone
    for i in range(len(display_contacts)):
      if display_contacts[i][-1] == tree_id:
        display_contacts[i][0] = first
        display_contacts[i][1] = last
        display_contacts[i][2] = phone

    #save contacts to csv
    save_to_csv()

    #remove old version of contact, add new version contact, and re-select it in the tree
    selected_items = tree.selection()        
    for selected_item in selected_items:
      tree.delete(selected_item)
      tree.insert('', tree_index, text=tree_id, values=(first, last, phone))
      contact_to_select = tree.get_children()[tree_index]
      tree.focus(contact_to_select)
      tree.selection_set(contact_to_select)

    # view_mode()
  
  # CANCEL EDIT
  def cancel_edit():

    #get index of 
    tree_index = get_tree_index()

    #set input values to values of saved contact
    first_name_VE.set( contacts[tree_index][0] )
    last_name_VE.set( contacts[tree_index][1] )
    phone_VE.set( contacts[tree_index][2] )

    view_mode()

  # ENABLE VIEW (READONLY) MODE
  def view_mode():

    alert_label.grid_forget()

    #hide cancel button
    cancel_button.grid_forget()
    
    #change text of button from "Create" to "Edit"
    create_or_edit['text'] = 'Edit'

    #change command of button
    create_or_edit['command'] = edit_click

    #disable editing of contact input fields
    first_name_entry['state'] = DISABLED
    last_name_entry['state'] = DISABLED
    phone_entry['state'] = DISABLED

  # ENABLE EDIT MODE
  def edit_mode():

    #change command of button
    create_or_edit['command'] = update_contact

    #change text of button from "Edit" to "Save"
    create_or_edit['text'] = 'Save'

    #show cancel button
    cancel_button.grid(row=9, column=0, sticky=E)

    #enable editing of contact entry fields
    enable_contact_entry_editing()

  # ENABLE ADD MODE
  def add_mode():
    #hide cancel button
    cancel_button.grid_forget()
    cancel_delete()
    delete_button.grid_forget()
    
    #change button text to "Create"
    create_or_edit['text'] = 'Create'

    #change command of button
    create_or_edit['command'] = create_contact

    #set textvariables from view/edit values to add values
    first_name_entry['textvariable'] = first_name_add
    last_name_entry['textvariable'] = last_name_add
    phone_entry['textvariable'] = phone_add

    #enable editing of contact entry fields
    enable_contact_entry_editing()

  # ENABLE EDITING OF CONTACT ENTRY FIELDS
  def enable_contact_entry_editing():
    first_name_entry['state'] = NORMAL
    last_name_entry['state'] = NORMAL
    phone_entry['state'] = NORMAL

  # CLEAR VIEW/EDIT ENTRIES
  def clear_VE_fields():
    first_name_VE.set('')
    last_name_VE.set('')
    phone_VE.set('')

  # CLEAR ADD ENTRIES
  def clear_add_fields():
    first_name_add.set('')
    last_name_add.set('')
    phone_add.set('')

  # SEARCH FOR CONTACTS
  def search():
    cancel_delete()
    view_mode()
    #grabbing index of search_by_val because it matches the index of desired attribute of contacts list
    index_of_search_by_options = search_by_options.index(search_by_val.get())
    
    display_contacts.clear()

    for i in range(len(contacts)):
      contact_attribute = contacts[i][index_of_search_by_options].lower()

      if search_text.get().lower() in contact_attribute:
        display_contacts.append(contacts[i])

    render_contacts(display_contacts)
      
  # HANDLE CONTACT TREE HEADER CLICK
  def header_click(attribute, index):
      merge_sort(contacts, index)
      merge_sort(display_contacts, index)

      if attribute == sort_attribute.get() and sort_ascending.get():
        sort_ascending.set(False)
        contacts.reverse()
        display_contacts.reverse()
      else:
        sort_ascending.set(True)
        sort_attribute.set(attribute)

      render_contacts(display_contacts)

  # MERGE SORT
  def merge_sort(arr, attribute_index):

    if len(arr) > 1:
      left_arr = arr[:len(arr)//2]
      right_arr = arr[len(arr)//2:]
      
      # recursion
      merge_sort(left_arr, attribute_index)
      merge_sort(right_arr, attribute_index)
      
      # merge
      i = 0 # index of left_arr
      e = 0 # index of right_arr
      m = 0 # index of merged array
      while i < len(left_arr) and e < len(right_arr):
        if left_arr[i][attribute_index].lower() < right_arr[e][attribute_index].lower():
          arr[m] = left_arr[i]
          i += 1
        else:
          arr[m] = right_arr[e]
          e += 1
        m += 1  
        
      while i < len(left_arr):
        arr[m] = left_arr[i]
        i += 1
        m += 1

      while e < len(right_arr):
        arr[m] = right_arr[e]
        e += 1
        m += 1

  # CLEAR SEARCH
  def clear_search():
    search_text.set('')
    search()


  # LABELS
  first_name_label = Label( text='First name', bg='#252526', fg='#f6f6f6' )
  last_name_label = Label( text='Last name', bg='#252526', fg='#f6f6f6' )
  phone_label = Label( text='Phone #', bg='#252526', fg='#f6f6f6' )
  search_label = Label( text='Search by:', bg='#252526', fg='#f6f6f6' )
  alert_label = Label( text='All fields must be filled out', bg='#252526', fg='#dc3545' )
  delete_confirm_label = Label( text='Delete this contact?', bg='#252526', fg='#f6f6f6' )
  # ENTRIES
  first_name_entry = Entry( bg='#3e3e42', textvariable=first_name_add, fg = 'white', relief = 'solid', highlightthickness=0, disabledbackground='#3e3e42', state=NORMAL )
  last_name_entry = Entry( bg='#3e3e42', textvariable=last_name_add, fg = 'white', relief = 'solid', highlightthickness=0, disabledbackground='#3e3e42', state=NORMAL )
  phone_entry = Entry( bg='#3e3e42', textvariable=phone_add, fg = 'white',relief = 'solid', highlightthickness=0, disabledbackground='#3e3e42', state=NORMAL )
  search_entry = Entry(bg='#3e3e42', textvariable=search_text, fg = 'white', relief = 'solid', highlightthickness=0, disabledbackground='#3e3e42', state=NORMAL )
  # BUTTONS
  create_or_edit = Button( text='Create', command=create_contact )
  delete_button = Button( text='Delete', command=delete_button_click )
  delete_yes_button = Button(text='Yes', command = delete_contact)
  delete_no_button = Button(text='No', command = cancel_delete)
  cancel_button = Button( text='Cancel', command=cancel_edit )
  search_button = Button( text='Search', command=search )
  clear_button = Button( text='Clear', command=clear_search)

  # RADIOBUTTONS
  edit_radio = Radiobutton(root, variable=add_VE_toggle, value=1, command=toggle_modes, text='View / Edit',fg='#f6f6f6',bg='#252526' )
  add_radio = Radiobutton(root, variable=add_VE_toggle, value=2, command=toggle_modes, text='Add',fg='#f6f6f6', bg='#252526' )

  # CONTACT TREE
  tree = ttk.Treeview(root, column=('c1', 'c2', 'c3'), show='headings')

  # SEARCH TYPE DROPDOWN
  search_by_dropdown = OptionMenu(root, search_by_val, *search_by_options)

  # LAYOUT
  create_or_edit.grid( row = 8, column = 0, sticky = E )
  delete_button.grid( row = 8, column = 4, sticky = E )
  edit_radio.grid( row = 8, column = 0, sticky = W )
  search_label.grid( row = 1, column = 5 )
  add_radio.grid( row = 9, column = 0, sticky = W )
  first_name_label.grid( row = 1, column = 0, pady = 0 )
  first_name_entry.grid( row = 2, column = 0, pady = 0 )
  last_name_label.grid( row = 3, column = 0, pady = 0 )
  last_name_entry.grid( row = 4, column = 0, pady = 0 )
  phone_label.grid( row = 5, column = 0, pady = 0 )
  phone_entry.grid( row = 6, column = 0, pady = 0 )
  tree.grid( row = 0, rowspan = 8, column = 4)
  search_by_dropdown.grid( row = 1, column = 6, columnspan=2 )
  search_entry.grid( row = 2, column = 5 )
  search_button.grid( row = 2, column = 6 )
  clear_button.grid( row = 2, column = 7 )

  # CONTACT TREE COLUMNS
  tree.column('# 1', anchor=CENTER)
  tree.column('# 2', anchor=CENTER)
  tree.column('# 3', anchor=CENTER)

  # CONTACT TREE HEADINGS
  tree.heading('# 1', text='First Name', command = lambda : header_click('First Name', 0))
  tree.heading('# 2', text='Last Name', command = lambda : header_click('Last Name', 1))
  tree.heading('# 3', text='Phone #')

  # TRIGGER contact_select EVERY TIME A CONTACT IS SELECTED IN THE TREE
  tree.bind('<<TreeviewSelect>>', contact_select)

  # RENDER CONTACTS
  def render_contacts(contacts):

    # clear contacts from tree
    tree.delete(*tree.get_children())

    # clear view/edit text fields
    clear_VE_fields()

    if contacts:
      # loop through contacts list that was passed in and insert each contact into tree
      for i in range(len(contacts)):
        tree.insert('', 'end', text=contacts[i][-1], values=(contacts[i][0], contacts[i][1], contacts[i][2]))

  # RUN ON START
  def on_start():
    merge_sort(contacts, 0)
    merge_sort(display_contacts, 0)
    render_contacts(display_contacts)

  on_start()

  root.mainloop()

main()
