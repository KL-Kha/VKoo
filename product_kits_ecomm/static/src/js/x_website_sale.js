odoo.define('product_kits-addons.website_sale', function (require) {
    'use strict';
    
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');
    const { useService } = require('@web/core/utils/hooks')
    
    var _t = core._t;
    
    publicWidget.registry.WebsiteSale.include({
        /**
         *
         * @override
         */
        _handleAdd: function ($form) {
            var self = this;
            this.$form = $form;
            this.orm = useService("orm");
    
            var productSelector = [
                'input[type="hidden"][name="product_id"]',
                'input[type="radio"][name="product_id"]:checked',
            ];
    
            var productReady = this.selectOrCreateProduct(
                $form,
                parseInt($form.find(productSelector.join(', ')).first().val(), 10),
                $form.find('.product_template_id').val(),
                false
            );
    
            return productReady.then(function (productId) {
                $form.find(productSelector.join(', ')).val(productId);
                // const action =  self.orm.call("product.template", "test_action", [[productId]])
                // console.log('test :' + action)
                self.rootProduct = {
                    product_id: productId,
                    quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
                    product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
                    variant_values: self.getSelectedVariantValues($form.find('.js_product')),
                    no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product'))
                };
    
                return self._onProductReady();
            });
        },
    });
    
    return publicWidget.registry.WebsiteSaleOptions;
    
    });
    