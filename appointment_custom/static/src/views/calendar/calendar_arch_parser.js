/** @odoo-module **/
import { CalendarArchParser, CalendarParseArchError } from "@web/views/calendar/calendar_arch_parser";
import { visitXML } from "@web/core/utils/xml";

export class CalendarArchParserCustom extends CalendarArchParser {

    parse(arch, models, modelName) {
        let params = super.parse(arch, models, modelName);
        let group_by = "appointment_resource_id";

        return {
            ...params,
            group_by
        }
    }
}