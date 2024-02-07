CREATE_RESOURCE = """
    mutation($input: ResourceInput!){
        createResource(input: $input){
            id
            name
            description
            availableTime
            startDate
            endDate
            location
            user{
                email
            }
        }
    }
"""

DELETE_RESOURCE = """
    mutation($id: UUID!){
        deleteResource(id: $id)
    }
"""

UPDATE_RESOURCE = """
    mutation($input: UpdateResourceInput!){
        updateResource(input: $input){
            id
            name
            description
            availableTime
            startDate
            endDate
            location
            user{
                email
            }
        }
    }
"""

CREATE_DAY_AVAILABILITY = """
    mutation($input:DayAvailabilityInput!, $resourceId:UUID!){
        createDayAvailability(input:$input, resourceId:$resourceId){
            resource{
                name
            }
            id
            day
            startTime
            endTime
        }
    }
"""

DELETE_DAY_AVAILABILITY = """
    mutation($id: UUID!){
        deleteDayAvailability(id: $id)
    }
"""

UPDATE_DAY_AVAILABILITY = """
    mutation($input: UpdateDayAvailabilityInput!){
        updateDayAvailability(input: $input){
             id
            resource{
                name
            }
            day
            startTime
            endTime
        }
    }
"""
