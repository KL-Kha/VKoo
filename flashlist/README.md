### Problem

Solar panels are often delivered in [pallettes](https://jcsolarpanels.co.za/wp-content/uploads/2020/07/340W-Solar-Panel-Pallet-JA-Solar-Products.jpg) and [containers](https://hackaday.com/wp-content/uploads/2021/03/dry-storage.jpg). During stock reciepts operation (WH/IN), it is difficult for stock manager to scan these large quantities of products one by one.

### What are Flashlists?

The **Photovoltaic Panels FlashLists** module is designed to import, process, and manage FlashLists - Excel files that contain manufacturer data for photovoltaic (PV) panels, identified uniquely by **serial numbers**. The data is stored in Odoo models, and utilised in WH/IN and WH/OUT workflows.

### Solution

1. Flashlists are uploaded once into Odoo, and serial-numbers of all the PV-panels are available in the `flashlist.data` model.
2. During stock reciepts (WH/IN) and stock delivery (WH/OUT) operations, these serial numbers are assigned to `stock.picking` operations.

### Required Fields in Flashlist Excel-file

Following fields are required in the Excel imported.

- `article_number`: Supplier's article number
- `article_description`: Supplier's article description
- `manufacturer`: Supplier's name 
- `performance`: Performance ratio of product 
- `serial_number`: Serial number of product lot
- `pallet_number`: Pallet number of product
- `container_number`: Container Number of product
- `order_number`: Supplier's container order number 
- `pmpp`: Pmpp value of product (Technical parameter)
- `umpp`: Umpp value of product (Technical parameter)
- `impp`: Impp value of product (Technical parameter)
- `vmpp`: Vmpp value of product (Technical parameter)
- `isc`: Isc value of product (Technical parameter)
- `uoc`: Uoc value of product (Technical parameter)
- `voc`: Voc value of product (Technical parameter)
- `pmax`: Pmax value of product (Technical parameter)
- `ff`: Fill facter value of product (Technical parameter)
- `attachment_id`: Name of imported file
- `product_id`: Display name of product (if not existing, it will be automatically created)

### Reference

[Original Specification](https://github.com/euroblaze/flashlist/blob/main/spec.md)
