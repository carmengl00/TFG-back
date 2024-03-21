RESOURCES_ITEMS = """
    query($pagination: PaginationInput!){
        myResources(pagination: $pagination){
            pageInfo{
                page
                pages
                totalResults
            }
            edges{
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
    }

"""

RESOURCE_ITEM = """
    query($id:UUID!){
        resource(id:$id){
            user{
                email
            }
            id
            name
            description
            availableTime
            startDate
            endDate
            location
        }
    }
"""

DAY_AVAILABILITY_ITEMS = """
    query($input: MonthInput!){
        myDailyAvailability(input: $input){
            day
            availabilities{
                startTime
                endTime
            }
        }
    }

"""
