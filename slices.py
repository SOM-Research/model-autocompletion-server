def getSlices(string):
    s = string[1:(len(string)-1)]
    ss = list(s.split('['))
    slices = []
    for slice in ss:
        newSlice = slice.strip(' ').strip(',').strip(']')
        if not newSlice == '':
            slices.append(newSlice)
    return slices

def getElementsFromSlice(string):
    li = list(string.split(", ")) 
    return li 

    
def convertStringToSlices(string):
    slicesAsText = getSlices(string)
    #Eliminan los [] y se deja como un array cuyos componentes string estan separados por comas
    slicesAsListOfLists = []
    for sl in slicesAsText:
        elems = getElementsFromSlice(sl)
        #cada componente del array anterior puede tener una serie de elementos tipo 'elem1, elem2, elem3'...
        #aqui se eliminan las comas de cada una de las componentes del array, de modo que la componente se dividiria en otras 3 componentes: 'elem1', 'elem2', 'elem3'...
        slice = []
        for e in elems:
            slice.append(e)
        slicesAsListOfLists.append(slice)
    return slicesAsListOfLists
    
slices_as_string = '[[Supervisor], [Order, subordinate, create, assigned, history, status], [Worker, name]]'
slices = convertStringToSlices(slices_as_string)
#El contenido tras procesar la lista inicial es el siguiente
#[['Supervisor'], ['Order', 'subordinate', 'create', 'assigned', 'history', 'status'], ['Worker', 'name']]
for slice in slices:
    print('\n-> ', slice)