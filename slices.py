'''Given a string containing slices, we remove [] and get a list whose strings are separated by commas.'''
def get_slices(string):
    s = string[1:(len(string)-1)]
    ss = list(s.split('['))
    slices = []
    for slice in ss:
        new_slice = slice.strip(' ').strip(',').strip(']')
        if not new_slice == '':
            slices.append(new_slice)
    return slices

'''Given a string, we get the elements that are separated by commas.'''
def get_elements_from_slice(string):
    li = list(string.split(", ")) 
    return li 

'''We convert a string to a list of lists. We start deleting [] and from the array we get after deleting [] we split each element separated by commas and divide it into new components.
e.g. suppose we had an array with these elements: 'elem1, elem2, elem3' we split it and get another array containing: 'elem1', 'elem2', 'elem3'...'''    
def convert_string_to_slices(string):
    slices_as_text = get_slices(string)
    #Eliminan los [] y se deja como un array cuyos componentes string estan separados por comas
    slices_as_list_of_lists = []
    for sl in slices_as_text:
        elems = get_elements_from_slice(sl)
        #cada componente del array anterior puede tener una serie de elementos tipo 'elem1, elem2, elem3'...
        #aqui se eliminan las comas de cada una de las componentes del array, de modo que la componente se dividiria en otras 3 componentes: 'elem1', 'elem2', 'elem3'...
        slice = []
        for e in elems:
            slice.append(e)
        slices_as_list_of_lists.append(slice)
    return slices_as_list_of_lists
    
slices_as_string = '[[Supervisor], [Order, subordinate, create, assigned, history, status], [Worker, name]]'
slices = convert_string_to_slices(slices_as_string)
#After processing the initial list, we get:
#[['Supervisor'], ['Order', 'subordinate', 'create', 'assigned', 'history', 'status'], ['Worker', 'name']]
for slice in slices:
    print('\n-> ', slice)