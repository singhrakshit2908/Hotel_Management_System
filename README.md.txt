
HOTEL MANAGEMENT SYSTEM
==============================================================

This TXT file contains a polished, professional overview of the Hotel Management System
built using Python, Tkinter, and Pandas. Designed for GitHub, college submissions, and
portfolio enhancement.

------------------------------------------------------------
PROJECT OVERVIEW
------------------------------------------------------------
The Hotel Management System is a complete desktop application that simulates real hotel
operations. It supports booking, room availability tracking, restaurant billing, necessities
requests, payment processing, and record management.

The system uses:
• Tkinter for GUI  
• Pandas for data handling  
• CSV for storage  
• Modular UI screens for each function  


------------------------------------------------------------
CORE FEATURES
------------------------------------------------------------

A. BOOKING MANAGEMENT
• Single Booking  
• Group Booking (up to 20 rooms at once)  
• Auto-assign rooms based on availability  
• Date validation (Check-in < Check-out)  
• Price calculation based on room type × days  
• Phone number verification  
• Summary popups  

B. ROOM AVAILABILITY
• Four room categories:
  - Standard Non-AC (₹3500/day)
  - Standard AC (₹4000/day)
  - 3-Bed Non-AC (₹4500/day)
  - 3-Bed AC (₹5000/day)
• Shows occupied, available, and total rooms  
• Percentage occupancy indicators  

C. RESTAURANT MODULE
• Organized menu (South Indian, Rice, Breads, Curry, Non-Veg)  
• Add items to cart  
• Total updates in real-time  
• Customer ID verification  
• Restaurant charges auto-added to the booking  

D. NECESSITIES MODULE
Supports service requests for:
• Extra Towels  
• Extra Pillows  
• Blankets  
• Toiletries  
• Iron Box  
• Laundry Service  
Charges are added directly to the customer's account.

E. PAYMENT & BILLING
• Search by Customer ID or Phone Number  
• Billing breakdown includes:
  - Room Rent  
  - Restaurant Charges  
  - Necessities Charges  
• Payment methods supported:
  - Card  
  - UPI  
  - Cash  
• Ensures no double-payment

F. RECORD MANAGEMENT
• View All Bookings  
• View Active Bookings  
• View Completed Bookings  
• Search bar for filtering by:
  - Name  
  - Phone  
  - Customer ID  
• CSV export option  

------------------------------------------------------------
INSTALLATION & RUNNING
------------------------------------------------------------

1. Install required dependency:
   pip install pandas

2. Run the application:
   python HMS_main.py

The system automatically creates and updates:
hotel_data.csv


------------------------------------------------------------
INTERNAL SYSTEM DESIGN
------------------------------------------------------------

A. DATA LAYER
• CSV file stores:
  name, phone, address, check-in, check-out, room type, charges, status, etc.
• Pandas handles reading, writing, type conversion  
• Auto-creates columns like necessities_charges if missing  

B. GUI LAYER
Tkinter interface includes:
• Frames  
• Scrollable views  
• Label Frames  
• Buttons  
• Radio buttons  
• Spinboxes  
• TreeView tables  

C. BOOKING ENGINE
• Generates random but unique Customer IDs  
• Allocates rooms from available pool  
• Calculates stay duration based on date difference  

D. BILLING ENGINE
• Unified logic for calculating:
  room charges + restaurant + necessities  
• Prevents modification after payment completion  

E. RECORD SYSTEM
• Searchable and sortable  
• CSV export supported  
• Status color coding:
  ACTIVE  
  COMPLETED  
  CANCELLED  


------------------------------------------------------------
FUTURE IMPROVEMENTS
------------------------------------------------------------
• Upgrade to SQLite or MySQL  
• Add login system  
• Generate PDF invoices  
• Add revenue charts  
• Add notifications or email receipts  
• Improve UI with modern theming  
• Add mobile or web edition  


------------------------------------------------------------
AUTHOR/TEAM LEADER
------------------------------------------------------------

Rakshit Singh

------------------------------------------------------------
COLLABORATOR/TEAM MEMBERS

Anupriya Yadav
Kashish
Divyanka Rai
Akshansh Gupta

------------------------------------------------------------
END OF DOCUMENT
------------------------------------------------------------
