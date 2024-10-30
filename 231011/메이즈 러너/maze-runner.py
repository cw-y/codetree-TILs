N, M, K = map(int, input().split())
game_map = [list(map(int, input().split())) for _ in range(N)]
gamer_loc = list()
for i in range(M):
    gamer_loc.append(list(map(int, input().split())))
exit = list(map(int, input().split()))
ans = 0
gamer_loc = [[a-1, b-1] for [a, b] in gamer_loc]
exit = [i-1 for i in exit]


# 최단거리 구하기
def get_shortest_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_real_distance(x1, y1, x2, y2):
    return ((abs(x1 - x2)**2) + (abs(y1 - y2)**2))**0.5


def get_square(x1, y1, x2, y2):
    r_di = abs(x1 - x2) + 1
    c_di = abs(y1 - y2) + 1
    min_r = min(x1, x2)
    min_c = min(y1, y2)
    if r_di > c_di:  # r이 정사각형 변의 길이가 된다.
        d = r_di
        r = min_r  # 이 부분 고침
        c = max(y1, y2) - r_di + 1
        if c < 0:
            c = 0
    else:  # c가 정사각형 변의 길이가 된다.
        d = c_di
        c = min_c
        r = max(x1, x2) - c_di + 1
        if r < 0:
            r = 0
    return r, c, d


out_man = 0
round_number = 0

# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 모두 탈출하지 않았으며, K초도 지나지 않은 한 실행하라
while gamer_loc and round_number < K:
    gi = 0
    for gamer in gamer_loc:
        x, y = gamer[0], gamer[1]  # 현재 참가자의 위치
        # 현재 최소 거리
        now_shortest_distance = get_shortest_distance(x, y, exit[0], exit[1])

        distances = []
        # 최단거리가 2개 이상이라면, 상하가 우선: 일치하는 가장 첫번째 원소 구하기
        for i in range(4):  # 0, 1, 2, 3
            # 런타임 에러1: 범위를 벗어나는 경우도 고려해야함
            if 0 <= x + dx[i] < N and 0 <= y + dy[i] < N:
                if not game_map[x + dx[i]][y + dy[i]] > 0:  # 벽이 아니다
                    new_distance = get_shortest_distance(x + dx[i], y + dy[i], exit[0], exit[1])
                    if new_distance < now_shortest_distance:
                        distances.append(i)
        if distances:  # 비어있지 않다면
            mindex = min(distances)
            x, y = x + dx[mindex], y + dy[mindex]
            gamer[0], gamer[1] = x, y
            ans += 1
            # print(ans)
    gamer_loc = [i for i in gamer_loc if not (i[0] == exit[0] and i[1] == exit[1])]
        # refactor: gamer를 순회하면서 일치하면 바로 삭제하도록 했으나, 그렇게 되면 뒤에 요소를 순회하지 못하고 넘어가는 일 발생
        # 따라서 출구 좌표와 일치하는 여부는 순회를 모두 마친 후 진행해줌!
        # gi += 1   => 앞에게 삭제되면 뒤에 요소는 순회를 못하게 됨

    di = []
    if gamer_loc:  # 참가자가 한 명이라도 남아있다면
        for gamer in gamer_loc:
            dis = []
    if gamer_loc:  # 참가자가 한 명이라도 남아있다면
        for gamer in gamer_loc:
            r, c, d = get_square(gamer[0], gamer[1], exit[0], exit[1])
            dis.append((r, c, d))

        dis.sort(key=lambda x: (x[2], x[0], x[1]))
        r = dis[0][0]
        c = dis[0][1]
        d = dis[0][2]

        for i in range(r, r + d):
            for j in range(c, c + d):
                if game_map[i][j] > 0:
                    game_map[i][j] -= 1

        new_map = [[0 for i in range(d)] for i in range(d)]
        for x in range(r, r + d):
            for y in range(c, c + d):
                ox, oy = x - r, y - c
                rx, ry = oy, d - ox - 1
                new_map[rx][ry] = game_map[x][y]

        for x in range(d):
            for y in range(d):
                game_map[r + x][c + y] = new_map[x][y]

        # 사람들 회전
        for i in range(len(gamer_loc)):
            if r <= gamer_loc[i][0] < r + d and c <= gamer_loc[i][1] < c + d:
                ox, oy = gamer_loc[i][0] - r, gamer_loc[i][1] - c
                rx, ry = oy, d - ox - 1
                gamer_loc[i] = [rx + r, ry + c]
        # 출구 회전
        ox, oy = exit[0] - r, exit[1] - c
        rx, ry = oy, d - ox - 1
        exit[0], exit[1] = rx + r, ry + c

    # list(zip(*reversed(?)))
    round_number += 1

print(ans)
print(exit[0]+1, exit[1]+1)