/** @odoo-module **/
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { _t } from "@web/core/l10n/translation";
import { renderToString } from "@web/core/utils/render";
const { DateTime } = luxon;

export class CalendarCommonRendererCustom extends CalendarCommonRenderer {

    getHeaderHtml(date) {
        const scale = this.props.model.scale;
        const {
            weekdayShort: weekdayShort,
            weekdayLong: weekdayLong,
            day,
        } = DateTime.fromJSDate(date);
        const group_by = this.props.model.group_by;
        let resource = false
        if (group_by) {
            resource = this.props.model.groupRecordsMap[day]
        }
        return renderToString(this.constructor.headerTemplate, {
            weekdayShort,
            weekdayLong,
            day,
            scale,
            group_by,
            resource
        });
    }

    get options() {
        let options = super.options;
        if (this.props.model.scale == 'day' && this.props.model.group_by) {
            options.defaultView = "timeGrid"
            options.dayCount = this.props.model.group_records.length
            let day = this.props.model.date.c.day
            let data = {}
            for (let i = 0; i < options.dayCount; i++) {
                data[day] = this.props.model.group_records[i]
                day++;
            }
            this.props.model.groupRecordsMap = data
        }
        return options
    }

    fcEventToRecord(event) {
        var res = super.fcEventToRecord(event)
        if (this.props.model.scale == 'day' && this.props.model.group_by) {
            res.appointment_resource_id = this.props.model.groupRecordsMap[res.start.c.day].id
            let day = this.props.model.date.c.day
            res.start = res.start.minus({ days: res.start.c.day - day })
            if (res.end) { res.end = res.end.minus({ days: res.end.c.day - day }) }
        }
        return res
    }

    convertRecordToEvent(record) {
        if (this.props.model.scale != 'day' || this.props.model.group_by == false) {
            return super.convertRecordToEvent(record)
        }

        const allDay = record.isAllDay || record.end.diff(record.start, "hours").hours >= 24;
        let dayMapped = Object.keys(this.props.model.groupRecordsMap).find(day => this.props.model.groupRecordsMap[day].id == record.appointment_resource_id);
        let day = this.props.model.date.c.day
        let start = record.start.plus({ days: dayMapped - day });
        let end = record.end.plus({ days: dayMapped - day });

        return {
            id: record.id,
            title: record.title,
            start: start.toISO(),
            end: end.toISO(),
            allDay: allDay,
        };
    }
}

CalendarCommonRendererCustom.headerTemplate = "appointment_custom.CalendarCommonRendererHeader";