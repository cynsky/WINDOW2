with open("layout_grid.dat", "w") as out:
    k = 0
    for i in range(11):
        for j in range(11):
            out.write("{} {} {}\n".format(k, i * 176.4, j * 176.4))
            k += 1
