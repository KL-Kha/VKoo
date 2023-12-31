### Problem

Solar panels are often delivered in [pallettes](https://jcsolarpanels.co.za/wp-content/uploads/2020/07/340W-Solar-Panel-Pallet-JA-Solar-Products.jpg) and [containers](https://hackaday.com/wp-content/uploads/2021/03/dry-storage.jpg). During stock reciepts operation (WH/IN), it is difficult for stock manager to scan these large quantities of products one by one.

### What are Flashlists?

The **Photovoltaic Panels FlashLists** module is designed to import, process, and manage FlashLists - Excel files that contain manufacturer data for photovoltaic (PV) panels, identified uniquely by **serial numbers**. The data is stored in Odoo models, and utilised in WH/IN and WH/OUT workflows.

### Solution

1. Flashlists are uploaded once into Odoo, and serial-numbers of all the PV-panels are available in the `flashlist.data` model.
2. During stock reciepts (WH/IN) and stock delivery (WH/OUT) operations, these serial numbers are assigned to `stock.picking` operations.

### Required Fields in Flashlist Excel-file

Following fields are required in the Excel imported.

- `article_number`: erp article number or supplier's?
- `article_description`:
- `manufacturer`:
- `performance`:
- `serial_number`:
- `pallet_number`:
- `container_number`:
- `order_number`: supplier order number or PO-Nr in ERP?
- `pmpp`:
- `umpp`:
- `impp`:
- `vmpp`:
- `isc`:
- `uoc`:
- `voc`:
- `pmax`:
- `ff`:
- `attachment_id`:
- `product_id`: which id is this?
- `serial_number_optimizer`: 
- Any other fields mandatory?

### Reference

[Original Specification](https://github.com/euroblaze/flashlist/blob/main/spec.md)
