# SRS for Invoice PrintOptions Module in Odoo 15

## Introduction
This document outlines the software requirements for the `invoice_printoptions` module extension for Odoo version 15. 
This extension provides various configuration options that enhance the invoice generation functionality, allowing users to customize the look, feel, and data output on PDF invoices.

## Features

### 1. Logo Position

The user should be able to determine the position of the company logo on the invoice. The module should provide four options:

    a. Display logo on the left
    b. Display logo on the right
    c. Display logo in the middle
    d. Do not display the logo

### 2. PreText

- The user should have the option to input custom text that will appear before the invoice line items. 
- This could be used for a personalized message, legal information, or any other relevant details.
- Implement Dynamic Placeholders for contextualisation and personalisation.

### 3. PostText

- Similarly, the user should have the ability to include custom text after the line items. 
- This could be used for additional notes, terms and conditions, etc.
- Implement Dynamic Placeholders for contextualisation and personalisation.

### 4. Page Output

The output PDF of the invoice should be in A4 size.

## Non-Functional Requirements

### 1. Modularity

This module should be built as an independent extension and should not conflict with other modules or existing functionalities of Odoo version 15.

### 2. Compatibility

- This module should be compatible with Odoo version 15 Community and Enterprise.
- The output of Invoice PDFs on any Odoo 15 instance must be same/equivalent when this module is installed.

### 3. Performance

- This module should not significantly degrade the performance of Odoo instance.
- The standard invoice print menus under "Print" on Detail View should be overwritten.

## Deliverables

The deliverables of this project will be:

1. The Python source code for the module.
2. The XML files necessary for the adaptable invoice PDF packaged together with the module.
3. Installation documentation, usage instructions and guidance for future programmers of the module.

## Test Case

The 'Knock Out' (KO) test case would be to install this module onto various instances of Odoo version 15 and validate that the invoice customization options work equivalently, and the output is identical across all instances.
