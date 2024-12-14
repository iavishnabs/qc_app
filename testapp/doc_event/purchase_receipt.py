import frappe


def before_save(doc,method):
    quality_check_detection(doc)
    warehouse_checking(doc)
    manage_quality_check_selection(doc)


def quality_check_detection(doc):
    print("\n\n\n quality check function called!!!")
    if doc.items:
        # doc.supplier_delivery_note = "hai"
        for its in doc.items:
            if its.item_code:
                if its.custom_quality_check is not None:
                    print("it has already values")
                    # frappe.throw("billls")
                else:
                    print("\n\n\n","!!!!!item code found and quality not found!!!!!")
                    items_doc = frappe.get_doc("Item",its.item_code)
                    if items_doc:
                        print("item fetching")
                        if items_doc.inspection_required_before_purchase == 1:
                            print("quality yes",items_doc.inspection_required_before_purchase)
                            its.db_set("custom_quality_check", "Yes")
                            
                        else:
                            print("no quality check\n\n",items_doc.inspection_required_before_purchase)
                            its.db_set("custom_quality_check", "No")
              
                
def warehouse_checking(doc):
    print("\n\n warehouse function called")
    if not doc.set_warehouse:
        frappe.throw("Please Choose Accepted Warehouse")
    else:
        print("\n\n warehouse found",doc.set_warehouse)
        if doc.set_warehouse != "Stores - TC":
            if doc.items:
                for its in doc.items:
                    if its.custom_quality_check == "Yes":
                        items_doc = frappe.get_doc("Item",its.item_code)
                        if items_doc:
                            print("item fetching for warehouse function")
                            if items_doc.inspection_required_before_purchase == 1:
                                items_doc.inspection_required_before_purchase = 0
                                items_doc.save()
                                print("value changed for the item",its.item_code)

def manage_quality_check_selection(doc):
    if doc.items:
        for its in doc.items:
            if its.quality_inspection is None and doc.set_warehouse == "Stores - TC":
                # frappe.throw("bye bye!!!")
                if its.custom_quality_check and its.custom_quality_check == "Yes":
                    frappe.throw("Please Select a Quality Check For the Items")
                else:
                    print("not required qc!!\n\n")

                


def on_submit(doc,method):
    pass
    if doc.set_warehouse:
        if doc.set_warehouse != "Stores - TC":
            for i in doc.items:
                if i.custom_quality_check == "Yes":
                    it = frappe.get_doc("Item",i.item_code)
                    it.inspection_required_before_purchase = 1
                    it.save()
                    frappe.msgprint("Item Updated")