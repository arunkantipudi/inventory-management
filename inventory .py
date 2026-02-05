#inventory managemant system by arun


#connectig the data base
import mysql.connector as db

con = db.connect(user='root',database = 'inventory_db',host = 'localhost',\
                 password = 'sql@123')

cu = con.cursor()

role = input("Are you a owner or customer : ").lower()
#owner code
if role == "owner":
  print("Hello, Good Morning")

  while True:
    choice = int(input('''Choose one option
    1.Add items to inventory
    2.Remove item
    3.update item
    4.view inventory
    5.view user Details
    6.Total Revenue 
    7.exit  :  '''))

    if choice == 1:
      
      adding = True
      while adding:
        item = input("Enter item name : ").lower()
        #check if item exits in table
        cu.execute("select 1  from inventory where item_name = %s",[item])
        exists = cu.fetchone()
    
        if exists:
          print("This item alredy exists ")
          
        else:
          cost_price = float(input("Enter item cost price : "))
          selling_price = int(input("Enter item selling price: "))
          quant = int(input("Enter item quantity : "))

          cu.execute("insert into inventory (item_name,quantity,cost_price,sell_price) values (%s,%s,%s,%s)",[item,quant,cost_price,selling_price])
          con.commit()
          print("Item dded successfully")
        ch = input("Do you want to add more items? (yes/no)").lower()
        if ch == "no":
          adding = False


    #remove items
    elif choice == 2:
      removing = True
      while removing:
        cu.execute("select count(*) from inventory")
        number_of_items = cu.fetchone()[0]
        if number_of_items == 0:
          print("store  is empty")
        else:
          item = input("Enter item name you want to remove  : ")
          cu.execute("select 1 from inventory where item_name = %s",[item])
          exists = cu.fetchone()
        
          if exists:
            cu.execute("delete from inventory where item_name = %s",[item])
            con.commit()
          else:
            print("item not found")
          ch = input("Do you want to remove more items? (yes/no)").lower()
          if ch == "no":
            removing  = False
            

    #update
    elif choice == 3:
      updating = True
      while updating:
        cu.execute("select count(*) from inventory")
        exists = cu.fetchone()[0]
        if exists>0:
          item = input("Enter item name you want to update  : ")
          cu.execute("select 1 from inventory where item_name = %s",[item])
          exists = cu.fetchone()
          if exists:
            opt = int(input('''enter one option
            1.update cost
            2.update quantity '''))
            if opt == 1:
                cost_price = float(input(f"Enter new cost price of {item}: "))
                selling_price = float(input(f"Enter new selling price of {item}: "))

                cu.execute(
                    "UPDATE inventory SET cost_price=%s, sell_price=%s WHERE item_name=%s",
                    [cost_price, selling_price, item]
                )
                con.commit()
                print("Price updated successfully")

            elif opt == 2:
                new_quant = int(input(f"Enter new quantity for {item}: "))

                cu.execute(
                    "update inventory set quantity=%s WHERE item_name=%s",
                    (new_quant, item)
                )
                con.commit()
                print("Quantity updated successfully")

            else:
                print("Invalid choice")
          else:
              print("Item not found in  table")
        else:
          print("Inventory is empty")
        ch = input("Do you want to update more items? (yes/no)").lower()
        if ch == "no":
          updating = False

    #inventry details
    elif choice == 4:
      print("Full details of inventy ")
      cu.execute("select * from inventory")
      details = cu.fetchall()
      for row in details:
          print(row)
    #for customers details 
    elif choice == 5:
      print("Full details of users ")
      cu.execute("select * from customers")
      details = cu.fetchall()
      for row in details:
          print(row)


    elif choice == 6:
        cu.execute("select sum(revenue) from  sales")
        print("Total Revenue:", cu.fetchone()[0])

    elif choice == 7:
      print("Thank you for using our system")
      break
    else:
      print("Invalid choice")

# customer side
elif role == "customer":

    shopping = True
    while shopping:
        choice = int(input("""
        enter an option
        1.add items to cart
        2.view cart
        3.remove item from cart
        4.modify cart
        5.bill
        6.exit  : """))

        # 1. add items to cart
        if choice == 1:
            item = input("enter item name: ").lower()

            cu.execute(
                "select quantity, sell_price from inventory where item_name = %s",
                [item]
            )
            row = cu.fetchone()

            if not row:
                print("item not found")
            else:
                available_qty, sell_price = row
                qty = int(input("enter quantity: "))

                if qty > available_qty:
                    print("only", available_qty, " is available")
                else:
                    price = qty * sell_price

                    cu.execute(
                        "insert into cart (item_name, quantity, price) values (%s,%s,%s)",
                        [item, qty, price]
                    )
                    con.commit()

                    cu.execute(
                        "update inventory set quantity = quantity - %s where item_name = %s",
                        [qty, item]
                    )

                    con.commit()
                    print("item added to cart")

        # 2. view cart
        elif choice == 2:
            cu.execute("select item_name, quantity, price from cart")
            rows = cu.fetchall()

            if not rows:
                print("cart is empty")
            else:
                print("items in cart:")
                for r in rows:
                    print(r[0], "qty : ", r[1], " price : ", r[2])

        # 3. remove item from cart
        elif choice == 3:
            item = input("enter item name to remove: ").lower()

            cu.execute(
                "select quantity from cart where item_name = %s",
                [item]
            )
            row = cu.fetchone()

            if not row:
                print("item not in cart")
            else:
                cart_qty = row[0]

                cu.execute(
                    "delete from cart where item_name = %s",
                    [item]
                )
                con.commit()

                cu.execute(
                    "update inventory set quantity = quantity + %s where item_name = %s",
                    [cart_qty, item]
                )

                con.commit()
                print("item removed from cart")

        # 4. modify cart
        elif choice == 4:
            item = input("enter item name: ").lower()

            cu.execute(
                "select quantity from cart where item_name = %s",
                [item]
            )
            row = cu.fetchone()

            if not row:
                print("item not in cart")
            else:
                old_qty = row[0]
                new_qty = int(input("enter new quantity: "))

                cu.execute(
                    "select quantity, sell_price from inventory where item_name = %s",
                    [item]
                )
                inv_qty, sell_price = cu.fetchone()

                if new_qty > inv_qty + old_qty:
                    print("quantity not available")
                else:
                    diff = new_qty - old_qty
                    new_price = new_qty * sell_price

                    cu.execute(
                        "update cart set quantity = %s, price = %s where item_name = %s",
                        [new_qty, new_price, item]
                    )
                    

                    cu.execute(
                        "update inventory set quantity = quantity - %s where item_name = %s",
                        [diff, item]
                    )

                    con.commit()
                    print("cart updated")

        # 5. bill
        elif choice == 5:
            cu.execute("select count(*) from cart")
            count = cu.fetchone()[0]

            if count == 0:
                print("cart is empty")
            else:
                name = input("enter customer name: ")
                mobile = input("enter mobile number: ")

                cu.execute(
                    "insert into customers (customer_name, mobile) values (%s,%s)",
                    [name, mobile]
                )
                con.commit()
                cu.execute("select customer_id  from customers where mobile = %s",[mobile])
                customer_id = cu.fetchone()[0]

                cu.execute(
                    "select item_name, quantity, price from cart"
                )
                rows = cu.fetchall()

                total_bill = 0

                for item_name, qty, price in rows:
                    cu.execute(
                        "select item_id, cost_price, sell_price from inventory where item_name = %s",
                        [item_name]
                    )
                    item_id, cost_price, sell_price = cu.fetchone()

                    revenue = price
                    profit = (sell_price - cost_price) * qty

                    cu.execute(
                        """insert into sales
                        (item_id, customer_id, quantity, revenue, profit)
                        values (%s,%s,%s,%s,%s)""",
                        [item_id, customer_id, qty, revenue, profit]
                    )

                    total_bill += revenue

                cu.execute("delete from cart")
                con.commit()

                print("bill amount:", total_bill)
                print("thank you for shopping")
                shopping = False

        # 6. exit
        elif choice == 6:
            print("thank you")
            shopping = False

        else:
            print("invalid option")



else:
  print("Invalid role")

