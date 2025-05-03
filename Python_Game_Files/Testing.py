_OFFSETS = [(dx, dy) 
                for dx in (-1, 0, 1) 
                for dy in (-1, 0, 1) 
                if not (dx == 0 and dy == 0)]

for i in _OFFSETS:
    for j in i:
        print(j)
