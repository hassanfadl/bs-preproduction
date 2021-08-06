odoo.define('website_customisation.website_customisation', function (require) {
    'use strict';

    $(document).ready(function()
    {
        $(document).on('contextmenu', 'img', function(e){
            return false;
        });
    });


});