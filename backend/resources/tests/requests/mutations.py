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
