# Google Spreadsheets to Odoo Importer

## Overview

This package provides a set of client-scripts to facilitate the import of data from Google Spreadsheets into Odoo, a popular open-source ERP and CRM platform. The scripts are designed to streamline the process of transferring data, ensuring compatibility between Google Sheets and Odoo.

## Prerequisites

Before installing the module, ensure that you have the following external dependencies for Python installed:

- pandas
- gspread
- oauth2client

You can install these dependencies using the following command:

```bash
pip install pandas gspread oauth2client

## Google Cloud Platform Configuration
1. Create Service Account
--Go to https://console.cloud.google.com/iam-admin/serviceaccounts
--Create a new service account and download the JSON credential file.

2. Enable Google Sheets API
--Go to https://console.cloud.google.com/apis/api/sheets.googleapis.com
--Enable the Google Sheets API.