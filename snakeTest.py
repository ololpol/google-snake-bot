import main

move_order1 = 4*"U" + 4*"R" + 4*"D" + 4*"L"

main.display()
for i in move_order1:
    main.move(i, False)

