## What this module does?

- Users of the Sales Module can configure the look & feel of their quotations using these "print options".

## Installation

- Pull code from this repo
- Restart the Docker
- Upgrade the module under Apps > Upgrade/Aktualisieren
- Uninistall the 3rd party app `sale_discount_total`, in case it is being included in the runtime.

## What are the print options available to users?

Following print options are available to sales-module users with permissions to create Quotation.

### Logo

- Print logo on the Quotation or not.

### Show prices on quotation

- Show prices in line-items in quotations or not.

### Pre-Text

- Text that is shown before the quotation positions (line items)

### PostText_1

- First textblock that is shown after the quotation positions (line items)

### PostText_2

- Second textblock that is shown after the quotation positions (line items)
- 
![image](https://github.com/euroblaze/quotation_print_options/assets/7826363/03a41704-6be8-49f0-b94e-cf5166a636eb)

### Code Inventory

```
root@hc:/.../quotation_print_options# cloc $(git ls-files)
      17 text files.
      17 unique files.                              
       2 files ignored.

github.com/AlDanial/cloc v 1.82  T=0.02 s (780.9 files/s, 76166.4 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
XML                              7             35             28           1115
Python                           5             32             14            157
PO File                          1              8             20             16
Markdown                         1             11              0             14
YAML                             1              1              1             11
-------------------------------------------------------------------------------
SUM:                            15             87             63           1313
-------------------------------------------------------------------------------
```
