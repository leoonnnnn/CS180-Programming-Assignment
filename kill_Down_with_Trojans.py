import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    memo = np.empty((n, n))
    memo[:] = np.nan                 # use np.nan as the null value

    print("\nmemo before:")      # COMMENT OUT!!!
    print(memo)                  # COMMENT OUT!!!
    res = H + DP_helper(memo, n, H, tile_types, tile_values, 0, 0)
    print("memo after:")         # COMMENT OUT!!!
    print(memo)                  # COMMENT OUT!!!
    print("Final hp: ", res)     # COMMENT OUT!!!
    return res >= 0


def DP_helper(memo, n, hp, tile_types, tile_values, x, y):  #add tokens later
    #BCs
    if x >= n or y >= n:    #out of bounds
        return -100000
    if hp < 0:
        return -123    # can't revive, so penalize reviving    #change to -100000

    type = 0
    if tile_types[x][y] == 0:
        type = -1        #take damage
        #print(x, y, "damage")
    elif tile_types[x][y] == 1:
        type = 1         #heal
        #print(x, y, "heal")
    #else:
        #maybe for token shit

    if x == n-1 and y == n-1:
        return tile_values[x][y] * type   # reached end
    if not np.isnan(memo[x][y]):
        return memo[x][y]

    #print(x, y, type, tile_values[x][y])
    #print(tile_types[x][y])    #wait this is actually useful lol, literally tells you the tile type
    curval = tile_values[x][y] * type
    hp += curval
    opt1 = DP_helper(memo, n, hp, tile_types, tile_values, x+1, y) + curval   # move down, lowkey just call it down and right instead of opt1 and opt2... (tho in future opts can also include using tokens :shrug:)
    opt2 = DP_helper(memo, n, hp, tile_types, tile_values, x, y+1) + curval    # move right
    memo[x][y] = max(opt1, opt2) 
    return max(opt1, opt2)   #test that it works by spitting out the max path sum


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
