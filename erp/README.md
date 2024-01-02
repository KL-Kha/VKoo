**What is this Repo for?**

1. For managing source-code of our internal ERP + Website across branches and versions of Odoo.
2. Documenting the evolution of this ERP.
3. Managing coordinates and credentials of production and dev servers.

The internal Odoo-ERP has evolved over 9e, 12c and today is on 16e.

# Credentials

As of 08.12.23, following keys have access to `88.198.107.188` VM. 
```
root@devweberp|pwo
ashant@feather.local, ashant@Ashants-iMac.zyxel.box

odoo16_ee_dev@88.198.107.188
trungvyvo123@gmail.com, ashant@feather.local, ashant@Ashants-iMac.zyxel.box
```

# Coordinates

## Production

- Runs on `88.198.107.188`
- Runs on Docker homed in `/home/odoo16_ee`
- Loads at https://poweron.software/ (and /web)

## Dev

- Runs on `88.198.107.188`
- Runs on Docker homed in `/home/odoo16_ee_dev`
- Loads at https://devweberp.poweron.software/ (and /web)

# ERP Evolution
https://poweron.software/web

# Website Evolution

In Dec. 2023, the decision was made to pivot to a full SaaS model, employing full online customer acquisition methods. Accordingly changes were made to the website, based on `xx` template. The website went through following changes.

- [Website Conversion Optimisation – Price sanitisation, e-Commerce](https://github.com/euroblaze/erp/issues/3)

## v16e
- In this branch we consolidate code pertaining to internal ERP, based on v16e.
- Some very specific backend modules/features are code-repoed here.
- Website https://poweron.software is repoed here.

Also here..
- Issues are specified.
- Figma files are linked.
