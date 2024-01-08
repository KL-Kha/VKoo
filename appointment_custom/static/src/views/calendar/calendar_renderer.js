/** @odoo-module **/

import { CalendarCommonRendererCustom } from "./calendar_common_renderer";
import { CalendarRenderer } from "@web/views/calendar/calendar_renderer";

export class CalendarRendererCustom extends CalendarRenderer {

}

CalendarRendererCustom.components = {
    ...CalendarRenderer.components,
    day: CalendarCommonRendererCustom,
};
CalendarRendererCustom.template = "web.CalendarRenderer";