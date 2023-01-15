def positionNodes(self):
    x_0_pos = (500, 500)
    add_and_multiply_0_pos = (x_0_pos[0] - add_and_multiply_0.width - 200, 500)
    number_node_0_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 50)
    number_node_1_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 100)
    number_node_2_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 150)
    # posiziona i nodi
    self.x_0.setPos(x_0_pos[0], x_0_pos[1])
    self.add_and_multiply_0.setPos(add_and_multiply_0_pos[0], add_and_multiply_0_pos[1])
    self.number_node_0.setPos(number_node_0_pos[0], number_node_0_pos[1])
    self.number_node_1.setPos(number_node_1_pos[0], number_node_1_pos[1])
    self.number_node_2.setPos(number_node_2_pos[0], number_node_2_pos[1])
    # continua con le altre righe del codice
