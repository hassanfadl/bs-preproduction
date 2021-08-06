odoo.define('website_customisation.recently_viewed', function (require) {
    var publicWidget = require('web.public.widget');
    publicWidget.registry.productsRecentlyViewedSnippet.include({
        xmlDependencies: (publicWidget.registry.productsRecentlyViewedSnippet.prototype.xmlDependencies || []).concat(
            ['/website_customisation/static/src/xml/price_hide.xml']
        ),
    });
});