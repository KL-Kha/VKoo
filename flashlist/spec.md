# PV Module Flashlists

## 1. Introduction

The PV Module FlashLists is an Odoo module designed to import, process, and manage FlashLists - excel files that contain manufacturer data for photovoltaic (PV) modules identified uniquely by serial numbers. The data is stored on an Odoo server and integrated into Odoo ERP models.

## 2. General Description

### 2.1 Product Perspective

The PV Module/FlashLists module will be a part of the existing Odoo ERP system, augmenting its capabilities by adding PV module inventory management through flash lists.

### 2.2 Product Functions

The PV Module/Lists will:

- Import flash lists from XL files.
- Store uploaded flash lists on the Odoo server.
- Import data from flash lists into Odoo models, making it searchable and listable.
- Track stock in and out of the warehouse using FlashLists.
- ~Match and connect flash lists with corresponding purchase orders.~

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interface

The PV Module/FlashLists should integrate with the existing Odoo's user interface and present options to import and manage flash lists.

### ~3.2 Performance~

~The PV Module/Lists should be capable of handling multiple flash lists at the same time without impacting system performance.~

### 3.3 Design, UI/UX

The PV Module/Lists must comply with Odoo's design and UI/UX standards.

## 4. Features

### 4.1 Flash List Import on Product 

The system should provide functionality to import flash lists from XL files. The imported data should be stored on the Odoo server and made available for search and listing in Odoo models.

![2023-09-28_10-40-04](https://github.com/euroblaze/flashlist/assets/7826363/db8dcc61-0ca4-46ee-b9be-717994bed8ee)


### 4.2 Inventory Management

The system should allow the use of flash list data for tracking stock in and out of the warehouse. When a flash list is linked to a product, it is further likable to a confirmed purchase order and/or a confirmed WH-IN delivery note in the inventory management module.

### 4.3 WH-IN Order Linking

The system should allow flash lists to be  linked to a WH-IN in the Odoo ERP system. This should facilitate the input of freshly arrived stock into the inventory.

### 4.4 Serial Numbers from Flashlists

1. Flashlists carry serial numbers. These should be specifically assigned to various material-movement processes where products are utilised, ex. WH-OUT delivery operations, Installation Documentation etc.
2. Technical parameters from Flashlists will be stored on an extension of the `stock.quant` model, for ex. `stock.quant.panel_technical_params`.

![2023-09-28_10-53-09](https://github.com/euroblaze/flashlist/assets/7826363/a85c4dad-689a-4d4b-89a7-1754874fef44)


### 4.5 Flashlist Management 

1. all FlashLists can be viewed in a list view. columns are name of file, date of upload, manufacturer, a download button. The manufacturer can be changed by user (select from contacts columns are name of file, date of upload, manufacturer, a download button. The manufacture can be changed by user. A mini module should facilitate the.).

2. Flash lists can be deleted by inventory admin. All other users can upload them.

3. each line in a flash list is databased. 10 columns are stored and searchable.

4. The serial numbers uploaded by flash lists are listed in Odoo's standard sequence and lot number views. 

![2023-09-28_10-43-00](https://github.com/euroblaze/flashlist/assets/7826363/39766b81-0e92-4cec-b771-0efd749f9338)
