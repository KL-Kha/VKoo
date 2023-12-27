odoo.define('product_kits.ProductConfiguratorFormController', function (require) {
    "use strict";

var core = require('web.core');
var _t = core._t;

var ProductConfiguratorFormController = require('sale_product_configurator.ProductConfiguratorFormController');

ProductConfiguratorFormController.include({
    _onButtonClicked: function (event) {
        if (event.stopPropagation) {
            event.stopPropagation();
        }
        var attrs = event.data.attrs;
        if (attrs.class === 'btn-primary o_sale_product_configurator_configure') {
            var self = this;
            var $modal = this.$el;
            var productSelector = [
                'input[type="hidden"][name="product_id"]',
                'input[type="radio"][name="product_id"]:checked'
            ];
            var product_id = parseInt($modal.find(productSelector.join(', ')).first().val(), 10);
            var quantity = parseFloat($modal.find('input[name="add_qty"]').val() || 1);
            var context = _.extend({}, event.data.record.context, {'product_id': product_id}, {'quantity': quantity});

            this._rpc({
                model: 'sale.product.configurator',
                method: 'product_configurator',
                args: [event.data.record_id],
                context: context,
            }).then(function (res_id) {
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'add.bundle.wizard',
                    views: [[false, 'form']],
                    res_id: res_id,
                    target: 'new',
                    context: context,
                });
            });
        } else {
            if (attrs.special === 'cancel') {
                this._super.apply(this, arguments);

            } else {
                if (!this.$el
                    .parents('.modal')
                    .find('.o_sale_product_configurator_add')
                    .hasClass('disabled')) {
                    this._handleAdd();
                }
            }

        }
    },
});
}
);
