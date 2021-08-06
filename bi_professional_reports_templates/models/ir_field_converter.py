# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, api
REFERENCING_FIELDS = {None, 'id', '.id'}
def only_ref_fields(record):
    return {k: v for k, v in record.items() if k in REFERENCING_FIELDS}
def exclude_ref_fields(record):
    return {k: v for k, v in record.items() if k not in REFERENCING_FIELDS}


class IrFieldsConverterInherited(models.AbstractModel):
    _inherit = 'ir.fields.converter'

    @api.model
    def for_model(self, model, fromtype=str):
        """ Returns a converter object for the model. A converter is a
        callable taking a record-ish (a dictionary representing an odoo
        record with values of typetag ``fromtype``) and returning a converted
        records matching what :meth:`odoo.osv.orm.Model.write` expects.

        :param model: :class:`odoo.osv.orm.Model` for the conversion base
        :returns: a converter callable
        :rtype: (record: dict, logger: (field, error) -> None) -> dict
        """
        # make sure model is new api
        model = self.env[model._name]

        converters = {
            name: self.to_field(model, field, fromtype)
            for name, field in model._fields.items()
        }

        def fn(record, log):
            attribute_obj = self.env['product.attribute']
            attribute_value_obj = self.env['product.attribute.value']
            converted = {}
            for field, value in record.items():
                if field in REFERENCING_FIELDS:
                    continue
                if not value:
                    converted[field] = False
                    continue
                try:
                    converted[field], ws = converters[field](value)
                    for w in ws:
                        if isinstance(w, str):
                            # wrap warning string in an ImportWarning for
                            # uniform handling
                            w = ImportWarning(w)
                        log(field, w)
                except (UnicodeEncodeError, UnicodeDecodeError) as e:
                    log(field, ValueError(str(e)))
                except ValueError as e:
                    log(field, e)
            if 'attribute_id' in converted and 'value_ids' in converted:
                attribute_id = attribute_obj.browse(converted['attribute_id'])
                values_list = []
                for value in converted['value_ids']:
                    attr_value_list = []
                    for value_attr in value[2]:
                        attribute_value_id = attribute_value_obj.browse(value_attr)
                        attribute_original_id = attribute_value_obj.search([('attribute_id', '=', attribute_id.id),
                                                                            ('name', '=', attribute_value_id.name)], limit=1)
                        if attribute_original_id:
                            attr_value_list.append(attribute_original_id.id)
                    if attr_value_list:
                        values_list.append((value[0], value[1], attr_value_list))
                if values_list:
                    converted['value_ids'] = values_list
            if 'attribute_line_ids' in converted:
                update_list = []
                delete_list = []
                attribute_line_ids_list = converted['attribute_line_ids']
                for conversion in attribute_line_ids_list:
                    converted_list = []
                    attribute_id = attribute_obj.browse(conversion[2]['attribute_id'])
                    for attribute_value in conversion[2]['value_ids']:
                        attr_value_list = []
                        for value_attr in attribute_value[2]:
                            attribute_value_id = attribute_value_obj.browse(value_attr)
                            attribute_original_id = attribute_value_obj.search([('attribute_id', '=', attribute_id.id),
                                                                            ('name', '=', attribute_value_id.name)], limit=1)
                            if attribute_original_id:
                                attr_value_list.append(attribute_original_id.id)
                        if attr_value_list:
                            converted_list.append((attribute_value[0], attribute_value[1], attr_value_list))
                    if converted_list:
                        attribute_values = conversion[2]
                        attribute_values['value_ids'] = converted_list
                        update_list.append((conversion[0], conversion[1], attribute_values))
                        delete_list.append(conversion)
                for delete in delete_list:
                    attribute_line_ids_list.remove(delete)
                for update in update_list:
                    attribute_line_ids_list.append(update)
                converted['attribute_line_ids'] = attribute_line_ids_list
            return converted

        return fn
