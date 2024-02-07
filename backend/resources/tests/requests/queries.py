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

DAY_AVAILABILITY_ITEMS = """
    query($pagination: PaginationInput!, $input: MonthInput!){
        myDailyAvailability(pagination: $pagination, input: $input){
            pageInfo{
                page
                pages
                totalResults
            }
            edges{
                id
                resource{
                    name
                }
                day
                startTime
                endTime
            }
        }
    }

"""
