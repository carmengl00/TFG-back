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

CREATE_OR_UPDATE_AVAILABILITY = """
    mutation($input:CreateOrUpdateAvailabilityInput!){
        createOrUpdateAvailability(input:$input)
    }
"""

DELETE_DAY_AVAILABILITY = """
    mutation($id: UUID!){
        deleteDayAvailability(id: $id)
    }
"""

DELETE_ALL_AVAILABILITIES = """
    mutation($resourceId: UUID!){
        deleteAllAvailabilities(resourceId:$resourceId)
    }
"""
