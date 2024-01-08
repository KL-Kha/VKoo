/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CalendarRendererCustom } from "./calendar_renderer";
import { CalendarModelCustom } from "./calendar_model";
import { calendarView } from "@web/views/calendar/calendar_view";
import { CalendarArchParserCustom } from "./calendar_arch_parser";


calendarView.Renderer = CalendarRendererCustom
calendarView.Model = CalendarModelCustom
calendarView.ArchParser = CalendarArchParserCustom

registry.category("views").add("group_calendar", calendarView, { force: true });