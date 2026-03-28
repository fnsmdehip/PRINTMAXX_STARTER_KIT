import type { Template } from '../types';

export const templates: Template[] = [
  {
    id: 'intimate-consent',
    name: 'Intimate Consent Agreement',
    description: 'Document mutual consent for intimate activities between adults.',
    category: 'Personal',
    isPremium: true,
    parties: [
      { role: 'Party A', placeholder: 'First person full name' },
      { role: 'Party B', placeholder: 'Second person full name' },
    ],
    termsTemplate: `MUTUAL CONSENT AGREEMENT

This agreement is entered into voluntarily by the undersigned parties on the date indicated below.

1. VOLUNTARY PARTICIPATION
Both parties confirm that they are of legal age and are entering into this agreement of their own free will, without coercion, undue influence, or impairment of any kind.

2. MUTUAL CONSENT
Both parties affirm their mutual, informed, and enthusiastic consent to engage in intimate activities as discussed and agreed upon between themselves. Each party understands they have the absolute right to withdraw consent at any time, for any reason, without consequence.

3. BOUNDARIES AND COMMUNICATION
Both parties agree to respect clearly communicated boundaries. Any activity not explicitly discussed and agreed upon is not covered by this agreement. Both parties commit to open communication before, during, and after any activities.

4. SOBRIETY AFFIRMATION
Both parties confirm they are not under the influence of alcohol, drugs, or any substance that would impair their ability to give informed consent at the time of signing.

5. PRIVACY
Both parties agree to maintain the confidentiality of this agreement and the activities it references. Neither party shall share, distribute, or disclose any details without the explicit written consent of the other party.

6. NO RECORDING
Neither party shall make any audio, video, or photographic recordings without the prior explicit consent of the other party.

7. REVOCABILITY
This consent may be revoked by either party at any time. Revocation of consent is immediate and requires no explanation.

8. ACKNOWLEDGMENT
By signing below, both parties acknowledge they have read, understood, and agree to all terms stated in this document.`,
    detailsPrompts: [
      'Location where this agreement is being signed',
      'Any specific boundaries or conditions discussed',
    ],
  },
  {
    id: 'house-guest-waiver',
    name: 'House Guest Liability Waiver',
    description: 'Protect yourself when hosting guests in your home.',
    category: 'Property',
    isPremium: false,
    parties: [
      { role: 'Host', placeholder: 'Homeowner/tenant name' },
      { role: 'Guest', placeholder: 'Guest full name' },
    ],
    termsTemplate: `HOUSE GUEST LIABILITY WAIVER AND RELEASE

1. ASSUMPTION OF RISK
The Guest acknowledges that staying at the Host's property involves certain inherent risks, including but not limited to: slips, trips, falls, exposure to allergens, pet interactions, pool or recreational equipment use, and other hazards common to residential properties.

2. WAIVER OF LIABILITY
The Guest hereby waives, releases, and discharges the Host from any and all liability, claims, demands, or causes of action arising from injury, illness, property damage, or loss sustained while on the premises, except in cases of gross negligence or intentional misconduct by the Host.

3. PROPERTY CONDITION
The Host has made reasonable efforts to maintain the property in a safe condition. The Guest agrees to report any unsafe conditions immediately and to exercise reasonable care while on the premises.

4. HOUSE RULES
The Guest agrees to abide by all house rules communicated by the Host, including but not limited to: noise levels, smoking restrictions, pet policies, parking arrangements, and use of shared spaces.

5. PERSONAL PROPERTY
The Host is not responsible for loss, theft, or damage to the Guest's personal property while on the premises. The Guest is advised to secure their valuables.

6. GUEST'S RESPONSIBILITIES
The Guest agrees to leave the premises in substantially the same condition as upon arrival, report any damage promptly, and respect the Host's property and neighbors.

7. DURATION
This waiver is effective for the duration of the Guest's stay as agreed upon by both parties.

8. GOVERNING LAW
This agreement shall be governed by the laws of the state in which the property is located.`,
    detailsPrompts: [
      'Property address',
      'Duration of stay (check-in and check-out dates)',
      'Any specific house rules or restrictions',
    ],
  },
  {
    id: 'personal-nda',
    name: 'Personal Non-Disclosure Agreement',
    description: 'Protect confidential information shared between individuals.',
    category: 'Legal',
    isPremium: true,
    parties: [
      { role: 'Disclosing Party', placeholder: 'Person sharing confidential info' },
      { role: 'Receiving Party', placeholder: 'Person receiving confidential info' },
    ],
    termsTemplate: `PERSONAL NON-DISCLOSURE AGREEMENT (NDA)

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any non-public information disclosed by the Disclosing Party to the Receiving Party, whether orally, in writing, electronically, or by any other means. This includes but is not limited to: personal information, financial data, business ideas, creative works, health information, relationship details, and any information marked or identified as confidential.

2. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to:
a) Hold all Confidential Information in strict confidence
b) Not disclose any Confidential Information to any third party without prior written consent
c) Use Confidential Information only for purposes expressly authorized by the Disclosing Party
d) Take reasonable measures to protect the confidentiality of the information, at minimum the same degree of care used to protect their own confidential information

3. EXCLUSIONS
This agreement does not apply to information that:
a) Was publicly known at the time of disclosure
b) Becomes publicly known through no fault of the Receiving Party
c) Was already known to the Receiving Party prior to disclosure
d) Is independently developed by the Receiving Party without use of Confidential Information
e) Is required to be disclosed by law or court order, provided the Receiving Party gives prompt notice

4. TERM
This agreement remains in effect for a period of two (2) years from the date of signing, unless terminated earlier by written mutual consent. Obligations of confidentiality survive termination for information disclosed during the term.

5. RETURN OF MATERIALS
Upon request or termination, the Receiving Party shall promptly return or destroy all materials containing Confidential Information and certify in writing that all copies have been returned or destroyed.

6. REMEDIES
The Disclosing Party shall be entitled to seek injunctive relief in addition to any other available legal remedies for any breach of this agreement.

7. NO LICENSE
Nothing in this agreement grants any license or rights to intellectual property of the Disclosing Party.`,
    detailsPrompts: [
      'General subject matter of confidential information',
      'Specific purposes for which information may be used',
      'Any exclusions or carve-outs to note',
    ],
  },
  {
    id: 'event-host-waiver',
    name: 'Event Host Waiver',
    description: 'Liability waiver for private events and gatherings you host.',
    category: 'Events',
    isPremium: false,
    parties: [
      { role: 'Event Host', placeholder: 'Host/organizer name' },
      { role: 'Attendee', placeholder: 'Attendee full name' },
    ],
    termsTemplate: `EVENT LIABILITY WAIVER AND RELEASE OF CLAIMS

1. EVENT DETAILS
The Attendee acknowledges their voluntary participation in the event organized by the Event Host at the location and date specified below.

2. ASSUMPTION OF RISK
The Attendee understands that participation in this event may involve risks including but not limited to: physical injury, property damage, exposure to communicable diseases, food allergies, alcohol-related incidents, and other hazards associated with social gatherings and events.

3. WAIVER AND RELEASE
The Attendee hereby releases, waives, and discharges the Event Host from any and all liability, claims, demands, actions, or causes of action arising out of or related to any loss, damage, or injury sustained while attending or participating in this event, except where such loss, damage, or injury results from the gross negligence or willful misconduct of the Event Host.

4. INDEMNIFICATION
The Attendee agrees to indemnify, defend, and hold harmless the Event Host from any claims, damages, or expenses arising from the Attendee's own negligence or misconduct during the event.

5. MEDICAL AUTHORIZATION
In the event of a medical emergency, the Attendee authorizes the Event Host to seek emergency medical treatment on their behalf if the Attendee is unable to communicate.

6. PHOTO/VIDEO CONSENT
The Attendee consents to being photographed, filmed, or recorded during the event, and grants the Event Host permission to use such media for personal, non-commercial purposes unless otherwise noted below.

7. ALCOHOL ACKNOWLEDGMENT
If alcohol is served at this event, the Attendee confirms they are of legal drinking age and accepts full responsibility for their alcohol consumption and resulting behavior.

8. PERSONAL PROPERTY
The Event Host is not responsible for lost, stolen, or damaged personal property of attendees.`,
    detailsPrompts: [
      'Event name and description',
      'Event location (full address)',
      'Event date and time',
      'Any specific activities or risks to note',
    ],
  },
  {
    id: 'freelancer-agreement',
    name: 'Freelancer Service Agreement',
    description: 'Simple contract for freelance work between individuals.',
    category: 'Business',
    isPremium: true,
    parties: [
      { role: 'Client', placeholder: 'Person hiring the freelancer' },
      { role: 'Freelancer', placeholder: 'Person providing services' },
    ],
    termsTemplate: `FREELANCER SERVICE AGREEMENT

1. SCOPE OF WORK
The Freelancer agrees to perform the services described in the Details section below ("Services") for the Client. Any work beyond the described scope requires written agreement from both parties and may be subject to additional compensation.

2. COMPENSATION
The Client agrees to pay the Freelancer the amount specified below for the completion of the Services. Payment terms, schedule, and method are as described in the Details section.

3. TIMELINE
The Freelancer shall complete the Services within the timeframe specified below. If delays occur due to factors outside the Freelancer's control, both parties agree to negotiate a reasonable extension in good faith.

4. INTELLECTUAL PROPERTY
Upon full payment, all intellectual property rights in the deliverables created under this agreement shall transfer to the Client. The Freelancer retains the right to display the work in their portfolio unless otherwise agreed.

5. REVISIONS
The scope of work includes up to two (2) rounds of revisions. Additional revisions may be subject to additional charges at the Freelancer's standard hourly rate.

6. CONFIDENTIALITY
Both parties agree to keep confidential any proprietary information shared during the course of this engagement. This obligation survives termination of this agreement.

7. INDEPENDENT CONTRACTOR STATUS
The Freelancer is an independent contractor, not an employee. The Freelancer is responsible for their own taxes, insurance, and benefits.

8. TERMINATION
Either party may terminate this agreement with seven (7) days written notice. Upon termination, the Client shall pay for all work completed up to the termination date.

9. LIABILITY
The Freelancer's total liability under this agreement shall not exceed the total compensation paid. Neither party shall be liable for indirect, consequential, or incidental damages.

10. DISPUTE RESOLUTION
Any disputes arising from this agreement shall first be addressed through good-faith negotiation. If unresolved, disputes shall be settled through mediation or binding arbitration.`,
    detailsPrompts: [
      'Description of services to be performed',
      'Total compensation amount',
      'Payment schedule (e.g., 50% upfront, 50% on completion)',
      'Deadline for completion',
      'Payment method (e.g., bank transfer, PayPal)',
    ],
  },
  {
    id: 'roommate-agreement',
    name: 'Roommate Agreement',
    description: 'Set clear expectations for shared living arrangements.',
    category: 'Property',
    isPremium: false,
    parties: [
      { role: 'Roommate A', placeholder: 'First roommate name' },
      { role: 'Roommate B', placeholder: 'Second roommate name' },
    ],
    termsTemplate: `ROOMMATE AGREEMENT

1. PROPERTY AND TERM
This agreement covers the shared living arrangement at the address specified below for the term indicated. All roommates are equally bound by this agreement.

2. RENT AND UTILITIES
Each roommate agrees to pay their share of rent and utilities as outlined in the Details section. Payments are due on the first of each month. Late payments incur a penalty of $25 after a five-day grace period.

3. SECURITY DEPOSIT
Each roommate's share of the security deposit is specified below. Deductions for damages will be allocated to the responsible party. Shared-space damage costs will be split equally unless a responsible party is identified.

4. SHARED SPACES
Common areas (kitchen, living room, bathroom) shall be kept clean and tidy. Each roommate agrees to clean up after themselves promptly. A cleaning schedule may be established by mutual agreement.

5. QUIET HOURS
Quiet hours are from 10:00 PM to 8:00 AM Sunday through Thursday, and 11:00 PM to 9:00 AM on Friday and Saturday. During quiet hours, noise should be kept to a level that does not disturb other roommates.

6. GUESTS AND OVERNIGHT VISITORS
Roommates may have guests, but overnight guests staying more than three consecutive nights or more than six nights per month require advance notice to and agreement from all roommates.

7. PERSONAL PROPERTY
Each roommate's personal property remains their own. Borrowing another roommate's belongings requires explicit permission. Each roommate is responsible for their own belongings and renter's insurance is recommended.

8. FOOD AND SUPPLIES
Unless agreed otherwise, food is not shared. Shared household supplies (toilet paper, cleaning products, trash bags) will be purchased on a rotating basis or split equally.

9. PARKING
Parking spaces, if available, shall be allocated as described in the Details section.

10. PETS
No pets are allowed without written consent of all roommates. If a pet is approved, the pet owner is solely responsible for all pet-related costs, damages, and cleaning.

11. TERMINATION AND MOVE-OUT
A roommate wishing to leave must provide at least 30 days written notice. The departing roommate is responsible for finding an acceptable replacement or paying their share of rent until the lease term ends or a replacement is found.`,
    detailsPrompts: [
      'Property address',
      'Monthly rent total and each person share',
      'Utility split arrangement',
      'Lease start and end dates',
      'Parking arrangements',
    ],
  },
  {
    id: 'vehicle-lending',
    name: 'Vehicle Lending Agreement',
    description: 'Document terms when lending your vehicle to someone.',
    category: 'Property',
    isPremium: false,
    parties: [
      { role: 'Vehicle Owner', placeholder: 'Owner full name' },
      { role: 'Borrower', placeholder: 'Borrower full name' },
    ],
    termsTemplate: `VEHICLE LENDING AGREEMENT

1. VEHICLE INFORMATION
The Vehicle Owner agrees to lend the vehicle described in the Details section to the Borrower for the period and purposes specified below.

2. CONDITION
The Borrower acknowledges receiving the vehicle in its current condition and agrees to return it in substantially the same condition, normal wear and tear excepted. Both parties should document the vehicle's condition (photos recommended) before and after the lending period.

3. PERMITTED USE
The Borrower shall use the vehicle only for lawful purposes and within the geographic area specified. The vehicle shall not be used for commercial purposes, racing, towing, or any illegal activity.

4. AUTHORIZED DRIVERS
Only the Borrower named in this agreement is authorized to operate the vehicle. The Borrower shall not permit any other person to drive the vehicle without the Owner's prior written consent.

5. INSURANCE
The Borrower confirms they hold a valid driver's license and are covered by insurance that extends to borrowed vehicles. The Borrower is responsible for any deductible amounts and insurance premium increases resulting from incidents during the lending period.

6. FUEL
The Borrower agrees to return the vehicle with at least the same fuel level as when received, or to reimburse the Owner for any fuel consumed.

7. TRAFFIC VIOLATIONS AND FEES
The Borrower is solely responsible for any traffic citations, parking tickets, toll charges, or other fees incurred while in possession of the vehicle.

8. DAMAGE AND LIABILITY
The Borrower assumes full financial responsibility for any damage to the vehicle, excluding normal wear and tear, that occurs during the lending period. This includes collision damage, vandalism, theft, and any damage to third parties or their property.

9. BREAKDOWN OR ACCIDENT
In the event of a breakdown or accident, the Borrower shall immediately notify the Owner and cooperate fully with insurance claims and police reports.

10. RETURN
The Borrower shall return the vehicle to the Owner at the agreed location and time. Failure to return the vehicle as agreed may be reported as unauthorized use.`,
    detailsPrompts: [
      'Vehicle make, model, year, and color',
      'License plate number',
      'VIN (Vehicle Identification Number)',
      'Lending period (start and end dates)',
      'Permitted geographic area of use',
      'Mileage at time of lending',
    ],
  },
  {
    id: 'pet-sitting',
    name: 'Pet Sitting Agreement',
    description: 'Terms for someone caring for your pet while you are away.',
    category: 'Personal',
    isPremium: false,
    parties: [
      { role: 'Pet Owner', placeholder: 'Pet owner full name' },
      { role: 'Pet Sitter', placeholder: 'Sitter full name' },
    ],
    termsTemplate: `PET SITTING AGREEMENT

1. PET INFORMATION
The Pet Owner entrusts the care of the pet(s) described in the Details section to the Pet Sitter for the period specified below.

2. CARE INSTRUCTIONS
The Pet Sitter agrees to follow all care instructions provided by the Pet Owner, including feeding schedules, medication administration, exercise requirements, and any special needs or behavioral considerations.

3. VETERINARY CARE
In the event of illness or injury, the Pet Sitter is authorized to seek veterinary care at the facility specified below. The Pet Owner shall reimburse the Pet Sitter for all reasonable veterinary expenses incurred. For non-emergency situations, the Pet Sitter shall attempt to contact the Pet Owner before seeking treatment.

4. EMERGENCY CONTACT
The Pet Owner shall provide emergency contact information, including their own contact details and an alternate contact person who can make decisions regarding the pet if the Owner is unreachable.

5. COMPENSATION
The Pet Owner agrees to compensate the Pet Sitter as specified in the Details section. Payment is due upon the Owner's return unless otherwise agreed.

6. LIABILITY
The Pet Owner acknowledges that pet care involves inherent risks. The Pet Sitter shall exercise reasonable care but shall not be liable for illness, injury, or death of the pet that occurs despite reasonable care, unless caused by the Pet Sitter's negligence.

7. PROPERTY DAMAGE
If pet sitting occurs at the Pet Sitter's home, the Pet Owner shall be responsible for any damage caused by the pet to the Sitter's property. If at the Owner's home, the Pet Sitter shall exercise reasonable care of the Owner's property.

8. KEY/ACCESS
If the Pet Sitter requires access to the Pet Owner's home, the Owner shall provide necessary keys or access codes. The Pet Sitter agrees not to duplicate keys or share access codes and to return all keys upon completion of the sitting period.

9. SUPPLIES
The Pet Owner shall provide all necessary supplies including food, medication, leashes, carriers, and toys. Any additional supplies purchased by the Pet Sitter shall be reimbursed by the Owner.

10. CANCELLATION
Either party may cancel with at least 48 hours notice. Cancellation with less notice may be subject to a cancellation fee equal to one day's compensation.`,
    detailsPrompts: [
      'Pet name, species, breed, age, and description',
      'Sitting period (start and end dates)',
      'Feeding schedule and food details',
      'Medications and administration instructions',
      'Veterinarian name, address, and phone number',
      'Compensation amount and payment method',
      'Location (sitter home or owner home)',
    ],
  },
  {
    id: 'photo-video-release',
    name: 'Photo/Video Release',
    description: 'Get permission to use someone\'s likeness in photos or videos.',
    category: 'Media',
    isPremium: false,
    parties: [
      { role: 'Photographer/Videographer', placeholder: 'Person taking photos/video' },
      { role: 'Subject', placeholder: 'Person being photographed/filmed' },
    ],
    termsTemplate: `PHOTO AND VIDEO RELEASE FORM

1. GRANT OF RIGHTS
The Subject hereby grants the Photographer/Videographer (and their assigns, licensees, and successors) the irrevocable and unrestricted right to use, reproduce, publish, and distribute photographs, video recordings, and any other visual media ("Media") containing the Subject's likeness, voice, or image for the purposes described below.

2. PERMITTED USES
The Media may be used for the purposes checked or described in the Details section. Common uses include:
- Personal/non-commercial use
- Social media posting
- Portfolio and promotional materials
- Commercial advertising and marketing
- Editorial and journalistic purposes
- Educational materials

3. COMPENSATION
The Subject acknowledges that compensation, if any, for this release is as described in the Details section. If no compensation is specified, the Subject agrees that this release is provided without monetary consideration.

4. NO APPROVAL REQUIRED
The Subject waives any right to inspect or approve the finished product or the advertising copy that may be used in connection with the Media, unless otherwise specified below.

5. NAME AND LIKENESS
The Photographer/Videographer may use the Subject's name in connection with the Media unless the Subject indicates otherwise in the Details section.

6. MODIFICATIONS
The Subject consents to reasonable digital editing, color correction, cropping, and compositing of the Media, provided such modifications do not misrepresent the Subject in a defamatory manner.

7. RELEASE OF CLAIMS
The Subject releases the Photographer/Videographer from any claims arising from the use of the Media as described herein, including claims for invasion of privacy, defamation, or right of publicity.

8. DURATION
This release is effective in perpetuity unless a specific duration is noted in the Details section.

9. MINORS
If the Subject is under 18, a parent or legal guardian must sign this release on their behalf.`,
    detailsPrompts: [
      'Date and location of photography/filming',
      'Description of the project or event',
      'Specific permitted uses (check all that apply)',
      'Compensation amount (if any)',
      'Any restrictions on use',
      'Duration of release (if not perpetual)',
    ],
  },
  {
    id: 'property-access',
    name: 'Property Access Agreement',
    description: 'Grant temporary access to your property for specific purposes.',
    category: 'Property',
    isPremium: false,
    parties: [
      { role: 'Property Owner', placeholder: 'Owner full name' },
      { role: 'Accessor', placeholder: 'Person granted access' },
    ],
    termsTemplate: `PROPERTY ACCESS AGREEMENT

1. GRANT OF ACCESS
The Property Owner grants the Accessor temporary, revocable access to the property described in the Details section for the specific purpose and duration stated below.

2. PURPOSE
Access is granted solely for the purpose described in the Details section. The Accessor shall not use the property for any other purpose without prior written consent from the Owner.

3. ACCESS PERIOD
Access is permitted during the dates and times specified in the Details section. The Accessor shall not access the property outside of these designated times without prior arrangement.

4. CONDITIONS OF ACCESS
The Accessor agrees to:
a) Exercise reasonable care while on the property
b) Not cause damage to the property or any structures, fixtures, or improvements
c) Not remove any items from the property without written permission
d) Follow all safety guidelines and restrictions communicated by the Owner
e) Not grant access to any third parties without the Owner's consent
f) Leave the property in the same condition as found

5. LIABILITY AND INDEMNIFICATION
The Accessor assumes all risk associated with accessing the property. The Accessor shall indemnify and hold harmless the Property Owner from any claims, damages, or injuries arising from the Accessor's use of the property, except those caused by the Owner's gross negligence.

6. INSURANCE
The Accessor is responsible for maintaining adequate insurance coverage for their activities on the property. Proof of insurance may be required by the Owner.

7. DAMAGE AND REPAIR
The Accessor shall immediately report any damage to the property and shall be financially responsible for repairs or replacement of any damage caused during their access.

8. REVOCATION
The Property Owner reserves the right to revoke access at any time for any reason with reasonable notice. In emergency situations, access may be revoked immediately.

9. KEYS AND SECURITY
If keys, codes, or other security access is provided, the Accessor shall not duplicate these and shall return all physical keys upon termination of this agreement.`,
    detailsPrompts: [
      'Property address and description',
      'Specific purpose of access',
      'Access dates and permitted hours',
      'Areas of property accessible',
      'Any specific restrictions or safety requirements',
    ],
  },
  {
    id: 'digital-content-license',
    name: 'Digital Content License',
    description: 'License digital content (code, designs, writing) to another person.',
    category: 'Business',
    isPremium: false,
    parties: [
      { role: 'Licensor', placeholder: 'Content creator/owner name' },
      { role: 'Licensee', placeholder: 'Person receiving the license' },
    ],
    termsTemplate: `DIGITAL CONTENT LICENSE AGREEMENT

1. CONTENT DESCRIPTION
The Licensor grants the Licensee a license to use the digital content described in the Details section ("Content") subject to the terms and conditions of this agreement.

2. LICENSE GRANT
Subject to the terms herein, the Licensor grants the Licensee a non-exclusive, non-transferable license to use the Content for the purposes described in the Details section.

3. LICENSE TYPE
The license type is as specified in the Details section:
- Personal Use Only: Content may be used for personal, non-commercial purposes only
- Commercial Use: Content may be used for commercial purposes, including in products or services
- Extended Commercial: Content may be used for commercial purposes including for resale as part of a substantially different product

4. RESTRICTIONS
Unless explicitly permitted, the Licensee shall NOT:
a) Redistribute, resell, or sublicense the Content in its original form
b) Claim authorship or ownership of the Content
c) Use the Content in a manner that is defamatory, obscene, or illegal
d) Remove any copyright notices, watermarks, or attribution from the Content
e) Use the Content to train artificial intelligence or machine learning models

5. ATTRIBUTION
If required (as specified in Details), the Licensee shall provide appropriate credit to the Licensor in the manner specified.

6. INTELLECTUAL PROPERTY
All intellectual property rights in the Content remain with the Licensor. This license does not transfer ownership.

7. WARRANTY
The Licensor warrants that they are the rightful owner of the Content and have the authority to grant this license. The Content is provided "as is" without any other warranties.

8. TERM AND TERMINATION
This license is effective from the date of signing for the duration specified. The Licensor may terminate this license if the Licensee breaches any term. Upon termination, the Licensee must cease all use of the Content and destroy any copies.

9. COMPENSATION
Compensation for this license is as described in the Details section.

10. LIMITATION OF LIABILITY
The Licensor's total liability under this agreement shall not exceed the total license fee paid by the Licensee.`,
    detailsPrompts: [
      'Description of digital content being licensed',
      'License type (Personal, Commercial, Extended Commercial)',
      'License duration (e.g., perpetual, 1 year)',
      'License fee/compensation',
      'Attribution requirements (if any)',
      'Any specific usage restrictions',
    ],
  },
];

export function getTemplate(id: string): Template | undefined {
  return templates.find((t) => t.id === id);
}

export function getFreeTemplates(): Template[] {
  return templates.filter((t) => !t.isPremium);
}

export function getPremiumTemplates(): Template[] {
  return templates.filter((t) => t.isPremium);
}
