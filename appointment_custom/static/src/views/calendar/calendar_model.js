/** @odoo-module **/
import { CalendarModel } from "@web/views/calendar/calendar_model";

export class CalendarModelCustom extends CalendarModel {

    get group_by() {
        return this.meta.group_by;
    }

    get group_records() {
        return this.meta.group_records;
    }

    async load(params = {}) {
        this.meta.group_records = await this.loadGroupRecords();
        await super.load(params)
    }

    async loadGroupRecords() {
        if (this.group_by && 'relation' in this.fields[this.group_by]) {
            const resModel = this.fields[this.group_by].relation
            return this.orm.searchRead(resModel, [], ['id', 'name']);
        }
        return []
    }

    async loadRecords(data) {
        const rawRecords = await this.fetchRecords(data);
        const records = {};
        for (const rawRecord of rawRecords) {
            if (this.group_by) {
                if (rawRecord.appointment_resource_id) {
                    records[rawRecord.id] = this.normalizeRecord(rawRecord);
                }
            } else {
                records[rawRecord.id] = this.normalizeRecord(rawRecord);
            }
        }
        return records;
    }

    normalizeRecord(rawRecord) {
        var res = super.normalizeRecord(rawRecord)
        res.appointment_resource_id = rawRecord.appointment_resource_id ? rawRecord.appointment_resource_id[0] : false
        return res
    }

    buildRawRecord(partialRecord, options = {}) {
        var res = super.buildRawRecord(partialRecord, options)
        if (partialRecord.appointment_resource_id) {
            res.appointment_resource_id = partialRecord.appointment_resource_id
        }
        return res
    }

    makeContextDefaults(rawRecord) {
        var res = super.makeContextDefaults(rawRecord);
        if (rawRecord.appointment_resource_id) {
            res.default_appointment_resource_id = rawRecord.appointment_resource_id
        }
        return res
    }
}