import datetime
from uuid import UUID

from base.utils import send_mail
import strawberry

from resources.models import Resource
from slots.graphql.types import EmailResponse, ReservedSlotType
from slots.models import ReservedSlot
from strawberry_django_jwt.decorators import login_required

from .inputs import CreateReservedSlotInput, SendEmailReservationInput


@strawberry.type
class ReservedSlotMutation:
    @strawberry.field(description="Creates a reserved slot")
    def create_reserved_slot(self, input: CreateReservedSlotInput) -> ReservedSlotType:
        resource = Resource.objects.get(id=input.resource_id)
        start_datetime = datetime.datetime.combine(input.day, input.start_time)
        end_datetime = datetime.datetime.combine(input.day, input.end_time)

        reserved_slot = ReservedSlot.objects.create(
            resource=resource,
            name=input.name,
            description=input.description,
            email=input.email,
            start_time=start_datetime,
            end_time=end_datetime,
        )
        return reserved_slot
    
    @strawberry.field(description="Deletes a reserved slot")
    @login_required
    def delete_reserved_slot(self, id: UUID) -> bool:
        ReservedSlot.objects.get(id=id).delete()
        return True
    
    @strawberry.field(description="Send an email to the user of a reserved slot")
    def send_email_to_reserved_slot_user(input: SendEmailReservationInput) -> EmailResponse:
        try:
            context = {
                'resource_description': input.resource_description,
                'resource_name': input.resource_name,
                'available_time': input.available_time,
                'location': input.location,
                'start_time': input.start_time,
                'end_time': input.end_time,
                'first_name': input.first_name,
                'last_name': input.last_name,
                'email': input.email,
                'description': input.description,
                'admin_email': input.admin_email,
            }
            send_mail(
                subject_template_name="reservation/subject_template.txt",
                email_template_name="reservation/email_template.txt",
                context=context,
                from_email=None,
                to_email=input.email,
                html_email_template_name="reservation/email_template.html",
            )

            return EmailResponse(success=True, message="Correo electrónico enviado exitosamente")
        except Exception as e:
            return EmailResponse(success=False, message=str(e))