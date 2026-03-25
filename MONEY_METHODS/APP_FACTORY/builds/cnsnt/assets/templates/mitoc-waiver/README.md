MITOC Waiver
============

This repository contains the legal waiver that individuals must sign in order
to participate in the MIT Outing Club. The release may be
[completed online][sign-waiver] in a self-service fashion.


Automated waiver process
------------------------

MITOC uses DocuSign to collect waivers from all participants. The form fields
in our PDF waiver are annotated to support waiver completion from any computer
or mobile device. The process is completely automated, and completed in a few
steps:

1. **Waiver initiation**: The user navigates to [mitoc-trips.mit.edu/profile/waiver/][sign-waiver]
2. **Pre-filling form**: If the user holds an account on
   [MITOC Trips][mitoc-trips], then their waiver information can be pre-filled.
   If they are not an account holder, they simply enter their name and email
   address.
3. **Programmatic request**: When the user submits the form, our servers
   [generate a waiver request][code-mitoc-trips-waivers].
    - If submitting as an account holder, this form request includes pre-filled
      form data (such as their MIT affiliation, emergency contact, etc.).
    - If the user is a minor, a signature is required from their parent or guardian.
      The waiver will not be complete until the guardian has signed the form as well.
    - The waiver request contains an ["event notification"][code-event-notification].
      This field asks DocuSign to notify our API endpoint when the waiver has
      been completed by all parties. Our [always-listening membership API][repo-mitoc-member]
      receives these notifications, and updates our internal database. The exact payload
      that DocuSign sends us is also
      [specified at the time of waiver creation][code-mitoc-member-callback]. We verify
      that the payload originated at DocuSign via [mutual TLS][code-mutual-tls].
    - If the waiver was initiated by an authenticated user, then we include
      [an assertion that their email has already been verified][code-email-known].
4. **Redirection**: If the user holds an account on [MITOC Trips][mitoc-trips],
   they are immediately redirected into the waiver (since their email address
   is known & verified). Otherwise, they receive a link to complete the waiver
   in their inbox.
5. **Completion**: Once the waiver has been signed by the participant (and
   their guardian, if necessary), all parties are notified.
    - Our [membership API][repo-mitoc-member] processes the event. If the
      participant is new to MITOC, then an account is created for them. If they
      are an existing member, then their waiver status & affiliation are
      updated.
    - MITOC, the participant, and the guardian all receive a PDF copy of the
      signed waiver.


Integrating with DocuSign
-------------------------

DocuSign supports importing and exporting Templates from JSON. A
DocuSign ["Template"][docusign-templates] is a document that is intended to be
completed by many different recipients. The Template is defined by an underlying
document, annotated fields within that document, and a number of pre-defined
roles that may complete that document.

[MIT offers DocuSign free of charge to students, faculty, staff, and affiliates][ist-docusign].
To support a system like this one, an MIT affiliate must obtain an account with
elevated privileges to use Templates.


Generating a new waiver revision
--------------------------------
1. Modify `waiver.tex`
2. Run `make`, inspect output at `documents/YYYY-MM-DD.pdf`
3. If satisfied, upload `docusign_templates/YYYY-MM-DD.json` to DocuSign
   (Templates --> New --> Upload Template).
4. Adjust any annotated fields (if necessary)
5. Run `make clean` to remove `pdflatex` artifacts (optional)


Related projects
----------------

- [MITOC Trips][repo-mitoc-trips]: MITOC's trip system - waivers are required to
  participate on all trips, and participants may [sign a new waiver][sign-waiver] here.
- [mitoc-member][repo-mitoc-member]: API that receives callbacks when members pay their
  annual dues or sign a waiver. Upon receipt of a new event, this project updates their account.
- [mitoc-ansible][repo-mitoc-ansible]: Server configuration for the above two projects.


Screenshots
-----------

### Generated document in the DocuSign template editor
![DocuSign template editor][img-edit-docusign-template]

### Roles definition in DocuSign
![Roles defined for the waiver][img-uploaded-template]

### Pre-filling a waiver with profile information
![Waiver completion UI from MITOC Trips][img-sign-authenticated]

### Signing the release as a minor
![Signing the release for participants under 18][img-sign-as-minor]



[ist-docusign]: https://ist.mit.edu/docusign
[docusign-templates]: https://support.docusign.com/guides/ndse-user-guide-working-with-templates

[mitoc-trips]: https://mitoc-trips.mit.edu/
[sign-waiver]: https://mitoc-trips.mit.edu/profile/waiver/

[repo-mitoc-ansible]: https://github.com/DavidCain/mitoc-ansible/
[repo-mitoc-member]: https://github.com/DavidCain/mitoc-member/
[repo-mitoc-trips]: https://github.com/DavidCain/mitoc-trips/

[code-mitoc-trips-waivers]: https://github.com/DavidCain/mitoc-trips/blob/f887160bf6535cd396df8c59432fdc2e01e1be85/ws/waivers.py
[code-event-notification]: https://github.com/DavidCain/mitoc-trips/blob/f887160bf6535cd396df8c59432fdc2e01e1be85/ws/waivers.py#L160
[code-email-known]: https://github.com/DavidCain/mitoc-trips/blob/f887160bf6535cd396df8c59432fdc2e01e1be85/ws/waivers.py#L163
[code-mitoc-member-callback]: https://github.com/DavidCain/mitoc-trips/blob/f8874847aaebd25c74e26bfb83a0334de4b37d94/ws/settings.py#L178
[code-mutual-tls]: https://github.com/DavidCain/mitoc-ansible/blob/5fadcec355894ed58777dd1551df17400932a22d/roles/nginx/templates/member.j2#L70

[img-edit-docusign-template]: https://dcain.me/static/images/mitoc-waiver/edit_docusign_template.png
[img-sign-anonymously]: https://dcain.me/static/images/mitoc-waiver/sign_anonymously.png
[img-sign-as-minor]: https://dcain.me/static/images/mitoc-waiver/sign_as_minor.png
[img-sign-authenticated]: https://dcain.me/static/images/mitoc-waiver/sign_authenticated.png
[img-uploaded-template]: https://dcain.me/static/images/mitoc-waiver/uploaded_template.png
