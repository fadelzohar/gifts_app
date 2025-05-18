class layer_2_utility:
    # public
    layer_1 = None
    layer_2 = None
    building = None

    def __init__(self, _building: str, _layer_1: str, _layer_2: str):
        self.layer_1 = _layer_1
        self.layer_2 = _layer_2
        self.building = _building

    def extract(self):
        main_list = []
        for i in range(len(self.building)):
            for ii in range(len(self.building[i][self.layer_1])):
                main_list.extend(self.building[i][self.layer_1][ii][self.layer_2])
        return main_list


class layer_0_utility:
    # public
    building = None

    def __init__(self, _building):
        self.building = _building

    def remove_repeated(self) -> list:
        new_list = []
        for i in self.building:
            if i not in new_list:
                new_list.append(i)
        return new_list

    def create_layer_1(self) -> list:
        map = []
        for item_1 in range(len(self.building)):
            map.append({
                "item": self.building[item_1]
            })
        return map


class layer_1_utility:
    # public
    building = None
    layer_1 = None

    def __init__(self, _building, _layer_1):
        self.building = _building
        self.layer_1 = _layer_1

    def sorting(self):
        for n in range(len(self.building)):
            for nn in range(len(self.building) - 1):
                if self.building[nn][self.layer_1] >= self.building[nn + 1][self.layer_1]:
                    temp = self.building[nn]  # pos 1
                    self.building[nn] = self.building[nn + 1]  # pos2
                    self.building[nn + 1] = temp  # pos
        return self.building



    def extract(self) -> list:
        main_list = []
        for i in range(len(self.building)):
            main_list.extend(self.building[i][self.layer_1])
        return main_list

    def extract_as_list(self) -> list:
        main_list = []
        for item in range(len(self.building)):
            main_list.append(self.building[item][self.layer_1])
        return main_list

    def remove_repeated(self):
        #self.building.reverse()
        new_list = [i for n, i in enumerate(self.building) if
                    i.get(self.layer_1) not in [y.get(self.layer_1) for y in self.building[n + 1:]]]
        return new_list

    def remove_repeated_v2(self) -> list:
        mapp = []
        for item in range(len(self.building)):
            for item_2 in range(len(self.building)):
                if item < item_2:
                    if self.building[item][self.layer_1] == self.building[item_2][self.layer_1]:
                       mapp.append(self.building[item_2])
        return mapp

    def append_not_repeated(self):
        mapp = []
        callback = self.remove_repeated_v2()
        for item in range(len(self.building)):
            if self.building[item][self.layer_1] != self.layer_1:
                mapp.append(self.building[item])
        mapp.extend(callback)
        return mapp


    def find_frequency(self):
        for i in range(len(self.building)):
            self.building[i]['freq'] = 0
            for ii in range(len(self.building)):
                if self.building[i][self.layer_1] == self.building[ii][self.layer_1] and i <= ii:
                    self.building[i]['freq'] += 1
        return self.building


'''class layer_1_utility_value(layer_1_utility):

    # public
    val = None
    def __init__(self,_building, _layer_1, _val):
        layer_1_utility.__init__(self,_building, _layer_1)
        self.val = _val

    def find_where_value(self) -> dict:
        what_return = None
        for item in self.building:
            if item[self.layer_1] == self.val:
                what_return =             '''

data = [
    {
        'item': 1,
        'freq': 1
    },
    {
        'item': 1,
        'freq': 2
    },
    {
        "item": 2,
        "freq": 3
    }
]
ob = layer_1_utility(data,'item')
print(ob.building)
print((ob.remove_repeated()))
