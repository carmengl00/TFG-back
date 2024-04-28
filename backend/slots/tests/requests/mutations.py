DELETE_RESERVED_SLOT = """
    mutation($id: UUID!){
        deleteReservedSlot(id: $id)
    }
"""