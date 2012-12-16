def cell_could_contain(cell, value):
    return cell & value

def get_row_ix(cell_ix):
    return cell_ix / 9

def get_col_ix(cell_ix):
    return cell_ix % 9

def get_box_ix(cell_ix):
    return ((cell_ix / 3) % 3) + ((cell_ix / 27) * 3)
