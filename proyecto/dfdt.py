import numpy as np
from scipy.constants import epsilon_0

__author__ = 'Mathias Lambert'


def dfdt(celdas_z, celdas_t, epsilon_r=1, sigma=0):
    ex = np.zeros((celdas_t, celdas_z))
    hy = np.zeros((celdas_t, celdas_z))
    dz = 0.01
    dt = dz / (6 * 10 ** 8)
    cte = dt * sigma / (2 * epsilon_r * epsilon_0)

    a = np.concatenate((np.ones((1, celdas_z // 3)),
                        np.ones((1, celdas_z // 3)) * ((1 - cte) / (1 + cte))
                        ), axis=1)

    a = np.concatenate((a,
                        np.ones((1, celdas_z // 3))), axis=1)

    b = np.concatenate((np.ones((1, celdas_z // 3)) * 0.5,
                        np.ones((1, celdas_z // 3)) * (0.5 / (epsilon_r * (1 + cte)))), axis=1)

    b = np.concatenate((b,
                        np.ones((1, celdas_z // 3)) * 0.5), axis=1)

    t0 = 80
    spread = 24
    exlm1 = 0
    exlm2 = 0
    exhm1 = 0
    exhm2 = 0
    t = 0
    for n in range(celdas_t - 1):
        t += 1
        ex[n + 1] = a * ex[n] - b * (hy[n] - np.concatenate(([hy[n, 0]], hy[n, :-1]), axis=0))

        pulso = np.cos(3 * np.pi * (t0 - t) / spread) * np.exp(-0.5 * ((t0 - t) / spread) ** 2)
        ex[n + 1, 1] += pulso
        ex[n + 1, 0] = exlm2
        exlm2 = exlm1
        exlm1 = ex[n + 1, 1]
        ex[n + 1, celdas_z - 1] = exhm2
        exhm2 = exhm1
        exhm1 = ex[n + 1, celdas_z - 2]

        hy[n + 1] = hy[n] - 0.5 * (np.concatenate((ex[n + 1, 1:], [ex[n + 1, -1]]), axis=0) - ex[n + 1])

    return ex, hy


if __name__ == "__main__":
    a, b = dfdt(200, 600)
    print(len(a))
    print(a[201])
