class VertexMating():

    def __init__(self,first_fragment_id,first_vertex_i, second_fragment_id, second_vertex_i) -> None:
        self.first_fragment_id = first_fragment_id
        self.first_vertex_i = first_vertex_i
        self.second_fragment_id = second_fragment_id
        self.second_vertex_i = second_vertex_i

    def __repr__(self) -> str:
        return f"{self.first_fragment_id}_{self.first_vertex_i}<--->{self.second_fragment_id}_{self.second_vertex_i}"
    
    def __str__(self) -> str:
        return f"{self.first_fragment_id},{self.first_vertex_i},{self.second_fragment_id},{self.second_vertex_i}\r\n"
