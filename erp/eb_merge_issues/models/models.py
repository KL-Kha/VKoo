# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger('base.issue.merge.automatic.wizard')
class MergeIssuesLine(models.TransientModel):

    _name = 'base.issue.merge.line'
    _order = 'min_id asc'

    wizard_id = fields.Many2one('base.issue.merge.automatic.wizard', 'Wizard')
    min_id = fields.Integer('MinID')
    aggr_ids = fields.Char('Ids', required=True)

class EbMergeIssues(models.TransientModel):

    _name = 'base.issue.merge.automatic.wizard'
    _description = 'Merge Issues'

    @api.model
    def default_get(self, fields):
        res = super(EbMergeIssues, self).default_get(fields)
        active_ids = self.env.context.get('active_ids')
        if self.env.context.get('active_model') == 'project.issue' and active_ids:
            res['issue_ids'] = active_ids
        return res

    issue_ids = fields.Many2many('project.issue', string='Issues')#'merge_issues_rel', 'merge_id', 'issue_id',)
    user_id = fields.Many2one('res.users', 'Assigned to', index=True)
    dst_issue_id = fields.Many2one('project.issue', string='Destination Issue')
    dst_project = fields.Many2one('project.project', string = "Project")


    @api.multi
    def action_merge_issues(self):
        names=[]
        #write the name of the destination issue because it will overwritten
        if self.dst_issue_id:
            names.append(self.dst_issue_id.name)
        else:
            raise UserError(_("You must select a Destination Issue"))


        desc=[]
        #also write the description of the destination issue because it will be overwritten
        desc.append(self.dst_issue_id.description)
        for id in self.issue_ids:
            for name in id:
            # append the names and desc to the empty lists
                names.append(name.name)
                desc.append(name.description)
                #self.issue_ids.write({'message_ids' : self.dst_issue_id.message_ids})
        #transfering the messages from issue_ids to dst_issue_id
        for message in self.issue_ids:
            for msg_id in message.message_ids:
                msg_id.write({'res_id': self.dst_issue_id.id})

        #Transfer the timesheets from issue_ids to dst_issue_id
        for timesheet in self.issue_ids:
            for ts_id in timesheet.timesheet_ids:
                ts_id.write({'issue_id': self.dst_issue_id.id})
                #the issue id for timesheet is updated with the dst_issue_id.id

        # # #loop the issue_ids and transfer the tag_ids to the dst_issue_id
        # for issue in self.issue_ids:
        #     for tag in issue.tag_ids:
        #         tag.write({'tag_ids': (6, 0, [self.dst_issue_id.id])})



        #no planned hours in issues
        # plan_hours = self.dst_issue_id.planned_hours
        # for hour in self.issue_ids:
        #     for time in hour:
        #         plan_hours+=time.planned_hours
        #Write to dst_issue_id full planned hours from all issues
        #self.dst_issue_id.write({'planned_hours': plan_hours})

        #actual writing to the issues
        transformed_names = ', '.join([unicode(i) for i in names])
        self.dst_issue_id.write({'name' : transformed_names})

        # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), names)

        transformed_desc = ', '.join([unicode(i) for i in desc])
        self.dst_issue_id.write({'description' : transformed_desc})

        # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), desc)
        #Posting a note in the merged and archived issues
        ###################################################################
        #get the base url from ir.config_parameter
        base_url   =  self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #loop all active issues
        for issue in self.issue_ids:
            #post the link to every issue
            issue.message_post(body="This issue has been merged into: " '%s/#id=%s&amp;view_type=form&amp;model=project.issue' % (base_url, self.dst_issue_id.id))

        self.issue_ids.write({'active':False})
        #explicitly write the dst_issue_id TRUE for ACTIVE for security reasons

        self.dst_issue_id.write({'active':True})

        #Check if user has been assigned and if not raise error

        if self.user_id.id:
        #write the Assiged TO user_id
            self.dst_issue_id.write({'user_id' : self.user_id.id})
        elif self.dst_issue_id.user_id.id:
                self.dst_issue_id.write({'user_id' : self.dst_issue_id.user_id.id})
        else:
            raise UserError(_("There is no user assigned to the merged issue, and the destination issue doesn't have assigned user too!!!"))


        #For project_id check if any is given from user, if not use the project_id from dst_issue_id project
        #write the project id to the dst_issue_id
        if self.dst_project:
            self.dst_issue_id.write({'project_id': self.dst_project.id})
        else:
            self.dst_issue_id.write({'project_id': self.dst_issue_id.project_id.id})

        return True
