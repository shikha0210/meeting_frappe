import frappe
from frappe import _
from frappe.utils import nowdate, add_days
@frappe.whitelist()
def send_invitation_emails(meeting):
    meeting=frappe.get_doc("Meeting",meeting)
    meeting.check_permission("email")

    if meeting.status=="Planned":
        frappe.sendmail(
            recipients=[d.attendee for d in meeting.attendees],
            sender=frappe.session.user,
            subject=meeting.title,
            message=meeting.invitation_message,
            reference_doctype=meeting.doctype,
            reference_name=meeting.name,
            #as_bulk=True
        )

        meeting.status = "Invitation Sent"
        meeting.save()

        frappe.msgprint(_("Invitation Sent"))
    
    else:
        frappe.msgprint(_("Meeting status must be 'Planned'"))
def make_orientation_meeting(doc,method):
    meeting= frappe.get_doc({
        "doctype": "Meeting",
        "title": "Orientation for {0}". format(doc.first_name),
        "date": add_days(nowdate(),1),
        "from_time": "09:00",
        "to_time": "09:30",
        "status":"Planned",
        "attendees":[{
            "attendee": doc.name
        }]
    })
    meeting.flags.ignore_permissions = True
    meeting.insert()

    frappe.msgprint(_("Orentation meeting created"))