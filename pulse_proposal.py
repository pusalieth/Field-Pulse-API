# All data fields for the invoice object

invoice_data = {"_id": "",
                "customer_id": "",
                "job_id": None,
                "status": 2,
                "notes": "",
                "invoiced_date": "",
                "due_date": None,
                "cuid": None,
                "tax_rate": "",
                "created_at": None,
                "items": [],
                "line_items": [{"line_number": 0,
                                "line_type": "item",
                                "line_title": "",
                                "description": "",
                                "line_price_visibility": "all",
                                "line_visibility": "all",
                                "line_components": [{"_id": "",
                                                     "unit_price": "",
                                                     "quantity": "",
                                                     "taxable": False,
                                                     "title": "",
                                                     "description": "",
                                                     "unit_cost": "",
                                                     "type": "",
                                                     "sku": "",
                                                     "hidden": False,
                                                     "unit_measure": "",
                                                     "tax_rate": "0",
                                                     "xero_sales_account": None,
                                                     "xero_tax_account": None
                                                     }]
                                }],
                "subtotal": "0.00",
                "tax": "0.00",
                "amount_paid": "0.00",
                "amount_unpaid": "0.00",
                "qbo_id": 0,
                "last_qbo_sync": None,
                "failed_sync": False,
                "invoice_show_line_item_unit_price": False,
                "invoice_show_line_item_qty": False,
                "invoice_show_line_item_taxed": False,
                "invoice_show_line_item_total": False,
                "invoice_show_line_item_desc": True,
                "invoice_show_total_tax": False,
                "invoice_use_contract": True,
                "contract_id": "",
                "author_id": None,
                "project_id": None,
                "deleted_at": "",
                "invoice_show_job_title": False,
                "invoice_show_job_location": False,
                "invoice_show_assigned_members": False,
                "invoice_show_author": True,
                "invoice_contract_signature_lines": 1,
                "commission_type": 1, # boolean
                "commission_percent": "", # whole number
                "commission": "0", # actual number
                "invoice_show_service_address": True,
                "invoice_show_line_item_sku": False,
                "invoice_amount_due_display_type": "",
                "invoice_amount_due_display_value": "0",
                "estimate_status": 5,
                "expenses": [],
                "line_discount": None,
                "line_surcharge": None,
                "total": "0.00",
                "title": "Customer Proposal",
                "invoice_pdf_title": ""}
